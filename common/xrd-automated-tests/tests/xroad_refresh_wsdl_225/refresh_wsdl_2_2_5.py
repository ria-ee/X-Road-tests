# coding=utf-8

from view_models import clients_table_vm, popups, messages
from selenium.webdriver.common.by import By
from helpers import ssh_client, xroad, soaptestclient
import time
from tests.xroad_add_to_acl_218 import add_to_acl_2_1_8

# These faults are checked when we need the result to be unsuccessful. Otherwise the checking function returns True.
faults_unsuccessful = ['Server.ServerProxy.AccessDenied', 'Server.ServerProxy.UnknownService']
# These faults are checked when we need the result to be successful. Otherwise the checking function returns False.
faults_successful = ['Server.ServerProxy.AccessDenied', 'Server.ServerProxy.UnknownService',
                     'Server.ServerProxy.ServiceDisabled', 'Server.ClientProxy.*', 'Client.*']

wsdl_delete_command = 'rm {0}'  # {0} is replaced with wsdl_local_path+wsdl_filename

# Use symbolic links instead of copy:
# wsdl_replace_command = 'ln -s {0} {1}'  # {0} is replaced with source filename and {1} with  wsdl_local_path+wsdl_filename
# Use copy instead of using links:
wsdl_replace_command = 'cp {0} {1}'  # {0} is replaced with source filename and {1} with  wsdl_local_path+wsdl_filename


def webserver_set_wsdl(self, wsdl_source_filename, wsdl_target_filename):
    replace_commmand = wsdl_replace_command.format(wsdl_source_filename, wsdl_target_filename)
    self.ssh_client.exec_command(replace_commmand)
    return (self.ssh_client.exit_status() == 0)


def webserver_delete_wsdl(self, wsdl_target_filename):
    delete_commmand = wsdl_delete_command.format(wsdl_target_filename)
    self.ssh_client.exec_command(delete_commmand)
    return (self.ssh_client.exit_status() == 0)


def webserver_connect(self, ssh_host, ssh_username, ssh_password):
    self.ssh_client = ssh_client.SSHClient(host=ssh_host, username=ssh_username, password=ssh_password)


def webserver_close(self):
    self.ssh_client.close()


def test_refresh_wsdl(case, client=None, client_name=None, client_id=None, wsdl_index=None, wsdl_url=None,
                      requester=None, service_name=None,
                      service_name_2=None, wsdl_path=None,
                      wsdl_local_path=None, wsdl_filename=None, wsdl_correct=None, wsdl_missing_service=None,
                      wsdl_error=None, wsdl_warning=None, ssh_host=None, ssh_username=None, ssh_password=None):
    '''
    MainController test function. Refreshes WSDL and checks for error scenarios.
    :return:
    '''

    self = case
    client_id = xroad.get_xroad_subsystem(client)
    requester_id = xroad.get_xroad_subsystem(requester)

    query_url = self.config.get('ss1.service_path')
    query_filename = self.config.get('services.request_template_filename')
    query_2_filename = self.config.get('services.request_template_filename')
    query = self.get_xml_query(query_filename)
    query_2 = self.get_xml_query(query_2_filename)

    # Immediate queries, no delay needed, no retry allowed.
    sync_retry = 0
    sync_max_seconds = 0

    testclient_params = {
        'xroadProtocolVersion': self.config.get('services.xroad_protocol'),
        'xroadIssue': self.config.get('services.xroad_issue'),
        'xroadUserId': self.config.get('services.xroad_userid'),
        'serviceMemberInstance': client['instance'],
        'serviceMemberClass': client['class'],
        'serviceMemberCode': client['code'],
        'serviceSubsystemCode': client['subsystem'],
        'serviceCode': xroad.get_service_name(service_name),
        'serviceVersion': xroad.get_service_version(service_name),
        'memberInstance': requester['instance'],
        'memberClass': requester['class'],
        'memberCode': requester['code'],
        'subsystemCode': requester['subsystem'],
        'requestBody': self.config.get('services.testservice_2_request_body')
    }

    testclient_params_2 = {
        'xroadProtocolVersion': self.config.get('services.xroad_protocol'),
        'xroadIssue': self.config.get('services.xroad_issue'),
        'xroadUserId': self.config.get('services.xroad_userid'),
        'serviceMemberInstance': client['instance'],
        'serviceMemberClass': client['class'],
        'serviceMemberCode': client['code'],
        'serviceSubsystemCode': client['subsystem'],
        'serviceCode': xroad.get_service_name(service_name_2),
        'serviceVersion': xroad.get_service_version(service_name_2),
        'memberInstance': requester['instance'],
        'memberClass': requester['class'],
        'memberCode': requester['code'],
        'subsystemCode': requester['subsystem'],
        'requestBody': self.config.get('services.testservice_request_body')
    }

    testclient_http = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                    retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                    faults_successful=faults_successful,
                                                    faults_unsuccessful=faults_unsuccessful, params=testclient_params)
    testclient_http_2 = soaptestclient.SoapTestClient(url=query_url, body=query_2,
                                                      retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                      faults_successful=faults_successful,
                                                      faults_unsuccessful=faults_unsuccessful,
                                                      params=testclient_params_2)

    def refresh_wsdl():
        # Find the "Refresh" button
        refresh_button = self.by_id(popups.CLIENT_DETAILS_POPUP_REFRESH_WSDL_BTN_ID)

        time.sleep(3)
        # Click the "Refresh" button to reload the WSDL. This may take some time as the system does an
        # HTTP(S) request to another server. Then wait until the ajax query finishes.
        refresh_button.click()
        self.wait_jquery()

        console_output = messages.get_console_output(
            self)  # Console message (displayed if WSDL validator gives a warning)
        warning_message = messages.get_warning_message(self)  # Warning message
        error_message = messages.get_error_message(self)  # Error message (anywhere)

        if console_output is not None:
            popups.close_console_output_dialog(self)

        return warning_message, error_message, console_output

    def refresh_existing_wsdl():
        """
        :param self: MainController class object
        :return: None
        ''"""

        # TEST PLAN 2.2.5 - refresh service WSDL
        self.log('*** 2.2.5 / XT-469')

        # Open an SSH connection to the webserver
        webserver_connect(self, ssh_host, ssh_username, ssh_password)

        self.log('2.2.5 initialize with the correct WSDL file: {0}'.format(wsdl_correct))
        webserver_set_wsdl(self, wsdl_source_filename=wsdl_local_path.format(wsdl_correct),
                           wsdl_target_filename=wsdl_local_path.format(wsdl_filename))

        # TEST PLAN 2.2.5-1 test query from TS1 client CLIENT1:sub to service bodyMassIndex. Query should succeed.
        self.log('2.2.5-1 test query {0} to bodyMassIndex. Query should succeed.'.format(query_filename))
        case.is_true(testclient_http.check_success(), msg='2.2.5-1 test query failed')

        # TEST PLAN 2.2.5-2 delete service bodyMassIndex and refresh WSDL
        self.log('2.2.5-2 delete service bodyMassIndex and refresh WSDL')

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        # Find the table that lists all WSDL files and services
        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        # Wait until that table is visible (opened in a popup)
        self.wait_until_visible(services_table)

        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index, wsdl_url=wsdl_url)

        service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_index=wsdl_index,
                                                                          wsdl_url=wsdl_url, service_name=service_name)
        service_row_2 = clients_table_vm.client_services_popup_find_service(self, wsdl_index=wsdl_index,
                                                                            wsdl_url=wsdl_url,
                                                                            service_name=service_name_2)
        service_rows = clients_table_vm.client_services_popup_get_services_rows(self, wsdl_index=wsdl_index,
                                                                                wsdl_url=wsdl_url)

        service_parameters = clients_table_vm.get_service_parameters(self, service_row)
        service_parameters_2 = clients_table_vm.get_service_parameters(self, service_row_2)

        # TEST PLAN 2.2.5.1 - replace WSDL with a file that gives a validation error
        self.log('2.2.5.1 - replace WSDL with a file that cannot be validated at all: {0}'.format(wsdl_error))
        webserver_set_wsdl(self, wsdl_source_filename=wsdl_local_path.format(wsdl_error),
                           wsdl_target_filename=wsdl_local_path.format(wsdl_filename))

        # Click "Refresh" and return status
        warning, error, console = refresh_wsdl()
        self.is_not_none(error, msg='Invalid WSDL: no error shown for WSDL {0}'.format(wsdl_url))
        self.is_equal(error, messages.WSDL_REFRESH_ERROR_VALIDATION_FAILED.format(wsdl_url),
                      msg='Refresh invalid WSDL: wrong error shown for WSDL {0} : {1}'
                      .format(wsdl_url, error))
        self.is_none(warning, msg='Refresh invalid WSDL: got warning for WSDL {0} : {1}'
                     .format(wsdl_url, warning))
        self.is_not_none(console, msg='Refresh invalid WSDL: no console output for WSDL {0}'
                         .format(wsdl_url))
        self.log('Error message: {0}'.format(warning))

        # TEST PLAN 2.2.5.2 - replace WSDL with a file that gives a validation warning
        self.log('2.2.5.2 - replace WSDL with a file that gives a validation warning: {0}'.format(wsdl_warning))
        webserver_set_wsdl(self, wsdl_source_filename=wsdl_local_path.format(wsdl_warning),
                           wsdl_target_filename=wsdl_local_path.format(wsdl_filename))
        warning, error, console = refresh_wsdl()
        self.is_none(error,
                     msg='Refresh WSDL with validator warnings: got error for WSDL {0}'.format(wsdl_url))
        self.is_not_none(warning, msg='Refresh WSDL with validator warnings: no warning shown for WSDL {0} : {1}'
                         .format(wsdl_url, warning))
        self.is_none(console, msg='Refresh WSDL with validator warnings: got console output for WSDL {0} : {1}'
                     .format(wsdl_url, console))
        self.log('Warning message: {0}'.format(warning))

        # A warning popup should appear. We will not update the WSDL with a one that does not fully validate.
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CANCEL_XPATH).click()
        self.wait_jquery()

        # TEST PLAN 2.2.5-2 - replace WSDL with a correct file that doesn't include bodyMassIndex service.
        # In the test plan, there are two variants of how to delete the service (v1 and v2). One of them is commenting
        # out bodyMassIndex service and the second is to replace the WSDL with one that only contains service
        # xroadGetRandom. As the outcome is the same and only relies on parsing the XML (parser just ignores commented-out
        # blocks), we're just using variant 2 (v2 - replacing the WSDL with one that only contains xroadGetRandom).
        # If it is necessary to test both, the full 2.2.5-2 block may be duplicated and wsdl_missing_service variable
        # should be replaced or updated with one that specifies a file with commented-out bodyMassIndex.
        self.log(
            '2.2.5-2 - replace WSDL with a file that only contains xroadGetRandom: {0}'.format(wsdl_missing_service))

        webserver_set_wsdl(self, wsdl_source_filename=wsdl_local_path.format(wsdl_missing_service),
                           wsdl_target_filename=wsdl_local_path.format(wsdl_filename))

        # Click "Refresh" and return status
        warning, error, console = refresh_wsdl()

        # Check if warning message is correct.
        warning_message_is_correct = warning.startswith(
            messages.WSDL_REFRESH_WARNING_DELETING_SERVICES.format(wsdl_missing_service))

        self.is_none(error,
                     msg='Refresh WSDL (xroadGetRandom): got error for WSDL {0} : {1}'.format(wsdl_missing_service,
                                                                                              error))
        self.is_not_none(warning, msg='Refresh WSDL (xroadGetRandom): no warning shown for WSDL {0}'.format(
            wsdl_missing_service))
        self.is_equal(warning_message_is_correct, True,
                      msg='Refresh WSDL (xroadGetRandom): wrong error shown for WSDL {0} : {1}'.format(
                          wsdl_missing_service,
                          warning))
        self.is_none(console,
                     msg='Refresh WSDL (xroadGetRandom): got console output for WSDL {0} : {1}'.format(
                         wsdl_missing_service,
                         console))

        # A warning dialog should be open. Confirm the deletion by clicking "Continue".
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()

        # Wait until the settings are saved.
        self.wait_jquery()

        # TEST PLAN 2.2.5-3 test query from TS1 client CLIENT1:sub to service bodyMassIndex. Query should fail.
        self.log('2.2.5-3 test query {0} to service bodyMassIndex. Query should fail.'.format(query_filename))
        case.is_true(testclient_http.check_fail(), msg='2.2.5-3 test query succeeded')

        # TEST PLAN 2.2.5-4 add service bodyMassIndex to service WSDL and refresh the service. UI should notify about
        # an added service. NB! Service settings must not change.

        self.log('2.2.5-4 add service bodyMassIndex to service WSDL and refresh the service: {0}'.format(wsdl_correct))

        webserver_set_wsdl(self, wsdl_source_filename=wsdl_local_path.format(wsdl_correct),
                           wsdl_target_filename=wsdl_local_path.format(wsdl_filename))

        # Click "Refresh" and return status
        warning, error, console = refresh_wsdl()

        # Check if warning message is correct.
        warning_message_is_correct = warning.startswith(
            messages.WSDL_REFRESH_WARNING_ADDING_SERVICES.format(wsdl_correct))

        self.is_none(error,
                     msg='Refresh WSDL (xroadGetRandom, bodyMassIndex): got error for WSDL {0} : {1}'.format(
                         wsdl_correct, error))
        self.is_not_none(warning,
                         msg='Refresh WSDL (xroadGetRandom, bodyMassIndex): no warning shown for WSDL {0}'.format(
                             wsdl_correct))
        self.is_equal(warning_message_is_correct, True,
                      msg='Refresh WSDL (xroadGetRandom, bodyMassIndex): wrong error shown for WSDL {0} : {1}'.format(
                          wsdl_correct,
                          warning))
        self.is_none(console,
                     msg='Refresh WSDL (xroadGetRandom): got console output for WSDL {0} : {1}'.format(
                         wsdl_correct,
                         console))

        # A warning dialog should be open. Confirm the deletion by clicking "Continue".
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()

        # Wait until the settings are saved.
        self.wait_jquery()

        # Verify that the settings are not overwritten with default values.
        # Find the service row again because deleting and re-enabling might have reordered the services.
        service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_index=wsdl_index,
                                                                          wsdl_url=wsdl_url, service_name=service_name)
        service_row_2 = clients_table_vm.client_services_popup_find_service(self, wsdl_index=wsdl_index,
                                                                            wsdl_url=wsdl_url,
                                                                            service_name=service_name_2)

        new_service_parameters = clients_table_vm.get_service_parameters(self, service_row)
        new_service_parameters_2 = clients_table_vm.get_service_parameters(self, service_row_2)

        self.is_equal(service_parameters_2['url'], new_service_parameters_2['url'],
                      msg='Service URLs are not equal, old={0}, new={1}'.format(
                          service_parameters_2['url'], new_service_parameters_2['url']))
        self.is_equal(service_parameters_2['timeout'], new_service_parameters_2['timeout'],
                      msg='Service timeouts are not equal, old={0}, new={1}'.format(
                          service_parameters_2['timeout'], new_service_parameters_2['timeout']))

        popups.close_all_open_dialogs(self)

        # TEST PLAN 2.2.5-5 set bodyMassIndex address and ACL (give access to CLIENT1:sub)
        self.log('2.2.5-5 set bodyMassIndex address and ACL (give access to client)')

        add_acl = add_to_acl_2_1_8.test_add_subjects(self, client=client, client_id=client_id, wsdl_url=wsdl_url,
                                                     service_name=service_name, service_subjects=[requester_id],
                                                     remove_data=False,
                                                     allow_remove_all=False)
        add_acl()

        # TEST PLAN 2.2.5-6 test queries from TS1 client CLIENT1:sub to services bodyMassIndex and xroadGetRandom.
        # Both queries should succeed.
        self.log('2.2.5-6 test query {0} to service bodyMassIndex. Query should succeed.'.format(query_filename))
        case.is_true(testclient_http.check_success(), msg='2.2.5-6 test query failed')

        self.log('2.2.5-6 test query 2 {0} to service xroadGetRandom. Query should succeed.'.format(query_2_filename))
        case.is_true(testclient_http_2.check_success(), msg='2.2.5-6 test query 2 failed')

    return refresh_existing_wsdl


def test_reset_wsdl(case, wsdl_local_path=None, wsdl_filename=None, wsdl_correct=None, ssh_host=None, ssh_username=None,
                    ssh_password=None):
    '''
    MainController test function.
    :param client_name: string | None - name of the client whose ACL we modify
    :param client_id: string | None - XRoad ID of the client whose ACL we modify
    :param wsdl_index: int | None - index (zero-based) for WSDL we select from the list
    :param wsdl_url: str | None - URL for WSDL we select from the list
    :return:
    '''

    self = case

    def reset_wsdl():
        """
        :return: None
        ''"""

        self.log('2.2.5-del reset_wsdl')

        # TEST PLAN 2.2.5 error handling - reset service WSDL to original

        # Open an SSH connection to the webserver
        webserver_connect(self, ssh_host, ssh_username, ssh_password)

        self.log('2.2.5-del set the correct WSDL file: {0}'.format(wsdl_correct))
        webserver_set_wsdl(self, wsdl_source_filename=wsdl_local_path.format(wsdl_correct),
                           wsdl_target_filename=wsdl_local_path.format(wsdl_filename))

    return reset_wsdl
