import unittest
from helpers import ssh_client
from main.maincontroller import MainController
from view_models import configuration_proxy


class XroadTestConfiguration(unittest.TestCase):
    """
    CP_14: Test Configuration
    RIA URL: https://jira.ria.ee/browse/XTKB-211
    Depends on finishing other test(s): CP_04
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_log_out_from_software_token(self):
        main = MainController(self)

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        cp_url = main.config.get('cp.conf_url')

        configuration_temp_dir = '/tmp/test_download'
        anchor_file = '/tmp/anchor.xml'
        download_script = '/usr/share/xroad/scripts/download_instance_configuration.sh'
        try:

            main.log(
                'CP_14 2.CP administrator runs the configuration download script providing it with the generated anchor and a directory for placing the downloaded configuration.')

            '''Run download script'''
            download_url = sshclient.exec_command(
                '{0} {1} {2} '.format(download_script, anchor_file, configuration_temp_dir))

            url = download_url[0][0]
            shared_parameters = download_url[0][4]
            private_parameters = download_url[0][7]

            main.log(
                'CP_14 3.The configuration is downloaded from the configuration source: UC GCONF_21: Download Configuration from a Configuration Source.')

            '''Verify url'''
            if cp_url not in url:
                raise Exception('Downloading configuration url is wrong.')
            '''Verify saving of shared parameters content'''
            if configuration_proxy.CP_SHARED_PARAMETERS not in shared_parameters:
                raise Exception('Saving shared parameters content to wrong file')
            '''Verify saving of private parameters content'''
            if configuration_proxy.CP_PRIVATE_PARAMETERS not in private_parameters:
                raise Exception('Saving private parameters content to wrong file')

            main.log(
                'CP_14 4.CP administrator verifies that configuration download and configuration directory generation were successful.')

            '''Verify created directory'''
            try:
                sshclient.exec_command('find /tmp -name KS1 -type d')[0][0]
            except IndexError:
                raise Exception('No directory found')

            '''Verify instance-identifier file'''
            try:
                sshclient.exec_command('find /tmp -name instance-identifier -type f')[0][0]
            except IndexError:
                raise Exception('No instance-identifier file found')

            '''Verify private-params.xml file'''
            try:
                sshclient.exec_command('find /tmp -name private-params.xml -type f')[0][0]
            except IndexError:
                raise Exception('No private-params.xml file found')

            '''Verify private-params.xml.metadata file'''
            try:
                sshclient.exec_command('find /tmp -name private-params.xml.metadata -type f')[0][0]
            except IndexError:
                raise Exception('No private-params.xml.metadata file found')

            '''Verify shared-params.xml file'''
            try:
                sshclient.exec_command('find /tmp -name shared-params.xml -type f')[0][0]
            except IndexError:
                raise Exception('No shared-params.xml file found')

            '''Verify shared-params.xml.metadata file'''
            try:
                sshclient.exec_command('find /tmp -name shared-params.xml.metadata -type f')[0][0]
            except IndexError:
                raise Exception('No shared-params.xml.metadata file found')
        finally:
            '''Delete test_download directory'''
            sshclient.exec_command('rm -rf {}'.format(configuration_temp_dir))
