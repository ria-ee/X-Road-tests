import unittest

from helpers import auditchecker, xroad
from main.maincontroller import MainController
from tests.xroad_global_groups_tests import global_groups_tests


class XroadMemberRemoveFromGlobalGroup(unittest.TestCase):
    """
    SERVICE_38 Remove an X-Road Member from a Global Group
    RIA URL: https://jira.ria.ee/browse/XTKB-183
    Depends on finishing other test(s): member add to global group
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_member_remove_from_global_group(self):
        main = MainController(self)

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        group_name = main.config.get('cs.global_group')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        member_name = main.config.get('ss1.client_name')
        member_code = xroad.split_xroad_id(main.config.get('ss1.client_id'))['code']

        test_member_remove_from_global_group = global_groups_tests.test_member_remove_from_global_group(main, member_name,
                                                                                                        member_code,
                                                                                                        group_name,
                                                                                                        log_checker=log_checker)

        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_member_remove_from_global_group()
        finally:
            main.tearDown()
