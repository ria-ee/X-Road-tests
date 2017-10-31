# coding=utf-8
import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import configure_service_2_2_2

class XroadDeleteService(unittest.TestCase):
    def test_xroad_configure_service(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.2'
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
        test_delete_service = configure_service_2_2_2.test_delete_service(case=main, client=client, wsdl_url=wsdl_url,
                                                                          log_checker=log_checker)

        # Delete the other added service
        wsdl_test_service_url = main.config.get('wsdl.remote_path').format(wsdl_test_service)
        test_delete_service1 = configure_service_2_2_2.test_delete_service(case=main, client=client,
                                                                           wsdl_url=wsdl_test_service_url)
        try:
            # Delete service
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_delete_service()
        except:
            main.log('XroadDeleteService: Failed to delete service')
            assert False
        finally:
            try:
                main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
                test_delete_service1()
            except:
                main.log('XroadDeleteService: Failed to delete service (2).')
                main.save_exception_data()
            # Test teardown
            main.tearDown()

