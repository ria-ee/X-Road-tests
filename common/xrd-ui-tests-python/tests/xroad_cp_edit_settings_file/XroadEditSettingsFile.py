import unittest

from helpers import ssh_client
from main.maincontroller import MainController
from tests.xroad_cp_edit_settings_file.edit_settings_file import test_edit_settings_file


class XroadEditSettingsFile(unittest.TestCase):
    """
    CP_03 Edit Settings File
    RIA URL: https://jira.ria.ee/browse/XTKB-205
    Depends on finishing other test(s): CP_11
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_edit_settings_file(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        cp_conf_location = main.config.get('cp.conf_path')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        edit_service_file = test_edit_settings_file(main, sshclient, cp_identifier, cp_conf_location)
        edit_service_file()
