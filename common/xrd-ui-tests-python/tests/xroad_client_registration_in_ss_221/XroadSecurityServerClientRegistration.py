from __future__ import absolute_import

import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss


class XroadSecurityServerClientRegistration(unittest.TestCase):
    """
    MEMBER_10 1-2, 4-5 Add an X-Road Member
    MEMBER_37 1-5, 3a Approve a Security Server Client Registration Request
    MEMBER_39 1-6, 3a Revoke a Registration Request
    MEMBER_47 1, 2, 4, 5, 6 Add a Client
    MEMBER_48 1-7, 2a, 4a Register a Security Server Client
    SS_29 Generate a Certificate Signing Request
    SS_39 Delete Certificate
    RIA URL: https://jira.ria.ee/browse/XT-362
    RIA URL: https://jira.ria.ee/browse/XT-389, https://jira.ria.ee/browse/XTKB-44
    RIA URL: https://jira.ria.ee/browse/XT-391, https://jira.ria.ee/browse/XTKB-45, https://jira.ria.ee/browse/XTKB-91
    RIA URL: https://jira.ria.ee/browse/XT-400, https://jira.ria.ee/browse/XTKB-46, https://jira.ria.ee/browse/XTKB-92
    RIA URL: https://jira.ria.ee/browse/XT-342
    RIA URL: https://jira.ria.ee/browse/XT-399
    RIA URL: https://jira.ria.ee/browse/XT-351
    Depends on finishing other test(s):
    Requires helper scenarios: xroad_ss_client_certification_213
    X-Road version: 6.16.0
    """

    def test_client_registration(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'MEMBER_47 / MEMBER_48 / MEMBER_37'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        remove_added_data = False

        main.management_services = xroad.split_xroad_subsystem(main.config.get('ss1.management_id'))
        cs_member = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        ss2_client_2 = xroad.split_xroad_id(main.config.get('ss2.client2_id'))

        cs_member_name = main.config.get('ss1.client_name')
        ss1_client_name = main.config.get('ss1.client_name')
        ss1_client_2_name = main.config.get('ss1.client2_name')
        ss2_client_name = main.config.get('ss2.client_name')
        ss2_client_2_name = main.config.get('ss2.client2_name')

        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        ss1_host = main.config.get('ss1.ssh_host')

        ss1_server_name = main.config.get('ss1.server_name')
        ss2_server_name = main.config.get('ss2.server_name')

        management_wsdl_url = main.config.get('wsdl.management_service_wsdl_url')
        management_client = xroad.split_xroad_id(main.config.get('ss1.management_id'))
        management_client_id = xroad.get_xroad_subsystem(management_client)

        main.log('TEST: REGISTERING SECURITY SERVER CLIENT')
        test_func = client_registration_in_ss.test_test(main, main.config.get('cs.host'),
                                                        main.config.get('cs.user'),
                                                        main.config.get('cs.pass'),
                                                        main.config.get('ss1.host'), main.config.get('ss1.user'),
                                                        main.config.get('ss1.pass'),
                                                        main.config.get('ss2.host'), main.config.get('ss2.user'),
                                                        main.config.get('ss2.pass'),
                                                        cs_new_member=cs_member, cs_member_name=cs_member_name,
                                                        ss1_client=ss1_client, ss1_client_name=ss1_client_name,
                                                        ss2_client=ss2_client, ss2_client_name=ss2_client_name,
                                                        ss1_client_2=ss1_client_2,
                                                        ss1_client_2_name=ss1_client_2_name,
                                                        ss2_client_2=ss2_client_2,
                                                        ss2_client_2_name=ss2_client_2_name,
                                                        remove_added_data=remove_added_data,
                                                        ss1_ssh_host=main.config.get('ss1.ssh_host'),
                                                        ss1_ssh_user=main.config.get('ss1.ssh_user'),
                                                        ss1_ssh_pass=main.config.get('ss1.ssh_pass'),
                                                        ss2_ssh_host=ss2_ssh_host,
                                                        ss2_ssh_user=ss2_ssh_user,
                                                        ss2_ssh_pass=ss2_ssh_pass,
                                                        ss1_host=ss1_host,
                                                        ss1_server_name=ss1_server_name,
                                                        ss2_server_name=ss2_server_name,
                                                        ca_ssh_host=main.config.get('ca.ssh_host'),
                                                        ca_ssh_username=main.config.get('ca.ssh_user'),
                                                        ca_ssh_password=main.config.get('ca.ssh_pass'),
                                                        global_group=main.config.get('cs.global_group'),
                                                        cs_ssh_host=main.config.get('cs.ssh_host'),
                                                        cs_ssh_user=main.config.get('cs.ssh_user'),
                                                        cs_ssh_pass=main.config.get('cs.ssh_pass'),
                                                        management_client_id=management_client_id,
                                                        management_wsdl_url=management_wsdl_url)
        test_func()
        main.tearDown()
