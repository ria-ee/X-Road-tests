from __future__ import absolute_import

import unittest

import time
from helpers import xroad
from tests.xroad_ss_client_certification_213 import client_certification_2_1_3
from main.maincontroller import MainController


class SecurityServerClientRegistration(unittest.TestCase):
    def test_security_server_client_registration_2_1_3(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.1.3'
        main.test_name = self.__class__.__name__

        ssh_host = main.config.get('ss2.ssh_host')
        ssh_username = main.config.get('ss2.ssh_user')
        ssh_password = main.config.get('ss2.ssh_pass')

        config_wait_time = 120

        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
        client_id = main.config.get('ss2.client2_id')

        client = xroad.split_xroad_id(client_id)
        member_name = client['code']
        member_class = client['class']

        main.log('TEST: CERTIFYING SECURITY SERVER CLIENTS')

        try:
            # Create webdriver and go to main URL
            main.reset_webdriver(main.url, main.username, main.password)

            # TODO: check_inputs=True
            test_func = client_certification_2_1_3.test(member_name, member_class, check_inputs=False)
            test_func(main)

            main.log('Waiting {0} seconds for configuration update'.format(config_wait_time))
            time.sleep(config_wait_time)

            main.test_number = '2.1.3 / SS_29-9'

            test_configuration_update = client_certification_2_1_3.test_configuration(ssh_host, ssh_username, ssh_password,
                                                                                      member_name, member_class)
            test_configuration_update(main)
        except AssertionError:
            main.log('Error, deleting any data that was added.')
            try:
                # Delete the key
                client_certification_2_1_3.delete_added_key(main, member_name, member_class)
            except:
                pass
            raise
        except:
            main.log('Failed to certify security server client.')
            try:
                # Delete the key
                client_certification_2_1_3.delete_added_key(main, member_name, member_class)
            except:
                pass
            assert False
        finally:
            main.tearDown()
