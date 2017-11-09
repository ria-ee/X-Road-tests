# -*- coding: utf-8 -*-
from webframework import TESTDATA
import os
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.cs_cert_services import Cs_cert_services
from pagemodel.ca_cert_services_ca_details import Ca_cert_services_ca_details
from pagemodel.cs_cert_services_ocsp_responder_dlg import Cs_cert_services_ocsp_responder_dlg
from pagemodel.cs_cert_services_insert_service_ca_cert import Cs_cert_services_insert_service_ca_cert
from pagemodel.cs_cert_services_ocsp_add_new_dlg import Cs_cert_services_ocsp_add_new_dlg
from pagemodel.cs_cert_services_dlg_ca_settings import Cs_cert_services_dlg_ca_settings


class Component_cs_cert_services(CommonUtils):
    """
    Components common to central server certification services view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    cs_cert_services = Cs_cert_services()
    ca_cert_services_ca_details = Ca_cert_services_ca_details()
    cs_cert_services_ocsp_responder_dlg = Cs_cert_services_ocsp_responder_dlg()
    cs_cert_services_insert_service_ca_cert = Cs_cert_services_insert_service_ca_cert()
    cs_cert_services_ocsp_add_new_dlg = Cs_cert_services_ocsp_add_new_dlg()
    cs_cert_services_dlg_ca_settings = Cs_cert_services_dlg_ca_settings()

    def upload_ca_certificate(self, section1=u'paths', section2=u'cs_url'):
        """
        Uploda ca certificate

        *Updated: 11.07.2017*

        :param section1:  Test data section name
        :param section2:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *type_string*
        """
        sleep(2)
        type_string = os.path.join(os.getcwd(),
                                   TESTDATA[section1][u'data_folder'],
                                   TESTDATA[section2][u'ca_cert_file_name'])
        print(type_string)
        self.common_lib.type_file_name_pyautogui(type_string)
        print("done upload")
        sleep(2)

    def add_certification_service_and_upload_ca_root_to_cs(self, section1=u'paths', section2=u'cs_url', section3=u'server_environment'):
        """
        Add certification service and upload ca root to central server

        *Updated: 11.07.2017*

        :param section1:  Test data section name
        :param section2:  Test data section name
        :param section3:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_cert_services.Cs_cert_services.click_button_id_ca_add`
                * **Step 2:** :func:`~pagemodel.cs_cert_services_insert_service_ca_cert.Cs_cert_services_insert_service_ca_cert.click_button_browse`
                * **Step 4:** :func:`~pagemodel.cs_cert_services_insert_service_ca_cert.Cs_cert_services_insert_service_ca_cert.click_button_next`
                * **Step 5:** :func:`~pagemodel.cs_cert_services_dlg_ca_settings.Cs_cert_services_dlg_ca_settings.input_text_to_cert_profile_info_text`, *TESTDATA[section3]*
                * **Step 6:** :func:`~pagemodel.cs_cert_services_dlg_ca_settings.Cs_cert_services_dlg_ca_settings.click_button_id_ca_settings_submit`
                * **Step 7:** :func:`~pagemodel.ca_cert_services_ca_details.Ca_cert_services_ca_details.click_button_close`
        """
        self.cs_cert_services.click_button_id_ca_add()
        self.cs_cert_services_insert_service_ca_cert.click_button_browse()
        self.upload_ca_certificate(section1, section2)
        self.cs_cert_services_insert_service_ca_cert.click_button_next()
        self.cs_cert_services_dlg_ca_settings.input_text_to_cert_profile_info_text(TESTDATA[section3])
        self.cs_cert_services_dlg_ca_settings.click_button_id_ca_settings_submit()
        self.ca_cert_services_ca_details.click_button_close()

    def add_new_ocsp_responder(self, section=u'cs_url'):
        """
        Add new oscp responder

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_cert_services.Cs_cert_services.click_trusted_cert_table_first_row`
                * **Step 2:** :func:`~pagemodel.cs_cert_services.Cs_cert_services.click_button_id_ca_details`
                * **Step 3:** :func:`~pagemodel.ca_cert_services_ca_details.Ca_cert_services_ca_details.click_oscp_responders`
                * **Step 4:** :func:`~pagemodel.cs_cert_services_ocsp_responder_dlg.Cs_cert_services_ocsp_responder_dlg.click_button_id_ocsp_responder_add`
                * **Step 5:** :func:`~pagemodel.cs_cert_services_ocsp_add_new_dlg.Cs_cert_services_ocsp_add_new_dlg.input_text_to_id_ocsp_responder_url`, *TESTDATA[section]*
                * **Step 6:** :func:`~pagemodel.cs_cert_services_ocsp_add_new_dlg.Cs_cert_services_ocsp_add_new_dlg.click_button_ok`
                * **Step 7:** :func:`~pagemodel.cs_cert_services_ocsp_responder_dlg.Cs_cert_services_ocsp_responder_dlg.click_button_close`
        """
        self.cs_cert_services.click_trusted_cert_table_first_row()
        self.cs_cert_services.click_button_id_ca_details()
        self.ca_cert_services_ca_details.click_oscp_responders()
        self.cs_cert_services_ocsp_responder_dlg.click_button_id_ocsp_responder_add()
        self.cs_cert_services_ocsp_add_new_dlg.input_text_to_id_ocsp_responder_url(TESTDATA[section])
        self.cs_cert_services_ocsp_add_new_dlg.click_button_ok()
        self.cs_cert_services_ocsp_responder_dlg.click_button_close()