import time

import requests
import urllib3

from helpers import ssh_client
from tests.xroad_configure_service_222 import configure_service
from tests.xroad_refresh_wsdl_225 import refresh_wsdl
from view_models import clients_table_vm, ss_system_parameters
from view_models.log_constants import ADD_WSDL_FAILED, REFRESH_WSDL_FAILED
from view_models.messages import WSDL_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE, \
    WSDL_ADD_ERROR_VALIDATOR_COMMAND_NOT_FOUND, WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_FOUND, \
    WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE, WSDL_ERROR_VALIDATION_FAILED

from selenium.webdriver.common.by import By

from helpers import xroad, auditchecker
from view_models import clients_table_vm, popups, messages

from view_models.messages import WSDL_ERROR_VALIDATION_FAILED


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


    wsdl_correct_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl'))  # Correct URL that returns a WSDL file


    wsdl_error_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_error_filename'))  # WSDL that cannot be validated

    wsdl_warning_url = self.config.get('wsdl.remote_path').format(
        self.config.get('wsdl.service_wsdl_warning_filename'))  # WSDL that gives a validator warning


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



        if check_add_errors:


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

    return configure_service


def test_wsdl_validator_crash(self, wsdl_url, ssh_host, ssh_username, ssh_password, ss_host, ss_user, ss_pass,
                              client_name, client_id, wsdl_validator_wrapper_path):
    def wsdl_validator_crash():
        self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
        self.log('Backing up wsdlvalidator wrapper')
        self.ssh_client.exec_command('cp -p {0} {0}.backup'.format(wsdl_validator_wrapper_path), sudo=True)
        self.log('Adding invalid argument(-asd) to wsdlvalidator_wrapper validator execution command')
        self.ssh_client.exec_command('sed -i -e "s/-r/-asd/g" {0}'.format(wsdl_validator_wrapper_path), sudo=True)
        self.ssh_client.close()

        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)
        self.log('Try to add wsdl')
        warning, error, console = configure_service.add_wsdl(self, wsdl_url=wsdl_url)
        expected_error_msg = WSDL_ERROR_VALIDATION_FAILED.format(wsdl_url)
        self.log('SERVICE_44 1c.1 System displays the error message "{0}"'.format(expected_error_msg))
        self.is_equal(expected_error_msg, error)
        self.log('Check if wsdl validation error popup contains expected strings')
        self.is_true("WSDLValidator Error" and "Unexpected argument" in console)

    return wsdl_validator_crash


def test_adding_wsdl_validator_not_set(self, wsdl_url, ss_host, ss_user, ss_pass, client_name, client_id, ssh_host,
                                       ssh_username, ssh_password):
    """
    SERVICE_08 6a The location of the WSDL validator is not set
    :param self: obj - mainController instance
    :param wsdl_url: str - wsdl url
    :param ss_host: str - security server host
    :param ss_user: str - security server user
    :param ss_pass: str - security server pass
    :param ssh_host: str - security server host
    :param ssh_username: str - security server user
    :param ssh_password: str - security server pass
    :param client_name: str - client name, whos wsdl will be used in test
    :param client_id: str - client id, whos wsdl will be used in test
    :return:
    """

    def test_success_no_wsdl_validator():
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        self.log('SERVICE_08 6a. Adding wsdl when wsdl validator is not set, wsdl will not be checked')
        warning, error, console = configure_service.add_wsdl(self, wsdl_url=wsdl_url)
        self.log('SERVICE_08 6a.1. System skips the process of validation: ')
        self.log('Checking if no issues occured, while adding service with warning')
        self.is_none(warning)
        self.is_none(error)
        self.is_none(console)
        self.log('Checking if wsdl is visible in services table')
        self.is_not_none(clients_table_vm.find_wsdl_by_name(self, wsdl_url))

    return test_success_no_wsdl_validator


def test_refreshing_wsdl_validator_not_set(self, wsdl_url, ss_host, ss_user, ss_pass, client_name, client_id):
    """
    SERVICE_14 3a The location of the WSDL validator is not set
    :param self: obj - mainController instance
    :param wsdl_url: str - wsdl url
    :param ss_host: str - security server host
    :param ss_user: str - security server user
    :param ss_pass: str - security server pass
    :param client_name: str - client name, whos wsdl will be used in test
    :param client_id: str - client id, whos wsdl will be used in test
    :return:
    """

    def test_refresh_success_no_validator():
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)
        clients_table_vm.client_services_popup_select_wsdl(self, wsdl_url=wsdl_url)
        self.log('Refresh added wsdl(wsdl with error)')
        warning, error, console = refresh_wsdl.refresh_wsdl(self)
        self.log('SERVICE_14 3a.1 System skips the process of validation')
        self.log('Check if wsdl was refreshed successfully')
        self.is_none(warning)
        self.is_none(error)
        self.is_none(console)

    return test_refresh_success_no_validator


def remove_wsdl_validator_from_conf(self, ssh_host, ssh_username, ssh_password, ss_host):
    '''Command to backup local.ini to local.ini.backup file'''
    backup_local_ini_command = 'cp -p {0} {1}'.format(ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION,
                                                   '/etc/xroad/conf.d/local.ini.backup')
    '''Command to create empty local.ini file'''
    create_empty_local_ini_command = 'sh -c "echo \'\' > {0}"'.format(
        ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION)
    self.log('Connecting ssh client')
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Creating backup from local.ini')
    self.ssh_client.exec_command(command=backup_local_ini_command, sudo=True)
    self.log('Create empty local.ini file, so WSDL parser path is not set')
    self.ssh_client.exec_command(command=create_empty_local_ini_command, sudo=True)

    self.log('Reload application config')
    self.ssh_client.exec_command(command=ss_system_parameters.RELOAD_APP_COMMAND, sudo=True)
    self.log('Waiting until server has fully reloaded')
    wait_until_server_up(ss_host)


def test_adding_wsdl_validator_invalid_command(self, ss_host,
                                               ss_user, ss_pass, log_checker,
                                               client_name, client_id, wsdl_warning_url):
    """
    SERVICE_08 6d The address of the WSDL validator program is incorrect and
    system was not able to run the validation program.
    :param self: obj - mainController instance
    :param wsdl_warning_url: str - wsdl with warning url
    :param ss_host: str - security server host
    :param ss_user: str - security server user
    :param ss_pass: str - security server pass
    :param log_checker: obj - auditchecker instance
    :param client_name: str - client name, whos wsdl will be used in test
    :param client_id: str - client id, whos wsdl will be used in test
    :return:
    """

    def test_wsdl_validator_invalid_command_validation():
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services table')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        current_log_lines = log_checker.get_line_count()
        self.log('Trying to add wsdl to client')
        warning, error, console = configure_service.add_wsdl(self, wsdl_url=wsdl_warning_url)
        expected_error_msg = WSDL_ADD_ERROR_VALIDATOR_COMMAND_NOT_FOUND
        self.log('SERVICE_08 6d.1 System displays the error message "{0}"'.format(expected_error_msg))
        self.is_equal(expected_error_msg, error)
        expected_log_msg = ADD_WSDL_FAILED
        self.log('SERVICE_08 6d.2 System logs the event "{0}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

    return test_wsdl_validator_invalid_command_validation


def test_refreshing_wsdl_validator_invalid_command(self, wsdl_url, ss_host,
                                                   ss_user, ss_pass, log_checker,
                                                   client_name, client_id):
    """
    SERVICE_14 3d The address of the WSDL validator program is incorrect and
    system was not able to run the validation program.
    :param self: obj - mainController instance
    :param wsdl_url: str - wsdl url
    :param ss_host: str - security server host
    :param ss_user: str - security server user
    :param ss_pass: str - security server pass
    :param log_checker: obj - auditchecker instance
    :param client_name: str - client name, whos wsdl will be used in test
    :param client_id: str - client id, whos wsdl will be used in test
    :return:
    """

    def refreshing_wsdl_invalid_validator():
        current_log_lines = log_checker.get_line_count()
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services table')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)
        self.log('Select wsdl which was added before')
        clients_table_vm.client_services_popup_select_wsdl(self, wsdl_url=wsdl_url)
        self.log('SERVICE_14 3d. The address of the WSDL validator program is incorrect and '
                 'system was not able to run the validation program.')
        self.log('Refreshing wsdl')
        warning, error, console = refresh_wsdl.refresh_wsdl(self)
        expected_error_msg = WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_FOUND
        self.log('SERVICE_14 3d.1 System displays the error message "{0}"'.format(expected_error_msg))
        self.is_equal(expected_error_msg, error)

        expected_log_msg = REFRESH_WSDL_FAILED
        self.log('SERVICE_14 3d.2 System logs the message message "{0}"'.format(expected_error_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

    return refreshing_wsdl_invalid_validator


def set_wsdl_validator_invalid_command(self, ssh_host, ssh_username, ssh_password, ss_host):
    '''Command to create local.ini with not existing command'''
    create_not_existing_wsdl_validator_path_local_ini_command = 'sh -c "echo \'{0}\' > {1}"'.format(
        '\n[proxy-ui]\nwsdl-validator-command=randasd', ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION)
    self.log('Connecting ssh client')
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Creating local.ini with non-existing wsdl-validator command')
    self.ssh_client.exec_command(command=create_not_existing_wsdl_validator_path_local_ini_command, sudo=True)
    self.log('Reload application')
    self.ssh_client.exec_command(command=ss_system_parameters.RELOAD_APP_COMMAND, sudo=True)
    self.log('Wait until server up again')
    wait_until_server_up(ss_host)


def test_adding_wsdl_validator_not_executable(self, wsdl_warning_url, ss_host,
                                              ss_user, ss_pass, log_checker,
                                              client_name, client_id):
    """
    SERVICE_08 6e The address of the WSDL validator refers to non-executable file and system
    was not able to run the validation program.
    :param self: obj - mainController instance
    :param wsdl_warning_url: str - wsdl with warning url
    :param ss_host: str - security server host
    :param ss_user: str - security server user
    :param ss_pass: str - security server pass
    :param log_checker: obj - auditchecker instance
    :param client_name: str - client name, whos wsdl will be used in test
    :param client_id: str - client id, whos wsdl will be used in test
    :return:
    """

    def adding_wsdl_validator_not_executable():
        current_log_lines = log_checker.get_line_count()
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        self.log('Try to add wsdl')
        warning, error, console = configure_service.add_wsdl(self, wsdl_url=wsdl_warning_url)
        expected_error_msg = WSDL_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE
        self.log('SERVICE_08 6e.1 System displays the error message "{0}"'.format(expected_error_msg))
        self.is_equal(expected_error_msg, error)
        expected_log_msg = ADD_WSDL_FAILED
        self.log('SERVICE_08 6e.2 System logs the event {0}'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

    return adding_wsdl_validator_not_executable


def test_refreshing_wsdl_validator_not_executable(self, wsdl_url, ss_host, ss_user, ss_pass, log_checker, client_name,
                                                  client_id):
    """
    SERVICE_14 3e The address of the WSDL validator refers to non-executable file and
    system was not able to run the validation program.
    :param self: obj - mainController instance
    :param wsdl_url: str - wsdl url
    :param ss_host: str - security server host
    :param ss_user: str - security server user
    :param ss_pass: str - security server pass
    :param log_checker: obj - auditchecker instance
    :param client_name: str - client name, whos wsdl will be used in test
    :param client_id: str - client id, whos wsdl will be used in test
    :return:
    """

    def refreshing_wsdl_validator_not_executable():
        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)
        self.log('Select WSDL from services')
        clients_table_vm.client_services_popup_select_wsdl(self, wsdl_url=wsdl_url)
        current_log_lines = log_checker.get_line_count()
        self.log('Refreshing wsdl')
        warning, error, console = refresh_wsdl.refresh_wsdl(self)
        expected_error_msg = WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE
        self.log('SERVICE_14 3e.1 System displays the error message "{0}"'.format(expected_error_msg))
        self.is_equal(expected_error_msg, error)
        expected_log_msg = REFRESH_WSDL_FAILED
        self.log('SERVICE_14 3e.2 System logs the event "{0}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

    return refreshing_wsdl_validator_not_executable


def set_wsdl_validator_not_executable(self, ssh_host, ssh_username, ssh_password, ss_host, not_exec_file_path):
    '''Command to create not executable file'''
    create_not_exec_file_command = 'touch {0}'.format(not_exec_file_path)
    '''Set wsdl validator path to not executable file'''
    set_wsdl_validator_path_to_not_executable_file = 'sh -c "echo \'{0}\' > {1}"'.format(
        '\n[proxy-ui]\nwsdl-validator-command=/etc/xroad/conf.d/notExecutableParser',
        ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION)
    self.log('Connecting to ssh client')
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Creating not executable file')
    self.ssh_client.exec_command(command=create_not_exec_file_command, sudo=True)
    self.log('Set wsdl validator path to not executable file')
    self.ssh_client.exec_command(command=set_wsdl_validator_path_to_not_executable_file, sudo=True)
    self.log('Reload application')
    self.ssh_client.exec_command(command=ss_system_parameters.RELOAD_APP_COMMAND, sudo=True)
    self.log('Wait until server is up')
    wait_until_server_up(ss_host)


def restore_wsdl_validator(case, ssh_host, ssh_username, ssh_password, not_exec_file_path):
    self = case
    '''Restore wsdl validator location conf from backup'''
    restore_backup_command = 'cp -p /etc/xroad/conf.d/local.ini.backup {0}'.format(
        ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION)
    '''Command to remove not executable file'''
    remove_not_exec_file = 'rm {0}'.format(not_exec_file_path)
    self.log('Connect ssh client')
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Remove not executable file')
    self.ssh_client.exec_command(command=remove_not_exec_file, sudo=True)
    self.log('Restore wsdl validator location conf')
    self.ssh_client.exec_command(command=restore_backup_command, sudo=True)
    self.log('Reload application')
    self.ssh_client.exec_command(command=ss_system_parameters.RELOAD_APP_COMMAND, sudo=True)
    self.log('Close ssh connection')
    self.ssh_client.close()


def restore_wsdl_validator_wrapper(case, ssh_host, ssh_username, ssh_password, wsdl_validator_wrapper_path):
    self = case
    '''Security server ssh client instance'''
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
    self.log('Restore wsdl validator wrapper')
    self.ssh_client.exec_command('cp -p {0}.backup {0}'.format(wsdl_validator_wrapper_path), sudo=True)
    self.log('Remove wsdl validator wrapper backup')
    self.ssh_client.exec_command('rm {0}.backup'.format(wsdl_validator_wrapper_path), sudo=True)
    self.ssh_client.close()


def wait_until_server_up(ss_host):
    '''Wait until reloading process has started'''
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    time.sleep(5)
    '''Make get request on ss server, without cert verification'''
    response = requests.get(ss_host, verify=False)
    '''Make get request on ss server until response code is 200 
    one moment it gets the connection, but waits reply for a while'''
    while response.status_code != 200:
        time.sleep(10)
        response = requests.get(ss_host, verify=False)
    time.sleep(10)
