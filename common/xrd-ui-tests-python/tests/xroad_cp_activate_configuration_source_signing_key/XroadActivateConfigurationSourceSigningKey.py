import unittest

from helpers import ssh_client
from main.maincontroller import MainController
from tests.xroad_cp_activate_configuration_source_signing_key.activate_configuration_source_signing_key import \
    activate_signing_key


class XroadActivateConfigurationSourceSigningKey(unittest.TestCase):
    """
    CP_10 Activate Configuration Source Signing Key
    RIA URL: https://jira.ria.ee/browse/XTKB-203
    Depends on finishing other test(s): CP_09
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_activate_configuration_source_signing_key(self):
        main = MainController(self)

        main.test_number = 'CP_10'
        main.test_name = self.__class__.__name__

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        conf_path = main.config.get('cp.conf_path')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        activate_signing_key(main, sshclient, conf_path, cp_identifier)
