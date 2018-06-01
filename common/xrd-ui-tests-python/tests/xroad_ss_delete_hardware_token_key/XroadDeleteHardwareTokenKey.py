# coding=utf-8
import unittest

import ht_management
from helpers import ssh_client
from main.maincontroller import MainController
from tests.xroad_configure_service_222.wsdl_validator_errors import wait_until_server_up
import os

class XroadDeleteHardwareTokenKey(unittest.TestCase):
    """
    SS_35 6. Delete a Key from the System Configuration
    UC SS_37: Delete a Key from a Hardware Token
    RIA URL: https://jira.ria.ee/browse/XTKB-162
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_xroad_delete_hardtoken_key(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC SS 37'
        main.log('TEST:  UC SS_37: Delete a Key from a Hardware Token')

        main.test_name = self.__class__.__name__

        ss_host = main.config.get('hwtoken.host')
        ss_user = main.config.get('hwtoken.user')
        ss_pass = main.config.get('hwtoken.pass')
        ss_token_pin = main.config.get('hwtoken.token_pin')

        ss_ssh_host = main.config.get('hwtoken.ssh_host')
        ss_ssh_user = main.config.get('hwtoken.ssh_user')
        ss_ssh_pass = main.config.get('hwtoken.ssh_pass')

        '''Configure the service'''
        test_delete_key = ht_management.test_hardware_key_delete(case=main, ssh_host=ss_ssh_host,
                                                                 ssh_username=ss_ssh_user,
                                                                 ssh_password=ss_ssh_pass, pin=ss_token_pin)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            '''Run the test'''
            test_delete_key()
        except:
            main.log('test_xroad_delete_hardtoken_key: Failed to delete Hardware Token key')
            main.save_exception_data()
            raise
        finally:
            '''Test teardown'''
            sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
            '''Start preconfigured docker container'''
            os.system('sudo docker run -p3001:3001 -dt --rm --name cssim410_test cssim410_test')
            '''Restart xroad-signer service'''
            sshclient.exec_command('service xroad-signer restart', sudo=True)
            wait_until_server_up(main.url)

            main.tearDown()
