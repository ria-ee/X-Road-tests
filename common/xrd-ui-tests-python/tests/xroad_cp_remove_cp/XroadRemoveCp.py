import unittest
from main.maincontroller import MainController
from helpers import ssh_client

class XroadRemoveCp(unittest.TestCase):
    """
    RIA URL: None
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_upload_trusted_anchor(self):
        main = MainController(self)
        main.test_number = 'XroadRemoveCp'
        main.test_name = self.__class__.__name__


        main.log('Clear environment from CP')

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')

        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)

        sshclient.exec_command('sudo apt-get purge -y xroad-*', sudo=True)
        sshclient.exec_command('sudo rm -rf /etc/xroad/ /var/lib/xroad/', sudo=True)
