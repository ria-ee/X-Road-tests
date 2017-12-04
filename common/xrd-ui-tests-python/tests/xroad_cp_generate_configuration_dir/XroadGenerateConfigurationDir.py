import unittest

from helpers import ssh_client
from main.maincontroller import MainController
from tests.xroad_cp_generate_configuration_dir import generate_configuration_dir


class XroadGenerateConfigurationDir(unittest.TestCase):
    """
    CP_16 Generate Configuration Directory
    RIA URL: https://jira.ria.ee/browse/XTKB-212
    Depends on finishing other test(s): CP_02, CP_13
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_generate_configuration_dir(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        cs_identifier = main.config.get('cs.identifier')
        cp_ssh_client = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        cp_url = main.config.get('cp.conf_url')
        conf_dir = main.config.get('cp.generated_conf_path')
        hash_algorithm = main.config.get('cp.hash_algorithm')
        instance_conf_dir = '{}/{}'.format(conf_dir, cp_identifier)
        cs_ssh_client = ssh_client.SSHClient(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        test_generate_conf_dir = generate_configuration_dir.test_generate_configuration_dir(main, cp_ssh_client,
                                                                                            cs_ssh_client,
                                                                                            instance_conf_dir,
                                                                                            conf_dir, cs_identifier,
                                                                                            hash_algorithm, cp_url)
        test_generate_conf_dir()
