import unittest
from main.maincontroller import MainController
import ss_client_management
from helpers import xroad


class XroadAddClient(unittest.TestCase):
    '''
    UC MEMBER_47 Add a Client
    RIA URL: https://jira.ria.ee/browse/XT-399, https://jira.ria.ee/browse/XTKB-40
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    '''

    def test_xroad_register_client(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_47'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client_id = main.config.get('ss2.client_id')
        client_name = main.config.get('ss2.client_name')

        existing_client = xroad.split_xroad_subsystem(main.config.get('ss2.client2_id'))
        existing_client['name'] = main.config.get('ss2.client2_name')

        unregistered_member = xroad.split_xroad_subsystem(
            '{0} : {1} : _UNREGISTERED : _unregistered'.format(existing_client['instance'], existing_client['class']))

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')

        # Configure the service
        test_add_client = ss_client_management.test_add_client(case=main,
                                                               client_name=client_name,
                                                               client_id=client_id, duplicate_client=existing_client,
                                                               unregistered_member=unregistered_member,
                                                               ssh_host=ss_ssh_host,
                                                               ssh_user=ss_ssh_user, ssh_pass=ss_ssh_pass,
                                                               check_errors=True
                                                               )

        test_delete_client = ss_client_management.test_delete_client(case=main, client_id=client_id)

        try:
            # Open webdriver
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            # Run the test
            test_add_client()
        except:
            main.log('XroadAddClient: Failed to add client')
            main.save_exception_data()
            try:
                # Delete service
                main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

                test_delete_client()
            except:
                main.log('XroadAddClient: Failed to delete added data.')
                main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
