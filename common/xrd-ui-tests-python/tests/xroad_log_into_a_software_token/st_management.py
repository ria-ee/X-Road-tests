# coding=utf-8

from selenium.webdriver.common.by import By
from helpers import auditchecker
from view_models import sidebar, keys_and_certificates_table, popups, messages, log_constants
import time


def test_edit_conf(case, ssh_host=None, ssh_username=None, ssh_password=None):
    self = case

    def backup_conf():

        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
            current_log_lines = log_checker.get_line_count()

        '''Click "Keys and Certificates" button" '''
        self.log('Click "Keys and Certificates" button"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        '''Click "LOGOUT"'''
        self.driver.find_element_by_xpath(keys_and_certificates_table.SOFTTOKEN_LOGOUT).click()
        self.wait_jquery()

        '''Click "LOGIN"'''
        self.log('SS_24 1.SS administrator selects to log in to a software token.')

        self.driver.find_element_by_xpath(keys_and_certificates_table.SOFTTOKEN_LOGIN).click()
        self.wait_jquery()

        find_errors_login(self)
        whitespace_login(self)
        successful_login(self)

        '''Check audit log'''

        if ssh_host is not None:
            # Check logs for entries
            self.log('Check the audit log')
            self.log('SS_24 5.System logs the event “Log in to token” to the audit log.')

            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

    return backup_conf


def successful_login(self):
    self.log('Log out and log in for testing correct PIN')
    self.wait_jquery()
    '''Click "LOGOUT"'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.SOFTTOKEN_LOGOUT).click()
    self.wait_jquery()

    '''Click "LOGIN"'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.SOFTTOKEN_LOGIN).click()
    self.wait_jquery()

    '''Input area'''
    key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_PIN_LABEL_AREA)
    self.log('SS_24 2.SS administrator enters the PIN code of the token.')

    '''Insert correct PIN'''
    self.input(key_label_input, keys_and_certificates_table.TOKEN_PIN)
    self.wait_jquery

    '''Click "OK" button'''
    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_OK_BTN_XPATH).click()
    self.wait_jquery
    self.log('SS_24 4.System verifies that the PIN code is correct and logs in to the token.')

    '''Set "Log in to token" to logdata'''
    self.logdata.append(log_constants.TOKEN_LOG_OUT)

    self.logdata.append(log_constants.SOFTTOKEN_LOGIN_SUCCESS)
    time.sleep(1)
    return self.logdata


def find_errors_login(self):
    error_count = 0
    success_count = 0
    KEY_LABEL_TEXT_AND_RESULTS = [
        [256 * 'S', messages.INPUT_EXCEEDS_255_CHARS.format(keys_and_certificates_table.SOFTTOKEN_PIN_ERROR_PARAMETER),
         None, False],
        ['', messages.MISSING_PARAMETER.format(keys_and_certificates_table.SOFTTOKEN_PIN_ERROR_PARAMETER), None, False],
        [keys_and_certificates_table.TOKEN_PIN[::-1], messages.TOKEN_PIN_INCORRECT, None, False]]

    # Loop through different key label names and expected results
    counter = 1
    for keys in KEY_LABEL_TEXT_AND_RESULTS:

        input_text = keys[0]
        error_message = keys[1]
        error = error_message is not None

        '''Input area'''
        key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_PIN_LABEL_AREA)

        '''Inserting PIN from KEY_LABEL_TEXT_AND_RESULTS'''
        self.input(key_label_input, input_text)
        self.wait_jquery()

        '''Click "OK" button'''
        self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_OK_BTN_XPATH).click()
        self.wait_jquery
        time.sleep(2)
        '''Set "Log in to token failed" to logdata'''
        self.logdata.append(log_constants.SOFTTOKEN_LOGIN_FAILED)


        ui_error = messages.get_error_message(self)

        self.log('SS_24 3a., 4a. The process of parsing the user input terminated with an error message. Checking error message: "{0}"'.format(ui_error))
        '''Expecting error'''
        if error:
            if ui_error is not None:
                error_count += 1
                self.is_equal(ui_error, error_message, msg='Wrong error message, expected: {0}'.format(error_message))
            else:
                raise RuntimeError('Not able to verify error messages')
        else:
            self.is_none(ui_error, msg='Got error message for: "{0}"'.format(input_text))

            success_count += 1
        counter += 1

        self.wait_jquery()
    return success_count, error_count, self.logdata


def whitespace_login(self):
    self.log('Log in with correct PIN that consist whitespaces')

    '''Input area'''
    key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_PIN_LABEL_AREA)

    '''Inserting name correct PIN with whitespaces'''
    self.input(key_label_input, keys_and_certificates_table.SOFTTOKEN_PIN_WHITESPACES)
    self.wait_jquery

    '''Click "OK" button'''
    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_OK_BTN_XPATH).click()
    self.wait_jquery

    '''Set "Log in to token" to logdata'''
    self.logdata.append(log_constants.SOFTTOKEN_LOGIN_SUCCESS)
    return self.logdata
