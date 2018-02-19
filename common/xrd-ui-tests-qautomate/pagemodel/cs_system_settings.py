# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from variables import errors
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_system_settings(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161011132221
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/system_settings
    # Pagemodel area: (270, 0, 1647, 810)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Depth of css path: 3
    # Minimize css selector: True
    # Create automated methods: True
    # Use css pattern: False
    # Allow non unique css pattern: False
    # Pagemodel template: False
    # Use testability: True
    # testability attribute: data-name
    # Use contains text in xpath: True
    # Exclude dynamic table filter: True
    # Row count: 7
    # Element count: 30
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 138 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SYSTEM_PARAMETERS = (By.XPATH, u'//div[1]/div[1]/span[1]') # x: 300 y: 80 width: 175 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: member_classes, href: None
    INSTANCE_IDENTIFIER = (By.XPATH, u'//div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 300 y: 116 width: 274 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    TEST = (By.XPATH, u'//div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]') # x: 574 y: 116 width: 1242 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    CENTRAL_SERVER = (By.XPATH, u'//div[1]/div[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 300 y: 147 width: 274 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    ID_CENTRAL_SERVER_ADDRESS = (By.ID, u'central_server_address') # x: 579 y: 152 width: 1234 height: 33, tag: input, type: text, name: central_server_address, form_id: , checkbox: , table_id: 1, href:
    ID_CENTRAL_SERVER_ADDRESS_EDIT = (By.ID, u'central_server_address_edit') # x: 1821 y: 152 width: 54 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 1, href:
    MANAGEMENT_SERVICES = (By.XPATH, u'//div[2]/div[1]/span[1]') # x: 300 y: 230 width: 197 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: member_classes, href: None
    BODY_SERVICE_PROVIDER_IDENTIFIER = (By.XPATH, u'//body[1]/div[3]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]') # x: 300 y: 266 width: 274 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    ID_SERVICE_PROVIDER_ID = (By.ID, u'service_provider_id') # x: 579 y: 271 width: 1234 height: 33, tag: input, type: text, name: service_provider_id, form_id: , checkbox: , table_id: 2, href:
    ID_SERVICE_PROVIDER_EDIT = (By.ID, u'service_provider_edit') # x: 1821 y: 271 width: 54 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 2, href:
    SERVICE_PROVIDER_NAME = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[2]/td[1]') # x: 300 y: 309 width: 274 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    ID_SERVICE_PROVIDER_NAME = (By.ID, u'service_provider_name') # x: 574 y: 309 width: 1242 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: 2, href:
    MANAGEMENT_SERVICES_SECURITY_SERVER = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[3]/td[1]') # x: 300 y: 340 width: 274 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    ID_SERVICE_PROVIDER_SECURITY_SERVER_REGISTER = (By.ID, u'service_provider_security_server_register') # x: 579 y: 345 width: 89 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 2, href:
    ID_SERVICE_PROVIDER_SECURITY_SERVERS = (By.ID, u'service_provider_security_servers') # x: 579 y: 351 width: 0 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: 2, href: None
    WSDL = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[4]/td[1]') # x: 300 y: 383 width: 274 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    ID_WSDL_ADDRESS = (By.ID, u'wsdl_address') # x: 574 y: 383 width: 1242 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: 2, href:
    UNKNOWN_5 = (By.XPATH, u'//tr[4]/td[3]') # x: 1816 y: 383 width: 64 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    SERVICES = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[5]/td[1]') # x: 300 y: 414 width: 274 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    ID_SERVICES_ADDRESS = (By.ID, u'services_address') # x: 574 y: 414 width: 1242 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: 2, href:
    SECURITY_SERVER_OWNERS_GROUP = (By.XPATH, u'//tr[6]/td[1]') # x: 300 y: 445 width: 274 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    SECURITY_SERVER_OWNERS = (By.XPATH, u'//tr[6]/td[2]') # x: 574 y: 445 width: 1242 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:
    BOX_HEADING_CF_TITLE_MEMBER_CLASSES = (By.CSS_SELECTOR, u'div.box-heading.cf>.box-title') # x: 300 y: 516 width: 145 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ADD_ICON = (By.CSS_SELECTOR, u'.add-icon') # x: 1679 y: 516 width: 53 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    RIGHT_EDIT_ICON_UI_STATE_DISABLED = (By.CSS_SELECTOR, u'button.right.edit-icon.ui-state-disabled') # x: 1743 y: 516 width: 54 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    DELETE_ICON = (By.CSS_SELECTOR, u'.delete-icon') # x: 1806 y: 516 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    DESCRIPTION = (By.XPATH, u'//div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 491 y: 560 width: 1388 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: member_classes, href:

    def click_button_id_central_server_address_edit(self):
        """
        Click button to edit server address

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_CENTRAL_SERVER_ADDRESS_EDIT*
        """
        # AutoGen method
        self.click_element(self.ID_CENTRAL_SERVER_ADDRESS_EDIT)

    def click_button_id_service_provider_edit(self):
        """
        Click button to edit service provider

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SERVICE_PROVIDER_EDIT*
        """
        # AutoGen method
        self.click_element(self.ID_SERVICE_PROVIDER_EDIT)

    def click_button_add_icon(self):
        """
        Click button to add icon

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ADD_ICON*
        """
        # AutoGen method
        self.click_element(self.ADD_ICON)

    def get_wsdl_and_services_address(self, parameters=None):
        """
        Add wsdl and services address to parameters. Parameters saved to 'wsdl_add_url' and 'service_mgm_address'

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.add_dynamic_content_to_parameters`, *parameters*, *u'wsdl_add_url'*, *address*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.add_dynamic_content_to_parameters`, *parameters*, *u'service_mgm_address'*, *service_address*
        """
        address = self.get_text(self.ID_WSDL_ADDRESS)
        self.add_dynamic_content_to_parameters(parameters, u'wsdl_add_url', address)
        service_address = self.get_text(self.ID_SERVICES_ADDRESS)
        self.add_dynamic_content_to_parameters(parameters, u'service_mgm_address', service_address)

    def click_element_id_service_provider_security_server_register(self):
        """
        Click button to register security server provider

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SERVICE_PROVIDER_SECURITY_SERVER_REGISTER*
        """
        self.click_element(self.ID_SERVICE_PROVIDER_SECURITY_SERVER_REGISTER)

    def verify_central_address_does_not_contain_whitespace(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.value_starts_with_whitespace*
        """
        if self.get_value(self.ID_CENTRAL_SERVER_ADDRESS).startswith(" ") or self.get_value(self.ID_CENTRAL_SERVER_ADDRESS).endswith(" "):
            self.fail(errors.value_starts_with_whitespace)
