import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import configure_service


class XroadViewServiceAccessRights(unittest.TestCase):
    """
    SERVICE_16 View the Access Rights of a Service
    RIA URL: https://jira.ria.ee/browse/XTKB-171
    Depends on finishing other test(s): configure service
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_xroad_view_service_access_rights(self):
        main = MainController(self)

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client_name = main.config.get('ss2.client_name')
        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        remote_path = main.config.get('wsdl.remote_path')
        service_wsdl = main.config.get('wsdl.service_wsdl')
        wsdl_url = remote_path.format(service_wsdl)

        test_view_service_access_rights = configure_service.view_service_access_rights(main, client, client_name, wsdl_url)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_view_service_access_rights()
        finally:
            main.tearDown()
