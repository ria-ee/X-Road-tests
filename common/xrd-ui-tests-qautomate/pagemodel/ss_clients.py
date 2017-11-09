# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from variables import errors
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151209105005
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/clients
    # Pagemodel area: (272, 1, 1640, 545)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: False
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Depth of css path: 8
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
    ID_CLIENT_ADD = (By.ID, u'client_add') # x: 1724 y: 8 width: 107 height: 33
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 202 height: 22
    CLIENTS_FILTER = (By.CSS_SELECTOR, u'#clients_filter>label>input') # x: 346 y: 76 width: 179 height: 33
    ID_CLIENTS = (By.ID, u'clients') # x: 291 y: 153 width: 1608 height: 255

    def click_client_add_subsystem_server(self):
        """
        Click button to add subsystem

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_CLIENT_ADD*
        """
        self.click_element(self.ID_CLIENT_ADD)

    def verify_service_registration_complete(self, parameters=None):
        """
        Verify service registeration is complete

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *parameters[u'subsystem_code']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_attribute_should_contains`, *element_circle*, *u'title'*, *u'registration in progress'*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.reload_page`
            * **Step 5:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_attribute_should_contains`, *element_circle*, *u'title'*, *u'registered'*
        """
        self.wait_until_jquery_ajax_loaded()
        self.wait_until_page_contains(parameters[u'subsystem_code'])
        element_rowtable = self.get_table_column_and_row_by_text_contains(self.ID_CLIENTS, parameters[u'subsystem_code'], "TBODY/TR","TD/SPAN")
        try:
            element_circle = element_rowtable[0].find_element(By.XPATH, "//*[contains(@class, \'status waiting\')]")
            self.element_attribute_should_contains(element_circle, u'title', u'registration in progress')
            sleep(22)
        except:
            sleep(22)
            pass
        self.reload_page()
        element_rowtable = self.get_table_column_and_row_by_text_contains(self.ID_CLIENTS, parameters[u'member_id'],"TBODY/TR","TD/SPAN")
        element_circle = element_rowtable[0].find_element(By.XPATH, "//*[contains(@class, \'status ok\')]")
        self.element_attribute_should_contains(element_circle, u'title', u'registered')

    def click_and_open_details_of_client_in_table(self, parameters=None):
        """
        Click client in clients table with parameter 'subsystem_code'

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *parameters[u'subsystem_code']*
        """
        self.wait_until_jquery_ajax_loaded()
        self.wait_until_page_contains(parameters[u'subsystem_code'])
        element_rowtable = self.get_table_column_and_row_by_text_contains(self.ID_CLIENTS,
                                                                          parameters[u'subsystem_code'], "TBODY/TR",
                                                                          "TD/SPAN")
        element_rowtable[0].find_element(By.CSS_SELECTOR, '.fa-wrench').click()

    def find_and_open_by_text_dlg_by_subsystem_code(self, parameters=None):
        """
        Click client in clients table. Parameters used 'instance_identifier', 'member_class', 'member_code' and 'subsystem_code'

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *parameters[u'subsystem_code']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.subsystem_status_error*
        """
        self.wait_until_jquery_ajax_loaded()
        self.wait_until_page_contains(parameters[u'subsystem_code'])
        subsystem_row = "SUBSYSTEM : " + parameters[u'instance_identifier'] + " : " + parameters['member_class'] + " : " + parameters['member_code'] + " : " + parameters[u'subsystem_code']

        # Should not be hard coded t
        for x in range(15):
            self.wait_until_jquery_ajax_loaded()
            element_rowtable = self.get_table_column_and_row_by_text(self.ID_CLIENTS, subsystem_row,"TBODY/TR","TD/SPAN")

            column_number = 1
            row_element = element_rowtable[0]

            element = row_element.find_elements(By.XPATH, "TD/SPAN")[int(column_number) - 1]
            if element.get_attribute("class") == "status ok":
                row_element.find_element(By.CSS_SELECTOR, '.fa-wrench').click()
                return
            sleep(2)
        self.fail(errors.subsystem_status_error)

    def verify_table_contains_subsystem(self, parameters=None):
        """
        Verify clients table contains subsystem. Parameters used 'instance_identifier', 'member_class', 'member_code' and 'subsystem_code'

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.subsystem_not_found*
        """
        self.wait_until_jquery_ajax_loaded()
        subsystem_row = "SUBSYSTEM : " + parameters[u'instance_identifier'] + " : " + parameters['member_class'] + " : " + parameters['member_code'] + " : " + parameters[u'subsystem_code']
        table_contains = self.table_contains_text(self.ID_CLIENTS, subsystem_row)
        if not table_contains:
            self.fail(errors.subsystem_not_found)
