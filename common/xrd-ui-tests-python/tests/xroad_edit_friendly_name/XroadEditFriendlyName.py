# coding=utf-8
import unittest
from main.maincontroller import MainController
import kc_management


class XroadEditFriendlyName(unittest.TestCase):

    """
    UC SS_22: Edit the Friendly Name of a Token
    RIA URL: https://jira.ria.ee/browse/XTKB-74
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16
    """




    def test_xroad_edit_friendly_name(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC SS_22'
        main.test_number = 'UC SS_22: Edit the Friendly Name of a Token'
        main.test_name = self.__class__.__name__

        ssh_host = main.config.get('ss2.ssh_host')
        ssh_username = main.config.get('ss2.ssh_user')
        ssh_password = main.config.get('ss2.ssh_pass')

        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')

        '''Configure the service'''
        test_ss_backup_upload = kc_management.test_edit_conf(case=main, ssh_host=ssh_host, ssh_username=ssh_username,
                                                             ssh_password=ssh_password)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=main.url, username=main.username, password=main.password)

            '''Run the test'''
            test_ss_backup_upload()
        except:
            main.log('XroadEditFriendlyName: Failed to edit Friendly name')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
