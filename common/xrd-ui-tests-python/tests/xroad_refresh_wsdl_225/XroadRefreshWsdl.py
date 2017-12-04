# coding=utf-8
import unittest

import refresh_wsdl
from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import configure_service


class XroadRefreshWsdl(unittest.TestCase):
    """
    UC SERVICE_14: Refresh Security Server Client's WSDL (covers all steps except extensions 3a, 3d, 3e which
    are covered by XroadWsdlValidatorErrors)
    RIA URL: https://jira.ria.ee/browse/XT-271, https://jira.ria.ee/browse/XTKB-25
    RIA URL: https://jira.ria.ee/browse/XTKB-26, https://jira.ria.ee/browse/XTKB-95
    Depends on finishing other test(s): XroadSecurityServerClientRegistration, XroadConfigureService
    Requires helper scenarios: xroad_add_to_acl_218
    X-Road version: 6.16.0
    """

    def test_refresh_wsdl(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC SERVICE_14'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')

        ssh_host = main.config.get('wsdl.ssh_host')
        ssh_username = main.config.get('wsdl.ssh_user')
        ssh_password = main.config.get('wsdl.ssh_pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss1.client_id'))

        wsdl_remote_path = main.config.get('wsdl.remote_path')
        wsdl_local_path = main.config.get('wsdl.local_path')

        wsdl_filename = main.config.get('wsdl.service_wsdl')
        wsdl_url = wsdl_remote_path.format(wsdl_filename)

        wsdl_correct = main.config.get('wsdl.service_correct_filename')
        wsdl_missing_service = main.config.get('wsdl.service_single_service_filename')
        wsdl_error = main.config.get('wsdl.service_wsdl_error_filename')
        wsdl_warning = main.config.get('wsdl.service_wsdl_warning_filename')

        service_name = main.config.get('services.test_service_2')
        service_2_name = main.config.get('services.test_service')

        new_wsdl = main.config.get('wsdl.service_wsdl_test_service1')
        new_wsdl_url = wsdl_remote_path.format(new_wsdl)

        # Configure the service
        test_refresh_wsdl = refresh_wsdl.test_refresh_wsdl(main, client=client, wsdl_url=wsdl_url,
                                                           service_name=service_name,
                                                           service_name_2=service_2_name,
                                                           requester=requester,
                                                           wsdl_path=wsdl_remote_path,
                                                           wsdl_local_path=wsdl_local_path,
                                                           wsdl_filename=wsdl_filename,
                                                           wsdl_correct=wsdl_correct,
                                                           wsdl_missing_service=wsdl_missing_service,
                                                           wsdl_error=wsdl_error, wsdl_warning=wsdl_warning,
                                                           ssh_host=ssh_host, ssh_username=ssh_username,
                                                           ssh_password=ssh_password, new_wsdl=new_wsdl,
                                                           ss_ssh_host=ss_ssh_host, ss_ssh_user=ss_ssh_user,
                                                           ss_ssh_pass=ss_ssh_pass)

        # Reset the service
        test_reset_wsdl = refresh_wsdl.test_reset_wsdl(main, wsdl_local_path=wsdl_local_path,
                                                       wsdl_filename=wsdl_filename,
                                                       wsdl_correct=wsdl_correct,
                                                       ssh_host=ssh_host, ssh_username=ssh_username,
                                                       ssh_password=ssh_password)

        # Delete the added WSDL
        delete_service = configure_service.test_delete_service(case=main, client=client,
                                                               wsdl_url=new_wsdl_url)
        try:
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_refresh_wsdl()
        except:
            main.log('XroadRefreshWsdl: Failed to refresh WSDL')
            main.save_exception_data()
            try:
                test_reset_wsdl()
            except:
                main.log('XroadRefreshWsdl: Failed to reset WSDL to original file')
                main.save_exception_data()
            assert False
        finally:
            try:
                # Delete service
                main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
                delete_service()
            except:
                main.log('XroadDeleteService: Failed to delete service')
                assert False
            # Test teardown
            finally:
                main.tearDown()
