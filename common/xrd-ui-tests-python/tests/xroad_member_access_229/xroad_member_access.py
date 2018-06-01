# coding=utf-8

from view_models import clients_table_vm, popups
from helpers import xroad, soaptestclient
from tests.xroad_add_to_acl_218 import add_to_acl

# These faults are checked when we need the result to be unsuccessful. Otherwise the checking function returns True.
faults_unsuccessful = ['Server.ServerProxy.AccessDenied']
# These faults are checked when we need the result to be successful. Otherwise the checking function returns False.
faults_successful = ['Server.ServerProxy.AccessDenied', 'Server.ServerProxy.UnknownService',
                     'Server.ServerProxy.ServiceDisabled', 'Server.ClientProxy.*', 'Client.*']


def test_xroad_member_access(case, client=None, client_id=None, requester=None, wsdl_index=None, wsdl_url=None,
                             service_name=None):
    '''
    MainController test function. Tests XRoad member access.
    :return:
    '''

    self = case
    client_id = xroad.get_xroad_subsystem(client)
    requester_id = xroad.get_xroad_subsystem(requester)

    query_url = self.config.get('ss2.service_path')
    query_filename = self.config.get('services.request_template_filename')
    query = self.get_xml_query(query_filename)

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

    testclient = soaptestclient.SoapTestClient(url=query_url,
                                               body=query,
                                               retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                               faults_successful=faults_successful,
                                               faults_unsuccessful=faults_unsuccessful, params=testclient_params)

    def xroad_member_access():
        """
        :param self: MainController class object
        :return: None
        """

        self.log('*** SERVICE_17 / SERVICE_18')

        # UC SERVICE_17 / SERVICE_18 Giving and removing access to XRoad member

        # UC SERVICE_17/SERVICE_18 test query (1) from SS2 client subsystem to service bodyMassIndex. Query should fail.
        self.log('SERVICE_17/SERVICE_18 test query (1) {0} to service bodyMassIndex. Query should fail.'.format(
            query_filename))

        case.is_true(testclient.check_fail(), msg='2.2.9-1 test query (1) succeeded')

        # UC SERVICE_17/SERVICE_18 set bodyMassIndex address and ACL (give access to SS2 client subsystem)
        self.log('SERVICE_17/SERVICE_18 set bodyMassIndex address and ACL (give access to {0}'.format(requester_id))

        add_acl = add_to_acl.test_add_subjects(self, client=client, wsdl_url=wsdl_url,
                                               service_name=service_name, service_subjects=[requester_id],
                                               remove_data=False,
                                               allow_remove_all=False)
        try:
            # Try to add subject to ACL
            add_acl()

            # UC SERVICE_17/SERVICE_18 test query (2) from SS2 client subsystem to service bodyMassIndex. Query should succeed.
            self.log('SERVICE_17/SERVICE_18 test query (2) {0} to service bodyMassIndex. Query should succeed.'.format(
                query_filename))

            case.is_true(testclient.check_success(), msg='SERVICE_17/SERVICE_18 test query (2) failed')
        finally:
            # Always try to remove access

            # UC SERVICE_17/SERVICE_18 Remove added subject from test service ACL
            self.log('SERVICE_17/SERVICE_18 Remove added subject from test service ACL.')

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

            add_to_acl.remove_subjects_from_acl(self, [requester_id], select_duplicate=True)

        # Check if removal was successful - create a test query that should fail.
        # UC SERVICE_17/SERVICE_18 test query (3) from SS2 client subsystem to service bodyMassIndex. Query should fail.
        self.log('SERVICE_17/SERVICE_18 test query (3) {0} to service bodyMassIndex. Query should fail.'.format(
            query_filename))
        case.is_true(testclient.check_fail(), msg='SERVICE_17/SERVICE_18 test query (3) succeeded')

    return xroad_member_access
