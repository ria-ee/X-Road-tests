import unittest
from helpers.list_utils import flatten
from helpers import ssh_client, auditchecker
from main.maincontroller import MainController
from view_models import messages
import time


class XroadUpdateConfiguration(unittest.TestCase):
    """
    CP_15: Update Configuration
    RIA URL: https://jira.ria.ee/browse/XT-423, https://jira.ria.ee/browse/XTKB-211
    Depends on finishing other test(s): CP_16
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_log_out_from_software_token(self):
        main = MainController(self)

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        cs_host = main.config.get('cs.ssh_host')
        anchor_file = '/etc/xroad/confproxy/cp-test/anchor.xml'
        hosts_replacement = 'cs.asd'
        configuration_client_log = '/var/log/xroad/configuration_client.log'

        try:
            '''Change download url in anchor.xml file'''
            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(cs_host, hosts_replacement, anchor_file),
                sudo=True)

            file_age = int(flatten(
                sshclient.exec_command('echo $(($(date +"%s")-$(date +"%s" -r {})))'.format(configuration_client_log)))[
                               0])

            log_checker = auditchecker.AuditChecker(cp_ssh_host, cp_ssh_user, cp_ssh_pass,
                                                    logfile=configuration_client_log)
            current_log_lines = log_checker.get_line_count()
            main.log('Configuration was updated {} seconds ago'.format(file_age))
            if file_age > 60:
                raise AssertionError('Configuration was last edited more than a minute ago')
            if file_age <= 60:
                time_to_wait = 65 - file_age
                main.log('Waiting {} seconds for configuration update'.format(time_to_wait))
                time.sleep(time_to_wait)

            main.log(
                'CP_15 1.System downloads the configuration from a Configuration Source')

            main.log(
                'CP_15 1a. Configuration download terminates with an error. ')

            '''Get log lines'''
            logs_found = log_checker.get_log_lines(from_line=current_log_lines)

            main.is_true(any(messages.CP_DOWNLOAD_UPDATE_CONFIGURATION_ERROR in line for line in logs_found),
                         msg='Error {0} not shown'.format(messages.CP_DOWNLOAD_UPDATE_CONFIGURATION_ERROR))
            main.is_true(any(
                messages.CP_DOWNLOAD_UPDATE_CONFIGURATION_LOCATION_ERROR.format(hosts_replacement) in line for line in
                logs_found), msg='Error {0} not shown'.format(
                messages.CP_DOWNLOAD_UPDATE_CONFIGURATION_LOCATION_ERROR.format(hosts_replacement)))

            '''Correct the anchor.xml file'''
            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(hosts_replacement, cs_host,
                                                     '/etc/xroad/confproxy/cp-test/anchor.xml'),
                sudo=True)

            current_log_lines_correct = log_checker.get_line_count()

            file_age = int(flatten(
                sshclient.exec_command(
                    'echo $(($(date +"%s")-$(date +"%s" -r {})))'.format(anchor_file)))[
                               0])
            main.log('Configuration was updated {} seconds ago'.format(file_age))
            if file_age > 60:
                raise AssertionError('Configuration was last edited more than a minute ago')
            if file_age <= 60:
                time_to_wait = 65 - file_age
                main.log('Waiting {} seconds for configuration update'.format(time_to_wait))
                time.sleep(time_to_wait)

            main.log(
                'CP_15 1.System downloads the configuration from a Configuration Source')

            logs_found_correct = log_checker.get_log_lines(from_line=current_log_lines_correct)
            main.is_true(any(messages.CP_DOWNLOAD_SUCCESSFULL.format(cs_host) in line for line in logs_found_correct),
                         msg='Error {0} not shown'.format(messages.CP_DOWNLOAD_SUCCESSFULL.format(cs_host)))

        finally:
            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(hosts_replacement, cs_host,
                                                     '/etc/xroad/confproxy/cp-test/anchor.xml'),
                sudo=True)
