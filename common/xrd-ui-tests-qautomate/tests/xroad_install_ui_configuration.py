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
from common_lib.component_cs_sidebar import Component_cs_sidebar
from common_lib.component_ss_sidebar import Component_ss_sidebar
from pagemodel.cs_members import Cs_members
from pagemodel.cs_sidebar import Cs_sidebar
from pagemodel.cs_sec_servers import Cs_sec_servers
from pagemodel.cs_conf_mgm import Cs_conf_mgm
from pagemodel.cs_system_settings import Cs_system_settings
from pagemodel.cs_sec_servers_mgm_requests import Cs_sec_servers_mgm_requests
from pagemodel.ss_clients_dlg_services import Ss_clients_dlg_services
from pagemodel.ss_clients_add_search_client_dlg import Ss_clients_add_search_client_dlg
from pagemodel.ss_clients import Ss_clients
from pagemodel.ss_keys_and_cert import Ss_keys_and_cert
from pagemodel.ss_clients_add_client import Ss_clients_add_client
from pagemodel.ss_enter_pin_dlg import Ss_enter_pin_dlg
from pagemodel.ss_sidebar import Ss_sidebar

class Xroad_install_ui_configuration(SetupTest):
    """
    Xroad cases for installing ui configurations

    **Changelog:**
        * 11.07.2017
            | Documentation updated
    """
    start_log_time = ""
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
    component_cs_sidebar = Component_cs_sidebar()
    component_ss_sidebar = Component_ss_sidebar()
    ss_clients_dlg_services = Ss_clients_dlg_services()
    ss_clients_add_search_client_dlg = Ss_clients_add_search_client_dlg()
    ss_keys_and_cert = Ss_keys_and_cert()
    ss_clients_add_client = Ss_clients_add_client()
    ss_clients = Ss_clients()
    ss_enter_pin_dlg = Ss_enter_pin_dlg()
    ss_sidebar = Ss_sidebar()
    cs_members = Cs_members()
    cs_sidebar = Cs_sidebar()
    cs_sec_servers = Cs_sec_servers()
    cs_conf_mgm = Cs_conf_mgm()
    cs_system_settings = Cs_system_settings()
    cs_sec_servers_mgm_requests = Cs_sec_servers_mgm_requests()
    
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
                * **Step 1:** :func:`~common_lib.common_lib.Common_lib.remove_anchor_and_certs_from_downloads`, *TESTDATA[u'paths']*
                * **Step 2:** :func:`~pagemodel.start_log_time = self.Start_log_time = self.common_lib`
                * **Step 3:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"ss1_url"*
                * **Step 4:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"cs_url"*
                * **Step 5:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.empty_all_logs_from_server`, *"ss_mgm_url"*
        """
        self.common_lib.remove_anchor_and_certs_from_downloads(TESTDATA[u'paths'])
        self.start_log_time = self.common_lib.get_log_utc_time()
        self.common_lib_ssh.empty_all_logs_from_server("ss1_url")
        self.common_lib_ssh.empty_all_logs_from_server("cs_url")
        self.common_lib_ssh.empty_all_logs_from_server("ss_mgm_url")

    def tearDown(self):
        """
        Method that runs after every test case

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.get_all_logs_from_server`, *u'ss_mgm_url'*
                * **Step 2:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.find_exception_from_logs_and_save`, *self.start_log_time*, *stop_log_time*, *u'ss_mgm_url'*, *copy_log*
                * **Step 3:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.get_all_logs_from_server`, *u'cs_url'*
                * **Step 4:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.find_exception_from_logs_and_save`, *self.start_log_time*, *stop_log_time*, *u'cs_url'*, *copy_log*
                * **Step 5:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.get_all_logs_from_server`, *u'ss1_url'*
                * **Step 6:** :func:`~common_lib.common_lib_ssh.Common_lib_ssh.find_exception_from_logs_and_save`, *self.start_log_time*, *stop_log_time*, *u'ss1_url'*, *copy_log*
                * **Step 7:** :func:`~common_lib.common_lib.Common_lib.get_ui_error_message`
                * **Step 8:** :func:`~common_lib.common_lib.Common_lib.remove_anchor_and_certs_from_downloads`, *TESTDATA[u'paths']*
        """
        stop_log_time = self.common_lib.get_log_utc_time()
        if not self.is_last_test_passed():
            _, copy_log = self.get_log_file_paths()
            self.common_lib_ssh.get_all_logs_from_server(u'ss_mgm_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'ss_mgm_url', copy_log)
            self.common_lib_ssh.get_all_logs_from_server(u'cs_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'cs_url', copy_log)
            self.common_lib_ssh.get_all_logs_from_server(u'ss1_url')
            self.common_lib_ssh.find_exception_from_logs_and_save(self.start_log_time, stop_log_time, u'ss1_url', copy_log)

        self.common_lib.get_ui_error_message()
        self.common_lib.remove_anchor_and_certs_from_downloads(TESTDATA[u'paths'])

    def test_configure_ss_server_add_to_existing_cs_2(self):
        """
        Configure security server and add to existing central server

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: read liityntapalvelin konfiguraatio parameters**
                * :func:`~common_lib.common_lib.Common_lib.read_liityntapalvelin_konfiguraatio_parameters`, *TESTDATA*
            * **Step 2: find existing member in central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~pagemodel.cs_members.Cs_members.wait_until_element_is_visible_member_name`
                * :func:`~common_lib.component_cs_members.Component_cs_members.open_member_details_dlg`, *u'member1_configuration'*, *u'member_name'*
            * **Step 3: add subsystem code existing member to central server**
                * :func:`~common_lib.component_cs_members.Component_cs_members.add_new_subsystem_to_existing_member_in_cs`, *u'member1_configuration'*
                * :func:`~common_lib.common_lib.Common_lib.get_ui_error_message`
            * **Step 4: download anchor from central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.download_source_anchor_from_cs`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 5: import configuration anchor to security server**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*, *initial_conf=True*
                * :func:`~common_lib.component_ss_initial_conf.Component_ss_initial_conf.import_configuration_anchor`, *u'paths'*
                * :func:`~common_lib.component_ss_initial_conf.Component_ss_initial_conf.add_initial_server_configuration_values_to_ss`, *u'member1_configuration'*, *u'ss1_url'*
            * **Step 6: verify active token in security server**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed`, *u'ss1_url'*
            * **Step 7: add timestamping services to ss**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_system_parameters_view`
                * :func:`~common_lib.component_ss.Component_ss.add_timestamping_url_to_ss`, *u'ss1_url'*
            * **Step 8: add sign certificate to security server**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss`, *strings.sign_key_label*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_sign_certificate_request_in_ss`, *u'member1_configuration'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_key_and_sign_certificate_sign`, *u'paths'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.import_and_upload_key_certificate`, *"sign"*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_uploaded_certificate`, *"sign"*
            * **Step 9: add auth certificate to security server**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss`, *strings.auth_key_label*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_auth_certificate_request_in_ss`, *u'member1_configuration'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_key_and_sign_certificate_auth`, *u'paths'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.import_and_upload_key_certificate`, *"auth"*
            * **Step 10: register request auth certificate and activate**
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.register_auth_certificate_in_ss`, *key_auth_name*, *u'member1_configuration'*
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_cert_activate`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 11: accept auth key request in central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.accept_auth_certificate_request_in_cs`, *u'member1_configuration'*
            * **Step 12: get wsdl address**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_system_settings_view`
                * :func:`~pagemodel.cs_system_settings.Cs_system_settings.get_wsdl_and_services_address`, *TESTDATA[u'cs_url']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 13: add subsystem to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.new_client_registration_request_in_cs`, *u'member1_configuration'*
                * :func:`~pagemodel.cs_sec_servers_mgm_requests.Cs_sec_servers_mgm_requests.click_close_mgm_req_dlg`
                * :func:`~common_lib.component_cs_members.Component_cs_members.close_member_details_dlg`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
                * :func:`~common_lib.common_lib.Common_lib.sync_global_conf`, *TESTDATA[u'ss1_url'][u'sync_timeout']*
            * **Step 14: add subsystem to security server**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
                * :func:`~pagemodel.ss_clients.Ss_clients.verify_service_registration_complete`, *TESTDATA[u'member1_configuration']*
                * :func:`~common_lib.component_ss_clients.Component_ss_clients.add_new_subsystem_to_ss`, *u'member1_configuration'*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
                * :func:`~common_lib.common_lib.Common_lib.sync_global_conf`, *TESTDATA[u'ss1_url'][u'sync_timeout']*
            * **Step 15: accept subsystem in in central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.accept_mgm_requests_in_cs`, *u'member1_configuration'*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 16: check registration complete**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
                * :func:`~pagemodel.ss_clients.Ss_clients.verify_service_registration_complete`, *TESTDATA[u'member1_configuration']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Read liityntapalvelin konfiguraatio parameters
        self.common_lib.read_liityntapalvelin_konfiguraatio_parameters(TESTDATA)

        # Step Find existing member in central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.cs_members.wait_until_element_is_visible_member_name()
        self.component_cs_members.open_member_details_dlg(u'member1_configuration', u'member_name')

        # Step Add subsystem code existing member to central server
        self.component_cs_members.add_new_subsystem_to_existing_member_in_cs(u'member1_configuration')
        self.common_lib.get_ui_error_message()

        # Step Download anchor from central server
        self.component_cs_sidebar.open_global_configuration_view()
        self.component_cs_conf_mgm.download_source_anchor_from_cs()
        self.common_lib.log_out()
        # Sync global conf timeout
        sleep(15)
        #self.common_lib.sync_global_conf(self.parameters[u'server_configuration'][u'sync_timeout'])

        # Step Import configuration anchor to security server
        self.component_ss.login(u'ss1_url', initial_conf=True)
        self.component_ss_initial_conf.import_configuration_anchor(u'paths')
        self.component_ss_initial_conf.add_initial_server_configuration_values_to_ss(u'member1_configuration', u'ss1_url')

        # Step Verify active token in security server
        self.ss_sidebar.verify_sidebar_title()
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed(u'ss1_url')

        # Step Add timestamping services to ss
        self.component_ss_sidebar.open_system_parameters_view()
        self.component_ss.add_timestamping_url_to_ss(u'ss1_url')

        # Step Add sign certificate to security server
        self.ss_sidebar.verify_sidebar_title()
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.sign_key_label)
        self.component_ss_keys_and_certs.generate_sign_certificate_request_in_ss(u'member1_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_sign(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("sign")
        self.component_ss_keys_and_certs.verify_uploaded_certificate("sign")

        # Step Add auth certificate to security server
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.auth_key_label)
        self.component_ss_keys_and_certs.generate_auth_certificate_request_in_ss(u'member1_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_auth(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("auth")
        cert_number = self.component_ss_keys_and_certs.verify_uploaded_certificate("auth")[0]
        key_auth_name = strings.server_environment_approved_ca() + " " + str(cert_number)

        # Step Register request auth certificate and activate
        self.component_ss_keys_and_certs.register_auth_certificate_in_ss(key_auth_name, u'member1_configuration')
        self.ss_keys_and_cert.click_cert_activate()
        self.common_lib.log_out()

        # Step Accept auth key request in central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.accept_auth_certificate_request_in_cs(u'member1_configuration')

        # Step Get WSDL address
        self.component_cs_sidebar.open_system_settings_view()
        self.cs_system_settings.get_wsdl_and_services_address(TESTDATA[u'cs_url'])
        self.common_lib.log_out()

        # Step Add subsystem to central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.new_client_registration_request_in_cs(u'member1_configuration')
        self.cs_sec_servers_mgm_requests.click_close_mgm_req_dlg()
        self.component_cs_members.close_member_details_dlg()
        self.common_lib.log_out()
        # Sync global conf timeout
        self.common_lib.sync_global_conf(TESTDATA[u'ss1_url'][u'sync_timeout'])

        # Step Add subsystem to security server
        self.component_ss.login(u'ss1_url')
        self.ss_clients.verify_service_registration_complete(TESTDATA[u'member1_configuration'])
        self.component_ss_clients.add_new_subsystem_to_ss(u'member1_configuration')
        self.common_lib.log_out()
        self.common_lib.sync_global_conf(TESTDATA[u'ss1_url'][u'sync_timeout'])

        # Step Accept subsystem in in central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.accept_mgm_requests_in_cs(u'member1_configuration')
        self.common_lib.log_out()

        # Step Check registration complete
        self.component_ss.login(u'ss1_url')
        self.ss_clients.verify_service_registration_complete(TESTDATA[u'member1_configuration'])
        self.common_lib.log_out()

    def test_configure_cs_and_ss_mgm_servers_1(self):
        """
        Configure central server and security servers

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: read liityntapalvelin konfiguraatio parameters**
                * :func:`~common_lib.common_lib.Common_lib.read_keskuspalvelin_konfiguraatio_parameters`, *TESTDATA*
            * **Step 2: initialize server and add new member in central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *initial_conf=True*
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.initialize_cs_server_config`, *u'cs_url'*
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.add_init_member_class`, *u'member_mgm_configuration'*
            * **Step 3: add ca certification services in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_certification_services_view`
                * :func:`~common_lib.component_cs_cert_services.Component_cs_cert_services.add_certification_service_and_upload_ca_root_to_cs`
            * **Step 4: add timestamping to central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_timestamping_services_view`
                * :func:`~common_lib.component_cs_tsp_services.Component_cs_tsp_services.add_timestamping_service_to_cs`, *u'paths'*, *u'cs_url'*
            * **Step 5: add members to central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.add_member_to_cs`, *u'member_mgm_configuration'*
            * **Step 6: add subsystem code to central server**
                * :func:`~common_lib.component_cs_members.Component_cs_members.add_new_subsystem_to_existing_member_in_cs`, *u'member_mgm_configuration'*
            * **Step 7: edit management service in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_system_settings_view`
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.edit_mgm_service_provider_in_cs`, *u'member_mgm_configuration'*
            * **Step 8: set global conf internal conf key in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.generate_config_key`, *key_type="internal"*
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.try_insert_pin_code`, *u'cs_url'*
                * :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 9: set global conf external key in central server**
                * :func:`~pagemodel.cs_conf_mgm.Cs_conf_mgm.click_link_external_configuration`
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.generate_config_key`, *key_type="external"*
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.try_insert_pin_code`, *u'cs_url'*
                * :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 10: set ocsp responder in central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_certification_services_view`
                * :func:`~common_lib.component_cs_cert_services.Component_cs_cert_services.add_new_ocsp_responder`, *u'cs_url'*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 11: download anchor from central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.download_source_anchor_from_cs`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 12: import configuration anchor to security server**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss_mgm_url'*, *initial_conf=True*
                * :func:`~common_lib.component_ss_initial_conf.Component_ss_initial_conf.import_configuration_anchor`, *u'paths'*
                * :func:`~common_lib.component_ss_initial_conf.Component_ss_initial_conf.add_initial_server_configuration_values_to_ss`, *u'member_mgm_configuration'*, *u'ss_mgm_url'*
            * **Step 13: verify token active in security server**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed`, *u'ss_mgm_url'*
            * **Step 14: add timestamping services to security server**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_system_parameters_view`
                * :func:`~common_lib.component_ss.Component_ss.add_timestamping_url_to_ss`, *u'ss_mgm_url'*
            * **Step 15: add sign certificate to security server**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss`, *strings.sign_key_label*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_sign_certificate_request_in_ss`, *u'member_mgm_configuration'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_key_and_sign_certificate_sign`, *u'paths'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.import_and_upload_key_certificate`, *"sign"*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_uploaded_certificate`, *"sign"*
            * **Step 16: add auth certificate to security server**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss`, *strings.auth_key_label*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_auth_certificate_request_in_ss`, *u'member_mgm_configuration'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_key_and_sign_certificate_auth`, *u'paths'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.import_and_upload_key_certificate`, *"auth"*
            * **Step 17: register request auth certificate and activate**
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.register_auth_certificate_in_ss`, *key_auth_name*, *u'member_mgm_configuration'*
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_cert_activate`
            * **Step 18: log out securityserver**
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 19: accept auth key request in central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.accept_auth_certificate_request_in_cs`, *u'member_mgm_configuration'*
            * **Step 20:8 copy wsdl addressitle phase 17 -> copy wsdl and register subsystem in cs**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_system_settings_view`
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.copy_wsdl_addresses_in_cs`, *u'cs_url'*
            * **Step 21: register subsystem in central server**
                * :func:`~common_lib.component_cs_system_settings.Component_cs_system_settings.register_subsystem_system_settings_in_cs`, *u'member_mgm_configuration'*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
                * :func:`~common_lib.common_lib.Common_lib.sync_global_conf`, *TESTDATA[u'cs_url'][u'sync_timeout']*
            * **Step 22: add subsystem to security server**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss_mgm_url'*
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * :func:`~common_lib.component_ss_clients.Component_ss_clients.add_from_search_existing_client_in_ss`, *u'member_mgm_configuration'*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 23: add wsdl service to security server subsystem**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss_mgm_url'*
                * :func:`~common_lib.component_ss_clients.Component_ss_clients.open_clients_details_dlg_with_subsystem_code`, *u'member_mgm_configuration'*
                * :func:`~common_lib.component_ss_services.Component_ss_services.add_new_wsdl`, *u'cs_url'*
                * :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_wsdl_enable`
                * :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.open_wsdl_service`
            * **Step 24: add management service parameters to auth cert deletion**
                * :func:`~common_lib.component_ss_services.Component_ss_services.edit_wsdl_service_parameters_in_ss`, *u'wsdl_service_auth_cert_deletion'*, *u'service_wsdl_auth_cert_deletion'*, *u'cs_url'*, *u'service_mgm_address'*
                * :func:`~common_lib.component_ss_services.Component_ss_services.add_service_access_rights_to_all_in_ss`
            * **Step 25: add management service parameters to client deletion**
                * :func:`~common_lib.component_ss_services.Component_ss_services.edit_wsdl_service_parameters_in_ss`, *u'wsdl_service_client_deletion'*, *u'service_wsdl_client_deletion'*, *u'cs_url'*, *u'service_mgm_address'*
                * :func:`~common_lib.component_ss_services.Component_ss_services.add_service_access_rights_to_all_in_ss`
            * **Step 26: add management service parameters to auth client registration**
                * :func:`~common_lib.component_ss_services.Component_ss_services.edit_wsdl_service_parameters_in_ss`, *u'wsdl_service_client_reg'*, *u'service_wsdl_client_reg'*, *u'cs_url'*, *u'service_mgm_address'*
                * :func:`~common_lib.component_ss_services.Component_ss_services.add_service_access_rights_to_all_in_ss`
                * :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_close_services_dlg`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """

        # Step Read liityntapalvelin konfiguraatio parameters
        self.common_lib.read_keskuspalvelin_konfiguraatio_parameters(TESTDATA)

        # Step Initialize server and add new member in central server
        self.component_cs.login(u'cs_url', initial_conf=True)
        self.component_cs_system_settings.initialize_cs_server_config(u'cs_url')
        self.component_cs_system_settings.add_init_member_class(u'member_mgm_configuration')

        # Step Add CA certification services in central server
        self.component_cs_sidebar.open_certification_services_view()
        self.component_cs_cert_services.add_certification_service_and_upload_ca_root_to_cs(u'paths',
                                                                                           u'cs_url',
                                                                                           u'server_environment')

        # Step Add timestamping to central server
        self.component_cs_sidebar.open_timestamping_services_view()
        self.component_cs_tsp_services.add_timestamping_service_to_cs(u'paths', u'cs_url')

        # Step Add members to central server
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.add_member_to_cs(u'member_mgm_configuration')

        # Step Add subsystem code to central server
        self.component_cs_members.add_new_subsystem_to_existing_member_in_cs(u'member_mgm_configuration')

        # Step Edit management service in central server
        self.component_cs_sidebar.open_system_settings_view()
        self.component_cs_system_settings.edit_mgm_service_provider_in_cs(u'member_mgm_configuration')

        # Step Set global conf internal conf key in central server
        self.component_cs_sidebar.open_global_configuration_view()
        self.component_cs_conf_mgm.generate_config_key(key_type="internal")
        self.component_cs_conf_mgm.try_insert_pin_code(u'cs_url')
        self.common_utils.wait_until_jquery_ajax_loaded()

        # Step Set global conf external key in central server
        self.cs_conf_mgm.click_link_external_configuration()
        self.component_cs_conf_mgm.generate_config_key(key_type="external")

        ## Might show double pin dialog
        self.component_cs_conf_mgm.try_insert_pin_code(u'cs_url')
        self.common_utils.wait_until_jquery_ajax_loaded()

        # Step set OCSP responder in central server
        self.component_cs_sidebar.open_certification_services_view()
        self.component_cs_cert_services.add_new_ocsp_responder(u'cs_url')
        self.common_lib.log_out()
        sleep(30)

        # Step Download anchor from central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_global_configuration_view()
        self.component_cs_conf_mgm.download_source_anchor_from_cs()
        self.common_lib.log_out()

        # Step Import configuration anchor to security server
        self.component_ss.login(u'ss_mgm_url', initial_conf=True)
        self.component_ss_initial_conf.import_configuration_anchor(u'paths')
        self.component_ss_initial_conf.add_initial_server_configuration_values_to_ss(u'member_mgm_configuration', u'ss_mgm_url')

        # Step Verify token active in security server
        self.ss_sidebar.verify_sidebar_title()
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed(u'ss_mgm_url')

        # Step Add timestamping services to security server
        self.ss_sidebar.verify_sidebar_title()
        self.component_ss_sidebar.open_system_parameters_view()
        self.component_ss.add_timestamping_url_to_ss(u'ss_mgm_url')

        # Step Add sign certificate to security server
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.sign_key_label)
        self.component_ss_keys_and_certs.generate_sign_certificate_request_in_ss(u'member_mgm_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_sign(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("sign")
        self.component_ss_keys_and_certs.verify_uploaded_certificate("sign")

        # Step Add auth certificate to security server
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.auth_key_label)
        self.component_ss_keys_and_certs.generate_auth_certificate_request_in_ss(u'member_mgm_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_auth(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("auth")
        cert_number = self.component_ss_keys_and_certs.verify_uploaded_certificate("auth")[0]
        key_auth_name = strings.server_environment_approved_ca() + " " + str(cert_number)

        # Step Register request auth certificate and activate
        self.component_ss_keys_and_certs.register_auth_certificate_in_ss(key_auth_name, u'member_mgm_configuration')
        self.ss_keys_and_cert.click_cert_activate()
        # Step Log out securityserver
        self.common_lib.log_out()

        # Step Accept auth key request in central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.accept_auth_certificate_request_in_cs(u'member_mgm_configuration')

        # Step8 Copy WSDL addressitle PHASE 17 -> COPY WSDL AND REGISTER SUBSYSTEM IN CS
        self.component_cs_sidebar.open_system_settings_view()
        self.component_cs_system_settings.copy_wsdl_addresses_in_cs(u'cs_url')

        # Step Register subsystem in central server
        self.component_cs_system_settings.register_subsystem_system_settings_in_cs(u'member_mgm_configuration')
        self.common_lib.log_out()
        self.common_lib.sync_global_conf(TESTDATA[u'cs_url'][u'sync_timeout'])

        # Step Add subsystem to security server
        self.component_ss.login(u'ss_mgm_url')
        self.ss_sidebar.verify_sidebar_title()
        self.component_ss_clients.add_from_search_existing_client_in_ss(u'member_mgm_configuration')
        sleep(2)
        self.common_lib.log_out()
        print("waiting while")
        sleep(30)

        # Step Add WSDL service to security server subsystem
        self.component_ss.login(u'ss_mgm_url')
        self.component_ss_clients.open_clients_details_dlg_with_subsystem_code(u'member_mgm_configuration')
        self.component_ss_services.add_new_wsdl(u'cs_url')
        self.ss_clients_dlg_services.click_wsdl_enable()
        sleep(2)
        self.ss_clients_dlg_services.open_wsdl_service()

        # Step Add management service parameters to auth cert deletion
        self.component_ss_services.edit_wsdl_service_parameters_in_ss(u'wsdl_service_auth_cert_deletion', u'service_wsdl_auth_cert_deletion', u'cs_url', u'service_mgm_address')
        self.component_ss_services.add_service_access_rights_to_all_in_ss()

        # Step Add management service parameters to client deletion
        self.component_ss_services.edit_wsdl_service_parameters_in_ss(u'wsdl_service_client_deletion', u'service_wsdl_client_deletion', u'cs_url', u'service_mgm_address')
        self.component_ss_services.add_service_access_rights_to_all_in_ss()

        # Step Add management service parameters to auth client registration
        self.component_ss_services.edit_wsdl_service_parameters_in_ss(u'wsdl_service_client_reg', u'service_wsdl_client_reg', u'cs_url', u'service_mgm_address')
        self.component_ss_services.add_service_access_rights_to_all_in_ss()
        self.ss_clients_dlg_services.click_close_services_dlg()
        self.common_lib.log_out()
        sleep(2)

    def test_configure_ss_server_with_new_member_add_to_existing_cs_3(self):
        """
        Configure security server with new member and add to existing central server

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: read liityntapalvelin konfiguraatio parameters**
                * :func:`~common_lib.common_lib.Common_lib.read_liityntapalvelin_konfiguraatio_parameters`, *TESTDATA*
            * **Step 2: add new member to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.add_member_to_cs`, *u'member1_configuration'*
            * **Step 3: add new subsystem to to existing member**
                * :func:`~common_lib.component_cs_members.Component_cs_members.add_new_subsystem_to_existing_member_in_cs`, *u'member1_configuration'*
            * **Step 4: download anchor from central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.download_source_anchor_from_cs`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 5: import configuration anchor to security server**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*, *initial_conf=True*
                * :func:`~common_lib.component_ss_initial_conf.Component_ss_initial_conf.import_configuration_anchor`, *u'paths'*
                * :func:`~common_lib.component_ss_initial_conf.Component_ss_initial_conf.add_initial_server_configuration_values_to_ss`, *u'member1_configuration'*, *u'ss1_url'*
            * **Step 6: verify and insert pin if needed in security server**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed`, *u'ss1_url'*
            * **Step 7: add timestamping services to security server**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_system_parameters_view`
                * :func:`~common_lib.component_ss.Component_ss.add_timestamping_url_to_ss`, *u'ss1_url'*
            * **Step 8: add sign certificate to security server**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss`, *strings.sign_key_label*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_sign_certificate_request_in_ss`, *u'member1_configuration'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_key_and_sign_certificate_sign`, *u'paths'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.import_and_upload_key_certificate`, *"sign"*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_uploaded_certificate`, *"sign"*
            * **Step 9: add auth certificate to security server**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss`, *strings.auth_key_label*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_auth_certificate_request_in_ss`, *u'member1_configuration'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_key_and_sign_certificate_auth`, *u'paths'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.import_and_upload_key_certificate`, *"auth"*
            * **Step 10: register request auth certificate and activate**
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.register_auth_certificate_in_ss`, *key_auth_name*, *u'member1_configuration'*
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_cert_activate`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 11: accept auth key request in central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.accept_auth_certificate_request_in_cs`, *u'member1_configuration'*
            * **Step 12: get wsdl address**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_system_settings_view`
            * **Step 13: get wsdl and services address #webpage: cs_system_settings**
                * :func:`~pagemodel.cs_system_settings.Cs_system_settings.get_wsdl_and_services_address`, *TESTDATA[u'cs_url']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 14: add subsystem to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.new_client_registration_request_in_cs`, *u'member1_configuration'*
                * :func:`~pagemodel.cs_sec_servers_mgm_requests.Cs_sec_servers_mgm_requests.click_close_mgm_req_dlg`
                * :func:`~common_lib.component_cs_members.Component_cs_members.close_member_details_dlg`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
                * :func:`~common_lib.common_lib.Common_lib.sync_global_conf`, *TESTDATA[u'ss1_url'][u'sync_timeout']*
            * **Step 15: add subsystem to security server**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
                * :func:`~common_lib.component_ss_clients.Component_ss_clients.add_new_subsystem_to_ss`, *u'member1_configuration'*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
                * :func:`~common_lib.common_lib.Common_lib.sync_global_conf`, *TESTDATA[u'ss1_url'][u'sync_timeout']*
            * **Step 16: accept subsystem in in central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.accept_mgm_requests_in_cs`, *u'member1_configuration'*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 17: check registration complete**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
            * **Step 18: check service registration complete #webpage: ss_clients #parameters: server_configuration**
                * :func:`~pagemodel.ss_clients.Ss_clients.verify_service_registration_complete`, *TESTDATA[u'member1_configuration']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Read liityntapalvelin konfiguraatio parameters
        self.common_lib.read_liityntapalvelin_konfiguraatio_parameters(TESTDATA)

        # Step Add new member to central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.add_member_to_cs(u'member1_configuration')

        # Step Add new subsystem to to existing member
        self.component_cs_members.add_new_subsystem_to_existing_member_in_cs(u'member1_configuration')

        # Step Download anchor from central server
        self.component_cs_sidebar.open_global_configuration_view()
        self.component_cs_conf_mgm.download_source_anchor_from_cs()
        self.common_lib.log_out()

        print("Waiting server sync time that member name can be found on security server")
        sleep(41)

        # Step Import configuration anchor to security server
        self.component_ss.login(u'ss1_url', initial_conf=True)
        self.component_ss_initial_conf.import_configuration_anchor(u'paths')
        self.component_ss_initial_conf.add_initial_server_configuration_values_to_ss(u'member1_configuration', u'ss1_url')

        # Step Verify and insert pin if needed in security server
        self.ss_sidebar.verify_sidebar_title()
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed(u'ss1_url')

        # Step Add timestamping services to security server
        self.component_ss_sidebar.open_system_parameters_view()
        self.component_ss.add_timestamping_url_to_ss(u'ss1_url')

        # Step Add sign certificate to security server
        self.ss_sidebar.verify_sidebar_title()
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.sign_key_label)
        self.component_ss_keys_and_certs.generate_sign_certificate_request_in_ss(u'member1_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_sign(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("sign")
        self.component_ss_keys_and_certs.verify_uploaded_certificate("sign")

        # Step Add auth certificate to security server
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.auth_key_label)
        self.component_ss_keys_and_certs.generate_auth_certificate_request_in_ss(u'member1_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_auth(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("auth")
        cert_number = self.component_ss_keys_and_certs.verify_uploaded_certificate("auth")[0]
        key_auth_name = strings.server_environment_approved_ca() + " " + str(cert_number)

        # Step Register request auth certificate and activate
        self.component_ss_keys_and_certs.register_auth_certificate_in_ss(key_auth_name, u'member1_configuration')
        self.ss_keys_and_cert.click_cert_activate()
        self.common_lib.log_out()

        # Step Accept auth key request in central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.accept_auth_certificate_request_in_cs(u'member1_configuration')

        # Step Get WSDL address
        self.component_cs_sidebar.open_system_settings_view()
        # Step Get wsdl and services address #Webpage: cs_system_settings
        self.cs_system_settings.get_wsdl_and_services_address(TESTDATA[u'cs_url'])
        self.common_lib.log_out()
        #self.common_lib.sync_global_conf(self.parameters[u'central_server_configuration'][u'sync_timeout'])

        # Step Add subsystem to central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.new_client_registration_request_in_cs(u'member1_configuration')
        self.cs_sec_servers_mgm_requests.click_close_mgm_req_dlg()
        self.component_cs_members.close_member_details_dlg()
        self.common_lib.log_out()
        # Sync global conf timeout
        self.common_lib.sync_global_conf(TESTDATA[u'ss1_url'][u'sync_timeout'])

        # Step Add subsystem to security server
        self.component_ss.login(u'ss1_url')
        self.component_ss_clients.add_new_subsystem_to_ss(u'member1_configuration')
        # Sync global conf timeout
        self.common_lib.log_out()
        self.common_lib.sync_global_conf(TESTDATA[u'ss1_url'][u'sync_timeout'])

        # Step Accept subsystem in in central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.accept_mgm_requests_in_cs(u'member1_configuration')
        self.common_lib.log_out()

        # Step Check registration complete
        self.component_ss.login(u'ss1_url')
        self.ss_sidebar.verify_sidebar_title()
        # Step Check service registration complete #Webpage: ss_clients #Parameters: server_configuration
        self.ss_clients.verify_service_registration_complete(TESTDATA[u'member1_configuration'])
        self.common_lib.log_out()

    def test_configure_ss_server_with_new_member_add_to_existing_cs_4(self):
        """
        Configure security server with new member and add to existing central server

        *Updated: 11.07.2017*

        **Test steps:**
            * **Step 1: read liityntapalvelin konfiguraatio parameters**
                * :func:`~common_lib.common_lib.Common_lib.read_liityntapalvelin_konfiguraatio_parameters`, *TESTDATA*
            * **Step 2: add new member to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.add_member_to_cs`, *u'member2_configuration'*
            * **Step 3: add new subsystem to to existing member**
                * :func:`~common_lib.component_cs_members.Component_cs_members.add_new_subsystem_to_existing_member_in_cs`, *u'member2_configuration'*
            * **Step 4: download anchor from central server**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
                * :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.download_source_anchor_from_cs`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 5: import configuration anchor to security server**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss2_url'*, *initial_conf=True*
                * :func:`~common_lib.component_ss_initial_conf.Component_ss_initial_conf.import_configuration_anchor`, *u'paths'*
                * :func:`~common_lib.component_ss_initial_conf.Component_ss_initial_conf.add_initial_server_configuration_values_to_ss`, *u'member2_configuration'*, *u'ss2_url'*
            * **Step 6: verify and insert pin if needed in security server**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed`, *u'ss2_url'*
            * **Step 7: add timestamping services to security server**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_system_parameters_view`
                * :func:`~common_lib.component_ss.Component_ss.add_timestamping_url_to_ss`, *u'ss2_url'*
            * **Step 8: add sign certificate to security server**
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss`, *strings.sign_key_label*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_sign_certificate_request_in_ss`, *u'member2_configuration'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_key_and_sign_certificate_sign`, *u'paths'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.import_and_upload_key_certificate`, *"sign"*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_uploaded_certificate`, *"sign"*
            * **Step 9: add auth certificate to security server**
                * :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss`, *strings.auth_key_label*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.generate_auth_certificate_request_in_ss`, *u'member2_configuration'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.verify_key_and_sign_certificate_auth`, *u'paths'*
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.import_and_upload_key_certificate`, *"auth"*
            * **Step 10: register request auth certificate and activate**
                * :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.register_auth_certificate_in_ss`, *key_auth_name*, *u'member2_configuration'*
                * :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_cert_activate`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 11: accept auth key request in central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.accept_auth_certificate_request_in_cs`, *u'member2_configuration'*
            * **Step 12: get wsdl address**
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_system_settings_view`
            * **Step 13: get wsdl and services address #webpage: cs_system_settings**
                * :func:`~pagemodel.cs_system_settings.Cs_system_settings.get_wsdl_and_services_address`, *TESTDATA[u'cs_url']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 14: add subsystem to central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.new_client_registration_request_in_cs`, *u'member2_configuration'*
                * :func:`~pagemodel.cs_sec_servers_mgm_requests.Cs_sec_servers_mgm_requests.click_close_mgm_req_dlg`
                * :func:`~common_lib.component_cs_members.Component_cs_members.close_member_details_dlg`
                * :func:`~common_lib.common_lib.Common_lib.log_out`
                * :func:`~common_lib.common_lib.Common_lib.sync_global_conf`, *TESTDATA[u'ss2_url'][u'sync_timeout']*
            * **Step 15: add subsystem to security server**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss2_url'*
                * :func:`~common_lib.component_ss_clients.Component_ss_clients.add_new_subsystem_to_ss`, *u'member2_configuration'*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
                * :func:`~common_lib.common_lib.Common_lib.sync_global_conf`, *TESTDATA[u'ss2_url'][u'sync_timeout']*
            * **Step 16: accept subsystem in in central server**
                * :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*
                * :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_members_view`
                * :func:`~common_lib.component_cs_members.Component_cs_members.accept_mgm_requests_in_cs`, *u'member2_configuration'*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
            * **Step 17: check registration complete**
                * :func:`~common_lib.component_ss.Component_ss.login`, *u'ss2_url'*
                * :func:`~pagemodel.ss_sidebar.Ss_sidebar.verify_sidebar_title`
            * **Step 18: check service registration complete #webpage: ss_clients #parameters: server_configuration**
                * :func:`~pagemodel.ss_clients.Ss_clients.verify_service_registration_complete`, *TESTDATA[u'member2_configuration']*
                * :func:`~common_lib.common_lib.Common_lib.log_out`
        """
        # Step Read liityntapalvelin konfiguraatio parameters
        self.common_lib.read_liityntapalvelin_konfiguraatio_parameters(TESTDATA)

        # Step Add new member to central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.add_member_to_cs(u'member2_configuration')

        # Step Add new subsystem to to existing member
        self.component_cs_members.add_new_subsystem_to_existing_member_in_cs(u'member2_configuration')

        # Step Download anchor from central server
        self.component_cs_sidebar.open_global_configuration_view()
        self.component_cs_conf_mgm.download_source_anchor_from_cs()
        self.common_lib.log_out()

        print("Waiting server sync time that member name can be found on security server")
        sleep(40)

        # Step Import configuration anchor to security server
        self.component_ss.login(u'ss2_url', initial_conf=True)
        self.component_ss_initial_conf.import_configuration_anchor(u'paths')
        self.component_ss_initial_conf.add_initial_server_configuration_values_to_ss(u'member2_configuration', u'ss2_url')

        # Step Verify and insert pin if needed in security server
        self.ss_sidebar.verify_sidebar_title()
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed(u'ss2_url')

        # Step Add timestamping services to security server
        self.component_ss_sidebar.open_system_parameters_view()
        self.component_ss.add_timestamping_url_to_ss(u'ss2_url')

        # Step Add sign certificate to security server
        self.ss_sidebar.verify_sidebar_title()
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.sign_key_label)
        self.component_ss_keys_and_certs.generate_sign_certificate_request_in_ss(u'member2_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_sign(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("sign")
        self.component_ss_keys_and_certs.verify_uploaded_certificate("sign")

        # Step Add auth certificate to security server
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.generate_and_select_certificate_key_in_ss(strings.auth_key_label)
        self.component_ss_keys_and_certs.generate_auth_certificate_request_in_ss(u'member2_configuration')
        self.component_ss_keys_and_certs.verify_key_and_sign_certificate_auth(u'paths')
        self.component_ss_keys_and_certs.import_and_upload_key_certificate("auth")
        cert_number = self.component_ss_keys_and_certs.verify_uploaded_certificate("auth")[0]
        key_auth_name = strings.server_environment_approved_ca() + " " + str(cert_number)

        # Step Register request auth certificate and activate
        self.component_ss_keys_and_certs.register_auth_certificate_in_ss(key_auth_name, u'member2_configuration')
        self.ss_keys_and_cert.click_cert_activate()
        self.common_lib.log_out()

        # Step Accept auth key request in central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.accept_auth_certificate_request_in_cs(u'member2_configuration')

        # Step Get WSDL address
        self.component_cs_sidebar.open_system_settings_view()
        # Step Get wsdl and services address #Webpage: cs_system_settings
        self.cs_system_settings.get_wsdl_and_services_address(TESTDATA[u'cs_url'])
        self.common_lib.log_out()
        # self.common_lib.sync_global_conf(self.parameters[u'central_server_configuration'][u'sync_timeout'])

        # Step Add subsystem to central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.new_client_registration_request_in_cs(u'member2_configuration')
        self.cs_sec_servers_mgm_requests.click_close_mgm_req_dlg()
        self.component_cs_members.close_member_details_dlg()
        self.common_lib.log_out()
        # Sync global conf timeout
        self.common_lib.sync_global_conf(TESTDATA[u'ss2_url'][u'sync_timeout'])

        # Step Add subsystem to security server
        self.component_ss.login(u'ss2_url')
        self.component_ss_clients.add_new_subsystem_to_ss(u'member2_configuration')
        # Sync global conf timeout
        self.common_lib.log_out()
        self.common_lib.sync_global_conf(TESTDATA[u'ss2_url'][u'sync_timeout'])

        # Step Accept subsystem in in central server
        self.component_cs.login(u'cs_url')
        self.component_cs_sidebar.open_members_view()
        self.component_cs_members.accept_mgm_requests_in_cs(u'member2_configuration')
        self.common_lib.log_out()

        # Step Check registration complete
        self.component_ss.login(u'ss2_url')
        self.ss_sidebar.verify_sidebar_title()
        # Step Check service registration complete #Webpage: ss_clients #Parameters: server_configuration
        self.ss_clients.verify_service_registration_complete(TESTDATA[u'member2_configuration'])
        self.common_lib.log_out()