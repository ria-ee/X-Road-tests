# coding=utf-8
import unittest

import deactivate_wsdl_2_2_6
from helpers import xroad, auditchecker
from main.maincontroller import MainController


class XroadDeactivateWsdl(unittest.TestCase):
    """
    SERVICE_13 3a, 6
    RIA URL: https://jira.ria.ee/browse/XTKB-24
    RIA URL: https://jira.ria.ee/browse/XTKB-95
    Depends on finishing other test(s): client_registration, configure_services
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_deactivate_wsdl(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.6'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss1.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        # Configure the service
        test_deactivate_wsdl = deactivate_wsdl_2_2_6.test_disable_wsdl(main, client=client, wsdl_url=wsdl_url,
                                                                       requester=requester, log_checker=log_checker)

        test_reactivate_wsdl = deactivate_wsdl_2_2_6.test_enable_wsdl(main, client=client, wsdl_url=wsdl_url,
                                                                      requester=requester)

        try:
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_deactivate_wsdl()
        except:
            main.log('XroadDeactivateWsdl: Failed to deactivate WSDL')
            main.save_exception_data()
            assert False
        finally:
            try:
                main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
                test_reactivate_wsdl()
            except:
                main.log('XroadDeactivateWsdl: Failed to reactivate WSDL')
                main.save_exception_data()
                assert False
            finally:
                # Test teardown
                main.tearDown(save_exception=False)
