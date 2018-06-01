import unittest

from main.maincontroller import MainController
from tests.xroad_cs_view_central_services import view_central_service


class XroadViewCentralService(unittest.TestCase):
    """
    SERVICE_40 View Central Services
    RIA URL: https://jira.ria.ee/browse/XTKB-180
    Depends on finishing other test(s): central service adding
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_view_central_service(self):
        main = MainController(self)

        main.test_number = 'UC SERVICE_40'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        test_view_central_service = view_central_service.test_view_central_service(main)

        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_view_central_service()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
