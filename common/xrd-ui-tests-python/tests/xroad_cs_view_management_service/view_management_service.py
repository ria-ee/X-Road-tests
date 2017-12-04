import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_cs_view_management_service.XroadViewManagementService import view_management_service


class xroad_view_management_service(unittest.TestCase):
    """
    MEMBER_32 View the Configuration for Management Services
    RIA URL: https://jira.ria.ee/browse/XT-384, https://jira.ria.ee/browse/XTKB-136
    Depends on finishing other test(s): MEMBER_57
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_view_management_service(self):
        main = MainController(self)
        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        client = xroad.split_xroad_id(main.config.get('ss1.management_id'))
        server = xroad.split_xroad_id(main.config.get('ss1.server_id'))
        service_provider = xroad.get_xroad_path(client, client_type='SUBSYSTEM')
        server_name = main.config.get('ss1.server_name')
        management_server_name = xroad.get_xroad_path(server, client_type='SERVER')
        wsdl_url = main.config.get('wsdl.management_service_wsdl_url')
        service_address_uri = main.config.get('cs.service_url')
        owners_group = main.config.get('cs.owners_group')
        test_view_management_service = view_management_service(main, service_provider, server_name,
                                                               management_server_name, wsdl_url, service_address_uri,
                                                               owners_group)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_view_management_service()
        finally:
            main.tearDown()
