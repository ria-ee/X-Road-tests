# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_backup_restore_dlg_up_back_conf_exist(CommonUtils):
    """

    """
    # Pagemodel timestamp: 20171019021218
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/backup
    # Pagemodel area: (593, 355, 735, 146)
    # Pagemodel screen resolution: (1920, 975)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Create automated methods: False
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
    DATA_NAME_FILE_UPLOAD_UI_RESIZABLE_W = (By.CSS_SELECTOR, u'div[data-name="file_upload_dialog"]>.ui-resizable-w') # x: 605 y: 312 width: 7 height: 230, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    DATA_NAME_FILE_UPLOAD_UI_RESIZABLE_E = (By.CSS_SELECTOR, u'div[data-name="file_upload_dialog"]>.ui-resizable-e') # x: 1308 y: 312 width: 7 height: 230, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    SUBMIT_0 = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]') # x: 1228 y: 352 width: 51 height: 49, tag: button, type: submit, name: None, form_id: upload_new, checkbox: , table_id: 2, href:
    SUBMIT = (By.XPATH, u'//div[8]/div[1]/div[1]/button[2]') # x: 1279 y: 352 width: 51 height: 49, tag: button, type: submit, name: None, form_id: upload_new, checkbox: , table_id: 2, href:
    ID_UI_ID_4 = (By.ID, u'ui-id-4') # x: 601 y: 366 width: 167 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    UNKNOWN = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]/i[1]') # x: 1243 y: 366 width: 21 height: 21, tag: i, type: , name: None, form_id: upload_new, checkbox: , table_id: 2, href:
    UNKNOWN_0 = (By.XPATH, u'//div[8]/div[1]/div[1]/button[2]/i[1]') # x: 1299 y: 369 width: 12 height: 15, tag: i, type: , name: None, form_id: upload_new, checkbox: , table_id: 2, href:
    SELECTED_FILE_C_FAKEPATH_CONF_BACKUP_20171018_230834_TAR_TEXT = (By.CSS_SELECTOR, u'.selected_file') # x: 630 y: 382 width: 569 height: 32, tag: input, type: text, name: None, form_id: , checkbox: , table_id: 2, href:
    UI_WIDGET_CONTENT_CORNER_ALL_FRONT_BUTTONS_DRAGGABLE_RESIZABLE_CONFIRM = (By.CSS_SELECTOR, u'div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable>#confirm') # x: 591 y: 403 width: 740 height: 53, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    CANCEL_0 = (By.XPATH, u'//div[11]/div[1]/button[2]') # x: 1155 y: 461 width: 75 height: 36, tag: button, type: button, name: None, form_id: upload_new, checkbox: , table_id: 2, href:
    UI_BUTTONSET_CONFIRM = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>#confirm') # x: 1240 y: 461 width: 85 height: 36, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:
    CANCEL = (By.XPATH, u'//div[11]/div[1]/button[2]/span[1]') # x: 1168 y: 470 width: 49 height: 18, tag: span, type: , name: None, form_id: upload_new, checkbox: , table_id: 2, href: None
    CONFIRM_UI_TEXT = (By.CSS_SELECTOR, u'#confirm>.ui-button-text') # x: 1253 y: 470 width: 59 height: 18, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None

    def click_button_confirm(self, parameters=None):
        """
        Click button confirm
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.UI_BUTTONSET_CONFIRM*
        """
        self.click_element(self.UI_BUTTONSET_CONFIRM)
