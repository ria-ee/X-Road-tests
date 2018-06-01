import re
import unittest
import xml.etree.ElementTree

from helpers import ssh_client
from helpers.list_utils import flatten
from helpers.ssh_server_actions import exec_as_xroad
from main.maincontroller import MainController
from view_models.configuration_proxy import CP_CONF_DOES_NOT_EXIST_MSG, get_cp_could_not_load_source_anchor_errors, \
    NO_SIGNING_KEYS_CONFIGURED_ERROR_MSG, CP_ANCHOR_TIME_REGEX, GENERATED_ANCHOR_XML_TO_MSG


class XroadGenerateConfigurationSourceAnchor(unittest.TestCase):
    """
    CP_04 Generate Configuration Source Anchor
    RIA URL: https://jira.ria.ee/browse/XTKB-210
    Depends on finishing other test(s): CP_01
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_a_generate_configuration_source_anchor_no_instance(self):
        main = MainController(self)
        main.test_number = 'CP_04.a'
        main.test_name = self.__class__.__name__

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        not_existing_proxy_name = 'notExistingProxy'
        main.log('CP_04 1b. Trying to generate a configuration anchor '
                 'for a proxy instance that does not exist({})'.format(not_existing_proxy_name))
        std_out = flatten(
            exec_as_xroad(sshclient, 'confproxy-generate-anchor -p {} -f anchor.xml'.format(not_existing_proxy_name)))
        expected_msg = CP_CONF_DOES_NOT_EXIST_MSG.format(not_existing_proxy_name)
        main.log('CP_04 1b.1 System notifies with the error message: "{}"'.format(expected_msg))
        main.is_true(any(expected_msg in a for a in std_out), msg='Expected error msgs not found')

    def test_b_generate_configuration_source_anchor_no_source_anchor(self):
        main = MainController(self)
        main.test_number = 'CP_04.b'
        main.test_name = self.__class__.__name__

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        cp_identifier = main.config.get('cp.empty_cp_identifier')
        main.log('CP_04 2a. Trying to generate a configuration anchor for a proxy, '
                 'which source anchor does not exist({})'.format(cp_identifier))
        std_out = flatten(
            exec_as_xroad(sshclient, 'confproxy-generate-anchor -p {} -f anchor.xml'.format(cp_identifier)))
        expected_msgs = get_cp_could_not_load_source_anchor_errors(cp_identifier)
        main.log('CP_04 2a.1 System notifies with the error message: "{}"'.format(' '.join(expected_msgs)))
        main.is_true(all(any(msg in a for a in std_out) for msg in expected_msgs), msg='Expected error msgs not found')

    def test_c_generate_configuration_source_anchor_no_signing_keys(self):
        main = MainController(self)
        main.test_number = 'CP_04.c'
        main.test_name = self.__class__.__name__

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        cp_identifier = main.config.get('cp.empty_cp_identifier')
        valid_cp_anchor_path = main.config.get('cp.anchor_path')
        empty_cp_anchor_path = main.config.get('cp.empty_cp_anchor_path')
        main.log('Copying anchor file from "{}" to "{}"'.format(valid_cp_anchor_path, empty_cp_anchor_path))
        exec_as_xroad(sshclient, 'cp -p {} {}'.format(valid_cp_anchor_path, empty_cp_anchor_path))
        main.log('CP_04 2c. Trying to generate sourche anchor '
                 'for proxy which has no signing keys({})'.format(cp_identifier))
        std_out = flatten(
            exec_as_xroad(sshclient, 'confproxy-generate-anchor -p {} -f anchor.xml'.format(cp_identifier)))
        expected_msg = NO_SIGNING_KEYS_CONFIGURED_ERROR_MSG
        main.log('CP_04 2c.1 System notifies with the error message: "{}"'.format(expected_msg))
        main.is_true(any(expected_msg in row for row in std_out), msg='Expected error msgs not found')

    def test_d_generate_configuration_source_anchor_no_write_permissions(self):
        main = MainController(self)
        main.test_number = 'CP_04.d'
        main.test_name = self.__class__.__name__

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        cp_identifier = main.config.get('cp.identifier')
        dest_path = '/etc/anchor.xml'
        main.log('CP_04 3a. Trying to generate {} anchor '
                 'without writing permissions in folder "{}"'.format(cp_identifier, dest_path))
        std_out = flatten(exec_as_xroad(sshclient, 'confproxy-generate-anchor -p {} -f {}'.format(cp_identifier,
                                                                                                  dest_path)))
        expected_msg = 'Cannot write anchor to \'{}\', permission denied.'.format(dest_path)
        main.log('CP_04 3a.1 System notifies with the error message: "{}"'.format(expected_msg))
        main.is_true(any(expected_msg in a for a in std_out), msg='Expected error msgs not found')

    def test_e_generate_configuration_source_anchor(self):
        main = MainController(self)
        main.test_number = 'CP_04.e'
        main.test_name = self.__class__.__name__

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        cs_identifier = main.config.get('cs.identifier')
        cp_identifier = main.config.get('cp.identifier')
        cp_url = main.config.get('cp.conf_url')
        dest_path = '/tmp/anchor.xml'
        main.log('CP_04 1. Trying to generate {} configuration anchor to {}'.format(cp_identifier, dest_path))
        std_out = flatten(exec_as_xroad(sshclient, 'confproxy-generate-anchor -p {} -f {}'.format(cp_identifier,
                                                                                                  dest_path)))
        main.log('CP_04 3. System generates and saves the anchor file')
        expected_msg = GENERATED_ANCHOR_XML_TO_MSG.format(dest_path)
        main.log('Checking success message "{}"'.format(expected_msg))
        main.is_true(any(expected_msg in a for a in std_out), msg='Expected success msg not found')

        main.log('Get written anchor file content')
        std_out = flatten(sshclient.exec_command('sudo cat {}'.format(dest_path)))
        main.log('Parse XML')
        root = ''.join(std_out)
        root = xml.etree.ElementTree.fromstring(root)
        main.log('Checking if instance identifier equal to {}'.format(cs_identifier))
        main.is_equal(root.find('instanceIdentifier').text, cs_identifier)
        main.log('Checking if generated at matches regex {}'.format(CP_ANCHOR_TIME_REGEX))
        date = root.find('generatedAt').text
        main.is_true(re.match(CP_ANCHOR_TIME_REGEX, date))
        source = root.find('source')
        main.log('Checking if one verification cert element present')
        verification_cert = source.findall('verificationCert')
        main.is_true(len(verification_cert) == 1)
        download_url = source.find('downloadURL').text
        main.log('Checking if downloadURL is {}'.format(download_url))
        main.is_equal(cp_url, download_url)
