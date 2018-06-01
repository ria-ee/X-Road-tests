# coding=utf-8
import unittest
import sys

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import configure_service

class XroadDeleteService(unittest.TestCase):
    """
    SERVICE_15 Delete a Security Server Client's WSDL
    RIA URL: https://jira.ria.ee/browse/XT-272, https://jira.ria.ee/browse/XTKB-27, https://jira.ria.ee/browse/XTKB-95
    Depends on finishing other test(s): XroadSecurityServerClientRegistration, XroadConfigureService
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_xroad_configure_service(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SERVICE_15'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))
        wsdl_test_service = main.config.get('wsdl.service_wsdl_test_service1')

        # Delete the added service
        test_delete_service = configure_service.test_delete_service(case=main, client=client, wsdl_url=wsdl_url,
                                                                    log_checker=log_checker)

        # Delete the other added service
        wsdl_test_service_url = main.config.get('wsdl.remote_path').format(wsdl_test_service)
        test_delete_service1 = configure_service.test_delete_service(case=main, client=client,
                                                                     wsdl_url=wsdl_test_service_url)

        try:
            main.log('Trying to check for and remove leftover service (2): {0}'.format(wsdl_test_service_url))
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_delete_service1()
        except Exception:
            main.log('XroadDeleteService: Service (2) not found, no need to delete.')
            sys.exc_clear()

        try:
            # Delete service
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_delete_service()
        except:
            main.log('XroadDeleteService: Failed to delete service')
            assert False
        finally:
            # Test teardown
            main.tearDown()
