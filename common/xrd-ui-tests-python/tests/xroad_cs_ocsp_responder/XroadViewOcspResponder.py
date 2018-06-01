import unittest
from main.maincontroller import MainController
import ocsp_responder


class XroadViewOcspResponder(unittest.TestCase):
    """
    TRUST_05 View the OCSP Responders of a CA
    RIA URL: https://jira.ria.ee/browse/XTKB-192
    Depends on finishing other test(s): Add OCSP
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_xroad_delete_ocsp_responder(self):
        main = MainController(self)

        main.test_number = 'UC TRUST_05'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ca_name = main.config.get('ca.name')
        ocsp_url = main.config.get('ca.ocs_host')

        test_view_ocsp_responder = ocsp_responder.test_view_ocsp_responder(main, ca_name=ca_name,
                                                                           ocsp_url=ocsp_url)

        try:
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            test_view_ocsp_responder()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
