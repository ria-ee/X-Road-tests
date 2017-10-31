import time
import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss_2_2_1 import add_client_to_ss, \
    add_sub_as_client_to_member
from tests.xroad_decline_registration_request.XroadDeclineRegistrationRequest import decline_request
from tests.xroad_logging_in_cs_2111.logging_in_cs_2_11_1 import add_subsystem_to_member
from tests.xroad_logging_service_ss_2112.logging_service_ss_2_11_2 import certify_client_in_ss


class testDeclineRegistrationRequest(unittest.TestCase):
    """
    MEMBER_38 Decline a Registration Request
    RIA URL: https://jira.ria.ee/browse/XTKB-137
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.9.4
    """
    def test_decline_registration_request(self):
        main = MainController(self)
        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')
        server_name = main.config.get('ss1.server_name')

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        member = xroad.split_xroad_id(main.config.get('ss1.server_id'))
        member['subsystem_code'] = member['subsystem'] = 'declinesub'
        member['name'] = main.config.get('ss1.server_name')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)

        try:
            main.log('Creating client registration request, which will be declined')
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_subsystem_to_member(main, member=member)
            time.sleep(120)
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            add_client_to_ss(main, member)
            certify_client_in_ss(main, ss_host, ss_user, ss_pass, member)

            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_sub_as_client_to_member(main, server_name, member, wait_input=2,
                                        step='Adding subsystem')
        finally:
            main.log('MEMBER_38 Decline a Registration Request')
            decline_request(main, log_checker=log_checker)()
            main.tearDown()
