import unittest

from main.maincontroller import MainController
from tests.xroad_fed_view_trusted_anchor.view_trusted_anchor import test_view_trusted_anchors


class XroadFedViewTrustedAnchor(unittest.TestCase):
    """
    FED_01 View Trusted Anchors
    RIA URL: https://jira.ria.ee/browse/XTKB-226
    Depends on finishing other test(s): FED_02
    Requires helper scenarios: None
    X-Road version: 6.16.0
    """
    def test_view_trusted_anchor(self):
        main = MainController(self)

        main.test_number = 'UC FED_01'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        view_trusted_anchors = test_view_trusted_anchors(main)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            view_trusted_anchors()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
