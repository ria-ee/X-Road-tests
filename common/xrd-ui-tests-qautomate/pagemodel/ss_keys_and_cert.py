# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from variables import strings
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep
from common_lib.common_lib import Common_lib

class Ss_keys_and_cert(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    common_lib = Common_lib()
    # Pagemodel timestamp: 20160928092450
    # Pagemodel url: https://xroad-lxd-ss1.lxd:4000/keys
    # Pagemodel area: (270, 2, 1640, 669)
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
    # Row count: 5
    # Element count: 20
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 184 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    KEYS_FILTER = (By.CSS_SELECTOR, u'#keys_filter>label>input') # x: 346 y: 76 width: 179 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:
    CERTIFICATE = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 291 y: 115 width: 613 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    MEMBER = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 904 y: 115 width: 613 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    OCSP_RESPONSE = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 1517 y: 115 width: 88 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    EXPIRES = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[4]') # x: 1605 y: 115 width: 94 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    STATUS = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[5]') # x: 1699 y: 115 width: 106 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    UNKNOWN = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[6]') # x: 1805 y: 115 width: 94 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    ID_DETAILS = (By.ID, u'details') # x: 290 y: 480 width: 78 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_GENERATE_KEY = (By.ID, u'generate_key') # x: 372 y: 480 width: 125 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_GENERATE_CSR = (By.ID, u'generate_csr') # x: 501 y: 480 width: 126 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_DISABLE = (By.ID, u'disable') # x: 631 y: 480 width: 81 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_REGISTER = (By.ID, u'register') # x: 715 y: 480 width: 89 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_DELETE = (By.ID, u'delete') # x: 808 y: 480 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_IMPORT_CERT = (By.ID, u'import_cert') # x: 1732 y: 480 width: 168 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    CLASS_TOKEN_NAME = (By.CLASS_NAME, u'token-name') # x: 296 y: 175 width: 1266 height: 21 # Dynamic object
    ID_KEYS = (By.ID, u'keys') # x: 291 y: 98 width: 1592 height: 472 # Dynamic object
    ID_ACTIVATE = (By.ID, u'activate') # x: 759 y: 365 width: 87 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def verify_keys_and_cert_title(self):
        """
        Verify view is visble

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.ID_HEADING*
        """
        self.wait_until_element_is_visible(self.ID_HEADING)

    def click_soft_token(self):
        """
        Click button to open soft token

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.CLASS_TOKEN_NAME*
        """
        self.click_element(self.CLASS_TOKEN_NAME)

    def click_generate_key(self):
        """
        Click button to generate key

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_GENERATE_KEY*
        """
        self.click_element(self.ID_GENERATE_KEY)

    def click_generated_key_request(self, text=u'ta_generated_key_sign'):
        """
        Click generate key in generated keys table with given text

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_jquery_ajax_loaded()
        print("finding key")
        element_rowtable = self.get_table_column_and_row_by_text(self.ID_KEYS, "Key: " + text + " (?)","TBODY/TR","TD")
        #Key: ta_generated_key_sign (?)
        print(element_rowtable[0])
        sleep(0.5)
        element_rowtable[0].click()
        #element_rowtable[0].find_element(By.XPATH, u'//span[contains(text(),"?")]').click()
        print("ELEMENT SELECTED")
        #element_rowtable[0].find_element(By.CSS_SELECTOR, '.fa-info').click_element()
        sleep(3)

    def click_delete_cert(self):
        """
        Click button to delete certification

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_DELETE*
        """
        self.click_element(self.ID_DELETE)

    def click_generate_certificate_request(self):
        """
        Click button to generate certificate request

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_GENERATE_CSR*
        """
        self.click_element(self.ID_GENERATE_CSR)

    def click_generated_key_request_to_signed_label(self, text=u'ta_generated_key_sign'):
        """
        Click generate key in generated keys table with given text

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_jquery_ajax_loaded()
        print("finding request key")
        sleep(2)
        search_key_string = "Key: " + text + " (sign)"
        element_rowtable = self.get_table_column_and_row_by_text(self.ID_KEYS, search_key_string,"TBODY/TR","TD")
        sleep(0.5)
        #element_rowtable[0].click_element()
        element_rowtable[0].click()
        print("ELEMENT SELECTED")
        #element_rowtable[0].find_element(By.CSS_SELECTOR, '.fa-info').click_element()
        sleep(4)

    def click_import_cert(self):
        """
        Click button to import certificate

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_IMPORT_CERT*
        """
        self.click_element(self.ID_IMPORT_CERT)

    def delete_imported_cert_key(self, parameters=None):
        """
        Click button to delete imported certificate key

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.ID_DELETE*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_DELETE*
        """
        # AutoGen method search_text_from_table_keys
        elem_table = self.get_table_column_and_row_by_text((By.ID, 'keys'), parameters, row='TBODY/TR', cell='TD')
        elem_table[1].click()
        self.wait_until_element_is_enabled(self.ID_DELETE)
        self.click_element(self.ID_DELETE)
        sleep(2)

    def find_texts_from_table_keys(self, cert_number=""):
        """
        Find key from keys table with text and return its content text

        :return cert_key: keys tables found row

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_jquery_ajax_loaded()
        find_word = strings.server_environment_approved_ca() +  " " + str(cert_number)
        elem_table = self.get_table_column_and_row_by_text((By.ID, 'keys'), find_word, row='TBODY/TR', cell='TD')
        row_cert_details = elem_table[2]
        cell_cert_details = elem_table[3]

        cell_cert_oscp = int(elem_table[3]) + 2
        cell_cert_register = int(elem_table[3]) + 4
        row_cert_key = int(elem_table[2]) - 2

        if self.get_table_cell_text_by_column_and_row(self.ID_KEYS, str(cell_cert_details), str(row_cert_details)) == find_word:
            print("Succesfully imported certificate")
        if self.get_table_cell_text_by_column_and_row(self.ID_KEYS, str(cell_cert_oscp), str(row_cert_details)) in  ["good", "revoked"]:
            print("OSCP response ok")
        if self.get_table_cell_text_by_column_and_row(self.ID_KEYS, str(cell_cert_register), str(row_cert_details)) in ["registered"]:
            print("Registered ok")

        cert_key = self.get_table_cell_text_by_column_and_row(self.ID_KEYS, str(cell_cert_details), str(row_cert_key))
        # Find key for registered cert
        print(cert_key)
        if "Key" in cert_key:
            print("Find cert key")
            return cert_key

    def wait_until_cert_req_active(self):
        """
        Wait until certificate reg is active

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.ID_GENERATE_CSR*
        """
        self.wait_until_element_is_enabled(self.ID_GENERATE_CSR)

    def register_auth_cert(self, text=None):
        """
        Click authentication in table and then click button to register it

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.ID_REGISTER*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_REGISTER*
        """
        # AutoGen method search_text_from_table_keys
        elem_table = self.get_table_column_and_row_by_text((By.ID, 'keys'), text, row='TBODY/TR', cell='TD')
        elem_table[1].click()
        self.wait_until_element_is_enabled(self.ID_REGISTER)
        self.click_element(self.ID_REGISTER)
        sleep(2)

    def find_texts_from_table_keys_auth(self, cert_number=""):
        """
        Find key from keys table with text and return its content text

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_jquery_ajax_loaded()
        # AutoGen method search_text_from_table_keys
        find_word = strings.server_environment_approved_ca() +  " " + str(cert_number)
        elem_table = self.get_table_column_and_row_by_text((By.ID, 'keys'), find_word, row='TBODY/TR', cell='TD')
        row_cert_details = elem_table[2]
        cell_cert_details = elem_table[3]

        cell_cert_oscp = int(elem_table[3]) + 2
        cell_cert_register = int(elem_table[3]) + 4
        row_cert_key = int(elem_table[2]) - 2

        if self.get_table_cell_text_by_column_and_row(self.ID_KEYS, str(cell_cert_details), str(row_cert_details)) == find_word:
            print("Succesfully imported certificate")
        if self.get_table_cell_text_by_column_and_row(self.ID_KEYS, str(cell_cert_oscp), str(row_cert_details)) in  ["disabled"]:
            print("Disabled ok")
        if self.get_table_cell_text_by_column_and_row(self.ID_KEYS, str(cell_cert_register), str(row_cert_details)) in ["saved"]:
            print("Saved ok")

        cert_key = self.get_table_cell_text_by_column_and_row(self.ID_KEYS, str(cell_cert_details), str(row_cert_key))

        # Find key for registered cert
        print(cert_key)
        if "Key" in cert_key:
            print("Find cert key")
            return cert_key

    def click_cert_activate(self):
        """
        Click button to activate certificate

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_ACTIVATE*
        """
        self.click_element(self.ID_ACTIVATE)