import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_cs_add_client_to_member.add_client_to_member import add_subsystem_to_server_client, \
    add_sub_as_client_to_member, test_create_registration_request


class XroadAddClientToMember(unittest.TestCase):
    """
    MEMBER_15 Create a Security Server Client Registration Request
    RIA URL: https://jira.ria.ee/browse/XT-465
    RIA URL: https://jira.ria.ee/browse/XT-367, https://jira.ria.ee/browse/XTKB-40
    Depends on finishing other test(s): XroadCertifyClient
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_add_client_to_member(self):
        main = MainController(self)

        main.test_number = 'MEMBER_15'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)

        ss1_client_2_name = main.config.get('ss1.client2_name')
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_name = main.config.get('ss1.client_name')
        ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                       'subsystem_code': ss1_client['subsystem']}
        ss_1_client_2 = {'name': ss1_client_2_name, 'class': ss1_client_2['class'], 'code': ss1_client_2['code'],
                         'subsystem_code': ss1_client_2['subsystem']}

        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        ss2_client_name = main.config.get('ss2.client_name')
        ss_2_client = {'name': ss2_client_name, 'class': ss2_client['class'], 'code': ss2_client['code'],
                       'subsystem_code': ss2_client['subsystem']}
        ss2_client_2 = xroad.split_xroad_id(main.config.get('ss2.client2_id'))
        ss2_client_2_name = main.config.get('ss2.client2_name')
        ss_2_client_2 = {'name': ss2_client_2_name, 'class': ss2_client_2['class'], 'code': ss2_client_2['code'],
                         'subsystem_code': ss2_client_2['subsystem']}
        ss2_server_name = main.config.get('ss2.server_name')
        ss1_server_name = main.config.get('ss1.server_name')
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_subsystem_to_server_client(main, ss2_server_name, ss_2_client, log_checker=log_checker)
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_sub_as_client_to_member(main, ss2_server_name, ss_2_client_2)
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_sub_as_client_to_member(main, ss1_server_name, ss_1_client_2)
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_sub_as_client_to_member(main, ss1_server_name, ss_1_client)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

