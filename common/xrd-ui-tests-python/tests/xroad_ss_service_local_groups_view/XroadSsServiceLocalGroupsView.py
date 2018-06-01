# coding=utf-8
import unittest
from main.maincontroller import MainController
import view_management

"""
 SERVICE_23: View the Local Groups of a Security Server Client
 RIA URL: https://jira.ria.ee/browse/XTKB-169
 Depends on finishing other test(s):
 Requires helper scenarios:
 X-Road version: 6.16.0
 """


class XroadSsServiceLocalGroupsView(unittest.TestCase):
    def test_xroad_logout_token(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC SERVICE_23'
        main.log('TEST:  UC SERVICE_23: View the Local Groups of a Security Server Client')

        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        '''Configure the service'''
        test_view_groups = view_management.test_verify_local_group_client(case=main)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            '''Run the test'''
            test_view_groups()
        except:
            main.log('XroadSsServiceLocalGroupsView: Failed to View the Local Groups of a Security Server Client')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
