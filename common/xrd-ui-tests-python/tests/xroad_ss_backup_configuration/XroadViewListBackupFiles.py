import unittest
from main.maincontroller import MainController
import ss_management


class XroadViewListBackupFiles(unittest.TestCase):
    """
    UC  SS 13  View the List of Configuration Backup Files
    RIA URL: https://jira.ria.ee/browse/XT-326, https://jira.ria.ee/browse/XTKB-123
    Depends on finishing other test(s): XroadBackupConfiguration
    Requires helper scenarios: None
    X-Road version: 6.16.0
    """

    def test_view_list_backup_files(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC SS 13'
        main.test_name = self.__class__.__name__

        main.log('TEST: UC  SS 13  View the List of Configuration Backup Files')
        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')

        '''Configure the service'''
        test_view_list_backup_files = ss_management.test_view_list_backup_files(case=main)
        try:
            '''Open webdriver'''
            main.reload_webdriver(url=main.url, username=main.username, password=main.password)

            '''Run the test'''
            test_view_list_backup_files()
        except:
            main.log('XroadViewListBackupFiles: Failed to view the list of configuration backup files')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
