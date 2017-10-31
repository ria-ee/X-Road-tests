# coding=utf-8
from view_models import popups, messages, sidebar, certification_services, log_constants, timestamp_services
from selenium.webdriver.common.by import By
import re
import time
from helpers import xroad, auditchecker


def select_ts(self, ts_name):
    '''
    :param self: MainController object
    :param ts_name: TS display name
    :return:
    '''

    # Click on Timestamping Services
    self.log('UC TRUST_15 1.CS administrator selects to view approved timestamping services.: {0}'.format(ts_name))
    self.wait_until_visible(self.by_css(sidebar.TIMESTAMPING_SERVICES_CSS)).click()
    self.wait_jquery()

    # Activate timestamp services - make one click on it.
    self.log(
        'UC TRUST_15 2.The value of the subject common name (CN) element from the TSA certificate is displayed as the name of the timestamping service')
    self.wait_until_visible(element=certification_services.ts_get_ca_by_td_text(ts_name), type=By.XPATH).click()
    self.wait_jquery()


def verify_ts(self, ts_name):
    '''
    Verifies valid dates with regex (format 0000-00-00 00:00:00) and enabled Add, Delete, Edit buttons
    :param self: MainController object
    :return: None
    '''
    cert_name = self.by_xpath(timestamp_services.SERTIFICATE_NAME).text

    self.log('UC TRUST_15 2."Valid sertificate name {0}'.format(cert_name))

    self.is_true(cert_name == ts_name,
                 msg='Sertificate has wrong name')

    # Get Valid from time
    from_date = self.by_xpath(timestamp_services.SERTIFICATE_VALID_FROM).text

    # Get Valid to time
    to_date = self.by_xpath(timestamp_services.SERTIFICATE_VALID_TO).text

    # Date verification
    from_date_match = re.match(timestamp_services.DATE_REGEX, from_date)
    to_date_match = re.match(timestamp_services.DATE_REGEX, to_date)

    self.log('UC TRUST_15 2."Valid From" verification {0}'.format(from_date))

    self.is_true(from_date_match,
                 msg='From date in wrong format')

    self.log('UC TRUST_15 2."Valid To" verification {0}'.format(from_date))

    self.is_true(to_date_match,
                 msg='To date in wrong format')

    # Locate visible "Add" button
    self.log('UC TRUST_15 2."Add button verification"')

    ts_add_btn = self.wait_until_visible(self.by_id(certification_services.TSADD_BTN_ID)).is_enabled()
    self.is_true(ts_add_btn,
                 msg='Add button not enabled')

    self.log('UC TRUST_15 2."Delete button verification"')

    # Locate visible "Delete" button
    ts_delete_btn = self.wait_until_visible(self.by_id(certification_services.TSDELETE_BTN_ID)).is_enabled()
    self.is_true(ts_delete_btn,
                 msg='Delete button not enabled')

    self.log('UC TRUST_15 2."Edit button verification"')
    # Locate visible "Edit" button
    ts_edit_btn = self.wait_until_visible(self.by_id(certification_services.TSEDIT_BTN_ID)).is_enabled()
    self.is_true(ts_edit_btn,
                 msg='Edit button not enabled')


def click_ts(self):
    '''
    Selects on row and verifies View certificate button
    :param self: MainController object
    :return: None
    '''

    # Clicks on TS sertificate
    self.by_id(certification_services.TSEDIT_BTN_ID).click()

    view_certificate_btn = self.wait_until_visible(self.by_id(certification_services.VIEW_CERTIFICATE)).is_enabled()

    self.log('UC TRUST_15 2."View sertificate" button verification"')
    self.is_true(view_certificate_btn,
                 msg='View certificate button not found')


def test_view_approved_ts(case, ts_name):
    '''
    :param case: MainController object
    :param ts_name: str - TS display name (hostname)
    :return:
    '''
    self = case

    def view_ts():
        # UC TRUST_15: View Approved Timestamping Services
        self.log('UC TRUST_15 View Approved Timestamping Services: {0}'.format(ts_name))

        # Open "Timestamping services"
        select_ts(self, ts_name)

        # Verify "Timestaming services" displayed information
        verify_ts(self, ts_name)

        # Verify View certificate button verification
        click_ts(self)

    return view_ts


def test_add_ts(case, ts_url, ts_certificate, invalid_ts_certificate=None, certificate_classpath=None, cs_ssh_host=None,
                cs_ssh_user=None, cs_ssh_pass=None, ts_name=None, test_name=None):
    '''
    UC TRUST_16 main test method. Tries to add a TS and check logs if cs_ssh_host is set.
    :param case: MainController object
    :param ts_url: str - correct TS url to add
    :param ts_certificate: str - pathname of the correct TS certificate to upload
    :param invalid_ts_certificate: str - pathname of the invalid certificate to upload
    :param certificate_classpath: str - TS certificate profile class
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - TS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - TS SSH password, needed if cs_ssh_host is set
    :param ts_name: str - TS display name (hostname)
    :param test_name: str - name of the test (to distinguish add or edit test)
    :return:
    '''
    self = case

    def add_ca():
        self.logdata = []

        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()

        # UC TRUST_16: Add an Approved Timestamping Service
        self.log('UC TRUST_16: Add an Approved Timestamping Service')

        # Open "Timestamping services"
        self.wait_until_visible(self.by_css(sidebar.TIMESTAMPING_SERVICES_CSS)).click()
        self.wait_jquery()

        self.log('UC TRUST_16: 1. CS administrator selects to add an approved timestamping service.')

        # Click "Add"
        self.by_id(certification_services.TSADD_BTN_ID).click()
        self.wait_jquery()

        self.log('UC TRUST_16: 2. CS administrator selects to add an approved timestamping service.')
        # Add Url
        self.by_id(certification_services.TIMESTAMP_SERVICES_URL_ID).send_keys(ts_url)
        self.wait_jquery()

        self.log('UC TRUST_16: 3. CS administrator selects and uploads the TSA certificate file from the local file system.')
        # Add valid sertificate
        add_first_certifcate(self, ts_certificate)
        # Click "Add" for trying to add invalid sertificates
        self.by_id(certification_services.TSADD_BTN_ID).click()
        self.wait_jquery()

        # Configure TS certificates
        configure_ts_certificate(self, certificate_filename=ts_certificate,
                                 invalid_certificate_filename=invalid_ts_certificate)

        # Configure other TS settings
        configure_ts(self, check_errors=True,
                     log_success=log_constants.ADD_CA, log_fail=log_constants.ADD_TS_FAILED,
                     save_button_id=certification_services.SUBMIT_TS_CERT_BTN_ID, ts_url=ts_url, test_name=test_name)

        if cs_ssh_host is not None:
            # Check logs for entries
            self.log('TRUST_16 5a, 6a, 7a - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

    return add_ca


def test_edit_ts(case, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None,
                 ts_url=None, ts_name=None, test_name=None):
    '''
    :param case: MainController object
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :param ca_name: str - CA display name (hostname)
    :param certificate_classpath: str - CA certificate profile class
    :param ts_url: str - correct TS url to add
    :param ts_name: str - TS display name (hostname)
    :param test_name: str - name of the test (to distinguish add or edit test)
    :return:
    '''
    self = case

    def edit_ca():
        self.logdata = []

        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()
        self.log(
        'UC TRUST_17 Open Timestaming services')

        # Open "Timestamping services"
        select_ts(self, ts_name)

        self.log('UC TRUST_17 1.CS administrator selects to edit the URL of a timestamping server.')
        # Clicks on TS row
        click_ts(self)
        self.wait_jquery()


        self.log(
        'UC TRUST_17 Parse user input')

        # Configure TS certificates
        configure_ts(self, check_errors=True,
                     log_success=log_constants.ADD_CA, log_fail=log_constants.ADD_TS_FAILED,
                     save_button_id=certification_services.SUBMIT_TS_CERT_BTN_ID, ts_url=ts_url, test_name=test_name)

        # Clears URL value
        self.by_id(certification_services.TIMESTAMP_SERVICES_URL_ID).clear()
        self.wait_jquery()

        # Save invalid URL
        test_url = '   {0}   '.format(timestamp_services.TEST_URL)

        # Insert invalid URL
        self.by_id(certification_services.TIMESTAMP_SERVICES_URL_ID).send_keys(test_url)

        # Click OK button
        self.by_id(certification_services.SUBMIT_TS_CERT_BTN_ID).click()
        self.wait_jquery()

        # Open "Timestamping services"
        select_ts(self, ts_name)

        # Clicks on TS row
        click_ts(self)
        self.wait_jquery()

        element = self.by_id(certification_services.TIMESTAMP_SERVICES_URL_ID).text
        self.wait_jquery()

        cert_name = self.wait_until_visible(type=By.ID, element='tsp_url').get_attribute('value')
        input_text_stripped = cert_name.strip(' ')

        # Compare inserted URL
        self.is_true(cert_name == (timestamp_services.TEST_URL),
                     msg='Sertificate has wrong name')

        # Clear URL field
        self.by_id(certification_services.TIMESTAMP_SERVICES_URL_ID).clear()

        # Send valid URL
        self.by_id(certification_services.TIMESTAMP_SERVICES_URL_ID).send_keys(ts_url)

        # Save valid URL
        self.by_id(certification_services.SUBMIT_TS_CERT_BTN_ID).click()
        self.wait_jquery()

        # Open TS
        select_ts(self, ts_name)

        # Click on TS
        click_ts(self)

        # Save URL text
        cert_name = self.wait_until_visible(type=By.ID, element='tsp_url').get_attribute('value')

        self.logdata.append(log_constants.EDIT_TS)

        self.log(
        'UC TRUST_17 Compares and verifies new correct URL')
        # Compare URL
        self.is_true(cert_name == (ts_url),
                     msg='Sertificate has wrong name')

        if cs_ssh_host is not None:
            # Check logs for entries
            self.log('System logs the event “Edit timestamping service” to the audit log.')
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))


    return edit_ca


def add_first_certifcate(self, ts_certificate, close_errors=False):
    '''
    :param self: MainController object
    :param ts_certificate: str - pathname of the certificate to upload
    :param close_errors: bool - close error/warning messages if any are displayed
    :return:
    '''

    set_ts_certificate(self, ts_certificate, close_errors=False)

    # Verify Certificate import successful message
    confirmation_message = messages.get_notice_message(self)
    self.is_equal(confirmation_message, messages.CERTIFICATE_IMPORT_SUCCESSFUL,
                  msg='Expected message "{0}", got "{1}"'.format(messages.CERTIFICATE_IMPORT_SUCCESSFUL,
                                                                 confirmation_message))
    # Click on OK button to save certificate
    self.wait_until_visible(type=By.ID, element=certification_services.SUBMIT_TS_CERT_BTN_ID).click()

    # UC TRUST_16_4 - check for correct confirmation message
    self.log(
        'UC TRUST_16 4 -System verifies that the uploaded file is in DER or PEM format and displays the message “Certificate imported successfully”.')

    self.logdata.append(log_constants.ADD_TS)
    self.wait_jquery()

    # Get error messages if any
    console_output = messages.get_console_output(self)  # Console message (displayed if WSDL validator gives a warning)
    warning_message = messages.get_warning_message(self)  # Warning message
    error_message = messages.get_error_message(self)  # Error message (anywhere)

    if console_output is not None:
        popups.close_console_output_dialog(self)

    # Close all error messages
    if close_errors:
        messages.close_error_messages(self)
    return warning_message, error_message, console_output


def set_ts_certificate(self, ts_certificate, close_errors=False):
    self.log('Setting TS certificate: {0}'.format(ts_certificate))

    # Get the "Import certificate" button.
    import_cert_btn = self.wait_until_visible(type=By.ID,
                                              element=certification_services.IMPORT_TS_CERT_BTN_ID)
    # Set TS certificate
    xroad.fill_upload_input(self, import_cert_btn, ts_certificate)
    # Give some time for JS to react to file input being changed.
    time.sleep(0.5)
    # If an ajax query is initiated, wait for it to finish.
    self.wait_jquery()

    # Get error messages if any
    console_output = messages.get_console_output(self)  # Console message (displayed if WSDL validator gives a warning)
    warning_message = messages.get_warning_message(self)  # Warning message
    error_message = messages.get_error_message(self)  # Error message (anywhere)

    if console_output is not None:
        popups.close_console_output_dialog(self)

    # Close all error messages
    if close_errors:
        messages.close_error_messages(self)

    return warning_message, error_message, console_output


def set_invalid_ts_certificate(self, ts_certificate):
    warning, error, console = set_ts_certificate(self, ts_certificate)
    # Check if an error was shown and if the error was the correct one.
    self.is_not_none(error, msg='Set invalid TS certificate: no error shown'.format(ts_certificate))
    self.is_equal(error, messages.WRONG_FORMAT_TS_CERTIFICATE,
                  msg='Set invalid TS certificate: wrong error shown : {0}'.format(error))

    # Close all errors
    messages.close_error_messages(self)


def configure_ts_certificate(self, certificate_filename=None, invalid_certificate_filename=None):
    # UC TRUST_16 3 - setting valid TS certificate
    self.log('TRUST_16 3 - setting valid TS certificate')
    set_ts_certificate(self, certificate_filename)
    # If invalid_certificate_filename is set, try to upload and check for errors.
    if invalid_certificate_filename is not None:
        time.sleep(4)
        # UC TRUST_16 4a - set invalid TS certificate
        self.log('TRUST_16 4a - setting invalid TS certificate')
        set_invalid_ts_certificate(self, invalid_certificate_filename)

    time.sleep(4)
    # UC TRUST_16 4b - check for correct confirmation message
    set_ts_certificate(self, certificate_filename)
    self.log('TRUST_16 4b - check for correct confirmation message')

    # Get the confirmation message and check if it was the one we were looking for.
    confirmation_message = messages.get_notice_message(self)
    self.is_equal(confirmation_message, messages.CERTIFICATE_IMPORT_SUCCESSFUL,
                  msg='Expected message "{0}", got "{1}"'.format(messages.CERTIFICATE_IMPORT_SUCCESSFUL,
                                                                 confirmation_message))


def configure_ts(self, certificate_classpath=None, check_errors=False, log_success=None, log_fail=None,
                 save_button_id=None, ts_url=None,
                 test_name=None):
    '''

    :param self: MainController object
    :param certificate_classpath: str - CA certificate profile class
    :param check_errors: bool - True to check for error scenarios, False otherwise
    :param ts_url: str - correct TS url to add
    :param ts_name: str - TS display name (hostname)
    :return:

    '''
    # Check user input parsing if instructed so

    if check_errors:
        # Parse user input UC TRUST_19,  UC_TRUST_16 (4a, 5a, 6a, 7a), UC_TRUST_17 (3a, 4a)
        self.log(
            'Parse user input UC TRUST_19,  UC_TRUST_16 (4a, 5a, 6a, 7a), UC_TRUST_17 (3a, 4a)')
        self.log('UC_TRUST_17 3a. The parsing of the user input terminated with an error message.')
        self.log('UC_TRUST_17 4a .The URL is malformed.')

        # Using UC_TRUST 19 and URL inputs. Check input parsing
        successes, errors, final_url = check_inputs(self,
                                                    input_element='tsp_url',
                                                    final_value=certificate_classpath, label_name='url',
                                                    save_btn=save_button_id,
                                                    input_element_type=By.ID, save_btn_type=By.ID, ts_url=ts_url,
                                                    test_name=test_name)

        # Save logged error messages and successes for later checking
        self.logdata += [log_fail] * errors
        self.logdata += [log_success] * successes


def check_inputs(self, input_element, final_value, save_btn, label_name='tsp_url',
                 invalid_url=timestamp_services.INVALID_URL,
                 input_element_type=By.ID,
                 save_btn_type=By.ID, ts_url=None, test_name=None):
    error_count = 0
    success_count = 0

    if test_name == timestamp_services.ADD_TEST_NAME:
        URL_TEXT_AND_RESULTS = [
            [256 * 'S', messages.INPUT_DATA_TOO_LONG.format(label_name), False],
            [' ', messages.MISSING_PARAMETER.format(label_name), False],
            [invalid_url, messages.INVALID_URL.format(invalid_url), False],
            [ts_url, log_constants.ADD_TS_EXISTING_URL.format(ts_url), False],
            ['   {0}   '.format(ts_url), log_constants.ADD_TS_EXISTING_URL.format(ts_url), False]
        ]
    else:
        URL_TEXT_AND_RESULTS = [
            [256 * 'S', messages.INPUT_DATA_TOO_LONG.format(label_name), False],
            [' ', messages.MISSING_PARAMETER.format(label_name), False],
        ]

    self.log('System verifies entered text, ')

    # Loop through different key label names and expected results
    counter = 1
    for data in URL_TEXT_AND_RESULTS:
        input_text = data[0].format(final_value, label_name)
        error_message = data[1]
        whitespaces = data[2]
        error = error_message is not None

        if error_message is not None and error_message is not True:
            error_message = error_message.format(input_text)
        if whitespaces:
            input_text_stripped = input_text.strip(' ')
        else:
            input_text_stripped = input_text

        self.log('Test-' + str(counter) + '. set - "' + input_text + '"')

        # Fill field
        input_field = self.wait_until_visible(element=input_element, type=input_element_type)
        self.input(input_field, input_text)

        try:
            # Click "OK" to try to save the settings.
            self.wait_until_visible(element=save_btn, type=save_btn_type).click()

            # Clicking the button starts an ajax query. Wait until request is complete.
            self.wait_jquery()
        except:
            self.is_equal(error_message, True, msg='Got an exception trying to save data')
            continue

        # Get the error message if any
        ui_error = messages.get_error_message(self)

        # Expecting error
        if error:
            if ui_error is not None:
                error_count += 1
                self.is_equal(ui_error, error_message, msg='Wrong error message, expected: {0}'.format(error_message))
            else:
                # Did not get an error.
                input_field = self.wait_until_visible(element=input_element, type=input_element_type)
                # URL input is not visible so the dialog has been closed = expected an error but data was saved instead
                if not input_field.is_displayed():
                    if error_message == True:
                        self.is_not_none(ui_error, msg='Expected failure but succeeded')
                    else:
                        self.is_not_none(ui_error, msg='No error message, expected: {0}'.format(error_message))

            messages.close_error_messages(self)
        else:
            self.is_none(ui_error, msg='Got error message for: "{0}"'.format(input_text))

            success_count += 1
        counter += 1

    self.wait_jquery()
    return success_count, error_count, input_text_stripped


def test_delete_ts(case, ts_name, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None):
    '''
    :param case: MainController object
    :param ts_name: str - TS display name (hostname)
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :return:
    '''
    self = case

    def del_ca():

        ''' We're looking for "Delete TS" log '''
        self.logdata = [log_constants.DELETE_TS]

        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()

        '''Select TS sertificate'''
        select_ts(self, ts_name)

        '''Save current TS sertificate name'''
        cert_name = self.by_xpath(timestamp_services.SERTIFICATE_NAME).text

        '''Click on delete button'''
        self.by_id(certification_services.TSDELETE_BTN_ID).click()
        self.wait_jquery()

        '''Click cancel button on popup'''
        self.by_xpath(popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()

        '''Confirm that sertificate is not deleted'''
        self.is_true(cert_name == ts_name,
                     msg='Sertificate is deleted')

        '''Select TS sertificate'''
        select_ts(self, ts_name)

        self.log('UC_TRUST_18 1. CS administrator selects to delete an approved timestamping service.')

        '''Click on delete button'''
        self.by_id(certification_services.TSDELETE_BTN_ID).click()
        self.wait_jquery()

        self.log('UC_TRUST_18 2. System prompts for confirmation.')
        self.log('UC_TRUST_18 3. CS administrator confirms.')

        '''Click ok button on popup'''
        self.by_xpath(popups.CONFIRM_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        self.log('UC_TRUST_18 4. System deletes the approved timestamping service information from the system configuration.')

        '''Get text "No (matching) records"'''
        no_records = self.by_xpath(timestamp_services.SERTIFICATE_EMPTY).text

        '''Confirm text "No (matching) records"'''
        self.is_false(no_records == ts_name,
                      msg='Sertificate is not deleted')

        if cs_ssh_host is not None:
            '''Check logs for entries'''
        self.log('TRUST_18 5.System logs the event “Delete timestamping service” to the audit log.')
        logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                               log_checker.found_lines))

    return del_ca
