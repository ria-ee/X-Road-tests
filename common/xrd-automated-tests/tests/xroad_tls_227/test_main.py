# coding=utf-8
import unittest

import local_tls_2_2_7
from main.maincontroller import MainController
from helpers import xroad


class XroadLocalTls(unittest.TestCase):
    def test_tls_227(self):
        MainController.driver_autostart = False
        main = MainController(self)

        main.log_in = True
        main.close_webdriver = True

        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        # Configure the tests
        test_local_tls = local_tls_2_2_7.test_tls(case=main, client=client, requester=requester)
        delete_local_tls = local_tls_2_2_7.test_delete_tls(case=main, client=client, requester=requester)

        try:
            # Test local TLS
            test_local_tls()
        except:
            main.log('XroadLocalTls: Failed to configure TLS for local service')
            # Delete internal certificates from the servers
            try:
                delete_local_tls()
            except:
                main.log('XroadLocalTls: failed to remove TLS from local service')
            raise
        finally:
            # Test teardown
            main.tearDown()


class XroadDeleteLocalTls(unittest.TestCase):
    def test_tls_227(self):
        MainController.driver_autostart = False
        main = MainController(self)

        main.log_in = True
        main.close_webdriver = True

        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        # Configure the tests
        delete_local_tls = local_tls_2_2_7.test_delete_tls(case=main, client=client, requester=requester)

        try:
            # Delete internal certificates from the servers
            delete_local_tls()
        except:
            main.log('XroadDeleteLocalTls: failed to remove TLS from local service')
            raise
        finally:
            # Test teardown
            main.tearDown()
