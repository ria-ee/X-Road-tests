# coding=utf-8
import unittest

import refresh_wsdl_2_2_5
from main.maincontroller import MainController
from helpers import xroad


class XroadRefreshWsdl(unittest.TestCase):
    def test_refresh_wsdl(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.5'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

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

        # Configure the service
        test_refresh_wsdl = refresh_wsdl_2_2_5.test_refresh_wsdl(main, client=client, wsdl_url=wsdl_url,
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
                                                                 ssh_password=ssh_password)

        # Reset the service
        test_reset_wsdl = refresh_wsdl_2_2_5.test_reset_wsdl(main, wsdl_local_path=wsdl_local_path,
                                                             wsdl_filename=wsdl_filename,
                                                             wsdl_correct=wsdl_correct,
                                                             ssh_host=ssh_host, ssh_username=ssh_username,
                                                             ssh_password=ssh_password)

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
            # Test teardown
            main.tearDown(save_exception=False)

