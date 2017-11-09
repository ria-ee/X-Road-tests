# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.cs_mgm_requests_dlg_reg_details import Cs_mgm_requests_dlg_reg_details
from pagemodel.cs_mgm_requests import Cs_mgm_requests

class Component_cs_mgm_requests(CommonUtils):
    """
    Components common to central server management requests view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    cs_mgm_requests_dlg_reg_details = Cs_mgm_requests_dlg_reg_details()
    cs_mgm_requests = Cs_mgm_requests()

    def verify_comment_in_request_details_dlg(self, text=None):
        """
        Verify comment in request details dialog

        *Updated: 11.07.2017*

        :param text:  String value for text
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_mgm_requests_dlg_reg_details.Cs_mgm_requests_dlg_reg_details.verify_comment_text`, *text*
        """
        self.cs_mgm_requests_dlg_reg_details.verify_comment_text(text)

    def close_request_details_dlg(self):
        """
        Close request details dialog

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_mgm_requests_dlg_reg_details.Cs_mgm_requests_dlg_reg_details.click_button_close`
        """
        self.cs_mgm_requests_dlg_reg_details.click_button_close()

    def open_request_details_dlg(self, text=u'Certificate deletion'):
        """
        Open request details dialog

        *Updated: 11.07.2017*

        :param text:  String value for text
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_mgm_requests.Cs_mgm_requests.search_text_from_table_management_requests_all`, *text*
                * **Step 2:** :func:`~pagemodel.cs_mgm_requests.Cs_mgm_requests.click_button_id_request_details`
        """
        self.cs_mgm_requests.search_text_from_table_management_requests_all(text)
        self.cs_mgm_requests.click_button_id_request_details()
