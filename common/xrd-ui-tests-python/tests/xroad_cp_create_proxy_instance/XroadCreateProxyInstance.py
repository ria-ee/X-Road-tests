import unittest

from helpers import ssh_client
from helpers.list_utils import flatten
from helpers.ssh_server_actions import exec_as_xroad
from main.maincontroller import MainController
from view_models.configuration_proxy import CP_CREATION_CP_EXISTS_MESSAGE, get_cp_creation_success_messages, \
    VALIDITY_CONFIG_LINE, VALIDITY_DEFAULT_TIMEOUT


class XroadCreateProxyInstance(unittest.TestCase):
    """
    CP_02 Create Proxy Instance
    RIA URL: https://jira.ria.ee/browse/XTKB-199
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_create_proxy_instance(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        identifier = main.config.get('cp.identifier')
        conf_path = main.config.get('cp.conf_path')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        expected_conf_line = VALIDITY_CONFIG_LINE.format(VALIDITY_DEFAULT_TIMEOUT)
        success_messages = get_cp_creation_success_messages(identifier)

        main.log('CP_02 1. Creating configuration proxy instance with "{}" identifier'.format(identifier))
        std_out = exec_as_xroad(sshclient, 'confproxy-create-instance -p {0}'.format(identifier))
        main.log('Checking if script output contains {}'.format(success_messages))
        main.is_true(all(x in flatten(std_out) for x in success_messages),
                     msg='Configuration Proxy instance creation failed, creation script output: {}'.format(flatten))
        main.log('Configuration Proxy instance created successfully')
        main.log('CP_02 2. System creates the settings directory for the new proxy instance and '
                 '\ngenerates the initial configuration file \'conf.ini\', '
                 'containing a default value (600) for validity-interval-seconds')
        std_out = sshclient.exec_command(
            'grep \'{0}\' {1}'.format(expected_conf_line, conf_path))
        main.is_equal(expected_conf_line, std_out[0][0])

    def test_create_proxy_instance_exists(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        identifier = main.config.get('cp.identifier')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        expected_message = CP_CREATION_CP_EXISTS_MESSAGE.format(identifier)

        main.log(
            'CP_02 1. Trying to create existing configuration proxy instance with "{}" identifier'.format(identifier))
        std_out = exec_as_xroad(sshclient, 'confproxy-create-instance -p {0}'.format(identifier))
        main.log('CP_02 1a. System notifies with the error message "{}"'.format(expected_message))
        main.is_true(any(expected_message in line for line in flatten(std_out)),
                     msg='Expected cp creation to fail with "{0}" message, got: {1}'.format(expected_message, std_out))
