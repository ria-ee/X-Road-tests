# coding=utf-8
import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_deactivate_wsdl_226.deactivate_wsdl import test_enable_wsdl


class XroadEnableWSDL(unittest.TestCase):
    """
    UC SERVICE_12 Enable a Security Server Client's WSDL
    RIA URL:
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_activate_wsdl(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC SERVICE_12'
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

        test_reactivate_wsdl = test_enable_wsdl(main, client=client, wsdl_url=wsdl_url,
                                                                requester=requester, log_checker=log_checker)

        try:
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_reactivate_wsdl()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
