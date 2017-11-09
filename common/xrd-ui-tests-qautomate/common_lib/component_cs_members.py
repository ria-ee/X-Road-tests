# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_all_parameters
from time import sleep
import os
from common_lib import Common_lib
from pagemodel.cs_members import Cs_members
from pagemodel.cs_members_owned_auth_cert_reg_dlg import Cs_members_owned_auth_cert_reg_dlg
from pagemodel.cs_members_subsystems_dlg import Cs_members_subsystems_dlg
from pagemodel.cs_sec_servers_new_client_req_search import Cs_sec_servers_new_client_req_search
from pagemodel.cs_sec_servers_details import Cs_sec_servers_details
from pagemodel.cs_member_details_owned_servers import Cs_member_details_owned_servers
from pagemodel.cs_sec_servers_details_clients import Cs_sec_servers_details_clients
from pagemodel.cs_sec_servers_new_client_req import Cs_sec_servers_new_client_req
from pagemodel.cs_add_member_dlg import Cs_add_member_dlg
from pagemodel.ss_keys_and_cert import Ss_keys_and_cert
from pagemodel.cs_sec_servers import Cs_sec_servers
from pagemodel.cs_sec_servers_mgm_request_app_conf import Cs_sec_servers_mgm_request_app_conf
from pagemodel.ss_keys_and_cert_dlg_import_cert import Ss_keys_and_cert_dlg_import_cert
from pagemodel.cs_members_add_subsystem_dlg import Cs_members_add_subsystem_dlg
from pagemodel.cs_sec_serves_mgm_request_approve import Cs_sec_serves_mgm_request_approve
from pagemodel.cs_members_mgm_requests_dlg import Cs_members_mgm_requests_dlg
from pagemodel.cs_remove_member_dlg import Cs_remove_member_dlg
from pagemodel.cs_members_details_dlg import Cs_members_details_dlg
from pagemodel.cs_sec_servers_mgm_requests import Cs_sec_servers_mgm_requests

class Component_cs_members(CommonUtils):
    """
    Components common to central server members view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    parameters = get_all_parameters()
    common_lib = Common_lib()
    cs_members = Cs_members()
    cs_members_owned_auth_cert_reg_dlg = Cs_members_owned_auth_cert_reg_dlg()
    cs_members_subsystems_dlg = Cs_members_subsystems_dlg()
    cs_sec_servers_new_client_req_search = Cs_sec_servers_new_client_req_search()
    cs_sec_servers_details = Cs_sec_servers_details()
    cs_member_details_owned_servers = Cs_member_details_owned_servers()
    cs_sec_servers_details_clients = Cs_sec_servers_details_clients()
    cs_sec_servers_new_client_req = Cs_sec_servers_new_client_req()
    cs_add_member_dlg = Cs_add_member_dlg()
    ss_keys_and_cert = Ss_keys_and_cert()
    cs_sec_servers = Cs_sec_servers()
    cs_sec_servers_mgm_request_app_conf = Cs_sec_servers_mgm_request_app_conf()
    ss_keys_and_cert_dlg_import_cert = Ss_keys_and_cert_dlg_import_cert()
    cs_members_add_subsystem_dlg = Cs_members_add_subsystem_dlg()
    cs_sec_serves_mgm_request_approve = Cs_sec_serves_mgm_request_approve()
    cs_members_mgm_requests_dlg = Cs_members_mgm_requests_dlg()
    cs_remove_member_dlg = Cs_remove_member_dlg()
    cs_members_details_dlg = Cs_members_details_dlg()
    cs_sec_servers_mgm_requests = Cs_sec_servers_mgm_requests()

    def make_cert_file_upload(self, parameters="sign"):
        """
        Upload ceritificate file

        *Updated: 11.07.2017*

        :param parameters:  Test data section dictionary
        
        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *str(type_string*
        """
        sleep(6)
        path = os.getcwd() + "/scripts/" + parameters + "-cert_automation.der"
        print(path)
        type_string = path
        self.common_lib.type_file_name_pyautogui(str(type_string))
        print("done upload")
        sleep(2)

    def open_member_details_dlg(self, section=u'member_mgm_configuration', parameter=u'member_name'):
        """
        Open memeber details dialog

        *Updated: 11.07.2017*

        :param section:  Test data section name
        :param parameter:  Test data parameter name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_members.Cs_members.click_element_from_table_members`, *TESTDATA[section][parameter]*
                * **Step 2:** :func:`~pagemodel.cs_members.Cs_members.click_button_member_action`
        """
        self.cs_members.click_element_from_table_members(TESTDATA[section][parameter])
        self.cs_members.click_button_member_action()

    def close_member_details_dlg(self):
        """
        Close member details dialog

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_button_close`
        """
        self.cs_members_details_dlg.click_button_close()

    def add_new_subsystem_to_existing_member_in_cs(self, section=u'member_mgm_configuration'):
        """
        Add new subsystem to existing member in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 2:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_subsystems_tab`
                * **Step 3:** :func:`~pagemodel.cs_members_subsystems_dlg.Cs_members_subsystems_dlg.click_button_add`
                * **Step 4:** :func:`~pagemodel.cs_members_add_subsystem_dlg.Cs_members_add_subsystem_dlg.input_text_to_id_subsystem_add_code`, *TESTDATA[section]*
                * **Step 5:** :func:`~pagemodel.cs_members_add_subsystem_dlg.Cs_members_add_subsystem_dlg.click_button_id_subsystem_add_submit`
                * **Step 6:** :func:`~pagemodel.cs_members_subsystems_dlg.Cs_members_subsystems_dlg.click_button_submit`
        """
        self.wait_until_jquery_ajax_loaded()
        self.cs_members_details_dlg.click_subsystems_tab()
        self.cs_members_subsystems_dlg.click_button_add()
        self.cs_members_add_subsystem_dlg.input_text_to_id_subsystem_add_code(TESTDATA[section])
        self.cs_members_add_subsystem_dlg.click_button_id_subsystem_add_submit()
        self.cs_members_subsystems_dlg.click_button_submit()
        #self.common_lib.get_ui_error_message()

    def add_member_to_cs(self, section=u'member_mgm_configuration'):
        """
        Add member to central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_members.Cs_members.click_button_group_add_icon`
                * **Step 2:** :func:`~pagemodel.cs_add_member_dlg.Cs_add_member_dlg.fill_input_add_member`, *TESTDATA[section]*
                * **Step 3:** :func:`~pagemodel.cs_add_member_dlg.Cs_add_member_dlg.click_button_ok_0`
        """
        self.cs_members.click_button_group_add_icon()
        self.cs_add_member_dlg.fill_input_add_member(TESTDATA[section])
        self.cs_add_member_dlg.click_button_ok_0()

    def delete_member_in_member_details_dlg(self):
        """
        Delete member in member details dialog

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_member_detail_tab`
                * **Step 2:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_button_delete`
                * **Step 3:** :func:`~pagemodel.cs_remove_member_dlg.Cs_remove_member_dlg.click_link_confirm_ui_text`
        """
        self.cs_members_details_dlg.click_member_detail_tab()
        self.cs_members_details_dlg.click_button_delete()
        self.cs_remove_member_dlg.click_link_confirm_ui_text()

    def new_client_registration_request_in_cs(self, section=u'member_mgm_configuration'):
        """
        New client registeration request in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 2:** :func:`~pagemodel.cs_members.Cs_members.wait_until_element_is_visible_member_name`
                * **Step 3:** :func:`~pagemodel.cs_members.Cs_members.search_text_from_table_members`, *TESTDATA[section]*
                * **Step 4:** :func:`~pagemodel.cs_members.Cs_members.click_button_member_action`
                * **Step 5:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_element_owned_servers`
                * **Step 6:** :func:`~pagemodel.cs_member_details_owned_servers.Cs_member_details_owned_servers.click_element_owned_server`, *TESTDATA[section]*
                * **Step 7:** :func:`~pagemodel.cs_sec_servers_details.Cs_sec_servers_details.click_clients_tab`
                * **Step 8:** :func:`~pagemodel.cs_sec_servers_details_clients.Cs_sec_servers_details_clients.click_add_new_client_request`
                * **Step 9:** :func:`~pagemodel.cs_sec_servers_new_client_req.Cs_sec_servers_new_client_req.click_new_client_search`
                * **Step 10:** :func:`~pagemodel.cs_sec_servers_new_client_req_search.Cs_sec_servers_new_client_req_search.click_member_from_table`, *TESTDATA[section]['member_name']*
                * **Step 11:** :func:`~pagemodel.cs_sec_servers_new_client_req_search.Cs_sec_servers_new_client_req_search.click_ok_search`
                * **Step 12:** :func:`~pagemodel.cs_sec_servers_new_client_req.Cs_sec_servers_new_client_req.insert_subsystem_code`, *TESTDATA[section]*
                * **Step 13:** :func:`~pagemodel.cs_sec_servers_new_client_req.Cs_sec_servers_new_client_req.click_submit_new_client_request`
                * **Step 14:** :func:`~pagemodel.cs_sec_servers_details.Cs_sec_servers_details.click_mgm_requests_tab`
        """
        self.wait_until_jquery_ajax_loaded()
        self.cs_members.wait_until_element_is_visible_member_name()
        self.cs_members.search_text_from_table_members(TESTDATA[section])
        self.cs_members.click_button_member_action()
        self.cs_members_details_dlg.click_element_owned_servers()
        self.cs_member_details_owned_servers.click_element_owned_server(TESTDATA[section])
        self.cs_sec_servers_details.click_clients_tab()
        self.cs_sec_servers_details_clients.click_add_new_client_request()
        self.cs_sec_servers_new_client_req.click_new_client_search()
        self.cs_sec_servers_new_client_req_search.click_member_from_table(TESTDATA[section]['member_name'])
        self.cs_sec_servers_new_client_req_search.click_ok_search()
        self.cs_sec_servers_new_client_req.insert_subsystem_code(TESTDATA[section])
        self.cs_sec_servers_new_client_req.click_submit_new_client_request()
        sleep(3)
        self.cs_sec_servers_details.click_mgm_requests_tab()
        sleep(2)

    def accept_mgm_requests_in_cs(self, section=u'member_mgm_configuration'):
        """
        Accept management request in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_members.Cs_members.search_text_from_table_members`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.cs_members.Cs_members.click_button_member_action`
                * **Step 3:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_element_management_requests_tab`
                * **Step 4:** :func:`~pagemodel.cs_members_mgm_requests_dlg.Cs_members_mgm_requests_dlg.find_and_click_mgm_request`
                * **Step 5:** :func:`~pagemodel.cs_sec_serves_mgm_request_approve.Cs_sec_serves_mgm_request_approve.click_approve_request`
                * **Step 6:** :func:`~pagemodel.cs_sec_servers_mgm_request_app_conf.Cs_sec_servers_mgm_request_app_conf.click_confirm_approve_request`
                * **Step 7:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_button_close`
        """
        self.cs_members.search_text_from_table_members(TESTDATA[section])
        sleep(1)
        self.cs_members.click_button_member_action()
        self.cs_members_details_dlg.click_element_management_requests_tab()
        sleep(1)
        self.cs_members_mgm_requests_dlg.find_and_click_mgm_request()
        self.cs_sec_serves_mgm_request_approve.click_approve_request()
        sleep(1)
        self.cs_sec_servers_mgm_request_app_conf.click_confirm_approve_request()
        sleep(3)
        self.cs_members_details_dlg.click_button_close()

    def accept_mgm_request_security_servers_in_cs(self):
        """
        Accept management request security servers in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sec_servers_mgm_requests.Cs_sec_servers_mgm_requests.find_and_click_mgm_request`
                * **Step 2:** :func:`~pagemodel.cs_sec_serves_mgm_request_approve.Cs_sec_serves_mgm_request_approve.click_approve_request`
                * **Step 3:** :func:`~pagemodel.cs_sec_servers_mgm_request_app_conf.Cs_sec_servers_mgm_request_app_conf.click_confirm_approve_request`
                * **Step 4:** :func:`~pagemodel.cs_sec_servers_mgm_requests.Cs_sec_servers_mgm_requests.click_close_mgm_req_dlg`
        """
        self.cs_sec_servers_mgm_requests.find_and_click_mgm_request()
        self.cs_sec_serves_mgm_request_approve.click_approve_request()
        self.cs_sec_servers_mgm_request_app_conf.click_confirm_approve_request()
        self.cs_sec_servers_mgm_requests.click_close_mgm_req_dlg()

    def accept_auth_certificate_request_in_cs(self, section=u'member_mgm_configuration'):
        """
        Accept authentication certificate request in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 2:** :func:`~pagemodel.cs_members.Cs_members.wait_until_element_is_visible_member_name`
                * **Step 3:** :func:`~pagemodel.cs_members.Cs_members.search_text_from_table_members`, *TESTDATA[section]*
                * **Step 4:** :func:`~pagemodel.cs_members.Cs_members.click_button_member_action`
                * **Step 5:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_element_owned_servers`
                * **Step 6:** :func:`~pagemodel.cs_member_details_owned_servers.Cs_member_details_owned_servers.click_button_ui_titlebar_widget_corner_all_helper_clearfix_draggable_handle_tabs`
                * **Step 7:** :func:`~pagemodel.cs_members_owned_auth_cert_reg_dlg.Cs_members_owned_auth_cert_reg_dlg.click_element_id_owned_server_cert_upload_button`
                * **Step 9:** :func:`~pagemodel.cs_members_owned_auth_cert_reg_dlg.Cs_members_owned_auth_cert_reg_dlg.input_text_to_id_owned_server_add_servercode`, *TESTDATA[section]*
                * **Step 10:** :func:`~pagemodel.cs_members_owned_auth_cert_reg_dlg.Cs_members_owned_auth_cert_reg_dlg.click_button_id_add_owned_server_submit`
                * **Step 11:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.wait_until_submitted_certificate`
                * **Step 12:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_element_management_requests_tab`
                * **Step 13:** :func:`~pagemodel.cs_members_mgm_requests_dlg.Cs_members_mgm_requests_dlg.find_and_click_mgm_request`
                * **Step 14:** :func:`~pagemodel.cs_sec_serves_mgm_request_approve.Cs_sec_serves_mgm_request_approve.click_approve_request`
                * **Step 15:** :func:`~pagemodel.cs_sec_servers_mgm_request_app_conf.Cs_sec_servers_mgm_request_app_conf.click_confirm_approve_request`
                * **Step 16:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_button_close`
        """
        self.wait_until_jquery_ajax_loaded()
        self.cs_members.wait_until_element_is_visible_member_name()
        self.cs_members.search_text_from_table_members(TESTDATA[section])
        self.cs_members.click_button_member_action()
        self.cs_members_details_dlg.click_element_owned_servers()
        self.cs_member_details_owned_servers.click_button_ui_titlebar_widget_corner_all_helper_clearfix_draggable_handle_tabs()
        self.cs_members_owned_auth_cert_reg_dlg.click_element_id_owned_server_cert_upload_button()
        self.make_cert_file_upload("auth")
        sleep(2)
        self.cs_members_owned_auth_cert_reg_dlg.input_text_to_id_owned_server_add_servercode(TESTDATA[section])
        self.cs_members_owned_auth_cert_reg_dlg.click_button_id_add_owned_server_submit()
        self.cs_members_details_dlg.wait_until_submitted_certificate()
        self.cs_members_details_dlg.click_element_management_requests_tab()
        sleep(3)
        self.cs_members_mgm_requests_dlg.find_and_click_mgm_request()
        self.cs_sec_serves_mgm_request_approve.click_approve_request()
        sleep(1)
        self.cs_sec_servers_mgm_request_app_conf.click_confirm_approve_request()
        sleep(3)
        self.cs_members_details_dlg.click_button_close()
        sleep(5)

    def verify_subsystem_is_removable_in_member_details_dlg(self, section=u'central_server_config', parameter=u'subsystem'):
        """
        Verify subsystem in removable in member details dialog

        *Updated: 11.07.2017*

        :param section:  Test data section name
        :param parameter:  Test data parameter name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_members_details_dlg.Cs_members_details_dlg.click_subsystems_tab`
                * **Step 2:** :func:`~pagemodel.cs_members_subsystems_dlg.Cs_members_subsystems_dlg.check_subsystem_is_red`, *TESTDATA[section][parameter]*
                * **Step 3:** :func:`~pagemodel.cs_members_subsystems_dlg.Cs_members_subsystems_dlg.click_element_in_subsystems_table`, *TESTDATA[section][parameter]*
                * **Step 4:** :func:`~pagemodel.cs_members_subsystems_dlg.Cs_members_subsystems_dlg.sub_delete_is_enabled`
        """
        self.cs_members_details_dlg.click_subsystems_tab()
        self.cs_members_subsystems_dlg.check_subsystem_is_red(TESTDATA[section][parameter])
        self.cs_members_subsystems_dlg.click_element_in_subsystems_table(TESTDATA[section][parameter])
        self.cs_members_subsystems_dlg.sub_delete_is_enabled()

    def verify_members_does_not_contain_member(self, section=u'central_server_config', parameter=u'member_name'):
        """
        Verify members does not conatin member

        *Updated: 11.07.2017*

        :param section:  Test data section name
        :param parameter:  Test data parameter name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_members.Cs_members.table_does_not_contain_member`, *TESTDATA[section][parameter]*
        """
        self.cs_members.table_does_not_contain_member(TESTDATA[section][parameter])

    def verify_members_does_contain_member(self, section=u'member_mgm_configuration', parameter=u'member_name'):
        """
        Verify members does contain member

        *Updated: 11.07.2017*

        :param section:  Test data section name
        :param parameter:  Test data parameter name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_members.Cs_members.table_contains_member`, *TESTDATA[section][parameter]*
        """
        self.cs_members.table_contains_member(TESTDATA[section][parameter])
