# -*- coding: utf-8 -*-
from variables import strings
from webframework import TESTDATA
from webframework.extension.base.baseTest import BaseTest
from webframework.extension.parsers.parameter_parser import get_all_parameters
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib.component_cs_sidebar import Component_cs_sidebar
from common_lib.common_lib import Common_lib
from common_lib.common_lib_ssh import Common_lib_ssh
from common_lib.component_cs_mgm_requests import Component_cs_mgm_requests
from common_lib.component_cs_backup import Component_cs_backup
from common_lib.component_cs_sec_servers import Component_cs_sec_servers
from common_lib.component_cs import Component_cs
from common_lib.component_cs_members import Component_cs_members
from common_lib.component_ss import Component_ss
from common_lib.component_ss_backup import Component_ss_backup
from common_lib.component_ss_sidebar import Component_ss_sidebar
from common_lib.component_ss_keys_and_certs import Component_ss_keys_and_certs
from common_lib.component_cs_conf_mgm import Component_cs_conf_mgm
from common_lib.component_ss_clients import Component_ss_clients
from pagemodel.ss_clients import Ss_clients
from pagemodel.ss_login import Ss_login
from pagemodel.cs_login import Cs_login

class Xroad_deletion_of_registered_object(BaseTest):
    """
    Xroad cases for deleting registered objects

    **Changelog:**
        * 11.07.2017
            | Documentation updated
    """
    common_utils = CommonUtils()
    component_cs_sidebar = Component_cs_sidebar()
    common_lib = Common_lib()
    common_lib_ssh = Common_lib_ssh()
    component_cs_mgm_requests = Component_cs_mgm_requests()
    component_cs_backup = Component_cs_backup()
    component_cs_sec_servers = Component_cs_sec_servers()
    component_cs = Component_cs()
    component_cs_members = Component_cs_members()
    component_ss = Component_ss()
    component_ss_backup = Component_ss_backup()
    component_ss_sidebar = Component_ss_sidebar()
    component_ss_keys_and_certs = Component_ss_keys_and_certs()
    component_cs_conf_mgm = Component_cs_conf_mgm()
    component_ss_clients = Component_ss_clients()
    ss_clients = Ss_clients()
    cs_login = Cs_login()
    ss_login = Ss_login()

    @classmethod
    def setUpTestSet(self):
        """
        Method that runs before every unittest

        *Updated: 11.07.2017*
        """
        pass

    @classmethod
    def tearDownTestSet(self):
        """
        Method that runs after every unittest

        *Updated: 11.07.2017*
        """
        pass

    def setUp(self):
        """
        Method that runs before every test case

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 3:** :func:`~pagemodel.start_log_time = self.Start_log_time = self.common_lib`
                * **Step 4:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"ss1_url"*
                * **Step 5:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"cs_url"*
        """
        self.restore_ss = False
        self.restore_cs = False
        self.start_log_time = self.common_lib.get_log_utc_time()
        self.common_lib_ssh.empty_all_logs_from_server("ss1_url")
        self.common_lib_ssh.empty_all_logs_from_server("cs_url")

    def tearDown(self):
        """
        Method that runs after every test case

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: restore central server backup in central server if needed**
                * :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.restore_backup`
            * **Step 2: restore security server in security server if needed**
                * :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss1_url']['url']*
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * :func:`~common_lib.component_ss_backup.Component_ss_backup.restore_backup`
            * **Step 3: log out from security if logged in**
                * :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss1_url']['url']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 4: log out from central server if logged in**
                * :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 5: return server to defaults**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.delete_files_from_directory`, *u'cs_url'*, *strings.backup_directory*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.delete_files_from_directory`, *u'ss1_url'*, *strings.backup_directory*
        """
        stop_log_time = self.common_lib.get_log_utc_time()
        if not self.is_last_test_passed():
            _, copy_log = self.get_log_file_paths()
            self.common_lib_ssh.get_all_logs_from_server(u'ss1_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'ss1_url', copy_log)
            self.common_lib_ssh.get_all_logs_from_server(u'cs_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'cs_url', copy_log)

        # Step Restore central server backup in central server if needed
        if self.restore_cs:
            print("tearDown_restore_cs")
            self.common_utils.open_url(TESTDATA[u'cs_url']['url'])
            self.component_cs_sidebar.open_backup_restore_view()
            self.component_cs_backup.restore_backup()

        # Step Restore security server in security server if needed
        if self.restore_ss:
            print("tearDown_restore_ss")
            self.common_utils.open_url(TESTDATA[u'ss1_url']['url'])
            self.component_ss_sidebar.open_backup_restore_view()
            self.component_ss_backup.restore_backup()

        # Step Log out from security if logged in
        self.common_utils.open_url(TESTDATA[u'ss1_url']['url'])
        if not self.ss_login.verify_is_login_page():
            self.common_lib.log_out()

        # Step Log out from central server if logged in
        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])
        if not self.cs_login.verify_is_login_page():
            self.common_lib.log_out()

        # Step Return server to defaults
        self.common_lib_ssh.delete_files_from_directory(u'cs_url', strings.backup_directory)
        self.common_lib_ssh.delete_files_from_directory(u'ss1_url', strings.backup_directory)

    def test_deletion_of_the_owner_of_ss_from_cs(self):
        """
        Test case for deleting owner of security server from central server

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
            * **Step 2: generate central server backup in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 3: delete member from cs with ss in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.open_member_details_dlg`, *u'member1_configuration'*, *u'member_name'*
                * :func:`~common_lib.component_cs_members.Component_cs_members.delete_member_in_member_details_dlg`
            * **Step 4: verify members is removed in central server**
                * :func:`~common_lib.component_cs_members.Component_cs_members.verify_members_does_not_contain_member`, *u'member1_configuration'*, *u'member_name'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_security_servers_view`
                * :func:`~common_lib.component_cs_sec_servers.Component_cs_sec_servers.verify_servers_does_not_contain_server`, *u'member1_configuration'*, *u'member_name'*
            * **Step 5: verify request comment in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_management_request_view`
                * :func:`~common_lib.component_cs_mgm_requests.Component_cs_mgm_requests.open_request_details_dlg`, *strings.request_cert_deletion*
                * :func:`~common_lib.component_cs_mgm_requests.Component_cs_mgm_requests.verify_comment_in_request_details_dlg`, *request_comment*
                * :func:`~common_lib.component_cs_mgm_requests.Component_cs_mgm_requests.close_request_details_dlg`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url')

        # Step Generate central server backup in central server
        self.component_cs_sidebar.open_backup_restore_view()
        self.component_cs_backup.generate_backup()
        self.restore_cs = True

        # Step Delete member from cs with ss in central server
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.open_member_details_dlg(u'member1_configuration',  u'member_name')
        self.component_cs_members.delete_member_in_member_details_dlg()

        # Step Verify members is removed in central server
        self.component_cs_members.verify_members_does_not_contain_member(u'member1_configuration', u'member_name')
        self.component_cs_sidebar.open_security_servers_view()
        self.component_cs_sec_servers.verify_servers_does_not_contain_server(u'member1_configuration', u'member_name')

        # Step Verify request comment in central server
        request_comment = strings.server_request_comment(u'member1_configuration')
        self.component_cs_sidebar.open_management_request_view()
        self.component_cs_mgm_requests.open_request_details_dlg(strings.request_cert_deletion)
        self.component_cs_mgm_requests.verify_comment_in_request_details_dlg(request_comment)
        self.component_cs_mgm_requests.close_request_details_dlg()

    def test_deletion_of_xroad_member_from_cs(self):
        """
        Test case for deleting xroad member from central server

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
            * **Step 2: generate central server backup in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 3: delete member from cs in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.open_member_details_dlg`, *u'member1_configuration'*, *u'member_name'*
                * :func:`~common_lib.component_cs_members.Component_cs_members.delete_member_in_member_details_dlg`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url')

        # Step Generate central server backup in central server
        self.component_cs_sidebar.open_backup_restore_view()
        self.component_cs_backup.generate_backup()
        self.restore_cs = True

        # Step Delete member from cs in central server
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.open_member_details_dlg(u'member1_configuration', u'member_name')
        self.component_cs_members.delete_member_in_member_details_dlg()

    def test_deletion_of_ss_from_cs(self):
        """
        Test case for deleting security server from security server

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
            * **Step 2: generate central server backup in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 3: delete security server in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_security_servers_view`
                * :func:`~common_lib.component_cs_sec_servers.Component_cs_sec_servers.open_server_details_dlg`, *u'member1_configuration'*, *u'security_server_code'*
                * :func:`~common_lib.component_cs_sec_servers.Component_cs_sec_servers.delete_server_in_server_details_dlg`
            * **Step 4: verify member subsystem state in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.open_member_details_dlg`, *u'member1_configuration'*, *u'member_name'*
                * :func:`~common_lib.component_cs_members.Component_cs_members.verify_subsystem_is_removable_in_member_details_dlg`, *u'member1_configuration'*, *u'subsystem_code'*
                * :func:`~common_lib.component_cs_members.Component_cs_members.close_member_details_dlg`
            * **Step 5: verify request comment in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_management_request_view`
                * :func:`~common_lib.component_cs_mgm_requests.Component_cs_mgm_requests.open_request_details_dlg`, *strings.request_cert_deletion*
                * :func:`~common_lib.component_cs_mgm_requests.Component_cs_mgm_requests.verify_comment_in_request_details_dlg`, *request_comment*
                * :func:`~common_lib.component_cs_mgm_requests.Component_cs_mgm_requests.close_request_details_dlg`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url')

        # Step Generate central server backup in central server
        self.component_cs_sidebar.open_backup_restore_view()
        self.component_cs_backup.generate_backup()
        self.restore_cs = True

        # Step Delete security server in central server
        self.component_cs_sidebar.open_security_servers_view()
        self.component_cs_sec_servers.open_server_details_dlg(u'member1_configuration', u'security_server_code')
        self.component_cs_sec_servers.delete_server_in_server_details_dlg()

        # Step Verify member subsystem state in central server
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.open_member_details_dlg(u'member1_configuration', u'member_name')
        self.component_cs_members.verify_subsystem_is_removable_in_member_details_dlg(u'member1_configuration', u'subsystem_code')
        self.component_cs_members.close_member_details_dlg()

        # Step Verify request comment in central server
        self.component_cs_sidebar.open_management_request_view()
        request_comment = strings.server_request_comment(u'member1_configuration')
        self.component_cs_mgm_requests.open_request_details_dlg(strings.request_cert_deletion)
        self.component_cs_mgm_requests.verify_comment_in_request_details_dlg(request_comment)
        self.component_cs_mgm_requests.close_request_details_dlg()

    def test_deletion_of_client_of_ss_from_cs(self):
        """
        Test case for deleting client of security server from central server

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
            * **Step 2: generate backup in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 3: delete server client in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_security_servers_view`
                * :func:`~common_lib.component_cs_sec_servers.Component_cs_sec_servers.open_server_details_dlg`, *u'member1_configuration'*, *u'security_server_code'*
                * :func:`~common_lib.component_cs_sec_servers.Component_cs_sec_servers.delete_client_in_server_details_dlg`, *u'member1_configuration'*
                * :func:`~common_lib.component_cs_sec_servers.Component_cs_sec_servers.close_server_details_dlg`
            * **Step 4: verify member subsystem state in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.open_member_details_dlg`, *'member1_configuration'*, *u'member_name'*
                * :func:`~common_lib.component_cs_members.Component_cs_members.verify_subsystem_is_removable_in_member_details_dlg`, *u'member1_configuration'*, *u'subsystem_code'*
                * :func:`~common_lib.component_cs_members.Component_cs_members.close_member_details_dlg`
            * **Step 5: verify reguest comment in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_management_request_view`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url')

        # Step Generate backup in central server
        self.component_cs_sidebar.open_backup_restore_view()
        self.component_cs_backup.generate_backup()
        self.restore_cs = True

        # Step Delete server client in central server
        self.component_cs_sidebar.open_security_servers_view()
        self.component_cs_sec_servers.open_server_details_dlg(u'member1_configuration', u'security_server_code')
        self.component_cs_sec_servers.delete_client_in_server_details_dlg(u'member1_configuration')
        self.component_cs_sec_servers.close_server_details_dlg()

        # Step Verify member subsystem state in central server
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.open_member_details_dlg('member1_configuration', u'member_name')
        self.component_cs_members.verify_subsystem_is_removable_in_member_details_dlg(u'member1_configuration', u'subsystem_code')
        self.component_cs_members.close_member_details_dlg()

        # Step Verify reguest comment in central server
        request_comment = strings.server_request_comment(u'member1_configuration')
        self.component_cs_sidebar.open_management_request_view()

    def test_deletion_of_authentication_certificate_from_cs(self):
        """
        Test case for deleting authentication of certificate from central server

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
            * **Step 2: generate backup in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 3: delete security server auth cert in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_security_servers_view`
                * :func:`~common_lib.component_cs_sec_servers.Component_cs_sec_servers.open_server_details_dlg`, *u'member1_configuration'*, *u'member_name'*
                * :func:`~common_lib.component_cs_sec_servers.Component_cs_sec_servers.delete_auth_cert_in_server_details_dlg`
                * :func:`~common_lib.component_cs_sec_servers.Component_cs_sec_servers.close_server_details_dlg`
            * **Step 4: verify reguest comment in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_management_request_view`
                * :func:`~common_lib.component_cs_mgm_requests.Component_cs_mgm_requests.open_request_details_dlg`, *strings.request_cert_deletion*
                * :func:`~common_lib.component_cs_mgm_requests.Component_cs_mgm_requests.verify_comment_in_request_details_dlg`, *strings.reg_auth_cert_deletion*
                * :func:`~common_lib.component_cs_mgm_requests.Component_cs_mgm_requests.close_request_details_dlg`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url')

        # Step Generate backup in central server
        self.component_cs_sidebar.open_backup_restore_view()
        self.component_cs_backup.generate_backup()
        self.restore_cs = True

        # Step Delete security server auth cert in central server
        self.component_cs_sidebar.open_security_servers_view()
        self.component_cs_sec_servers.open_server_details_dlg(u'member1_configuration', u'member_name')
        self.component_cs_sec_servers.delete_auth_cert_in_server_details_dlg()
        self.component_cs_sec_servers.close_server_details_dlg()

        # Step Verify reguest comment in central server
        self.component_cs_sidebar.open_management_request_view()
        self.component_cs_mgm_requests.open_request_details_dlg(strings.request_cert_deletion)
        self.component_cs_mgm_requests.verify_comment_in_request_details_dlg(strings.reg_auth_cert_deletion)
        self.component_cs_mgm_requests.close_request_details_dlg()

    def test_deletion_of_client_of_ss_from_ss(self):
        """
        Test case for deleting client of security server from security server

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: login to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
            * **Step 2: generate central server backup in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
            * **Step 3: login to security server**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
            * **Step 4: generate security server backup in security server**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * :func:`~common_lib.component_ss_backup.Component_ss_backup.generate_backup`
            * **Step 5: delete client of security server in security server**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_security_servers_client_view`
                * :func:`~pagemodel.ss_clients.Ss_clients.find_and_open_by_text_dlg_by_subsystem_code`, *TESTDATA[u'member1_configuration']*
                * :func:`~common_lib.component_ss_clients.Component_ss_clients.unregister_and_delete_subsystem_in_subsystem_details_dlg`
            * **Step 6: verify test service status in security server**
            * **Step 7: open central server url**
                * :func:`~common_lib.component_cs.Component_cs.open_central_server_url`, *u'cs_url'*
            * **Step 8: verify management request of client deletion in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_management_request_view`
            * **Step 9: verify subsystem state in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.open_member_details_dlg`, *'member1_configuration'*, *u'member_name'*
                * :func:`~common_lib.component_cs_members.Component_cs_members.verify_subsystem_is_removable_in_member_details_dlg`, *u'member1_configuration'*, *u'subsystem_code'*
                * :func:`~common_lib.component_cs_members.Component_cs_members.close_member_details_dlg`
        """
        # Step Login to central server
        self.component_cs.login(u'cs_url')

        # Step Generate central server backup in central server
        self.component_cs_sidebar.open_backup_restore_view()
        self.component_cs_backup.generate_backup()
        self.restore_cs = True

        # Step Login to security server
        self.component_ss.login(u'ss1_url')

        # Step Generate security server backup in security server
        self.component_ss_sidebar.open_backup_restore_view()
        self.component_ss_backup.generate_backup()
        self.restore_ss = True
        sleep(200)

        # Step Delete client of security server in security server
        self.component_ss_sidebar.open_security_servers_client_view()
        self.ss_clients.find_and_open_by_text_dlg_by_subsystem_code(TESTDATA[u'member1_configuration'])
        self.component_ss_clients.unregister_and_delete_subsystem_in_subsystem_details_dlg()

        # Step Open central server url
        self.component_cs.open_central_server_url(u'cs_url')

        # Step Verify management request of client deletion in central server
        self.component_cs_sidebar.open_management_request_view()

        # Step Verify subsystem state in central server
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.open_member_details_dlg('member1_configuration', u'member_name')
        self.component_cs_members.verify_subsystem_is_removable_in_member_details_dlg(u'member1_configuration', u'subsystem_code')
        self.component_cs_members.close_member_details_dlg()
