from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from helpers import soaptestclient, auditchecker
from view_models import popups, sidebar, messages, central_services, log_constants
# These faults are checked when we need the result to be unsuccessful. Otherwise the checking function returns True.
from view_models.log_constants import ADD_CENTRAL_SERVICE_FAILED, ADD_CENTRAL_SERVICE, EDIT_CENTRAL_SERVICE, \
    DELETE_CENTRAL_SERVICE
from view_models.messages import ADD_CENTRAL_SERVICE_EXISTS_ERROR, ADD_CENTRAL_SERVICE_PROVIDER_NOT_FOUND_ERROR
from view_models.popups import CENTRAL_SERVICE_POPUP_OK_BUTTON_ID

faults_unsuccessful = ['Server.ServerProxy.ServiceDisabled', 'Client.InternalError']
# These faults are checked when we need the result to be successful. Otherwise the checking function returns False.
faults_successful = ['Server.ServerProxy.AccessDenied', 'Server.ServerProxy.UnknownService',
                     'Server.ServerProxy.ServiceDisabled', 'Server.ClientProxy.*', 'Client.*',
                     'Server.ServerProxy.ServiceFailed.InvalidContentType']


def set_central_service_provider_fields(self, provider):
    # Find fields and fill them with our data
    central_service_target_code_input = self.by_id(popups.CENTRAL_SERVICE_POPUP_TARGET_CODE_ID)
    central_service_target_version_input = self.by_id(popups.CENTRAL_SERVICE_POPUP_TARGET_VERSION_ID)
    central_service_target_provider_input = self.by_id(popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_ID)
    central_service_target_provider_code_input = self.by_id(popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CODE_ID)
    central_service_target_provider_subsystem_input = self.by_id(
        popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_SUBSYSTEM_ID)
    central_service_target_provider_class_select = Select(
        self.by_id(popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CLASS_ID))

    self.input(central_service_target_code_input, provider['service_name'])
    self.input(central_service_target_version_input, provider['service_version'])
    # We can actually input anything here, it will be replaced with the real value from settings:
    self.input(central_service_target_provider_input, provider['code'])
    self.input(central_service_target_provider_code_input, provider['code'])
    self.input(central_service_target_provider_subsystem_input, provider['subsystem'])

    # Set service class
    central_service_target_provider_class_select.select_by_value(provider['class'])


def get_central_service_row(self, central_service_name):
    # Get the table rows.
    rows = self.by_xpath(central_services.SERVICES_TABLE_ROWS_XPATH, multiple=True)
    for row in rows:
        # Get first table cell (td element). If its contents match, return the row.
        if row.find_element_by_tag_name('td').text == central_service_name:
            return row

    # We're here so we didn't find anything. Return nothing.
    return None


def test_add_central_service(case, provider=None, central_service_name=None,
                             sync_max_seconds=0, wait_sync_retry_delay=0, requester=None, try_same_code_twice=False,
                             try_not_existing_member=False,
                             cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None):
    '''
    MainController test function. Adds a central service and tests if queries work.
    :param client_name: string | None - name of the client whose ACL we modify
    :param client_id: string | None - XRoad ID of the client whose ACL we modify
    :param wsdl_index: int | None - index (zero-based) for WSDL we select from the list
    :param wsdl_url: str | None - URL for WSDL we select from the list
    :return:
    '''

    self = case

    body_filename = self.config.get('services.request_template_filename')
    body_central_filename = self.config.get('services.central_request_template_filename')

    body = self.get_xml_query(body_filename)
    body_central = self.get_xml_query(body_central_filename)

    testclient_params = {
        'xroadProtocolVersion': self.config.get('services.xroad_protocol'),
        'xroadIssue': self.config.get('services.xroad_issue'),
        'xroadUserId': self.config.get('services.xroad_userid'),
        'serviceMemberInstance': provider['instance'],
        'serviceMemberClass': provider['class'],
        'serviceMemberCode': provider['code'],
        'serviceSubsystemCode': provider['subsystem'],
        'serviceCode': provider['service_name'],
        'serviceVersion': provider['service_version'],
        'memberInstance': requester['instance'],
        'memberClass': requester['class'],
        'memberCode': requester['code'],
        'subsystemCode': requester['subsystem'],
        'requestBody': self.config.get('services.testservice_2_request_body')
    }

    testclient_central_params = {
        'xroadProtocolVersion': self.config.get('services.xroad_protocol'),
        'xroadIssue': self.config.get('services.xroad_issue'),
        'xroadUserId': self.config.get('services.xroad_userid'),
        'serviceMemberInstance': provider['instance'],
        'serviceCode': central_service_name,
        'serviceProviderCode': provider['service_name'],
        'memberInstance': requester['instance'],
        'memberClass': requester['class'],
        'memberCode': requester['code'],
        'subsystemCode': requester['subsystem'],
        'requestBody': self.config.get('services.central_service_request_body')
    }

    testclient = soaptestclient.SoapTestClient(url=self.config.get('ss1.service_path'),
                                               body=body,
                                               retry_interval=wait_sync_retry_delay, fail_timeout=sync_max_seconds,
                                               faults_successful=faults_successful,
                                               faults_unsuccessful=faults_unsuccessful, params=testclient_params)

    testclient_central = soaptestclient.SoapTestClient(url=self.config.get('ss1.service_path'),
                                                       body=body_central,
                                                       retry_interval=wait_sync_retry_delay,
                                                       fail_timeout=sync_max_seconds,
                                                       faults_successful=faults_successful,
                                                       faults_unsuccessful=faults_unsuccessful,
                                                       params=testclient_central_params)

    def add_central_service():
        # UC SERVICE_41 Add a Central Service
        self.log('*** UC SERVICE_41 Add a Central Service')

        self.log('Starting mock service')
        self.start_mock_service()

        # Find "Central Services" menu item, click on it.
        central_services_menu = self.by_css(sidebar.CENTRAL_SERVICES_CSS)
        central_services_menu.click()
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user,
                                                password=cs_ssh_pass)

        # UC SERVICE_41 1. Select to add a central service.
        self.log('SERVICE_41 1. Select to add a central service.')

        # Wait until central services table appears (page has been loaded and table initialized)
        self.wait_until_visible(central_services.SERVICES_TABLE_ID, type=By.ID)

        # Wait until jquery has finished loading the list
        self.wait_jquery()

        # Click the "Add" button in the top right corner.
        add_button = self.by_id(central_services.SERVICE_ADD_BUTTON_ID)
        add_button.click()

        # Wait until popup opens
        self.wait_until_visible(element=popups.CENTRAL_SERVICE_POPUP, type=By.XPATH)

        # UC SERVICE_41 2. Insert central service information.
        self.log('SERVICE_41 2. Insert central service information.')
        self.log('Service name: {0}'.format(central_service_name))
        self.log('Service provider: {0}'.format(provider))

        # Find "service code" input field, clear it and enter the service name there
        central_service_code_input = self.by_id(popups.CENTRAL_SERVICE_POPUP_CENTRAL_SERVICE_CODE_ID)
        central_service_code_input.clear()
        self.input(central_service_code_input, central_service_name)

        current_log_lines = log_checker.get_line_count()
        # Set other fields
        set_central_service_provider_fields(self, provider=provider)

        add_service_ok_button = self.by_id(popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID)
        add_service_ok_button.click()

        # UC SERVICE_41 4. Verify that the service name is unique.
        self.log('SERVICE_41 4. Verify that the service name is unique.')
        # UC SERVICE_41 5. Verify that the provider exists.
        self.log('SERVICE_41 5. Verify that the provider exists.')

        # Wait until the service is added.
        self.wait_jquery()

        # Test that we didn't get an error. If we did, no need to continue.
        error_message = messages.get_error_message(self)  # Error message (anywhere)
        self.is_none(error_message,
                     msg='SERVICE_41 4, 5. Got error message when trying to add central service: {0}'.format(
                         error_message))

        # UC SERVICE_41 6. Central service has been saved.
        self.log('SERVICE_41 6. Central service has been saved.')

        expected_log_msg = ADD_CENTRAL_SERVICE
        self.log('SERVICE_41 7. System logs the event {0}'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found)

        # UC SERVICE_41 test query (1) from SS1 client 1 subsystem to service bodyMassIndex. Query should succeed.
        self.log('SERVICE_41 test query (1) {0} to bodyMassIndex. Query should succeed.'.format(body_filename))

        self.is_true(testclient.check_success(), msg='SERVICE_41 test query (1) failed')

        # UC SERVICE_41 test query (2) from SS1 client 1 subsystem to CENTRAL service. Query should succeed.
        self.log(
            'SERVICE_41 test query (2) {0} to central service {1}. Query should succeed.'.format(body_central_filename,
                                                                                                 central_service_name))

        self.is_true(testclient_central.check_success(), msg='SERVICE_41 test query (2) to central service failed')

        '''SERVICE_41 4a A central service with the inserted central service code already exists'''
        if try_same_code_twice:
            current_log_lines = log_checker.get_line_count()
            self.log('SERVICE_41 4a A central service with the inserted central service code already exists')
            self.log('Click on adding button')
            add_button = self.by_id(central_services.SERVICE_ADD_BUTTON_ID)
            add_button.click()

            '''Wait until popup opens'''
            self.wait_until_visible(element=popups.CENTRAL_SERVICE_POPUP, type=By.XPATH)

            '''Find "service code" input field, clear it and enter the service name there'''
            central_service_code_input = self.by_id(popups.CENTRAL_SERVICE_POPUP_CENTRAL_SERVICE_CODE_ID)
            central_service_code_input.clear()
            self.input(central_service_code_input, central_service_name)
            add_service_ok_button = self.by_id(popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID)
            add_service_ok_button.click()
            self.wait_jquery()
            expected_error_msg = ADD_CENTRAL_SERVICE_EXISTS_ERROR.format(central_service_name)
            self.log('SERVICE_41 4a.1 System displays the error message "{0}"'.format(expected_error_msg))
            error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_message)
            expected_log_msg = ADD_CENTRAL_SERVICE_FAILED
            self.log('SERVICE_41 4a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            popups.close_all_open_dialogs(self)
        if try_not_existing_member:
            current_log_lines = log_checker.get_line_count()
            self.log('SERVICE_41 5a Adding central service with not existing member')
            self.log('Click on adding button')
            self.by_id(central_services.SERVICE_ADD_BUTTON_ID).click()
            self.log('Wait until popup opens')
            self.wait_until_visible(element=popups.CENTRAL_SERVICE_POPUP, type=By.XPATH)
            self.log('Find "service code" input field, clear it and enter the service name there')
            central_service_code_input = self.by_id(popups.CENTRAL_SERVICE_POPUP_CENTRAL_SERVICE_CODE_ID)
            self.input(central_service_code_input, central_service_name)
            not_existing_provider = 'notexisting'
            provider['code'] = not_existing_provider
            self.log('Fill provider fields')
            set_central_service_provider_fields(self, provider=provider)
            self.log('Click OK')
            self.by_id(CENTRAL_SERVICE_POPUP_OK_BUTTON_ID).click()
            self.wait_jquery()
            expected_error_msg = ADD_CENTRAL_SERVICE_PROVIDER_NOT_FOUND_ERROR.format(provider['instance'],
                                                                                     provider['class'],
                                                                                     not_existing_provider,
                                                                                     provider['subsystem'])
            self.log('SERVICE_41 5a.1 System displays the error message "{0}"'.format(expected_error_msg))
            error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_message)
            expected_log_msg = ADD_CENTRAL_SERVICE_FAILED
            self.log('SERVICE_41 5a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found)
            popups.close_all_open_dialogs(self)

    return add_central_service


def test_edit_central_service(case, provider, requester, central_service_name, sync_max_seconds=0,
                              wait_sync_retry_delay=0, try_not_existing_provider=False, cs_ssh_host=None,
                              cs_ssh_user=None,
                              cs_ssh_pass=None):
    self = case

    query_url = self.config.get('ss1.service_path')
    query_filename = self.config.get('services.central_request_template_filename')
    query = self.get_xml_query(query_filename)

    testclient_central_params = {
        'xroadProtocolVersion': self.config.get('services.xroad_protocol'),
        'xroadIssue': self.config.get('services.xroad_issue'),
        'xroadUserId': self.config.get('services.xroad_userid'),
        'serviceMemberInstance': provider['instance'],
        'serviceCode': central_service_name,
        'serviceProviderCode': provider['service_name'],
        'memberInstance': requester['instance'],
        'memberClass': requester['class'],
        'memberCode': requester['code'],
        'subsystemCode': requester['subsystem'],
        'requestBody': self.config.get('services.central_service_request_body')
    }

    testclient_central = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                       retry_interval=wait_sync_retry_delay,
                                                       fail_timeout=sync_max_seconds,
                                                       faults_successful=faults_successful,
                                                       faults_unsuccessful=faults_unsuccessful,
                                                       params=testclient_central_params
                                                       )

    def edit_central_service():
        # UC SERVICE_42 Edit the Implementing Service of a Central Service
        self.log('*** UC SERVICE_42 Edit the Implementing Service of a Central Service')

        self.log('Starting mock service')
        self.mock_service = self.start_mock_service()

        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user,
                                                password=cs_ssh_pass)

        # UC SERVICE_42 1. Select to edit the implementing service of a central service
        self.log('SERVICE_42 1. Select to edit the implementing service of a central service')

        # Find "Central Services" menu item, click on it.
        central_services_menu = self.by_css(sidebar.CENTRAL_SERVICES_CSS)
        central_services_menu.click()

        # Wait until central services table appears (page has been loaded and table initialized)
        self.wait_until_visible(central_services.SERVICES_TABLE_ID, type=By.ID)

        # Wait until jquery has finished loading the list
        self.wait_jquery()

        # Find the service we're looking for. If nothing is found, cancel everything with assertion - no need to waste time.
        service_row = get_central_service_row(self, central_service_name)
        self.is_not_none(service_row, msg='SERVICE_42 1. Central service not found: {0}'.format(central_service_name))
        #
        # Click the row to select it
        service_row.click()

        # Find and click the "Edit" button to edit the service
        edit_button = self.by_id(central_services.SERVICE_EDIT_BUTTON_ID)
        edit_button.click()

        # Wait until ajax query finishes.
        self.wait_jquery()

        # UC SERVICE_42 2. Set the X-Road identifier and name of the service provider
        self.log('SERVICE_42 2. Set the X-Road identifier and name of the service provider')
        self.log('Service name: {0}'.format(central_service_name))
        self.log('Service provider: {0}'.format(provider))

        # Find and click the "Clear" button (after the Edit dialog opens) to clear fields.
        clear_button = self.wait_until_visible(central_services.SERVICE_EDIT_DIALOG_CLEAR_BUTTON_ID, type=By.ID)
        clear_button.click()

        current_log_lines = log_checker.get_line_count()
        # Set the new provider data
        set_central_service_provider_fields(self, provider=provider)

        add_service_ok_button = self.by_id(popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID)
        add_service_ok_button.click()

        # Wait until the service is added.
        self.wait_jquery()

        # UC SERVICE_42 4. Verify that the provider exists.
        self.log('SERVICE_42 4. Verify that the provider exists.')

        # UC SERVICE_42 5. Check if the changes are saved.
        self.log('SERVICE_42 5. Check if the changes are saved.')

        # Test that we didn't get an error. If we did, no need to continue.
        error_message = messages.get_error_message(self)  # Error message (anywhere)
        self.is_none(error_message,
                     msg='SERVICE_42 5. Got error message when trying to update central service: {0}'.format(
                         error_message))

        expected_log_msg = EDIT_CENTRAL_SERVICE
        self.log('SERVICE_42 6. System logs the event {0}'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

        # UC SERVICE_42 test query (1) from SS1 client subsystem 1 to service bodyMassIndex. Query should succeed.
        self.log(
            'SERVICE_42 test query (1) {0} to bodyMassIndex. Query should succeed, served by {1}:{2}.'.format(
                query_filename,
                provider['code'],
                provider[
                    'subsystem']))

        verify_service = {'class': provider['class'], 'code': provider['code'],
                          'subsystem': provider['subsystem']}

        testclient_central.verify_service_data = verify_service

        case.is_true(testclient_central.check_success(),
                     msg='SERVICE_42 test query (2) after updating central service failed')
        if try_not_existing_provider:
            # UC SERVICE_42 4a. Try to set a service provider that does not exist.
            self.log('SERVICE_42 4a. Try to set a service provider that does not exist.')

            current_log_lines = log_checker.get_line_count()
            edit_button = self.by_id(central_services.SERVICE_EDIT_BUTTON_ID)
            edit_button.click()

            # Wait until ajax query finishes.
            self.wait_jquery()

            # Find and click the "Clear" button (after the Edit dialog opens) to clear fields.
            clear_button = self.wait_until_visible(central_services.SERVICE_EDIT_DIALOG_CLEAR_BUTTON_ID, type=By.ID)
            clear_button.click()

            not_existing_provider = 'notexisting'
            provider['code'] = not_existing_provider

            set_central_service_provider_fields(self, provider=provider)

            add_service_ok_button = self.by_id(popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID)
            add_service_ok_button.click()
            self.wait_jquery()

            # UC SERVICE_42 4a.1. Check error message
            self.log('SERVICE_42 4a.1. Check error message.')
            error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(
                messages.EDIT_CENTRAL_SERVICE_PROVIDER_NOT_FOUND_ERROR.format(provider['instance'], provider['class'],
                                                                              not_existing_provider,
                                                                              provider['subsystem']),
                error_message)

            # UC SERVICE_42 4a.2. Check logs
            self.log('SERVICE_42 4a.2. Check logs for: {0}'.format(log_constants.EDIT_CENTRAL_SERVICE_FAILED))

            logs_found = log_checker.check_log(log_constants.EDIT_CENTRAL_SERVICE_FAILED,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='SERVICE_42 4a.2. Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                             log_constants.EDIT_CENTRAL_SERVICE_FAILED,
                             log_checker.found_lines))
            popups.close_all_open_dialogs(self)

    return edit_central_service


def test_delete_central_service(case, cs_ssh_host, cs_ssh_user, cs_ssh_pass, central_service_name, provider, requester,
                                sync_max_seconds=0,
                                wait_sync_retry_delay=0, cancel_deletion=False):
    self = case

    query_url = self.config.get('ss1.service_path')
    query_filename = self.config.get('services.central_request_template_filename')
    query = self.get_xml_query(query_filename)

    testclient_central_params = {
        'xroadProtocolVersion': self.config.get('services.xroad_protocol'),
        'xroadIssue': self.config.get('services.xroad_issue'),
        'xroadUserId': self.config.get('services.xroad_userid'),
        'serviceMemberInstance': provider['instance'],
        'serviceCode': central_service_name,
        'serviceProviderCode': provider['service_name'],
        'memberInstance': requester['instance'],
        'memberClass': requester['class'],
        'memberCode': requester['code'],
        'subsystemCode': requester['subsystem'],
        'requestBody': self.config.get('services.central_service_request_body')
    }

    testclient_central = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                       retry_interval=wait_sync_retry_delay,
                                                       fail_timeout=sync_max_seconds,
                                                       faults_successful=faults_successful,
                                                       faults_unsuccessful=faults_unsuccessful,
                                                       params=testclient_central_params)

    def delete_central_service():
        # UC SERVICE_43 Delete a Central Service
        self.log('*** UC SERVICE_43 Delete a Central Service')

        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user,
                                                password=cs_ssh_pass)

        # UC SERVICE_43 1. Select to delete a central service.
        self.log('SERVICE_43 1. Select to delete a central service.')

        # Find "Central Services" menu item, click on it.
        central_services_menu = self.by_css(sidebar.CENTRAL_SERVICES_CSS)
        central_services_menu.click()

        # Wait until central services table appears (page has been loaded and table initialized)
        self.wait_until_visible(central_services.SERVICES_TABLE_ID, type=By.ID)

        # Wait until jquery has finished loading the list
        self.wait_jquery()

        # Find the service we're looking for. If nothing is found, cancel everything with assertion - no need to waste time.
        service_row = get_central_service_row(self, central_service_name)
        self.is_not_none(service_row, msg='SERVICE_43 1. Central service not found: {0}'.format(central_service_name))

        # Click the row to select it
        service_row.click()

        current_log_lines = log_checker.get_line_count()

        # Find and click the "Delete" button to delete the service
        delete_button = self.by_id(central_services.SERVICE_DELETE_BUTTON_ID)
        delete_button.click()

        # UC SERVICE_43 2. System prompts for confirmation
        self.log('SERVICE_43 2. System prompts for confirmation')

        '''UC SERVICE_43 3a. service deletion is canceled'''
        self.log('UC SERVICE_43 3a. service deletion is canceled')
        if cancel_deletion:
            '''Cancel the deletion'''
            self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()

            '''Check if service still exists'''
            self.wait_jquery()
            service_row = get_central_service_row(self, central_service_name)
            self.is_not_none(service_row,
                             msg='SERVICE_43 3a. Central service not found after canceling: {0}'.format(
                                 central_service_name))

            '''Click delete button again'''
            delete_button.click()

        # UC SERVICE_43 3. Confirm deletion
        self.log('SERVICE_43 3. Confirm deletion')

        # A confirmation dialog should open. Confirm the deletion.
        popups.confirm_dialog_click(self)

        # Wait until ajax query finishes.
        self.wait_jquery()

        # UC SERVICE_43 4. Check if service has been deleted
        self.log('SERVICE_43 4. Check if service has been deleted')

        # Test if the service was deleted.
        service_row = get_central_service_row(self, central_service_name)
        self.is_none(service_row, msg='SERVICE_43 4. Central service not deleted: {0}'.format(central_service_name))

        expected_log_msg = DELETE_CENTRAL_SERVICE
        self.log('SERVICE_43 5. System logs the event {0}'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

        # UC SERVICE_43 test query (1) from SS1 client 1 subsystem to CENTRAL service. Query should succeed.
        self.log('SERVICE_43 test query (1) {0} to central service {1}. Query should fail.'.format(query_filename,
                                                                                                   central_service_name))

        self.is_equal(testclient_central.check_fail(), True,
                      msg='SERVICE_43 test query (1) to central service succeeded')

    return delete_central_service
