import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_cs_add_client_to_member.add_client_to_member import test_create_registration_request


class XroadAddClientToMemberExtensions(unittest.TestCase):
    """
    MEMBER_15(extensions) Create a Security Server Client Registration Request
    RIA URL: https://jira.ria.ee/browse/XT-465
    RIA URL: https://jira.ria.ee/browse/XT-367, https://jira.ria.ee/browse/XTKB-40
    Depends on finishing other test(s): XroadApproveRequests
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_add_client_extensions(self):
        main = MainController(self)
        main.test_number = 'MEMBER_15_extensions'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        server = xroad.split_xroad_id(main.config.get('ss1.server_id'), type='SERVER')
        client = xroad.split_xroad_subsystem(main.config.get('ss1.client_id'))
        client['subsystem'] = 'TESTSUB'
        client_name = main.config.get('ss1.client_name')
        existing_client = xroad.split_xroad_subsystem(main.config.get('ss1.client_id'))
        existing_client['name'] = main.config.get('ss1.client_name')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        create_registration_request = test_create_registration_request(main, server, client_name,
                                                                       client=client,
                                                                       duplicate_client=existing_client,
                                                                       log_checker=log_checker)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            create_registration_request()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
