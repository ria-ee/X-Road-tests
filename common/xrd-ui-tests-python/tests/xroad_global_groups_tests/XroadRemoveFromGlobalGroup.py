import unittest

from helpers import xroad, soaptestclient, auditchecker
from main.maincontroller import MainController
from tests.xroad_add_to_acl_218 import add_to_acl
from tests.xroad_global_groups_tests import global_groups_tests


class XroadRemoveFromGlobalGroup(unittest.TestCase):
    """
    SERVICE_34 Remove Global Group Members
    RIA URL: https://jira.ria.ee/browse/XTKB-177
    Depends on finishing other test(s): global group adding
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_a_remove_selected_from_global_group(self):
        main = MainController(self)

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')
        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        group = main.config.get('cs.global_group')

        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        client['name'] = main.config.get('ss1.client_name')
        testservice_name = main.config.get('services.test_service')
        provider = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        identifier = main.config.get('cs.identifier')
        testclient_params = {
            'xroadProtocolVersion': main.config.get('services.xroad_protocol'),
            'xroadIssue': main.config.get('services.xroad_issue'),
            'xroadUserId': main.config.get('services.xroad_userid'),
            'serviceMemberInstance': provider['instance'],
            'serviceMemberClass': provider['class'],
            'serviceMemberCode': provider['code'],
            'serviceSubsystemCode': provider['subsystem'],
            'serviceCode': xroad.get_service_name(testservice_name),
            'serviceVersion': xroad.get_service_version(testservice_name),
            'memberInstance': client['instance'],
            'memberClass': client['class'],
            'memberCode': client['code'],
            'subsystemCode': client['subsystem'],
            'requestBody': main.config.get('services.testservice_request_body')
        }

        sync_retry = main.config.get('services.request_sync_delay')
        sync_max_seconds = main.config.get('services.request_sync_timeout')
        '''Not expected faults, query fails'''
        faults_unsuccessful = ['Server.ClientProxy.SslAuthenticationFailed', 'Server.ServerProxy.AccessDenied']
        '''Expected faults'''
        faults_successful = ['Server.ServerProxy.ServiceFailed']
        query_url = main.config.get('ss1.service_path')
        query_filename = main.config.get('services.request_template_filename')
        query = main.get_xml_query(query_filename)
        testclient = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                   retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                   faults_successful=faults_successful,
                                                   faults_unsuccessful=faults_unsuccessful,
                                                   params=testclient_params)
        wsdl_url = main.config.get('wsdl.remote_path').format(
            main.config.get('wsdl.service_wsdl'))
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)

        subject_list = ['GLOBALGROUP : {0} : {1}'.format(identifier, group)]
        test_configure_service_acl = add_to_acl.test_add_subjects(case=main, client=client,
                                                                  client_name=client['name'],
                                                                  wsdl_url=wsdl_url,
                                                                  service_name=testservice_name,
                                                                  service_subjects=subject_list,
                                                                  remove_data=False,
                                                                  allow_remove_all=False,
                                                                  remove_current=True)
        test_remove_selected_from_global_group = global_groups_tests.test_remove_from_global_group(main, group=group,
                                                                                                   testclient=testclient,
                                                                                                   log_checker=log_checker,
                                                                                                   delete_member=client
                                                                                                   )

        restore_acl = global_groups_tests.restore_acl(main, client['name'], client, testservice_name, wsdl_url,
                                                      subject_list)
        try:
            main.log('Add global group to {0} service ACL'.format(testservice_name))
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            current_subjects = test_configure_service_acl()

            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_remove_selected_from_global_group()

            main.log('Restore service ACL')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            restore_acl(current_subjects)
        finally:
            main.tearDown()

    def test_b_remove_all_from_global_group(self):
        main = MainController(self)

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')
        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        group = main.config.get('cs.global_group')

        client_1 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        client_1['name'] = main.config.get('ss1.client2_name')
        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        client['name'] = main.config.get('ss1.client_name')
        testservice_name = main.config.get('services.test_service')
        provider = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        identifier = main.config.get('cs.identifier')
        testclient_params = {
            'xroadProtocolVersion': main.config.get('services.xroad_protocol'),
            'xroadIssue': main.config.get('services.xroad_issue'),
            'xroadUserId': main.config.get('services.xroad_userid'),
            'serviceMemberInstance': provider['instance'],
            'serviceMemberClass': provider['class'],
            'serviceMemberCode': provider['code'],
            'serviceSubsystemCode': provider['subsystem'],
            'serviceCode': xroad.get_service_name(testservice_name),
            'serviceVersion': xroad.get_service_version(testservice_name),
            'memberInstance': client_1['instance'],
            'memberClass': client_1['class'],
            'memberCode': client_1['code'],
            'subsystemCode': client_1['subsystem'],
            'requestBody': main.config.get('services.testservice_request_body')
        }

        sync_retry = main.config.get('services.request_sync_delay')
        sync_max_seconds = main.config.get('services.request_sync_timeout')
        '''Not expected faults, query fails'''
        faults_unsuccessful = ['Server.ClientProxy.SslAuthenticationFailed', 'Server.ServerProxy.AccessDenied']
        '''Expected faults'''
        faults_successful = ['Server.ServerProxy.ServiceFailed']
        query_url = main.config.get('ss1.service_path')
        query_filename = main.config.get('services.request_template_filename')
        query = main.get_xml_query(query_filename)
        testclient = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                   retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                   faults_successful=faults_successful,
                                                   faults_unsuccessful=faults_unsuccessful,
                                                   params=testclient_params)
        wsdl_url = main.config.get('wsdl.remote_path').format(
            main.config.get('wsdl.service_wsdl'))
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)

        subject_list = ['GLOBALGROUP : {0} : {1}'.format(identifier, group)]
        test_configure_service_acl = add_to_acl.test_add_subjects(case=main, client=client,
                                                                  client_name=client['name'],
                                                                  wsdl_url=wsdl_url,
                                                                  service_name=testservice_name,
                                                                  service_subjects=subject_list,
                                                                  remove_data=False,
                                                                  allow_remove_all=False,
                                                                  remove_current=True)
        test_remove_all_from_global_group = global_groups_tests.test_remove_from_global_group(main, group=group,
                                                                                              testclient=testclient,
                                                                                              log_checker=log_checker)
        restore_acl = global_groups_tests.restore_acl(main, client['name'], client, testservice_name, wsdl_url,
                                                      subject_list)

        try:
            main.log('Add global group to {0} service ACL'.format(testservice_name))
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            current_subjects = test_configure_service_acl()

            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_remove_all_from_global_group()

            main.log('Restore service ACL')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            restore_acl(current_subjects)
        finally:
            main.tearDown()
