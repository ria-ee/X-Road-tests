# coding=utf-8
import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import wsdl_validator_errors
from tests.xroad_configure_service_222.wsdl_validator_errors import restore_wsdl_validator_wrapper
from view_models import ss_system_parameters


class XroadWsdlValidation(unittest.TestCase):
    """
    SERVICE_44: Validate a WSDL
    RIA URL: https://jira.ria.ee/browse/XTKB-30
    Depends on finishing other test(s): XroadSecurityServerClientRegistration
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_xroad_wsdl_validator_crash(self):
        main = MainController(self)

        main.test_number = 'SERVICE_44'
        main.test_name = self.__class__.__name__

        ssh_host = main.config.get('ss2.ssh_host')
        ssh_user = main.config.get('ss2.ssh_user')
        ssh_pass = main.config.get('ss2.ssh_pass')

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        service_name = main.config.get('services.test_service')  # xroadGetRandom
        service_url = main.config.get('services.test_service_url')
        service_2_name = main.config.get('services.test_service_2')  # bodyMassIndex
        service_2_url = main.config.get('services.test_service_2_url')

        client_id = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        client_name = main.config.get('ss1.client_name')

        wsdl_warning_url = main.config.get('wsdl.remote_path').format(
            main.config.get('wsdl.service_wsdl_warning_filename'))
        wsdl_validator_wrapper_path = ss_system_parameters.WSDL_VALIDATOR_WRAPPER_LOCATION

        test_configure_service = wsdl_validator_errors.test_configure_service(case=main, client=client,
                                                                              check_add_errors=True,
                                                                              check_edit_errors=True,
                                                                              check_parameter_errors=True,
                                                                              service_name=service_name,
                                                                              service_url=service_url,
                                                                              service_2_name=service_2_name,
                                                                              service_2_url=service_2_url)

        test_wsdl_validator_crash = wsdl_validator_errors.test_wsdl_validator_crash(self=main,
                                                                                    ssh_host=ssh_host,
                                                                                    ssh_username=ssh_user,
                                                                                    ssh_password=ssh_pass,
                                                                                    wsdl_url=wsdl_warning_url,
                                                                                    ss_host=ss_host,
                                                                                    ss_user=ss_user,
                                                                                    ss_pass=ss_pass,
                                                                                    client_id=client_id,
                                                                                    client_name=client_name,
                                                                                    wsdl_validator_wrapper_path=wsdl_validator_wrapper_path)

        try:
            main.log('SERVICE_44 1.c The validation program crashed while validating the WSDL file')
            test_configure_service()
            test_wsdl_validator_crash()
        finally:
            main.log('Restoring wsdl wrapper')
            restore_wsdl_validator_wrapper(case=main, ssh_host=ssh_host, ssh_username=ssh_user,
                                           ssh_password=ssh_pass,
                                           wsdl_validator_wrapper_path=wsdl_validator_wrapper_path)
            main.tearDown()
