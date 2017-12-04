import unittest
import paramiko
from helpers.ssh_server_actions import exec_commands
from main.maincontroller import MainController


class XroadLogoutSoftwareToken(unittest.TestCase):
    """
    CP_07: Log Out of Software Security Token
    RIA URL: https://jira.ria.ee/browse/XTKB-207
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_log_out_from_software_token(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        ssh_client.connect(hostname=cp_ssh_host, username=cp_ssh_user, password=cp_ssh_pass)
        '''
        Commands to  log out from software token:
        1. Logout as user "xroad"
        2. Logout from software token
        3. List tokens
        '''
        main.log('CP_07 1. CP administrator selects to log out of a token.')
        commands = ['sudo su - xroad', cp_ssh_pass, 'signer-console lo 0', 'signer-console lt']
        output = exec_commands(main, ssh_client, commands, timeout=3)

        main.log('CP_07 2. System logs out of the token.')
        main.log('Checking if software token is in "inactive" state')
        main.is_true('Token: 0 (OK, writable, available, inactive)' in output, msg='Software token is in "active" state')