import unittest
from main.maincontroller import MainController
import cs_client_management
from helpers import xroad


class XroadCreateClientRegistrationRequest(unittest.TestCase):
    '''
    UC MEMBER_15 Create a Security Server Client Registration Request
    '''

    def test_xroad_register_client(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_15'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        client_id = 'KS1 : COM : CLIENT1 : kalamaja'  # main.config.get('ss1.client_id')
        client_name = 'Client One'

        server = xroad.split_xroad_id(main.config.get('ss1.server_id'), type='SERVER')

        existing_client = xroad.split_xroad_subsystem(main.config.get('ss1.client_id'))
        existing_client['name'] = main.config.get('ss1.client_name')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        # Configure the service
        test_add_client = cs_client_management.test_create_registration_request(case=main, server=server,
                                                                                client_name=client_name,
                                                                                client_id=client_id, duplicate_client=existing_client,
                                                                                ssh_host=cs_ssh_host,
                                                                                ssh_user=cs_ssh_user, ssh_pass=cs_ssh_pass)

        test_delete_client = cs_client_management.test_delete_client(case=main, client_id=client_id, ssh_host=cs_ssh_host,
                                                     ssh_user=cs_ssh_user, ssh_pass=cs_ssh_pass)

        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

            # Run the test
            test_add_client()
        except:
            main.log('XroadCreateClientRegistrationRequest: Failed to add client registration request')
            main.save_exception_data()
            try:
                # Delete service
                main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

                test_delete_client()
            except:
                main.log('XroadCreateClientRegistrationRequest: Failed to delete added data.')
                main.save_exception_data()
            assert False
        finally:
            # Test teardown
            # main.tearDown()
            pass
