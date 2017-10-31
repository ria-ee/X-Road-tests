import unittest
from main.maincontroller import MainController
import view_management
from helpers import xroad
from view_models import popups


class XroadViewCSMembers(unittest.TestCase):
    '''
    UC MEMBER_04: View X-Road Members
    UC MEMBER_05: View the Details of an X-Road Member
    UC MEMBER_06: View the Security Servers Owned by an X-Road Member
    UC MEMBER_07: View the Subsystems of an X-Road Member
    UC MEMBER_08: View the Security Servers Used by an X-Road Member
    UC MEMBER_09: View the Management Requests Associated with an X-Road Member
    '''

    def test_xroad_verify_ts(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_04: View X-Road Members, ' \
                           'UC MEMBER_05: View the Details of an X-Road Member,' \
                           'UC MEMBER_06: View the Security Servers Owned by an X-Road Member,' \
                           'UC MEMBER_07: View the Subsystems of an X-Road Member,' \
                           'UC MEMBER_08: View the Security Servers Used by an X-Road Member, ' \
                           'UC MEMBER_09: View the Management Requests Associated with an X-Road Member'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ss1_server_name = main.config.get('ss1.server_name')
        ss1_management_id = xroad.split_xroad_id(main.config.get('ss1.management_id'))
        ss1_class = ss1_management_id['class']
        ss1_subsystem = ss1_management_id['subsystem']
        ss1_code = ss1_management_id['code']


        # Configure the service
        test_select_members = view_management.test_select_members(case=main, ss1_server_name=ss1_server_name, ss1_class=ss1_class, ss1_code=ss1_code)
        test_member_details = view_management.test_members_details(case=main)
        test_list_security_servers = view_management.test_list_security_servers(case=main, ss1_server_name=ss1_server_name)
        test_view_member_subystems = view_management.test_view_member_subystems(case=main, ss1_server_name=ss1_server_name, ss1_subsystem=ss1_subsystem, ss1_class=ss1_class, ss1_code=ss1_code)
        test_view_security_servers = view_management.test_view_security_servers(case=main, ss1_server_name=ss1_server_name, ss1_subsystem=ss1_subsystem, ss1_class=ss1_class, ss1_code=ss1_code)
        test_view_member_management_requests = view_management.test_view_member_management_requests(case=main)
        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

            # Run the test
            test_select_members()
            test_member_details()
            test_list_security_servers()
            test_view_member_subystems()
            test_select_members()
            test_view_security_servers()
            test_select_members()
            test_view_member_management_requests()

        except:
            main.log('XroadViewCSMember: Failed to view CS member')
            main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
