# -*- coding: utf-8 -*-
from variables import strings
from webframework import TESTDATA
from webframework.extension.base.setupTest import SetupTest
from webframework.extension.util.common_utils import *
from pagemodel.open_application import Open_application
from common_lib.component_cs import Component_cs
from common_lib.common_lib import Common_lib
from common_lib.component_common import Component_common
from common_lib.common_lib_ssh import Common_lib_ssh
from common_lib.component_cs_sidebar import Component_cs_sidebar
from common_lib.component_cs_version import Component_component_cs_version
from pagemodel.cs_backup_restore import Cs_backup_restore
from common_lib.component_cs_backup import Component_cs_backup
from pagemodel.cs_login import Cs_login

class Xroad_cs_server_management(SetupTest):
    """
    .. _document: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md
    .. _2.5: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#25-uc-cs_04-change-the-graphical-user-interface-language
    .. _2.6: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#26-uc-cs_05-view-the-installed-software-version
    .. _2.7: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#27-uc-cs_06-view-the-list-of-configuration-backup-files
    .. _2.8: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#28-uc-cs_07-back-up-configuration
    .. _2.9: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#29-uc-cs_08-restore-configuration-from-a-backup-file
    .. _2.10: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#210-uc-cs_09-download-a-backup-file
    .. _2.11: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#211-uc-cs_10-delete-a-backup-file
    .. _2.12: https://github.com/vrk-kpa/X-Road/blob/develop/doc/UseCases/uc-cs_x-road_use_case_model_for_central_server_management_1.2_Y-883-6.md#212-uc-cs_11-upload-a-backup-file

    Xroad cases for central management test cases

    Use cases `document`_

    **Use cases:**
        * `2.5`_: Change the Graphical User Interface Language
        * `2.6`_: View the Installed Software Version
        * `2.7`_: View the List of Configuration Backup Files
        * `2.8`_: Back Up Configuration
            * 3a. Backing up the central server configuration failed.
        * `2.9`_: Restore Configuration from a Backup File
            * 3a. CS administrator cancels the restoring of the configuration from the backup file.
            * 4a. Restoring the central server configuration failed.
        * `2.10`_: Download a Backup File
        * `2.11`_: Delete a Backup File
            * 3a. CS administrator cancels the deleting of the backup file.
        * `2.12`_: Upload a Backup File
            * 3a. The file name contains invalid characters.
            * 4a. The file extension is not .tar.
            * 5a. The content of the file is not in valid format.
            * 6a. A backup file with the same file name is saved in the system configuration.

    **Changelog:**
        * 19.10.2017
            | All cases done
        * 15.09.2017
            | Test set created and cases + documentation links added
    """
    common_utils = CommonUtils()
    open_application = Open_application()
    component_cs = Component_cs()
    common_lib = Common_lib()
    component_common = Component_common()
    common_lib_ssh = Common_lib_ssh()
    component_cs_sidebar = Component_cs_sidebar()
    component_cs_version = Component_component_cs_version()
    cs_backup_restore = Cs_backup_restore()
    component_cs_backup = Component_cs_backup()
    cs_login = Cs_login()

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
                * **Step 1:** :func:`~pagemodel.start_log_time = self.Start_log_time = self.common_lib`
                * **Step 2:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"cs_url"*
        """
        self.start_log_time = self.common_lib.get_log_utc_time()
        self.common_lib_ssh.empty_all_logs_from_server("cs_url")

    def tearDown(self):
        """
        Method that runs after every test case

        **Test steps:**
            * **Step 1: find exceptions from log files**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.get_all_logs_from_server`, *u'cs_url'*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.find_exception_from_logs_and_save`
            * **Step 2: log out if logged in**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 3: return server to defaults**
                * :func:`~common_lib.common_lib.Common_lib.delete_files_with_extension`, *TESTDATA.get_parameter(u'paths'*, *u'downloads_folder'*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.delete_files_from_directory`, *u'cs_url'*, *strings.backup_directory*
        """
        # Step Find exceptions from log files
        stop_log_time = self.common_lib.get_log_utc_time()
        if not self.is_last_test_passed():
            _, copy_log = self.get_log_file_paths()
            self.common_lib_ssh.get_all_logs_from_server(u'cs_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time,
                                                                  u'cs_url', copy_log)

        # Step log out if logged in
        if not self.cs_login.verify_is_login_page():
            self.common_lib.log_out()

        # Step Return server to defaults
        self.common_lib.delete_files_with_extension(TESTDATA.get_parameter(u'paths', u'downloads_folder'), u'.tar')
        self.common_lib_ssh.delete_files_from_directory(u'cs_url', strings.backup_directory)

    def test_change_the_graphical_user_interface_language(self):
        """
        Test case for changeing the graphical user interface language

        **Use cases:**
            * `2.5`_: Change the Graphical User Interface Language

        **Test steps:**
            * **Step 1: open central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *False*
            * **Step 2: change language**
                * :func:`~common_lib.component_common.Component_common.open_select_language_dlg`
                * :func:`~common_lib.component_common.Component_common.change_language_in_dlg`, *strings.lanquage_eng*
                * :func:`~common_lib.component_common.Component_common.accept_select_language_dlg`
            * **Step 3: verify audit log for language change**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *strings.set_ui_language*
            * **Step 4: log out of central server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Open central server
        self.component_cs.login(u'cs_url', False)

        # Step Change language
        self.component_common.open_select_language_dlg()
        self.component_common.change_language_in_dlg(strings.lanquage_eng)
        self.component_common.accept_select_language_dlg()

        # Step Verify audit log for language change
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.set_ui_language)

        # Step Log out of central server
        self.common_lib.log_out()

    def test_view_the_installed_software_version(self):
        """
        Test case for viewing the installed software version

        **Use cases:**
            * `2.6`_: View the Installed Software Version

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *False*
            * **Step 2: open version view**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_version_view`
            * **Step 3: verify version**
                * :func:`~common_lib.component_cs_version.Component_cs_version.verify_version`, *u'Central Server version 6'*
            * **Step 4: log out of central server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step login to central server
        self.component_cs.login(u'cs_url', False)

        # Step open version view
        self.component_cs_sidebar.open_version_view()

        # Step verify version
        self.component_cs_version.verify_version(u'Central Server version 6')

        # Step log out of central server
        self.common_lib.log_out()

    def test_view_backup_list(self):
        """
        Test case view list of configuration back up files

        **Use cases:**
            * `2.7`_: View the List of Configuration Backup Files

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *False*
            * **Step 2: open backup view**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
            * **Step 3: generate backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 4: verify backup view user actions**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.verify_contains_all_user_actions`
            * **Step 5: log out of central server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url', False)

        # Step Open backup view
        self.component_cs_sidebar.open_backup_restore_view()

        # Step Generate backup
        self.component_cs_backup.generate_backup()

        # Step Verify backup view user actions
        self.cs_backup_restore.verify_contains_all_user_actions()

        # Step Log out of central server
        self.common_lib.log_out()

    def test_backup_configuration(self):
        """
        Test generate backup

        **Use cases:**
            * `2.8`_: Back Up Configuration
                * 3a. Backing up the central server configuration failed.

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *False*
            * **Step 2: open backup view**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
            * **Step 3: generate backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_invalid_backup`
            * **Step 4: generate backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 5: log out of central server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url', False)

        # Step Open backup view
        self.component_cs_sidebar.open_backup_restore_view()

        # Step Generate backup
        self.component_cs_backup.generate_invalid_backup()

        # Step Generate backup
        self.component_cs_backup.generate_backup()

        # Step Log out of central server
        self.common_lib.log_out()

    def test_restore_backup(self):
        """
        Test restore backup

        **Use cases:**
            * `2.9`_: Restore Configuration from a Backup File
                * 3a. CS administrator cancels the restoring of the configuration from the backup file.
                * 4a. Restoring the central server configuration failed.

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *False*
            * **Step 2: open backup view**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
            * **Step 3: restore invalid backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.restore_invalid_backup`
            * **Step 4: generate backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 5: cancel restore backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.cancel_restore_backup`
            * **Step 6: restore backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.restore_backup`
            * **Step 7: log out of central server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url', False)

        # Step Open backup view
        self.component_cs_sidebar.open_backup_restore_view()

        # Step Restore invalid backup
        self.component_cs_backup.restore_invalid_backup()

        # Step Generate backup
        self.component_cs_backup.generate_backup()

        # Step Cancel restore backup
        self.component_cs_backup.cancel_restore_backup()

        # Step Restore backup
        self.component_cs_backup.restore_backup()

        # Step Log out of central server
        self.common_lib.log_out()

    def test_download_backup(self):
        """
        Test download backup

        **Use cases:**
            * `2.10`_: Download a Backup File

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *False*
            * **Step 2: open backup view**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
            * **Step 3: generate backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 4: download backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.download_backup`
            * **Step 5: log out of central server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url', False)

        # Step Open backup view
        self.component_cs_sidebar.open_backup_restore_view()

        # Step Generate backup
        self.component_cs_backup.generate_backup()

        # Step Download backup
        self.component_cs_backup.download_backup()

        # Step Log out of central server
        self.common_lib.log_out()

    def test_delete_backup(self):
        """
        Test delete backup

        **Use cases:**
            * `2.11`_: Delete a Backup File
                * 3a. CS administrator cancels the deleting of the backup file.

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *False*
            * **Step 2: open backup view**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
            * **Step 3: generate backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 4: cancel delete backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.cancel_delete_backup`
            * **Step 5: delete backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.delete_backup`
            * **Step 6: log out of central server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url', False)

        # Step Open backup view
        self.component_cs_sidebar.open_backup_restore_view()

        # Step Generate backup
        self.component_cs_backup.generate_backup()

        # Step Cancel delete backup
        self.component_cs_backup.cancel_delete_backup()

        # Step Delete backup
        self.component_cs_backup.delete_backup()

        # Step Log out of central server
        self.common_lib.log_out()

    def test_upload_backup(self):
        """
        Test upload backup

        **Use cases:**
            * `2.12`_: Upload a Backup File
                * 3a. The file name contains invalid characters.
                * 4a. The file extension is not .tar.
                * 5a. The content of the file is not in valid format.
                * 6a. A backup file with the same file name is saved in the system configuration.

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *False*
            * **Step 2: open backup view**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
            * **Step 3: generate backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 4: download backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.download_backup`
            * **Step 5: delete backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.delete_backup`
            * **Step 6: upload backup**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.upload_backup`
            * **Step 7: upload backup that already exists**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.upload_backup_already_exists`
            * **Step 8: upload backup with invalid characters in name**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.upload_backup_invalid_char`
            * **Step 9: upload backup with invalid extension**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.upload_backup_invalid_extension`
            * **Step 10: upload backup with invalid format**
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.upload_backup_invalid_format`
            * **Step 11: log out of central server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url', False)

        # Step Open backup view
        self.component_cs_sidebar.open_backup_restore_view()

        # Step Generate backup
        self.component_cs_backup.generate_backup()

        # Step Download backup
        self.component_cs_backup.download_backup()

        # Step Delete backup
        self.component_cs_backup.delete_backup()

        # Step Upload backup
        self.component_cs_backup.upload_backup()

        # Step Upload backup that already exists
        self.component_cs_backup.upload_backup_already_exists()

        # Step Upload backup with invalid characters in name
        self.component_cs_backup.upload_backup_invalid_char()

        # Step Upload backup with invalid extension
        self.component_cs_backup.upload_backup_invalid_extension()

        # Step Upload backup with invalid format
        self.component_cs_backup.upload_backup_invalid_format()

        # Step Log out of central server
        self.common_lib.log_out()
