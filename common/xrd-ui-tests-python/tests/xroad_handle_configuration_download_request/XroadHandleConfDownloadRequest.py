import unittest
from helpers import ssh_client
from main.maincontroller import MainController
from view_models import messages


class XroadHandleConfDownloadRequest(unittest.TestCase):
    """
    CP_17: Test Configuration
    RIA URL: https://jira.ria.ee/browse/XTKB-425, https://jira.ria.ee/browse/XTKB-214
    Depends on finishing other test(s): CP_04
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_conf_download_request(self):
        main = MainController(self)

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
        hosts_replacement = 'asd'

        configuration_temp_dir = '/tmp/test_download'
        anchor_file = '/tmp/anchor.xml'
        download_script = '/usr/share/xroad/scripts/download_instance_configuration.sh'

        try:
            main.log('''Cut connetcion with target host''')
            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(cp_ssh_host, hosts_replacement, '/etc/hosts'), sudo=True)

            main.log('''UC CP_17/1 Configuration client requests to download the signed configuration directory or a 
            configuration part file.''')
            download_url = sshclient.exec_command('{0} {1} {2} '.format(download_script, anchor_file,
                                                                        configuration_temp_dir))
            main.log('''UC CP_17/2 System responds with the requested files -  is covered with CP_14/3 and CP_14/4 in
            ...\\x-road-tests\\tests\\xroad_cp_test_configuration\\XroadTestConfiguration.py''')

            '''Get error messages from a system'''
            system_error_message_1 = str(download_url[0][1])
            system_error_message_2 = str(download_url[0][3])
            system_error_message_3 = str(download_url[0][4])

            main.log('UC CP_17/2a Request cannot be served.')
            main.log('UC CP_17/2a1 System responds with an error message.')
            assert messages.CP_CONF_DOWNLOAD_REQUEST_ERROR_1 == system_error_message_1
            main.log('''System responds with an error message - "{0}"'''.format(system_error_message_1))
            assert messages.CP_CONF_DOWNLOAD_REQUEST_ERROR_2 == system_error_message_2
            main.log('''System responds with an error message - "{0}"'''.format(system_error_message_2))
            assert messages.CP_CONF_DOWNLOAD_REQUEST_ERROR_3.format(main.config.get('cp.ssh_host')) in \
                   system_error_message_3
            main.log('''System responds with an error message - "{0}"'''.format(system_error_message_3))
        except:
            main.log('XroadHandleConfDownloadRequest: Failed to to handle a configuration download request')
            main.save_exception_data()
            assert False
        finally:
            main.log('''Restore connetcion with target host''')
            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(hosts_replacement, cp_ssh_host, '/etc/hosts'), sudo=True)
