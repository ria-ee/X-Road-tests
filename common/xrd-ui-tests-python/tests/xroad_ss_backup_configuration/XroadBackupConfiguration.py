# coding=utf-8
import unittest
from main.maincontroller import MainController
import ss_management


class XroadBackupConfiguration(unittest.TestCase):
    """
      UC SS_14: Back Up Configuration
      RIA URL: https://jira.ria.ee/browse/XTKB-97
      Depends on finishing other test(s):
      Requires helper scenarios:
      X-Road version: 6.16
    """



    def test_backup_configuration(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC SS_14'
        main.log('TEST: UC SS_14: Back Up Configuration')

        main.test_name = self.__class__.__name__

        ssh_host = main.config.get('ss2.ssh_host')
        ssh_username = main.config.get('ss2.ssh_user')
        ssh_password = main.config.get('ss2.ssh_pass')


        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')

        '''Configure the service'''
        test_ss_backup_conf = ss_management.test_ss_backup_conf(case=main, ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password)
        try:
            '''Open webdriver'''
            main.reload_webdriver(url=main.url, username=main.username, password=main.password)

            '''Run the test'''
            test_ss_backup_conf()
        except:
            main.log('XroadBackupConfiguration: Failed to run SS backup configuration')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
