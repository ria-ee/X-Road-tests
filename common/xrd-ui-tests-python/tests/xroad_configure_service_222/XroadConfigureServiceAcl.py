# coding=utf-8
import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_add_to_acl_218 import add_to_acl


class XroadConfigureServiceAcl(unittest.TestCase):
    """
    SERVICE_17 Add Access Rights to a Service
    RIA URL: https://jira.ria.ee/browse/XT-274, https://jira.ria.ee/browse/XTKB-172
    Depends on finishing other test(s): XroadAddWsdlSecurityServerClient
    Requires helper scenarios: xroad_add_to_acl_218
    X-Road version: 6.16.0
    """

    def test_xroad_configure_service(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SERVICE_17'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss1.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        service_name = main.config.get('services.test_service')  # xroadGetRandom
        service_2_name = main.config.get('services.test_service_2')  # bodyMassIndex

        subject_list = [xroad.get_xroad_subsystem(requester)]

        # Add the subject to ACL
        test_configure_service_acl = add_to_acl.test_add_subjects(case=main, client=client,
                                                                  wsdl_url=wsdl_url,
                                                                  service_name=service_name,
                                                                  service_subjects=subject_list,
                                                                  remove_data=False,
                                                                  allow_remove_all=False)
        test_configure_service_acl_2 = add_to_acl.test_add_subjects(case=main, client=client,
                                                                    wsdl_url=wsdl_url,
                                                                    service_name=service_2_name,
                                                                    service_subjects=subject_list,
                                                                    remove_data=False,
                                                                    allow_remove_all=False)

        try:
            # Open webdriver and configure the access rights
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_configure_service_acl()

            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_configure_service_acl_2()
        except:
            main.log('XroadConfigureServiceAcl: Failed to configure service ACL')
            main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
