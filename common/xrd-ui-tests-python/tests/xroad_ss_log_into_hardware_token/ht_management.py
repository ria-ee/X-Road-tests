# coding=utf-8

from selenium.webdriver.common.by import By
from helpers import auditchecker, xroad, ssh_client
from view_models import sidebar, keys_and_certificates_table, popups, messages, log_constants, \
    keys_and_certificates_table
import time
from selenium.common.exceptions import NoSuchElementException


def test_hardtoken_login(case, ssh_host=None, ssh_username=None, ssh_password=None, pin=None, docker_ip = None):
    self = case

    def backup_conf():

        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
            current_log_lines = log_checker.get_line_count()

        sshclient = ssh_client.SSHClient(ssh_host, ssh_username, ssh_password)


        '''Set maximum authentication fail count'''

        sshclient.exec_command('cd /tmp; ./csadm Dev=3001@{0} LogonSign=ADMIN,"/tmp/ADMIN.key" SetMaxAuthFails=3'.format(docker_ip))
        sshclient.exec_command('sudo service xroad-signer restart')

        time.sleep(40)
        '''Reload page and wait until additional data is loaded using jQuery'''
        self.driver.refresh()
        self.wait_jquery()

        '''Click "Keys and Certificates" button" '''
        self.log('Click "Keys and Certificates" button"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        self.log('Click on hardware token row')
        self.wait_until_visible(type=By.XPATH, element=keys_and_certificates_table.HARDTOKEN_TABLE_XPATH).click()

        self.log('Log out from hardware token')

        '''Click "LOGOUT"'''
        if self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOGOUT).is_displayed():
            self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOGOUT).click()
            self.wait_jquery()

        '''Click "LOGIN"'''
        self.log('SS_25 1.SS administrator selects to log in to a hardware token.')

        self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOGIN).click()
        self.wait_jquery()

        find_errors_login(self, pin)

        self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_CLOSE_BTN_XPATH).click()
        self.wait_jquery()

        blocked_token = self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOCKED).is_displayed()
        if blocked_token is True:
            unlock_pin(ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password, docker_ip=docker_ip)
        else:
            raise RuntimeError('Token not blocked')

        '''Refresh website'''
        self.driver.refresh()
        self.wait_jquery()
        time.sleep(1)
        self.log('SS_25 4.System verifies that the token is not locked.')

        try:
            element = self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOCKED)
            if element.is_displayed():
                raise RuntimeError('Token is blocked')
        except NoSuchElementException:
            pass
        self.logdata.append('Log into the token')
        whitespace_login(self, pin)
        successful_login(self, pin)
        token_inaccessible(self, pin)

        '''Check audit log'''
        time.sleep(50)
        if ssh_host is not None:
            # Check logs for entries
            self.log('Check the audit log')
            self.log('SS_25 System logs the event “Log in to token” and “Log in to token failed” to the audit log.')

            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

    return backup_conf


def successful_login(self, pin):
    self.log('Log out and log in for testing correct PIN')
    self.wait_jquery()
    '''Click "LOGOUT"'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOGOUT).click()
    self.wait_jquery()

    '''Click "LOGIN"'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOGIN).click()
    self.wait_jquery()

    '''Input area'''
    key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_PIN_LABEL_AREA)
    self.log('SS_25 2.SS administrator enters the PIN code of the token.')

    '''Insert correct PIN'''
    self.input(key_label_input, pin)
    self.wait_jquery()

    '''Click "OK" button'''
    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_OK_BTN_XPATH).click()
    self.wait_jquery()
    self.log('SS_25 6.System verifies that the PIN code is correct and logs in to the token.')

    '''Set "Log in to token" to logdata'''
    self.logdata.append(log_constants.TOKEN_LOG_OUT)

    self.logdata.append(log_constants.SOFTTOKEN_LOGIN_SUCCESS)
    time.sleep(1)
    return self.logdata


def find_errors_login(self, pin):
    error_count = 0
    success_count = 0
    KEY_LABEL_TEXT_AND_RESULTS = [
        [256 * 'S', messages.INPUT_EXCEEDS_255_CHARS.format(keys_and_certificates_table.SOFTTOKEN_PIN_ERROR_PARAMETER),
         None, False],
        ['', messages.MISSING_PARAMETER.format(keys_and_certificates_table.SOFTTOKEN_PIN_ERROR_PARAMETER), None, False],
        [keys_and_certificates_table.SOFTTOKEN_PIN_ERROR_PARAMETER, messages.HARDTOKEN_PIN_INCORRECT_FORMAT, None,
         False],
        [pin[::-1], messages.HARDTOKEN_PIN_INCORRECT, None, False],
        [pin[::-1], messages.HARDTOKEN_PIN_INCORRECT_2TRY, None, False],
        [pin[::-1], messages.HARDTOKEN_PIN_INCORRECT_3TRY, None, False],
        [pin[::-1], messages.HARDTOKEN_PIN_INCORRECT_PIN_LOCKED, None, False], ]

    # Loop through different key label names and expected results
    counter = 1
    for keys in KEY_LABEL_TEXT_AND_RESULTS:

        input_text = keys[0]
        error_message = keys[1]
        error = error_message is not None
        self.log('SS_25 3. System parses the user input')

        '''Input area'''
        key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_PIN_LABEL_AREA)

        '''Inserting PIN from KEY_LABEL_TEXT_AND_RESULTS'''
        self.input(key_label_input, input_text)
        self.wait_jquery()

        '''Click "OK" button'''
        self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_OK_BTN_XPATH).click()
        self.wait_jquery()
        time.sleep(2)
        '''Set "Log in to token failed" to logdata'''
        self.logdata.append(log_constants.SOFTTOKEN_LOGIN_FAILED)

        ui_error = messages.get_error_message(self)

        self.log(
            'SS_24 3a., 4a., 4b., 5b., 6b., 6c., 6d. The process of parsing the user input terminated with an error message. Checking error message: "{0}"'.format(
                ui_error))
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


def whitespace_login(self, pin):
    self.log('Log in with correct PIN that consist whitespaces')
    '''Click "LOGIN"'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_LOGIN).click()
    self.wait_jquery()

    '''Input area'''
    key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_PIN_LABEL_AREA)

    '''Inserting name correct PIN with whitespaces'''
    self.input(key_label_input, '  {0}  '.format(pin))
    self.wait_jquery()

    '''Click "OK" button'''
    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_OK_BTN_XPATH).click()
    self.wait_jquery()

    '''Set "Log in to token" to logdata'''
    self.logdata.append(log_constants.SOFTTOKEN_LOGIN_SUCCESS)
    return self.logdata


def unlock_pin(ssh_host=None, ssh_username=None, ssh_password=None, docker_ip=None):
    sshclient = ssh_client.SSHClient(ssh_host, ssh_username, ssh_password)

    '''Cut connetcion with target host'''
    sshclient.exec_command(
        'cd /tmp; ./csadm Dev=3001@{0} LogonSign=ADMIN,"/tmp/ADMIN.key" ChangeUser=USR_0000,1234'.format(docker_ip))
    sshclient.exec_command('sudo service xroad-signer restart', sudo=True)
    time.sleep(40)


def token_inaccessible(self, pin):
    '''Click "LOGIN"'''
    self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_ERROR_LOGIN).click()
    self.wait_jquery()

    '''Input area'''
    key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_PIN_LABEL_AREA)

    '''Insert correct PIN'''
    self.input(key_label_input, pin)
    self.wait_jquery()

    '''Click "OK" button'''
    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_LOGIN_OK_BTN_XPATH).click()
    self.wait_jquery()
    time.sleep(3)
    self.log('SS_25 4-6a. The login attempt failed (e.g., token is inaccessible).')
    ui_error = messages.get_error_message(self)
    self.is_equal(ui_error, messages.HARDTOKEN_LOGIN_FAILED,
                  msg='Wrong error message, expected: {0}'.format(messages.HARDTOKEN_LOGIN_FAILED))
    '''Set "Log in to token failed" to logdata'''
    self.logdata.append(log_constants.SOFTTOKEN_LOGIN_FAILED)

    return self.logdata
