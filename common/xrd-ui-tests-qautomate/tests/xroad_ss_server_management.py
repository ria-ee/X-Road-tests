# -*- coding: utf-8 -*-
from variables import strings
from webframework import TESTDATA
from webframework.extension.base.setupTest import SetupTest
from webframework.extension.util.common_utils import *
from pagemodel.open_application import Open_application
from common_lib.component_ss import Component_ss
from common_lib.common_lib import Common_lib
from common_lib.common_lib_ssh import Common_lib_ssh
from common_lib.component_ss_backup import Component_ss_backup
from common_lib.component_ss_sidebar import Component_ss_sidebar
from common_lib.component_ss_version import Component_ss_version
from pagemodel.ss_login import Ss_login
from pagemodel.ss_backup_restore import Ss_backup_restore
from pagemodel.ss_backup_restore_confirm_restore import Ss_backup_restore_confirm_restore
from common_lib.component_ss_keys_and_certs import Component_ss_keys_and_certs
from common_lib.component_common import Component_common

class Xroad_ss_server_management(SetupTest):
    """
    .. _document: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md
    .. _3.2: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md#32-uc-ss_01-log-in-to-the-graphical-user-interface
    .. _3.3: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md#33-uc-ss_02-log-out-of-the-graphical-user-interface
    .. _3.5: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md#35-uc-ss_04-change-the-graphical-user-interface-language
    .. _3.6: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md#36-uc-ss_05-view-the-installed-software-version
    .. _3.7: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md#37-uc-ss_06-view-timestamping-services
    .. _3.8: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md#38-uc-ss_07-add-a-timestamping-service
    .. _3.9: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md#39-uc-ss_08-delete-a-timestamping-service
    .. _3.10: https://github.com/ria-ee/X-Road/blob/develop/doc/UseCases/uc-ss_x-road_use_case_model_for_security_server_management_1.4_Y-883-4.md#310-uc-ss_09-view-certificate-details

    Xroad cases for security server management test cases

    Use cases `document`_

    **Use cases:**
        * `3.2`_: Log In to the Graphical User Interface
            * 3a: The system is currently undergoing the system restore process
            * 4a: The user with the inserted user name does not exist or the password is incorrect
        * `3.3`_: Log Out of the Graphical User Interface
        * `3.5`_: Change the Graphical User Interface Language
        * `3.6`_: View the Installed Software Version
        * `3.7`_: View Timestamping Services
        * `3.8`_: Add a Timestamping Service
            * 3a: SS administrator selected a timestamping service that already exists in the security server
        * `3.9`_: Delete a Timestamping Service
        * `3.10`_: View Certificate Details

    **Changelog:**
        * 20.09.2017
            | Links added to md use case documentation
        * 11.07.2017
            | Documentation updated
    """
    common_utils = CommonUtils()
    open_application = Open_application()
    component_ss = Component_ss()
    common_lib = Common_lib()
    common_lib_ssh = Common_lib_ssh()
    component_ss_backup = Component_ss_backup()
    component_ss_sidebar = Component_ss_sidebar()
    component_ss_version = Component_ss_version()
    ss_login = Ss_login()
    ss_backup_restore = Ss_backup_restore()
    ss_backup_restore_confirm_restore = Ss_backup_restore_confirm_restore()
    component_ss_keys_and_certs = Component_ss_keys_and_certs()
    component_common = Component_common()

    @classmethod
    def setUpTestSet(self):
        """
        Method that runs before every unittest

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.autogen_browser = self.Autogen_browser = self.common_utils`
        """
        self.autogen_browser = self.common_utils.open_browser()

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
                * **Step 1:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *u'ss1_url'*
                * **Step 2:** :func:`~pagemodel.start_log_time = self.Start_log_time = self.common_lib`
        """
        self.common_lib_ssh.empty_all_logs_from_server(u'ss1_url')
        self.start_log_time = self.common_lib.get_log_utc_time()
        self.restore_ss = False

    def tearDown(self):
        """
        Method that runs after every test case

        **Test steps:**
            * **Step 1: log out from system gui**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        stop_log_time = self.common_lib.get_log_utc_time()
        if not self.is_last_test_passed():
            self.common_lib_ssh.get_all_logs_from_server(u'ss1_url')
            _, copy_log = self.get_log_file_paths()
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, copy_log)

        error = ""

        if not self.ss_login.verify_is_login_page():
            # Step Log out from system GUI
            self.common_lib.log_out()

        if error:
            print(error)

    def test_login_and_logout_ss_gui(self):
        """
        Test case for logging in and logging out from security server qui

        **Use cases:**
            * `3.2`_: Log In to the Graphical User Interface
            * `3.3`_: Log Out of the Graphical User Interface

        **Test steps:**
            * **Step 1: open security server for login add user name password**
            * **Step 2: system verify's login success and log file**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
            * **Step 3: system logs the event "log in user" to the audit log**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'ss1_url'*, *strings.login_user*
            * **Step 4: log out from system gui**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 5: system logs the event “log out user” to the audit log.**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'ss1_url'*, *strings.logout_user*
        """
        # Step Open security server for login add user name password
        # Step System verify's login success and log file
        self.component_ss.login(u'ss1_url')

        # Step System logs the event "Log in user" to the audit log
        self.common_lib_ssh.verify_audit_log(u'ss1_url', strings.login_user)

        # Step Log out from system GUI
        self.common_lib.log_out()

        # Step System logs the event “Log out user” to the audit log.
        self.common_lib_ssh.verify_audit_log(u'ss1_url', strings.logout_user)

    def test_login_with_wrong_password(self):
        """
        Test case for logging in with wrong password

            **Use cases:**
                * `3.2`_: Log In to the Graphical User Interface
                    * 4a: The user with the inserted user name does not exist or the password is incorrect

        **Test steps:**
            * **Step 1: open security server the user with the inserted user name does not exist or the password is incorrect.**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'security_server_url_wrong_password'*, *initial_conf=True*, *wait_for_jquery=False*
            * **Step 2: system displays the error message “authentication failed”.**
                * :func:`~common_lib.component_ss.Component_ss.verify_login_fail`, *strings.authentication_failed*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'ss1_url'*, *strings.login_user_failed*
        """
        # Step Open security server The user with the inserted user name does not exist or the password is incorrect.
        self.component_ss.login(u'security_server_url_wrong_password', initial_conf=True, wait_for_jquery=False)
        # Step System displays the error message “Authentication failed”.
        self.component_ss.verify_login_fail(strings.authentication_failed)

        self.common_lib_ssh.verify_audit_log(u'ss1_url', strings.login_user_failed)

    def test_login_restore_back_up_in_process(self):
        """
        Test case for logging in during restore back up process

        **Use cases:**
            * `3.2`_: Log In to the Graphical User Interface
                * 3a: The system is currently undergoing the system restore process

        **Test steps:**
            * **Step 1: open security server for login add user name password**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*, *initial_conf=True*, *wait_for_jquery=False*
                * :func:`~common_lib.component_ss.Component_ss.verify_login_fail`, *strings.login_restore_in_progress*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'ss1_url'*, *strings.logout_user*
        """
        self.restore_backup_browser = self.common_utils.open_browser()
        self.component_ss.login(u'ss1_url')
        self.component_ss_sidebar.open_backup_restore_view()
        self.component_ss_backup.generate_backup()
        self.restore_ss = True
        self.ss_backup_restore.click_element_first_row_restore()
        self.ss_backup_restore_confirm_restore.click_button_confirm(False)

        self.common_utils.switch_browser(self.autogen_browser)
        # Step Open security server for login add user name password
        self.component_ss.login(u'ss1_url', initial_conf=True, wait_for_jquery=False)

        # The system is currently undergoing the system restore process.
        #3a.1. System displays the error message “Restore in progress, try again later”.
        self.component_ss.verify_login_fail(strings.login_restore_in_progress)
        #3a.2. System logs the event “Log out user” to the audit log.
        self.common_lib_ssh.verify_audit_log(u'ss1_url', strings.logout_user)

    def test_change_language(self):
        """
        Test case for changing qui language

        **Use cases:**
            * `3.5`_: Change the Graphical User Interface Language

        **Test steps:**
            * **Step 1: open security server for login add user name password**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
            * **Step 2: change language**
                * :func:`~common_lib.component_common.Component_common.open_select_language_dlg`
                * :func:`~common_lib.component_common.Component_common.change_language_in_dlg`, *strings.lanquage_eng*
                * :func:`~common_lib.component_common.Component_common.accept_select_language_dlg`
            * **Step 3: verify audit log for language change**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'ss1_url'*, *strings.set_ui_language*
        """
        # Step Open security server for login add user name password
        self.component_ss.login(u'ss1_url')

        # Step Change language
        self.component_common.open_select_language_dlg()
        self.component_common.change_language_in_dlg(strings.lanquage_eng)
        self.component_common.accept_select_language_dlg()

        # Step Verify audit log for language change
        self.common_lib_ssh.verify_audit_log(u'ss1_url', strings.set_ui_language)

    def test_view_installed_software_version(self):
        """
        Test case for viewing installed software version

        **Use cases:**
            * `3.6`_: View the Installed Software Version

        **Test steps:**
            * **Step 1: open security server for login add user name password**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
            * **Step 2: open version view**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_version_view`
            * **Step 3: verify version**
                * :func:`~common_lib.component_ss_version.Component_ss_version.verify_version`, *strings.security_server_version*
            * **Step 4: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Open security server for login add user name password
        self.component_ss.login(u'ss1_url')

        # Step Open version view
        self.component_ss_sidebar.open_version_view()

        # Step Verify version
        self.component_ss_version.verify_version(strings.security_server_version)

        # Step Log out
        self.common_lib.log_out()

    def test_timestamping_services(self):
        """
        Test case for time stamping services

        **Use cases:**
            * `3.7`_: View Timestamping Services
            * `3.8`_: Add a Timestamping Service
                * 3a: SS administrator selected a timestamping service that already exists in the security server
            * `3.9`_: Delete a Timestamping Service

        **Test steps:**
            * **Step 1: open security server for login add user name password**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_system_parameters_view`
            * **Step 2: delete timestamp services**
                * :func:`~common_lib.component_ss.Component_ss.delete_timestamping_url_from_ss`, *u'cs_url'*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'ss1_url'*, *strings.delete_timestamping_services*
            * **Step 3: add timestamp services**
                * :func:`~common_lib.component_ss.Component_ss.add_timestamping_url_to_ss`, *u'cs_url'*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'ss1_url'*, *strings.add_timestamping_services*
            * **Step 4: add timestamp services fail**
                * :func:`~common_lib.component_ss.Component_ss.add_timestamping_url_to_ss`, *u'cs_url'*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'ss1_url'*, *strings.add_timestamping_services_failed*
            * **Step 5: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Add timestamping service, view timestamping service, try add existing tsp service and delete tsp service
        # Step Open security server for login add user name password
        self.component_ss.login(u'ss1_url')
        self.component_ss_sidebar.open_system_parameters_view()

        # Step Delete timestamp services
        self.component_ss.delete_timestamping_url_from_ss(u'cs_url')
        self.common_lib_ssh.verify_audit_log(u'ss1_url', strings.delete_timestamping_services)

        # Step Add timestamp services
        self.component_ss.add_timestamping_url_to_ss(u'cs_url')
        self.common_lib_ssh.verify_audit_log(u'ss1_url', strings.add_timestamping_services)

        # Step Add timestamp services fail
        self.component_ss.add_timestamping_url_to_ss(u'cs_url')
        self.common_lib_ssh.verify_audit_log(u'ss1_url', strings.add_timestamping_services_failed)

        # Step Log out
        self.common_lib.log_out()

    def test_view_certificate_details(self):
        """
        Test case for viewing certificate details

        **Use cases:**
            * `3.10`_: View Certificate Details

        **Test steps:**
            * **Step 1: open security server for login add user name password**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*, *False*, *True*
            * **Step 2: view certificate details**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_details_dlg`
            * **Step 3: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Open security server for login add user name password
        self.component_ss.login(u'ss1_url', False, True)

        # Step View certificate details
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.verify_details_dlg()

        # Step Log out
        self.common_lib.log_out()

    def test_open_multiple_diagnostics_simultaneously(self):
        """
        Test case for opening multiple diagnostic views simultaneosly

        **Test steps:**
                * **Step 1:** :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*, *False*, *True*
                * **Step 2:** :func:`~pagemodel.autogen_browser2 = self.Autogen_browser2 = self.common_utils`
                * **Step 3:** :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*, *False*, *True*
                * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.switch_browser`, *self.autogen_browser*
                * **Step 5:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_diagnostics_view`
                * **Step 6:** :func:`~webframework.extension.util.common_utils.CommonUtils.switch_browser`, *self.autogen_browser2*
                * **Step 7:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_diagnostics_view`
                * **Step 8:** :func:`~webframework.extension.util.common_utils.CommonUtils.close_browser`
                * **Step 9:** :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        self.component_ss.login(u'ss1_url', False, True)
        self.autogen_browser2 = self.common_utils.open_browser()
        self.component_ss.login(u'ss1_url', False, True)

        self.common_utils.switch_browser(self.autogen_browser)
        self.component_ss_sidebar.open_diagnostics_view()

        self.common_utils.switch_browser(self.autogen_browser2)
        self.component_ss_sidebar.open_diagnostics_view()
        self.common_utils.close_browser()

        self.common_lib.log_out()
