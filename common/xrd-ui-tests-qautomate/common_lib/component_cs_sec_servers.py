# -*- coding: utf-8 -*-
from variables import strings
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.cs_sec_servers import Cs_sec_servers
from pagemodel.cs_sec_servers_details_del_confirm import Cs_sec_servers_details_del_confirm
from pagemodel.cs_sec_servers_details import Cs_sec_servers_details
from pagemodel.cs_sec_servers_details_clients import Cs_sec_servers_details_clients
from pagemodel.cs_sec_servers_delete_clients import Cs_sec_servers_delete_clients
from pagemodel.cs_sec_servers_details_auth import Cs_sec_servers_details_auth
from pagemodel.cs_sec_servers_auth_dlg import Cs_sec_servers_auth_dlg
from pagemodel.ss_clients import Ss_clients

class Component_cs_sec_servers(CommonUtils):
    """
    Components common to central server security servers view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    cs_sec_servers = Cs_sec_servers()
    cs_sec_servers_details_del_confirm = Cs_sec_servers_details_del_confirm()
    cs_sec_servers_details = Cs_sec_servers_details()
    cs_sec_servers_details_clients = Cs_sec_servers_details_clients()
    cs_sec_servers_delete_clients = Cs_sec_servers_delete_clients()
    cs_sec_servers_details_auth = Cs_sec_servers_details_auth()
    cs_sec_servers_auth_dlg = Cs_sec_servers_auth_dlg()
    ss_clients = Ss_clients()

    def open_server_details_dlg(self, section=u'member_mgm_configuration', parameter=u'member_name'):
        """
        Open server details dialog

        *Updated: 11.07.2017*
        
        :param section:  Test data section name
        :param parameter:  Test data parameter name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sec_servers.Cs_sec_servers.click_security_servers_row_with_text`, *TESTDATA[section][parameter]*
                * **Step 2:** :func:`~pagemodel.cs_sec_servers.Cs_sec_servers.click_ss_details`
        """
        self.cs_sec_servers.click_security_servers_row_with_text(TESTDATA[section][parameter])
        self.cs_sec_servers.click_ss_details()

    def delete_server_in_server_details_dlg(self):
        """
        Delete server in server details dialog

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sec_servers_details.Cs_sec_servers_details.click_security_server_details_tab`
                * **Step 2:** :func:`~pagemodel.cs_sec_servers_details.Cs_sec_servers_details.click_element_id_securityserver_delete`
                * **Step 3:** :func:`~pagemodel.cs_sec_servers_details_del_confirm.Cs_sec_servers_details_del_confirm.click_link_confirm_ui_text`
        """
        self.cs_sec_servers_details.click_security_server_details_tab()
        self.cs_sec_servers_details.click_element_id_securityserver_delete()
        self.cs_sec_servers_details_del_confirm.click_link_confirm_ui_text()

    def delete_client_in_server_details_dlg(self, section=u'member_mgm_configuration'):
        """
        Delete client in server details in dialog

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sec_servers_details.Cs_sec_servers_details.click_clients_tab`
                * **Step 2:** :func:`~pagemodel.cs_sec_servers_details_clients.Cs_sec_servers_details_clients.search_text_from_table_securityserver_clients_1`, *TESTDATA[section]*
                * **Step 3:** :func:`~pagemodel.cs_sec_servers_details_clients.Cs_sec_servers_details_clients.click_element_id_securityserver_client_delete`
                * **Step 4:** :func:`~pagemodel.cs_sec_servers_delete_clients.Cs_sec_servers_delete_clients.click_element_submit`
        """
        self.cs_sec_servers_details.click_clients_tab()
        self.cs_sec_servers_details_clients.search_text_from_table_securityserver_clients_1(TESTDATA[section])
        self.cs_sec_servers_details_clients.click_element_id_securityserver_client_delete()
        self.cs_sec_servers_delete_clients.click_element_submit()

    def close_server_details_dlg(self):
        """
        Close server details dialog

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sec_servers_details_clients.Cs_sec_servers_details_clients.click_element_submit`
        """
        self.cs_sec_servers_details_clients.click_element_submit()

    def delete_auth_cert_in_server_details_dlg(self):
        """
        Delete authentication certification in server details dialog

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sec_servers_details_clients.Cs_sec_servers_details_clients.click_element_auth_cert`
                * **Step 2:** :func:`~pagemodel.cs_sec_servers_details_auth.Cs_sec_servers_details_auth.click_element_from_table_securityserver_auth_certs`, *approved_ca*
                * **Step 3:** :func:`~pagemodel.cs_sec_servers_details_auth.Cs_sec_servers_details_auth.click_button_id_securityserver_authcert_delete`
                * **Step 4:** :func:`~pagemodel.cs_sec_servers_auth_dlg.Cs_sec_servers_auth_dlg.click_element_submit`
        """
        approved_ca = strings.server_environment_approved_ca()
        self.cs_sec_servers_details_clients.click_element_auth_cert()
        self.cs_sec_servers_details_auth.click_element_from_table_securityserver_auth_certs(approved_ca)
        self.cs_sec_servers_details_auth.click_button_id_securityserver_authcert_delete()
        self.cs_sec_servers_auth_dlg.click_element_submit()

    def verify_servers_does_not_contain_server(self, section=u'member_mgm_configuration', parameter=u'member_name'):
        """
        Verify servers does not contain server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        :param parameter:  Test data parameter name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sec_servers.Cs_sec_servers.table_does_not_contain_server`, *TESTDATA[section][parameter]*
        """
        self.cs_sec_servers.table_does_not_contain_server(TESTDATA[section][parameter])

    def verify_servers_does_contain_server(self, section=u'member_mgm_configuration', parameter=u'member_name'):
        """
        Verify servers does contain server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        :param parameter:  Test data parameter name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sec_servers.Cs_sec_servers.table_contains_server`, *TESTDATA[section][parameter]*
        """
        self.cs_sec_servers.table_contains_server(TESTDATA[section][parameter])

    def verify_table_contains_subsystem(self, section=u'member_mgm_configuration'):
        """
        Verify table contains subsystem

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients.Ss_clients.verify_table_contains_subsystem`, *TESTDATA[section]*
        """
        self.ss_clients.verify_table_contains_subsystem(TESTDATA[section])
