# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.ss_clients_dlg_services_add_wsdl import Ss_clients_dlg_services_add_wsdl
from pagemodel.ss_clients_dlg_services import Ss_clients_dlg_services
from pagemodel.ss_clients_dlg_services_edit_wsdl import Ss_clients_dlg_services_edit_wsdl
from pagemodel.ss_clients import Ss_clients
from pagemodel.ss_clients_dlg_services_acl_for_service import Ss_clients_dlg_services_acl_for_service
from pagemodel.ss_clients_services_dlg_add_subjects import Ss_clients_services_dlg_add_subjects
from pagemodel.ss_clients_services_dlg_acl_confirm import Ss_clients_services_dlg_acl_confirm

class Component_ss_services(CommonUtils):
    """
    Components common to security server services view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    ss_clients_dlg_services_add_wsdl = Ss_clients_dlg_services_add_wsdl()
    ss_clients_dlg_services = Ss_clients_dlg_services()
    ss_clients_dlg_services_edit_wsdl = Ss_clients_dlg_services_edit_wsdl()
    ss_clients = Ss_clients()
    ss_clients_dlg_services_acl_for_service = Ss_clients_dlg_services_acl_for_service()
    ss_clients_services_dlg_add_subjects = Ss_clients_services_dlg_add_subjects()
    ss_clients_services_dlg_acl_confirm = Ss_clients_services_dlg_acl_confirm()

    def add_new_wsdl(self, section=u'add_wsdl'):
        """
        Add new wsdl

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_wsdl_add`
                * **Step 2:** :func:`~pagemodel.ss_clients_dlg_services_add_wsdl.Ss_clients_dlg_services_add_wsdl.verify_add_wsdl_dlg_open`
                * **Step 3:** :func:`~pagemodel.ss_clients_dlg_services_add_wsdl.Ss_clients_dlg_services_add_wsdl.add_wsdl`, *TESTDATA[section]*
        """
        self.ss_clients_dlg_services.click_wsdl_add()
        self.ss_clients_dlg_services_add_wsdl.verify_add_wsdl_dlg_open()
        self.ss_clients_dlg_services_add_wsdl.add_wsdl(TESTDATA[section])

    def edit_wsdl_service_parameters_in_ss(self, section1=u'wsdl_service_auth_cert_deletion', section2=u'service_wsdl_auth_cert_deletion', section3=u'cs_url', parameter=u'service_mgm_address'):
        """
        Edit wsdl service service parameters in security server

        *Updated: 11.07.2017*

        :param section1:  Test data section name
        :param section2:  Test data section name
        :param section3:  Test data section name
        :param parameter:  Test data parameter name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_and_open_wsdl_service`, *TESTDATA[section1]*
                * **Step 2:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_edit_service_params`
                * **Step 3:** :func:`~pagemodel.ss_clients_dlg_services_edit_wsdl.Ss_clients_dlg_services_edit_wsdl.verify_edit_serv_param_dlg_open`
                * **Step 5:** :func:`~pagemodel.ss_clients_dlg_services_edit_wsdl.Ss_clients_dlg_services_edit_wsdl.fill_service_parameters`, *TESTDATA[section2]*
                * **Step 6:** :func:`~pagemodel.ss_clients_dlg_services_edit_wsdl.Ss_clients_dlg_services_edit_wsdl.click_ok_service_parameters`
        """
        sleep(2)
        self.ss_clients_dlg_services.click_and_open_wsdl_service(TESTDATA[section1])
        self.ss_clients_dlg_services.click_edit_service_params()
        self.ss_clients_dlg_services_edit_wsdl.verify_edit_serv_param_dlg_open()
        new_wsdl_value = TESTDATA[section3][parameter]
        self.add_dynamic_content_to_parameters(TESTDATA, u'params_url', new_wsdl_value, section2)
        self.ss_clients_dlg_services_edit_wsdl.fill_service_parameters(TESTDATA[section2])
        self.ss_clients_dlg_services_edit_wsdl.click_ok_service_parameters()

    def edit_wsdl_default_service_parameters_in_ss(self, section1=u'wsdl_service', section2=u'service_wsdl'):
        """
        Edit wsdl default service parameters in security server

        *Updated: 11.07.2017*

        :param section1:  Test data section name
        :param section2:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_and_open_wsdl_service`, *TESTDATA[section1]*
                * **Step 2:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_edit_service_params`
                * **Step 3:** :func:`~pagemodel.ss_clients_dlg_services_edit_wsdl.Ss_clients_dlg_services_edit_wsdl.verify_edit_serv_param_dlg_open`
                * **Step 4:** :func:`~pagemodel.ss_clients_dlg_services_edit_wsdl.Ss_clients_dlg_services_edit_wsdl.fill_service_parameters`, *TESTDATA[section2]*
                * **Step 5:** :func:`~pagemodel.ss_clients_dlg_services_edit_wsdl.Ss_clients_dlg_services_edit_wsdl.click_ok_service_parameters`
        """
        sleep(2)
        self.ss_clients_dlg_services.click_and_open_wsdl_service(TESTDATA[section1])
        self.ss_clients_dlg_services.click_edit_service_params()
        self.ss_clients_dlg_services_edit_wsdl.verify_edit_serv_param_dlg_open()
        self.ss_clients_dlg_services_edit_wsdl.fill_service_parameters(TESTDATA[section2])
        self.ss_clients_dlg_services_edit_wsdl.click_ok_service_parameters()

    def add_service_access_rights_to_add_to_subjects_in_ss(self):
        """
        Add service access rights to subjects in security server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_services_access_rights`
                * **Step 2:** :func:`~pagemodel.ss_clients_dlg_services_acl_for_service.Ss_clients_dlg_services_acl_for_service.verify_acl_dlg_open`
                * **Step 3:** :func:`~pagemodel.ss_clients_dlg_services_acl_for_service.Ss_clients_dlg_services_acl_for_service.click_acl_subjects_add`
                * **Step 4:** :func:`~pagemodel.ss_clients_services_dlg_add_subjects.Ss_clients_services_dlg_add_subjects.verify_add_subjects_dlg_open`
                * **Step 5:** :func:`~pagemodel.ss_clients_services_dlg_add_subjects.Ss_clients_services_dlg_add_subjects.click_search`
                * **Step 6:** :func:`~pagemodel.ss_clients_services_dlg_add_subjects.Ss_clients_services_dlg_add_subjects.click_and_open_subject`
                * **Step 7:** :func:`~pagemodel.ss_clients_services_dlg_add_subjects.Ss_clients_services_dlg_add_subjects.click_element_id_acl_subjects_search_add_selected`
                * **Step 8:** :func:`~pagemodel.ss_clients_dlg_services_acl_for_service.Ss_clients_dlg_services_acl_for_service.click_close_dlg_acl`
        """
        self.ss_clients_dlg_services.click_services_access_rights()
        self.ss_clients_dlg_services_acl_for_service.verify_acl_dlg_open()
        self.ss_clients_dlg_services_acl_for_service.click_acl_subjects_add()
        self.ss_clients_services_dlg_add_subjects.verify_add_subjects_dlg_open()
        self.ss_clients_services_dlg_add_subjects.click_search()
        self.ss_clients_services_dlg_add_subjects.click_and_open_subject()
        sleep(1)
        self.ss_clients_services_dlg_add_subjects.click_element_id_acl_subjects_search_add_selected()
        self.ss_clients_dlg_services_acl_for_service.click_close_dlg_acl()

    def add_service_access_rights_to_all_in_ss(self):
        """
        Add service access rights to all in security server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_clients_dlg_services.Ss_clients_dlg_services.click_services_access_rights`
                * **Step 2:** :func:`~pagemodel.ss_clients_dlg_services_acl_for_service.Ss_clients_dlg_services_acl_for_service.verify_acl_dlg_open`
                * **Step 3:** :func:`~pagemodel.ss_clients_dlg_services_acl_for_service.Ss_clients_dlg_services_acl_for_service.click_acl_subjects_add`
                * **Step 4:** :func:`~pagemodel.ss_clients_services_dlg_add_subjects.Ss_clients_services_dlg_add_subjects.verify_add_subjects_dlg_open`
                * **Step 5:** :func:`~pagemodel.ss_clients_services_dlg_add_subjects.Ss_clients_services_dlg_add_subjects.click_search`
                * **Step 6:** :func:`~pagemodel.ss_clients_services_dlg_add_subjects.Ss_clients_services_dlg_add_subjects.click_acl_subjects_add_to_acl`
                * **Step 7:** :func:`~pagemodel.ss_clients_services_dlg_acl_confirm.Ss_clients_services_dlg_acl_confirm.click_confirm_acl_subject_add`
                * **Step 8:** :func:`~pagemodel.ss_clients_dlg_services_acl_for_service.Ss_clients_dlg_services_acl_for_service.click_close_dlg_acl`
        """
        self.ss_clients_dlg_services.click_services_access_rights()
        self.ss_clients_dlg_services_acl_for_service.verify_acl_dlg_open()
        self.ss_clients_dlg_services_acl_for_service.click_acl_subjects_add()
        self.ss_clients_services_dlg_add_subjects.verify_add_subjects_dlg_open()
        self.ss_clients_services_dlg_add_subjects.click_search()
        self.ss_clients_services_dlg_add_subjects.click_acl_subjects_add_to_acl()
        sleep(1)
        self.ss_clients_services_dlg_acl_confirm.click_confirm_acl_subject_add()
        self.ss_clients_dlg_services_acl_for_service.click_close_dlg_acl()
