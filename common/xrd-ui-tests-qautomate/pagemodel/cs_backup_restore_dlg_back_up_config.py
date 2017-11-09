# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_backup_restore_dlg_back_up_config(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20170206125749
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/backup
    # Pagemodel area: (511, 181, 899, 598)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1308 y: 180 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: backup_files, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1359 y: 180 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: backup_files, href:
    CREATING_DATABASE_DUMP_TO_LIB_XROAD_DBDUMP_DAT = (By.XPATH, u'//pre[1]/p[1]') # x: 525 y: 260 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    CREATING_TAR_ARCHIVE_TO_LIB_XROAD_BACKUP_CONF_20170206_105652 = (By.XPATH, u'//pre[1]/p[2]') # x: 525 y: 288 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    CENTRAL_XROAD_6_8_FISUOMI = (By.XPATH, u'//pre[1]/p[3]') # x: 525 y: 316 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    TAR_REMOVING_LEADING_FROM_MEMBER_NAMES = (By.XPATH, u'//p[4]') # x: 525 y: 344 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD = (By.XPATH, u'//p[5]') # x: 525 y: 372 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_NGINX = (By.XPATH, u'//p[6]') # x: 525 y: 400 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_NGINX_INSECURE_CONF = (By.XPATH, u'//p[7]') # x: 525 y: 428 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_NGINX_PUBLIC_CONF = (By.XPATH, u'//p[8]') # x: 525 y: 456 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_NGINX_CONF = (By.XPATH, u'//p[9]') # x: 525 y: 484 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_NGINX_DEFAULT_CONF = (By.XPATH, u'//p[10]') # x: 525 y: 512 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_NGINX_SECURE_ADDONS_CONF = (By.XPATH, u'//p[11]') # x: 525 y: 540 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_GLOBALCONF = (By.XPATH, u'//p[12]') # x: 525 y: 568 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_GLOBALCONF_INSTANCE_IDENTIFIER = (By.XPATH, u'//p[13]') # x: 525 y: 596 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_GLOBALCONF_FISUOMI = (By.XPATH, u'//p[14]') # x: 525 y: 624 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_GLOBALCONF_FISUOMI_SHARED_PARAMS_XML_METADATA = (By.XPATH, u'//p[15]') # x: 525 y: 652 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_GLOBALCONF_FISUOMI_SHARED_PARAMS_XML = (By.XPATH, u'//p[16]') # x: 525 y: 680 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    ETC_XROAD_GLOBALCONF_FISUOMI_PRIVATE_PARAMS_XML = (By.XPATH, u'//p[17]') # x: 525 y: 708 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    MESSAGE_FA_TIMES = (By.CSS_SELECTOR, u'.message>.fa-times') # x: 1380 y: 711 width: 20 height: 20, tag: i, type: , name: None, form_id: , checkbox: , table_id: , href:
    ETC_XROAD_GLOBALCONF_FISUOMI_PRIVATE_PARAMS_XML_METADATA = (By.XPATH, u'//p[18]') # x: 525 y: 736 width: 861 height: 18, tag: p, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    BUTTON_OK = (By.CSS_SELECTOR, u'.ui-state-focus') # x: 1361 y: 739 width: 44 height: 36, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    def click_button_ok(self):
        """
        Click ok button

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        self.click_element(self.BUTTON_OK)

    def click_button_cancel(self):
        """
        Click cancel button
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.MENUBAR_CLOSE*
        """
        self.click_element(self.MENUBAR_CLOSE)
