# coding=utf-8
import unittest

import local_tls_2_2_7
from helpers import xroad
from main.maincontroller import MainController


class XroadDeleteLocalTls(unittest.TestCase):
    """
    MEMBER_51 5, 3a Delete a Security Server Client's Internal TLS certificate
    RIA URL: https://jira.ria.ee/browse/XTKB-42
    Depends on finishing other test(s): client_registration, configure_service, XroadAddLocalTls
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_tls_227(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.7-del'
        main.test_name = self.__class__.__name__

        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        provider = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        # Configure the tests
        delete_local_tls = local_tls_2_2_7.test_delete_tls(case=main, client=client, provider=provider)

        try:
            # Delete internal certificates from the servers
            delete_local_tls()
        except:
            main.log('XroadDeleteLocalTls: failed to remove TLS from local service')
            assert False
        finally:
            # Test teardown
            main.tearDown()
