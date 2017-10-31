import re
import time

from selenium.webdriver.common.by import By

from helpers import xroad, soaptestclient
from view_models import clients_table_vm, popups
# These faults are checked when we need the result to be unsuccessful. Otherwise the checking function returns True.
from view_models.log_constants import DISABLE_WSDL

faults_unsuccessful = ['Server.ServerProxy.ServiceDisabled']
# These faults are checked when we need the result to be successful. Otherwise the checking function returns False.
faults_successful = ['Server.ServerProxy.AccessDenied', 'Server.ServerProxy.UnknownService',
                     'Server.ServerProxy.ServiceDisabled', 'Server.ClientProxy.*', 'Client.*']


def test_disable_wsdl(case, client=None, client_name=None, client_id=None, wsdl_index=None, wsdl_url=None,
                      requester=None, log_checker=None):
    '''
    MainController test function. Disables a WSDL for a client and tests if queries fail after.
    :param client: dict | None - client XRoad data
    :param client_name: string | None - name of the client whose ACL we modify
    :param client_id: string | None - XRoad ID of the client whose ACL we modify
    :param wsdl_index: int | None - index (zero-based) for WSDL we select from the list
    :param wsdl_url: str | None - URL for WSDL we select from the list
    :param requester: dict | None - requester XRoad data
    :return:
    '''

    self = case
    client_id = xroad.get_xroad_subsystem(client)

    wsdl_disabled_class = self.config.get_string('wsdl.disabled_class', 'disabled')

    query_url = self.config.get('ss1.service_path')
    query_filename = self.config.get('services.request_template_filename')
    query = self.get_xml_query(query_filename)

    service_name = self.config.get('services.test_service_2')

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

    testclient_http = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                    retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                    faults_successful=faults_successful,
                                                    faults_unsuccessful=faults_unsuccessful, params=testclient_params)

    def disable_wsdl():
        """
        :return: None
        """

        # TEST PLAN 2.2.6 deactivate WSDL
        self.log('*** 2.2.6 / XT-470')
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()

        # Create an out of order message with timestamp and milliseconds. We need to compare the error we get later.
        out_of_order_message = 'Out of order: {0}'.format(int(round(time.time() * 1000)))

        # TEST PLAN 2.2.6-1 test query from TS1 client CLIENT1:sub to service bodyMassIndex. Query should succeed.
        self.log('2.2.6-1 test query {0} to bodyMassIndex. Query should succeed.'.format(query_filename))

        case.is_true(testclient_http.check_success(), msg='2.2.6-1 test query failed')

        # TEST PLAN 2.2.6-2 disable/deactivate the WSDL.
        self.log('2.2.6-2 disable the WSDL.')

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        # Find the table that lists all WSDL files and services
        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        # Wait until that table is visible (opened in a popup)
        self.wait_until_visible(services_table)

        # Find the service under the specified WSDL in service list
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

        # Find and click the "Disable" button to enable the WSDL.
        self.by_id(popups.CLIENT_DETAILS_POPUP_DISABLE_WSDL_BTN_ID).click()

        # Wait until the "Disable WSDL" dialog opens.
        self.wait_until_visible(popups.DISABLE_WSDL_POPUP_XPATH, type=By.XPATH)

        self.log('SERVICE_13 3a. Disabling WSDL confirmation dialog is cancelled')
        self.by_xpath(popups.DISABLE_WSDL_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_jquery()

        # Find and click the "Disable" button to enable the WSDL.
        self.by_id(popups.CLIENT_DETAILS_POPUP_DISABLE_WSDL_BTN_ID).click()

        # Get the OK button
        disable_dialog_ok_button = self.by_xpath(popups.DISABLE_WSDL_POPUP_OK_BTN_XPATH)

        # Get the disabled notice input.
        disable_notice_input = self.by_id(popups.DISABLE_WSDL_POPUP_NOTICE_ID)

        # Clear the disabled notice input and set a new text
        self.input(disable_notice_input, out_of_order_message)

        # Click "OK" button to save the data
        disable_dialog_ok_button.click()

        # Wait until ajax query finishes
        self.wait_jquery()

        if log_checker is not None:
            expected_log_msg = DISABLE_WSDL
            self.log('SERVICE_13 6. System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found)

        # TEST PLAN 2.2.6-2 sub: check that the WSDL is written in red text (class "disabled") and starts with
        # "WSDL DISABLED"

        # Try to find the same WSDL row again
        wsdl_row = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index,
                                                                      wsdl_url=wsdl_url)

        # Find the second cell in the row - this is the "WSDL xxx" text.
        wsdl_element = wsdl_row.find_elements_by_tag_name('td')[1]

        # Check that WSDL element has class "disabled" (red text)
        self.is_equal(wsdl_disabled_class in self.get_classes(wsdl_row), True,
                      msg='2.2.6-4 error - WSDL still has "{0}" class (red text): {1}'.format(wsdl_disabled_class,
                                                                                              wsdl_url))

        # Get the WSDL row text and verify that it starts with "WSDL DISABLED". As we have a regex for it that matches
        # only an empty string OR the "DISABLED" part, we can compare with the empty string (in case someone wants to
        # change the "DISABLED" text in the future)
        self.log(wsdl_element.text + " " + popups.CLIENT_DETAILS_POPUP_WSDL_URL_REGEX)
        wsdl_text = re.match(popups.CLIENT_DETAILS_POPUP_WSDL_URL_REGEX, wsdl_element.text).group(1)
        self.not_equal(wsdl_text, '', msg='2.2.6-4 WSDL row starts with "WSDL DISABLED": {0}'.format(wsdl_url))

        # TEST PLAN 2.2.6-3 test query from TS1 client CLIENT1:sub to service bodyMassIndex. Query should fail.
        self.log('2.2.6-3 test query {0} to bodyMassIndex. Query should fail.'.format(query_filename))
        case.is_true(testclient_http.check_fail(), msg='2.2.6-3 test query succeeded')

        # Check if the returned message was the same we specified earlier. As this is appended to a generic error, only
        # compare the ending. We should have unique enough message using milliseconds.
        self.is_equal(testclient_http.fault_message.endswith(out_of_order_message), True,
                      msg='2.2.6-3 fault message expected "{0}", got "{1}"'.format(out_of_order_message,
                                                                                   testclient_http.fault_message))

    return disable_wsdl


def test_enable_wsdl(case, client=None, client_name=None, client_id=None, wsdl_index=None, wsdl_url=None,
                     requester=None):
    '''
    MainController test function. Re-enables a WSDL for a client and tests if queries work after.
    :param client: dict | None - client XRoad data
    :param client_name: string | None - name of the client whose ACL we modify
    :param client_id: string | None - XRoad ID of the client whose ACL we modify
    :param wsdl_index: int | None - index (zero-based) for WSDL we select from the list
    :param wsdl_url: str | None - URL for WSDL we select from the list
    :param requester: dict | None - requester XRoad data
    :return:
    '''

    self = case
    client_id = xroad.get_xroad_subsystem(client)

    query_url = self.config.get('ss1.service_path')
    query_filename = self.config.get('services.request_template_filename')
    query = self.get_xml_query(query_filename)

    service_name = self.config.get('services.test_service_2')

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

    testclient_http = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                    retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                    faults_successful=faults_successful,
                                                    faults_unsuccessful=faults_unsuccessful, params=testclient_params)

    wsdl_disabled_class = self.config.get_string('wsdl.disabled_class', 'disabled')

    def enable_wsdl():
        """
        :param self: MainController class object
        :return: None
        ''"""

        self.log('2.2.6 enable_wsdl')

        # TEST PLAN 2.2.6-4 reactivate the WSDL
        self.log('2.2.6-4 reactivate the WSDL.')

        # Enable WSDL that we added to restore original state.

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        # Find the table that lists all WSDL files and services
        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        # Wait until that table is visible (opened in a popup)
        self.wait_until_visible(services_table)

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

        # Find and click the "Enable" button to enable the WSDL.
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()

        # Wait until ajax query finishes
        self.wait_jquery()

        # TEST PLAN 2.2.6-4 sub: Check that the WSDL is in black (does not have class "disabled") and does not start
        # with "DISABLED".

        # Now try to find the same WSDL again
        wsdl_row = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=wsdl_index,
                                                                      wsdl_url=wsdl_url)

        # Find the second cell in the row - this is the "WSDL xxx" text.
        wsdl_element = wsdl_row.find_elements_by_tag_name('td')[1]

        # Check that WSDL element does not have class "disabled" (red text)
        self.is_equal(wsdl_disabled_class in self.get_classes(wsdl_row), False,
                      msg='2.2.6-4 error - WSDL still has "{0}" class (red text): {1}'.format(wsdl_disabled_class,
                                                                                              wsdl_url))

        # Get the WSDL row text and verify that it starts with "WSDL DISABLED". As we have a regex for it that matches
        # only an empty string OR the "DISABLED" part, we can compare with the empty string (in case someone wants to
        # change the "DISABLED" text in the future)
        self.log(wsdl_element.text + " " + popups.CLIENT_DETAILS_POPUP_WSDL_URL_REGEX)
        wsdl_text = re.match(popups.CLIENT_DETAILS_POPUP_WSDL_URL_REGEX, wsdl_element.text).group(1)
        self.is_equal(wsdl_text, '', msg='2.2.6-4 WSDL row starts with "WSDL DISABLED": {0}'.format(wsdl_url))

        # TEST PLAN 2.2.6-5 test query from TS1 client CLIENT1:sub to service bodyMassIndex. Query should succeed.
        self.log('2.2.6-5 test query {0} to bodyMassIndex. Query should succeed.'.format(query_filename))
        case.is_true(testclient_http.check_success(), msg='2.2.6-5 test query failed')

    return enable_wsdl
