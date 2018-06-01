# coding=utf-8

import time

from selenium.webdriver.common.by import By

from helpers import xroad, auditchecker, ssh_server_actions
from view_models import clients_table_vm, popups, messages
from view_models.log_constants import EDIT_WSDL_FAILED, EDIT_WSDL
from view_models.messages import WSDL_EDIT_ERROR_WSDL_EXISTS, WSDL_EDIT_ERROR_VALIDATION_FAILED, \
    WSDL_EDIT_ERROR_FILE_DOES_NOT_EXIST
from view_models.popups import EDIT_WSDL_POPUP_CANCEL_BTN_XPATH, CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID
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
                           check_parameter_errors=True, wsdl_url=None, wsdl_index=None, wsdl_test_service=None):
    '''
    MainController test function. Configures a new service.
    '''

    self = case

    ss2_ssh_host = self.config.get('ss2.ssh_host')
    ss2_ssh_user = self.config.get('ss2.ssh_user')
    ss2_ssh_pass = self.config.get('ss2.ssh_pass')
    wsdl_ssh_host = self.config.get('wsdl.ssh_host')
    wsdl_ssh_user = self.config.get('wsdl.ssh_user')
    wsdl_ssh_pass = self.config.get('wsdl.ssh_pass')

    wsdl_correct_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl'))  # Correct URL that returns a WSDL file

    #wsdl_test_service = self.config.get('wsdl.service_wsdl_test_service1')
    wsdl_single_service = self.config.get('wsdl.service_single_service_filename')

    wsdl_test_service_url = self.config.get('wsdl.remote_path').format(wsdl_test_service)

    wsdl_error_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_error_filename'))  # WSDL that cannot be validated

    wsdl_warning_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_warning_filename'))  # WSDL that gives a validator warning

    wsdl_local_path = self.config.get('wsdl.local_path')
    target_wsdl_path = wsdl_local_path.format(wsdl_test_service)

    client_id = xroad.get_xroad_subsystem(client)

    def configure_service():
        log_checker = auditchecker.AuditChecker(host=ss2_ssh_host, username=ss2_ssh_user, password=ss2_ssh_pass)

        if check_edit_errors:

            # Open client popup using shortcut button to open it directly at Services tab.
            clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

            # Find the table that lists all WSDL files and services
            services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
            # Wait until that table is visible (opened in a popup)
            self.wait_until_visible(services_table)
            wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_warning_url)

            # # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
            clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index, wsdl_url=wsdl_url)

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
            time.sleep(10)
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

    return configure_service
