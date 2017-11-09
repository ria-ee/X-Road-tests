# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sidebar(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161007174738
    # Pagemodel url: https://test-cs2.i.palveluvayla.com:4000/
    # Pagemodel area: (2, 1, 273, 593)
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
    XROAD_ID_FISUOMI = (By.CSS_SELECTOR, u'.xroad-id') # x: 20 y: 78 width: 63 height: 23, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SERVER_INFO_CENTRAL = (By.CSS_SELECTOR, u'#server-info>h2') # x: 0 y: 99 width: 270 height: 13, tag: h2, type: , name: None, form_id: , checkbox: , table_id: , href:
    DATA_NAME_SECURITYSERVERS_SECURITY_SERVERS = (By.CSS_SELECTOR, u'a[data-name="securityservers"]') # x: 20 y: 198 width: 99 height: 18, tag: a, type: , name: securityservers, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/securityservers
    DATA_NAME_GROUPS_GLOBAL = (By.CSS_SELECTOR, u'a[data-name="groups"]') # x: 20 y: 226 width: 89 height: 18, tag: a, type: , name: groups, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/groups
    DATA_NAME_CENTRAL_SERVICES = (By.CSS_SELECTOR, u'a[data-name="central_services"]') # x: 20 y: 254 width: 99 height: 18, tag: a, type: , name: central_services, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/central_services
    DATA_NAME_APPROVED_CAS_CERTIFICATION_SERVICES = (By.CSS_SELECTOR, u'a[data-name="approved_cas"]') # x: 20 y: 282 width: 129 height: 18, tag: a, type: , name: approved_cas, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/approved_cas
    DATA_NAME_TSPS_TIMESTAMPING_SERVICES = (By.CSS_SELECTOR, u'a[data-name="tsps"]') # x: 20 y: 310 width: 143 height: 18, tag: a, type: , name: tsps, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/tsps
    DATA_NAME_REQUESTS_MANAGEMENT = (By.CSS_SELECTOR, u'a[data-name="requests"]') # x: 20 y: 413 width: 143 height: 18, tag: a, type: , name: requests, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/requests
    DATA_NAME_CONFIGURATION_MANAGEMENT_GLOBAL = (By.CSS_SELECTOR, u'a[data-name="configuration_management"]') # x: 20 y: 441 width: 128 height: 18, tag: a, type: , name: configuration_management, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/configuration_management
    DATA_NAME_SYSTEM_SETTINGS = (By.CSS_SELECTOR, u'a[data-name="system_settings"]') # x: 20 y: 469 width: 98 height: 18, tag: a, type: , name: system_settings, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/system_settings
    DATA_NAME_BACKUP_BACK_UP_AND_RESTORE = (By.CSS_SELECTOR, u'a[data-name="backup"]') # x: 20 y: 497 width: 129 height: 18, tag: a, type: , name: backup, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/backup

    # Dynamic objects:
    MEMBERS = (By.LINK_TEXT, u'Members') # x: 20 y: 136 width: 59 height: 18, tag: a, type: , name: , form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/ # Dynamic object
    DATA_NAME_ABOUT_VERSION = (By.CSS_SELECTOR, u'a[data-name="about"]') # x: 20 y: 530 width: 45 height: 18, tag: a, type: , name: about, form_id: , checkbox: , table_id: , href: https://xroad-lxd-cs.lxd:4000/about

    def verify_central_server_title(self):
        """
        Verify that page contains central server title

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.SERVER_INFO_CENTRAL*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_contain`, *self.SERVER_INFO_CENTRAL*, *u'CENTRAL SERVER'*
        """
        self.wait_until_element_is_visible(self.SERVER_INFO_CENTRAL)
        self.element_should_contain(self.SERVER_INFO_CENTRAL, u'CENTRAL SERVER')

    def click_link_data_name_securityservers_security_servers(self):
        """
        Click sidebar link to open security server view
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.DATA_NAME_SECURITYSERVERS_SECURITY_SERVERS*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_SECURITYSERVERS_SECURITY_SERVERS*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: https://test-cs.i.palveluvayla.com:4000/securityservers
        self.wait_until_element_is_enabled(self.DATA_NAME_SECURITYSERVERS_SECURITY_SERVERS)
        self.click_element(self.DATA_NAME_SECURITYSERVERS_SECURITY_SERVERS)
        self.wait_until_jquery_ajax_loaded()

    def click_link_data_name_groups(self):
        """
        Click sidebar link to open

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.DATA_NAME_GROUPS*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_GROUPS*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: https://test-cs.i.palveluvayla.com:4000/groups
        self.wait_until_element_is_enabled(self.DATA_NAME_GROUPS)
        self.click_element(self.DATA_NAME_GROUPS)
        self.wait_until_jquery_ajax_loaded()

    def click_link_data_name_central_services(self):
        """
        Click sidebar link to open central services view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.DATA_NAME_CENTRAL_SERVICES*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_CENTRAL_SERVICES*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: https://test-cs.i.palveluvayla.com:4000/central_services
        self.wait_until_element_is_enabled(self.DATA_NAME_CENTRAL_SERVICES)
        self.click_element(self.DATA_NAME_CENTRAL_SERVICES)
        self.wait_until_jquery_ajax_loaded()

    def click_link_data_name_approved_cas_certification_services(self):
        """
        Click sidebar link to open certificate services view
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.DATA_NAME_APPROVED_CAS_CERTIFICATION_SERVICES*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_APPROVED_CAS_CERTIFICATION_SERVICES*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: https://test-cs.i.palveluvayla.com:4000/approved_cas
        self.wait_until_element_is_enabled(self.DATA_NAME_APPROVED_CAS_CERTIFICATION_SERVICES)
        self.click_element(self.DATA_NAME_APPROVED_CAS_CERTIFICATION_SERVICES)
        self.wait_until_jquery_ajax_loaded()

    def click_link_data_name_requests_management(self):
        """
        Click sidebar link to open requests management view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.DATA_NAME_REQUESTS_MANAGEMENT*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_REQUESTS_MANAGEMENT*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: https://test-cs.i.palveluvayla.com:4000/requests
        self.wait_until_element_is_enabled(self.DATA_NAME_REQUESTS_MANAGEMENT)
        self.click_element(self.DATA_NAME_REQUESTS_MANAGEMENT)
        self.wait_until_jquery_ajax_loaded()

    def click_link_data_name_configuration_management(self):
        """
        Click sidebar link to open configuration management view
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.DATA_NAME_CONFIGURATION_MANAGEMENT_GLOBAL*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_CONFIGURATION_MANAGEMENT_GLOBAL*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: https://test-cs.i.palveluvayla.com:4000/configuration_management
        self.wait_until_element_is_enabled(self.DATA_NAME_CONFIGURATION_MANAGEMENT_GLOBAL)
        self.click_element(self.DATA_NAME_CONFIGURATION_MANAGEMENT_GLOBAL)
        self.wait_until_jquery_ajax_loaded()

    def click_link_data_name_system_settings(self):
        """
        Click sidebar link to open system settings view
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.DATA_NAME_SYSTEM_SETTINGS*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_SYSTEM_SETTINGS*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: https://test-cs.i.palveluvayla.com:4000/system_settings
        self.wait_until_element_is_enabled(self.DATA_NAME_SYSTEM_SETTINGS)
        self.click_element(self.DATA_NAME_SYSTEM_SETTINGS)
        self.wait_until_jquery_ajax_loaded()

    def click_link_data_name_backup_back_up_and_restore(self):
        """
        Click sidebar link to open backups view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.DATA_NAME_BACKUP_BACK_UP_AND_RESTORE*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_BACKUP_BACK_UP_AND_RESTORE*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: https://test-cs.i.palveluvayla.com:4000/backup
        self.wait_until_element_is_enabled(self.DATA_NAME_BACKUP_BACK_UP_AND_RESTORE)
        self.click_element(self.DATA_NAME_BACKUP_BACK_UP_AND_RESTORE)
        self.wait_until_jquery_ajax_loaded()

    def click_link_data_name_about_version(self):
        """
        Click sidebar link to open version view
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_ABOUT_VERSION*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: https://test-cs.i.palveluvayla.com:4000/about
        self.click_element(self.DATA_NAME_ABOUT_VERSION)
        self.wait_until_jquery_ajax_loaded()

    def click_element_members(self):
        """
        Click sidebar link to open members view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.MEMBERS*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.MEMBERS*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_element_is_enabled(self.MEMBERS)
        self.click_element(self.MEMBERS)
        self.wait_until_jquery_ajax_loaded()

    def click_link_data_name_tsps_stamping_services(self):
        """
        Click sidebar link to open timestamping services view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_enabled`, *self.DATA_NAME_TSPS_TIMESTAMPING_SERVICES*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_TSPS_TIMESTAMPING_SERVICES*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_element_is_enabled(self.DATA_NAME_TSPS_TIMESTAMPING_SERVICES)
        self.click_element(self.DATA_NAME_TSPS_TIMESTAMPING_SERVICES)
        self.wait_until_jquery_ajax_loaded()
