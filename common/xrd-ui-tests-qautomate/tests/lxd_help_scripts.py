# -*- coding: utf-8 -*-
from webframework import TESTDATA
from webframework.extension.base.setupTest import SetupTest
from webframework.extension.parsers.parameter_parser import get_all_parameters
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.open_application import Open_application
from common_lib.component_cs import Component_cs
from common_lib.component_ss import Component_ss
from selenium.webdriver.common.keys import Keys
from webframework.extension.config import set_config_value
from common_lib.component_cs_conf_mgm import Component_cs_conf_mgm
from common_lib.component_ss_sidebar import Component_ss_sidebar
from common_lib.component_cs_sidebar import Component_cs_sidebar
from common_lib.component_ss_keys_and_certs import Component_ss_keys_and_certs
from common_lib.component_ss_backup import Component_ss_backup
from common_lib.component_cs_backup import Component_cs_backup
from pagemodel.cs_backup_restore import Cs_backup_restore
from pagemodel.cs_backup_restore_dlg_delete_confirm import Cs_backup_restore_dlg_delete_confirm
from pagemodel.ss_backup_restore_confirm_delete import Ss_backup_restore_confirm_delete
from pagemodel.ss_backup_restore import Ss_backup_restore

class Lxd_help_scripts(SetupTest):
    """
    Test set that contains useful test cases for lxd enviroment

    **Changelog:**
        * 11.07.2017
            | Documentation updated
    """
    common_utils = CommonUtils()
    open_application = Open_application()
    component_cs = Component_cs()
    component_ss = Component_ss()
    component_cs_conf_mgm = Component_cs_conf_mgm()
    component_ss_sidebar = Component_ss_sidebar()
    component_cs_sidebar = Component_cs_sidebar()
    component_ss_keys_and_certs = Component_ss_keys_and_certs()
    component_ss_backup = Component_ss_backup()
    component_cs_backup = Component_cs_backup()
    cs_backup_restore = Cs_backup_restore()
    cs_backup_restore_dlg_delete_confirm = Cs_backup_restore_dlg_delete_confirm()
    ss_backup_restore_confirm_delete = Ss_backup_restore_confirm_delete()
    ss_backup_restore = Ss_backup_restore()

    @classmethod
    def setUpTestSet(self):
        """
        Method that runs before every unittest

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.autogen_browser = self.Autogen_browser = self.common_utils`
        """
        self.autogen_browser = self.common_utils.open_browser()

    @classmethod
    def tearDownTestSet(self):
        """
        Method that runs after every unittest

        *Updated: 11.07.2017*

        """
        pass
        #self.common_utils.close_all_browsers()

    def setUp(self):
        """
        Method that runs before every test case

        *Updated: 11.07.2017*

        """
        pass

    def tearDown(self):
        """
        Method that runs after every test case

        *Updated: 11.07.2017*

        """
        set_config_value("default_timeout", 20)

    def test_login_all_servers(self):
        """
        Test case that logins to every lxd server

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~common_lib.component_cs.Component_cs.login`, *u'cs_url'*, *False*
                * **Step 2:** :func:`~common_lib.component_ss.Component_ss.login`, *u'ss_mgm_url'*, *False*
                * **Step 3:** :func:`~common_lib.component_ss.Component_ss.login`, *u'ss1_url'*, *False*
                * **Step 4:** :func:`~common_lib.component_ss.Component_ss.login`, *u'ss2_url'*, *False*
                * **Step 5:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
        """
        try:
            self.component_cs.login(u'cs_url', False)
        except:
            pass

        try:
            self.component_ss.login(u'ss_mgm_url', False)
        except:
            pass

        try:
            self.component_ss.login(u'ss1_url', False)
        except:
            pass

        try:
            self.component_ss.login(u'ss2_url', False)
        except:
            pass

        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])

    def test_add_all_pins(self):
        """
        Login to every lxd enviroment server token

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
                * **Step 2:** :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_global_configuration_view`
                * **Step 3:** :func:`~common_lib.component_cs_conf_mgm.Component_cs_conf_mgm.log_in_to_software_token`, *u'cs_url'*
                * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss_mgm_url']['url']*
                * **Step 5:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * **Step 6:** :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed`, *u'ss_mgm_url'*
                * **Step 7:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss1_url']['url']*
                * **Step 8:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * **Step 9:** :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed`, *u'ss1_url'*
                * **Step 10:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss2_url']['url']*
                * **Step 11:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_keys_and_certs_view`
                * **Step 12:** :func:`~common_lib.component_ss_keys_and_certs.Component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed`, *u'ss2_url'*
                * **Step 13:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
        """
        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])
        self.component_cs_sidebar.open_global_configuration_view()
        try:
            self.component_cs_conf_mgm.log_in_to_software_token(u'cs_url')
        except:
            print("Pin not needed?")

        self.common_utils.open_url(TESTDATA[u'ss_mgm_url']['url'])
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed(u'ss_mgm_url')

        self.common_utils.open_url(TESTDATA[u'ss1_url']['url'])
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed(u'ss1_url')

        self.common_utils.open_url(TESTDATA[u'ss2_url']['url'])
        self.component_ss_sidebar.open_keys_and_certs_view()
        self.component_ss_keys_and_certs.active_token_and_insert_pin_code_if_needed(u'ss2_url')

        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])

    def test_generate_all_backup(self):
        """
        Generate backup of all lxd enviroment servers

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
                * **Step 2:** :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * **Step 3:** :func:`~common_lib.component_cs_backup.Component_cs_backup.generate_backup`
                * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss_mgm_url']['url']*
                * **Step 5:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * **Step 6:** :func:`~common_lib.component_ss_backup.Component_ss_backup.generate_backup`
                * **Step 7:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss1_url']['url']*
                * **Step 8:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * **Step 9:** :func:`~common_lib.component_ss_backup.Component_ss_backup.generate_backup`
                * **Step 10:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss2_url']['url']*
                * **Step 11:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * **Step 12:** :func:`~common_lib.component_ss_backup.Component_ss_backup.generate_backup`
                * **Step 13:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
        """
        #self.test_login_all_servers()

        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])
        self.component_cs_sidebar.open_backup_restore_view()
        self.component_cs_backup.generate_backup()

        self.common_utils.open_url(TESTDATA[u'ss_mgm_url']['url'])
        self.component_ss_sidebar.open_backup_restore_view()
        self.component_ss_backup.generate_backup()

        self.common_utils.open_url(TESTDATA[u'ss1_url']['url'])
        self.component_ss_sidebar.open_backup_restore_view()
        self.component_ss_backup.generate_backup()

        self.common_utils.open_url(TESTDATA[u'ss2_url']['url'])
        self.component_ss_sidebar.open_backup_restore_view()
        self.component_ss_backup.generate_backup()

        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])

    def test_restore_all_backup(self):
        """
        Restore all lxd enviroment server backups

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
                * **Step 2:** :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * **Step 3:** :func:`~common_lib.component_cs_backup.Component_cs_backup.restore_backup`
                * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss_mgm_url']['url']*
                * **Step 5:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * **Step 6:** :func:`~common_lib.component_ss_backup.Component_ss_backup.restore_backup`
                * **Step 7:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss1_url']['url']*
                * **Step 8:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * **Step 9:** :func:`~common_lib.component_ss_backup.Component_ss_backup.restore_backup`
                * **Step 10:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss2_url']['url']*
                * **Step 11:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * **Step 12:** :func:`~common_lib.component_ss_backup.Component_ss_backup.restore_backup`
                * **Step 13:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
        """
        #self.test_login_all_servers()

        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])
        self.component_cs_sidebar.open_backup_restore_view()
        self.component_cs_backup.restore_backup()

        self.common_utils.open_url(TESTDATA[u'ss_mgm_url']['url'])
        self.component_ss_sidebar.open_backup_restore_view()
        self.component_ss_backup.restore_backup()

        self.common_utils.open_url(TESTDATA[u'ss1_url']['url'])
        self.component_ss_sidebar.open_backup_restore_view()
        self.component_ss_backup.restore_backup()

        self.common_utils.open_url(TESTDATA[u'ss2_url']['url'])
        self.component_ss_sidebar.open_backup_restore_view()
        self.component_ss_backup.restore_backup()

        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])

    def test_delete_all_backups(self):
        """
        Delete all backups on lxd enviroment servers

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
                * **Step 2:** :func:`~common_lib.component_cs_sidebar.Component_cs_sidebar.open_backup_restore_view`
                * **Step 3:** :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_newest_delete`
                * **Step 4:** :func:`~pagemodel.cs_backup_restore_dlg_delete_confirm.Cs_backup_restore_dlg_delete_confirm.click_button_ui_buttonset_confirm`
                * **Step 5:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss_mgm_url']['url']*
                * **Step 6:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * **Step 7:** :func:`~pagemodel.ss_backup_restore.Ss_backup_restore.click_element_first_row_delete`
                * **Step 8:** :func:`~pagemodel.ss_backup_restore_confirm_delete.Ss_backup_restore_confirm_delete.click_button_confirm`
                * **Step 9:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss1_url']['url']*
                * **Step 10:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * **Step 11:** :func:`~pagemodel.ss_backup_restore.Ss_backup_restore.click_element_first_row_delete`
                * **Step 12:** :func:`~pagemodel.ss_backup_restore_confirm_delete.Ss_backup_restore_confirm_delete.click_button_confirm`
                * **Step 13:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss2_url']['url']*
                * **Step 14:** :func:`~common_lib.component_ss_sidebar.Component_ss_sidebar.open_backup_restore_view`
                * **Step 15:** :func:`~pagemodel.ss_backup_restore.Ss_backup_restore.click_element_first_row_delete`
                * **Step 16:** :func:`~pagemodel.ss_backup_restore_confirm_delete.Ss_backup_restore_confirm_delete.click_button_confirm`
        """
        set_config_value("default_timeout", 5)
        # self.test_login_all_servers()

        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])
        self.component_cs_sidebar.open_backup_restore_view()
        for x in range(100):
            try:
                self.cs_backup_restore.click_element_newest_delete()
                self.cs_backup_restore_dlg_delete_confirm.click_button_ui_buttonset_confirm()
            except:
                break

        self.common_utils.open_url(TESTDATA[u'ss_mgm_url']['url'])
        self.component_ss_sidebar.open_backup_restore_view()
        for x in range(100):
            try:
                self.ss_backup_restore.click_element_first_row_delete()
                self.ss_backup_restore_confirm_delete.click_button_confirm()
            except:
                break

        self.common_utils.open_url(TESTDATA[u'ss1_url']['url'])
        self.component_ss_sidebar.open_backup_restore_view()
        for x in range(100):
            try:
                self.ss_backup_restore.click_element_first_row_delete()
                self.ss_backup_restore_confirm_delete.click_button_confirm()
            except:
                break

        self.common_utils.open_url(TESTDATA[u'ss2_url']['url'])
        self.component_ss_sidebar.open_backup_restore_view()
        for x in range(100):
            try:
                self.ss_backup_restore.click_element_first_row_delete()
                self.ss_backup_restore_confirm_delete.click_button_confirm()
            except:
                break

    def test_open_all_servers_into_tabs(self):
        """
        Open all lxd enviroment servers into different browser tabs (Firefox)

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'cs_url']['url']*
                * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss_mgm_url']['url']*
                * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss1_url']['url']*
                * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.open_url`, *TESTDATA[u'ss2_url']['url']*
        """
        driver = self.common_utils.driver_cache._get_current_driver()
        self.common_utils.open_url(TESTDATA[u'cs_url']['url'])

        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+'t')
        driver.switch_to.window(driver.window_handles[-1])
        self.common_utils.open_url(TESTDATA[u'ss_mgm_url']['url'])

        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+'t')
        driver.switch_to.window(driver.window_handles[-1])
        self.common_utils.open_url(TESTDATA[u'ss1_url']['url'])

        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+'t')
        driver.switch_to.window(driver.window_handles[-1])
        self.common_utils.open_url(TESTDATA[u'ss2_url']['url'])

        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL, Keys.SHIFT, Keys.TAB)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL, Keys.SHIFT, Keys.TAB)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL, Keys.SHIFT, Keys.TAB)
        driver.switch_to.window(driver.window_handles[-1])

    def test_initilization_all_servers(self):
        """
        Initialize all servers into different browser tabs by login in to server and token.

        *Updated: 11.07.2017*
        """
        set_config_value("default_timeout", 5)
        self.test_login_all_servers()
        self.test_add_all_pins()
        self.test_open_all_servers_into_tabs()