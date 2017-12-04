import unittest
from main.maincontroller import MainController
import ss_client_management
from helpers import xroad


class XroadDeleteClient(unittest.TestCase):
    '''
    UC MEMBER_53 Delete a Security Server Client
    RIA URL: https://jira.ria.ee/browse/XT-405, https://jira.ria.ee/browse/XTKB-124
    Depends on finishing other test(s): XroadAddClient, XroadRegisterClient
    Requires helper scenarios:
    X-Road version: 6.16.0
    '''

    def test_delete_client(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_53'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client_id = main.config.get('ss2.client_id')
        client_id = 'KS1 : COM : CLIENT1MT : sub'

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')

        test_delete_client = ss_client_management.test_delete_client(case=main, client_id=client_id,
                                                                     ssh_host=ss_ssh_host, ssh_user=ss_ssh_user,
                                                                     ssh_pass=ss_ssh_pass, test_cancel=True)

        try:
            # Open webdriver
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            # Run the test
            test_delete_client()
        except:
            main.log('XroadDeleteClient: Failed to delete client')
            main.save_exception_data()
            assert False
        finally:
            # Test teardown
            # main.tearDown()
            pass
