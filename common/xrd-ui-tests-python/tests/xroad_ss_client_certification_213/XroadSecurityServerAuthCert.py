import time
import unittest

from helpers import xroad, ssh_client
from main.maincontroller import MainController
from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss_2_2_1
from tests.xroad_configure_service_222.wsdl_validator_errors import wait_until_server_up
from tests.xroad_ss_client_certification_213 import client_certification_2_1_3
from tests.xroad_ss_client_certification_213.client_certification_2_1_3 import test_add_cert_to_ss, register_cert, \
    delete_cert_from_key, activate_cert, unregister_cert
from view_models import popups


class XroadDisablingCert(unittest.TestCase):
    """
    SS_33 Disable a certificate
    RIA URL: https://jira.ria.ee/browse/XTKB-109
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_xroad_disable_auth_cert(self):
        main = MainController(self)

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        ss2_host = main.config.get('ss2.host')
        ss2_username = main.config.get('ss2.user')
        ss2_password = main.config.get('ss2.pass')

        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        test_activate_cert = client_certification_2_1_3.activate_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                                                                      registered=True)
        test_disable_cert = client_certification_2_1_3.disable_cert(main, ss2_host, ss2_username, ss2_password,
                                                                    ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        try:
            main.reload_webdriver(ss2_host, ss2_username, ss2_password)
            test_disable_cert()
        except Exception as error:
            main.log(error)
            assert False
        finally:
            test_activate_cert()
            main.log('Wait until server up again')
            wait_until_server_up(ss2_host)
            main.tearDown()


class XroadUnregisterAuthCert(unittest.TestCase):
    """
    SS_38 Unregister an Authentication Certificate
    MEMBER_23 3a-5a Create an Authentication Certificate Registration Request
    RIA URL: https://jira.ria.ee/browse/XTKB-116
    RIA URL: https://jira.ria.ee/browse/XTKB-129
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_xroad_unregister_auth_cert(self):
        main = MainController(self)

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        ss2_host = main.config.get('ss2.host')
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

        test_unregister_cert = unregister_cert(main, ss2_host, ss2_username, ss2_password,
                                               ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        test_activate_cert = activate_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                                           registered=True)
        delete_unregistered_cert = delete_cert_from_key(main, auth=True,
                                                        ssh_host=ss2_ssh_host,
                                                        ssh_user=ss2_ssh_user,
                                                        ssh_pass=ss2_ssh_pass,
                                                        cancel_deleting=True,
                                                        only_cert=True)
        test_register_cert = register_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                                           cs_host=cs_ssh_host, client=client, cert_path=cert_path,
                                           check_inputs=False, ca_ssh_host=ca_ssh_host,
                                           ca_ssh_user=ca_ssh_user, ca_ssh_pass=ca_ssh_pass)
        try:
            main.reload_webdriver(ss2_host, ss2_username, ss2_password)
            test_unregister_cert()
        finally:
            delete_unregistered_cert()
            test_register_cert()
            test_activate_cert()
            test_add_cert_to_ss(main, cs_host, cs_username, cs_password, client, cert_path,
                                cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                                cancel_cert_registration=True, file_format_errors=True)
            test_add_cert_to_ss(main, cs_host, cs_username, cs_password, client, cert_path,
                                cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                                add_existing_error=True)
            client_registration_in_ss_2_2_1.approve_requests(main)
            main.log('Wait until servers synced')
            time.sleep(120)
            main.tearDown()


class XroadUnregisterAuthCertFailsWhenRequestCantBeSent(unittest.TestCase):
    """
    SS_38 6.a Unregister a certificate when request cant be sent
    MEMBER_23 1-8 Create an Authentication Certificate Registration Request
    MEMBER_24 Create an Authentication Certificate Deletion Request
    RIA URL: https://jira.ria.ee/browse/XTKB-119
    RIA URL: https://jira.ria.ee/browse/XTKB-118
    RIA URL: https://jira.ria.ee/browse/XTKB-116
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_xroad_unregister_auth_cert(self):
        main = MainController(self)

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        ss2_host = main.config.get('ss2.host')
        ss2_username = main.config.get('ss2.user')
        ss2_password = main.config.get('ss2.pass')

        cs_host = main.config.get('cs.host')
        cs_username = main.config.get('cs.user')
        cs_password = main.config.get('cs.pass')

        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        client_id = main.config.get('ss2.client2_id')
        client_name = main.config.get('ss2.client2_name')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        cert_path = 'temp.pem'

        test_unregister_cert = client_certification_2_1_3.unregister_cert(main, ss2_host, ss2_username, ss2_password,
                                                                          ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                                                                          request_fail=True)
        test_activate_cert = client_certification_2_1_3.activate_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                                                                      registered=True)
        delete_unregistered_cert = client_certification_2_1_3.delete_cert(main)
        delete_cert_from_ss = client_certification_2_1_3.delete_cert_from_ss(main, client, cs_ssh_host, cs_ssh_user,
                                                                             cs_ssh_pass)
        ss_host = main.config.get('ss1.ssh_host')
        hosts_replacement = 'asd'
        sshclient = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        try:
            main.log('Replace {0} with {1} in hosts file'.format(ss_host, hosts_replacement))
            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(ss_host, hosts_replacement, '/etc/hosts'),
                sudo=True)
            main.reload_webdriver(ss2_host, ss2_username, ss2_password)
            test_unregister_cert()
        finally:
            main.log('Replace {0} with {1} in hosts file'.format(hosts_replacement, ss_host))
            sshclient.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(hosts_replacement, ss_host, '/etc/hosts'),
                sudo=True)
            delete_unregistered_cert()
            main.reload_webdriver(cs_host, cs_username, cs_password)
            delete_cert_from_ss()
            main.reload_webdriver(ss2_host, ss2_username, ss2_password)
            client_certification_2_1_3.register_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                                                     cs_host=cs_ssh_host, client=client, cert_path=cert_path,
                                                     check_inputs=False, ca_ssh_host=ca_ssh_host,
                                                     ca_ssh_user=ca_ssh_user, ca_ssh_pass=ca_ssh_pass)()
            test_activate_cert()
            client_certification_2_1_3.test_add_cert_to_ss(main, cs_host, cs_username, cs_password, client, cert_path,
                                                           cs_ssh_host, cs_ssh_user, cs_ssh_pass)
            client_registration_in_ss_2_2_1.approve_requests(main)
            main.log('Waiting until cert is registered')
            time.sleep(120)
            main.tearDown()


class XroadUnregisterAuthCertFailsWhenNoValidAuthCert(unittest.TestCase):
    """SS_38 4.a Unregister a certificate when no valid auth cert present"""

    def test_xroad_unregister_auth_cert(self):
        main = MainController(self)

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        ss2_host = main.config.get('ss2.host')
        ss2_username = main.config.get('ss2.user')
        ss2_password = main.config.get('ss2.pass')

        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        client_id = main.config.get('ss2.client2_id')
        client_name = main.config.get('ss2.client2_name')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name

        test_unregister_cert = client_certification_2_1_3.unregister_cert(main, ss2_host, ss2_username, ss2_password,
                                                                          ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                                                                          no_valid_cert=True)
        log_out_token = client_certification_2_1_3.log_out_token(main)
        log_in_token = client_certification_2_1_3.log_in_token(main)
        try:
            main.reload_webdriver(ss2_host, ss2_username, ss2_password)
            log_out_token()
            test_unregister_cert()
        except Exception as error:
            main.log(error)
            assert False
        finally:
            popups.close_all_open_dialogs(main)
            log_in_token()
            main.tearDown()
