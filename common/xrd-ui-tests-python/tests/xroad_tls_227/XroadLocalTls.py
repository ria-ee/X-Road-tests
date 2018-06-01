# coding=utf-8
import unittest

import local_tls
from helpers import xroad
from main.maincontroller import MainController


class XroadLocalTls(unittest.TestCase):
    """
    MEMBER_49 Change a Security Server Client's Internal Server Connection Type
    MEMBER_50 5, 6, 3a, 4a Add a Security Server Client's Internal TLS Certificate
    SS_10 View the Internal TLS Certificate of the Security Server
    SS_11 Generate a New TLS key and Certificate for the security server
    SS_12 Export the Internal TLS Certificate of the Security Server
    SERVICE_20 Set the Option to Verify TLS Certificate of a Service
    RIA URL: https://jira.ria.ee/browse/XT-401, https://jira.ria.ee/browse/XTKB-42
    RIA URL: https://jira.ria.ee/browse/XT-402, https://jira.ria.ee/browse/XTKB-93
    RIA URL: https://jira.ria.ee/browse/XT-323, https://jira.ria.ee/browse/XTKB-96
    RIA URL: https://jira.ria.ee/browse/XT-324, https://jira.ria.ee/browse/XTKB-84
    RIA URL: https://jira.ria.ee/browse/XT-325
    RIA URL: https://jira.ria.ee/browse/XT-277, https://jira.ria.ee/browse/XTKB-77
    Depends on finishing other test(s): XroadSecurityServerClientRegistration, XroadConfigureService
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_tls_227(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'MEMBER_49/MEMBER_50'
        main.test_name = self.__class__.__name__

        client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        provider = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        # Configure the tests
        test_local_tls = local_tls.test_tls(case=main, client=client, provider=provider)
        delete_local_tls = local_tls.test_delete_tls(case=main, client=client, provider=provider)

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
