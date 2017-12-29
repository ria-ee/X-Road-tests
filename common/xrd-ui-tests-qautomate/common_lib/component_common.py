# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.ss_sidebar import Ss_sidebar
from pagemodel.dlg_change_language import Dlg_change_language
from pagemodel.common_elements import Common_elements

class Component_common(CommonUtils):
    """
    Common library for common components

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    ss_sidebar = Ss_sidebar()
    dlg_change_language = Dlg_change_language()
    common_elements = Common_elements()

    def open_select_language_dlg(self):
        """
        Open select language dialog

        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_elements.Common_elements.click_user_info`
                * **Step 2:** :func:`~common_lib.common_elements.Common_elements.click_change_language`
        """
        self.common_elements.click_user_info()
        self.common_elements.click_change_language()

    def accept_select_language_dlg(self):
        """
        Accept select languege dialog

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.dlg_change_language.Dlg_change_language.click_button_ok`
        """
        self.dlg_change_language.click_button_ok()

    def change_language_in_dlg(self, text=None):
        """
        Input text to change langueage dialog

        :param text:  String value for text
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.dlg_change_language.Dlg_change_language.change_language`, *text*
        """
        self.dlg_change_language.change_language(text)

    def verify_notice_message(self, message=u'Internal configuration anchor generated successfully'):
        """
        Verify notice message

        :param message:  String value for message
        
        **Test steps:**
                * **Step 2:** :func:`~common_lib.common_elements.Common_elements.verify_message_contains`, *message*
        """
        self.wait_until_jquery_ajax_loaded()
        self.common_elements.verify_message_contains(message)

    def verify_error_message(self, message=u'Internal configuration anchor generation failed'):
        """
        Verify notice message

        :param message:  String value for message
        
        **Test steps:**
                * **Step 2:** :func:`~common_lib.common_elements.Common_elements.verify_error_contains`, *message*
        """
        self.wait_until_jquery_ajax_loaded()
        self.common_elements.verify_error_contains(message)
