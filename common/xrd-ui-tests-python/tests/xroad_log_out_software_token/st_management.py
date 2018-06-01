# coding=utf-8

from selenium.webdriver.common.by import By
from helpers import auditchecker
from view_models import sidebar, keys_and_certificates_table, popups, log_constants


def test_edit_conf(case, ssh_host=None, ssh_username=None, ssh_password=None, token_pin=None):
    self = case

    def logging_conf():

        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
            current_log_lines = log_checker.get_line_count()

        '''Click "Keys and Certificates" button" '''
        self.log('Click "Keys and Certificates" button"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        software_token_logout(self)

        '''Verify "LOGOUT" from audit log'''

        if ssh_host is not None:
            # Check logs for entries
            self.log('UC SS_26: 3.System logs the event “Log out from token” to the audit log.')
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

        '''Log in again'''
        software_token_login(self, token_pin=token_pin)

    return logging_conf


def software_token_logout(self):
    self.log('UC SS_26: 1.SS administrator selects to log out of a software token.')
    '''Click "LOGOUT"'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.SOFTTOKEN_LOGOUT).click()
    self.wait_jquery()
    self.log('UC SS_26: 2.System logs out of the token.')

    '''Set "Log out from token" to logdata'''
    self.logdata.append(log_constants.TOKEN_LOG_OUT)

    '''Click on Token row'''
    self.wait_until_visible(type=By.XPATH,
                            element=keys_and_certificates_table.SOFTTOKEN_TABLE_ROW_XPATH2).click()
    self.wait_jquery()
    self.log('Verify that "Generate key" button is disabled')
    '''Verify that "Generate key" button is disabled'''
    generate_key_btn = self.wait_until_visible(self.by_id(keys_and_certificates_table.GENERATEKEY_BTN_ID)).is_enabled()
    self.is_false(generate_key_btn,
                  msg='"Generate key" button is enabled')

    '''Click on Token key row'''
    self.wait_until_visible(type=By.XPATH,
                            element=keys_and_certificates_table.SOFTTOKEN_KEY_ROW).click()
    self.wait_jquery()

    self.log('Verify that "Generate CSR" button is disabled')
    '''Verify that "Generate CSR" button is disabled'''
    generate_csr_btn = self.wait_until_visible(self.by_id(keys_and_certificates_table.GENERATECSR_BTN_ID)).is_enabled()
    self.is_false(generate_csr_btn,
                  msg='"Generate key" button is enabled')

    return self.logdata


def software_token_login(self, token_pin=None):
    self.log('Log in again')
    '''Click "LOGIN"'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.SOFTTOKEN_LOGIN).click()
    self.wait_jquery()

    '''Input area'''
    key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_PIN_LABEL_AREA)

    '''Insert correct PIN'''
    self.input(key_label_input, token_pin)
    self.wait_jquery()

    '''Click "OK" button'''
    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_OK_BTN_XPATH).click()
    self.wait_jquery()

    return self.logdata
