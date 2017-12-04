import unittest
from main.maincontroller import MainController
from helpers import ssh_client, xroad
from view_models import configuration_proxy
import re


class XroadViewTrustedAnchor(unittest.TestCase):
    """
    CP_12: View Trusted Anchor
    RIA URL: https://jira.ria.ee/browse/XTKB-209
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_log_out_from_software_token(self):
        main = MainController(self)
        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        anchor_path = main.config.get('cp.anchor_path')
        ss_id = xroad.split_xroad_subsystem(main.config.get('ss2.server_id'))
        instance = ss_id['instance']

        '''
        Commands to View Trusted Anchor:
        1. CP administrator selects to view trusted anchor.
        2. System displays the anchor file content.
        '''
        main.log('CP_12: View Trusted Anchor')

        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        main.log('CP_12 1. CP administrator selects to view trusted anchor.')
        main.log('CP_12 2. System displays the anchor file content.')

        generated_at = sshclient.exec_command("grep -o -P '(?<=<generatedAt>).*(?=</generatedAt>)' {0}".format(anchor_path))[0][0]
        instance_identifier = sshclient.exec_command(
            "grep -o -P '(?<=<instanceIdentifier>).*?(?=</instanceIdentifier>)' {0}".format(anchor_path))[0][0]
        verification_cert = sshclient.exec_command(
            "grep -o -P '(?<=<verificationCert>).*?(?=</verificationCert>)' {0}".format(anchor_path))[0][0]

        '''Verify download url tags'''
        try:
            download_url = sshclient.exec_command("grep -o -P 'downloadURL' {0}".format(anchor_path))[0][0]
        except IndexError:
            raise Exception('No download url in anchor.xml file')

        '''"Valid "Generated at" verification'''
        valid_date_time_match = re.match(configuration_proxy.DATE_TIME_REGEX, generated_at)

        main.is_true(valid_date_time_match,
                     msg='No valid "Generated At" timestamp in anchor.xml file')

        '''InstanceIdentifier verification'''
        main.is_equal(instance_identifier, instance,
                      msg='InstanceIdentifier is wrong')

        '''Verify "Verification cert"'''
        if len(verification_cert) != 916:
            raise Exception('Verification cert has wrong length')
