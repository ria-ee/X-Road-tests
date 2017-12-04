# coding=utf-8
from selenium.webdriver.common.by import By
from helpers import auditchecker, xroad, ssh_client
from view_models import sidebar, keys_and_certificates_table, popups, messages, log_constants
import time


def test_hardware_key_delete(case, ssh_host=None, ssh_username=None, ssh_password=None):
    self = case

    def deletion_conf():
        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
            current_log_lines = log_checker.get_line_count()

        '''Click "Keys and Certificates" button" '''
        self.log('Click "Keys and Certificates" button"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        '''If token is loged out then log in'''
        if self.driver.find_element_by_xpath(keys_and_certificates_table.HARDTOKEN_ERROR_LOGIN2).is_displayed():
            hardware_token_login(self)

        '''Add key deletion failed message to logdata'''
        self.logdata.append(log_constants.DELETE_KEY_FAILED)

        self.log('Click on softtoken row')
        self.wait_until_visible(type=By.XPATH, element=keys_and_certificates_table.HARDTOKEN_TABLE_XPATH2).click()
        self.wait_jquery()

        '''Add key to token'''
        add_key_hardware_token(self)

        '''Click on key'''
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.KEY_TABLE_ROW_BY_LABEL_XPATH.format(
                                    'delete')).click()

        self.log('Click on "Details" button')
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DETAILS_BTN_ID).click()
        self.wait_jquery
        '''Get key details'''
        token_info = self.wait_until_visible(type=By.XPATH, element=popups.KEY_DETAILS_TOKEN_INFO_XPATH)
        token_info = token_info.text.encode('utf-8').split()
        '''Get key id'''
        token_id = token_info[2]
        '''Click cancel button'''
        self.wait_until_visible(type=By.XPATH, element=popups.KEY_DETAILS_POPUP_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_jquery

        '''Click on key'''
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.KEY_TABLE_ROW_BY_LABEL_XPATH.format(
                                    'delete')).click()

        '''Open connection'''
        sshclient = ssh_client.SSHClient(ssh_host, ssh_username, ssh_password)

        '''Stop docker container'''
        sshclient.exec_command('docker stop cssim410_test', sudo=True)
        '''Kill docker process'''
        sshclient.exec_command('pkill docker-', sudo=True)

        '''Delete key'''
        delete_added_key_label(self)

        self.log('UC SS_37:  4a. Deletion failed')
        '''Get error message'''
        ui_error = messages.get_error_message(self)

        '''Verify error message'''
        self.is_equal(ui_error, messages.HARDTOKEN_KEY_DELETE_FAILED.format(token_id),
                      msg='Wrong error message, expected: {0}'.format(
                          messages.HARDTOKEN_KEY_DELETE_FAILED.format(token_id)))

        '''Click on token'''
        self.wait_until_visible(type=By.XPATH, element=keys_and_certificates_table.HARDTOKEN_TABLE_XPATH2).click()

        '''Start preconfigured docker container'''
        sshclient.exec_command('docker run -p3001:3001 -dt --rm --name cssim410_test cssim410_test', sudo=True)
        '''Restart xroad-signer service'''
        sshclient.exec_command('service xroad-signer restart', sudo=True)
        time.sleep(7)
        '''Reload page'''
        self.reset_page()
        self.wait_jquery()

        '''Click on token'''
        self.wait_until_visible(type=By.XPATH, element=keys_and_certificates_table.HARDTOKEN_TABLE_XPATH2).click()
        '''Add key to token'''
        add_key_hardware_token(self)

        '''Click "Cancel" button on delete confirmation '''
        unconfirm_delete_added_key_label(self)
        '''Delete key'''
        delete_added_key_label(self)
        self.log('SS_37 4. System deletes the key from the token.')
        if self.wait_until_visible(type=By.XPATH, element=keys_and_certificates_table.HARDTOKEN_TABLE_XPATH2).click():
            raise Exception('Token key not deleted')

        '''Add generate key message to logdata'''
        self.logdata.append(log_constants.GENERATE_KEY)
        '''Add delete key message to logdata'''
        self.logdata.append(log_constants.DELETE_KEY)

        '''Check audit log'''
        if ssh_host is not None:
            # Check logs for entries
            self.log('Check the audit log')
            self.log(
                'SS_37 System checks audit log."Delete key from token and configuration", "Delete key from token and configuration failed"')
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

    return deletion_conf


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


def delete_added_key_label(self):
    self.log('Delete added key')
    self.wait_jquery()
    self.log('SS_37 1.SS administrator selects to delete a key."')
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
    self.log('SS_37 2.System prompts for confirmation.')
    self.log('SS_37 3.SS administrator confirms.')

    self.log('Click on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()
    time.sleep(1)
    self.log('Added key is deleted')


def unconfirm_delete_added_key_label(self):
    self.log('Delete added key')
    self.wait_jquery()
    self.log('SS_37 3a. SS administrator terminates the use case."')
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
    self.log('SS_37 2.System prompts for confirmation.')
    self.log('SS_37 3.SS administrator cancels confirmation.')
    self.log('Click on "Cancel" button')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()


def add_key_hardware_token(self):
    self.log('Click on "Generate key" button')
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.GENERATEKEY_BTN_ID).click()

    self.log(
        'Insert delete to "LABEL" area')
    key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
    self.input(key_label_input, 'delete')

    '''Save the key data'''
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
