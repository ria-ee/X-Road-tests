import time
import unittest

from selenium.webdriver.common.by import By

from helpers import ssh_client, auditchecker, xroad
from main.maincontroller import MainController
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import approve_requests
from tests.xroad_delete_csr_and_cert.XroadCertAndCSRDeletion import test_delete_csr_key_has_more_items, \
    test_delete_cert_key_has_more_items, test_delete_only_cert_from_only_key, test_delete_only_csr_from_only_key
from tests.xroad_parse_users_inputs.xroad_parse_user_inputs import add_key_label
from tests.xroad_ss_client_certification_213.client_certification import register_cert, activate_cert, \
    test_add_cert_to_ss, \
    test_generate_csr_and_import_cert
from view_models import sidebar
from view_models.keys_and_certificates_table import SIGNING_KEY_LABEL, AUTH_KEY_LABEL


class cert_and_csr_deletion_tests(unittest.TestCase):
    """
    SS_39 1-5, 3a, 4a, 4b Delete Certificate or a Certificate Signing Request Notice from System Configuration
    RIA URL: https://jira.ria.ee/browse/XTKB-100
    RIA URL: https://jira.ria.ee/browse/XTKB-126
    Depends on finishing other test(s):
    Requires helper scenarios: SS_29, SS_30
    X-Road version: 6.16.0
    """

    def test_cert_and_csr_deletion(self):
        main = MainController(self)
        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        cert_path = 'temp.pem'

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')
        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        client_id = main.config.get('ss1.server_id')
        client_name = main.config.get('ss1.server_name')
        client = xroad.split_xroad_subsystem(client_id)
        client_code = client['code']
        client_class = client['class']
        client['name'] = client_name

        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        delete_csr_key_has_more = test_delete_csr_key_has_more_items(main, sshclient, log_checker, client_code,
                                                                     client_class)
        delete_cert_key_has_more = test_delete_cert_key_has_more_items(main, client_code, client_class, ss_ssh_host,
                                                                       ss_ssh_user, ss_ssh_pass)
        delete_only_cert_from_only_key = test_delete_only_cert_from_only_key(main, ss_ssh_host, ss_ssh_user,
                                                                             ss_ssh_pass)
        delete_only_csr_from_only_key = test_delete_only_csr_from_only_key(main, client_code, client_class,
                                                                           ss_ssh_host,
                                                                           ss_ssh_user, ss_ssh_pass)
        test_register_cert = register_cert(main, ss_ssh_host, ss_ssh_user, ss_ssh_pass,
                                           cs_host=cs_ssh_host, client=client,
                                           ca_ssh_host=ca_ssh_host, ca_ssh_user=ca_ssh_user,
                                           ca_ssh_pass=ca_ssh_pass,
                                           cert_path=cert_path)

        test_activate_cert = activate_cert(main, ss_ssh_host, ss_ssh_user, ss_ssh_pass,
                                           registered=True)
        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            delete_csr_key_has_more()
            delete_cert_key_has_more()
            delete_only_cert_from_only_key()
            delete_only_csr_from_only_key()
        finally:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_generate_csr_and_import_cert(client_code, client_class, key_label=SIGNING_KEY_LABEL,
                                              ss2_ssh_host=ss_ssh_host,
                                              ss2_ssh_user=ss_ssh_user, ss2_ssh_pass=ss_ssh_pass, generate_key=False,
                                              cancel_key_generation=False,
                                              cancel_csr_generation=False, generate_same_csr_twice=False)(main)
            main.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
            main.wait_jquery()
            add_key_label(main, AUTH_KEY_LABEL)
            test_register_cert()
            test_activate_cert()
            test_add_cert_to_ss(main, cs_host, cs_user, cs_pass, client, cert_path,
                                cs_ssh_host, cs_ssh_user, cs_ssh_pass)
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            approve_requests(main)
            main.log('Wait until servers have synced')
            time.sleep(120)
            main.tearDown()
