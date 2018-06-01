import time
import unittest

from selenium.webdriver.common.by import By

from helpers import xroad, auditchecker, ssh_client
from helpers.ssh_server_actions import get_keyconf_update_timeout
from main.maincontroller import MainController
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import disable_management_wsdl, \
    enable_management_wsdl
from tests.xroad_parse_users_inputs.xroad_parse_user_inputs import add_key_label
from tests.xroad_ss_client_certification_213.client_certification import register_cert
from tests.xroad_ss_delete_key_from_configuration.delete_key_from_configuration import delete_key_from_configuration, \
    wait_until_proxy_up
from view_models.sidebar import KEYSANDCERTIFICATES_BTN_CSS


class XroadDeleteKeyFromConfiguration(unittest.TestCase):
    """
    SS_35 Delete a Key from the System Configuration
    SS_42 Unregister an Authentication Certificate on Key Deletion
    RIA URL: https://jira.ria.ee/browse/XTKB-122
    RIA URL: https://jira.ria.ee/browse/XTKB-223
    Depends on finishing other test(s): MEMBER_01
    Requires helper scenarios: SS_28, SS_34, SERVICE_12, SERVICE_13
    X-Road version: 6.16.0
    """

    def test_a_delete_key_from_configuration_canceling(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_35/42.a'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        main.log('XroadDeleteKeyFromConfiguration.test_a_delete_key_from_configuration_canceling')
        main.test_number = 'XroadDeleteKeyFromConfiguration.test_a'

        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')
        ca_name = main.config.get('ca.name')
        cert_path = 'temp.pem'
        client_id = main.config.get('ss1.server_id')
        client_name = main.config.get('ss1.server_name')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name
        auth_deletion = 'test_key_deletion'

        test_register_cert = register_cert(main, ss_ssh_host, ss_ssh_user, ss_ssh_pass,
                                           client=client,
                                           cs_host=None,
                                           ca_ssh_host=ca_ssh_host, ca_ssh_user=ca_ssh_user,
                                           ca_ssh_pass=ca_ssh_pass,
                                           cert_path=cert_path, ca_name=ca_name, dns='test', organization='test',
                                           key_name=auth_deletion)
        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            main.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
            main.wait_jquery()
            main.log('Adding key to server')
            add_key_label(main, auth_deletion)
            main.log('Creating and registering cert')
            test_register_cert()
            timeout = get_keyconf_update_timeout(sshclient)
            main.log('Waiting {} seconds for keyconf update'.format(timeout))
            time.sleep(timeout)
            delete_key_from_configuration(main, auth_deletion, sshclient, try_cancel=True)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_b_delete_key_unregister_error(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_35/42.b'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        main.log('XroadDeleteKeyFromConfiguration.test_b_delete_key_unregister_error')
        main.test_number = 'XroadDeleteKeyFromConfiguration.test_b'

        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        auth_deletion = 'test_key_deletion'
        management_wsdl_url = main.config.get('wsdl.management_service_wsdl_url')
        management_client = xroad.split_xroad_id(main.config.get('ss1.management_id'))
        management_client_id = xroad.get_xroad_subsystem(management_client)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            disable_management_wsdl(main, management_client_id, management_wsdl_url)()
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            main.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
            main.wait_jquery()
            delete_key_from_configuration(main, auth_deletion, sshclient, unregister_request_fail=True,
                                          log_checker=log_checker)
        except:
            main.save_exception_data()
            raise
        finally:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            enable_management_wsdl(main, management_client_id, management_wsdl_url)()
            main.tearDown()

    def test_c_delete_key_unregister_sending_error(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_35/42.c'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        main.log('XroadDeleteKeyFromConfiguration.test_c_delete_key_unregister_sending_error')
        main.test_number = 'XroadDeleteKeyFromConfiguration.test_c'

        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        auth_key_name = main.config.get('certs.ss_auth_key_label')

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            main.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
            main.wait_jquery()
            sshclient.exec_command('service xroad-proxy stop', sudo=True)
            delete_key_from_configuration(main, auth_key_name, sshclient, request_sending_fail=True)
            sshclient.exec_command('service xroad-proxy start', sudo=True)
            wait_until_proxy_up('https://{}:5500'.format(ss_ssh_host), main, timeout=1200)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_d_delete_key_from_configuration_with_cert(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_35/42.d'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        main.log('XroadDeleteKeyFromConfiguration.test_d_delete_key_from_configuration_with_cert')
        main.test_number = 'XroadDeleteKeyFromConfiguration.test_d'

        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        auth_deletion = 'test_key_deletion'
        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            main.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
            main.wait_jquery()
            delete_key_from_configuration(main, auth_deletion, sshclient, log_checker=log_checker)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_e_delete_key_from_configuration_without_certs_canceling(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_35/42.e'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        main.log('XroadDeleteKeyFromConfiguration.test_e_delete_key_from_configuration_without_certs_canceling')
        main.test_number = 'XroadDeleteKeyFromConfiguration.test_e'

        auth_deletion = 'test_key_deletion'
        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            main.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
            main.wait_jquery()
            add_key_label(main, auth_deletion)
            timeout = get_keyconf_update_timeout(sshclient)
            main.log('Waiting {} seconds for keyconf update'.format(timeout))
            time.sleep(timeout)
            delete_key_from_configuration(main, auth_deletion, sshclient, log_checker=log_checker, has_auth_certs=False,
                                          try_cancel=True)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_f_delete_key_from_configuration_no_certs(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_35/42.f'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        main.log('XroadDeleteKeyFromConfiguration.test_e_delete_key_from_configuration_without_certs_canceling')
        main.test_number = 'XroadDeleteKeyFromConfiguration.test_f'

        auth_deletion = 'test_key_deletion'
        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            main.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
            main.wait_jquery()
            delete_key_from_configuration(main, auth_deletion, sshclient, log_checker=log_checker, has_auth_certs=False)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
