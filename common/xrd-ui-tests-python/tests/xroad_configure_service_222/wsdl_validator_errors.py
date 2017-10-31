import time

import requests
import urllib3

from helpers import ssh_client
from tests.xroad_configure_service_222 import configure_service_2_2_2
from tests.xroad_refresh_wsdl_225 import refresh_wsdl_2_2_5
from view_models import clients_table_vm, ss_system_parameters
from view_models.log_constants import ADD_WSDL_FAILED, REFRESH_WSDL_FAILED
from view_models.messages import WSDL_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE, \
    WSDL_ADD_ERROR_VALIDATOR_COMMAND_NOT_FOUND, WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_FOUND, \
    WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE, WSDL_ERROR_VALIDATION_FAILED


def test_wsdl_validator_crash(self, wsdl_url, ssh_host, ssh_username, ssh_password, ss_host, ss_user, ss_pass,
                              client_name, client_id, wsdl_validator_wrapper_path):
    def wsdl_validator_crash():
        self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)
        self.log('Backing up wsdlvalidator wrapper')
        self.ssh_client.exec_command('cp {0} {0}.backup'.format(wsdl_validator_wrapper_path), sudo=True)
        self.log('Adding invalid argument(-asd) to wsdlvalidator_wrapper validator execution command')
        self.ssh_client.exec_command('sed -i -e "s/-r/-asd/g" {0}'.format(wsdl_validator_wrapper_path), sudo=True)
        self.ssh_client.close()

        self.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)
        self.log('Try to add wsdl')
        warning, error, console = configure_service_2_2_2.add_wsdl(self, wsdl_url=wsdl_url)
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
        warning, error, console = configure_service_2_2_2.add_wsdl(self, wsdl_url=wsdl_url)
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
        warning, error, console = refresh_wsdl_2_2_5.refresh_wsdl(self)
        self.log('SERVICE_14 3a.1 System skips the process of validation')
        self.log('Check if wsdl was refreshed successfully')
        self.is_none(warning)
        self.is_none(error)
        self.is_none(console)

    return test_refresh_success_no_validator


def remove_wsdl_validator_from_conf(self, ssh_host, ssh_username, ssh_password, ss_host):
    '''Command to backup local.ini to local.ini.backup file'''
    backup_local_ini_command = 'cp {0} {1}'.format(ss_system_parameters.WSDL_VALIDATOR_CONF_LOCATION,
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
        warning, error, console = configure_service_2_2_2.add_wsdl(self, wsdl_url=wsdl_warning_url)
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
        warning, error, console = refresh_wsdl_2_2_5.refresh_wsdl(self)
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
        warning, error, console = configure_service_2_2_2.add_wsdl(self, wsdl_url=wsdl_warning_url)
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
        warning, error, console = refresh_wsdl_2_2_5.refresh_wsdl(self)
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
    restore_backup_command = 'cp /etc/xroad/conf.d/local.ini.backup {0}'.format(
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
    self.ssh_client.exec_command('cp {0}.backup {0}'.format(wsdl_validator_wrapper_path), sudo=True)
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
    time.sleep(5)
