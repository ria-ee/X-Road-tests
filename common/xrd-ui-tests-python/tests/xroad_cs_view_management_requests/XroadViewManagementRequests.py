import unittest

from main.maincontroller import MainController
from tests.xroad_cs_view_management_requests.view_management_requests import test_view_management_request


class XroadViewManagementRequest(unittest.TestCase):
    """
    MEMBER_34 View Management Requests
    RIA URL: https://jira.ria.ee/browse/XT-386, https://jira.ria.ee/browse/XTKB-161
    Depends on finishing other test(s): client deletion, client registration, certificate registration, certificate deletion
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_view_management_requests(self):
        main = MainController(self)

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        view_management_requests = test_view_management_request(main)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            view_management_requests()
        finally:
            main.tearDown()
