# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_conf_mgm(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160330092643
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/configuration_management
    # Pagemodel area: (270, 0, 1647, 885)
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
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 249 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    INTERNAL_CONFIQURATION = (By.ID, u'ui-id-3') # x: 856 y: 71 width: 171 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    EXTERNAL_CONFIGURATION = (By.ID, u'ui-id-4') # x: 1028 y: 71 width: 173 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    TRUSTED_ANCHOR = (By.ID, u'ui-id-5') # x: 1202 y: 71 width: 132 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ANCHOR = (By.XPATH, u'//div[1]/div[1]/div[1]/span[1]') # x: 300 y: 126 width: 65 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href: None
    ID_GENERATE_SOURCE_ANCHOR = (By.ID, u'generate_source_anchor') # x: 1665 y: 126 width: 96 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_DOWNLOAD_SOURCE_ANCHOR = (By.ID, u'download_source_anchor') # x: 1771 y: 126 width: 109 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    HASH_SHA_224 = (By.XPATH, u'//div[1]/p[1]/label[1]') # x: 300 y: 169 width: 109 height: 21, tag: label, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    BOX_ANCHOR_HASH_07_AA_3E_F2_35_ED_E3 = (By.CSS_SELECTOR, u'div.box>p>.anchor-hash') # x: 413 y: 169 width: 593 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    GENERATED_0 = (By.XPATH, u'//div[1]/p[2]/label[1]') # x: 300 y: 200 width: 76 height: 21, tag: label, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    BOX_ANCHOR_GENERATED_AT_UTC_2016_03_01_12_14 = (By.CSS_SELECTOR, u'div.box>p>.anchor-generated_at') # x: 380 y: 200 width: 170 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    DOWNLOAD_URL = (By.XPATH, u'//div[2]/div[1]/span[1]') # x: 300 y: 271 width: 131 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href: None
    ID_CONF_URL = (By.ID, u'conf_url') # x: 300 y: 307 width: 314 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SIGNING_KEYS = (By.XPATH, u'//div[3]/div[1]/span[1]') # x: 300 y: 378 width: 111 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href: None
    ID_GENERATE_SIGNING_KEY = (By.ID, u'generate_signing_key') # x: 1614 y: 378 width: 86 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_ACTIVATE_SIGNING_KEY = (By.ID, u'activate_signing_key') # x: 1709 y: 378 width: 87 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_DELETE_SIGNING_KEY = (By.ID, u'delete_signing_key') # x: 1806 y: 378 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    DEVICE_ID_KEY = (By.XPATH, u'//div[3]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 301 y: 422 width: 1306 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    GENERATED = (By.XPATH, u'//div[3]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 1607 y: 422 width: 166 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    LOGOUT = (By.CSS_SELECTOR, u'.logout') # x: 1778 y: 465 width: 83 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: signing_keys, href:
    CONFIGURATION_PARTS = (By.XPATH, u'//div[1]/div[4]/div[1]/span[1]') # x: 300 y: 554 width: 176 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href: None
    ID_UPLOAD_CONF_PART = (By.ID, u'upload_conf_part') # x: 1680 y: 554 width: 81 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_DOWNLOAD_CONF_PART = (By.ID, u'download_conf_part') # x: 1771 y: 554 width: 109 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    FILE = (By.XPATH, u'//div[4]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 301 y: 598 width: 526 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    CONTENT_IDENTIFIER = (By.XPATH, u'//div[4]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 827 y: 598 width: 526 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    UPDATED = (By.XPATH, u'//div[4]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 1353 y: 598 width: 526 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    # Dynamic objects:
    SIGNINGKEYS = (By.ID, u'signing_keys') # x: 301 y: 531 width: 1578 height: 43, tag: table, type: , name: None, form_id: , checkbox: , table_id: , href:
    CONFPARTS = (By.ID, u'conf_parts') # x: 301 y: 707 width: 1578 height: 30, tag: table, type: , name: None, form_id: , checkbox: , table_id: , href:
    LOGIN = (By.CLASS_NAME, u'login') # x: 1778 y: 536 width: 70 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    CONFPARTS1 = (By.ID, u'conf_parts') # x: 301 y: 636 width: 1568 height: 185, tag: table, type: , name: None, form_id: , checkbox: , table_id: , href:

    def click_link_internal_configuration(self):
        """
        Click link to internal configurations view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.INTERNAL_CONFIQURATION*
        """
        self.click_element(self.INTERNAL_CONFIQURATION)

    def click_link_external_configuration(self):
        """
        Click link to external configurations view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.EXTERNAL_CONFIGURATION*
        """
        self.click_element(self.EXTERNAL_CONFIGURATION)

    def click_button_id_generate_source_anchor(self):
        """
        Click button to generate source anchor

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_GENERATE_SOURCE_ANCHOR*
        """
        # AutoGen method
        self.click_element(self.ID_GENERATE_SOURCE_ANCHOR)

    def click_button_id_download_source_anchor(self):
        """
        Click button to download source anchor

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_DOWNLOAD_SOURCE_ANCHOR*
        """
        # AutoGen method
        self.click_element(self.ID_DOWNLOAD_SOURCE_ANCHOR)

    def click_button_id_generate_signing_key(self):
        """
        Click button to generate signing key

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_GENERATE_SIGNING_KEY*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method
        self.click_element(self.ID_GENERATE_SIGNING_KEY)
        self.wait_until_jquery_ajax_loaded()

    def click_button_id_activate_signing_key(self):
        """
        Click button to activate signing key

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_ACTIVATE_SIGNING_KEY*
        """
        # AutoGen method
        self.click_element(self.ID_ACTIVATE_SIGNING_KEY)

    def click_button_id_delete_signing_key(self):
        """
        Click button to delete signing key

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_DELETE_SIGNING_KEY*
        """
        # AutoGen method
        self.click_element(self.ID_DELETE_SIGNING_KEY)

    def click_button_logout(self):
        """
        Click button to logout from token

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.LOGOUT*
        """
        # AutoGen method
        self.click_element(self.LOGOUT)

    def click_element_login(self):
        """
        Click button to login to token

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.LOGIN*
        """
        self.click_element(self.LOGIN)

    def verify_hash_value_is_visible(self):
        """
        Verify that hash value is visible on the page

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_be_visible`, *self.BOX_ANCHOR_HASH_07_AA_3E_F2_35_ED_E3*
        """
        self.element_should_be_visible(self.BOX_ANCHOR_HASH_07_AA_3E_F2_35_ED_E3)

    def verify_date_time_is_visible(self):
        """
        Verify that date time is visible on the page

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_be_visible`, *self.BOX_ANCHOR_GENERATED_AT_UTC_2016_03_01_12_14*
        """
        self.element_should_be_visible(self.BOX_ANCHOR_GENERATED_AT_UTC_2016_03_01_12_14)

    def verify_download_url_contains(self, text=u'/internalconf'):
        """
        Verify that download url contains given text

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_contain`, *self.ID_CONF_URL*, *text*
        """
        self.element_should_contain(self.ID_CONF_URL, text)

    def verify_conf_parts(self):
        """
        Verify that configuration parts does not contain 'conf part is empty'
        """
        locator = self.CONFPARTS
        table = self.find_element(locator)
        rows = table.find_elements_by_xpath(".//tr")

        for row in rows:
            if "unavailable" in row.get_attribute("class"):
                continue
            columns = row.find_elements_by_xpath(".//td")
            if len(columns):
                assert(all(column.text for column in columns)), "Conf part is empty"

    def verify_signing_keys(self):
        """
        Verify that signing keys does not contain 'Signing key'
        """
        locator = self.SIGNINGKEYS
        table = self.find_element(locator)
        rows = table.find_elements_by_xpath(".//tr")

        for row in rows:
            columns = row.find_elements_by_xpath(".//td")
            if len(columns):
                assert(all(column.text for column in columns)), "Signing key info is empty"

    def click_newest_signing_key(self):
        """
        Click newest signing key on the signing keys table

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_jquery_ajax_loaded()
        locator = self.SIGNINGKEYS
        table = self.find_element(locator)
        rows = table.find_elements_by_xpath(".//tr")
        rows = [row for row in rows if len(row.find_elements_by_xpath(".//td"))]
        newest = max(rows, key=lambda p: p.find_elements_by_xpath(".//td")[1].text)
        newest.click()

    def click_oldest_signing_key(self):
        """
        Click oldest signing key on the signing keys table

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_jquery_ajax_loaded()
        locator = self.SIGNINGKEYS
        table = self.find_element(locator)
        rows = table.find_elements_by_xpath(".//tr")
        rows = [row for row in rows if len(row.find_elements_by_xpath(".//td"))]
        oldest = min(rows, key=lambda p: p.find_elements_by_xpath(".//td")[1].text)
        oldest.click()

    def verify_signing_keys(self):
        """
        Verify that signing keys does not contain 'Signing key'
        """
        locator = self.SIGNINGKEYS
        table = self.find_element(locator)
        rows = table.find_elements_by_xpath(".//tr")

        for row in rows:
            columns = row.find_elements_by_xpath(".//td")
            if len(columns):
                assert(all(column.text for column in columns)), "Signing key info is empty"

    def click_element_from_table_conf_parts(self, text=u'foo.xml'):
        """

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element*
        """
        # Element search
        locator = self.CONFPARTS1
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

    def click_conf_upload(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_UPLOAD_CONF_PART*
        """
        self.click_element(self.ID_UPLOAD_CONF_PART)

    def click_download(self, parameters=None):
        """

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_DOWNLOAD_CONF_PART*
        """
        self.click_element(self.ID_DOWNLOAD_CONF_PART)

    def get_newest_key_id(self, parameters=None):
        """
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_jquery_ajax_loaded()
        locator = self.SIGNINGKEYS
        table = self.find_element(locator)
        rows = table.find_elements_by_xpath(".//tr")
        rows = [row for row in rows if len(row.find_elements_by_xpath(".//td"))]
        newest = max(rows, key=lambda p: p.find_elements_by_xpath(".//td")[1].text)
        return newest.text.split(" ")[1]
