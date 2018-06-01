import unittest

import time

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_ss_delete_client.delete_client import remove_client


class XroadDeleteClient(unittest.TestCase):
    """
    MEMBER_53 Delete a Security Server Client
    RIA URL: https://jira.ria.ee/browse/XT-405, https://jira.ria.ee/browse/XTKB-34, https://jira.ria.ee/browse/XTKB-124
    Depends on finishing other test(s): MEMBER_26
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_delete_client(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'MEMBER_53'
        main.test_name = self.__class__.__name__

        ss1_host = main.config.get('ss1.host')
        ss1_user = main.config.get('ss1.user')
        ss1_pass = main.config.get('ss1.pass')

        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')

        ss1_ssh_host = main.config.get('ss1.ssh_host')
        ss1_ssh_user = main.config.get('ss1.ssh_user')
        ss1_ssh_pass = main.config.get('ss1.ssh_pass')
        log_checker = auditchecker.AuditChecker(ss1_ssh_host, ss1_ssh_user, ss1_ssh_pass)

        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        ss2_client_2 = xroad.split_xroad_id(main.config.get('ss2.client2_id'))
        try:
            main.reload_webdriver(ss1_host, ss1_user, ss1_pass)
            remove_client(main, ss1_client, delete_cert=True, cancel_deletion=True, log_checker=log_checker)
            remove_client(main, ss1_client_2, deny_cert_deletion=True)
            main.log('Wait until client state is unregistered from cs subsystem deletion')
            time.sleep(120)
            main.reload_webdriver(ss2_host, ss2_user, ss2_pass)
            remove_client(main, ss2_client, delete_cert=False)
            remove_client(main, ss2_client_2)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
