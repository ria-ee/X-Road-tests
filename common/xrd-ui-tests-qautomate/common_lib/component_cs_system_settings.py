# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.cs_initial_configuration import Cs_initial_configuration
from pagemodel.cs_system_settings_mgm_sp_reg_req_dlg import Cs_system_settings_mgm_sp_reg_req_dlg
from pagemodel.cs_system_settings_mgm_req_servers_dlg import Cs_system_settings_mgm_req_servers_dlg
from pagemodel.cs_sidebar import Cs_sidebar
from pagemodel.cs_system_settings_search_member import Cs_system_settings_search_member
from pagemodel.cs_system_settings import Cs_system_settings
from pagemodel.cs_initial_conf_initilialized_dlg import Cs_initial_conf_initilialized_dlg
from pagemodel.cs_system_settings_change_cs_address_dlg import Cs_system_settings_change_cs_address_dlg
from pagemodel.cs_system_settings_add_member_class import Cs_system_settings_add_member_class

class Component_cs_system_settings(CommonUtils):
    """
    Components common to central server system settings view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    cs_initial_configuration = Cs_initial_configuration()
    cs_system_settings_mgm_sp_reg_req_dlg = Cs_system_settings_mgm_sp_reg_req_dlg()
    cs_system_settings_mgm_req_servers_dlg = Cs_system_settings_mgm_req_servers_dlg()
    cs_system_settings_add_member_class = Cs_system_settings_add_member_class()
    cs_sidebar = Cs_sidebar()
    cs_system_settings_search_member = Cs_system_settings_search_member()
    cs_system_settings = Cs_system_settings()
    cs_initial_conf_initilialized_dlg = Cs_initial_conf_initilialized_dlg()
    cs_system_settings_change_cs_address_dlg = Cs_system_settings_change_cs_address_dlg()

    def register_subsystem_system_settings_in_cs(self, section=u'member_mgm_configuration'):
        """
        Register subsystem settings in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_system_settings.Cs_system_settings.click_element_id_service_provider_security_server_register`
                * **Step 2:** :func:`~pagemodel.cs_system_settings_mgm_sp_reg_req_dlg.Cs_system_settings_mgm_sp_reg_req_dlg.click_button_id_used_server_server_search`
                * **Step 3:** :func:`~pagemodel.cs_system_settings_mgm_req_servers_dlg.Cs_system_settings_mgm_req_servers_dlg.click_server_from_table_usedserversearchall`, *TESTDATA[section]*
                * **Step 4:** :func:`~pagemodel.cs_system_settings_mgm_req_servers_dlg.Cs_system_settings_mgm_req_servers_dlg.click_button_select`
                * **Step 5:** :func:`~pagemodel.cs_system_settings_mgm_sp_reg_req_dlg.Cs_system_settings_mgm_sp_reg_req_dlg.click_button_submit`
        """
        self.cs_system_settings.click_element_id_service_provider_security_server_register()
        self.cs_system_settings_mgm_sp_reg_req_dlg.click_button_id_used_server_server_search()
        self.cs_system_settings_mgm_req_servers_dlg.click_server_from_table_usedserversearchall(TESTDATA[section])
        self.cs_system_settings_mgm_req_servers_dlg.click_button_select()
        self.cs_system_settings_mgm_sp_reg_req_dlg.click_button_submit()

    def copy_wsdl_addresses_in_cs(self, section=u'cs_url'):
        """
        Copy wsdl address in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_system_settings.Cs_system_settings.get_wsdl_and_services_address`, *TESTDATA[section]*
        """
        self.cs_system_settings.get_wsdl_and_services_address(TESTDATA[section])

    def edit_mgm_service_provider_in_cs(self, section=u'member_mgm_configuration'):
        """
        Edit management service provider in central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_system_settings.Cs_system_settings.click_button_id_service_provider_edit`
                * **Step 2:** :func:`~pagemodel.cs_system_settings_search_member.Cs_system_settings_search_member.wait_until_element_is_visible_type`
                * **Step 3:** :func:`~pagemodel.cs_system_settings_search_member.Cs_system_settings_search_member.click_member_from_table_membersearch`, *TESTDATA[section]*
                * **Step 4:** :func:`~pagemodel.cs_system_settings_search_member.Cs_system_settings_search_member.click_element_dlg_select`
        """
        self.cs_system_settings.click_button_id_service_provider_edit()
        self.cs_system_settings_search_member.wait_until_element_is_visible_type()
        self.cs_system_settings_search_member.click_member_from_table_membersearch(TESTDATA[section])
        self.cs_system_settings_search_member.click_element_dlg_select()

    # TODO FIX

    def initialize_cs_server_config(self, section=u'cs_url'):
        """
        Initialize central servers server config

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_initial_configuration.Cs_initial_configuration.fill_input_values_init`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.cs_initial_configuration.Cs_initial_configuration.submit_init_noname1`
                * **Step 3:** :func:`~pagemodel.cs_initial_conf_initilialized_dlg.Cs_initial_conf_initilialized_dlg.click_button_ok`
                * **Step 4:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.verify_central_server_title`
        """
        self.cs_initial_configuration.fill_input_values_init(TESTDATA[section])
        self.cs_initial_configuration.submit_init_noname1()
        self.cs_initial_conf_initilialized_dlg.click_button_ok()
        self.cs_sidebar.verify_central_server_title()

    def add_init_member_class(self, section=u'member_mgm_configuration'):
        """
        Add init member class

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_system_settings`
                * **Step 2:** :func:`~pagemodel.cs_system_settings.Cs_system_settings.click_button_add_icon`
                * **Step 3:** :func:`~pagemodel.cs_system_settings_add_member_class.Cs_system_settings_add_member_class.input_text_to_name_member_class_fill_text`, *TESTDATA[section]*
                * **Step 4:** :func:`~pagemodel.cs_system_settings_add_member_class.Cs_system_settings_add_member_class.input_text_name_member_class_description`, *TESTDATA[section]*
                * **Step 5:** :func:`~pagemodel.cs_system_settings_add_member_class.Cs_system_settings_add_member_class.click_button_ok`
        """
        self.cs_sidebar.click_link_data_name_system_settings()
        self.cs_system_settings.click_button_add_icon()
        self.cs_system_settings_add_member_class.input_text_to_name_member_class_fill_text(TESTDATA[section])
        self.cs_system_settings_add_member_class.input_text_name_member_class_description(TESTDATA[section])
        self.cs_system_settings_add_member_class.click_button_ok()
        self.wait_until_jquery_ajax_loaded()

    def change_server_address(self, section=u'cs_url'):
        """
        Change server address

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_system_settings.Cs_system_settings.click_button_id_central_server_address_edit`
        """
        self.cs_system_settings.click_button_id_central_server_address_edit()
        self.input_server_address_in_dlg(section)
        self.confirm_server_address_dlg()

    def cancel_server_address_dlg(self):
        """
        Cancel server address dialog

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_system_settings_change_cs_address_dlg.Cs_system_settings_change_cs_address_dlg.click_cancel`
        """
        self.cs_system_settings_change_cs_address_dlg.click_cancel()

    def confirm_server_address_dlg(self):
        """
        Confirm server address dialog

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_system_settings_change_cs_address_dlg.Cs_system_settings_change_cs_address_dlg.click_confim`
        """
        self.cs_system_settings_change_cs_address_dlg.click_confim()

    def input_server_address_in_dlg(self, section):
        """
        Input server address in dlg

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_system_settings_change_cs_address_dlg.Cs_system_settings_change_cs_address_dlg.input_server_address`, *TESTDATA[section]*
        """
        self.cs_system_settings_change_cs_address_dlg.input_server_address(TESTDATA[section])