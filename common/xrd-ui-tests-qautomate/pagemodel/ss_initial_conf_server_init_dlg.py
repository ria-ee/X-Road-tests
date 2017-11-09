# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_initial_conf_server_init_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160330100459
    # Pagemodel url: https://test-rh1.i.palveluvayla.com:4000/init
    # Pagemodel area: (809, 410, 303, 152)
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
    # Use contains text in xpath: True
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]') # x: 1008 y: 410 width: 51 height: 49, tag: button, type: submit, name: None, form_id: serverconf_form, checkbox: , table_id: 4, href: 
    MENUBAR_CLOSE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[2]') # x: 1059 y: 410 width: 51 height: 49, tag: button, type: submit, name: None, form_id: serverconf_form, checkbox: , table_id: 4, href: 
    TITLE = (By.ID, u'ui-id-9') # x: 820 y: 424 width: 46 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_ALERT = (By.ID, u'alert') # x: 810 y: 461 width: 300 height: 52, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href: 
    BUTTON_OK = (By.XPATH, u'//div[8]/div[3]/div[1]/button[1]') # x: 1060 y: 518 width: 45 height: 37, tag: button, type: button, name: None, form_id: serverconf_form, checkbox: , table_id: 4, href: 

    def submit_serverconfform_noname3(self):
        """
        Click button to submit the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # AutoGen method submit form: serverconf_form
        self.click_element(self.BUTTON_OK)

    def wait_until_element_is_visible_id_alert(self):
        """
        Wait until alert is visible

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.ID_ALERT*
        """
        self.wait_until_element_is_visible(self.ID_ALERT)
