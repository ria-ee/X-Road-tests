# coding=utf-8
import unittest

import add_central_service
from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import configure_service


class XroadDeleteCentralService(unittest.TestCase):
    """
    SERVICE_43 Delete a Central Service
    RIA URL: https://jira.ria.ee/browse/XT-300, https://jira.ria.ee/browse/XTKB-35
    Depends on finishing other test(s): XroadSecurityServerClientRegistration, XroadConfigureService, XroadAddCentralService
    Requires helper scenarios: xroad_configure_service_222, xroad_add_to_acl_218
    X-Road version: 6.16.0
    """

    def test_add_central_service_2_2_8(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SERVICE_43'
        main.test_name = self.__class__.__name__

        main.start_mock_service()

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')

        requester = xroad.split_xroad_id(main.config.get('ss1.client_id'))

        provider_2 = xroad.split_xroad_id(main.config.get('services.central_service_provider_2_id'))

        central_service_name = main.config.get('services.central_service')

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        wait_sync_retry_delay = main.config.get('services.request_sync_delay')
        sync_max_seconds = main.config.get('services.request_sync_timeout')

        delete_service = configure_service.test_delete_service(main, client=provider_2, wsdl_url=wsdl_url)

        delete_central_service = add_central_service.test_delete_central_service(main,
                                                                                 cs_ssh_host=cs_ssh_host,
                                                                                 cs_ssh_user=cs_ssh_user,
                                                                                 cs_ssh_pass=cs_ssh_pass,
                                                                                 provider=provider_2,
                                                                                 requester=requester,
                                                                                 central_service_name=central_service_name,
                                                                                 sync_max_seconds=sync_max_seconds,
                                                                                 wait_sync_retry_delay=wait_sync_retry_delay,
                                                                                 cancel_deletion=True)

        try:
            try:
                # Go to CS main page (login again if necessary) and edit the central service
                main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

                # Delete central service
                delete_central_service()
            except:
                main.log('XroadDeleteCentralService: Failed to delete central service')
                assert False
            finally:
                try:
                    # Go to SS2 main page (re-login if necessary) and delete the newly created service
                    main.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)
                    delete_service()
                except:
                    main.log('XroadDeleteCentralService: failed to delete security server service')
                    assert False
        finally:
            # Test teardown
            main.tearDown()
