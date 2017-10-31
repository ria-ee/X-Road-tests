from selenium.webdriver.common.by import By
import re
from helpers import auditchecker
from view_models import sidebar as sidebar_constants, keys_and_certificates_table as keyscertificates_constants, \
    popups, log_constants, messages


def test_view_list_of_tokens_keys_certs(host_cert_name):
    """
     UC SS_19: View the List of Tokens, Keys and Certificates
    """
    def test_case(self):
        def verify_cert_data_display(cert_data, key_type=None):
            if key_type == '(auth)':
                cert_name = host_cert_name
                displayed_cert_name = cert_data[0]
                displayed_serial_number = cert_data[1]
                displayed_ocsp_response = cert_data[2]
                displayed_expire_date = cert_data[3]
                displayed_status = cert_data[4]

                expire_date = displayed_expire_date.split('-')
                expire_date_year = expire_date[0]
                expire_date_month = expire_date[1]
                expire_date_day = expire_date[2]
            elif key_type == '(sign)':
                cert_name = host_cert_name
                displayed_cert_name = cert_data[0]
                displayed_serial_number = cert_data[1]
                displayed_member_class = cert_data[2]
                displayed_colon = cert_data[3]
                displeyed_member_code = cert_data[4]
                displayed_ocsp_response = cert_data[5]
                displayed_expire_date = cert_data[6]
                displayed_status = cert_data[7]

                expire_date = displayed_expire_date.split('-')
                expire_date_year = expire_date[0]
                expire_date_month = expire_date[1]
                expire_date_day = expire_date[2]

            '''Verify that certificate name is displayed'''
            cert_name_displayed = False
            if cert_name == displayed_cert_name:
                cert_name_displayed = True
            assert cert_name_displayed is True

            '''Verify that certificate serial number is displayed'''
            serial_number_displayed = False
            if type(int(displayed_serial_number)) == int:
                serial_number_displayed = True
            assert serial_number_displayed is True

            '''Verify that certificate serial number is displayed'''
            serial_number_displayed = False
            if type(int(displayed_serial_number)) == int:
                serial_number_displayed = True
            assert serial_number_displayed is True

            '''Verify that OCSP response is displayed'''
            ocsp_response_displayed = False
            if type(displayed_ocsp_response) == str and len(displayed_ocsp_response) > 0:
                ocsp_response_displayed = True
            assert ocsp_response_displayed is True

            '''Verify that expire date is displayed'''
            expire_date_displayed = False
            if type(int(expire_date_year) == int) and int(expire_date_year) > 999 \
                    and type(int(expire_date_month) == int) and int(expire_date_month) > 0 \
                    and type(int(expire_date_day) == int) and int(expire_date_day) > 0 \
                    and len(displayed_expire_date) == 10:
                expire_date_displayed = True
            assert expire_date_displayed is True

            '''Verify that status is displayed'''
            status_displayed = False
            if displayed_status == 'registered':
                status_displayed = True
            assert status_displayed is True

            if key_type == '(auth)':
                self.log('Certificate name: {0}, Serial number: {1}, OCSP response: {2}, Expires: {3}, Status: {4}'.
                         format(displayed_cert_name, displayed_serial_number, displayed_ocsp_response,
                                displayed_expire_date, displayed_status))

            elif key_type == '(sign)':
                '''Verify that the identifier of the member is displayed in the format - member class : member code'''
                member_displayed = False
                if len(displayed_member_class) > 0 and displayed_colon == ':' and len(displeyed_member_code) > 0:
                    member_displayed = True
                assert member_displayed is True
                self.log('Certificate name: {0}, Serial number: {1}, Member: {2} {3} {4}, OCSP response: {5}, '
                         'Expires: {6}, Status: {7}'.
                         format(displayed_cert_name, displayed_serial_number, displayed_member_class,
                                displayed_colon, displeyed_member_code, displayed_ocsp_response,
                                displayed_expire_date, displayed_status))

        key_type_sign = '(sign)'
        key_type_auth = '(auth)'

        '''UC SS_19 step 1. SS administrator selects to view the list of tokens, keys and certificates'''
        self.log('UC SS_19 step 1. SS administrator selects to view the list of tokens, keys and certificates, '
                 'by clicking on "Keys and certificates" tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        '''UC SS_19 step 2. System displays the list of tokens, keys and certificates'''
        self.log('''UC SS_19 step 2. System displays the list of tokens, keys and certificates''')

        keys_and_certificates_table = self.wait_until_visible(type=By.ID,
                                                              element=keyscertificates_constants.
                                                              KEYS_AND_CERTIFICATES_TABLE_ID,
                                                              multiple=True)

        keys_and_certificates_table_rows = keys_and_certificates_table[0].text.encode('utf-8').split('\n')

        for row in range(len(keys_and_certificates_table_rows)):
            splited_row = keys_and_certificates_table_rows[row].split()

            if splited_row[0] == 'LOGOUT':
                pass

            elif splited_row[0] == 'Token:':
                '''Verify that friendly name is displayed for token'''
                self.log('''Verify that friendly name is displayed for token.''')
                displayed_token_name = splited_row[1]
                token_name_displayed = False
                if len(displayed_token_name) > 0:
                    token_name_displayed = True
                assert token_name_displayed is True
                self.log('Token name - {0} - is displayed'.format(displayed_token_name))

            elif splited_row[0] == 'Key:':
                '''Verify that friendly name and type of the key are displayed for key'''
                self.log('''Verify that friendly name and type of the key are displayed for  key.''')

                key_data = splited_row
                key_name_displayed = False
                type_of_key_displayed = False

                if type(key_data[1]) == str and len(key_data[1]) > 0:  # key_data[1] is key label name
                    key_name_displayed = True
                if key_data[-1] == key_type_sign or key_data[-1] == key_type_auth or key_data[-1] == '(?)':  # key type
                    type_of_key_displayed = True
                assert key_name_displayed is True and type_of_key_displayed is True
                self.log('''Key name - {0} - and type of key - {1} - are displayed.'''.format(key_data[1],
                                                                                              key_data[-1]))
            else:
                cert_data = splited_row
                certificate_key_type = keys_and_certificates_table_rows[row - 1].split()
                certificate_key_type = certificate_key_type[-1]

                auth_request = False
                if certificate_key_type == key_type_auth and len(cert_data) == 1:
                    '''Verify that only - Request - is displayed for certificate, if key type for requested certificate 
                    is (auth).'''
                    self.log('Verify that only - Request - is displayed for certificate, if key type for requested '
                             'certificate is (auth).')
                    auth_request = True
                    self.log('''Certificate name - {0} - is displayed.'''.format(cert_data[0]))
                    assert auth_request is True

                elif certificate_key_type == key_type_auth and len(cert_data) > 1:
                    '''Verify that  - Certificate, OCSP response, Expires, Status - are displayed for certificate, if 
                    key type for certificate is (auth).'''
                    self.log('Verify that  - Certificate, OCSP response, Expires, Status - are displayed '
                             'for certificate, if key type for certificate is (auth).')

                    verify_cert_data_display(cert_data, key_type=key_type_auth)

                elif certificate_key_type == key_type_sign and len(cert_data) == 4:
                    '''Verify that  - Request, Member - is displayed for certificate, if key type for requested 
                    certificate is (sign).'''
                    self.log('Verify that  - Request, Member - is displayed for certificate, if key type for requested '
                             'certificate is (sign).')
                    displayed_cert_name = cert_data[0]
                    displayed_member_class = cert_data[1]
                    displayed_colon = cert_data[2]
                    displeyed_member_code = cert_data[3]

                    '''Verify that certificate name - Request - is displayed'''
                    cert_name_displayed = False
                    if displayed_cert_name == 'Request':
                        cert_name_displayed = True
                    assert cert_name_displayed is True

                    '''Verify that the identifier of the member is displayed in the format - 
                    member class : member code'''
                    member_displayed = False
                    if len(displayed_member_class) > 0 and displayed_colon == ':' and len(displeyed_member_code) > 0:
                        member_displayed = True
                    assert member_displayed is True
                    self.log('Certificate name: {0}, Member: {1} {2} {3}'.
                             format(displayed_cert_name, displayed_member_class, displayed_colon,
                                    displeyed_member_code))

                elif certificate_key_type == key_type_sign and len(cert_data) > 4:
                    '''Verify that  - Certificate, Member, OCSP response, Expires, Status - are displayed for 
                    certificate, if key type for certificate is (sign).'''
                    self.log('Verify that  - Certificate, Member, OCSP response, Expires, Status - are displayed for '
                             'certificate, if key type for certificate is (sign).')
                    verify_cert_data_display(cert_data, key_type_sign)

    return test_case


def test_view_token_details():
    """
    UC SS_20: View the Details of a Token
    """
    def test_case(self):
        '''SS administrator selects to view the list of tokens'''
        self.log('SS administrator selects to view the list of tokens, keys and certificates, '
                 'by clicking on "Keys and certificates" tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        '''System displays the tokens'''
        self.log('''System displays the tokens''')
        tokens = self.wait_until_visible(type=By.CLASS_NAME, element=keyscertificates_constants.TOKEN_NAMES_CLASS,
                                         multiple=True)

        for token in tokens:
            '''SS_20 step 1. SS administrator selects to view the details of a token.'''
            self.log('''SS_20 step 1. SS administrator selects to view the details of a token.''')
            self.double_click(token)
            self.wait_jquery()

            '''SS_20 step 2. System displays the details of the token'''
            self.log('''SS_20 step 2. System displays the details of the token''')

            '''SS_20 step 2.1. System displays the friendly name of the token'''
            token_name = self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_DETAILS_FRIENDLY_NAME)
            token_name = token_name.get_attribute('value')
            token_name_displayed = False
            if type(str(token_name)) == str and len(token_name) > 0:
                token_name_displayed = True
            assert token_name_displayed is True
            self.log('''SS_20 step 2.1. System displays the friendly name of the token - {0}'''.format(token_name))

            token_info = self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_DETAILS_TOKEN_INFO_XPATH)
            token_info = token_info.text.encode('utf-8').split()

            '''SS_20 step 2.2. the identifier of the token'''
            token_id = int(token_info[2])
            token_id_type = type(token_id)
            assert token_id_type is int
            self.log('''SS_20 step 2.2. System displays the identifier of the token - {0}'''.format(token_id))

            '''SS_20 step 2.3. the technical token status information'''
            token_type = token_info[-1]
            assert token_type is 'Software' or 'Hardware'
            self.log('''SS_20 step 2.3. System displays the technical token status information - {0}'''.
                     format(token_type))

            '''Close token details by clicking on 'Cancel' button'''
            self.log('''Close token details by clicking on 'Cancel' button''')
            self.wait_until_visible(type=By.XPATH, element=popups.TOKEN_DETAILS_POPUP_POPUP_CANCEL_BTN_XPATH)

    return test_case


def test_view_key_details():
    """
    UC SS_21: View the Details of a Key
    """
    def test_case(self):
        '''SS administrator selects to view the list of keys'''
        self.log('SS administrator selects to view the list of keys, '
                 'by clicking on "Keys and certificates" tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        '''System displays the keys'''
        self.log('''System displays the keys''')

        keys = self.wait_until_visible(type=By.CLASS_NAME, element='key-usage', multiple=True)

        for key in keys:
            '''SS_21 step 1. SS administrator selects to view the details of a key.'''
            self.log('''SS_21 step 1. SS administrator selects to view the details of a key.''')
            self.double_click(key)
            self.wait_jquery()

            '''SS_21 step 2. System displays the details of the key'''
            self.log('''SS_21 step 2. System displays the details of the key''')

            '''SS_21 step 2.1. System displays the friendly name of the key'''
            key_name = self.wait_until_visible(type=By.XPATH, element=popups.KEY_DETAILS_POPUP_FRIENDLY_NAME)
            key_name = key_name.get_attribute('value')
            key_name_displayed = False
            if type(str(key_name)) == str and len(key_name) > 0:
                key_name_displayed = True
            assert key_name_displayed is True
            self.log('''SS_21 step 2.1. System displays the friendly name of the key - {0}'''.format(key_name))

            key_info = self.wait_until_visible(type=By.XPATH, element=popups.KEY_DETAILS_TOKEN_INFO_XPATH)
            key_info = key_info.text.encode('utf-8').split()

            '''SS_21 step 2.2. System displays the identifier of the key'''
            key_id = key_info[2]
            reg_ex = r'^[A-Z0-9]*'
            rex_ex_compare = re.findall(reg_ex, key_id)
            key_id_displayed = False
            if len(key_id) == 40 and key_id == rex_ex_compare[0]:
                key_id_displayed = True
            assert key_id_displayed is True
            self.log('''SS_21 step 2.2. System displays the identifier of the key - {0}'''.format(key_id))

            '''SS_21 step 2.3. System displays the label of the key'''
            key_label = key_info[4]
            key_label_displayed = False
            if type(str(key_label)) == str and len(key_label) > 0:
                key_label_displayed = True
            assert key_label_displayed is True
            self.log('''SS_21 step 2.3. System displays the label of the key - {0}'''.format(key_label))

            '''SS_21 step 2.4. System displays the information, whether the key is read-only or not'''
            key_read_only = key_info[-1]
            assert key_read_only is 'true' or 'false'
            self.log('''SS_21 step 2.4. System displays the information, whether the key is read-only or not - {0}'''.
                     format(key_read_only))

            '''Close key details by clicking on 'Cancel' button'''
            self.log('''Close key details by clicking on 'Cancel' button''')
            self.wait_until_visible(type=By.XPATH, element=popups.KEY_DETAILS_POPUP_POPUP_CANCEL_BTN_XPATH).click()

    return test_case


def test_change_key_name(ssh_host, ssh_user, ssh_pass):
    """
    SS_23: Edit the Friendly Name of a Key
    :param ssh_host: str - ssh hostname
    :param ssh_user: str - ssh username
    :param ssh_pass: str - ssh password
    :return: None
    """
    def test_case(self):
        key_name = "test_certificate_keys"

        '''Key names and results = [entered string, are there errors(True/False), expected error message, 
        parameter for error message, are there whitespaces]'''
        key_name_and_results = [[256 * 'S', True, "Parameter '{0}' input exceeds 255 characters", 'friendly_name',
                                 False],
                                ['   ' + key_name + '   ', False, None, None, True],
                                ['z', False, None, None, False],
                                [255 * 'S', False, None, None, False],
                                ['', True, "Missing parameter: {0}", 'friendly_name', False],
                                [key_name, False, None, None, False]]

        '''Open the keys and certificates tab'''
        self.log('Open keys and certificates tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        '''Generate key from softtoken'''
        self.log('Generate key from softtoken')
        add_key_label(self, key_name)

        '''Generate CSR'''
        self.log('Generate CSR')
        add_csr_to_key(self)

        self.wait_jquery()

        '''SS_23 2a.3. SS administrator selects to reinsert the friendly name. Use case continues form step 2.'''
        self.log('SS_23 2a.3. SS administrator selects to reinsert the friendly name. Use case continues form step 2.')


        for key_name in key_name_and_results:

            input_text = key_name[0]
            error = key_name[1]
            error_message = key_name[2]
            error_message_label = key_name[3]
            whitespaces = key_name[4]

            '''Click on DETAILS button'''
            self.log('Click on DETAILS button')
            self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DETAILS_BTN_ID).click()

            '''SS_23 1. SS administrator selects to change the friendly name of a key and changes the name'''
            self.log('SS_23 1. SS administrator selects to change the friendly name of a key and changes the name')
            key_name_field = self.wait_until_visible(type=By.XPATH, element=popups.KEY_DETAILS_POPUP_FRIENDLY_NAME)
            key_name_field.click()
            self.input(key_name_field, input_text)
            self.log('SS administrator changes the friendly name to (string length is - {1})- {0}'.
                     format(input_text, len(input_text)))

            if ssh_host is not None:
                log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_user, password=ssh_pass)
                current_log_lines = log_checker.get_line_count()

            '''Click on OK button'''
            self.log('Click on DETAILS button')
            self.wait_until_visible(type=By.XPATH, element=popups.KEY_DETAILS_POPUP_POPUP_OK_BTN_XPATH).click()

            '''SS_23 2. System parses the user input'''
            self.log('SS_23 2. System parses the user input')
            check_error_message(self, error, error_message, error_message_label)

            if error:
                '''SS_23 2a.2 System logs the event 'Set friendly name to key failed' to the audit log.'''
                self.log('''SS_23 2a.2 System logs the event 'Set friendly name to key failed' to the audit log.''')
                if ssh_host is not None:
                    logs_found = log_checker.check_log([log_constants.CHANGE_FRIENLY_NAME_FAILED],
                                                       from_line=current_log_lines + 1)
                    self.is_true(logs_found, msg="Set friendly name to key failed")
                '''CSS_23 2a.3a SS administrator selects to terminate the use case.'''
                self.log('CSS_23 2a.3a SS administrator selects to terminate the use case.')
                self.wait_until_visible(type=By.XPATH, element=popups.KEY_DETAILS_POPUP_POPUP_CANCEL_BTN_XPATH).click()
            else:
                '''SS_23 4. System logs the event 'Set friendly name to key' to the audit log.'''
                self.log('''SS_23 4. System logs the event 'Set friendly name to key' to the audit log.''')
                if ssh_host is not None:
                    logs_found = log_checker.check_log(log_constants.CHANGE_FRIENDLY_NAME,
                                                       from_line=current_log_lines + 1)
                    self.is_true(logs_found, msg='Set friendly name to key')

                '''SS_23 3. System saves the changes to the system configuration.'''
                self.log('''SS_23 3. System saves the changes to the system configuration.''')
                key_label_name = self.wait_until_visible(type=By.XPATH,
                                                         element=keyscertificates_constants.
                                                         get_text(input_text.strip()))
                key_label_name = key_label_name.text

                if whitespaces:
                    find_text_with_whitespaces(self, input_text, key_label_name)
                else:
                    assert input_text in key_label_name
            self.wait_jquery()

        '''Delete the added key label'''
        self.log('''Delete the added key label''')
        delete_added_key_label(self)

    return test_case


def add_key_label(self, key_label):
    """
    Add central key label
    :param self: MainController object
    :param key_label: str - key label
    :return:
    """
    ''' Generate key from softtoken '''
    self.wait_jquery()
    self.log('Click on softtoken row')
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_XPATH).click()

    self.wait_jquery()
    self.log('Click on softtoken row')
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_XPATH).click()
    self.log('Click on "Generate key" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATEKEY_BTN_ID).click()

    '''Enter key label'''
    self.log('Insert "' + key_label + '" to "LABEL" area')
    key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
    self.input(key_label_input, key_label)
    self.wait_jquery()
    '''Save the key data'''
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()


def add_csr_to_key(self):
    """
    Add csr to key
    :param self: MainController object
    :return: None
    """
    self.log('Click on "GENERATE CSR" button')
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATECSR_BTN_ID).click()
    self.log('Choose Verify Usage:')
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.get_csr_data(
        keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_USAGE_DROPDOWN_ID, 1)).click()
    self.log('Choose Client:')
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.get_csr_data(
        keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CLIENT_DROPDOWN_ID, 1)).click()
    self.log('Choose Certification Service:')
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.get_csr_data(
        keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID, 2)).click()
    self.log('Choose CSR Format:')
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.get_csr_data(
        keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID, 1)).click()
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH).click()
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH).click()


def check_error_message(self, error, error_message, error_message_label):
    """
    Function Check for the error messages
    :param self: MainController object
    :param error: bool - Must there be a error message, True if there is and False if not
    :param error_message: str - Expected error message
    :param error_message_label: str - label for a expected error message
    :return:
    """
    if error:
        '''SS_23 2a.1. System displays the termination message from the parsing process.'''
        self.log('SS_23 2a.1. System displays the termination message from the parsing process.')
        self.log('Get the error message')
        self.wait_jquery()
        get_error_message = messages.get_error_message(self)
        self.log('Found error message - ' + get_error_message)
        self.log('Expected error message  - ' + error_message.format(error_message_label))

        self.log('Compare error message to the expected error message')
        assert get_error_message in error_message.format(error_message_label)

        self.log('Close the error message')
        messages.close_error_messages(self)
    else:
        '''Verify that there is not error messages'''
        self.log('Verify that there is not error messages')
        get_error_message = messages.get_error_message(self)
        if get_error_message is None:
            error = False
        else:
            error = True
        assert error is False


def find_text_with_whitespaces(self, added_text, expected_text):
    """
    Verifies, that there is not inputs with whitespaces
    :param self: MainController object
    :param added_text: str - added text
    :param expected_text: str - expected text
    :return: None
    """
    try:
        ''' Compare added text with whitespaces and displayed text'''
        self.log('Compare added text with whitespaces and displayed text')
        self.log("'" + added_text + "' != '" + expected_text + "'")
        assert added_text in expected_text
        whitespace = True
    except:
        '''Compare added text without whitespaces and displayed text'''
        self.log('Compare added text without whitespaces and displayed text')
        self.log("'" + added_text.strip() + "' == '" + expected_text + "'")
        assert added_text.strip() in expected_text
        whitespace = False
    assert whitespace is False


def delete_added_key_label(self):
    """
    Delete the key row from the list.
    :param self: MainController object
    :return: None
    """
    self.log('Delete added key')
    self.wait_jquery()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()
    self.log('Click on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()
    self.log('Added key is deleted')
