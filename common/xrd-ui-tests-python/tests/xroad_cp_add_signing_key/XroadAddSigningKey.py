import unittest

from helpers import ssh_client
from main.maincontroller import MainController
from tests.xroad_cp_add_signing_key.add_signing_key import generate_signing_key


class XroadAddSigningKey(unittest.TestCase):
    """
    CP_09 Add Configuration Source Signing Key
    RIA URL: https://jira.ria.ee/browse/XTKB-201
    Depends on finishing other test(s): CP_02, CP_05
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_a_cp_add_first_signing_key(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        cp_conf_location = main.config.get('cp.conf_path')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        generate_key = generate_signing_key(main, sshclient, cp_identifier, cp_conf_location, token_id=0,
                                            no_active_key=True)

        generate_key()

    def test_b_cp_add_another_signing_key(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        cp_conf_location = main.config.get('cp.conf_path')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        generate_key = generate_signing_key(main, sshclient, cp_identifier, cp_conf_location, token_id=0)

        generate_key()
