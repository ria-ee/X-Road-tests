import unittest

from helpers import auditchecker,xroad
from main.maincontroller import MainController
from tests.xroad_local_group.xroad_local_group import add_group_to_client


class XroadAddLocalGroupExtensions(unittest.TestCase):
    """
    SERVICE_25 Add a Local Group for a Security Server Client
    RIA URL: https://jira.ria.ee/browse/XT-282, https://jira.ria.ee/browse/XTKB-36, https://jira.ria.ee/browse/XTKB-157
    Depends on finishing other test(s): XroadApproveRequests
    Requires helper scenarios: delete_local_group
    X-Road version: 6.16.0
    """

    def test_add_local_group(self):
        main = MainController(self)

        main.test_number = 'UC SERVICE_25'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ssh_host = main.config.get('ss1.ssh_host')
        ssh_user = main.config.get('ss1.ssh_user')
        ssh_pass = main.config.get('ss1.ssh_pass')

        log_checker = auditchecker.AuditChecker(ssh_host, ssh_user, ssh_pass)
        client_id = main.config.get('ss1.client2_id')
        client_name = main.config.get('ss1.client2_name')
        subsystem_row = xroad.split_xroad_subsystem(main.config.get('ss1.client2_id'))
        subsystem = subsystem_row['subsystem']
        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            add_group_to_client(main, client_id, log_checker=log_checker, client_name=client_name, subsystem=subsystem)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
