# coding=utf-8
import unittest
from main.maincontroller import MainController
import view_management
from helpers import xroad

"""
 SERVICE_36: View the Global Group Membership of an X-Road Member
 RIA URL: https://jira.ria.ee/browse/XTKB-179
 Depends on finishing other test(s):
 Requires helper scenarios:
 X-Road version: 6.16.0
 """


class XroadServiceGlobalGroupMembershipView(unittest.TestCase):
    def test_xroad_local_groups_view_details(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC SERVICE_36'
        main.log('TEST:  UC SERVICE_36: View the Global Group Membership of an X-Road Member')

        main.test_name = self.__class__.__name__
        ss_client_name = main.config.get('ss2.client_name')

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        test_group_name = 'testGroup'
        provider = xroad.split_xroad_id(main.config.get('services.central_service_provider_id'))
        subsystem = provider['subsystem']



        '''Configure the service'''
        test_logout = view_management.test_verify_local_group_client(case=main, ss_client_name=ss_client_name, test_group_name=test_group_name, subsystem=subsystem)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            '''Run the test'''
            test_logout()
        except:
            main.log('Xroad_ss_service_local_groups_view_details: Failed to View the Local Groups of a Security Server Client')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
