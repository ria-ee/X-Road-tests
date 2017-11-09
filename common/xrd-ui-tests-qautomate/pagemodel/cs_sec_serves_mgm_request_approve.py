# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_serves_mgm_request_approve(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151214093830
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers#
    # Pagemodel area: (899, 19, 604, 774)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
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
    TITLE = (By.ID, u'ui-id-14') # x: 911 y: 35 width: 355 height: 21
    CLIENT_REG_REQUEST_EDIT_BODY_MANAGEMENT_COMMON_CONTAINER_INFORMATION = (By.CSS_SELECTOR, u'#client_reg_request_edit_dialog>.dialog-body>#management_request_edit_common>section.container>h2>span') # x: 926 y: 93 width: 182 height: 22
    ID_SECURITYSERVERS = (By.ID, u'securityservers') # x: 291 y: 153 width: 1608 height: 383
    ID_MANAGEMENT_REQUEST_EDIT_COMMON_OWNER_NAME = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[1]/TD[1]') # x: 926 y: 425 width: 101 height: 43
    ID_MANAGEMENT_REQUEST_EDIT_COMMON_ORG1 = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[1]/TD[2]/P[1]') # x: 1032 y: 430 width: 425 height: 33
    ID_MANAGEMENT_REQUEST_EDIT_COMMON_OWNER_CLASS = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[2]/TD[1]') # x: 926 y: 468 width: 101 height: 43
    ID_MANAGEMENT_REQUEST_EDIT_COMMON_PUB = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[2]/TD[2]/P[1]') # x: 1032 y: 473 width: 425 height: 33
    ID_MANAGEMENT_REQUEST_EDIT_COMMON_OWNER = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[3]/TD[1]') # x: 926 y: 511 width: 101 height: 43
    ID_MANAGEMENT_REQUEST_EDIT_COMMON_ORG1_0 = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[3]/TD[2]/P[1]') # x: 1032 y: 516 width: 425 height: 33
    ID_MANAGEMENT_REQUEST_EDIT_COMMON_SERVER = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[4]/TD[1]') # x: 926 y: 554 width: 101 height: 43
    ID_MANAGEMENT_REQUEST_EDIT_COMMON_SS1 = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[4]/TD[2]/P[1]') # x: 1032 y: 559 width: 425 height: 33
    ID_MANAGEMENT_REQUEST_EDIT_COMMON_0 = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[5]/TD[1]') # x: 926 y: 597 width: 101 height: 42
    ID_MANAGEMENT_REQUEST_EDIT_COMMON = (By.XPATH, u'id(\'management_request_edit_common\')/SECTION[2]/TABLE[1]/TBODY[1]/TR[5]/TD[2]/P[1]') # x: 1032 y: 602 width: 425 height: 32
    CLIENT_REG_REQUEST_EDIT_BODY_CONTAINER_SUBMITTED_FOR_REGISTRATION = (By.CSS_SELECTOR, u'#client_reg_request_edit_dialog>.dialog-body>.container>h2>span') # x: 926 y: 646 width: 293 height: 22
    ID_CLIENT_REG_REQUEST_EDIT_NAME = (By.XPATH, u'id(\'client_reg_request_edit_dialog\')/DIV[1]/SECTION[1]/TABLE[1]/TBODY[1]/TR[1]/TD[1]') # x: 926 y: 675 width: 124 height: 43
    CLIENT_REG_REQUEST_EDIT_BODY_CONTAINER_NAME_ORG1 = (By.CSS_SELECTOR, u'#client_reg_request_edit_dialog>.dialog-body>.container>.details>tbody>tr>td>.client_details_name') # x: 1054 y: 680 width: 402 height: 33
    ID_CLIENT_REG_REQUEST_EDIT_CLASS = (By.XPATH, u'id(\'client_reg_request_edit_dialog\')/DIV[1]/SECTION[1]/TABLE[1]/TBODY[1]/TR[2]/TD[1]') # x: 926 y: 718 width: 124 height: 43
    CLIENT_REG_REQUEST_EDIT_BODY_CONTAINER_CLASS_PUB = (By.CSS_SELECTOR, u'#client_reg_request_edit_dialog>.dialog-body>.container>.details>tbody>tr>td>.client_details_class') # x: 1054 y: 723 width: 402 height: 33
    BUTTON_CLOSE = (By.CSS_SELECTOR, u'button.right.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only') # x: 1243 y: 752 width: 67 height: 37

    # Dynamic objects:
    BUTTON_APPROVE = (By.CLASS_NAME, u'ui-state-focus')     # x: 1170 y: 827 width: 85 height: 37 # Dynamic object

    def click_approve_request(self):
        """
        Click button to approve requests

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_APPROVE*
        """
        self.click_element(self.BUTTON_APPROVE)