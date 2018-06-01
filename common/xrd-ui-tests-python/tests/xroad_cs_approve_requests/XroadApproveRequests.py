import unittest

import time

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import approve_requests
from tests.xroad_cs_approve_requests.approve_requests import check_client_registration_status, check_client_in_cs


class XroadApproveRequests(unittest.TestCase):
    """
    MEMBER_02 4. Security Server subsystem state is registered
    MEMBER_37 Approve a Security Server Client Registration Request
    RIA URL: https://jira.ria.ee/browse/XT-389, https://jira.ria.ee/browse/XTKB-44
    RIA URL: https://jira.ria.ee/browse/XTKB-215
    Depends on finishing other test(s): MEMBER_56
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_approve_requests(self):
        main = MainController(self)
        main.test_number = 'MEMBER_37'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)

        ss1_host = main.config.get('ss1.host')
        ss1_user = main.config.get('ss1.user')
        ss1_pass = main.config.get('ss1.pass')
        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')

        ss1_client_2_name = main.config.get('ss1.client2_name')
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_name = main.config.get('ss1.client_name')
        ss1_server_name = main.config.get('ss1.server_name')
        ss2_server_name = main.config.get('ss2.server_name')
        ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                       'subsystem_code': ss1_client['subsystem'], 'server_name': ss1_server_name}
        ss_1_client_2 = {'name': ss1_client_2_name, 'class': ss1_client_2['class'], 'code': ss1_client_2['code'],
                         'subsystem_code': ss1_client_2['subsystem'], 'server_name': ss2_server_name}

        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        ss2_client_name = main.config.get('ss2.client_name')
        ss_2_client = {'name': ss2_client_name, 'class': ss2_client['class'], 'code': ss2_client['code'],
                       'subsystem_code': ss2_client['subsystem'], 'server_name': ss2_server_name}
        approve_ss2_client1 = False

        ss2_client_2 = xroad.split_xroad_id(main.config.get('ss2.client2_id'))
        ss2_client_2_name = main.config.get('ss2.client2_name')
        ss_2_client_2 = {'name': ss2_client_2_name, 'class': ss2_client_2['class'], 'code': ss2_client_2['code'],
                         'subsystem_code': ss2_client_2['subsystem'], 'server_name': ss2_server_name}
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            approve_requests(main, cancel_confirmation=True, use_case='MEMBER_37', log_checker=log_checker)
            approve_requests(main, use_case='MEMBER_37')
            main.reload_webdriver(cs_host, cs_user, cs_pass)

            check_client_in_cs(main, [ss_1_client])
            if approve_ss2_client1:
                main.reload_webdriver(cs_host, cs_user, cs_pass)
                check_client_in_cs(main, [ss_2_client])


            main.log('Waiting until servers synced')
            time.sleep(120)

            main.reload_webdriver(ss1_host, ss1_user, ss1_pass)
            check_client_registration_status(main, ss_1_client)
            check_client_registration_status(main, ss_1_client_2)

            main.reload_webdriver(ss2_host, ss2_user, ss2_pass)
            if approve_ss2_client1:
                check_client_registration_status(main, ss_2_client)
            check_client_registration_status(main, ss_2_client_2)

        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
