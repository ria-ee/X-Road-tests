# coding=utf-8

import time

from selenium.webdriver.common.by import By

from helpers import xroad, auditchecker
from view_models import popups, messages, sidebar, certification_services, log_constants


def select_ca(self, ca_name):
    '''
    Selects a certification authority from the table and selects it by clicking on the row.
    :param self: MainController object
    :param ca_name: str - CA display name
    :return: None
    '''
    # Find the correct CA from the list
    ca = self.wait_until_visible(element=certification_services.get_ca_by_td_text(ca_name), type=By.XPATH)
    self.is_not_none(ca, msg='CA "{0}" not found in the table'.format(ca_name))

    # Click on the CA row to activate it
    ca.click()


def edit_ca_settings(self, ca_name):
    '''
    Selects a certification authority from the table and opens its settings by clicking the "Edit" button.
    :param self: MainController object
    :param ca_name: str - CA display name
    :return: None
    '''
    select_ca(self, ca_name)

    # Click the "Edit" button
    self.by_id(certification_services.DETAILS_BTN_ID).click()

    # Wait until the data has been loaded.
    self.wait_jquery()


def save_ca(self, close_errors=False):
    '''
    Tries to save certification authority settings by clicking "OK" in the settings dialog.
    :param self: MainController object
    :param close_errors: bool - close error/warning messages if any are displayed
    :return: (str|None, str|None, str|None) - warning message, error message, console output if shown, None if not shown
    '''

    # Click "OK" to try to save the settings.
    self.by_id(certification_services.SUBMIT_CA_CERT_BTN_ID).click()

    # Clicking the button starts an ajax query. Wait until request is complete.
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


def set_ca_certificate(self, ca_certificate, close_errors=False):
    '''
    Tries to upload a CA certificate in the settings dialog.
    :param self: MainController object
    :param ca_certificate: str - pathname of the certificate to upload
    :param close_errors: bool - close error/warning messages if any are displayed
    :return: (str|None, str|None, str|None) - warning message, error message, console output if shown, None if not shown
    '''
    self.log('Setting CA certificate: {0}'.format(ca_certificate))

    # Get the "Import certificate" button.
    import_cert_btn = self.wait_until_visible(type=By.ID,
                                              element=certification_services.IMPORT_CA_CERT_BTN_ID)

    # Set CA certificate
    xroad.fill_upload_input(self, import_cert_btn, ca_certificate)
    # Give some time for JS to react to file input being changed.
    time.sleep(0.5)

    # If an ajax query is initiated, wait for it to finish.
    self.wait_jquery()

    # Try to upload/save the certificate.
    self.wait_until_visible(type=By.ID, element=certification_services.SUBMIT_CA_CERT_BTN_ID).click()

    # Clicking the button starts an ajax query. Wait until request is complete.
    time.sleep(0.5)
    self.wait_jquery()
    time.sleep(0.1)

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


def set_invalid_ca_certificate(self, ca_certificate):
    '''
    Try to upload an invalid CA certificate and check if there was an error displayed.
    :param self: MainController object
    :param ca_certificate: str - pathname of the invalid certificate to upload
    :return: None
    '''

    # Try to set CA certificate and get returned error messages.
    warning, error, console = set_ca_certificate(self, ca_certificate)

    # Check if an error was shown and if the error was the correct one.
    self.is_not_none(error, msg='Set invalid CA certificate: no error shown'.format(ca_certificate))
    self.is_equal(error, messages.WRONG_FORMAT_CA_CERTIFICATE,
                  msg='Set invalid CA certificate: wrong error shown : {0}'.format(error))

    # Close all errors
    messages.close_error_messages(self)


def delete_ca(self, ca_name):
    '''
    Deletes a certification authority from the configuration.
    :param self: MainController object
    :param ca_name: str - CA display name
    :return: None
    '''
    # Select the CA from the list
    select_ca(self, ca_name)

    # Click "Delete"
    self.by_id(certification_services.DELETE_BTN_ID).click()

    # Wait until the table is refreshed
    self.wait_jquery()


def configure_ca_certificate(self, certificate_filename=None, invalid_certificate_filename=None):
    '''
    Adds a CA certificate (when adding a CA). If invalid_certificate_filename is not None, also tries to upload an
    invalid certificate and checks that the error message was correct.
    :param self: MainController object
    :param certificate_filename: str - pathname of the working certificate to upload
    :param invalid_certificate_filename: str|None - pathname of the invalid certificate to upload, None to not check
    :return: None
    '''
    # If invalid_certificate_filename is set, try to upload and check for errors.
    if invalid_certificate_filename is not None:
        # UC TRUST_08 3a - set invalid CA certificate
        self.log('TRUST_08 3a - setting invalid CA certificate')
        set_invalid_ca_certificate(self, invalid_certificate_filename)

    # UC TRUST_08 3 - set valid CA certificate
    self.log('TRUST_08 3 - setting valid CA certificate')
    set_ca_certificate(self, certificate_filename)

    # UC TRUST_08 4 - check for correct confirmation message
    self.log('TRUST_08 4 - check for correct confirmation message')

    # Get the confirmation message and check if it was the one we were looking for.
    confirmation_message = messages.get_notice_message(self)
    self.is_equal(confirmation_message, messages.CERTIFICATE_IMPORT_SUCCESSFUL,
                  msg='Expected message "{0}", got "{1}"'.format(messages.CERTIFICATE_IMPORT_SUCCESSFUL,
                                                                 confirmation_message))


def configure_ca(self, certificate_classpath=None,
                 auth_only_certs=False, check_errors=False, log_success=None, log_fail=None,
                 auth_only_element_xpath=None, classpath_element_xpath=None, save_button_id=None):
    '''
    Tries to configure the CA settings, checks for successes. If check_errors=True, also checks for error scenarios
    (wrong profile class, invalid input, etc). This function is used by both TRUST_08 and TRUST_09 cases so the
    comments and runtime logs have both bullet points in format TRUST_08-point/TRUST_09-point.
    :param self: MainController object
    :param certificate_classpath: str - certificate profile class path
    :param auth_only_certs: bool|None - only allow the CA to be used for authentication, None to use default
    :param check_errors: bool - True to check for error scenarios, False otherwise
    :return: None
    '''

    # UC TRUST_08 5a / TRUST_09 2a - set "authentication only" checkbox if specified. If auth_only_certs=None then ignore.
    if auth_only_certs is not None:
        self.log('TRUST_08 5a / TRUST_09 2a - set "authentication only" checkbox value to {0}'.format(auth_only_certs))

        # Find the checkbox
        auth_checkbox = self.wait_until_visible(auth_only_element_xpath, By.XPATH)
        checked = auth_checkbox.get_attribute('checked')

        # Click if the requested value is not already set
        checkbox_checked_when_not_needed = not auth_only_certs and (checked != '' and checked is not None)
        checkbox_not_checked_when_needed = auth_only_certs and (checked is None or checked == '')
        if checkbox_checked_when_not_needed or checkbox_not_checked_when_needed:
            auth_checkbox.click()

    # Check user input parsing if instructed so
    if check_errors:
        # UC TRUST_08 6 / TRUST_08 3 (parse user input), 6a/3a (user input parsing failed), 7a/4a (try to save wrong profile class), 5b/2b, 7/4 (correct class)
        self.log(
            'TRUST_08 6 / TRUST_08 3 (parse user input), 6a/3a (user input parsing failed), 7a/4a (try to save wrong profile class), 5b/2b, 7/4 (correct class)')

        # Use UC SS_41 to check input parsing, finish with space-padded data
        successes, errors, final_url = check_inputs(self,
                                                    input_element=classpath_element_xpath,
                                                    final_value=certificate_classpath, label_name='cert_profile_info',
                                                    save_btn=save_button_id,
                                                    input_element_type=By.XPATH, save_btn_type=By.ID,
                                                    invalid_input='invalid.class')

        # Save logged error messages and successes for later checking
        self.logdata += [log_fail] * errors
        self.logdata += [log_success] * successes
    else:
        # UC TRUST_08 5b, 7 / TRUST_09 2b, 4 - add correct class. No need to check for input parsing, just add the correct path.
        self.log(
            'TRUST_08 5b, 7 / TRUST_09 2b, 4 - add correct profile class')

        # Fill the profile class field
        input_field = filter(lambda x: x.size['height'] > 0, self.by_css(element=certification_services.CERTIFICATE_PROFILE_INFO_AREA_CSS, multiple=True))[0]
        self.input(input_field, certificate_classpath)
        # Save settings
        self.by_id(certification_services.SUBMIT_CA_SETTINGS_BTN_ID).click()

        # Save expected success log message for checking the logs later
        self.logdata.append(log_constants.ADD_CA)


def test_add_ca(case, ca_certificate, invalid_ca_certificate=None, certificate_classpath=None, cs_ssh_host=None,
                cs_ssh_user=None, cs_ssh_pass=None, auth_only_certs=False, check_errors=False):
    '''
    UC TRUST_08 main test method. Tries to add a CA and check logs if cs_ssh_host is set.
    :param case: MainController object
    :param ca_certificate: str - pathname of the correct CA certificate to upload
    :param ca_certificate: str|None - pathname of the invalid CA certificate to upload; if None, no invalid certificate
                            check will be done
    :param certificate_classpath: str - CA certificate profile class
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :return:
    '''
    self = case

    def add_ca():
        self.logdata = []

        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()

        # UC TRUST_10 1 - select to edit OCSP
        self.log('UC TRUST_08 1 - select to add CA')

        # Open "Certification services"
        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        # Click "Add"
        self.by_id(certification_services.ADD_BTN_ID).click()
        self.wait_jquery()

        # Configure CA certificates
        configure_ca_certificate(self, certificate_filename=ca_certificate,
                                 invalid_certificate_filename=invalid_ca_certificate)

        # Configure other CA settings
        configure_ca(self, certificate_classpath=certificate_classpath, check_errors=check_errors,
                     log_success=log_constants.ADD_CA, log_fail=log_constants.ADD_CA_FAILED,
                     auth_only_element_xpath=certification_services.ADD_CA_AUTH_ONLY_CHECKBOX_XPATH,
                     classpath_element_xpath=certification_services.ADD_CERTIFICATE_PROFILE_INFO_AREA_XPATH,
                     save_button_id=certification_services.SUBMIT_CA_SETTINGS_BTN_ID,
                     auth_only_certs=auth_only_certs
                     )

        # UC TRUST_08 8 - check for correct confirmation message
        self.log('TRUST_08 8 - check for correct confirmation message')

        confirmation_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
        self.is_equal(confirmation_message, messages.CA_ADD_SUCCESSFUL,
                      msg='Expected message "{0}", got "{1}"'.format(messages.CA_ADD_SUCCESSFUL, confirmation_message))

        if cs_ssh_host is not None:
            # Check logs for entries
            self.log('TRUST_08 6a, 7a, 9 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))
        if auth_only_certs:
            self.log('TRUST_08 5(a) certification service is marked for only authentication service')
            self.wait_until_visible(type=By.XPATH, element=certification_services.CA_SETTINGS_TAB_XPATH).click()
            auth_checkbox = self.wait_until_visible(certification_services.EDIT_CA_AUTH_ONLY_CHECKBOX_XPATH, By.XPATH)
            checked = auth_checkbox.get_attribute('checked')
            self.is_equal('true', checked)

    return add_ca


def test_edit_ca(case, ca_name, certificate_classpath=None, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None):
    '''
    UC TRUST_09 main test method. Tries to edit a CA and check logs if cs_ssh_host is set.
    :param case: MainController object
    :param ca_name: str - CA display name (hostname)
    :param certificate_classpath: str - CA certificate profile class
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :return:
    '''
    self = case

    def edit_ca():
        self.logdata = []

        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()

        # UC TRUST_10 1 - select to edit OCSP
        self.log('UC TRUST_09 1 - select to edit OCSP responder for CA: {0}'.format(ca_name))

        # Open "Certification services"
        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        # Edit CA settings
        edit_ca_settings(self, ca_name)

        # Open CA settings tab
        self.by_xpath(certification_services.CA_SETTINGS_TAB_XPATH).click()

        # Configure other CA settings
        configure_ca(self, certificate_classpath=certificate_classpath, check_errors=True,
                     log_success=log_constants.EDIT_CA, log_fail=log_constants.EDIT_CA_FAILED,
                     auth_only_element_xpath=certification_services.EDIT_CA_AUTH_ONLY_CHECKBOX_XPATH,
                     classpath_element_xpath=certification_services.EDIT_CERTIFICATE_PROFILE_INFO_AREA_XPATH,
                     save_button_id=certification_services.SAVE_CA_SETTINGS_BTN_ID)

        if cs_ssh_host is not None:
            # Check logs for entries
            self.log('TRUST_09 3a, 4a, 5 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

    return edit_ca


def delete_last_ca(self):
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.CERTIFICATION_SERVICES_CSS).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=certification_services.LAST_ADDED_CERT_XPATH).click()
    self.wait_until_visible(type=By.ID, element=certification_services.DELETE_BTN_ID).click()
    popups.confirm_dialog_click(self)

    # Wait until the table is refreshed
    self.wait_jquery()


def test_delete_ca(case, ca_name, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None, cancel_deletion=False):
    '''
    UC TRUST_14 main test method. Tries to delete a CA and check logs if cs_ssh_host is set.
    :param case: MainController object
    :param ca_name: str - CA display name (hostname)
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :param cancel_deletion: bool|None - if true, cancels deletion before deleting
    :return:
    '''
    self = case

    def del_ca():
        # We're looking for "Delete CA" log
        self.logdata = [log_constants.DELETE_CA]

        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()

        # UC TRUST_14 1 - select to delete CA
        self.log('TRUST_14 1 - select to delete CA: {0}'.format(ca_name))

        # Open "Certification services"
        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        # UC TRUST_14 2 select and delete CA
        self.log('TRUST_14 2 - delete CA')
        delete_ca(self, ca_name)

        # UC TRUST_14 3a cancel CA deletion
        if cancel_deletion:
            # Cancel the deletion
            self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            # Click "Delete" button again
            delete_ca(self, ca_name)

        # Confirm the deletion
        popups.confirm_dialog_click(self)

        if cs_ssh_host is not None:
            # Check logs for entries
            self.log('TRUST_14 3 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

    return del_ca


def check_inputs(self, input_element, final_value, save_btn, label_name='cert_profile_info', input_element_type=By.ID,
                 save_btn_type=By.XPATH, invalid_input='invalid input'):
    '''
    Tries to enter different erroneous values to an input field and check if the error messages were correct.
    :param self: MainController object
    :param input_element: str - input element ID, XPath, or CSS selector
    :param final_value: str - correct value to be entered as a final step
    :param save_btn: str - save/OK button ID, XPath, or CSS selector
    :param label_name: str - input label internal name, used in some error messages
    :param input_element_type: By - input element selector type, default is By.ID
    :param save_btn_type: By - input element selector type, default is By.XPATH
    :param invalid_input: str - invalid input value (for classes, URLs, etc)
    :return: (int, int, str) - number of successful save attempts, number of unsuccessful save attempts, final saved value;
                                numbers are used for counting the success/failure log entries.
    '''
    error_count = 0
    success_count = 0
    URL_TEXT_AND_RESULTS = [
        [256 * 'S', messages.INPUT_DATA_TOO_LONG.format(label_name), False],
        [invalid_input, messages.INVALID_CERTIFICATE_PROFILE.format(invalid_input), True],
        [' ', messages.MISSING_PARAMETER.format(label_name), False],
        ['', True, False],
        ['   {0}   ', None, True]
    ]

    self.log('SS_28_4 System verifies entered text')

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
