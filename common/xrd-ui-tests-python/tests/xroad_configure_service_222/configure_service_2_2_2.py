# coding=utf-8

import re
import time
import urllib

from selenium.webdriver.common.by import By

from helpers import xroad
from view_models import clients_table_vm, popups, messages, ss_system_parameters


def add_wsdl(self,
             wsdl_url, clear_field=True):
    '''
    Tries to enter WSDL url to "Add WSDL" URL input field and click "OK"
    :param self:
    :param url: str - URL that contains the WSDL
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
        # service_timeout_input.clear()
        # service_timeout_input.send_keys(service_timeout)
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


def test_configure_service(case, client=None, client_name=None, client_id=None, service_name=None,
                           check_add_errors=True,
                           check_edit_errors=True, check_parameter_errors=True):
    '''
    MainController test function. Configures a new service.
    '''

    self = case

    ss2_host = self.config.get('ss2.host')
    ss2_user = self.config.get('ss2.user')
    ss2_pass = self.config.get('ss2.pass')

    wsdl_incorrect_url = self.config.get_string('wsdl.incorrect_url',
                                                'incorrect url')  # URL that doesn't start with http or https
    wsdl_malformed_url = self.config.get_string('wsdl.malformed_url', self.config.get('wsdl.remote_path').format(
        ''))  # URL that doesn't return a WSDL
    wsdl_correct_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl'))  # Correct URL that returns a WSDL file

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

    client_id = xroad.get_xroad_subsystem(client)

    def configure_service():
        """
        :param self: MainController class object
        :return: None
        ''"""

        # TEST PLAN 2.2.2 configure test service
        self.log('*** 2.2.2 / XT-466')

        self.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)

        # TEST PLAN 2.2.2-1 add test service WSDL
        self.log('2.2.2-1 add test service WSDL')

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
                     msg='WSDL {0} has already been added. Remove the service and try again.'
                     .format(wsdl_correct_url))

        if check_add_errors:
            # TEST PLAN 2.2.2.1 error 1 - trying to add WSDL with an incorrect URL
            self.log('2.2.2.1 error 1 add WSDL with an incorrect URL: {0}'.format(wsdl_incorrect_url))
            warning, error, console = add_wsdl(self, wsdl_incorrect_url)
            self.is_not_none(error, msg='Incorrect URL: no error shown for WSDL {0}'.format(wsdl_incorrect_url))
            self.is_equal(error, messages.WSDL_ERROR_INVALID_URL.format(wsdl_incorrect_url),
                          msg='Incorrect URL: wrong error shown for WSDL {0} : {1}'
                          .format(wsdl_incorrect_url, error))
            self.is_none(warning, msg='Incorrect URL: got warning for WSDL {0} : {1}'
                         .format(wsdl_incorrect_url, warning))
            self.is_none(console, msg='Incorrect URL: got console output for WSDL {0} : {1}'
                         .format(wsdl_incorrect_url, console))
            self.log('Error message: {0}'.format(warning))

            # TEST PLAN 2.2.2.1 error 2 - trying to add WSDL with a URL that doesn't return a WSDL file
            self.log(
                '2.2.2.1 error 2 add WSDL with a URL that doesn''t return a WSDL file: {0}'.format(wsdl_malformed_url))
            warning, error, console = add_wsdl(self, wsdl_malformed_url)
            self.is_not_none(error, msg='Add duplicate WSDL: no error shown for WSDL {0}'.format(wsdl_malformed_url))
            self.is_equal(error, messages.WSDL_ERROR_INCORRECT_WSDL.format(wsdl_malformed_url),
                          msg='Incorrect WSDL: wrong error shown for WSDL {0} : {1}'
                          .format(wsdl_malformed_url, error))
            self.is_none(warning, msg='Incorrect WSDL: got warning for WSDL {0} : {1}'
                         .format(wsdl_malformed_url, warning))
            self.is_none(console, msg='Incorrect WSDL: got console output for WSDL {0} : {1}'
                         .format(wsdl_malformed_url, console))
            self.log('Error message: {0}'.format(warning))

            # TEST PLAN 2.2.2.1 error 3 - trying to add a WSDL with a URL that has already been added

        # TEST PLAN 2.2.2-1 - First let's add the unique WSDL and it should succeed. (Validation comes later)
        self.log('2.2.2-1 add (unique) WSDL with URL: {0}'.format(wsdl_correct_url))
        warning, error, console = add_wsdl(self, wsdl_correct_url)
        self.is_none(error, msg='Add unique WSDL: got error for WSDL {0} : {1}'.format(wsdl_correct_url, error))
        self.is_none(warning,
                     msg='Add unique WSDL: got warning for WSDL {0} : {1}'.format(wsdl_correct_url, warning))
        self.is_none(console,
                     msg='Add unique WSDL: got console output for WSDL {0} : {1}'.format(wsdl_correct_url,
                                                                                         console))

        if check_add_errors:
            # TEST PLAN 2.2.2.1 error 3 - trying to add a WSDL with a URL that has already been added

            # Second, the same WSDL file. We should get an error.
            self.log('2.2.2.1 error 3 add a WSDL with a URL that has already been added: {0}'.format(wsdl_correct_url))
            warning, error, console = add_wsdl(self, wsdl_correct_url)  # This should give an error
            self.is_not_none(error, msg='Add duplicate WSDL: no error shown for WSDL {0}'.format(wsdl_correct_url))
            self.is_equal(error, messages.WSDL_ERROR_ADDRESS_EXISTS.format(wsdl_correct_url),
                          msg='Add duplicate WSDL: wrong error shown for WSDL {0} : {1}'.format(wsdl_correct_url,
                                                                                                error))
            self.is_none(warning, msg='Add duplicate WSDL: got warning for WSDL {0} : {1}'
                         .format(wsdl_correct_url, warning))
            self.is_none(console, msg='Add duplicate WSDL: got console output for WSDL {0} : {1}'
                         .format(wsdl_correct_url, console))
            self.log('Error message: {0}'.format(warning))

            # TEST PLAN 2.2.2.1 error 4 - trying to add a WSDL that is a different URL but the service is already defined
            self.log(
                '2.2.2.1 error 4 add a WSDL that is a different URL but the service is already defined: {0}'.format(
                    wsdl_duplicate_url))
            warning, error, console = add_wsdl(self,
                                               wsdl_duplicate_url)  # This should give an error about duplicate service
            error_message_is_correct = error.startswith(
                messages.WSDL_ERROR_DUPLICATE_SERVICE.format(wsdl_duplicate_url))
            self.is_not_none(error, msg='Add duplicate service: no error shown for WSDL {0}'.format(wsdl_duplicate_url))
            self.is_equal(error_message_is_correct, True,
                          msg='Add duplicate service: wrong error shown for WSDL {0} : {1}'.format(wsdl_duplicate_url,
                                                                                                   error))
            self.is_none(warning, msg='Add duplicate service: got warning for WSDL {0} : {1}'
                         .format(wsdl_duplicate_url, warning))
            self.is_none(console, msg='Add duplicate service: got console output for WSDL {0} : {1}'
                         .format(wsdl_duplicate_url, console))
            self.log('Error message: {0}'.format(warning))

            # TEST PLAN 2.2.2.1 error 5 - trying to add WSDL that cannot be validated at all
            self.log('2.2.2.1 error 5 add WSDL that cannot be validated at all: {0}'.format(wsdl_error_url))
            warning, error, console = add_wsdl(self, wsdl_error_url)
            self.is_not_none(error, msg='Add invalid WSDL: no error shown for WSDL {0}'.format(wsdl_error_url))
            self.is_equal(error, messages.WSDL_ERROR_VALIDATION_FAILED.format(wsdl_error_url),
                          msg='Add invalid WSDL: wrong error shown for WSDL {0} : {1}'.format(wsdl_error_url, error))
            self.is_none(warning, msg='Add invalid WSDL: got warning for WSDL {0} : {1}'
                         .format(wsdl_error_url, warning))
            self.is_not_none(console, msg='Add invalid WSDL: no console output shown for WSDL {0} : {1}'
                             .format(wsdl_error_url, console))
            self.log('Error message: {0}'.format(error))
            self.log('Console output: {0}'.format(console))

            # TEST PLAN 2.2.2.1 error 6 - trying to add WSDL that gives a validator warning
            self.log('2.2.2.1 error 6 add WSDL that gives a validator warning: {0}'.format(wsdl_warning_url))
            warning, error, console = add_wsdl(self, wsdl_warning_url)
            self.is_none(error,
                         msg='Add WSDL with validator warnings: got error for WSDL {0}'.format(wsdl_warning_url))
            self.is_not_none(warning, msg='Add WSDL with validator warnings: no warning shown for WSDL {0} : {1}'
                             .format(wsdl_warning_url, warning))
            self.is_none(console, msg='Add WSDL with validator warnings: got console output for WSDL {0} : {1}'
                         .format(wsdl_warning_url, console))
            self.log('Warning message: {0}'.format(warning))

            # We're not adding the WSDL that gives us warnings, so find the "Cancel" button and click it.
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CANCEL_XPATH).click()
            self.wait_jquery()

            # Now we need to cancel the "Add WSDL" popup. Find the "Cancel" button and click it.
            self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_CANCEL_BTN_XPATH).click()

        # TEST PLAN 2.2.2-1 VALIDATION - Check if our unique WSDL has been successfully added
        self.log('2.2.2-1 validation - checking if WSDL was added: {0}'.format(wsdl_correct_url))

        wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_correct_url)
        self.log('WSDL table row index: {0}'.format(wsdl_index))

        # Check if wsdl_index is not None - if it is, we didn't find the WSDL in the list after adding it.
        self.is_not_none(wsdl_index,
                         msg='WSDL not found in services table after adding: {0}'.format(wsdl_correct_url))

        # Get the WSDL tr (table row) element from services table
        wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_index)

        # TEST PLAN 2.2.2.1 subtask - verify that the row starts with "WSDL DISABLED" and is in red letter (we're
        # checking if the class is "disabled" - this sets the color)

        # Get the service code td (table cell) element (this should start with WSDL DISABLED)
        wsdl_service_code = wsdl_row.find_elements_by_tag_name('td')[1]
        self.is_equal(wsdl_service_code.text.startswith(wsdl_disabled_prefix), True,
                      msg='Added WSDL row does not start with "WSDL DISABLED": {0}'.format(wsdl_correct_url))

        # Get the row classes to check if "disabled" is in this list. This is the class that makes the row text red.
        wsdl_row_classes = self.get_classes(wsdl_row)
        self.is_equal(wsdl_disabled_class in wsdl_row_classes, True,
                      msg='Added WSDL row does not have class "disabled": {0}'.format(wsdl_correct_url))

        # Select the WSDL by clicking on the row
        wsdl_row.click()

        # UC SERVICE_08 8. check if default disable message is correct
        # enable and disable WSDL to get disable message popup
        self.log('UC SERVICE 08 8. check if default disable message is correct')
        self.by_id(popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()
        self.wait_jquery()
        self.by_id(popups.CLIENT_DETAILS_POPUP_DISABLE_WSDL_BTN_ID).click()
        self.wait_jquery()
        disabled_message = self.by_id(popups.DISABLE_WSDL_POPUP_NOTICE_ID).get_attribute('value')
        # check disable message value
        self.is_equal(messages.SERVICE_DISABLED_MESSAGE, disabled_message,
                      msg='Disable message not equal to {0}'.format(messages.SERVICE_DISABLED_MESSAGE))
        # confirm disable message
        self.by_xpath(popups.DISABLE_WSDL_POPUP_OK_BTN_XPATH).click()

        # Open service parameters by finding the "Edit" button and clicking it.
        edit_wsdl_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)

        if check_edit_errors:
            edit_wsdl_button.click()

            # TEST PLAN 2.2.2.2 error 1 - trying to add WSDL that cannot be validated at all
            self.log(
                '2.2.2.2 error 1 trying to set WSDL URL that cannot be validated at all: {0}'.format(wsdl_error_url))
            warning, error, console = edit_wsdl(self, wsdl_error_url)
            self.is_not_none(error, msg='Set invalid WSDL: no error shown for WSDL {0}'.format(wsdl_error_url))
            self.is_equal(error, messages.WSDL_EDIT_ERROR_VALIDATION_FAILED.format(wsdl_error_url),
                          msg='Set invalid WSDL: wrong error shown for WSDL {0} : {1}'.format(wsdl_error_url, error))
            self.is_none(warning, msg='Set invalid WSDL: got warning for WSDL {0} : {1}'
                         .format(wsdl_error_url, warning))
            self.is_not_none(console, msg='Set invalid WSDL: no console output shown for WSDL {0} : {1}'
                             .format(wsdl_error_url, console))
            self.log('Error message: {0}'.format(error))
            self.log('Console output: {0}'.format(console))

            # TEST PLAN 2.2.2.2 error 2 - trying to update WSDL that gives a validator warning
            self.log(
                '2.2.2.2 error 2 trying to set WSDL URL that gives a validator warning: {0}'.format(wsdl_warning_url))
            warning, error, console = edit_wsdl(self, wsdl_warning_url)
            self.is_none(error,
                         msg='Set WSDL with validator warnings: got error for WSDL {0}'.format(wsdl_warning_url))
            self.is_not_none(warning, msg='Set WSDL with validator warnings: no warning shown for WSDL {0} : {1}'
                             .format(wsdl_warning_url, warning))
            self.is_none(console, msg='Set WSDL with validator warnings: got console output for WSDL {0} : {1}'
                         .format(wsdl_warning_url, console))
            self.log('Warning message: {0}'.format(warning))

            # We're not adding the WSDL that gives us warnings, so find the "Cancel" button and click it.
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CANCEL_XPATH).click()
            self.wait_jquery()

            # Close "Edit WSDL Parameters" dialog by finding the "Cancel" button and clicking it.
            self.wait_until_visible(type=By.XPATH, element=popups.EDIT_WSDL_POPUP_CANCEL_BTN_XPATH).click()

        # TEST PLAN 2.2.2-2 Editing service parameters
        self.log('2.2.2-2 Editing service parameters')

        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_index=wsdl_index,
                                                                          service_name=service_name)

        # Click on the service row to select it
        service_row.click()

        # Click the "Edit" button to open "Edit Service Parameters" popup
        edit_wsdl_button.click()

        # Wait until "Edit Service Parameters" popup opens
        self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_XPATH)

        # Find the "Service URL" and "Timeout" inputs. Get the service URL and timeout as we need them later.
        service_url_input = self.by_id(popups.EDIT_SERVICE_POPUP_URL_ID)
        service_url = service_url_input.get_attribute('value')
        service_timeout = self.by_id(popups.EDIT_SERVICE_POPUP_TIMEOUT_ID).get_attribute('value')

        # UC SERVICE 08 9. Check if default timeout value is correct and TLS checkbox checked when URL starts with https
        # Clear service url input
        self.log(
            'UC SERVICE 08 9. Check if default timeout value is correct and TLS checkbox checked when URL starts with https')
        service_url_input.clear()
        # Replace wsdl url http to https:
        wsdl_correct_url_https = wsdl_correct_url.replace('http:', 'https:')
        self.input(service_url_input, wsdl_correct_url_https)
        # Find TLS enabled checkbox
        service_tls_checkbox = self.by_xpath(popups.EDIT_SERVICE_POPUP_TLS_ENABLED_XPATH)
        # Check if checkbox is checked
        self.is_equal('true', service_tls_checkbox.get_attribute('checked'), msg="TLS checkbox not checked")
        # Clear service url input
        service_url_input.clear()
        # Replace service url back to http
        self.input(service_url_input, wsdl_correct_url)
        # Find TLS enabled checkbox
        service_tls_checkbox = self.by_id(popups.EDIT_SERVICE_POPUP_TLS_ID)
        # Check if checkbox is disabled
        self.is_false(service_tls_checkbox.is_enabled())
        # Check service timeout value
        self.is_equal(con1=ss_system_parameters.SERVICE_TIMEOUT_VALUE, con2=service_timeout,
                      msg='Service timeout not {0}'.format(service_timeout))

        modified_service_url = service_url

        if check_parameter_errors:
            # TEST PLAN 2.2.2.3 Test edit service parameters errors
            self.log('2.2.2.3 Test edit service parameters errors')

            # Append URL parameter db=CLIENT_CODE to the url

            # Let's be ready that the service may already have some parameters so check if a question mark exists or not.
            if '?' in modified_service_url:
                # We already have parameters, append to the list
                modified_service_url += '&'
            else:
                # No parameters, start a parameter string with a question mark
                modified_service_url += '?'

            # Append client code to service URL
            modified_service_url += urllib.urlencode({service_url_additional_parameter: client['code']})

            # TEST PLAN 2.2.2.3 error 1 Try to set invalid URL and original (correct) service timeout. Should get an error.
            self.log('2.2.2.3 error 1 trying to set invalid service URL {0}'.format(service_invalid_url))
            warning, error = edit_service(self, service_invalid_url, service_timeout)
            self.is_not_none(error,
                             msg='Set invalid service URL: no error shown for URL {0}'.format(service_invalid_url))
            self.is_equal(error, messages.SERVICE_EDIT_INVALID_URL.format(service_invalid_url),
                          msg='Set invalid service URL: wrong error shown for URL {0} : {1}'.format(service_invalid_url,
                                                                                                    error))
            self.is_none(warning,
                         msg='Set invalid service URL: got warning for URL {0} : {1}'
                         .format(modified_service_url, warning))
            # If any error messages are shown, close them.
            messages.close_error_messages(self)

            # TEST PLAN 2.2.2.3 error 2 Try to set invalid service timeout. Should get an error.
            for timeout in service_invalid_timeouts:
                self.log('2.2.2.3 error 2 Trying to set invalid timeout {0}'.format(timeout))
                warning, error = edit_service(self, modified_service_url, timeout)
                self.is_not_none(error, msg='Set invalid timeout: no error shown for timeout {0}'.format(timeout))
                self.is_equal(error, messages.SERVICE_EDIT_INVALID_TIMEOUT.format(timeout),
                              msg='Set invalid service URL: wrong error shown for timeout {0} : {1}'.format(timeout,
                                                                                                            error))
                self.is_none(warning,
                             msg='Set invalid service URL: got warning for timeout {0} : {1}'
                             .format(timeout, warning))
                # If any error messages are shown, close them.
                messages.close_error_messages(self)

            # TEST PLAN 2.2.2.3 error 3 Try to set infinite service timeout. Should get a warning.
            self.log('2.2.2.3 error 3 Trying to set infinite service timeout: {0}'.format(service_infinite_timeout))
            warning, error = edit_service(self, modified_service_url, service_infinite_timeout)
            self.is_none(error, msg='Set infinite service timeout: got error for timeout {0}'.format(
                service_infinite_timeout))
            self.is_not_none(warning,
                             msg='Set infinite service timeout: no warning for timeout {0}'.format(
                                 service_infinite_timeout))
            self.is_equal(warning, messages.SERVICE_EDIT_INFINITE_TIMEOUT_WARNING.format(service_infinite_timeout),
                          msg='Set infinite service timeout: wrong warning shown for timeout {0} : {1}'.format(
                              service_infinite_timeout, error))
            # If any error messages are shown, close them.
            messages.close_error_messages(self)

            # We're not saving the service with an infinite timeout, so find the "Cancel" button and click it.
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

        # TEST PLAN 2.2.2-4 - activate test service WSDL
        self.log('2.2.2-4 - activate test service WSDL')

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

        # Find the WSDL row and check if it has class 'disabled'. If it does, it is not enabled. If not, everything worked.
        wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_enabled_index)
        wsdl_is_enabled = 'disabled' not in self.get_classes(wsdl_row)

        # Assertion if wsdl is enabled
        self.is_true(wsdl_is_enabled, msg='WSDL {0} ({1}) is not enabled'.format(wsdl_enabled_index, wsdl_row.text))

    return enable_service


def test_delete_service(case, client=None, client_name=None, client_id=None, wsdl_index=None, wsdl_url=None):
    '''
    MainController test function. Deletes a service from security server.
    :param case: TestCase object
    :param client_name: string | None - name of the client whose ACL we modify
    :param client_id: string | None - XRoad ID of the client whose ACL we modify
    :param wsdl_index: int | None - index (zero-based) for WSDL we select from the list
    :param wsdl_url: str | None - URL for WSDL we select from the list
    :return:
    '''

    self = case
    client_id = xroad.get_xroad_subsystem(client)

    def delete_service():
        """
        :param self: MainController class object
        :return: None
        ''"""

        self.log('2.2.8 delete_service')

        # Delete WSDL that we added to restore original state.

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        # Find the table that lists all WSDL files and services
        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        # Wait until that table is visible (opened in a popup)
        self.wait_until_visible(services_table)
        self.wait_jquery()
        time.sleep(3)
        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        wsdl_element = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index,
                                                                          wsdl_url=wsdl_url)

        # Get the WSDL URL from wsdl_element text
        if wsdl_url is None:
            wsdl_text = wsdl_element.find_elements_by_tag_name('td')[1].text

            matches = re.search(popups.CLIENT_DETAILS_POPUP_WSDL_URL_REGEX, wsdl_text)
            wsdl_found_url = matches.group(2)

            self.log('Found WSDL URL: {0}'.format(wsdl_found_url))
        else:
            wsdl_found_url = wsdl_url

        # Find and click the "Delete" button to delete the WSDL.
        self.by_id(popups.CLIENT_DETAILS_POPUP_DELETE_WSDL_BTN_ID).click()

        # UC SERVICE 15 3a. When terminating deletion, the WSDL service remains
        # A confirmation dialog should open. Cancel the deletion.
        self.log("UC SERVICE 15 3a. When terminating deletion, the WSDL service remains")
        self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        # Find the wsdl element again
        wsdl_element = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index,
                                                                           wsdl_url=wsdl_url)
        # Select the WSDL again
        wsdl_element.click()
        # Click "Delete" button to delete the WSDL
        self.by_id(popups.CLIENT_DETAILS_POPUP_DELETE_WSDL_BTN_ID).click()
        # A confirmation dialog should open. Confirm the deletion.
        popups.confirm_dialog_click(self)

        # Wait until ajax query finishes
        self.wait_jquery()

        # Now check if we can find the same wsdl or not
        wsdl_found_index = clients_table_vm.find_wsdl_by_name(self, wsdl_found_url)
        self.is_none(wsdl_found_index, msg='WSDL {0} was not deleted.'
                     .format(wsdl_found_url))

    return delete_service
