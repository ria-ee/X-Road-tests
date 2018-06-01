# coding=utf-8

import re
import time
import urllib

from selenium.webdriver.common.by import By

from helpers import xroad, auditchecker, ssh_server_actions
from view_models import clients_table_vm, popups, messages, ss_system_parameters, log_constants
from view_models.clients_table_vm import SERVICE_CLASS_NAME
from view_models.log_constants import EDIT_WSDL_FAILED, EDIT_WSDL, EDIT_SERVICE_PARAMS_FAILED, ADD_WSDL_FAILED, \
    DELETE_WSDL
from view_models.messages import WSDL_EDIT_ERROR_WSDL_EXISTS, WSDL_EDIT_ERROR_VALIDATION_FAILED, \
    WSDL_EDIT_ERROR_FILE_DOES_NOT_EXIST, SERVICE_EDIT_INVALID_URL, SERVICE_EDIT_INFINITE_TIMEOUT_WARNING, \
    SERVICE_EDIT_INVALID_TIMEOUT, WSDL_ERROR_ADDRESS_EXISTS, WSDL_ERROR_DUPLICATE_SERVICE, WSDL_ERROR_VALIDATION_FAILED
from view_models.popups import EDIT_WSDL_POPUP_CANCEL_BTN_XPATH, CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID, \
    EDIT_WSDL_BUTTON_ID, CLIENT_DETAILS_POPUP_ACCESS_RIGHTS_BTN_ID, WSDL_SERVICE_CODE_REGEX, \
    WSDL_SERVICE_CODE_DATE_REGEX, WSDL_SERVICE_URL_REGEX, WSDL_SERVICE_TIMEOUT_REGEX, \
    CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_FIRST_SUBJECT_ROW_CSS, XROAD_IDENTIFIER_REGEX, \
    CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_ADD_SUBJECTS_BTN_CSS, \
    CLIENT_DETAILS_POPUP_ACL_SUBJECTS_REMOVE_ALL_BTN_ID, CLIENT_DETAILS_POPUP_ACL_SUBJECTS_REMOVE_SELECTED_BTN_ID


def view_wsdl(self, client, client_name, expected_wsdl_url):
    def view_wsdl():
        self.log('SERVICE_06 1. View security server client\'s WSDLs')
        clients_table_vm.open_client_popup_services(self, client=client, client_name=client_name)
        self.log('SERVICE_06 2. System displays the WSDL')
        wsdl_row = self.wait_until_visible(type=By.CLASS_NAME, element='wsdl')
        self.log('Get wsdl row columns')
        wsdl_cols = wsdl_row.find_elements_by_tag_name('td')
        expected_wsdl_url_col = 'WSDL ({})'.format(expected_wsdl_url)
        self.log('SERVICE_06 2. System displays the URL of the WSDL {}'.format(expected_wsdl_url))
        wsdl_url = wsdl_cols[1].text
        self.is_equal(expected_wsdl_url_col, wsdl_url)
        self.log('SERVICE_06 2. System displays the date of when the WSDL was last refresh')
        wsdl_refresh_date = wsdl_cols[-1].text
        self.is_true(re.match(WSDL_SERVICE_CODE_DATE_REGEX, wsdl_refresh_date))

    return view_wsdl


def add_wsdl(self,
             wsdl_url, clear_field=True):
    '''
    Tries to enter WSDL url to "Add WSDL" URL input field and click "OK"
    :param self:
    :param wsdl_url: str - URL that contains the WSDL
    :param clear_field: Boolean - clear the field before entering anything
    :return:
    '''

    self.log('Adding WSDL: {0}'.format(wsdl_url))

    # Find the "Add WSDL" dialog. Because this function can be called from a state where the dialog is open and
    # a state where it is not, we'll first check if the dialog is open. If it is not, we'll click the "Add WSDL"
    # button to open it.
    wsdl_dialog = self.by_xpath(popups.ADD_WSDL_POPUP_XPATH)

    # Open the dialog if it is not already open
    if not wsdl_dialog.is_displayed():
        # Find "Add WSDL" button and click it.
        add_wsdl_button = self.by_id(popups.CLIENT_DETAILS_POPUP_ADD_WSDL_BTN_ID)
        add_wsdl_button.click()

        # Find the dialog and wait until it is visible.
        self.wait_until_visible(wsdl_dialog)

    # Now an "Add WSDL" dialog with a URL prompt should be open. Let's try to add the WSDL.

    # Find the URL input element
    wsdl_url_input = self.by_id(popups.ADD_WSDL_POPUP_URL_ID)

    # Clear the field if told so
    if clear_field:
        wsdl_url_input.clear()

    # Enter the WSDL URL into the input.
    # wsdl_url_input.send_keys(wsdl_url)
    self.input(wsdl_url_input, wsdl_url)

    # Find the "OK" button in "Add WSDL" dialog
    wsdl_dialog_ok_button = self.by_xpath(popups.ADD_WSDL_POPUP_OK_BTN_XPATH)
    wsdl_dialog_ok_button.click()

    # Clicking the button starts an ajax query. Wait until request is complete.
    self.wait_jquery()

    console_output = messages.get_console_output(self)  # Console message (displayed if WSDL validator gives a warning)
    warning_message = messages.get_warning_message(self)  # Warning message
    error_message = messages.get_error_message(self)  # Error message (anywhere)

    if console_output is not None:
        popups.close_console_output_dialog(self)

    return warning_message, error_message, console_output


def edit_wsdl(self, wsdl_url, clear_field=True):
    '''
    Tries to enter WSDL url to "Edit WSDL Parameters" dialog URL input field and press "OK"
    :param self:
    :param url: str - URL that contains the WSDL
    :param clear_field: Boolean - clear the field before entering anything
    :return:
    '''

    self.log('Setting new WSDL: {0}'.format(wsdl_url))

    # Find the "Edit WSDL Parameters" dialog. Because this function can be called from a state where the dialog is open and
    # a state where it is not, we'll first check if the dialog is open. If it is not, we'll click the "Edit"
    # button to open it.
    wsdl_dialog = self.by_xpath(popups.EDIT_WSDL_POPUP_XPATH)

    # Open the dialog if it is not already open
    if not wsdl_dialog.is_displayed():
        # Find "Edit" button and click it.
        edit_wsdl_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)
        edit_wsdl_button.click()

        # Find the dialog and wait until it is visible.
        self.wait_until_visible(wsdl_dialog)

    # Now an "Edit WSDL Parameters" dialog with a URL prompt should be open. Let's try to set the WSDL URL.

    # Find the URL input element
    wsdl_url_input = self.by_id(popups.EDIT_WSDL_POPUP_URL_ID)

    # Clear the field if told so
    if clear_field:
        wsdl_url_input.clear()

    # Enter the WSDL URL into the input.
    # wsdl_url_input.send_keys(wsdl_url)
    self.input(wsdl_url_input, wsdl_url)

    # Find the "OK" button in "Edit WSDL Parameters" dialog
    wsdl_dialog_ok_button = self.by_xpath(popups.EDIT_WSDL_POPUP_OK_BTN_XPATH)
    wsdl_dialog_ok_button.click()

    # Clicking the button starts an ajax query. Wait until request is complete.
    self.wait_jquery()

    console_output = messages.get_console_output(self)  # Console message (displayed if WSDL validator gives a warning)
    warning_message = messages.get_warning_message(self)  # Warning message
    error_message = messages.get_error_message(self)  # Error message (anywhere)

    if console_output is not None:
        popups.close_console_output_dialog(self)

    return warning_message, error_message, console_output


def edit_service(self, service_url, service_timeout=None, verify_tls=None):
    '''
    Tries to enter WSDL url to "Edit WSDL Parameters" dialog URL input field and press "OK"
    :param self:
    :param url: str - URL that contains the WSDL
    :param clear_field: Boolean - clear the field before entering anything
    :return:
    '''

    self.log('Setting new service URL with timeout {1}: {0}'.format(service_timeout, service_url))

    # Find the "Edit Service Parameters" dialog. Because this function can be called from a state where the dialog is open and
    # a state where it is not, we'll first check if the dialog is open. If it is not, we'll click the "Edit"
    # button to open it.
    wsdl_dialog = self.by_xpath(popups.EDIT_SERVICE_POPUP_XPATH)

    # Open the dialog if it is not already open
    if not wsdl_dialog.is_displayed():
        # Find "Edit" button and click it.
        edit_wsdl_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)
        edit_wsdl_button.click()

        # Find the dialog and wait until it is visible.
        self.wait_until_visible(wsdl_dialog)

    # Now an "Edit Service Parameters" dialog with a URL prompt should be open. Let's try to set the service URL.

    # Find the URL input element
    service_url_input = self.by_id(popups.EDIT_SERVICE_POPUP_URL_ID)
    service_timeout_input = self.by_id(popups.EDIT_SERVICE_POPUP_TIMEOUT_ID)

    # Enter the service URL.
    self.input(service_url_input, service_url)

    # Set service timeout if specified
    if service_timeout is not None:
        # UC SERVICE_timeout_input.clear()
        # UC SERVICE_timeout_input.send_keys(service_timeout)
        self.input(service_timeout_input, service_timeout)

    # Set "Verify TLS" if specified
    if verify_tls is not None:
        service_tls_checkbox = self.wait_until_visible(popups.EDIT_SERVICE_POPUP_TLS_ENABLED_XPATH, By.XPATH)
        checked = service_tls_checkbox.get_attribute('checked')

        if ((checked != '' and checked is not None) and not verify_tls) or (checked is None and verify_tls):
            service_tls_checkbox.click()

    # Find the "OK" button in "Edit WSDL Parameters" dialog
    wsdl_dialog_ok_button = self.by_xpath(popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH)
    wsdl_dialog_ok_button.click()

    # Clicking the button starts an ajax query. Wait until request is complete.
    self.wait_jquery()

    warning_message = messages.get_warning_message(self)  # Warning message
    error_message = messages.get_error_message(self)  # Error message (anywhere)

    return warning_message, error_message


def test_configure_service(case, client=None, client_name=None, client_id=None, service_name=None, service_url=None,
                           service_2_name=None, service_2_url=None, check_add_errors=True, check_edit_errors=True,
                           check_parameter_errors=True):
    '''
    MainController test function. Configures a new service.
    '''

    self = case

    ss2_host = self.config.get('ss2.host')
    ss2_user = self.config.get('ss2.user')
    ss2_pass = self.config.get('ss2.pass')
    ss2_ssh_host = self.config.get('ss2.ssh_host')
    ss2_ssh_user = self.config.get('ss2.ssh_user')
    ss2_ssh_pass = self.config.get('ss2.ssh_pass')
    wsdl_ssh_host = self.config.get('wsdl.ssh_host')
    wsdl_ssh_user = self.config.get('wsdl.ssh_user')
    wsdl_ssh_pass = self.config.get('wsdl.ssh_pass')

    wsdl_incorrect_url = self.config.get_string('wsdl.incorrect_url',
                                                'incorrect url')  # URL that doesn't start with http or https
    wsdl_malformed_url = self.config.get_string('wsdl.malformed_url', self.config.get('wsdl.remote_path').format(
        ''))  # URL that doesn't return a WSDL
    wsdl_correct_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl'))  # Correct URL that returns a WSDL file

    wsdl_test_service = self.config.get('wsdl.service_wsdl_test_service1')
    wsdl_single_service = self.config.get('wsdl.service_single_service_filename')

    wsdl_test_service_url = self.config.get('wsdl.remote_path').format(wsdl_test_service)

    wsdl_duplicate_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.duplicate_service_wsdl'))  # Contains the same service as wsdl_correct_url

    wsdl_error_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_error_filename'))  # WSDL that cannot be validated

    wsdl_warning_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_warning_filename'))  # WSDL that gives a validator warning

    service_url_additional_parameter = 'db'  # Additional parameter name for client code to be appended to test service URL
    service_invalid_url = self.config.get_string('wsdl.invalid_url', 'invalid url')
    service_invalid_timeouts = ['-1', 'hello', '10error']  # List of timeouts to test
    service_infinite_timeout = self.config.get_string('wsdl.infinite_timeout',
                                                      '0')  # A timeout that should give an infinite timeout warning

    wsdl_disabled_prefix = self.config.get_string('wsdl.disabled_prefix', 'WSDL DISABLED')
    wsdl_disabled_class = self.config.get_string('wsdl.disabled_class', 'disabled')

    wsdl_local_path = self.config.get('wsdl.local_path')
    target_wsdl_path = wsdl_local_path.format(wsdl_test_service)

    client_id = xroad.get_xroad_subsystem(client)

    def configure_service():
        """
        :param self: MainController class object
        :return: None
        ''"""

        # UC SERVICE_08 Add a WSDL to a Security Server Client
        self.log('*** SERVICE_08 Add a WSDL to a Security Server Client')

        self.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)

        log_checker = auditchecker.AuditChecker(host=ss2_ssh_host, username=ss2_ssh_user, password=ss2_ssh_pass)
        # UC SERVICE_08 1. Select to add test service WSDL
        self.log('SERVICE_08 1. Select to add test service WSDL')

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        # Find the table that lists all WSDL files and services
        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        # Wait until that table is visible (opened in a popup)
        self.wait_jquery()
        self.wait_until_visible(services_table)

        # Test precondition: the WSDL has not been added already. Check if finding service with wsdl_correct_url
        # returns None (= not found).
        self.is_none(clients_table_vm.find_wsdl_by_name(self, wsdl_correct_url),
                     msg='SERVICE_08 1. WSDL {0} has already been added. Remove the service and try again.'
                     .format(wsdl_correct_url))

        # UC SERVICE_08 2. Insert the WSDL URL.
        self.log('SERVICE_08 2. Insert the WSDL URL.')

        if check_add_errors:
            # UC SERVICE_08 3a. Trying to add WSDL with an incorrect URL
            self.log('SERVICE_08 3a. Trying to add WSDL with an incorrect URL: {0}'.format(wsdl_incorrect_url))
            warning, error, console = add_wsdl(self, wsdl_incorrect_url)
            self.is_not_none(error, msg='SERVICE_08 3a.1. Incorrect URL: no error shown for WSDL {0}'.format(
                wsdl_incorrect_url))
            self.is_equal(error, messages.WSDL_ERROR_INVALID_URL.format(wsdl_incorrect_url),
                          msg='SERVICE_08 3a.1. Incorrect URL: wrong error shown for WSDL {0} : {1}'
                          .format(wsdl_incorrect_url, error))
            self.is_none(warning, msg='SERVICE_08 3a.1. Incorrect URL: got warning for WSDL {0} : {1}'
                         .format(wsdl_incorrect_url, warning))
            self.is_none(console, msg='SERVICE_08 3a.1. Incorrect URL: got console output for WSDL {0} : {1}'
                         .format(wsdl_incorrect_url, console))
            self.log('SERVICE_08 3a.1. Error message: {0}'.format(warning))

            # UC SERVICE_08 3a.3. Reinsert the URL.
            self.log('SERVICE_08 3a.3. Reinsert the URL.')

            # UC SERVICE_08 5a./SERVICE_10 2b. Error 2 - trying to add WSDL with a URL that doesn't return a WSDL file
            self.log(
                'SERVICE_08 5a./SERVICE_10 2b. Error 2 add WSDL with a URL that doesn''t return a WSDL file: {0}'.format(
                    wsdl_malformed_url))
            current_log_lines = log_checker.get_line_count()
            warning, error, console = add_wsdl(self, wsdl_malformed_url)
            self.is_not_none(error, msg='SERVICE_08 5a.1. Incorrect WSDL: no error shown for WSDL {0}'.format(
                wsdl_malformed_url))
            self.is_equal(error, messages.WSDL_ERROR_INCORRECT_WSDL.format(wsdl_malformed_url),
                          msg='SERVICE_08 5a.1. Incorrect WSDL: wrong error shown for WSDL {0} : {1}'
                          .format(wsdl_malformed_url, error))
            self.is_none(warning, msg='SERVICE_08 5a.1. Incorrect WSDL: got warning for WSDL {0} : {1}'
                         .format(wsdl_malformed_url, warning))
            self.is_none(console, msg='SERVICE_08 5a.1. Incorrect WSDL: got console output for WSDL {0} : {1}'
                         .format(wsdl_malformed_url, console))
            self.log('SERVICE_08 5a.1. Error message: {0}'.format(warning))
            '''SERVICE_08 5a.2. Downloading and parsing WSDL terminated with error is logged in audit log'''
            self.log('SERVICE_08 5a.2. Checking if audit log contains "Add WSDL Failed" event')
            logs_found = log_checker.check_log(log_constants.ADD_WSDL_FAILED, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='SERVICE_08 5a.2. Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                             log_constants.ADD_WSDL_FAILED,
                             log_checker.found_lines))

        # UC SERVICE_08 3-7. System parses the user input, verified unique WSDL, reads info and parses the WSDL.
        self.log('SERVICE_08 3-7. System parses the user input, verified unique WSDL, reads info and parses the WSDL.')

        # UC SERVICE_08 8. First let's add the unique WSDL and it should succeed. (Validation comes later)
        self.log('SERVICE_08 3-7. Add (unique) WSDL with URL: {0}'.format(wsdl_correct_url))
        warning, error, console = add_wsdl(self, wsdl_correct_url)
        self.is_none(error, msg='SERVICE_08 3-7. Add unique WSDL: got error for WSDL {0} : {1}'.format(wsdl_correct_url,
                                                                                                       error))
        self.is_none(warning,
                     msg='SERVICE_08 3-7. Add unique WSDL: got warning for WSDL {0} : {1}'.format(wsdl_correct_url,
                                                                                                  warning))
        self.is_none(console,
                     msg='SERVICE_08 3-7. Add unique WSDL: got console output for WSDL {0} : {1}'.format(
                         wsdl_correct_url,
                         console))

        if check_add_errors:
            # Trying to add a WSDL with a URL that has already been added
            current_log_lines = log_checker.get_line_count()
            self.log('SERVICE_08 4a. The inserted URL already exists')
            warning, error, console = add_wsdl(self, wsdl_correct_url)
            self.is_not_none(error, msg='Add duplicate WSDL: no error shown for WSDL {0}'.format(wsdl_correct_url))
            expected_error_msg = WSDL_ERROR_ADDRESS_EXISTS.format(wsdl_correct_url)
            self.log('SERVICE_08 4a.1 System displays the error message "{0}"'.format(expected_error_msg))
            self.is_equal(expected_error_msg, error,
                          msg='Add duplicate WSDL: wrong error shown for WSDL {0} : {1}'.format(wsdl_correct_url,
                                                                                                error))
            self.is_none(warning, msg='Add duplicate WSDL: got warning for WSDL {0} : {1}'
                         .format(wsdl_correct_url, warning))
            self.is_none(console, msg='Add duplicate WSDL: got console output for WSDL {0} : {1}'
                         .format(wsdl_correct_url, console))
            self.log('Error message: {0}'.format(warning))
            expected_log_msg = ADD_WSDL_FAILED
            self.log('SERVICE_08 4a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            current_log_lines = log_checker.get_line_count()

            self.log('SERVICE_08 7a. A service with the same service code and version values as a '
                     'service read from the WSDL file was found for this client in the system configuration')
            warning, error, console = add_wsdl(self, wsdl_duplicate_url)
            expected_error_msg = WSDL_ERROR_DUPLICATE_SERVICE.format(wsdl_duplicate_url)
            self.log('SERVICE_08 7a.2 System displays the error message "{0}"'.format(expected_error_msg))
            self.is_not_none(error, msg='Add duplicate service: no error shown for WSDL {0}'.format(wsdl_duplicate_url))
            error_message_is_correct = error.startswith(expected_error_msg)
            self.is_true(error_message_is_correct,
                         msg='Add duplicate service: wrong error shown for WSDL {0} : {1}'.format(wsdl_duplicate_url,
                                                                                                  error))
            self.is_none(warning, msg='Add duplicate service: got warning for WSDL {0} : {1}'
                         .format(wsdl_duplicate_url, warning))
            self.is_none(console, msg='Add duplicate service: got console output for WSDL {0} : {1}'
                         .format(wsdl_duplicate_url, console))
            self.log('Error message: {0}'.format(warning))
            self.log('SERVICE_08 7a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            current_log_lines = log_checker.get_line_count()

            self.log('SERVICE_08 6b. The process of downloading and parsing the '
                     'WSDL file terminated with an error message')
            warning, error, console = add_wsdl(self, wsdl_error_url)
            expected_error_msg = WSDL_ERROR_VALIDATION_FAILED.format(wsdl_error_url)
            self.log(
                'SERVICE_08 6b.1/SERVICE_44 1a. System displays the error message "{0}"'.format(expected_error_msg))
            self.is_not_none(error, msg='Add invalid WSDL: no error shown for WSDL {0}'.format(wsdl_error_url))
            self.is_equal(expected_error_msg, error,
                          msg='Add invalid WSDL: wrong error shown for WSDL {0} : {1}'.format(wsdl_error_url, error))
            self.is_none(warning, msg='Add invalid WSDL: got warning for WSDL {0} : {1}'
                         .format(wsdl_error_url, warning))
            self.is_not_none(console, msg='Add invalid WSDL: no console output shown for WSDL {0} : {1}'
                             .format(wsdl_error_url, console))
            self.log('Error message: {0}'.format(error))
            self.log('Console output: {0}'.format(console))
            self.log('SERVICE_08 6b.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

            # UC SERVICE_08 6c. Add WSDL that gives a validator warning
            self.log(
                'SERVICE_08 6c./SERVICE_44 1b. Add WSDL that gives a validator warning: {0}'.format(wsdl_warning_url))
            warning, error, console = add_wsdl(self, wsdl_warning_url)
            self.is_none(error,
                         msg='SERVICE_08 6c.1. Add WSDL with validator warnings: got error for WSDL {0}'.format(
                             wsdl_warning_url))
            self.is_not_none(warning,
                             msg='SERVICE_08 6c.1. Add WSDL with validator warnings: no warning shown for WSDL {0} : {1}'
                             .format(wsdl_warning_url, warning))
            self.is_none(console,
                         msg='SERVICE_08 6c.1. Add WSDL with validator warnings: got console output for WSDL {0} : {1}'
                         .format(wsdl_warning_url, console))
            self.log('SERVICE_08 6c.1. Warning message: {0}'.format(warning))

            # We're not adding the WSDL that gives us warnings, so find the "Cancel" button and click it.
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CANCEL_XPATH).click()
            self.wait_jquery()

            # Now we need to cancel the "Add WSDL" popup. Find the "Cancel" button and click it.
            self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_CANCEL_BTN_XPATH).click()

            # UC SERVICE_08 6c.2a. Terminate the use case.
            self.log('SERVICE_08 6c.2a. Terminate the use case.')

        # UC SERVICE_08 9. Check if our unique WSDL has been successfully added and is disabled
        self.log('SERVICE_08 8. Checking if WSDL was added and is disabled: {0}'.format(wsdl_correct_url))

        wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_correct_url)
        self.log('SERVICE_08 8. WSDL table row index: {0}'.format(wsdl_index))

        # Check if wsdl_index is not None - if it is, we didn't find the WSDL in the list after adding it.
        self.is_not_none(wsdl_index,
                         msg='SERVICE_08 8. WSDL not found in services table after adding: {0}'.format(
                             wsdl_correct_url))

        # Get the WSDL tr (table row) element from services table
        wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_index)

        # Verify that the row starts with "WSDL DISABLED" and is in red letter (we're
        # checking if the class is "disabled" - this sets the color)

        # Get the service code td (table cell) element (this should start with WSDL DISABLED)
        wsdl_service_code = wsdl_row.find_elements_by_tag_name('td')[1]
        self.is_equal(wsdl_service_code.text.startswith(wsdl_disabled_prefix), True,
                      msg='SERVICE_08 8. Added WSDL row does not start with "WSDL DISABLED": {0}'.format(
                          wsdl_correct_url))

        # Get the row classes to check if "disabled" is in this list. This is the class that makes the row text red.
        wsdl_row_classes = self.get_classes(wsdl_row)
        self.is_equal(wsdl_disabled_class in wsdl_row_classes, True,
                      msg='SERVICE_08 8. Added WSDL row does not have class "disabled": {0}'.format(wsdl_correct_url))

        # Select the WSDL by clicking on the row
        self.click(wsdl_row)

        # UC SERVICE_08 8. check if default disable message is correct
        # enable and disable WSDL to get disable message popup
        self.log('SERVICE 08 8. Check if default disable message is correct')
        self.by_id(popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()
        self.wait_jquery()
        self.by_id(popups.CLIENT_DETAILS_POPUP_DISABLE_WSDL_BTN_ID).click()
        self.wait_jquery()
        disabled_message = self.by_id(popups.DISABLE_WSDL_POPUP_NOTICE_ID).get_attribute('value')
        # Check disable message value
        self.is_equal(messages.SERVICE_DISABLED_MESSAGE, disabled_message,
                      msg='SERVICE 08 8. Disable message not equal to {0}'.format(messages.SERVICE_DISABLED_MESSAGE))
        # Confirm disable message
        self.by_xpath(popups.DISABLE_WSDL_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        # Open service parameters by finding the "Edit" button and clicking it.
        edit_wsdl_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)
        self.wait_jquery()

        if check_edit_errors:
            # UC SERVICE_09 (Edit the Address of a WSDL) and SERVICE_10 (Download and Parse WSDL) checks
            self.log('SERVICE_09/SERVICE_10 checks')
            ssh_client = ssh_server_actions.get_client(wsdl_ssh_host, wsdl_ssh_user, wsdl_ssh_pass)
            self.log('Copy single wsdl file to test wsdl')
            ssh_server_actions.cp(ssh_client, wsdl_local_path.format(wsdl_single_service), target_wsdl_path)
            service_name_wo_version = service_name[:-3]
            self.log('Change {0} service to xroadTest123'.format(service_name_wo_version))
            ssh_client.exec_command(
                'sed -i -e "s/{0}/xroadTest123/g" {1}'.format(service_name_wo_version, target_wsdl_path),
                sudo=True)
            self.log('Add test wsdl to client')
            add_wsdl(self, wsdl_test_service_url)
            edit_wsdl_button = self.by_id(CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)
            edit_wsdl_button.click()
            self.log('SERVICE_10 2a. Downloading of the WSDL file failed')
            not_existing_wsdl_url = self.config.get('wsdl.remote_path').format('doesntexist.wsdl')
            self.log('Editing wsdl file to not existing file')
            warning, error, console = edit_wsdl(self, not_existing_wsdl_url)
            expected_error_msg = WSDL_EDIT_ERROR_FILE_DOES_NOT_EXIST
            self.log('SERVICE_10 2a.1 Use case terminates with the error message "{0}"'.format(expected_error_msg))
            self.is_equal(expected_error_msg, error)
            self.by_xpath(EDIT_WSDL_POPUP_CANCEL_BTN_XPATH).click()

            self.log('SERVICE_09 4a. The inserted URL already exists')
            current_log_lines = log_checker.get_line_count()
            warning, error, console = edit_wsdl(self, wsdl_test_service_url)
            expected_error_msg = WSDL_EDIT_ERROR_WSDL_EXISTS
            self.log('SERVICE_09 4a.1 System displays the error message "{0}"'.format(expected_error_msg))
            self.is_equal(expected_error_msg, error)
            expected_log_msg = EDIT_WSDL_FAILED
            self.log('SERVICE_09 4a.2 System logs the eventCheck if audit log contains WSDL edit fail event')
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            self.by_xpath(popups.EDIT_WSDL_POPUP_CANCEL_BTN_XPATH).click()

            current_log_lines = log_checker.get_line_count()
            self.log('SERVICE_10 3a. WSDL validation failed'
                     'SERVICE_09 5a. The process of refreshing the WSDL file terminated with error message')
            self.log('Changing wsdl to wsdl which can\'t be validated')
            warning, error, console = edit_wsdl(self, wsdl_error_url)
            expected_error_msg = WSDL_EDIT_ERROR_VALIDATION_FAILED.format(wsdl_error_url)
            self.log('SERVICE_10 3a.1 System displays the error message "{0}"'
                     'SERVICE_09 5a.1 System displays the error message "{0}"'.format(expected_error_msg))
            self.is_equal(expected_error_msg, error)
            self.is_not_none(console, msg='Set invalid WSDL: no console output shown for WSDL {0} : {1}'
                             .format(wsdl_error_url, console))
            expected_log_msg = EDIT_WSDL_FAILED
            self.log('SERVICE_09 5a.2 System logs the event "{0}" to the audit log'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

            self.log(
                'SERVICE_09 trying to set WSDL URL that gives a validator warning: {0}'.format(wsdl_warning_url))
            warning, error, console = edit_wsdl(self, wsdl_warning_url)
            self.is_none(error,
                         msg='Set WSDL with validator warnings: got error for WSDL {0}'.format(wsdl_warning_url))
            self.is_not_none(warning, msg='Set WSDL with validator warnings: no warning shown for WSDL {0} : {1}'
                             .format(wsdl_warning_url, warning))
            self.is_none(console, msg='Set WSDL with validator warnings: got console output for WSDL {0} : {1}'
                         .format(wsdl_warning_url, console))
            self.log('Warning message: {0}'.format(warning))

            self.log('SERVICE_09 5. Canceling wsdl with warning adding')
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CANCEL_XPATH).click()
            self.wait_jquery()

            self.log('SERVICE_09 5. Adding same wsdl again, this time confirming')
            edit_wsdl(self, wsdl_warning_url)
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
            self.wait_jquery()

            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
            self.wait_jquery()

            wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_warning_url)
            wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_index)

            open_services_element = wsdl_row.find_element_by_css_selector(
                popups.CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS)
            open_services_element.click()
            self.wait_jquery()
            self.log('Check if wsdl services got refreshed, it should not contain any services')
            try:
                self.by_css('.service')
                assert False
            except:
                pass

            # UC SERVICE_09 - trying to update WSDL that gives a validator warning
            self.log('SERVICE_09 Edit the Address of a WSDL')

            # UC SERVICE_09 1. Select to edit the address of a WSDL
            self.log('SERVICE_09 1. Select to edit the address of a WSDL')

            self.click(wsdl_row)
            edit_wsdl_button.click()

            current_log_lines = log_checker.get_line_count()

            # UC SERVICE_09 2. Insert new URL
            self.log('SERVICE_09 2. Insert new URL')

            edit_wsdl(self, wsdl_correct_url)
            # UC SERVICE_09 3-5. Parse, verify and refresh WSDL
            self.log('SERVICE_09 3-5. Parse, verify and refresh WSDL')

            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
            self.wait_jquery()

            expected_log_msg = EDIT_WSDL
            self.log('SERVICE_09 6. System logs the event "{0}" to the audit log'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

        # UC SERVICE_19 Edit the Address of a Service
        self.log('SERVICE_19 Edit the Address of a Service')

        wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_correct_url)

        self.log('Check wsdl services parameters')
        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        if check_edit_errors:
            service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_index=wsdl_index,
                                                                              service_name=service_2_name)
            check_wsdl_service_parameters(self, service_row, service_2_name, service_2_url)

        # UC SERVICE_19 1. Select to edit the address of a service.
        self.log('SERVICE_19 1. Select to edit the address of a service.')
        service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_index=wsdl_index,
                                                                          service_name=service_name)
        check_wsdl_service_parameters(self, service_row, service_name, service_url)

        # Click on the service row to select it
        self.click(service_row)

        # Click the "Edit" button to open "Edit Service Parameters" popup
        edit_wsdl_button.click()

        # Wait until "Edit Service Parameters" popup opens
        self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_XPATH)

        # Find the "Service URL" and "Timeout" inputs. Get the service URL and timeout as we need them later.
        service_url_input = self.by_id(popups.EDIT_SERVICE_POPUP_URL_ID)
        service_url_input_value = service_url_input.get_attribute('value')
        service_timeout = self.by_id(popups.EDIT_SERVICE_POPUP_TIMEOUT_ID).get_attribute('value')

        self.log('Replace url with https version')
        wsdl_correct_url_https = wsdl_correct_url.replace('http:', 'https:')
        self.input(service_url_input, wsdl_correct_url_https)
        self.log('SERVICE_19 5. System sets the TLS certification verification to "true" when url starts with https')
        service_tls_checkbox = self.by_xpath(popups.EDIT_SERVICE_POPUP_TLS_ENABLED_XPATH)
        self.is_equal('true', service_tls_checkbox.get_attribute('checked'))
        self.log('Click OK')
        self.by_xpath(popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
        self.log('Click on edit button again')
        edit_wsdl_button.click()
        self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_XPATH)
        self.log('Replace url with http version')
        self.input(service_url_input, wsdl_correct_url)
        self.log('SERVICE_19 5a. System sets the TLS certification verification to "false" when url starts with http')
        self.is_false(self.by_id(popups.EDIT_SERVICE_POPUP_TLS_ID).is_enabled())
        # Check service timeout value
        self.is_equal(con1=ss_system_parameters.SERVICE_TIMEOUT_VALUE, con2=service_timeout,
                      msg='Service timeout not {0}'.format(service_timeout))

        modified_service_url = service_url_input_value

        if check_parameter_errors:
            '''Append URL parameter db=CLIENT_CODE to the url'''
            '''Let's be ready that the service may already have some parameters 
               so check if a question mark exists or not.'''
            if '?' in modified_service_url:
                '''We already have parameters, append to the list'''
                modified_service_url += '&'
            else:
                '''No parameters, start a parameter string with a question mark'''
                modified_service_url += '?'

            modified_service_url += urllib.urlencode({service_url_additional_parameter: client['code']})
            current_log_lines = log_checker.get_line_count()
            self.log('SERVICE_19 4a. Invalid URL is inserted')
            warning, error = edit_service(self, service_invalid_url, service_timeout)
            expected_error_msg = SERVICE_EDIT_INVALID_URL.format(service_invalid_url)
            self.log('SERVICE_19 4a.1 System displays the error message "{0}"'.format(expected_error_msg))
            self.is_equal(expected_error_msg, error)
            self.is_none(warning,
                         msg='Set invalid service URL: got warning for URL {0} : {1}'
                         .format(modified_service_url, warning))
            expected_log_msg = EDIT_SERVICE_PARAMS_FAILED
            self.log('SERVICE_19 4a.2. System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found)
            self.log('Close error messages')
            messages.close_error_messages(self)

            self.log('SERVICE_21 4b. The inserted timeout value is not a positive integer')
            for timeout in service_invalid_timeouts:
                current_log_lines = log_checker.get_line_count()
                self.log('Trying to set timeout to {0}'.format(timeout))
                warning, error = edit_service(self, modified_service_url, timeout)
                expected_error_msg = SERVICE_EDIT_INVALID_TIMEOUT.format(timeout)
                self.log('SERVICE_21 4b.1 System displays the error message "{0}"'.format(expected_error_msg))
                self.is_equal(expected_error_msg, error)
                self.is_none(warning,
                             msg='Set invalid service URL: got warning for timeout {0} : {1}'
                             .format(timeout, warning))
                expected_log_msg = EDIT_SERVICE_PARAMS_FAILED
                self.log('SERVICE_21 4b.2 System logs the event "{0}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
                self.log('Close error messages if present')
                messages.close_error_messages(self)

            self.log('SERVICE_21 4a. edit the timeout value to infinity {0})'.format(service_infinite_timeout))
            warning, error = edit_service(self, modified_service_url, service_infinite_timeout)
            self.is_none(error, msg='Set infinite service timeout: got error for timeout {0}'.format(
                service_infinite_timeout))
            expected_warning_message = messages.SERVICE_EDIT_INFINITE_TIMEOUT_WARNING.format(service_infinite_timeout)
            self.log('SERVICE_21 4a.1 System displays a warning message "{0}"'.format(expected_warning_message))
            self.is_equal(expected_warning_message, warning)
            self.log('Close error messages if present')
            messages.close_error_messages(self)
            self.log('SERVICE_21 4a.2a. Set infinite service timeout confirmation is canceled')
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CANCEL_XPATH).click()
            self.wait_jquery()

        # Try to set modified service URL and original service timeout. Should get no errors or warnings.
        self.log('Trying to set service timeout {1}, URL {0}'.format(modified_service_url, service_timeout))
        warning, error = edit_service(self, modified_service_url, service_timeout)
        self.is_none(error,
                     msg='Edit service: got error for timeout {1}, URL {0}'
                     .format(modified_service_url, service_timeout))
        self.is_none(warning,
                     msg='Edit service: got warning for timeout {2}, URL {0} : {1}'
                     .format(modified_service_url, warning, service_timeout))
        # If any error messages are shown, close them.
        messages.close_error_messages(self)

    return configure_service


def check_wsdl_service_parameters(self, service_row, service_name, service_url):
    """
    Checks if service parameters match the WSDL file provided ones
    :param self: main instance
    :param service_row: service row selenium element
    :param service_name: service name with version
    :param service_url:  service url
    :return:
    """
    service_cols = service_row.find_elements_by_tag_name('td')
    self.is_equal(service_cols[1].text[:-4], service_name, msg='Expecting WSDL service name "{0}", got "{1}"'.
                  format(service_name, service_cols[1].text[:-4]))
    self.is_equal(service_cols[2].text, service_name[:-3],
                  msg='Expecting WSDL service version "{0}", got "{1}"'.format(service_name[:-3], service_cols[2].text))
    self.is_equal(service_cols[3].text, service_url,
                  msg='Expecting WSDL service URL "{0}", got "{1}"'.format(service_url, service_cols[3].text))


def test_enable_service(case, client=None, client_name=None, client_id=None, wsdl_index=None, wsdl_url=None):
    '''
    MainController test function. Enables a service.
    :return:
    '''

    self = case
    client_id = xroad.get_xroad_subsystem(client)

    def enable_service():
        """
        :param self: MainController class object
        :return: None
        ''"""

        # UC SERVICE_12 Enable a WSDL
        self.log('SERVICE_12 Enable a WSDL')

        # UC SERVICE_12 1. Select to enable a WSDL
        self.log('SERVICE_12 1. Select to enable a WSDL')

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        # Find the table that lists all WSDL files and services
        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        # Wait until that table is visible (opened in a popup)
        self.wait_until_visible(services_table)

        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index, wsdl_url=wsdl_url)

        # Find and click the "Enable" button to enable the WSDL.
        self.by_id(popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()

        # Wait until ajax query finishes
        self.wait_jquery()

        # Check if WSDL is really enabled - find the WSDL row by index and
        if wsdl_url is not None:
            wsdl_enabled_index = clients_table_vm.find_wsdl_by_name(self, wsdl_url)
        else:
            wsdl_enabled_index = wsdl_index

        if wsdl_enabled_index is None:
            raise RuntimeError('WSDL index not found for {0}'.format(wsdl_url))

        # UC SERVICE_12 2. Check if WSDL is enabled
        self.log('SERVICE_12 2. Check if WSDL is enabled')

        # Find the WSDL row and check if it has class 'disabled'. If it does, it is not enabled. If not, everything worked.
        wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_enabled_index)
        wsdl_is_enabled = 'disabled' not in self.get_classes(wsdl_row)

        # Assertion if wsdl is enabled
        self.is_true(wsdl_is_enabled,
                     msg='SERVICE_12 2. WSDL {0} ({1}) is not enabled'.format(wsdl_enabled_index, wsdl_row.text))

    return enable_service


def test_delete_service(case, client=None, client_name=None, client_id=None, wsdl_index=None, wsdl_url=None,
                        try_cancel=True, log_checker=None):
    '''
    MainController test function. Deletes a service from security server.
    :param case: TestCase object
    :param client_name: string | None - name of the client whose ACL we modify
    :param client_id: string | None - XRoad ID of the client whose ACL we modify
    :param wsdl_index: int | None - index (zero-based) for WSDL we select from the list
    :param wsdl_url: str | None - URL for WSDL we select from the list
    :param client | None - client which service will be deleted
    :param try_cancel | True - tries canceling deletion if True
    :param log_checker | None - checks log for deletion if present
    :return:
    '''

    self = case
    if client is not None:
        client_id = xroad.get_xroad_subsystem(client)

    def delete_service():
        """
        :param self: MainController class object
        :return: None
        ''"""

        self.log('SERVICE_15 Delete service')
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()

        '''Open client popup using shortcut button to open it directly at Services tab.'''
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        '''Find the table that lists all WSDL files and services'''
        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        '''Wait until that table is visible (opened in a popup)'''
        self.wait_until_visible(services_table)
        self.wait_jquery()
        time.sleep(3)
        '''Find the service under the specified WSDL in service list 
        (and expand the WSDL services list if not open yet)'''''
        wsdl_element = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index,
                                                                          wsdl_url=wsdl_url)

        '''Get the WSDL URL from wsdl_element text'''
        if wsdl_url is None:
            wsdl_text = wsdl_element.find_elements_by_tag_name('td')[1].text

            matches = re.search(popups.CLIENT_DETAILS_POPUP_WSDL_URL_REGEX, wsdl_text)
            wsdl_found_url = matches.group(2)

            self.log('Found WSDL URL: {0}'.format(wsdl_found_url))
        else:
            wsdl_found_url = wsdl_url

        '''Find and click the "Delete" button to delete the WSDL.'''
        self.by_id(popups.CLIENT_DETAILS_POPUP_DELETE_WSDL_BTN_ID).click()

        if try_cancel:
            '''UC SERVICE 15 3a. When terminating deletion, the WSDL service remains
            A confirmation dialog should open. Cancel the deletion.'''
            self.log("UC SERVICE 15 3a. When terminating deletion, the WSDL service remains")
            self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            '''Find the wsdl element again'''
            wsdl_element = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index,
                                                                              wsdl_url=wsdl_url)
            '''Select the WSDL again'''
            wsdl_element.click()
            '''Click "Delete" button to delete the WSDL'''
            self.by_id(popups.CLIENT_DETAILS_POPUP_DELETE_WSDL_BTN_ID).click()

        '''A confirmation dialog should open. Confirm the deletion.'''
        popups.confirm_dialog_click(self)

        '''Wait until ajax query finishes'''
        self.wait_jquery()

        '''Now check if we can find the same wsdl or not'''
        wsdl_found_index = clients_table_vm.find_wsdl_by_name(self, wsdl_found_url)
        self.is_none(wsdl_found_index, msg='WSDL {0} was not deleted.'
                     .format(wsdl_found_url))

        if log_checker is not None:
            expected_log_msg = DELETE_WSDL
            self.log('SERVICE_15 5. System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

    return delete_service


def view_services(self, client, client_name, wsdl_url):
    def view_service():
        self.log('SERVICE_07 1. View security server client\'s services')
        clients_table_vm.open_client_popup_services(self, client=client, client_name=client_name)
        self.log('Expanding wsdl services')
        wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_url)
        wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_index)
        wsdl_row.find_element_by_css_selector(
            popups.CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS).click()

        self.log('SERVICE_07 2. System displays the services')
        services = self.wait_until_visible(type=By.CLASS_NAME, element=SERVICE_CLASS_NAME, multiple=True)
        for service in services:
            service.click()
            self.log('SERVICE_07 2. "Edit" button is visible')
            self.is_not_none(self.wait_until_visible(type=By.ID, element=EDIT_WSDL_BUTTON_ID))
            self.log('SERVICE_07 2. "Access Rights" button is visible')
            self.is_not_none(self.wait_until_visible(type=By.ID, element=CLIENT_DETAILS_POPUP_ACCESS_RIGHTS_BTN_ID))
            tds = service.find_elements_by_tag_name('td')
            self.log('SERVICE_07 2. The code and the version of the service is visible(formatted as "code.version")')
            self.is_true(re.match(WSDL_SERVICE_CODE_REGEX, tds[1].text))
            self.log('SERVICE_07 2. The title of the service is visible')
            self.is_true(len(tds[2].text) > 0)
            self.log('SERVICE_07 2. The connection type for accessing the service is visible')
            self.is_not_none(tds[3].find_element_by_tag_name('i'))
            self.log('SERVICE_07 2. The url of the service is visible and starts with http or https')
            self.is_true(re.match(WSDL_SERVICE_URL_REGEX, tds[3].text))
            self.log('SERVICE_07 2. The timeout of the service is visible and is integer')
            self.is_true(re.match(WSDL_SERVICE_TIMEOUT_REGEX, tds[4].text))
            self.log('SERVICE_07 2. The date of the service WSDL refresh date is visible')
            self.is_true(re.match(WSDL_SERVICE_CODE_DATE_REGEX, tds[5].text))

    return view_service


def view_service_access_rights(self, client, client_name, wsdl_url):
    def view_service_access_right():
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client=client, client_name=client_name)
        self.log('Expanding service wsdl-s')
        wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_url)
        wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_index)
        wsdl_row.find_element_by_css_selector(
            popups.CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS).click()

        self.log('Get wsdl service rows')
        services = self.wait_until_visible(type=By.CLASS_NAME, element=SERVICE_CLASS_NAME, multiple=True)
        for service in services:
            service.click()
            self.log('SERVICE_16 1. View security server client\'s services')
            self.wait_until_visible(type=By.ID, element=CLIENT_DETAILS_POPUP_ACCESS_RIGHTS_BTN_ID).click()
            access_rights_table_rows = self.wait_until_visible(type=By.CSS_SELECTOR,
                                                               element=CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_FIRST_SUBJECT_ROW_CSS,
                                                               multiple=True)
            self.log('SERVICE_16 2. System displays the list of service clients '
                     'that have been given access rights to the service.')
            for member in access_rights_table_rows:
                self.log('Get member row columns')
                tds = member.find_elements_by_tag_name('td')
                self.log('SERVICE_16 2. The name of the X-Road member is visible')
                self.is_true(len(tds[0].text) > 0)
                self.log('SERVICE_16 2. The X-Road identifier is visible')
                self.is_true(re.match(XROAD_IDENTIFIER_REGEX, tds[1].text))
                self.log('SERVICE_16 2. The date of when the access right to the service was granted is visible')
                self.is_true(re.match(WSDL_SERVICE_CODE_DATE_REGEX, tds[2].text))
                self.log('SERVICE_16 2. "Add subjects" button is visible')
                self.is_not_none(self.by_id(CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_ADD_SUBJECTS_BTN_CSS))
                self.log('SERVICE_16 2. "Remove selected" button is visible')
                self.is_not_none(self.by_id(CLIENT_DETAILS_POPUP_ACL_SUBJECTS_REMOVE_SELECTED_BTN_ID))
                self.log('SERVICE_16 2. "Remove all" button is visible')
                self.is_not_none(self.by_id(CLIENT_DETAILS_POPUP_ACL_SUBJECTS_REMOVE_ALL_BTN_ID))
                self.log('Close access rights popup')
                popups.close_all_open_dialogs(self, limit=1)

    return view_service_access_right
