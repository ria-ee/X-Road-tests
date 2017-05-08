# coding=utf-8
import unittest

import deactivate_wsdl_2_2_6
from main.maincontroller import MainController
from helpers import xroad


class XroadDeactivateWsdl(unittest.TestCase):
    def test_deactivate_wsdl(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.6'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        # Configure the service
        test_deactivate_wsdl = deactivate_wsdl_2_2_6.test_disable_wsdl(main, client=client, wsdl_url=wsdl_url)

        test_reactivate_wsdl = deactivate_wsdl_2_2_6.test_enable_wsdl(main, client=client, wsdl_url=wsdl_url)

        try:
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_deactivate_wsdl()
        except:
            main.log('XroadDeactivateWsdl: Failed to deactivate WSDL')
            main.save_exception_data()
            raise
        finally:
            try:
                main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
                test_reactivate_wsdl()
            except:
                main.log('XroadDeactivateWsdl: Failed to reactivate WSDL')
                main.save_exception_data()
                raise
            finally:
                # Test teardown
                main.tearDown(save_exception=False)