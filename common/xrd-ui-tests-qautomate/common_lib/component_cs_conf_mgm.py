# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.cs_conf_mgm_external import Cs_conf_mgm_external
from pagemodel.cs_conf_mgm import Cs_conf_mgm
from pagemodel.cs_conf_mgm_internal_new_key import Cs_conf_mgm_internal_new_key
from pagemodel.cs_conf_mgm_enter_pin import Cs_conf_mgm_enter_pin
from pagemodel.cs_conf_mgm_delete_confirm_dlg import Cs_conf_mgm_delete_confirm_dlg
from pagemodel.cs_conf_mgm_activate_confirm_dlg import Cs_conf_mgm_activate_confirm_dlg

class Component_cs_conf_mgm(CommonUtils):
    """
    Components common to central server conf management view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    cs_conf_mgm_external = Cs_conf_mgm_external()
    cs_conf_mgm = Cs_conf_mgm()
    cs_conf_mgm_internal_new_key = Cs_conf_mgm_internal_new_key()
    cs_conf_mgm_enter_pin = Cs_conf_mgm_enter_pin()
    cs_conf_mgm_delete_confirm_dlg = Cs_conf_mgm_delete_confirm_dlg()
    cs_conf_mgm_activate_confirm_dlg = Cs_conf_mgm_activate_confirm_dlg()

    def download_source_anchor_from_cs(self):
        """
        Donwload source anchor from central server

        *Updated: 11.07.2017*
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_download_source_anchor`
        """
        self.cs_conf_mgm.click_button_id_download_source_anchor()

    def generate_new_internal_config_key_in_cs(self):
        """
        Generate new internal configuration key in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_generate_signing_key`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm_internal_new_key.Cs_conf_mgm_internal_new_key.click_button_ok`
        """
        self.cs_conf_mgm.click_button_id_generate_signing_key()
        self.cs_conf_mgm_internal_new_key.click_button_ok()

    def generate_new_external_config_key_in_cs(self):
        """
        Generate new external configuration key in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_link_external_configuration`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm_external.Cs_conf_mgm_external.click_button_id_generate_signing_key`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm_internal_new_key.Cs_conf_mgm_internal_new_key.click_button_ok`
        """
        self.cs_conf_mgm.click_link_external_configuration()
        self.cs_conf_mgm_external.click_button_id_generate_signing_key()
        self.cs_conf_mgm_internal_new_key.click_button_ok()

    def try_insert_pin_code(self, section=u'cs_url'):
        """
        Try inserting pin code to token in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm_enter_pin.Cs_conf_mgm_enter_pin.input_text_to_id_activate_token_pin`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm_enter_pin.Cs_conf_mgm_enter_pin.click_button_ok`
        """
        # Sometimes it will not ask pin code, recovery added
        try:
            self.cs_conf_mgm_enter_pin.input_text_to_id_activate_token_pin(TESTDATA[section])
            self.cs_conf_mgm_enter_pin.click_button_ok()
        except:
            print("Pin code query not prompted this time")
        sleep(2)

    def insert_pin_from_login_button(self, section=u'cs_url'):
        """
        Login to token in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_login`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_element_ok_pin_login_button`
        """
        self.cs_conf_mgm.click_element_login()
        self.try_insert_pin_code(section)
        self.cs_conf_mgm.click_element_ok_pin_login_button()

    def verify_external_configuration_view(self):
        """
        Verify external configuration view

        *Updated: 11.07.2017*

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

        *Updated: 11.07.2017*

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

    def recreate_source_anchor_from_cs(self):
        """
        Recreate source anchor from central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_generate_source_anchor`
        """
        self.cs_conf_mgm.click_button_id_generate_source_anchor()

    def logout_signing_key(self):
        """
        Logout signing key

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_logout`
        """
        self.cs_conf_mgm.click_button_logout()

    def activate_newest_signing_key(self):
        """
        Activate newest signing key

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_newest_signing_key`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_activate_signing_key`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm_activate_confirm_dlg.Cs_conf_mgm_activate_confirm_dlg.click_confirm`
        """
        self.cs_conf_mgm.click_newest_signing_key()
        self.cs_conf_mgm.click_button_id_activate_signing_key()
        self.cs_conf_mgm_activate_confirm_dlg.click_confirm()

    def activate_oldest_signing_key(self):
        """
        Activate oldest signing key

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_oldest_signing_key`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_activate_signing_key`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm_activate_confirm_dlg.Cs_conf_mgm_activate_confirm_dlg.click_confirm`
        """
        self.cs_conf_mgm.click_oldest_signing_key()
        self.cs_conf_mgm.click_button_id_activate_signing_key()
        self.cs_conf_mgm_activate_confirm_dlg.click_confirm()

    def delete_newest_signing_key(self):
        """
        Delete newest signing key

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_newest_signing_key`
                * **Step 2:** :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_button_id_delete_signing_key`
                * **Step 3:** :func:`~pagemodel.cs_conf_mgm_delete_confirm_dlg.Cs_conf_mgm_delete_confirm_dlg.click_confirm`
        """
        self.cs_conf_mgm.click_newest_signing_key()
        self.cs_conf_mgm.click_button_id_delete_signing_key()
        self.cs_conf_mgm_delete_confirm_dlg.click_confirm()
