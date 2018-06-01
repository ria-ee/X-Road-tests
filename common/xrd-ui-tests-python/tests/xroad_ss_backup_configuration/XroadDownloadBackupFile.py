# coding=utf-8
import unittest
from main.maincontroller import MainController
import ss_management



class XroadDownloadBackupFile(unittest.TestCase):

    """
    UC SS_16: Download a Backup File
    RIA URL: https://jira.ria.ee/browse/XTKB-103
    Depends on finishing other test(s): XroadBackupConfiguration
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_download_backupfile(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC SS_16'
        main.log('TEST: UC SS_16: Download a Backup File')

        main.test_name = self.__class__.__name__

        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')

        '''Configure the service'''
        test_ss_backup_download = ss_management.test_ss_backup_download(case=main)
        try:
            '''Open webdriver'''
            main.reload_webdriver(url=main.url, username=main.username, password=main.password)

            '''Run the test'''
            test_ss_backup_download()
        except:
            main.log('XroadBackupDownload: Failed to download backup file')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
