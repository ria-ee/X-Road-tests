import unittest

from helpers import ssh_client
from main.maincontroller import MainController
from tests.xroad_cp_activate_configuration_source_signing_key.activate_configuration_source_signing_key import \
    get_active_key, get_all_signing_keys, get_first_inactive_key
from tests.xroad_cp_delete_signing_key.delete_signing_key import test_delete_signing_key


class XroadDeleteSigningKey(unittest.TestCase):
    """
    CP_11 Delete Configuration Source Signing Key
    RIA URL: https://jira.ria.ee/browse/XTKB-204
    Depends on finishing other test(s): CP_10
    Requires helper scenarios: get_all_signing_keys, get_active_key
    X-Road version: 6.16.0
    """

    def test_delete_active_signing_key(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        cp_conf_location = main.config.get('cp.conf_path')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        active_key_id = get_active_key(sshclient, cp_identifier)
        delete_active_signing_key = test_delete_signing_key(main, sshclient, cp_identifier, active_key_id,
                                                            cp_conf_location, active=True)
        delete_active_signing_key()

    def test_delete_not_existing_signing_key(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        cp_conf_location = main.config.get('cp.conf_path')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        delete_not_existing_signing_key = test_delete_signing_key(main, sshclient, cp_identifier, 'asd',
                                                                  cp_conf_location, not_exists=True)
        delete_not_existing_signing_key()

    def test_delete_signing_key(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        cp_path = main.config.get('cp.conf_path')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        active_key_id = get_active_key(sshclient, cp_identifier)
        inactive_key = get_first_inactive_key(active_key_id, get_all_signing_keys(sshclient, cp_path))

        delete_signing_key = test_delete_signing_key(main, sshclient, cp_identifier, inactive_key,
                                                     cp_path)
        delete_signing_key()
