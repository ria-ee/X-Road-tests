# coding=utf-8
import time
from selenium.webdriver.common.by import By
from helpers import xroad, auditchecker
from view_models import clients_table_vm, popups, messages, log_constants
from view_models.log_constants import ADD_WSDL_FAILED
from view_models.messages import WSDL_ERROR_ADDRESS_EXISTS, WSDL_ERROR_DUPLICATE_SERVICE, WSDL_ERROR_VALIDATION_FAILED
from view_models import ss_system_parameters


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

    wsdl_incorrect_url = self.config.get_string('wsdl.incorrect_url',
                                                'incorrect url')  # URL that doesn't start with http or https
    wsdl_malformed_url = self.config.get_string('wsdl.malformed_url', self.config.get('wsdl.remote_path').format(
        ''))  # URL that doesn't return a WSDL
    wsdl_correct_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl'))  # Correct URL that returns a WSDL file

    wsdl_test_service = self.config.get('wsdl.service_wsdl_test_service1')

    wsdl_duplicate_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.duplicate_service_wsdl'))  # Contains the same service as wsdl_correct_url

    wsdl_error_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_error_filename'))  # WSDL that cannot be validated

    wsdl_warning_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_warning_filename'))  # WSDL that gives a validator warning

    wsdl_disabled_prefix = self.config.get_string('wsdl.disabled_prefix', 'WSDL DISABLED')
    wsdl_disabled_class = self.config.get_string('wsdl.disabled_class', 'disabled')

    wsdl_local_path = self.config.get('wsdl.local_path')

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
        self.log('SERVICE_08 3-7. Add (unique) WSDL with URL: {0}'.format(wsdl_correct_url))

        current_log_lines = log_checker.get_line_count()

        warning, error, console = add_wsdl(self, wsdl_correct_url)
        self.log('SERVICE_08 10. System logs the event “Add WSDL” to the audit log.')
        logs_found = log_checker.check_log(log_constants.ADD_WSDL, from_line=current_log_lines + 1)
        self.is_true(logs_found)

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
        '''Find service'''
        service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_index=wsdl_index,
                                                                          service_name=service_name)

        # Click on the service row to select it
        self.click(service_row)
        edit_wsdl_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)

        # Click the "Edit" button to open "Edit Service Parameters" popup
        edit_wsdl_button.click()

        # Wait until "Edit Service Parameters" popup opens
        self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_XPATH)

        # Find the "Service URL" and "Timeout" inputs. Get the service URL and timeout as we need them later.
        service_url_input = self.by_id(popups.EDIT_SERVICE_POPUP_URL_ID)
        service_timeout = self.by_id(popups.EDIT_SERVICE_POPUP_TIMEOUT_ID).get_attribute('value')

        self.is_false(self.by_id(popups.EDIT_SERVICE_POPUP_TLS_ID).is_enabled())
        '''Verify service timeout value'''
        self.is_equal(ss_system_parameters.SERVICE_TIMEOUT_VALUE, service_timeout,
                      msg='Service timeout not {0}'.format(ss_system_parameters.SERVICE_TIMEOUT_VALUE))

    return configure_service
