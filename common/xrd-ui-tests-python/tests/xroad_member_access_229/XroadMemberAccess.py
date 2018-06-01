# coding=utf-8
import unittest

import xroad_member_access
from main.maincontroller import MainController
from helpers import xroad


class XroadMemberAccess(unittest.TestCase):
    """
    Test X-Road Member access to services with test queries.
    SERVICE_17 Add Access Rights to a Service
    SERVICE_18 Remove Access Rights from a Service
    RIA URL: https://jira.ria.ee/browse/XT-274
    RIA URL: https://jira.ria.ee/browse/XT-275
    Depends on finishing other test(s): XroadConfigureService
    Requires helper scenarios: xroad_add_to_acl_218
    X-Road version: 6.16.0
    """

    def test_xroad_member_access(self):

        main = MainController(self)

        # Set test name and number
        main.test_number = 'SERVICE_17/18'
        main.test_name = self.__class__.__name__

        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))
        service_name = main.config.get('services.test_service')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss2.client2_id'))

        # Configure the test
        test_xroad_member_access = xroad_member_access.test_xroad_member_access(main, client=client,
                                                                                requester=requester,
                                                                                wsdl_url=wsdl_url,
                                                                                service_name=service_name)
        # Set Security Server 2
        main.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)

        try:
            # Test local TLS
            test_xroad_member_access()
        except:
            main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown(save_exception=False)
