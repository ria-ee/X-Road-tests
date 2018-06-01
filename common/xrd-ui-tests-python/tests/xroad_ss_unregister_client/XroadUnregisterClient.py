import unittest

from helpers import xroad, auditchecker
from helpers.auditchecker import AuditChecker
from main.maincontroller import MainController
from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss
from tests.xroad_ss_unregister_client.unregister_client import test_unregister_client, unregister_client_fail


class XroadUnregisterClient(unittest.TestCase):
    """
    MEMBER_52 Unregister a Security Server Client
    RIA URL: https://jira.ria.ee/browse/XT-404
    RIA URL: https://jira.ria.ee/browse/XTKB-164
    Depends on finishing other test(s): MEMBER_37
    Requires helper scenarios: disable wsdl, enable wsdl
    X-Road version: 6.16.0
    """

    def test_a_xroad_unregister_client_request_fail(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_52.a'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        log_checker = AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        management_wsdl_url = main.config.get('wsdl.management_service_wsdl_url')
        client = xroad.split_xroad_id(main.config.get('ss1.management_id'))
        client_id = xroad.get_xroad_subsystem(client)
        client['subsystem_code'] = client['subsystem']
        client_path = xroad.get_xroad_path(client, client_type='SERVICE')

        disable_management_service = client_registration_in_ss.disable_management_wsdl(main,
                                                                                             client_id,
                                                                                             management_wsdl_url)
        enable_management_service = client_registration_in_ss.enable_management_wsdl(main,
                                                                                           client_id,
                                                                                           management_wsdl_url)
        test_unregister_client_req_fail = unregister_client_fail(main,
                                                                 client,
                                                                 client_path,
                                                                 request_fail=True,
                                                                 log_checker=log_checker)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            disable_management_service()
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_unregister_client_req_fail()
        except:
            main.save_exception_data()
            raise
        finally:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            enable_management_service()
            main.tearDown()

    def test_b_xroad_unregister_client(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_52.b'
        main.test_name = self.__class__.__name__

        ss1_host = main.config.get('ss1.host')
        ss1_user = main.config.get('ss1.user')
        ss1_pass = main.config.get('ss1.pass')

        ss1_ssh_host = main.config.get('ss1.ssh_host')
        ss1_ssh_user = main.config.get('ss1.ssh_user')
        ss1_ssh_pass = main.config.get('ss1.ssh_pass')

        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')
        log_checker = auditchecker.AuditChecker(ss1_ssh_host, ss1_ssh_user, ss1_ssh_pass)

        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        ss2_client_2 = xroad.split_xroad_id(main.config.get('ss2.client2_id'))
        unreg_ss1_client = test_unregister_client(main, ss1_client, try_cancel=True, log_checker=log_checker)
        unreg_ss1_client_2 = test_unregister_client(main, ss1_client_2)
        unreg_ss2_client_2 = test_unregister_client(main, ss2_client_2)
        try:
            main.reload_webdriver(ss1_host, ss1_user, ss1_pass)
            unreg_ss1_client()
            main.reload_webdriver(ss1_host, ss1_user, ss1_pass)
            unreg_ss1_client_2()
            main.reload_webdriver(ss2_host, ss2_user, ss2_pass)
            unreg_ss2_client_2()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
