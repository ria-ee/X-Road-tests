# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_members_mgm_requests_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160427104507
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/
    # Pagemodel area: (458, 234, 1003, 504)
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
    # Links found: 5
    # Page model constants:
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[21]/div[1]/div[1]/button[1]') # x: 1358 y: 235 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: DataTables_Table_4, href:
    TITLE = (By.ID, u'ui-id-26') # x: 470 y: 249 width: 113 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MEMBER_DETAILS = (By.ID, u'ui-id-27') # x: 536 y: 301 width: 129 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    OWNED_SERVERS = (By.ID, u'ui-id-28') # x: 666 y: 301 width: 124 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    GLOBAL_GROUP_MEMBERSHIP = (By.ID, u'ui-id-29') # x: 791 y: 301 width: 202 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SUBSYSTEMS = (By.ID, u'ui-id-30') # x: 994 y: 301 width: 101 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    USED_SERVERS = (By.ID, u'ui-id-31') # x: 1096 y: 301 width: 110 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MANAGEMENT_REQUESTS = (By.ID, u'ui-id-32') # x: 1207 y: 301 width: 177 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    REQUEST_ID = (By.XPATH, u'//div[6]/div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 476 y: 347 width: 242 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: DataTables_Table_4, href:
    REQUEST_TYPE = (By.XPATH, u'//div[6]/div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 718 y: 347 width: 242 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: DataTables_Table_4, href:
    CREATED = (By.XPATH, u'//div[6]/div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 960 y: 347 width: 242 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: DataTables_Table_4, href:
    STATUS = (By.XPATH, u'//div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[4]') # x: 1202 y: 347 width: 242 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: DataTables_Table_4, href:
    BUTTON_CLOSE = (By.XPATH, u'//div[21]/div[3]/div[1]/button[1]') # x: 1388 y: 693 width: 67 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: DataTables_Table_4, href:

    def find_and_click_mgm_request(self):
        """
        Click first management request in management request table
        """
        element_rowtable = self.get_table_column_and_row_by_text((By.ID, 'DataTables_Table_4'),"SUBMITTED FOR APPROVAL","TBODY/TR","TD")
        req_number = self.get_text(element_rowtable[0].find_elements(By.XPATH, "TD")[0])
        element_rowtable[0].find_element(By.LINK_TEXT, str(req_number)).click()
        #self.click_table_cell_by_column_and_row(self.ID_SECURITYSERVER_MANAGEMENT_REQUESTS,element_rowtable[2], element_rowtable[3])
