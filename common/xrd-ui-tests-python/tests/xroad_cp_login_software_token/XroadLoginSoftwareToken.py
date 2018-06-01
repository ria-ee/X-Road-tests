import re
import unittest

import paramiko

from helpers.ssh_server_actions import exec_commands
from main.maincontroller import MainController
from view_models.configuration_proxy import PIN_INCORRECT_ERROR_MSG


class XroadLoginSoftwareToken(unittest.TestCase):
    """
    CP_05 Log in to a Software Security Token
    RIA URL: https://jira.ria.ee/browse/XTKB-200
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_a_login_to_software_token_wrong_pin(self):
        main = MainController(self)
        main.test_number = 'CP_05.a'
        main.test_name = self.__class__.__name__

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        ssh_client.connect(hostname=cp_ssh_host, username=cp_ssh_user, password=cp_ssh_pass)
        token_pin = str(main.config.get('cp.token_pin'))
        '''
        Commands to initialize software token:
        1. Login as user "xroad"
        2. Initialize software token with pin from configuration
        3. List tokens
        '''

        commands = ['sudo su - xroad', cp_ssh_pass, 'signer-console ist', token_pin, token_pin, 'signer-console lt']
        main.log('Initializing software token with pin "{}"'.format(token_pin))
        output = exec_commands(main, ssh_client, commands, timeout=4)
        main.log('Checking if token is initalized and in inactive state')
        main.is_true('Token: 0 (OK, writable, available, inactive)' in output)
        '''
        Commands to  log in to software token with invalid pin:
        1. Login as user "xroad"
        2. Try to login to software token with wrong pin
        '''
        commands = ['sudo su - xroad', cp_ssh_pass, 'signer-console li 0', '1124351']
        main.log('Executing commands {}'.format(commands))
        output = exec_commands(main, ssh_client, commands, timeout=4)
        expected_message = PIN_INCORRECT_ERROR_MSG
        main.log('CP_05 3a.1 System displays the error message "{}"'.format(expected_message))
        main.is_true(expected_message in output, msg='Error "{}" not displayed'.format(expected_message))

    def test_b_login_to_software_token(self):
        main = MainController(self)
        main.test_number = 'CP_05.b'
        main.test_name = self.__class__.__name__

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        token_pin = str(main.config.get('cp.token_pin'))
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        ssh_client.connect(hostname=cp_ssh_host, username=cp_ssh_user, password=cp_ssh_pass)
        '''
        Commands to  log in to software token:
        1. Login as user "xroad"
        2. Login to software token with pin from configuration
        3. List tokens
        '''
        commands = ['sudo su - xroad', cp_ssh_pass, 'signer-console li 0', str(token_pin), 'signer-console lt']
        main.log('CP_05 1-2. Logging in to software security token with pin "{}"'.format(token_pin))
        output = exec_commands(main, ssh_client, commands, timeout=4)
        main.log('CP_05 3. System verifies the PIN code is correct and logs in to the token')
        main.log('Checking if software token is in "active" state')
        main.is_true('Token: 0 (OK, writable, available, active)' in output, msg='Software token not in "active" state')

