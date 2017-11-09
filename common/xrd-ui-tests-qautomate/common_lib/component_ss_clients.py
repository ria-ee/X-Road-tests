# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.ss_clients import Ss_clients
from pagemodel.ss_clients_add_client import Ss_clients_add_client
from pagemodel.ss_clients_add_client_conf import Ss_clients_add_client_conf
from pagemodel.ss_clients_add_search_client_dlg import Ss_clients_add_search_client_dlg
from pagemodel.ss_clients_dlg_services import Ss_clients_dlg_services
from pagemodel.ss_client_dlg_details import Ss_client_dlg_details
from pagemodel.ss_client_dlg_unregister import Ss_client_dlg_unregister
from pagemodel.ss_client_dlg_delete_unregister import Ss_client_dlg_delete_unregister

class Component_ss_clients(CommonUtils):
    """
    Components common to security server backup view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    ss_clients = Ss_clients()
    ss_clients_add_client = Ss_clients_add_client()
    ss_clients_add_client_conf = Ss_clients_add_client_conf()
    ss_clients_add_search_client_dlg = Ss_clients_add_search_client_dlg()
    ss_clients_dlg_services = Ss_clients_dlg_services()
    ss_client_dlg_details = Ss_client_dlg_details()
    ss_client_dlg_unregister = Ss_client_dlg_unregister()
    ss_client_dlg_delete_unregister = Ss_client_dlg_delete_unregister()

    def add_new_subsystem_to_ss(self, section=u'member_mgm_configuration'):
        """
        Add new subsystem to security server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients.Ss_clients.click_client_add_subsystem_server`
                * **Step 2:** :func:`~pagemodel.ss_clients_add_client.Ss_clients_add_client.fill_and_submit_client_details`, *TESTDATA[section]*
                * **Step 3:** :func:`~pagemodel.ss_clients_add_client_conf.Ss_clients_add_client_conf.click_confirm_client_registration_request`
        """
        self.ss_clients.click_client_add_subsystem_server()
        self.ss_clients_add_client.fill_and_submit_client_details(TESTDATA[section])
        # self.ss_clients_add_warning.click_element_continue()
        self.ss_clients_add_client_conf.click_confirm_client_registration_request()
        # Sync registration request before jquery
        sleep(15)
        # Sometimes it does not recognize jquery
        try:
            self.wait_until_jquery_ajax_loaded()
        except:
            sleep(5)
            self.reload_page()
            print("jquery is not regocnized")
            sleep(15)

    def add_from_search_existing_client_in_ss(self, section=u'member_mgm_configuration'):
        """
        Add from search existing client in secuiryt server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients.Ss_clients.click_client_add_subsystem_server`
                * **Step 2:** :func:`~pagemodel.ss_clients_add_client.Ss_clients_add_client.click_element_id_client_select`
                * **Step 3:** :func:`~pagemodel.ss_clients_add_search_client_dlg.Ss_clients_add_search_client_dlg.click_element_id_search_filter`
                * **Step 4:** :func:`~pagemodel.ss_clients_add_search_client_dlg.Ss_clients_add_search_client_dlg.click_client_from_table_clientsglobal`, *TESTDATA[section]*
                * **Step 5:** :func:`~pagemodel.ss_clients_add_search_client_dlg.Ss_clients_add_search_client_dlg.click_button_id_client_select_ok`
                * **Step 6:** :func:`~pagemodel.ss_clients_add_client.Ss_clients_add_client.click_element_ok`
        """
        self.ss_clients.click_client_add_subsystem_server()
        self.ss_clients_add_client.click_element_id_client_select()
        self.ss_clients_add_search_client_dlg.click_element_id_search_filter()
        self.ss_clients_add_search_client_dlg.click_client_from_table_clientsglobal(TESTDATA[section])
        self.ss_clients_add_search_client_dlg.click_button_id_client_select_ok()
        self.ss_clients_add_client.click_element_ok()

    def open_clients_details_dlg_with_subsystem_code(self, section=u'member_mgm_configuration'):
        """
        Open client services dialog with subsystem code

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients.Ss_clients.find_and_open_by_text_dlg_by_subsystem_code`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.verify_client_dlg_open`
        """
        #step Open services dialog from dynamic list
        self.ss_clients.find_and_open_by_text_dlg_by_subsystem_code(TESTDATA[section])
        self.ss_clients_dlg_services.verify_client_dlg_open()

    def open_client_services_dlg_with_full_member_id(self, section=u'member1_configuration'):
        """
        Open client services dialog with full member id

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients.Ss_clients.click_and_open_details_of_client_in_table`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.verify_client_dlg_open`
        """
        self.ss_clients.click_and_open_details_of_client_in_table(TESTDATA[section])
        self.ss_clients_dlg_services.verify_client_dlg_open()

    def unregister_and_delete_subsystem_in_subsystem_details_dlg(self):
        """
        Unregister and delete subsystem in subsystem details dialog

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_element_details_tab`
                * **Step 2:** :func:`~pagemodel.ss_client_dlg_details.Ss_client_dlg_details.click_unregister_client`
                * **Step 3:** :func:`~pagemodel.ss_client_dlg_unregister.Ss_client_dlg_unregister.click_confirm_unregister`
                * **Step 4:** :func:`~pagemodel.ss_client_dlg_delete_unregister.Ss_client_dlg_delete_unregister.click_client_delete`
        """
        self.ss_clients_dlg_services.click_element_details_tab()
        self.ss_client_dlg_details.click_unregister_client()
        self.ss_client_dlg_unregister.click_confirm_unregister()
        self.ss_client_dlg_delete_unregister.click_client_delete()
