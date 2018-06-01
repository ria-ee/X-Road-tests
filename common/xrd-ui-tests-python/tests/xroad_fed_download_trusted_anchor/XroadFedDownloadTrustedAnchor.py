import unittest

from main.maincontroller import MainController
from tests.xroad_fed_download_trusted_anchor.download_trusted_anchor import test_download_trusted_anchor


class XroadFedDownloadTrustedAnchor(unittest.TestCase):
    """
    FED_06 Download a Trusted Anchor
    RIA URL: https://jira.ria.ee/browse/XTKB-231
    Depends on finishing other test(s): FED_01
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_download_trusted_anchor(self):
        main = MainController(self)
        main.test_number = 'UC FED_06'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        download_trusted_anchor = test_download_trusted_anchor(main)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            download_trusted_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
