# -*- coding: utf-8 -*-
import glob
import os

from variables import strings
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.cs_conf_mgm_external import Cs_conf_mgm_external
from pagemodel.cs_conf_mgm import Cs_conf_mgm
from pagemodel.cs_conf_mgm_internal_new_key import Cs_conf_mgm_internal_new_key
from pagemodel.cs_conf_mgm_enter_pin import Cs_conf_mgm_enter_pin
from pagemodel.cs_conf_mgm_delete_confirm_dlg import Cs_conf_mgm_delete_confirm_dlg
from pagemodel.cs_conf_mgm_activate_confirm_dlg import Cs_conf_mgm_activate_confirm_dlg
from pagemodel.cs_conf_upload_configuration_part import Cs_conf_upload_configuration_part
from common_lib import Common_lib
from common_lib_ssh import Common_lib_ssh
from component_common import Component_common

class Component_cs_conf_mgm(CommonUtils):
    """
    Components common to central server conf management view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    cs_conf_mgm_external = Cs_conf_mgm_external()
    cs_conf_mgm = Cs_conf_mgm()
    cs_conf_mgm_internal_new_key = Cs_conf_mgm_internal_new_key()
    cs_conf_mgm_enter_pin = Cs_conf_mgm_enter_pin()
    cs_conf_mgm_delete_confirm_dlg = Cs_conf_mgm_delete_confirm_dlg()
    cs_conf_mgm_activate_confirm_dlg = Cs_conf_mgm_activate_confirm_dlg()
    common_lib = Common_lib()
    common_lib_ssh = Common_lib_ssh()
    component_common = Component_common()
    cs_conf_upload_configuration_part = Cs_conf_upload_configuration_part()

    def download_source_anchor_from_cs(self):
        """
        Donwload source anchor from central server

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_download_source_anchor`
        """
        self.cs_conf_mgm.click_button_id_download_source_anchor()

    def generate_config_key(self, key_type=u'internal'):
        """
        Generate new internal configuration key in central server

        **Test steps:**
            * **Step 1: generate config key**
                * :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_generate_signing_key`
                * :func:`~pagemodel.cs_conf_mgm_internal_new_key.Cs_conf_mgm_internal_new_key.click_button_ok`
            * **Step 2: verify config generation audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.generate_config_signing_key.format(key_type*
        """
        # Step Generate config key
        self.cs_conf_mgm.click_button_id_generate_signing_key()
        self.cs_conf_mgm_internal_new_key.click_button_ok()
        # Step Verify config generation audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.generate_config_signing_key.format(key_type))

        self.wait_until_jquery_ajax_loaded()

    def generate_config_key_not_logged_in(self, section=u'cs_url', key_type=u'internal'):
        """
        
        :param section:  Test data section name
        
        **Test steps:**
            * **Step 1: insert pin**
                * :func:`~pagemodel.cs_conf_mgm_enter_pin.Cs_conf_mgm_enter_pin.verify_pin_dialog_is_open`
            * **Step 2: verify config generation audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.generate_config_signing_key.format(key_type*
        """
        # Generate config key
        self.cs_conf_mgm.click_button_id_generate_signing_key()
        self.cs_conf_mgm_internal_new_key.click_button_ok()
        self.wait_until_jquery_ajax_loaded()

        # Step Insert pin
        self.cs_conf_mgm_enter_pin.verify_pin_dialog_is_open()
        self.try_insert_pin_code(section)

        self.wait_until_jquery_ajax_loaded()

        # Step Verify config generation audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.generate_config_signing_key.format(key_type))

    def try_insert_pin_code(self, section=u'cs_url'):
        """
        Try inserting pin code to token in central server

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm_enter_pin.Cs_conf_mgm_enter_pin.input_text_to_id_activate_token_pin`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm_enter_pin.Cs_conf_mgm_enter_pin.click_button_ok`
        """
        # Sometimes it will not ask pin code, recovery added
        try:
            self.cs_conf_mgm_enter_pin.input_text_to_id_activate_token_pin(TESTDATA[section])
            self.cs_conf_mgm_enter_pin.click_button_ok()
            self.wait_until_jquery_ajax_loaded()
        except:
            print("Pin code query not prompted this time")

    def log_in_to_software_token(self, section=u'cs_url'):
        """
        Login to token in central server

        :param section:  Test data section name
        
        **Test steps:**
            * **Step 1: login to software token**
                * :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_login`
            * **Step 2: verify log in token audit log audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.login_token*
        """
        # Step Login to software token
        self.cs_conf_mgm.click_element_login()
        self.wait_until_jquery_ajax_loaded()

        self.cs_conf_mgm_enter_pin.input_text_to_id_activate_token_pin(TESTDATA[section])
        self.cs_conf_mgm_enter_pin.click_button_ok()
        self.wait_until_jquery_ajax_loaded()

        # Step Verify log in token audit log audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.login_token)

    def log_in_to_software_token_invalid_pin(self, section=u'invalid_cs_url'):
        """
        Login to token in central server

        :param section:  Test data section name
        
        **Test steps:**
            * **Step 1: login to software token**
                * :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_login`
            * **Step 2: verify log in token invalid pin audit log audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.login_token_failed*
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.login_software_token_invalid_pin*
            * **Step 3: close login dialog**
                * :func:`~pagemodel.cs_conf_mgm_enter_pin.Cs_conf_mgm_enter_pin.close_dialog`
        """
        # Step Login to software token
        self.cs_conf_mgm.click_element_login()
        self.wait_until_jquery_ajax_loaded()

        self.cs_conf_mgm_enter_pin.input_text_to_id_activate_token_pin(TESTDATA[section])
        self.cs_conf_mgm_enter_pin.click_button_ok()
        self.wait_until_jquery_ajax_loaded()

        # Step Verify log in token invalid pin audit log audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.login_token_failed)
        self.component_common.verify_notice_message(message=strings.login_software_token_invalid_pin)

        # Step Close login dialog
        self.cs_conf_mgm_enter_pin.close_dialog()

    def log_in_to_software_token_empty_pin(self, section=u'invalid_cs_url'):
        """
        Login to token in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
            * **Step 1: login to software token**
                * :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_login`
            * **Step 2: verify log in token invalid pin audit log audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.login_token_failed*
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.login_software_token_missing_pin*
            * **Step 3: close login dialog**
                * :func:`~pagemodel.cs_conf_mgm_enter_pin.Cs_conf_mgm_enter_pin.close_dialog`
        """
        # Step Login to software token
        self.cs_conf_mgm.click_element_login()
        self.wait_until_jquery_ajax_loaded()

        self.cs_conf_mgm_enter_pin.input_text_to_id_activate_token_pin(TESTDATA[section])
        self.cs_conf_mgm_enter_pin.click_button_ok()
        self.wait_until_jquery_ajax_loaded()

        # Step Verify log in token invalid pin audit log audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.login_token_failed)
        self.component_common.verify_notice_message(message=strings.login_software_token_missing_pin)

        # Step Close login dialog
        self.cs_conf_mgm_enter_pin.close_dialog()

    def verify_external_configuration_view(self):
        """
        Verify external configuration view

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_link_external_configuration`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_hash_value_is_visible`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_date_time_is_visible`
                * **Step 4:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_download_url_contains`, *"/externalconf"*
                * **Step 5:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_signing_keys`
                * **Step 6:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_conf_parts`
        """
        self.cs_conf_mgm.click_link_external_configuration()
        sleep(1)
        self.cs_conf_mgm.verify_hash_value_is_visible()
        self.cs_conf_mgm.verify_date_time_is_visible()
        self.cs_conf_mgm.verify_download_url_contains("/externalconf")
        self.cs_conf_mgm.verify_signing_keys()
        self.cs_conf_mgm.verify_conf_parts()

    def verify_internal_configuration_view(self):
        """
        Verify internal configuration view

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_link_internal_configuration`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_hash_value_is_visible`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_date_time_is_visible`
                * **Step 4:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_download_url_contains`, *"/internalconf"*
                * **Step 5:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_signing_keys`
                * **Step 6:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.verify_conf_parts`
        """
        self.cs_conf_mgm.click_link_internal_configuration()
        sleep(1)
        self.cs_conf_mgm.verify_hash_value_is_visible()
        self.cs_conf_mgm.verify_date_time_is_visible()
        self.cs_conf_mgm.verify_download_url_contains("/internalconf")
        self.cs_conf_mgm.verify_signing_keys()
        self.cs_conf_mgm.verify_conf_parts()

    def recreate_source_anchor_from_cs(self, key_type=u'internal'):
        """
        Recreate source anchor from central server

        **Test steps:**
            * **Step 1: generate source anchor**
                * :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_generate_source_anchor`
            * **Step 2: verify notice message**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.internal_conf_anchor_generated_success*
            * **Step 3: verify audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.recreate_configuration_anchor.format(key_type*
        """
        # Step Generate source anchor
        self.cs_conf_mgm.click_button_id_generate_source_anchor()
        # Step Verify notice message
        self.component_common.verify_notice_message(message=strings.internal_conf_anchor_generated_success)
        # Step Verify audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.recreate_configuration_anchor.format(key_type))

    def logout_software_token(self):
        """
        Logout signing key

        **Test steps:**
            * **Step 1:**
                * :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_logout`
            * **Step 2: verify log out token audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.logout_token*
        """
        # Step
        self.cs_conf_mgm.click_button_logout()
        # Step Verify log out token audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.logout_token)

    def activate_newest_signing_key(self, key_type=u'internal'):
        """
        Activate newest signing key

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_newest_signing_key`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_activate_signing_key`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm_activate_confirm_dlg.Cs_conf_mgm_activate_confirm_dlg.click_confirm`
                * **Step 4:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.activate_config_signing_key.format(key_type*
        """
        self.cs_conf_mgm.click_newest_signing_key()
        self.cs_conf_mgm.click_button_id_activate_signing_key()
        self.cs_conf_mgm_activate_confirm_dlg.click_confirm()

        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.activate_config_signing_key.format(key_type))

        self.wait_until_jquery_ajax_loaded()

    def activate_oldest_signing_key(self):
        """
        Activate oldest signing key

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_oldest_signing_key`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_activate_signing_key`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm_activate_confirm_dlg.Cs_conf_mgm_activate_confirm_dlg.click_confirm`
        """
        self.cs_conf_mgm.click_oldest_signing_key()
        self.cs_conf_mgm.click_button_id_activate_signing_key()
        self.cs_conf_mgm_activate_confirm_dlg.click_confirm()

        self.wait_until_jquery_ajax_loaded()

    def delete_newest_signing_key(self, key_type=u'internal'):
        """
        Delete newest signing key

        **Test steps:**
            * **Step 1: verify delete signing key audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.delete_config_signing_key.format(key_type*
            * **Step 2: verify delete messages**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.internal_conf_anchor_generated_success*
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.token_key_removed*
        """
        # Delete newest signing key
        self.cs_conf_mgm.click_newest_signing_key()
        self.cs_conf_mgm.click_button_id_delete_signing_key()
        self.cs_conf_mgm_delete_confirm_dlg.click_confirm()

        # Step Verify delete signing key audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.delete_config_signing_key.format(key_type))
        # Step Verify delete messages
        self.component_common.verify_notice_message(message=strings.internal_conf_anchor_generated_success)
        self.component_common.verify_notice_message(message=strings.token_key_removed)

        self.wait_until_jquery_ajax_loaded()

    def delete_signing_key_fail(self, key="", key_type=u'internal'):
        """
        Delete newest signing key

        **Test steps:**
            * **Step 1: delete signing key**
                * :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_newest_signing_key`
                * :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_delete_signing_key`
                * :func:`~pagemodel.cs_conf_mgm_delete_confirm_dlg.Cs_conf_mgm_delete_confirm_dlg.click_confirm`
            * **Step 2: verify delete signing key audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.delete_config_signing_key.format(key_type*
            * **Step 3: verify delete messages**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.internal_conf_anchor_generated_success*
                * :func:`~common_lib.component_common.Component_common.verify_error_message`, *message=strings.token_key_removed_fail.format("softToken-0"*, *key*
        """
        # Step delete signing key
        self.cs_conf_mgm.click_newest_signing_key()
        self.cs_conf_mgm.click_button_id_delete_signing_key()
        self.cs_conf_mgm_delete_confirm_dlg.click_confirm()

        # Step Verify delete signing key audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.delete_config_signing_key.format(key_type))
        # Step Verify delete messages
        self.component_common.verify_notice_message(message=strings.internal_conf_anchor_generated_success)
        self.component_common.verify_error_message(message=strings.token_key_removed_fail.format("softToken-0", key))

        self.wait_until_jquery_ajax_loaded()

    def generate_conf_part_file(self, part_file="test.ini", identifier="FOO", file_name="foo.xml", val_program=""):
        """
        Generate configuration file

        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.generate_and_write_to_file_as_xroad`, *"cs_url"*, *configuration_part_path*, *init_content*
        """
        configuration_part_path = os.path.join(strings.configuration_parts_directory, part_file)

        init_content = "content-identifier = {}\n".format(identifier)
        init_content += "file-name = {}\n".format(file_name)
        if val_program:
            init_content += "validation-program = {}".format(val_program)
        self.common_lib_ssh.generate_and_write_to_file_as_xroad("cs_url", configuration_part_path, init_content)

        self.reload_page()
        self.wait_until_jquery_ajax_loaded()

    def delete_conf_part_file(self, part_file):
        """
        Delete configuration part file

        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.delete_file`, *"cs_url"*, *configuration_part_path*
        """
        configuration_part_path = os.path.join(strings.configuration_parts_directory, part_file)
        self.common_lib_ssh.delete_file("cs_url", configuration_part_path)

    def download_configuration_part_file(self, identifier):
        """
        Donwload configuration part file
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_from_table_conf_parts`, *identifier*
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_download`
        """
        self.cs_conf_mgm.click_element_from_table_conf_parts(identifier)
        self.cs_conf_mgm.click_download()

        download_path = os.path.join(TESTDATA[u'paths'][u'downloads_folder'], '*.xml')
        downloaded_xml_file = glob.glob(download_path)
        newest_file = max(downloaded_xml_file, key=os.path.getctime)
        print(newest_file)

        self.reload_page()
        self.wait_until_jquery_ajax_loaded()

    def upload_configuration_part_file(self, identifier="FOO", path="downloads"):
        """
        Upload configuration part file

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_from_table_conf_parts`, *identifier*
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_conf_upload`
                * **Step 3:** :func:`~pagemodel.cs_conf_upload_configuration_part.Cs_conf_upload_configuration_part.click_browse`
                * **Step 4:** :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *path*
                * **Step 5:** :func:`~pagemodel.cs_conf_upload_configuration_part.Cs_conf_upload_configuration_part.click_ok`
                * **Step 6:** :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.configuration_file_upload.format(identifier*
                * **Step 7:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *strings.configuration_part_upload_audit_log*
        """
        self.cs_conf_mgm.click_element_from_table_conf_parts(identifier)
        self.cs_conf_mgm.click_conf_upload()
        self.cs_conf_upload_configuration_part.click_browse()

        self.common_lib.type_file_name_pyautogui(path)
        self.cs_conf_upload_configuration_part.click_ok()

        self.component_common.verify_notice_message(strings.configuration_file_upload.format(identifier))
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.configuration_part_upload_audit_log)

        self.reload_page()
        self.wait_until_jquery_ajax_loaded()

    def upload_conf_part_validation_fail(self, identifier="FOO", path="downloads"):
        """
        Upload configuration part file with fail

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_from_table_conf_parts`, *identifier*
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_conf_upload`
                * **Step 3:** :func:`~pagemodel.cs_conf_upload_configuration_part.Cs_conf_upload_configuration_part.click_browse`
                * **Step 4:** :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *path*
                * **Step 5:** :func:`~pagemodel.cs_conf_upload_configuration_part.Cs_conf_upload_configuration_part.click_ok`
                * **Step 6:** :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.configuration_file_upload_validation_fail.format(identifier*
                * **Step 7:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *strings.failed_configuration_part_upload_audit_log*
                * **Step 8:** :func:`~pagemodel.cs_conf_upload_configuration_part.Cs_conf_upload_configuration_part.click_close`
        """
        self.cs_conf_mgm.click_element_from_table_conf_parts(identifier)
        self.cs_conf_mgm.click_conf_upload()
        self.cs_conf_upload_configuration_part.click_browse()
        self.common_lib.type_file_name_pyautogui(path)
        self.cs_conf_upload_configuration_part.click_ok()
        # Has to sleep for
        sleep(3)
        self.component_common.verify_notice_message(strings.configuration_file_upload_validation_fail.format(identifier))
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.failed_configuration_part_upload_audit_log)
        self.cs_conf_upload_configuration_part.click_close()

        self.reload_page()
        self.wait_until_jquery_ajax_loaded()

    def upload_conf_part_validation_fail_missing_validation(self, identifier="FOO", path="downloads", validation_file="validation.sh"):
        """
        Upload configuration part file with fail

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_from_table_conf_parts`, *identifier*
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_conf_upload`
                * **Step 3:** :func:`~pagemodel.cs_conf_upload_configuration_part.Cs_conf_upload_configuration_part.click_browse`
                * **Step 4:** :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *path*
                * **Step 5:** :func:`~pagemodel.cs_conf_upload_configuration_part.Cs_conf_upload_configuration_part.click_ok`
                * **Step 6:** :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.configuration_file_upload_missing_validation_fail.format(validation_file*
                * **Step 7:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *strings.failed_configuration_part_upload_audit_log*
                * **Step 8:** :func:`~pagemodel.cs_conf_upload_configuration_part.Cs_conf_upload_configuration_part.click_close`
        """
        self.cs_conf_mgm.click_element_from_table_conf_parts(identifier)
        self.cs_conf_mgm.click_conf_upload()
        self.cs_conf_upload_configuration_part.click_browse()
        self.common_lib.type_file_name_pyautogui(path)
        self.cs_conf_upload_configuration_part.click_ok()
        # Has to sleep for
        sleep(3)
        self.component_common.verify_notice_message(strings.configuration_file_upload_missing_validation_fail.format(validation_file))
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.failed_configuration_part_upload_audit_log)
        self.cs_conf_upload_configuration_part.click_close()

        self.reload_page()
        self.wait_until_jquery_ajax_loaded()
