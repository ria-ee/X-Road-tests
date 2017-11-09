# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.cs_sidebar import Cs_sidebar

class Component_cs_sidebar(CommonUtils):
    """
    Components common to central server sidebar

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    cs_sidebar = Cs_sidebar()

    def open_members_view(self):
        """
        Open members view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_element_members`
        """
        self.cs_sidebar.click_element_members()

    def open_security_servers_view(self):
        """
        Open security servers view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_securityservers_security_servers`
        """
        self.cs_sidebar.click_link_data_name_securityservers_security_servers()

    def open_global_groups_view(self):
        """
        Open global groups view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_groups`
        """
        self.cs_sidebar.click_link_data_name_groups()

    def open_central_services_view(self):
        """
        Open central services view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_central_services`
        """
        self.cs_sidebar.click_link_data_name_central_services()

    def open_certification_services_view(self):
        """
        Open certificate services view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_approved_cas_certification_services`
        """
        self.cs_sidebar.click_link_data_name_approved_cas_certification_services()

    def open_timestamping_services_view(self):
        """
        Open timestamping services view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_tsps_stamping_services`
        """
        self.cs_sidebar.click_link_data_name_tsps_stamping_services()

    def open_management_request_view(self):
        """
        Open management request view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_requests_management`
        """
        self.cs_sidebar.click_link_data_name_requests_management()

    def open_global_configuration_view(self):
        """
        Open global configuration view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_configuration_management`
        """
        self.cs_sidebar.click_link_data_name_configuration_management()

    def open_system_settings_view(self):
        """
        Open system settings view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_system_settings`
        """
        self.cs_sidebar.click_link_data_name_system_settings()

    def open_backup_restore_view(self):
        """
        Open backup restore view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_backup_back_up_and_restore`
        """
        self.cs_sidebar.click_link_data_name_backup_back_up_and_restore()

    def open_version_view(self):
        """
        Open version view in central server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.click_link_data_name_about_version`
        """
        self.cs_sidebar.click_link_data_name_about_version()
