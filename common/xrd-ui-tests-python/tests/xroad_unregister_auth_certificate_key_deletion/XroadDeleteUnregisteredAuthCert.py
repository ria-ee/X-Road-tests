# coding=utf-8
import unittest
from main.maincontroller import MainController
import time
from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss
from helpers import xroad, ssh_client
import del_management


"""
UC SS_42: Unregister an Authentication Certificate on Key Deletion
RIA URL: https://jira.ria.ee/browse/XTKB-122
Depends on finishing other test(s):
Requires helper scenarios:
X-Road version: 6.16.0
"""



class XroadDeleteUnregisteredAuthCert(unittest.TestCase):
    def test_xroad_auth_cert_deletion(self):
        main = MainController(self)
        '''Set test name and number'''
        main.test_number = 'UC SS_42'
        main.log('TEST: UC SS_42: Unregister an Authentication Certificate on Key Deletion')

        ss_url = main.config.get('ss1.host')
        ss_username = main.config.get('ss1.user')
        ss_password = main.config.get('ss1.pass')
        wsdl_url = main.config.get('wsdl.management_service_wsdl_url')
        client2 = main.config.get('ss1.management_id')

        ss2_url = main.config.get('ss2.host')
        ss2_username = main.config.get('ss2.user')
        ss2_password = main.config.get('ss2.pass')

        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        cs_host = main.config.get('cs.host')
        cs_username = main.config.get('cs.user')
        cs_password = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        client_id = main.config.get('ss2.client2_id')
        client_name = main.config.get('ss2.client2_name')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        cert_path = 'temp.pem'
        ss_host = main.config.get('ss1.ssh_host')
        hosts_replacement = 'asd'
        sshclient = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)

        '''Disable wsdl'''
        test_disable_wsdl = del_management.test_disable_wsdl(case=main, ssh_host=ss_url, ssh_username=ss_username,
                                                           ssh_password=ss_password, client=client2, wsdl_url=wsdl_url)
        '''Enable wsdl'''
        test_enable_wsdl = del_management.test_enable_wsdl(case=main, ssh_host=ss_url,
                                                         ssh_username=ss_username,
                                                         ssh_password=ss_password, client=client2,
                                                         wsdl_url=wsdl_url)

        try:
            '''Disable wsdl'''
            main.reload_webdriver(url=ss_url, username=ss_username, password=ss_password)
            main.log('SS_42 9a.2. System logs the event “Add security server failed” to the audit log')

            test_disable_wsdl()

            main.reload_webdriver(url=ss2_url, username=ss2_username, password=ss2_password)
            '''Cert creation'''
            del_management.register_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                               cs_host=cs_ssh_host, client=client, cert_path=cert_path,
                               check_inputs=False, ca_ssh_host=ca_ssh_host,
                               ca_ssh_user=ca_ssh_user, ca_ssh_pass=ca_ssh_pass)()

            registration_in_progress_row = del_management.activate_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass, registered=True)
            del_management.test_add_cert_to_ss(main, cs_host, cs_username, cs_password, client, cert_path,
                                     cs_ssh_host, cs_ssh_user, cs_ssh_pass)
            client_registration_in_ss.approve_requests(main)
            time.sleep(120)

            main.reload_webdriver(url=ss2_url, username=ss2_username, password=ss2_password)
            '''wsdl disable error message function'''
            del_management.wsdl_disabled_error_test(main, registration_in_progress_row)

            main.reload_webdriver(url=ss_url, username=ss_username, password=ss_password)
            test_enable_wsdl()
            '''Cut connetcion with target host'''
            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(ss_host, hosts_replacement, '/etc/hosts'),
                sudo=True)

            main.reload_webdriver(url=ss2_url, username=ss2_username, password=ss2_password)




            del_management.register_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                               cs_host=cs_ssh_host, client=client, cert_path=cert_path,
                               check_inputs=False, ca_ssh_host=ca_ssh_host,
                               ca_ssh_user=ca_ssh_user, ca_ssh_pass=ca_ssh_pass)()

            registration_in_progress_row2 = del_management.activate_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass, registered=True)


            del_management.test_add_cert_to_ss(main, cs_host, cs_username, cs_password, client, cert_path,
                                     cs_ssh_host, cs_ssh_user, cs_ssh_pass)
            client_registration_in_ss.approve_requests(main)

            time.sleep(120)

            main.reload_webdriver(url=ss2_url, username=ss2_username, password=ss2_password)

            '''No connection error message test'''
            del_management.no_connection_test(main, registration_in_progress_row2)


            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(hosts_replacement, ss_host, '/etc/hosts'),
                sudo=True)
        except:
            main.log('Xroad_Unregistred_auth_cert_deletion test failed')
            main.save_exception_data()
            assert False
        finally:

            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(hosts_replacement, ss_host, '/etc/hosts'),
                sudo=True)

            '''Test teardown'''
            main.tearDown()
