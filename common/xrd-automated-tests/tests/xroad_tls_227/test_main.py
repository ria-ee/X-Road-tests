# coding=utf-8
import unittest

import local_tls_2_2_7
from main.maincontroller import MainController
from helpers import xroad


class XroadLocalTls(unittest.TestCase):
    def test_tls_227(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.7'
        main.test_name = self.__class__.__name__

        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        provider = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        # Configure the tests
        test_local_tls = local_tls_2_2_7.test_tls(case=main, client=client, provider=provider)
        delete_local_tls = local_tls_2_2_7.test_delete_tls(case=main, client=client, provider=provider)

        try:
            # Test local TLS
            test_local_tls()
        except:
            main.log('XroadLocalTls: Failed to configure TLS for local service')
            main.save_exception_data()
            # Delete internal certificates from the servers
            try:
                delete_local_tls()
            except:
                main.save_exception_data()
                main.log('XroadLocalTls: failed to remove TLS from local service')
            raise
        finally:
            # Test teardown
            main.tearDown(save_exception=False)


class XroadDeleteLocalTls(unittest.TestCase):
    def test_tls_227(self):
        main = MainController(self)

        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        provider = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        # Configure the tests
        delete_local_tls = local_tls_2_2_7.test_delete_tls(case=main, client=client, provider=provider)

        try:
            # Delete internal certificates from the servers
            delete_local_tls()
        except:
            main.log('XroadDeleteLocalTls: failed to remove TLS from local service')
            raise
        finally:
            # Test teardown
            main.tearDown()
