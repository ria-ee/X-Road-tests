import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_cs_add_member.add_cs_member import add_member_to_cs
from view_models import popups


class XroadAddCsMember(unittest.TestCase):
    """
    MEMBER_10 1-2, 4-7, 4a Add an X-Road Member
    RIA URL: https://jira.ria.ee/browse/XT-362
    RIA URL: https://jira.ria.ee/browse/XT-362, https://jira.ria.ee/browse/XTKB-38
    Depends on finishing other test(s): MEMBER_01
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_a_xroad_add_cs_member(self):
        main = MainController(self)
        main.test_number = 'MEMBER_10.a'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        ss_1_client_name = main.config.get('ss1.client_name')
        ss_1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_2_name = main.config.get('ss1.client2_name')
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))

        ss_1_client = {'name': ss_1_client_name, 'class': ss_1_client['class'], 'code': ss_1_client['code']}
        ss_1_client_2 = {'name': ss1_client_2_name, 'class': ss1_client_2['class'], 'code': ss1_client_2['code'],
                         'subsystem_code': ss1_client_2['subsystem']}
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_member_to_cs(main, ss_1_client, log_checker)
            popups.close_all_open_dialogs(main)
            add_member_to_cs(main, ss_1_client_2)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_b_xroad_add_cs_existing_member(self):
        main = MainController(self)
        main.test_number = 'MEMBER_10.b'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        ss_1_client_name = main.config.get('ss1.client_name')
        ss_1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))

        ss_1_client = {'name': ss_1_client_name, 'class': ss_1_client['class'], 'code': ss_1_client['code']}
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_member_to_cs(main, ss_1_client, exists=True, log_checker=log_checker)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

