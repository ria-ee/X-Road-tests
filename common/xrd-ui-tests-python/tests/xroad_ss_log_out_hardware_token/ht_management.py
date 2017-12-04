# coding=utf-8

from selenium.webdriver.common.by import By
from helpers import auditchecker, xroad, ssh_client
from view_models import sidebar, keys_and_certificates_table, popups, messages, log_constants, \
    keys_and_certificates_table
import time
from selenium.common.exceptions import NoSuchElementException


def test_hardware_logout(case, ssh_host=None, ssh_username=None, ssh_password=None):
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

        if self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_ERROR_LOGIN2).is_displayed():
            hardware_token_login(self)


        '''Successful log out'''
        hardware_token_logout(self)


        '''Log back in'''
        hardware_token_login(self)

        '''Open connection'''
        sshclient = ssh_client.SSHClient(ssh_host, ssh_username, ssh_password)

        '''Stop docker container'''
        sshclient.exec_command('docker stop cssim410_test', sudo=True)
        '''Kill docker process'''
        sshclient.exec_command('pkill docker-', sudo=True)



        '''Click "LOGOUT" button'''
        self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOGOUT2).click()
        self.wait_jquery()

        self.log('UC SS_27:  2a. The logout attempt failed (e.g., token is inaccessible)."')
        '''Get error message'''
        ui_error = messages.get_error_message(self)
        '''Verify error message'''
        self.is_equal(ui_error, messages.HARDTOKEN_LOGOUT_FAILED,
                      msg='Wrong error message, expected: {0}'.format(messages.HARDTOKEN_LOGOUT_FAILED))

        '''Set "Log out from token failed" to logdata'''
        self.logdata.append(log_constants.HARDTOKEN_LOG_OUT_FAILED)


        '''Check audit log'''

        if ssh_host is not None:
            # Check logs for entries
            self.log('Check the audit log')
            self.log('SS_27 System checks audit log."Log out from token", "Log in to token", "Log out from token failed"')
            print self.logdata
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

        '''Start preconfigured docker container'''
        sshclient.exec_command('docker run -p3001:3001 -dt --rm --name cssim410_test cssim410_test', sudo=True)
        '''Restart xroad-signer service'''
        sshclient.exec_command('service xroad-signer restart', sudo=True)


    return logging_conf


def hardware_token_logout(self):
    self.log('UC SS_27: 1.SS administrator selects to log out of a hardware token.')
    '''Click "LOGOUT"'''
    self.wait_jquery()

    self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOGOUT2).click()
    self.wait_jquery()
    self.log('UC SS_27: 2.System logs out of the token.')

    '''Set "Log out from token" to logdata'''
    self.logdata.append(log_constants.TOKEN_LOG_OUT)

    '''Click on Token row'''
    self.wait_until_visible(type=By.XPATH,
                            element=keys_and_certificates_table.HARDTOKEN_TABLE_ROW_XPATH4).click()
    self.wait_jquery()
    self.log('Verify that "Generate key" button is disabled')
    '''Verify that "Generate key" button is disabled'''
    generate_key_btn = self.wait_until_visible(
        self.by_id(keys_and_certificates_table.GENERATEKEY_BTN_ID)).is_enabled()
    self.is_false(generate_key_btn,
                  msg='"Generate key" button is enabled')

    '''Verify "ENTER PIN" is displayed'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_ERROR_LOGIN2).is_displayed()

    return self.logdata


def hardware_token_login(self):
    self.log('Log in again')
    '''Click "LOGIN"'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_ERROR_LOGIN2).click()
    self.wait_jquery()

    '''Input area'''
    key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_PIN_LABEL_AREA)

    '''Insert correct PIN'''
    self.input(key_label_input, keys_and_certificates_table.TOKEN_PIN)
    self.wait_jquery
    self.logdata.append(log_constants.SOFTTOKEN_LOGIN_SUCCESS)


    '''Click "OK" button'''
    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_OK_BTN_XPATH).click()
    self.wait_jquery
    time.sleep(2)

    return self.logdata
