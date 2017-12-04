import time
import unittest

from selenium.webdriver.common.by import By

from helpers import ssh_client
from main.maincontroller import MainController
from tests.xroad_cs_ca import ca_management
from tests.xroad_cs_ca.ca_management import test_add_ca
from tests.xroad_cs_ocsp_responder import ocsp_responder
from tests.xroad_cs_ocsp_responder.ocsp_responder import test_add_ocsp_responder
from tests.xroad_ss_client.ss_client_management import add_ss_client, delete_client, edit_client
from tests.xroad_ss_client_certification_213.client_certification import start_xroad_conf_client, \
    expire_global_conf
from tests.xroad_ss_import_certificate_from_token import xroad_import_cert_token
from tests.xroad_ss_import_certificate_from_token.xroad_import_cert_token import test_import_cert_from_token
from view_models.clients_table_vm import get_client_row_element
from view_models.popups import WARNING_POPUP_CONTINUE_XPATH, CONFIRM_POPUP_CANCEL_BTN_XPATH, \
    YESNO_POPUP_NO_BTN_XPATH, close_all_open_dialogs


class XroadImportCertFromTokenSigning(unittest.TestCase):
    """
    SS_31 1-16, 2a, 4a, 5a, 6a, 7a, 7c, 8a, 9a, 10a, 13a Import certificate from security token(sign)
    RIA URL: https://jira.ria.ee/browse/XTKB-121
    Depends on finishing other test(s):
    Requires helper scenarios: MEMBER_47, TRUST_08, TRUST_10, TRUST_14
    X-Road version: 6.16.0
    """
    def test_aimport_cert_from_token(self):
        main = MainController(self)

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')
        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')
        token_name = main.config.get('utimaco.token_name')
        import_cert_from_token = test_import_cert_from_token(main, ss_ssh_host, ss_ssh_user, ss_ssh_pass, token_name,
                                                             ss_host=ss_host, ss_user=ss_user, ss_pass=ss_pass,
                                                             already_exists_error=True, expired_cert_error=True,
                                                             auth_cert_sign_key_error=True)
        generate_certs_to_hsm = xroad_import_cert_token.generate_certs_to_hsm(main, ca_ssh_host, ca_ssh_user,
                                                                              ca_ssh_pass, ss_ssh_host, ss_ssh_user,
                                                                              ss_ssh_pass, token_name)
        member_code = subsystem_code = 'test'
        member_class = 'COM'

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            main.log('Adding test client to ss')
            add_ss_client(main, member_code, member_class, subsystem_code)
            main.wait_until_visible(type=By.XPATH, element=WARNING_POPUP_CONTINUE_XPATH).click()
            main.wait_until_visible(type=By.XPATH, element=CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            working_cert_id, auth_cert_id, expired_cert_id, existing_cert_id = generate_certs_to_hsm()
            main.log('Waiting until signer update')
            time.sleep(60)
            main.reset_page()
            import_cert_from_token(working_cert_id, auth_cert_id, expired_cert_id, existing_cert_id)
        finally:
            main.tearDown()

    def test_bimport_cert_from_token_global_conf_error(self):
        main = MainController(self)
        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')
        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        expire_globalconf = expire_global_conf(main, sshclient)
        import_cert_from_token_global_conf_error = test_import_cert_from_token(main, ss_ssh_host, ss_ssh_user,
                                                                               ss_ssh_pass, global_conf_error=True)
        start_conf_client = start_xroad_conf_client(main, sshclient)
        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            expire_globalconf()
            import_cert_from_token_global_conf_error()
        finally:
            start_conf_client()
            main.log('Waiting until global configuration is up to date')
            time.sleep(60)
            main.tearDown()

    def test_cimport_cert_from_token_no_ca(self):
        main = MainController(self)
        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')
        import_cert_from_token_no_ca_error = test_import_cert_from_token(main, ss_ssh_host, ss_ssh_user,
                                                                         ss_ssh_pass, no_ca_error=True)
        ca_certificate_filename = 'ca.cert.pem'
        certificate_classpath = main.config.get('ca.profile_class')

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        ocsp_responder.ca_get_certificates(main, ca_ssh_host, ca_ssh_user, ca_ssh_pass, [ca_certificate_filename])

        ca_certificate = main.get_download_path(ca_certificate_filename)
        invalid_ca_certificate = main.get_download_path('INFO')
        restore_ca = test_add_ca(case=main, ca_certificate=ca_certificate,
                                 invalid_ca_certificate=invalid_ca_certificate,
                                 certificate_classpath=certificate_classpath)

        ca_name = main.config.get('ca.host')

        ocsp_url = main.config.get('ca.ocs_host')
        ocsp_cert_filename = 'ocsp.cert.pem'

        main.log('Getting CA certificates from {0}'.format(ca_ssh_host))
        ocsp_responder.ca_get_certificates(main, ca_ssh_host, ca_ssh_user, ca_ssh_pass, filenames=[ocsp_cert_filename])

        certificate_filename = main.get_download_path(ocsp_cert_filename)
        restore_ocsp = test_add_ocsp_responder(case=main, ca_name=ca_name, ocsp_url=ocsp_url,
                                               certificate_filename=certificate_filename)

        delete_ca = ca_management.test_delete_ca(case=main, ca_name=ca_name)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            delete_ca()
            main.log('Wait 120 seconds for changes')
            time.sleep(120)
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            import_cert_from_token_no_ca_error()
        finally:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            restore_ca()
            close_all_open_dialogs(main)
            restore_ocsp()
            time.sleep(120)
            main.tearDown()

    def test_dimport_cert_from_token_no_client(self):
        main = MainController(self)

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')
        import_cert_from_token_no_key_error = test_import_cert_from_token(main, ss_ssh_host, ss_ssh_user,
                                                                          ss_ssh_pass, no_client_error=True)
        test_client_id = main.config.get('ss2.test_client_id')

        try:
            main.log('Deleting test client')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            client_row = get_client_row_element(main, client_id=test_client_id)
            edit_client(main, client_row)
            delete_client(main, False)
            main.wait_until_visible(type=By.XPATH, element=YESNO_POPUP_NO_BTN_XPATH).click()
            main.wait_jquery()
            import_cert_from_token_no_key_error()
        finally:
            main.tearDown()

    def test_eimport_cert_from_token_no_key(self):
        main = MainController(self)

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')
        token_name = main.config.get('utimaco.token_name')
        import_cert_from_token_no_key_error = test_import_cert_from_token(main, ss_ssh_host, ss_ssh_user,
                                                                          ss_ssh_pass, ss_host=ss_host, ss_user=ss_user,
                                                                          ss_pass=ss_pass, no_key_error=True, token_name=token_name)
        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            import_cert_from_token_no_key_error()
        finally:
            main.tearDown()
