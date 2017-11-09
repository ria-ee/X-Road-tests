# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.ss_sidebar import Ss_sidebar

class Component_ss_sidebar(CommonUtils):
    """
    Components common to security server sidebar

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    ss_sidebar = Ss_sidebar()

    def open_system_parameters_view(self):
        """
        Open security servers parameters view

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_sidebar.Ss_sidebar.click_element_data_name_sysparams_system_parameters`
        """
        self.ss_sidebar.click_element_data_name_sysparams_system_parameters()

    def open_keys_and_certs_view(self):
        """
        Open security servers keys and certifications view

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_sidebar.Ss_sidebar.click_keys_and_certificates`
        """
        self.ss_sidebar.click_keys_and_certificates()

    def open_backup_restore_view(self):
        """
        Open security servers restore backup view

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_sidebar.Ss_sidebar.click_element_backup_and_restore`
        """
        self.ss_sidebar.click_element_backup_and_restore()

    def open_diagnostics_view(self):
        """
        Open security servers diagnostics view

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_sidebar.Ss_sidebar.click_element_diagnostics`
        """
        self.ss_sidebar.click_element_diagnostics()

    def open_version_view(self):
        """
        Open security servers version view

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_sidebar.Ss_sidebar.click_element_version`
        """
        self.ss_sidebar.click_element_version()

    def open_security_servers_client_view(self):
        """
        Open security servers client view

        *Updated: 11.07.2017*
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_sidebar.Ss_sidebar.click_element_security_server_clients`
        """
        self.ss_sidebar.click_element_security_server_clients()
