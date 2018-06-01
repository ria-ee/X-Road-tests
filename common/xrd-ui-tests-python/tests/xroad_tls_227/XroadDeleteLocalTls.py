# coding=utf-8
import unittest

import local_tls
from helpers import xroad
from main.maincontroller import MainController


class XroadDeleteLocalTls(unittest.TestCase):
    """
    MEMBER_51 Delete a Security Server Client's Internal TLS certificate
    MEMBER_49 Change a Security Server Client's Internal Server Connection Type
    RIA URL: https://jira.ria.ee/browse/XT-403, https://jira.ria.ee/browse/XTKB-42
    RIA URL: https://jira.ria.ee/browse/XT-401
    Depends on finishing other test(s): XroadSecurityServerClientRegistration, XroadConfigureService, XroadAddLocalTls
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_tls_227(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_51'
        main.test_name = self.__class__.__name__

        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        provider = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        # Configure the tests
        delete_local_tls = local_tls.test_delete_tls(case=main, client=client, provider=provider)

        try:
            # Delete internal certificates from the servers
            delete_local_tls()
        except:
            main.save_exception_data()
            main.log('XroadDeleteLocalTls: failed to remove TLS from local service')
            assert False
        finally:
            # Test teardown
            main.tearDown()
