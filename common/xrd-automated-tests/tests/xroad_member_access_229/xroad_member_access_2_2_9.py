# coding=utf-8

from view_models import clients_table_vm, popups
from helpers import xroad, soaptestclient
from tests.xroad_add_to_acl_218 import add_to_acl_2_1_8

# These faults are checked when we need the result to be unsuccessful. Otherwise the checking function returns True.
faults_unsuccessful = ['Server.ServerProxy.AccessDenied']
# These faults are checked when we need the result to be successful. Otherwise the checking function returns False.
faults_successful = ['Server.ServerProxy.AccessDenied', 'Server.ServerProxy.UnknownService',
                     'Server.ServerProxy.ServiceDisabled', 'Server.ClientProxy.*', 'Client.*']


def test_xroad_member_access(case, client=None, client_id=None, requester=None, wsdl_index=None, wsdl_url=None,
                             service_name=None):
    '''
    MainController test function. Very similar to test_all_subjects but adds ALL subjects to a specified subject's ACL.
    :param client_name: string | None - name of the client whose ACL we modify
    :param client_id: string | None - XRoad ID of the client whose ACL we modify
    :param wsdl_index: int | None - index (zero-based) for WSDL we select from the list
    :param wsdl_url: str | None - URL for WSDL we select from the list
    :return:
    '''

    self = case
    client_id = xroad.get_xroad_subsystem(client)
    requester_id = xroad.get_xroad_subsystem(requester)

    query_url = self.config.get('ss2.service_path')
    query_filename = self.config.get('services.testservice_request_2_filename')
    query = self.get_xml_query(query_filename)

    sync_retry = 0
    sync_max_seconds = 0

    testclient = soaptestclient.SoapTestClient(url=query_url,
                                               body=query,
                                               retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                               faults_successful=faults_successful,
                                               faults_unsuccessful=faults_unsuccessful)

    def xroad_member_access():
        """
        :param self: MainController class object
        :return: None
        ''"""

        self.log('*** 2.2.9 / XT-473')

        # TEST PLAN 2.2.9 - giving access to XRoad member

        # TEST PLAN 2.2.9-1 test query from TS2 client TS2OWNER:sub to service bodyMassIndex. Query should fail.
        self.log('2.2.9-1 test query {0} to service bodyMassIndex. Query should fail.'.format(query_filename))

        case.is_true(testclient.check_fail(), msg='2.2.9-1 test query succeeded')

        # TEST PLAN 2.2.9-2 set bodyMassIndex address and ACL (give access to TS2OWNER:sub)
        self.log('2.2.9-2 set bodyMassIndex address and ACL (give access to {0}'.format(requester_id))

        add_acl = add_to_acl_2_1_8.test_add_subjects(self, client=client, wsdl_url=wsdl_url,
                                                     service_name=service_name, service_subjects=[requester_id],
                                                     remove_data=False,
                                                     allow_remove_all=False)
        try:
            # Try to add subject to ACL
            add_acl()

            # TEST PLAN 2.2.9-3 test query from TS2 client TS2OWNER:sub to service bodyMassIndex. Query should succeed.
            self.log('2.2.9-3 test query {0} to service bodyMassIndex. Query should succeed.'.format(query_filename))

            case.is_true(testclient.check_success(), msg='2.2.9-3 test query failed')
        finally:
            # Always try to remove access

            # TEST PLAN 2.2.9-4 Remove added subject from test service ACL
            self.log('2.2.9-4 Remove added subject from test service ACL.')

            # Open client popup using shortcut button to open it directly at Services tab.
            clients_table_vm.open_client_popup_services(self, client_id=client_id)

            # Find the table that lists all WSDL files and services
            services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
            # Wait until that table is visible (opened in a popup)
            self.wait_until_visible(services_table)

            # Find the WSDL, expand it and select service
            clients_table_vm.client_services_popup_open_wsdl_acl(self, services_table=services_table,
                                                                 service_name=service_name,
                                                                 wsdl_index=wsdl_index, wsdl_url=wsdl_url)

            add_to_acl_2_1_8.remove_subjects_from_acl(self, [requester_id], select_duplicate=True)

        # This is not in the specification but we should still check if removal was successful.
        # TEST PLAN 2.2.9-4 test query from TS2 client TS2OWNER:sub to service bodyMassIndex. Query should fail.
        self.log('2.2.9-4 test query {0} to service bodyMassIndex. Query should fail.'.format(query_filename))
        case.is_true(testclient.check_fail(), msg='2.2.9-4 test query succeeded')

    return xroad_member_access
