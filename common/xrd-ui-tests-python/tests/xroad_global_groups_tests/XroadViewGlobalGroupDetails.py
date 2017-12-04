import unittest

from main.maincontroller import MainController
from tests.xroad_global_groups_tests import global_groups_tests


class XroadViewGlobalGroupDetails(unittest.TestCase):
    """
    SERVICE_31 View Global Group Details
    RIA URL: https://jira.ria.ee/browse/XTKB-176
    Depends on finishing other test(s): global group adding
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_view_global_group_details(self):
        main = MainController(self)

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        test_view_global_group_details = global_groups_tests.test_view_global_group_details(main)

        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_view_global_group_details()
        finally:
            main.tearDown()
