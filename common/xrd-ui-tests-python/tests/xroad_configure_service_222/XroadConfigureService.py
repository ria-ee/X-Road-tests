# coding=utf-8
import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_add_to_acl_218 import add_to_acl
from tests.xroad_configure_service_222 import configure_service


class XroadConfigureService(unittest.TestCase):
    """
    SERVICE_08 1-8, 3a, 4a, 5a, 6b, 7a Add a WSDL to a Security Server Client
    SERVICE_09 Edit the Address of a WSDL
    SERVICE_10 Download and Parse WSDL
    SERVICE_12 1-2 Enable a Security Server Client's WSDL
    SERVICE_15 Delete a Security Server Client's WSDL
    SERVICE_17 Add Access Rights to a Service
    SERVICE_19 4, 4a, 5, 5a Edit the address of a service
    SERVICE_21 4a, 4b Edit the Timeout Value of a Service
    SERVICE_44 (1, 1a, 1b) Validate a WSDL
    RIA URL: https://jira.ria.ee/browse/XT-265, https://jira.ria.ee/browse/XTKB-94
    RIA URL: https://jira.ria.ee/browse/XT-266, https://jira.ria.ee/browse/XTKB-23
    RIA URL: https://jira.ria.ee/browse/XT-267
    RIA URL: https://jira.ria.ee/browse/XT-269
    RIA URL: https://jira.ria.ee/browse/XT-272, https://jira.ria.ee/browse/XTKB-27, https://jira.ria.ee/browse/XTKB-95
    RIA URL: https://jira.ria.ee/browse/XT-274, https://jira.ria.ee/browse/XTKB-172
    RIA URL: https://jira.ria.ee/browse/XT-276, https://jira.ria.ee/browse/XTKB-55, https://jira.ria.ee/browse/XTKB-28
    RIA URL: https://jira.ria.ee/browse/XT-278
    Depends on finishing other test(s): XroadSecurityServerClientRegistration
    Requires helper scenarios: xroad_add_to_acl_218
    X-Road version: 6.16.0
    """

    def test_xroad_configure_service(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SERVICE_08'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss1.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        service_name = main.config.get('services.test_service')  # xroadGetRandom
        service_url = main.config.get('services.test_service_url')
        service_2_name = main.config.get('services.test_service_2')  # bodyMassIndex
        service_2_url = main.config.get('services.test_service_2_url')

        subject_list = [xroad.get_xroad_subsystem(requester)]

        # Configure the service
        test_configure_service = configure_service.test_configure_service(case=main, client=client,
                                                                          check_add_errors=True,
                                                                          check_edit_errors=True,
                                                                          check_parameter_errors=True,
                                                                          service_name=service_name,
                                                                          service_url=service_url,
                                                                          service_2_name=service_2_name,
                                                                          service_2_url=service_2_url)

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
        # Enable the service
        test_enable_service = configure_service.test_enable_service(case=main, client=client, wsdl_url=wsdl_url)

        # Delete the added service
        test_delete_service = configure_service.test_delete_service(case=main, client=client, wsdl_url=wsdl_url)
        wsdl_test_service = main.config.get('wsdl.service_wsdl_test_service1')
        # Delete the other added service
        wsdl_test_service_url = main.config.get('wsdl.remote_path').format(wsdl_test_service)
        test_delete_service1 = configure_service.test_delete_service(case=main, client=client,
                                                                     wsdl_url=wsdl_test_service_url)

        try:
            # Open webdriver
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            # Add WSDL and configure service
            test_configure_service()

            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_configure_service_acl()

            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_configure_service_acl_2()

            # Enable service
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_enable_service()
        except:
            main.log('XroadConfigureService: Failed to configure service')
            main.save_exception_data()
            try:
                # Delete service
                main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
                test_delete_service()
            except:
                main.log('XroadConfigureService: Failed to delete added data.')
                main.save_exception_data()
            assert False
        finally:
            try:
                main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
                test_delete_service1()
            except:
                main.log('XroadConfigureService: Failed to delete added data (2).')
                main.save_exception_data()
            # Test teardown
            main.tearDown()
