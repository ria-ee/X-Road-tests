# coding=utf-8
import unittest

import xroad_member_access_2_2_9
from main.maincontroller import MainController
from helpers import xroad


class XroadMemberAccess(unittest.TestCase):
    def test_xroad_member_access(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.9'
        main.test_name = self.__class__.__name__

        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))
        service_name = main.config.get('services.test_service')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss2.client2_id'))

        # Configure the test
        test_xroad_member_access = xroad_member_access_2_2_9.test_xroad_member_access(main, client=client,
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
