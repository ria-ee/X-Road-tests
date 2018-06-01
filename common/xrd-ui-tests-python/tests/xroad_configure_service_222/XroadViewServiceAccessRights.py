import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import configure_service
from tests.xroad_add_to_acl_218 import add_to_acl
from tests.xroad_configure_service_222 import configure_add_wsdl


class XroadViewServiceAccessRights(unittest.TestCase):
    """
    SERVICE_16 View the Access Rights of a Service
    RIA URL: https://jira.ria.ee/browse/XTKB-171
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_xroad_view_service_access_rights(self):
        main = MainController(self)

        main.test_number = 'SERVICE_16'
        main.test_name = self.__class__.__name__

        client_name = main.config.get('ss2.client_name')

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        test_view_service_access_rights = configure_service.view_service_access_rights(main, client, client_name, wsdl_url)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_view_service_access_rights()
        finally:
            main.tearDown()
