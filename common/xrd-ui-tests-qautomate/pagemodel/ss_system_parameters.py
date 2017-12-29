# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_system_parameters(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160414093455
    # Pagemodel url: https://xroad-lxd-ss1.lxd:4000/sysparams
    # Pagemodel area: (271, 1, 1641, 669)
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
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 165 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    CONFIGURATION_ANCHOR = (By.XPATH, u'//div[1]/div[1]/span[1]') # x: 300 y: 80 width: 193 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: tsps, href: None
    ID_ANCHOR_DOWNLOAD = (By.ID, u'anchor_download') # x: 1680 y: 80 width: 109 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_ANCHOR_UPLOAD = (By.ID, u'anchor_upload') # x: 1799 y: 80 width: 81 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    HASH_SHA_224 = (By.XPATH, u'//div[1]/p[1]/label[1]') # x: 300 y: 123 width: 113 height: 21, tag: label, type: , name: None, form_id: , checkbox: , table_id: tsps, href:
    ANCHOR_HASH_07_AA_3E_F2_35_ED_E3_FA = (By.CSS_SELECTOR, u'.anchor-hash') # x: 413 y: 123 width: 593 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    GENERATED = (By.XPATH, u'//p[2]/label[1]') # x: 300 y: 154 width: 76 height: 21, tag: label, type: , name: None, form_id: , checkbox: , table_id: tsps, href:
    ANCHOR_GENERATED_AT_00_2016_03_01_12_14_20 = (By.CSS_SELECTOR, u'.anchor-generated_at') # x: 380 y: 154 width: 188 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    TIMESTAMPING_SERVICES = (By.XPATH, u'//div[2]/div[1]/span[1]') # x: 300 y: 225 width: 206 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: tsps, href: None
    ID_TSP_DELETE = (By.ID, u'tsp_delete') # x: 1743 y: 225 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_TSP_ADD = (By.ID, u'tsp_add') # x: 1827 y: 225 width: 53 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    TIMESTAMPING_SERVICE = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 301 y: 269 width: 789 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: tsps, href:
    SERVICE_URL = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 1090 y: 269 width: 789 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: tsps, href:
    SORTING_1_C_FI_O_PALVELUVAYLA_TEST_CN_TSA = (By.CSS_SELECTOR, u'.sorting_1') # x: 301 y: 307 width: 789 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: tsps, href:
    HTTP_DEV_IS_PALVELUVAYLA_COM_8899 = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[1]/td[2]') # x: 1090 y: 307 width: 789 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: tsps, href:
    INTERNAL_TLS_CERTIFICATE = (By.XPATH, u'//div[3]/div[1]/span[1]') # x: 300 y: 389 width: 207 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: tsps, href: None
    ID_GENERATE_INTERNAL_SSL = (By.ID, u'generate_internal_ssl') # x: 1072 y: 389 width: 191 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_GENERATE_SSL_CSR = (By.ID, u'generate_ssl_csr') # x: 1272 y: 389 width: 254 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_IMPORT_INTERNAL_SSL_CERT = (By.ID, u'import_internal_ssl_cert') # x: 1536 y: 389 width: 78 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_EXPORT_INTERNAL_SSL_CERT = (By.ID, u'export_internal_ssl_cert') # x: 1624 y: 389 width: 78 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_CERT_DETAILS = (By.ID, u'cert_details') # x: 1711 y: 389 width: 169 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    CERTIFICATE_HASH_SHA_1 = (By.XPATH, u'//div[3]/p[1]/label[1]') # x: 300 y: 432 width: 164 height: 21, tag: label, type: , name: None, form_id: , checkbox: , table_id: tsps, href:
    ID_INTERNAL_SSL_CERT_HASH = (By.ID, u'internal_ssl_cert_hash') # x: 468 y: 432 width: 419 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    # Dynamic objects:
    TSPS = (By.ID, u'tsps') # x: 301 y: 305 width: 1578 height: 30, tag: table, type: , name: None, form_id: , checkbox: , table_id: , href:

    def click_button_id_tsp_delete(self):
        """
        Click button to delete timestamping
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_TSP_DELETE*
        """
        # AutoGen method
        self.click_element(self.ID_TSP_DELETE)

    def click_button_id_tsp_add(self):
        """
        Click button to add timestamping
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_TSP_ADD*
        """
        # AutoGen method
        self.click_element(self.ID_TSP_ADD)

    def verify_time_stamping_url(self, parameters=None):
        """
        Veriyf timestamping url value
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.HTTP_DEV_IS_PALVELUVAYLA_COM_8899*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_text_should_be`, *self.HTTP_DEV_IS_PALVELUVAYLA_COM_8899*, *parameters[u'tsp_url']*
        """
        self.wait_until_element_is_visible(self.HTTP_DEV_IS_PALVELUVAYLA_COM_8899)
        self.element_text_should_be(self.HTTP_DEV_IS_PALVELUVAYLA_COM_8899, parameters[u'tsp_url'])

    def click_element_from_table_tsps_1(self, text=u'Palveluvayla Test TSA CN'):
        """
        Click timestamping from timestampings table with text

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element*
        """
        # Element search
        locator = self.TSPS
        value = text
        row = u'TBODY/TR'
        cell = u'TD'
        element_info = self.get_table_column_and_row_by_text(locator, value, row, cell)

        # Searched element info
        row_number = element_info[2]
        column_number = element_info[3]
        row_element = element_info[0]
        element = element_info[1]

        # Action for the element
        self.click_element(element)
