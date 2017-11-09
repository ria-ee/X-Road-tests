# -*- coding: utf-8 -*-
from webframework import TESTDATA
from webframework.extension.base.baseTest import BaseTest
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
from pagemodel.cs_members import Cs_members
from pagemodel.ss_clients_dlg_services import Ss_clients_dlg_services
from pagemodel.ss_client_dlg_details import Ss_client_dlg_details
from pagemodel.cs_sidebar import Cs_sidebar
from pagemodel.ss_clients import Ss_clients
from pagemodel.ss_login import Ss_login
from pagemodel.cs_sec_servers import Cs_sec_servers
from pagemodel.cs_sec_servers_mgm_request_app_conf import Cs_sec_servers_mgm_request_app_conf
from pagemodel.ss_clients_add_client import Ss_clients_add_client
from pagemodel.ss_client_dlg_unregister import Ss_client_dlg_unregister
from pagemodel.ss_client_dlg_delete_unregister import Ss_client_dlg_delete_unregister
from pagemodel.cs_sec_servers_mgm_requests import Cs_sec_servers_mgm_requests
from pagemodel.cs_sec_serves_mgm_request_approve import Cs_sec_serves_mgm_request_approve
from pagemodel.ss_sidebar import Ss_sidebar
from pagemodel.open_application import Open_application
from pagemodel.cs_members_details_dlg import Cs_members_details_dlg
from common_lib.component_cs_sidebar import Component_cs_sidebar

class Xroad_test_service(BaseTest):
    """
    Xroad cases for testing enabling wsdl services and sending messages

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
    cs_members = Cs_members()
    ss_clients_dlg_services = Ss_clients_dlg_services()
    ss_client_dlg_details = Ss_client_dlg_details()
    cs_sidebar = Cs_sidebar()
    ss_clients = Ss_clients()
    ss_login = Ss_login()
    cs_sec_servers = Cs_sec_servers()
    cs_sec_servers_mgm_request_app_conf = Cs_sec_servers_mgm_request_app_conf()
    ss_clients_add_client = Ss_clients_add_client()
    ss_client_dlg_unregister = Ss_client_dlg_unregister()
    ss_client_dlg_delete_unregister = Ss_client_dlg_delete_unregister()
    cs_sec_servers_mgm_requests = Cs_sec_servers_mgm_requests()
    cs_sec_serves_mgm_request_approve = Cs_sec_serves_mgm_request_approve()
    ss_sidebar = Ss_sidebar()
    open_application = Open_application()
    cs_members_details_dlg = Cs_members_details_dlg()
    component_cs_sidebar = Component_cs_sidebar()

    def setUp(self):
        """
        Method that runs before every unittest

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.start_log_time = self.Start_log_time = self.common_lib`
                * **Step 2:** :func:`~common_lib.common_lib.Common_lib.get_version_information`
        """
        self.start_log_time = self.common_lib.get_log_utc_time()
        if "test-" in TESTDATA[u'ss1_static_url']['url']:
            self.common_lib.get_version_information()

    def tearDown(self):
        """
        Method that runs after every unittest

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients_add_client.Ss_clients_add_client.cancel_client_adding`
                * **Step 2:** :func:`~common_lib.common_lib.Common_lib.log_out`
                * **Step 3:** :func:`~pagemodel.open_application.Open_application.open_application_url`, *TESTDATA[u'ss1_static_url']*
                * **Step 4:** :func:`~pagemodel.ss_login.Ss_login.login`, *TESTDATA[u'ss1_static_url']*
                * **Step 5:** :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * **Step 6:** :func:`~pagemodel.ss_clients.Ss_clients.click_and_open_details_of_client_in_table`, *TESTDATA[u'member_static_configuration']*
                * **Step 7:** :func:`~pagemodel.ss_client_dlg_details.Ss_client_dlg_details.click_unregister_client`
                * **Step 8:** :func:`~pagemodel.ss_client_dlg_unregister.Ss_client_dlg_unregister.click_confirm_unregister`
                * **Step 9:** :func:`~pagemodel.ss_client_dlg_delete_unregister.Ss_client_dlg_delete_unregister.click_client_delete`
                * **Step 10:** :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        stop_log_time = self.common_lib.get_log_utc_time()
        if not self.is_last_test_passed():
            pass

        # Check cancel button
        self.ss_clients_add_client.cancel_client_adding()
        sleep(1)
        try:
            self.common_lib.log_out()
        except:
            pass
        try:
            # Add new subsystem client
            self.open_application.open_application_url(TESTDATA[u'ss1_static_url'])
            # login
            self.ss_login.login(TESTDATA[u'ss1_static_url'])
            self.ss_sidebar.verify_sidebar_title()
            sleep(2)
            # Unregister client
            self.ss_clients.click_and_open_details_of_client_in_table(TESTDATA[u'member_static_configuration'])
            self.ss_client_dlg_details.click_unregister_client()
            self.ss_client_dlg_unregister.click_confirm_unregister()
            self.ss_client_dlg_delete_unregister.click_client_delete()
            sleep(1)
            self.common_lib.log_out()
        except:
            print("Error in teardown")

    def test_add_and_registering_new_subsystem_and_service_1(self):
        """
        Add and register new subsystem and service

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: click wsdl enable #webpage:ss_clients_dlg_services**
                * :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_wsdl_enable`
            * **Step 2: open wsdl servicel #webpage: ss_clients_dlg_services**
                * :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.open_wsdl_service`
                * :func:`~common_lib.component_ss_services.Component_ss_services.edit_wsdl_default_service_parameters_in_ss`, *u'wsdl_service'*, *u'service_wsdl'*
                * :func:`~common_lib.component_ss_services.Component_ss_services.add_service_access_rights_to_all_in_ss`
                * :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_close_services_dlg`
            * **Step 3: log out**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 4: next central server to create and accept new client request**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_static_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.new_client_registration_request_in_cs`, *u'member_static_configuration'*
                * :func:`~common_lib.component_cs_members.Component_cs_members.accept_mgm_request_security_servers_in_cs`
                * :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_button_close`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 5: login ss1 server**
                * :func:`~pagemodel.open_application.Open_application.open_application_url`, *TESTDATA[u'ss1_static_url']*
            * **Step 6: login #webpage: ss_login**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_static_url'*
            * **Step 7: check service registration complete #webpage: ss_clients #parameters:**
                * :func:`~pagemodel.ss_clients.Ss_clients.verify_service_registration_complete`, *TESTDATA[u'member_static_configuration']*
            * **Step 8: verify soap message**
                * :func:`~common_lib.common_lib.Common_lib.send_soap_api_request_hello`, *TESTDATA['soap']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        self.component_ss.login(u'ss1_static_url')
        self.component_ss_clients.add_new_subsystem_to_ss(u'member_static_configuration')
        self.component_ss_clients.open_client_services_dlg_with_full_member_id(u'member_static_configuration')

        self.component_ss_services.add_new_wsdl(u'add_wsdl')
        # Step Click wsdl enable #Webpage:ss_clients_dlg_services
        self.ss_clients_dlg_services.click_wsdl_enable()
        # Step Open wsdl servicel #Webpage: ss_clients_dlg_services
        self.ss_clients_dlg_services.open_wsdl_service()

        self.component_ss_services.edit_wsdl_default_service_parameters_in_ss(u'wsdl_service', u'service_wsdl')
        # step Add ACL subjects
        self.component_ss_services.add_service_access_rights_to_all_in_ss()
        self.ss_clients_dlg_services.click_close_services_dlg()
        # Step Log out
        self.common_lib.log_out()
        # Step Next central server to create and accept new client request
        self.component_cs.login(u'cs_static_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.new_client_registration_request_in_cs(u'member_static_configuration')
        self.component_cs_members.accept_mgm_request_security_servers_in_cs()
        self.cs_members_details_dlg.click_button_close()
        self.common_lib.log_out()
        sleep(23)
        # Step login ss1 server
        self.open_application.open_application_url(TESTDATA[u'ss1_static_url'])
        # Step login #Webpage: ss_login
        self.component_ss.login(u'ss1_static_url')
        # Step Check service registration complete #Webpage: ss_clients #Parameters:
        self.ss_clients.verify_service_registration_complete(TESTDATA[u'member_static_configuration'])
        # Step Verify soap message
        self.common_lib.send_soap_api_request_hello(TESTDATA['soap'])
        sleep(1)
        self.common_lib.log_out()
