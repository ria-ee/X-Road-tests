# coding=utf-8
import unittest

import local_tls_2_2_7
from helpers import xroad
from main.maincontroller import MainController


class XroadLocalTls(unittest.TestCase):
    """
    MEMBER_50 5, 6, 3a, 4a Add a Security Server Client's Internal TLS Certificate
    MEMBER_49 4 Change a Security Server Client's Internal Server Connection Type
    SS_11 6, 3a, 4a Generate a New TLS key and Certificate for the security server
    RIA URL: https://jira.ria.ee/browse/XTKB-42
    RIA URL: https://jira.ria.ee/browse/XTKB-84
    RIA URL: https://jira.ria.ee/browse/XTKB-93
    Depends on finishing other test(s): client_registration, configure_service
    Requires helper scenarios:
    X-Road version: 6.16
    """

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
            assert False
        finally:
            # Test teardown
            main.tearDown(save_exception=False)
