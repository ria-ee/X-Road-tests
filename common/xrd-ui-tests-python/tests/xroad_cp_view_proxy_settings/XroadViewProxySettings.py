import unittest

from helpers import ssh_client
from helpers.list_utils import flatten
from helpers.ssh_server_actions import exec_as_xroad
from main.maincontroller import MainController
from tests.xroad_cp_activate_configuration_source_signing_key.activate_configuration_source_signing_key import \
    get_all_signing_keys
from tests.xroad_cp_view_proxy_settings import view_conf_proxy_settings
from tests.xroad_cp_view_proxy_settings.view_conf_proxy_settings import check_empty_cp_view_lines, check_cp_view_lines
from view_models.configuration_proxy import CP_CONF_DOES_NOT_EXIST_MSG, get_cp_no_conf_file_errors


class XroadViewProxySettings(unittest.TestCase):
    """
    CP_01 View Proxy Settings
    RIA URL: https://jira.ria.ee/browse/XTKB-206
    Depends on finishing other test(s): CP_11, CP_13
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_a_view_cp_settings_not_existing_proxy(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        not_existing_proxy_name = 'testnotexistingproxy'
        main.log('CP_01 1b Trying to view not existing proxy "{}"'.format(not_existing_proxy_name))
        std_out = flatten(exec_as_xroad(sshclient, 'confproxy-view-conf -p {}'.format(not_existing_proxy_name)))

        expected_msg = CP_CONF_DOES_NOT_EXIST_MSG.format(not_existing_proxy_name)
        main.log('CP_01 1b.1 Checking if not existing proxy error "{}" is visible'.format(expected_msg))
        main.is_true(any(expected_msg in a for a in std_out))

    def test_b_view_cp_settings_not_existing_proxy_conf(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        cp_identifier = main.config.get('cp.empty_cp_identifier')
        proxy_dir = main.config.get('cp.proxy_dir')
        main.log('Creating empty proxy directory with id "{}"'.format(cp_identifier))
        exec_as_xroad(sshclient, 'mkdir {0}'.format(proxy_dir + cp_identifier))
        main.log('CP_01 1c. Trying to view the configuration of the proxy, which configuration file does not exist')
        std_out = flatten(exec_as_xroad(sshclient, 'confproxy-view-conf -p {}'.format(cp_identifier)))
        expected_msgs = get_cp_no_conf_file_errors(cp_identifier)
        main.log('CP_01 1c.1 System notifies with the error messages: {}'.format(', '.join(expected_msgs)))
        main.is_true(all(any(msg in a for a in std_out) for msg in expected_msgs),
                     msg='Expected error messages not found')

    def test_c_view_cp_settings(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.empty_cp_identifier')
        cp_conf_location = main.config.get('cp.empty_cp_conf_path')
        cp_anchor_location = main.config.get('cp.empty_cp_anchor_path')
        conf_url = main.config.get('cp.empty_cp_conf_url')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        main.log('Creating empty config file to proxy "{}"'.format(cp_identifier))
        exec_as_xroad(sshclient, 'touch {0}'.format(cp_conf_location))

        main.log('CP_01 2a. Trying to view settings of a proxy with empty config file')
        std_out = flatten(exec_as_xroad(sshclient, 'confproxy-view-conf -p {}'.format(cp_identifier)))
        main.log('CP_01 2a.1 Following error messages are shown for missing information: ')
        check_empty_cp_view_lines(main, std_out, cp_anchor_location, conf_url)

    def test_d_view_cp_instance_conf(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        cs_identifier = main.config.get('cs.identifier')
        cp_conf_location = main.config.get('cp.conf_path')
        cp_conf_url = main.config.get('cp.conf_url')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)

        main.log('CP_01 1a Trying to view settings of a specific proxy instance "{}"'.format(cp_identifier))
        std_out = flatten(exec_as_xroad(sshclient, 'confproxy-view-conf -p {}'.format(cp_identifier)))
        main.log('Getting all signing keys from configuration file')
        keys = set(get_all_signing_keys(sshclient, cp_conf_location))
        main.log('CP_01 1a.1 System displays the fields for the requested instance: ')
        check_cp_view_lines(main, std_out, cs_identifier, cp_conf_url, keys)

    def test_e_view_all_cp_settings(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_identifier = main.config.get('cp.identifier')
        empty_cp_identifier = main.config.get('cp.empty_cp_identifier')
        empty_cp_anchor_location = main.config.get('cp.empty_cp_anchor_path')
        empty_cp_conf_url = main.config.get('cp.empty_cp_conf_url')
        cp_conf_url = main.config.get('cp.conf_url')
        cp_conf_location = main.config.get('cp.conf_path')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        cs_identifier = main.config.get('cs.identifier')
        '''CP_01 main flow'''
        test_view_all_cp_settings = view_conf_proxy_settings.test_view_all_cp_settings(main, sshclient,
                                                                                       cp_identifier,
                                                                                       empty_cp_identifier,
                                                                                       cp_conf_location,
                                                                                       empty_cp_anchor_location,
                                                                                       cs_identifier,
                                                                                       cp_conf_url,
                                                                                       empty_cp_conf_url)
        test_view_all_cp_settings()
