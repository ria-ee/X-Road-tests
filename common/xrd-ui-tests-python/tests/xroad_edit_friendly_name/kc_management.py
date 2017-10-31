# coding=utf-8
from selenium.webdriver.common.by import By
from helpers import auditchecker
from view_models import sidebar, keys_and_certificates_table, popups, messages, log_constants


def test_edit_conf(case, ssh_host=None, ssh_username=None, ssh_password=None):
    '''
    UC SS_22: Edit the Friendly Name of a Token. Parse users input and save correct Friendly name of Token
    :param case: MainController object
    :param ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param ssh_username: str|None SSH username
    :param ssh_password: str|None SSH password
    :return:
    '''
    self = case

    def backup_conf():

        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
            current_log_lines = log_checker.get_line_count()

        self.log('System parses users input')
        find_errors(self)
        self.log('System parses users whitespace input')
        whitespace_friendly_name(self)
        self.log('Save correct friendly name of token')
        successful_edit(self)

        '''Check audit log'''
        if ssh_host is not None:
            # Check logs for entries
            self.log(
                'UC SS_22 4.System logs the event “Set friendly name to token” to the audit log.')
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

    return backup_conf


def clicking_buttons(self):
    '''Click "Keys and Certificates" button" '''
    self.log('Click "Keys and Certificates" button"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()

    '''Click on "Token: softToken-0" row'''
    self.log('Click on "Token: softToken-0" row')
    self.wait_until_visible(type=By.XPATH, element=keys_and_certificates_table.SOFTTOKEN_TABLE_ROW_XPATH2).click()

    '''Click on "Details" button'''
    self.log('Click on "Details" button')
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DETAILS_BTN_ID).click()
    self.wait_jquery


def successful_edit(self):
    clicking_buttons(self)
    '''Add "Set friendly name to token" to logdata'''
    self.logdata.append(log_constants.KEYS_AND_SERTIFICATES_SET_TOKEN)

    '''Input area'''
    key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_DETAILS_POPUP_KEY_LABEL_AREA_ID)

    '''Inserting name "softToken-0"'''
    self.input(key_label_input, keys_and_certificates_table.SOFTTOKEN_FRIENDLY_NAME)
    '''Click "OK" button'''
    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_DETAILS_POPUP_OK_BTN_XPATH).click()

    return self.logdata


def find_errors(self):
    clicking_buttons(self)

    error_count = 0
    success_count = 0

    KEY_LABEL_TEXT_AND_RESULTS = [
        [256 * 'S', messages.INPUT_EXCEEDS_255_CHARS.format(keys_and_certificates_table.TOKEN_DETAILS_ERROR_PARAMETER),
         None, False],
        ['', messages.TOKEN_DETAILS_MISSING_PARAMETER, None, False]]

    # Loop through different key label names and expected results
    counter = 1

    for keys in KEY_LABEL_TEXT_AND_RESULTS:

        input_text = keys[0]
        error_message = keys[1]
        error = error_message is not None

        '''Input area'''
        key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_DETAILS_POPUP_KEY_LABEL_AREA_ID)

        self.log('UC SS_22 2.System parses the user input')

        '''Inserting names from KEY_LABEL_TEXT_AND_RESULTS'''
        self.input(key_label_input, input_text)
        self.wait_jquery()

        '''Click "OK" button'''
        self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_DETAILS_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        '''Set "Set friendly name to token failed" to logdata'''
        self.logdata.append(log_constants.KEYS_AND_SERTIFICATES_SET_TOKEN_FAILED)

        ui_error = messages.get_error_message(self)

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

    '''Click "Cancel" button'''
    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_DETAILS_POPUP_CANCEL_BTN_XPATH).click()
    return success_count, error_count, self.logdata


def whitespace_friendly_name(self):
    '''Set "Set friendly name to token" to logdata'''
    self.logdata.append(log_constants.KEYS_AND_SERTIFICATES_SET_TOKEN)
    self.log('UC SS_22 1.SS administrator selects to change the friendly name of a security token and changes the name.')

    clicking_buttons(self)

    '''Input area'''
    key_label_input = self.wait_until_visible(type=By.NAME, element=popups.TOKEN_DETAILS_POPUP_KEY_LABEL_AREA_ID)

    text_with_whitespaces = keys_and_certificates_table.SOFTTOKEN_FRIENDLY_NAME_WHITESPACES
    self.input(key_label_input, text_with_whitespaces)

    self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_DETAILS_POPUP_OK_BTN_XPATH).click()

    '''Get the last word from token'''
    without_whitespaces = \
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.SOFTTOKEN_TABLE_ROW_XPATH2).text.split(
            " ")[-1]

    '''Remove whitespaces from test string'''
    without_whitespaces_cntrl = text_with_whitespaces.strip()
    self.log('UC SS_22 3.System saves the changes to the system configuration.')

    '''Verify whitespaces removing'''
    self.is_true(without_whitespaces == without_whitespaces_cntrl,
                 msg='Whitespaces not removed')

    return self.logdata
