# -*- coding: utf-8 -*-
from variables import strings
from webframework import TESTDATA
from webframework.extension.base.setupTest import SetupTest
from webframework.extension.parsers.parameter_parser import get_all_parameters
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib.common_lib import Common_lib
from common_lib.common_lib_ssh import Common_lib_ssh
from common_lib.component_cs import Component_cs
from common_lib.component_cs_backup import Component_cs_backup
from common_lib.component_cs_cert_services import Component_cs_cert_services
from common_lib.component_cs_conf_mgm import Component_cs_conf_mgm
from common_lib.component_cs_members import Component_cs_members
from common_lib.component_cs_system_settings import Component_cs_system_settings
from common_lib.component_cs_tsp_services import Component_cs_tsp_services
from common_lib.component_ss import Component_ss
from common_lib.component_ss_clients import Component_ss_clients
from common_lib.component_ss_initial_conf import Component_ss_initial_conf
from common_lib.component_ss_keys_and_certs import Component_ss_keys_and_certs
from common_lib.component_ss_services import Component_ss_services
from pagemodel.ss_keys_and_cert_dlg_delete import Ss_keys_and_cert_dlg_delete
from pagemodel.cs_sec_servers_details import Cs_sec_servers_details
from pagemodel.cs_sidebar import Cs_sidebar
from pagemodel.ss_keys_and_cert import Ss_keys_and_cert
from pagemodel.cs_sec_servers import Cs_sec_servers
from pagemodel.cs_sec_servers_mgm_request_app_conf import Cs_sec_servers_mgm_request_app_conf
from pagemodel.ss_keys_and_cert_dlg_import_cert import Ss_keys_and_cert_dlg_import_cert
from pagemodel.cs_sec_servers_auth_dlg import Cs_sec_servers_auth_dlg
from pagemodel.cs_sec_servers_details_auth import Cs_sec_servers_details_auth
from pagemodel.cs_sec_servers_mgm_requests import Cs_sec_servers_mgm_requests
from pagemodel.cs_sec_serves_mgm_request_approve import Cs_sec_serves_mgm_request_approve
from pagemodel.ss_sidebar import Ss_sidebar
from common_lib.component_cs_sidebar import Component_cs_sidebar
from common_lib.component_ss_sidebar import Component_ss_sidebar

class Xroad_keys_and_certs(SetupTest):
    """
    Xroad cases for testing key and certificate use cases

    **Changelog:**
        * 11.07.2017
            | Documentation updated
    """
    common_utils = CommonUtils()
    common_lib = Common_lib()
    common_lib_ssh = Common_lib_ssh()
    component_cs = Component_cs()
    component_cs_backup = Component_cs_backup()
    component_cs_cert_services = Component_cs_cert_services()
    component_cs_conf_mgm = Component_cs_conf_mgm()
    component_cs_members = Component_cs_members()
    component_cs_system_settings = Component_cs_system_settings()
    component_cs_tsp_services = Component_cs_tsp_services()
    component_ss = Component_ss()
    component_ss_clients = Component_ss_clients()
    component_ss_initial_conf = Component_ss_initial_conf()
    component_ss_keys_and_certs = Component_ss_keys_and_certs()
    component_ss_services = Component_ss_services()
    ss_keys_and_cert_dlg_delete = Ss_keys_and_cert_dlg_delete()
    cs_sec_servers_details = Cs_sec_servers_details()
    cs_sidebar = Cs_sidebar()
    ss_keys_and_cert = Ss_keys_and_cert()
    cs_sec_servers = Cs_sec_servers()
    cs_sec_servers_mgm_request_app_conf = Cs_sec_servers_mgm_request_app_conf()
    ss_keys_and_cert_dlg_import_cert = Ss_keys_and_cert_dlg_import_cert()
    cs_sec_servers_auth_dlg = Cs_sec_servers_auth_dlg()
    cs_sec_servers_details_auth = Cs_sec_servers_details_auth()
    cs_sec_servers_mgm_requests = Cs_sec_servers_mgm_requests()
    cs_sec_serves_mgm_request_approve = Cs_sec_serves_mgm_request_approve()
    ss_sidebar = Ss_sidebar()
    component_cs_sidebar = Component_cs_sidebar()
    component_ss_sidebar = Component_ss_sidebar()

    @classmethod
    def setUpTestSet(self):
        """
        Method that runs before every unittest

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.autogen_browser = self.Autogen_browser = self.common_utils`
        """
        self.autogen_browser = self.common_utils.open_browser()

    @classmethod
    def tearDownTestSet(self):
        """
        Method that runs after every unittest

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.close_all_browsers`
        """
        self.common_utils.close_all_browsers()

    def setUp(self):
        """
        Method that runs before every test case

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib.Common_lib.remove_cert_from_downloads`, *TESTDATA[u'paths']*
                * **Step 2:** :func:`~pagemodel.start_log_time = self.Start_log_time = self.common_lib`
                * **Step 3:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"ss1_url"*
                * **Step 4:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"cs_url"*
        """
        self.common_lib.remove_cert_from_downloads(TESTDATA[u'paths'])
        self.start_log_time = self.common_lib.get_log_utc_time()
        self.common_lib_ssh.empty_all_logs_from_server("ss1_url")
        self.common_lib_ssh.empty_all_logs_from_server("cs_url")

    def tearDown(self):
        """
        Method that runs after every unittest

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.get_all_logs_from_server`, *u'ss1_url'*
                * **Step 2:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.find_exception_from_logs_and_save`, *self.start_log_time*, *stop_log_time*, *u'ss1_url'*, *copy_log*
                * **Step 3:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.get_all_logs_from_server`, *u'cs_url'*
                * **Step 4:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.find_exception_from_logs_and_save`, *self.start_log_time*, *stop_log_time*, *u'cs_url'*, *copy_log*
                * **Step 5:** :func:`~common_lib.common_lib.Common_lib.remove_cert_from_downloads`, *TESTDATA[u'paths']*
                * **Step 6:** :func:`~common_lib.common_lib.Common_lib.get_ui_error_message`
                * **Step 7:** :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        stop_log_time = self.common_lib.get_log_utc_time()
        if not self.is_last_test_passed():
            _, copy_log = self.get_log_file_paths()
            self.common_lib_ssh.get_all_logs_from_server(u'ss1_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'ss1_url', copy_log)
            self.common_lib_ssh.get_all_logs_from_server(u'cs_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'cs_url', copy_log)

        self.common_lib.remove_cert_from_downloads(TESTDATA[u'paths'])
        self.common_lib.get_ui_error_message()
        sleep(1)
        try:
            self.common_lib.log_out()
        except:
            pass

    def test_generate_and_delete_cert_1(self):
        """
        Generate and delete certificate

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: delete generated key #webpage: ss_keys_and_cert**
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_delete_cert`
            * **Step 2: click delete cert confirm key #webpage: ss_keys_and_cert_dlg_delete**
                * :func:`~pagemodel.ss_keys_and_cert_dlg_delete.Ss_keys_and_cert_dlg_delete.click_delete_cert_confirm`, *strings.sign_key_label_2*
            * **Step 3: log out security server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        self.component_ss.login(u'ss1_url')
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.sign_key_label_2)
        # Step Delete generated key #Webpage: ss_keys_and_cert
        self.ss_keys_and_cert.click_delete_cert()
        # Step Click delete cert confirm key #Webpage: ss_keys_and_cert_dlg_delete
        self.ss_keys_and_cert_dlg_delete.click_delete_cert_confirm(strings.sign_key_label_2)
        # Step Log out security server
        self.common_lib.log_out()

    def test_generate_cert_request_2(self):
        """
        Generate certificate request

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: click logout**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        self.component_ss.login(u'ss1_url')
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.sign_key_label_2)
        self.component_ss_keys_and_certs.generate_sign_certificate_request_in_ss(u'member1_configuration')
        self.component_ss_keys_and_certs.verify_key_request(u'paths')
        self.component_ss_keys_and_certs.delete_key_by_label(strings.sign_key_label_2)
        sleep(3)
        # Step Click logout
        self.common_lib.log_out()

    def test_generate_cert_request_and_import_3(self):
        """
        Generate cert request and import

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: delete cert request #webpage: ss_keys_and_cert**
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.delete_imported_cert_key`, *cert_key*
            * **Step 2: click delete cert confirm key #webpage: ss_keys_and_cert_dlg_delete**
                * :func:`~pagemodel.ss_keys_and_cert_dlg_delete.Ss_keys_and_cert_dlg_delete.click_delete_cert_confirm`, *strings.sign_key_label_2*
                * :func:`~common_lib.common_lib.Common_lib.revoke_cert`, *TESTDATA[u'paths']*
            * **Step 3: log out from securityserver**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        self.component_ss.login(u'ss1_url')
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.sign_key_label_2)
        self.component_ss_keys_and_certs.generate_sign_certificate_request_in_ss(u'member1_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_sign(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("sign")
        cert_number, cert_key = self.component_ss_keys_and_certs.verify_uploaded_certificate("sign")
        # Step Delete cert request #Webpage: ss_keys_and_cert
        self.ss_keys_and_cert.delete_imported_cert_key(cert_key)

        cert_key = cert_key.split(": ")[-1]
        cert_key = cert_key.split(" ")[0]
        print(cert_key)
        # Step Click delete cert confirm key #Webpage: ss_keys_and_cert_dlg_delete
        self.ss_keys_and_cert_dlg_delete.click_delete_cert_confirm(strings.sign_key_label_2)
        self.common_lib.revoke_cert(TESTDATA[u'paths'])
        sleep(3)
        # Step Log out from securityserver
        self.common_lib.log_out()

    def test_generate_cert_request_and_import_auth_4(self):
        """
        Generate certificate request and import authentication

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: find security server by member name #webpage: cs_sec_servers #parameters: certificate_auth**
                * :func:`~pagemodel.cs_sec_servers.Cs_sec_servers.click_security_servers_row_with_text`, *TESTDATA[u'member1_configuration'][u'member_name']*
            * **Step 2: click ss details server #webpage: cs_sec_servers**
                * :func:`~pagemodel.cs_sec_servers.Cs_sec_servers.click_ss_details`
                * :func:`~pagemodel.cs_sec_servers_details.Cs_sec_servers_details.verify_ss_details_view`
            * **Step 3: click authentication certificates  #webpage: cs_sec_servers_details**
                * :func:`~pagemodel.cs_sec_servers_details.Cs_sec_servers_details.click_authentication_certificates_tab`
            * **Step 4: add auth certificate to server #webpage: cs_sec_servers_details_auth**
                * :func:`~pagemodel.cs_sec_servers_details_auth.Cs_sec_servers_details_auth.click_button_id_securityserver_authcert_add`
            * **Step 5: upload auth cert file #webpage: cs_sec_servers_auth_dlg**
                * :func:`~pagemodel.cs_sec_servers_auth_dlg.Cs_sec_servers_auth_dlg.click_upload_auth_cert`
            * **Step 6: make cert file upload #webpage: ss_keys_and_cert_dlg_import_cert**
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.make_cert_file_upload`, *"auth"*
            * **Step 7: submit auth cert add #webpage: cs_sec_servers_auth_dlg**
                * :func:`~pagemodel.cs_sec_servers_auth_dlg.Cs_sec_servers_auth_dlg.click_button_id_auth_cert_add_submit`
                * :func:`~pagemodel.cs_sec_servers_details.Cs_sec_servers_details.wait_until_submitted_certificate`
            * **Step 8: click mgm requests tab #webpage: cs_sec_servers_details**
                * :func:`~pagemodel.cs_sec_servers_details.Cs_sec_servers_details.click_mgm_requests_tab`
            * **Step 9: find and click mgm request  #webpage: cs_sec_servers_mgm_requests**
                * :func:`~pagemodel.cs_sec_servers_mgm_requests.Cs_sec_servers_mgm_requests.find_and_click_mgm_request`
            * **Step 10: accept request in central server #webpage: cs_sec_serves_mgm_request_approve**
                * :func:`~pagemodel.cs_sec_serves_mgm_request_approve.Cs_sec_serves_mgm_request_approve.click_approve_request`
            * **Step 11: click confirm approve request #webpage: cs_sec_servers_mgm_request_app_conf**
                * :func:`~pagemodel.cs_sec_servers_mgm_request_app_conf.Cs_sec_servers_mgm_request_app_conf.click_confirm_approve_request`
                * :func:`~pagemodel.cs_sec_servers_mgm_requests.Cs_sec_servers_mgm_requests.click_close_mgm_req_dlg`
            * **Step 12: log out from central server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
            * **Step 13: click keys and cert dev ss #webpage: ss_sidebar**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.click_keys_and_certificates`
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.verify_keys_and_cert_title`
            * **Step 14: verify that key is registered**
                * :func:`~webframework.extension.util.common_utils.CommonUtils.reload_page`
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.find_texts_from_table_keys_auth`, *cert_number*
            * **Step 15: delete auth cert request #webpage: ss_keys_and_cert**
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.delete_imported_cert_key`, *cert_key*
            * **Step 16: click unregister and delete cert confirm #webpage: ss_keys_and_cert_dlg_delete #parameters: certificate_auth**
                * :func:`~pagemodel.ss_keys_and_cert_dlg_delete.Ss_keys_and_cert_dlg_delete.click_unregister_and_delete_cert_confirm`, *strings.auth_key_label_2*
            * **Step 17: revoke cert**
                * :func:`~common_lib.common_lib.Common_lib.revoke_cert_auth`, *TESTDATA[u'paths']*
            * **Step 18: log out security server**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        self.component_ss.login(u'ss1_url')
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.auth_key_label_2)
        self.component_ss_keys_and_certs.generate_auth_certificate_request_in_ss(u'member1_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_auth(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("auth")
        cert_number, cert_key = self.component_ss_keys_and_certs.verify_uploaded_certificate("auth")
        key_auth_name = strings.server_environment_approved_ca() + " " + str(cert_number)
        self.component_ss_keys_and_certs.register_auth_certificate_in_ss(key_auth_name, u'member1_configuration')
        self.common_lib.log_out()

        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_security_servers_view()
        # Step Find security server by member name #Webpage: cs_sec_servers #Parameters: certificate_auth
        self.cs_sec_servers.click_security_servers_row_with_text(TESTDATA[u'member1_configuration'][u'member_name'])
        # Step Click ss details server #Webpage: cs_sec_servers
        self.cs_sec_servers.click_ss_details()
        self.cs_sec_servers_details.verify_ss_details_view()
        # Step Click authentication certificates  #Webpage: cs_sec_servers_details
        self.cs_sec_servers_details.click_authentication_certificates_tab()
        # Step Add auth certificate to server #Webpage: cs_sec_servers_details_auth
        self.cs_sec_servers_details_auth.click_button_id_securityserver_authcert_add()
        # Step Upload auth cert file #Webpage: cs_sec_servers_auth_dlg
        self.cs_sec_servers_auth_dlg.click_upload_auth_cert()
        # Step Make cert file upload #Webpage: ss_keys_and_cert_dlg_import_cert
        self.component_ss_keys_and_certs.make_cert_file_upload("auth")
        sleep(2)
        # Step Submit auth cert add #Webpage: cs_sec_servers_auth_dlg
        self.cs_sec_servers_auth_dlg.click_button_id_auth_cert_add_submit()
        self.cs_sec_servers_details.wait_until_submitted_certificate()
        # Step Click mgm requests tab #Webpage: cs_sec_servers_details
        self.cs_sec_servers_details.click_mgm_requests_tab()
        sleep(3)
         # Step Find and click mgm request  #Webpage: cs_sec_servers_mgm_requests
        self.cs_sec_servers_mgm_requests.find_and_click_mgm_request()
        sleep(1)
        # Step Accept request in central server #Webpage: cs_sec_serves_mgm_request_approve
        self.cs_sec_serves_mgm_request_approve.click_approve_request()
        sleep(1)
        # Step Click confirm approve request #Webpage: cs_sec_servers_mgm_request_app_conf
        self.cs_sec_servers_mgm_request_app_conf.click_confirm_approve_request()
        sleep(3)
        self.cs_sec_servers_mgm_requests.click_close_mgm_req_dlg()
        sleep(5)
        # Step Log out from central server
        self.common_lib.log_out()

        self.component_ss.login(u'ss1_url')
        self.ss_sidebar.verify_sidebar_title()
        # Step Click keys and cert dev ss #Webpage: ss_sidebar
        self.ss_sidebar.click_keys_and_certificates()
        self.ss_keys_and_cert.verify_keys_and_cert_title()
        # Step Verify that key is registered
        sleep(100)
        self.common_utils.reload_page()
        sleep(5)

        self.ss_keys_and_cert.find_texts_from_table_keys_auth(cert_number)

        # Step Delete auth cert request #Webpage: ss_keys_and_cert
        self.ss_keys_and_cert.delete_imported_cert_key(cert_key)
        cert_key = cert_key.split(": ")[-1]
        cert_key = cert_key.split(" ")[0]
        print(cert_key)
        # Step Click unregister and delete cert confirm #Webpage: ss_keys_and_cert_dlg_delete #Parameters: certificate_auth
        self.ss_keys_and_cert_dlg_delete.click_unregister_and_delete_cert_confirm(strings.auth_key_label_2)
        # Step Revoke cert
        self.common_lib.revoke_cert_auth(TESTDATA[u'paths'])
        sleep(3)
        # Step Log out security server
        self.common_lib.log_out()
