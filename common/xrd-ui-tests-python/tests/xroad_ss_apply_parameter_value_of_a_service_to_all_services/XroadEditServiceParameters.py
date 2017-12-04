import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_ss_apply_parameter_value_of_a_service_to_all_services import edit_service_params


class XroadEditServiceParameters(unittest.TestCase):
    """
    SERVICE_22 Apply the Parameter Value of a Service to All the Services in the WSDL
    RIA URL: https://jira.ria.ee/browse/XTKB-174
    Depends on finishing other test(s): configure service
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_xroad_apply_TLS_value_to_all_services_in_wsdl(self):
        main = MainController(self)

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')

        client_name = main.config.get('ss2.client_name')
        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        remote_path = main.config.get('wsdl.remote_path')
        service_wsdl = main.config.get('wsdl.service_wsdl')
        wsdl_url = remote_path.format(service_wsdl)
        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        test_edit_service_parameters = edit_service_params.test_edit_tls_to_all(main, client, client_name, wsdl_url, log_checker)
        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_edit_service_parameters()
        finally:
            main.tearDown()

    def test_xroad_apply_url_value_to_all_services_in_wsdl(self):
        main = MainController(self)

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client_name = main.config.get('ss2.client_name')
        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        remote_path = main.config.get('wsdl.remote_path')
        service_wsdl = main.config.get('wsdl.service_wsdl')
        wsdl_url = remote_path.format(service_wsdl)

        test_edit_service_parameters = edit_service_params.test_edit_url_to_all(main, client, client_name, wsdl_url)
        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_edit_service_parameters()
        finally:
            main.tearDown()

    def test_xroad_apply_timeout_value_to_all_services_in_wsdl(self):
        main = MainController(self)

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client_name = main.config.get('ss2.client_name')
        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        remote_path = main.config.get('wsdl.remote_path')
        service_wsdl = main.config.get('wsdl.service_wsdl')
        wsdl_url = remote_path.format(service_wsdl)

        test_edit_timeout_to_all = edit_service_params.test_edit_timeout_to_all(main, client, client_name, wsdl_url)
        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_edit_timeout_to_all()
        finally:
            main.tearDown()
