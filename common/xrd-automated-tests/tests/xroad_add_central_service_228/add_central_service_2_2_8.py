from helpers import soaptestclient
from view_models import popups, sidebar, messages, central_services
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# These faults are checked when we need the result to be unsuccessful. Otherwise the checking function returns True.
faults_unsuccessful = ['Server.ServerProxy.ServiceDisabled', 'Client.InternalError']
# These faults are checked when we need the result to be successful. Otherwise the checking function returns False.
faults_successful = ['Server.ServerProxy.AccessDenied', 'Server.ServerProxy.UnknownService',
                     'Server.ServerProxy.ServiceDisabled', 'Server.ClientProxy.*', 'Client.*']


def set_central_service_provider_fields(self, provider):
    # provider_data = helper.split_xroad_data(provider)

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
                             sync_max_seconds=0, wait_sync_retry_delay=0):
    '''
    MainController test function. Very similar to test_all_subjects but adds ALL subjects to a specified subject's ACL.
    :param client_name: string | None - name of the client whose ACL we modify
    :param client_id: string | None - XRoad ID of the client whose ACL we modify
    :param wsdl_index: int | None - index (zero-based) for WSDL we select from the list
    :param wsdl_url: str | None - URL for WSDL we select from the list
    :return:
    '''

    self = case

    body_filename = self.config.get('services.testservice_2_request_filename')
    body_central_filename = self.config.get('services.central_service_request_filename')

    body = self.get_xml_query(body_filename)
    body_central = self.get_xml_query(body_central_filename)

    testclient = soaptestclient.SoapTestClient(url=self.config.get('ss1.service_path'),
                                               body=body,
                                               retry_interval=wait_sync_retry_delay, fail_timeout=sync_max_seconds,
                                               faults_successful=faults_successful,
                                               faults_unsuccessful=faults_unsuccessful)

    testclient_central = soaptestclient.SoapTestClient(url=self.config.get('ss1.service_path'),
                                                       body=body_central,
                                                       retry_interval=wait_sync_retry_delay,
                                                       fail_timeout=sync_max_seconds,
                                                       faults_successful=faults_successful,
                                                       faults_unsuccessful=faults_unsuccessful)

    def add_central_service():
        self.log('*** add_central_service')

        self.log('Starting mock service')
        self.start_mock_service()

        # Find "Central Services" menu item, click on it.
        central_services_menu = self.by_css(sidebar.CENTRAL_SERVICES_CSS)
        central_services_menu.click()

        # TEST PLAN 2.2.8-1 define central service "random": code=xroadGetRandom; version=v1;
        #                                                   provider=SUBSYSTEM:KS1:COM:CLIENT1:testservice
        self.log('2.2.8-1 define central service')

        # Wait until central services table appears (page has been loaded and table initialized)
        self.wait_until_visible(central_services.SERVICES_TABLE_ID, type=By.ID)

        # Wait until jquery has finished loading the list
        self.wait_jquery()

        # Click the "Add" button in the top right corner.
        add_button = self.by_id(central_services.SERVICE_ADD_BUTTON_ID)
        add_button.click()

        # Wait until popup opens
        self.wait_until_visible(element=popups.CENTRAL_SERVICE_POPUP, type=By.XPATH)

        # Find "service code" input field, clear it and enter the service name there
        central_service_code_input = self.by_id(popups.CENTRAL_SERVICE_POPUP_CENTRAL_SERVICE_CODE_ID)
        central_service_code_input.clear()
        # central_service_code_input.send_keys(central_service_name)
        self.input(central_service_code_input, central_service_name)

        # Set other fields
        set_central_service_provider_fields(self, provider=provider)

        add_service_ok_button = self.by_id(popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID)
        add_service_ok_button.click()

        # Wait until the service is added.
        self.wait_jquery()

        # Test that we didn't get an error. If we did, no need to continue.
        error_message = messages.get_error_message(self)  # Error message (anywhere)
        self.is_none(error_message,
                     msg='2.2.8-1 Got error message when trying to add central service: {0}'.format(error_message))

        # TEST PLAN 2.2.8-2 test query from TS1 client CLIENT1:sub to service bodyMassIndex. Query should succeed.
        self.log('2.2.8-2 test query {0} to bodyMassIndex. Query should succeed.'.format(body_filename))

        self.is_true(testclient.check_success(), msg='2.2.8-2 Test query failed')

        # TEST PLAN 2.2.8-3 test query from TS1 client CLIENT1:sub to CENTRAL service. Query should succeed.
        self.log('2.2.8-3 test query {0} to central service {1}. Query should succeed.'.format(body_central_filename,
            central_service_name))

        self.is_true(testclient_central.check_success(), msg='2.2.8-3 Test query to central service failed')

    return add_central_service


def test_edit_central_service(case, provider, central_service_name, sync_max_seconds=0,
                              wait_sync_retry_delay=0):
    self = case

    query_url = self.config.get('ss1.service_path')
    query_filename = self.config.get('services.central_service_request_filename')
    query = self.get_xml_query(query_filename)

    testclient_central = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                       retry_interval=wait_sync_retry_delay,
                                                       fail_timeout=sync_max_seconds,
                                                       faults_successful=faults_successful,
                                                       faults_unsuccessful=faults_unsuccessful)

    def edit_central_service():
        self.log('*** edit_central_service')

        self.log('Starting mock service')
        self.mock_service = self.start_mock_service()

        # Find "Central Services" menu item, click on it.
        central_services_menu = self.by_css(sidebar.CENTRAL_SERVICES_CSS)
        central_services_menu.click()

        # Wait until central services table appears (page has been loaded and table initialized)
        self.wait_until_visible(central_services.SERVICES_TABLE_ID, type=By.ID)

        # Wait until jquery has finished loading the list
        self.wait_jquery()

        # Find the service we're looking for. If nothing is found, cancel everything with assertion - no need to waste time.
        service_row = get_central_service_row(self, central_service_name)
        self.is_not_none(service_row, msg='Central service not found: {0}'.format(central_service_name))
        #
        # Click the row to select it
        service_row.click()

        # Find and click the "Delete" button to delete the service
        edit_button = self.by_id(central_services.SERVICE_EDIT_BUTTON_ID)
        edit_button.click()

        # Wait until ajax query finishes.
        self.wait_jquery()

        # Find and click the "Clear" button (after the Edit dialog opens) to clear fields.
        clear_button = self.wait_until_visible(central_services.SERVICE_EDIT_DIALOG_CLEAR_BUTTON_ID, type=By.ID)
        clear_button.click()

        # Set the new provider data
        set_central_service_provider_fields(self, provider=provider)

        add_service_ok_button = self.by_id(popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID)
        add_service_ok_button.click()

        # Wait until the service is added.
        self.wait_jquery()

        # Test that we didn't get an error. If we did, no need to continue.
        error_message = messages.get_error_message(self)  # Error message (anywhere)
        self.is_none(error_message,
                     msg='2.2.8-5 Got error message when trying to add central service: {0}'.format(error_message))

        # data_saved_timestamp = time.time()

        # TEST PLAN 2.2.8-2 test query from TS1 client CLIENT1:sub to service bodyMassIndex. Query should succeed.
        self.log(
            '2.2.8-6 test query {0} to bodyMassIndex. Query should succeed, served by {1}:{2}.'.format(query_filename, provider['code'],
                                                                                      provider['subsystem']))

        verify_service = {'class': provider['class'], 'code': provider['code'],
                          'subsystem': provider['subsystem']}

        testclient_central.verify_service_data = verify_service

        case.is_true(testclient_central.check_success(), msg='2.2.8-3 Test query after updating central service failed')

    return edit_central_service


def test_delete_central_service(case, central_service_name, sync_max_seconds=0, wait_sync_retry_delay=0):
    self = case

    query_url = self.config.get('ss1.service_path')
    query_filename = self.config.get('services.central_service_request_filename')
    query = self.get_xml_query(query_filename)

    testclient_central = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                       retry_interval=wait_sync_retry_delay,
                                                       fail_timeout=sync_max_seconds,
                                                       faults_successful=faults_successful,
                                                       faults_unsuccessful=faults_unsuccessful)

    def delete_central_service():
        self.log('*** delete_central_service')

        # Find "Central Services" menu item, click on it.
        central_services_menu = self.by_css(sidebar.CENTRAL_SERVICES_CSS)
        central_services_menu.click()

        # Wait until central services table appears (page has been loaded and table initialized)
        self.wait_until_visible(central_services.SERVICES_TABLE_ID, type=By.ID)

        # Wait until jquery has finished loading the list
        self.wait_jquery()

        # Find the service we're looking for. If nothing is found, cancel everything with assertion - no need to waste time.
        service_row = get_central_service_row(self, central_service_name)
        self.is_not_none(service_row, msg='Central service not found: {0}'.format(central_service_name))
        #
        # Click the row to select it
        service_row.click()

        # Find and click the "Delete" button to delete the service
        delete_button = self.by_id(central_services.SERVICE_DELETE_BUTTON_ID)
        delete_button.click()

        # A confirmation dialog should open. Confirm the deletion.
        popups.confirm_dialog_click(self)

        # Wait until ajax query finishes.
        self.wait_jquery()

        # Test if the service was deleted.
        service_row = get_central_service_row(self, central_service_name)
        self.is_none(service_row, msg='Central service not deleted: {0}'.format(central_service_name))

        # TEST PLAN 2.2.8-3 test query from TS1 client CLIENT1:sub to CENTRAL service. Query should succeed.
        self.log('2.2.8-3 test query {0} to central service {1}. Query should fail.'.format(query_filename,
            central_service_name))

        self.is_equal(testclient_central.check_fail(), True, msg='2.2.8-3 Test query to central service succeeded')

    return delete_central_service
