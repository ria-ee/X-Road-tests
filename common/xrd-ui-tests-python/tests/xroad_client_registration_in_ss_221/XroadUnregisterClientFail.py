import unittest

from helpers import xroad
from helpers.auditchecker import AuditChecker
from main.maincontroller import MainController
from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import unregister_client


class XroadUnregisterClientFail(unittest.TestCase):
    """
    MEMBER_52 5a Unregister client
    RIA URL: https://jira.ria.ee/browse/XTKB-164
    Depends on finishing other test(s): client_registration
    Requires helper scenarios: disable wsdl, enable wsdl
    X-Road version: 6.16.0
    """

    def test_xroad_unregister_client_request_fail(self):
        main = MainController(self)

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
        test_unregister_client_req_fail = unregister_client(main,
                                                            client,
                                                            client_path,
                                                            request_fail=True,
                                                            log_checker=log_checker)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            disable_management_service()
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_unregister_client_req_fail()
        finally:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            enable_management_service()
            main.tearDown()
