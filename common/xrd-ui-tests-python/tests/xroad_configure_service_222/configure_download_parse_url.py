# coding=utf-8

import re
import time
from selenium.webdriver.common.by import By

from helpers import xroad, ssh_server_actions
from view_models import clients_table_vm, popups, messages

from view_models.messages import  WSDL_EDIT_ERROR_VALIDATION_FAILED, \
    WSDL_EDIT_ERROR_FILE_DOES_NOT_EXIST, WSDL_EDIT_INCORRECT_STRUCTURE
from view_models.popups import EDIT_WSDL_POPUP_CANCEL_BTN_XPATH, CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID, WSDL_SERVICE_CODE_DATE_REGEX

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
                           check_parameter_errors=True, wsdl_url=None, wsdl_index=None):
    '''
    MainController test function. Configures a new service.
    '''

    self = case

    wsdl_ssh_host = self.config.get('wsdl.ssh_host')
    wsdl_ssh_user = self.config.get('wsdl.ssh_user')
    wsdl_ssh_pass = self.config.get('wsdl.ssh_pass')

    wsdl_incorrect_url = self.config.get_string('wsdl.incorrect_url',
                                                'incorrect url')  # URL that doesn't start with http or https
    wsdl_test_service = self.config.get('wsdl.service_wsdl_test_service1')
    wsdl_single_service = self.config.get('wsdl.service_single_service_filename')
    wsdl_malformed_url = self.config.get_string('wsdl.malformed_url', self.config.get('wsdl.remote_path').format(
        ''))  # URL that doesn't return a WSDL
    wsdl_test_service_url = self.config.get('wsdl.remote_path').format(wsdl_test_service)

    wsdl_error_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_error_filename'))  # WSDL that cannot be validated

    wsdl_warning_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_warning_filename'))  # WSDL that gives a validator warning


    wsdl_local_path = self.config.get('wsdl.local_path')
    target_wsdl_path = wsdl_local_path.format(wsdl_test_service)

    client_id = xroad.get_xroad_subsystem(client)

    def configure_service():


        if check_edit_errors:

            # Open client popup using shortcut button to open it directly at Services tab.
            clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

            # Find the table that lists all WSDL files and services
            services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
            # Wait until that table is visible (opened in a popup)
            self.wait_until_visible(services_table)
            wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_warning_url)



            # UC SERVICE_10 (Download and Parse WSDL) checks
            self.log('SERVICE_10 checks')
            ssh_client = ssh_server_actions.get_client(wsdl_ssh_host, wsdl_ssh_user, wsdl_ssh_pass)
            self.log('Copy single wsdl file to test wsdl')
            ssh_server_actions.cp(ssh_client, wsdl_local_path.format(wsdl_single_service), target_wsdl_path)
            service_name_wo_version = service_name[:-3]
            self.log('Change {0} service to xroadTest123'.format(service_name_wo_version))
            ssh_client.exec_command(
                'sed -i -e "s/{0}/xroadTest123/g" {1}'.format(service_name_wo_version, target_wsdl_path),
                sudo=True)
            self.log('Add test wsdl to client')

            self.log('SERVICE_10 1a. The URL is malformed {0}'.format(wsdl_incorrect_url))
            warning, error, console = add_wsdl(self, wsdl_incorrect_url)
            self.is_not_none(error, msg='SERVICE_10 1a. Incorrect URL: no error shown for WSDL {0}'.format(
                wsdl_incorrect_url))
            self.is_equal(error, messages.WSDL_ERROR_INVALID_URL.format(wsdl_incorrect_url),
                          msg='SERVICE_10 1a. Incorrect URL: wrong error shown for WSDL {0} : {1}'
                          .format(wsdl_incorrect_url, error))
            add_wsdl(self, wsdl_test_service_url)

            time.sleep(10)

            # # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
            clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index, wsdl_url=wsdl_test_service_url)
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

            self.log('SERVICE_10 3a. WSDL validation failed')
            self.log('Changing wsdl to wsdl which can\'t be validated')
            warning, error, console = edit_wsdl(self, wsdl_error_url)
            expected_error_msg = WSDL_EDIT_ERROR_VALIDATION_FAILED.format(wsdl_error_url)
            self.log('SERVICE_10 3a.1 System displays the error message "{0}"'.format(expected_error_msg))
            self.is_equal(expected_error_msg, error)
            self.is_not_none(console, msg='Set invalid WSDL: no console output shown for WSDL {0} : {1}'
                             .format(wsdl_error_url, console))

            # UC SERVICE_10 2b. Error 2 - trying to add WSDL with a URL that doesn't return a WSDL file
            self.log('SERVICE_10 2b. Error 2 add WSDL with a URL that doesn''t return a WSDL file: {0}'.format(
                    wsdl_malformed_url))
            warning, error, console = edit_wsdl(self, wsdl_malformed_url)

            self.is_not_none(error, msg='SERVICE_10  2b Incorrect WSDL: no error shown for WSDL {0}'.format(
                wsdl_malformed_url))
            self.is_equal(WSDL_EDIT_INCORRECT_STRUCTURE, error)


            '''Click "Cancel" button'''
            self.by_xpath(popups.EDIT_WSDL_POPUP_CANCEL_BTN_XPATH).click()

            '''Click on WSDL'''
            wsdl_element = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index,
                                                                              wsdl_url=wsdl_test_service_url)
            wsdl_element.click()
            '''Delete WSDL'''
            self.by_id(popups.CLIENT_DETAILS_POPUP_DELETE_WSDL_BTN_ID).click()

            '''A confirmation dialog should open. Confirm the deletion.'''
            popups.confirm_dialog_click(self)

    return configure_service

