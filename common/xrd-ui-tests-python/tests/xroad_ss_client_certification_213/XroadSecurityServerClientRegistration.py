from __future__ import absolute_import

import time
import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_ss_client_certification_213 import client_certification


class XroadSecurityServerClientRegistration(unittest.TestCase):
    """
    SS_28 1-3, 5-6, 3a Generate a Key
    SS_29 1-4, 6-11, 4a, 4b, 5a Generate a Certificate Signing Request
    SS_30 1-16 Import a Certificate from Local File System
    RIA URL: https://jira.ria.ee/browse/XT-341, https://jira.ria.ee/browse/XTKB-85
    RIA URL: https://jira.ria.ee/browse/XT-342, https://jira.ria.ee/browse/XTKB-86
    RIA URL: https://jira.ria.ee/browse/XT-343
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_security_server_client_registration_2_1_3(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_28 / SS_29 / SS_30'
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

        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        main.log('SS_28 / SS_29 / SS_30. CERTIFYING SECURITY SERVER CLIENTS')

        try:
            # Create webdriver and go to main URL
            main.reset_webdriver(main.url, main.username, main.password)

            test_func = client_certification.test_generate_csr_and_import_cert(member_name, member_class,
                                                                               check_inputs=True,
                                                                               ss2_ssh_host=ss2_ssh_host,
                                                                               ss2_ssh_user=ss2_ssh_user,
                                                                               ss2_ssh_pass=ss2_ssh_pass,
                                                                               delete_csr_before_import=True)
            test_func(main)

            main.log('Waiting {0} seconds for configuration update'.format(config_wait_time))
            time.sleep(config_wait_time)

            # SS_29 9 test
            test_configuration_update = client_certification.test_configuration(ssh_host, ssh_username,
                                                                                ssh_password,
                                                                                member_name, member_class)
            test_configuration_update(main)
        except AssertionError:
            main.save_exception_data()
            main.log('Error, deleting any data that was added.')
            try:
                # Delete the key
                client_certification.delete_added_key(main, member_name, member_class)
            except:
                pass
            raise
        except:
            main.save_exception_data()
            main.log('Failed to certify security server client.')
            try:
                # Delete the key
                client_certification.delete_added_key(main, member_name, member_class)
            except:
                pass
            assert False
        finally:
            main.tearDown()
