# coding=utf-8
import unittest
from main.maincontroller import MainController
import view_management

"""
 SERVICE_24: View the Details of a Local Group
 RIA URL: https://jira.ria.ee/browse/XTKB-178
 Depends on finishing other test(s):
 Requires helper scenarios:
 X-Road version: 6.16.0
 """


class XroadSsServiceLocalGroupsViewDetails(unittest.TestCase):
    def test_xroad_local_groups_view_details(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC SERVICE_24'
        main.log('TEST:  UC SERVICE_24: View the Details of a Local Group')

        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')
        ss_client_id = main.config.get('ss2.client_id')
        ss_client_name = main.config.get('ss2.client_name')

        '''Configure the service'''
        test_logout = view_management.test_verify_local_group_client(case=main, ss_client_id=ss_client_id, ss_client_name=ss_client_name)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            '''Run the test'''
            test_logout()
        except:
            main.log('Xroad_ss_service_local_groups_view_details: Failed to View the Local Groups of a Security Server Client')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
