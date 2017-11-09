# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_mgm_requests_dlg_reg_details(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20170217123450
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/requests
    # Pagemodel area: (660, 85, 601, 813)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Create automated methods: True
    # Depth of css path: 3
    # Minimize css selector: True
    # Use css pattern: False
    # Allow non unique css pattern: False
    # Pagemodel template: False
    # Use testability: True
    # testability attribute: data-name
    # Use contains text in xpath: False
    # Exclude dynamic table filter: True
    # Row count: 5
    # Element count: 20
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[1]') # x: 1158 y: 84 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 5, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[2]') # x: 1209 y: 84 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 5, href:
    TITLE = (By.ID, u'ui-id-5') # x: 670 y: 98 width: 374 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    REQUEST_INFORMATION = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[1]/h2[1]/span[1]') # x: 685 y: 156 width: 180 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: 5, href: None
    REQUEST_ID_11_RECEIVED_2017_02_17_10_32_18 = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[1]/table[1]') # x: 685 y: 185 width: 551 height: 168, tag: table, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    AFFECTED_SECURITY_SERVER_INFORMATION = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/h2[1]/span[1]') # x: 685 y: 370 width: 322 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: 5, href: None
    OWNER_NAME = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[1]/td[1]') # x: 685 y: 399 width: 102 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    FIRMA_OY = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[1]/td[2]/p[1]') # x: 792 y: 404 width: 441 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    OWNER_CLASS = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[2]/td[1]') # x: 685 y: 441 width: 102 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    GOV = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[2]/td[2]/p[1]') # x: 792 y: 446 width: 441 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    OWNER = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[3]/td[1]') # x: 685 y: 483 width: 102 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    CONST_1234510_9 = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[3]/td[2]/p[1]') # x: 792 y: 488 width: 441 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    SERVER = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[4]/td[1]') # x: 685 y: 525 width: 102 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    XROAD_LXD_SS0 = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[4]/td[2]/p[1]') # x: 792 y: 530 width: 441 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    UNKNOWN_1 = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[5]/td[1]') # x: 685 y: 567 width: 102 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    UNKNOWN_3 = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[2]/table[1]/tbody[1]/tr[5]/td[2]/p[1]') # x: 792 y: 572 width: 441 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    AUTHENTICATION_CERTIFICATE_SUBMITTED_FOR_DELETION = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/h2[1]/span[1]') # x: 685 y: 616 width: 433 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: 5, href: None
    CA = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 685 y: 645 width: 109 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    PALVELUVAYLA_TEST_CA_CN = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[1]/td[2]/p[1]') # x: 799 y: 650 width: 434 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    SERIAL_NUMBER = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 685 y: 687 width: 109 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    CONST_4 = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[2]/td[2]/p[1]') # x: 799 y: 692 width: 434 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    SUBJECT = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[3]/td[1]') # x: 685 y: 729 width: 109 height: 62, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    C_FI_O_FIRMA_OYPZHR_CN_TEST_SS1_PALVELUVAYLA_COM = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[3]/td[2]/p[1]') # x: 799 y: 734 width: 434 height: 52, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    EXPIRES = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[4]/td[1]') # x: 685 y: 791 width: 109 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    CONST_2037_01_31_09_07_26 = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[4]/td[2]/p[1]') # x: 799 y: 796 width: 434 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    BUTTON_CLOSE = (By.CLASS_NAME, u'ui-state-focus') # x: 1190 y: 856 width: 65 height: 36, tag: button, type: button, name: close, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    COMMENT = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/section[1]/table[1]/tbody[1]/tr[7]/td[2]/p[1]') # x: 775 y: 316 width: 458 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: , href:

    def click_button_close(self):
        """
        Click button to close the dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CLOSE*
        """
        # AutoGen method click_link: None
        self.click_element(self.BUTTON_CLOSE)

    def verify_comment_text(self, text=None):
        """
        Verify comment with given text

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_text_should_be`, *self.COMMENT*, *text*
        """
        self.element_text_should_be(self.COMMENT, text)
