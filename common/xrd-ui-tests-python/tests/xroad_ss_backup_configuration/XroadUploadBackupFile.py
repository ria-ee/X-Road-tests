# coding=utf-8
import unittest
from main.maincontroller import MainController
import ss_management

class XroadUploadBackupFile(unittest.TestCase):
    '''
    UC SS_18: Upload a Backup File
    RIA URL: https://jira.ria.ee/browse/XTKB-105
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16
    '''

    def test_xroad_verify_ts(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC SS_18'
        main.log('TEST: UC  SS_18: Upload a Backup File')
        main.test_name = self.__class__.__name__

        ssh_host = main.config.get('ss2.ssh_host')
        ssh_username = main.config.get('ss2.ssh_user')
        ssh_password = main.config.get('ss2.ssh_pass')



        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')

        '''Configure the service'''
        test_ss_backup_upload = ss_management.test_ss_upload_backup(case=main, ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password)
        try:
            '''Open webdriver'''
            main.reload_webdriver(url=main.url, username=main.username, password=main.password)

            '''Run the test'''
            test_ss_backup_upload()
        except:
            main.log('XroadUploadBackupFile: Failed to upload backup file')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
