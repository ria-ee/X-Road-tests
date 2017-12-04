# coding=utf-8
import unittest
from main.maincontroller import MainController
from helpers import xroad
import del_management

"""
UC SS_40: Delete a Certificate from Hardware Token
RIA URL: https://jira.ria.ee/browse/XTKB-165
Depends on finishing other test(s):
Requires helper scenarios:
X-Road version: 6.16.0
"""


class XroadDeleteHardwareTokenCertificate(unittest.TestCase):
    def test_xroad_delete_hardtoken_cert(self):
        main = MainController(self)
        '''Set test name and number'''
        main.test_number = 'UC SS_40'
        main.log('TEST: UC SS_40: Delete a Certificate from Hardware Token')



        ss1_url = main.config.get('ss1.host')
        ss1_username = main.config.get('ss1.user')
        ss1_password = main.config.get('ss1.pass')

        ss1_ssh_host = main.config.get('ss1.ssh_host')
        ss1_ssh_user = main.config.get('ss1.ssh_user')
        ss1_ssh_pass = main.config.get('ss1.ssh_pass')

        client_id = main.config.get('ss1.server_id')
        client_name = main.config.get('ss1.client2_name')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        cert_path = 'temp.pem'


        try:

            # '''Cut connetcion with target host'''
            # sshclient.exec_command(
            #     'sed -i -e "s/{0}/{1}/g" {2}'.format(ss_host, hosts_replacement, '/etc/hosts'),
            #     sudo=True)


            main.reload_webdriver(url=ss1_url, username=ss1_username, password=ss1_password)
            '''Cert creation'''
            del_management.register_cert(main, ss1_ssh_host, ss1_ssh_user, ss1_ssh_pass,
                                         client=client, cert_path=cert_path,
                                         check_inputs=False, ca_ssh_host=ca_ssh_host,
                                         ca_ssh_user=ca_ssh_user, ca_ssh_pass=ca_ssh_pass)()


            del_management.delete_cert(main, ss1_ssh_host, ss1_ssh_user, ss1_ssh_pass)

        except:
            main.log('XroadDeleteHardwareTokenCertificate test failed')
            main.save_exception_data()
            assert False
        finally:
            # '''Create connection with target host'''
            # sshclient.exec_command(
            #     'sed -i -e "s/{0}/{1}/g" {2}'.format(hosts_replacement, ss_host, '/etc/hosts'),
            #     sudo=True)

            '''Test teardown'''
            main.tearDown()
