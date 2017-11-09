# -*- coding: utf-8 -*-
from variables import strings
from webframework import TESTDATA
from webframework.extension.base.setupTest import SetupTest
from webframework.extension.parsers.parameter_parser import get_all_parameters
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.open_application import Open_application
from pagemodel.ss_login import Ss_login
from common_lib.common_lib import Common_lib
from common_lib.component_cs import Component_cs
from common_lib.component_common import Component_common
from common_lib.common_lib_ssh import Common_lib_ssh
from common_lib.component_cs_conf_mgm import Component_cs_conf_mgm
from common_lib.component_cs_sidebar import Component_cs_sidebar
from common_lib.component_cs_system_settings import Component_cs_system_settings

class Xroad_global_configuration(SetupTest):
    """
    .. _document: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md
    .. _2.2.1: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#221-uc-gconf_01-view-a-configuration-source
    .. _2.2.2: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#222-uc-gconf_02-download-a-configuration-source-anchor-file
    .. _2.2.3: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#223-uc-gconf_03-re-create-a-configuration-source-anchor
    .. _2.2.7: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#227-uc-gconf_07-log-in-to-a-software-security-token
    .. _2.2.9: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#229-uc-gconf_09-log-out-of-a-software-security-token
    .. _2.2.11: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#2211-uc-gconf_11-add-a-configuration-source-signing-key
    .. _2.2.12: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#2212-uc-gconf_12-activate-a-configuration-source-signing-key
    .. _2.2.13: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#2213-uc-gconf_13-delete-a-configuration-source-signing-key
    .. _2.2.14: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#2214-uc-gconf_14-view-system-parameters
    .. _2.2.15: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-gconf_x-road_use_case_model_for_global_configuration_distribution_1.4_Y-883-8.md#2215-uc-gconf_15-edit-the-address-of-the-central-server

    Xroad cases for global configurations

    Use cases `document`_

    **Use cases:**
        * `2.2.1`_: View a Configuration Source
        * `2.2.2`_: Download a Configuration Source Anchor File
        * `2.2.3`_: Re-Create a Configuration Source Anchor
        * `2.2.7`_: Log In to a Software Security Token
        * `2.2.9`_: Log Out of a Software Security Token
        * `2.2.11`_: Add a Configuration Source Signing Key
        * `2.2.12`_: Activate a Configuration Source Signing Key
            * 3a: CS administrator cancels the key activation
        * `2.2.13`_: Delete a Configuration Source Signing Key
            * 3a: CS administrator cancels the key deletion
        * `2.2.14`_: View System Parameters
        * `2.2.15`_: Edit the Address of the Central Server
            * 3a: The parsing of the user input terminated with an error message
            * 4a: The inserted address is not valid

    **Changelog:**
        * 20.09.2017
            | Links added to md use case documentation
        * 11.07.2017
            | Documentation updated
    """
    common_utils = CommonUtils()
    open_application = Open_application()
    ss_login = Ss_login()
    common_lib = Common_lib()
    component_cs = Component_cs()
    component_common = Component_common()
    common_lib_ssh = Common_lib_ssh()
    component_cs_conf_mgm = Component_cs_conf_mgm()
    component_cs_sidebar = Component_cs_sidebar()
    component_cs_system_settings = Component_cs_system_settings()

    @classmethod
    def setUpTestSet(self):
        """
        Method that runs before every unittest

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.autogen_browser = self.Autogen_browser = self.common_utils`
        """
        self.autogen_browser = self.common_utils.open_browser()
        # Opens to second monitor for testing
        #driver = self.common_utils.driver_cache._get_current_driver()
        #driver.set_window_position(2000, 0)
        #driver.maximize_window()

    @classmethod
    def tearDownTestSet(self):
        """
        Method that runs after every unittest

        **Test steps:**
                * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.close_all_browsers`
        """
        self.common_utils.close_all_browsers()

    def setUp(self):
        """
        Method that runs before every test case

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.start_log_time = self.Start_log_time = self.common_lib`
                * **Step 2:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"ss1_url"*
                * **Step 3:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"cs_url"*
        """
        self.start_log_time = self.common_lib.get_log_utc_time()
        self.common_lib_ssh.empty_all_logs_from_server("ss1_url")
        self.common_lib_ssh.empty_all_logs_from_server("cs_url")

    def tearDown(self):
        """
        Method that runs after every test case

        **Test steps:**
            * **Step 1: log out if logged in**
                * :func:`~pagemodel.open_application.Open_application.open_application_url`, *TESTDATA[u'cs_url']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        stop_log_time = self.common_lib.get_log_utc_time()
        if not self.is_last_test_passed():
            _, copy_log = self.get_log_file_paths()
            self.common_lib_ssh.get_all_logs_from_server(u'ss1_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'ss1_url', copy_log)
            self.common_lib_ssh.get_all_logs_from_server(u'cs_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'cs_url', copy_log)

        # Step log out if logged in
        if not self.ss_login.verify_is_login_page():
            self.open_application.open_application_url(TESTDATA[u'cs_url'])
            self.common_lib.log_out()

    def test_global_configuration_view_source(self):
        """
        Test case for viewing global configuration view source

        **Use cases:**
            * `2.2.1`_: View a Configuration Source

        **Test steps:**
            * **Step 1: login to central server and open configuration view**
                * :func:`~common_lib.component_cs.Component_cs.login`, *section=u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
            * **Step 2: verify displayed information internalconf**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.verify_internal_configuration_view`
            * **Step 3: verify displayed information externalconf**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.verify_external_configuration_view`
            * **Step 4: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server and open configuration view
        self.component_cs.login(section=u'cs_url')
        self.component_cs_sidebar.open_global_configuration_view()

        # Step Verify displayed information internalconf
        self.component_cs_conf_mgm.verify_internal_configuration_view()

        # Step Verify displayed information externalconf
        self.component_cs_conf_mgm.verify_external_configuration_view()

        # Step Log out
        self.common_lib.log_out()

    def test_global_configuration_download_and_recreate(self):
        """
        Test case for downloading source anchor and recreating it

        **Use cases:**
            * `2.2.2`_: Download a Configuration Source Anchor File
            * `2.2.3`_: Re-Create a Configuration Source Anchor

        **Test steps:**
            * **Step 1: login to central server and open configuration view**
                * :func:`~common_lib.component_cs.Component_cs.login`, *section=u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
            * **Step 2: download configuration source anchor**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.download_source_anchor_from_cs`
            * **Step 3: recreate configuration source anchor**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.recreate_source_anchor_from_cs`
            * **Step 4: verify notice message**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.internal_conf_anchor_generated_success*
            * **Step 5: verify audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.recreate_internal_configuration_anchor*
            * **Step 6: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server and open configuration view
        self.component_cs.login(section=u'cs_url')
        self.component_cs_sidebar.open_global_configuration_view()

        # Step Download configuration source anchor
        self.component_cs_conf_mgm.download_source_anchor_from_cs()

        # Step Recreate configuration source anchor
        self.component_cs_conf_mgm.recreate_source_anchor_from_cs()

        # Step Verify notice message
        self.component_common.verify_notice_message(message=strings.internal_conf_anchor_generated_success)

        # Step Verify audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.recreate_internal_configuration_anchor)

        # Step Log out
        self.common_lib.log_out()

    def test_login_and_log_out_software_security_token(self):
        """
        Test case for logging in and logging out software security token

        **Use cases:**
            * `2.2.7`_: Log In to a Software Security Token
            * `2.2.9`_: Log Out of a Software Security Token

        **Test steps:**
            * **Step 1: login to central server and open configuration view**
                * :func:`~common_lib.component_cs.Component_cs.login`, *section=u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
            * **Step 2: log out token**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.logout_signing_key`
            * **Step 3: verify log out token audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.logout_token*
            * **Step 4: log in token**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.insert_pin_from_login_button`, *section=u'cs_url'*
            * **Step 5: verify log in audit log audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.login_token*
            * **Step 6: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server and open configuration view
        self.component_cs.login(section=u'cs_url')
        self.component_cs_sidebar.open_global_configuration_view()

        # Step Log out token
        self.component_cs_conf_mgm.logout_signing_key()

        # Step Verify log out token audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.logout_token)

        # Step Log in token
        self.component_cs_conf_mgm.insert_pin_from_login_button(section=u'cs_url')

        # Step Verify log in audit log audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.login_token)

        # Step Log out
        self.common_lib.log_out()

    def test_activate_and_delete_config_signing_key(self):
        """
        Test case for activating and deleting config signing key

        **Use cases:**
            * `2.2.12`_: Activate a Configuration Source Signing Key
               * 3a: CS administrator cancels the key activation
            * `2.2.13`_: Delete a Configuration Source Signing Key
                * 3a: CS administrator cancels the key deletion

        **Test steps:**
            * **Step 1: login to central server and open configuration view**
                * :func:`~common_lib.component_cs.Component_cs.login`, *section=u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
            * **Step 2: generate signing key**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.generate_new_internal_config_key_in_cs`
            * **Step 3: verify config generation audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.generate_internal_config_signing_key*
            * **Step 4: activate signing_key**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.activate_newest_signing_key`
            * **Step 5: verify active signing key audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.activate_internal_config_signing_key*
            * **Step 6: activate old signing key**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.activate_oldest_signing_key`
            * **Step 7: delete signing key**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.delete_newest_signing_key`
            * **Step 8: verify delete signing key audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.delete_internal_config_signing_key*
            * **Step 9: verify delete messages**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.internal_conf_anchor_generated_success*
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.token_key_removed*
            * **Step 10: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server and open configuration view
        self.component_cs.login(section=u'cs_url')
        self.component_cs_sidebar.open_global_configuration_view()

        # Step Generate signing key
        self.component_cs_conf_mgm.generate_new_internal_config_key_in_cs()
        # Step Verify config generation audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.generate_internal_config_signing_key)

        # Step Activate signing_key
        self.component_cs_conf_mgm.activate_newest_signing_key()
        # Step Verify active signing key audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.activate_internal_config_signing_key)

        # Step Activate old signing key
        self.component_cs_conf_mgm.activate_oldest_signing_key()

        # Step Delete signing key
        self.component_cs_conf_mgm.delete_newest_signing_key()
        # Step Verify delete signing key audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.delete_internal_config_signing_key)
        # Step Verify delete messages
        self.component_common.verify_notice_message(message=strings.internal_conf_anchor_generated_success)
        self.component_common.verify_notice_message(message=strings.token_key_removed)

        # Step Log out
        self.common_lib.log_out()

    def test_generate_config_signing_key(self):
        """
        Test case for generating config signing key

        **Use cases:**
            * `2.2.11`_: Add a Configuration Source Signing Key

        **Test steps:**
            * **Step 1: login to central server and open configuration view**
                * :func:`~common_lib.component_cs.Component_cs.login`, *section=u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
            * **Step 2: generate signing key**
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.generate_new_internal_config_key_in_cs`
            * **Step 3: verify config generation audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.generate_internal_config_signing_key*
            * **Step 4: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server and open configuration view
        self.component_cs.login(section=u'cs_url')
        self.component_cs_sidebar.open_global_configuration_view()

        # Step Generate signing key
        self.component_cs_conf_mgm.generate_new_internal_config_key_in_cs()
        # Step Verify config generation audit log
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.generate_internal_config_signing_key)

        # Step Log out
        self.common_lib.log_out()

    def test_view_sys_param_and_edit_address_of_cs(self):
        """
        Test case for viewing system parameters and editing address of central server

        **Use cases:**
            * `2.2.14`_: View System Parameters
            * `2.2.15`_: Edit the Address of the Central Server
                * 3a: The parsing of the user input terminated with an error message
                * 4a: The inserted address is not valid

        **Test steps:**
            * **Step 1: login to central server and open system settings**
                * :func:`~common_lib.component_cs.Component_cs.login`, *section=u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_system_settings_view`
            * **Step 2: change central server url**
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.change_server_address`, *u'new_cs_url'*
            * **Step 3: verify edit cs address**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.edit_cs_address*
            * **Step 4: change central server url invalid**
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.change_server_address`, *u'invalid_cs_url'*
            * **Step 5: verify edit cs address failed**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.edit_cs_address_failed*
            * **Step 6: verify address must be dns**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.change_address_error*
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.cancel_server_address_dlg`
            * **Step 7: change central server url invalid**
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.change_server_address`, *section=u'invalid_cs_url'*
            * **Step 8: verify edit cs address failed**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.edit_cs_address_failed*
            * **Step 9: verify address must be dns**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *message=strings.change_address_error*
            * **Step 10: input valid adress**
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.input_server_address_in_dlg`, *section=u'cs_url'*
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.confirm_server_address_dlg`
            * **Step 11: verify edit cs address**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *section=u'cs_url'*, *event=strings.edit_cs_address*
            * **Step 12: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server and open system settings
        self.component_cs.login(section=u'cs_url')
        self.component_cs_sidebar.open_system_settings_view()

        # Step Change central server url
        self.component_cs_system_settings.change_server_address(u'new_cs_url')
        # Step Verify edit cs address
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.edit_cs_address)

        # Step Change central server url invalid
        self.component_cs_system_settings.change_server_address(u'invalid_cs_url')
        # Step Verify edit cs address failed
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.edit_cs_address_failed)
        # Step Verify address must be dns
        self.component_common.verify_notice_message(message=strings.change_address_error)
        self.component_cs_system_settings.cancel_server_address_dlg()

        # Step Change central server url invalid
        self.component_cs_system_settings.change_server_address(section=u'invalid_cs_url')
        # Step Verify edit cs address failed
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.edit_cs_address_failed)
        # Step Verify address must be dns
        self.component_common.verify_notice_message(message=strings.change_address_error)
        # Step Input valid adress
        self.component_cs_system_settings.input_server_address_in_dlg(section=u'cs_url')
        self.component_cs_system_settings.confirm_server_address_dlg()
        # Step Verify edit cs address
        self.common_lib_ssh.verify_audit_log(section=u'cs_url', event=strings.edit_cs_address)

        # Step Log out
        self.common_lib.log_out()
