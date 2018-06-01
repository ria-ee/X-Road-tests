# coding=utf-8
import unittest
from main.maincontroller import MainController
import ht_management


"""
 UC SS_27: Log Out of a Hardware Token
 RIA URL: https://jira.ria.ee/browse/XTKB-159
 Depends on finishing other test(s):
 Requires helper scenarios:
 X-Road version: 6.16.0
 """

class XroadSsLogOutHardwareToken(unittest.TestCase):
    def test_xroad_logout_token(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC SS 27'
        main.log('TEST:  UC SS_27: Log Out of a Hardware Token')

        main.test_name = self.__class__.__name__

        ss_host = main.config.get('hwtoken.host')
        ss_user = main.config.get('hwtoken.user')
        ss_pass = main.config.get('hwtoken.pass')
        ss_token_pin = main.config.get('hwtoken.token_pin')

        ss_ssh_host = main.config.get('hwtoken.ssh_host')
        ss_ssh_user = main.config.get('hwtoken.ssh_user')
        ss_ssh_pass = main.config.get('hwtoken.ssh_pass')

        '''Configure the service'''
        test_logout = ht_management.test_hardware_logout(case=main, ssh_host=ss_ssh_host, ssh_username=ss_ssh_user,
                                                   ssh_password=ss_ssh_pass, pin=ss_token_pin)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            '''Run the test'''
            test_logout()
        except:
            main.log('Xroad_log_out_hardware_token: Failed to Log Out of a Hardware Token')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
