import unittest

from selenium.webdriver.common.by import By

from helpers import xroad, ssh_client
from main.maincontroller import MainController
from tests.xroad_ss_client_certification_213.client_certification import generate_auth_csr
from tests.xroad_ss_import_certificate_from_token.xroad_import_cert_token import import_auth_cert_from_token, \
    reset_hard_token
from view_models.keys_and_certificates_table import KEY_TABLE_ROW_BY_LABEL_XPATH, DELETE_BTN_ID, AUTH_KEY_LABEL
from view_models.popups import confirm_dialog_click
from view_models.sidebar import KEYSANDCERTIFICATES_BTN_CSS


class XroadImportCertFromTokenAuth(unittest.TestCase):
    """
    SS_31 1-14(auth), 7b Import certificate from security token(auth)
    RIA URL: https://jira.ria.ee/browse/XTKB-121
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_aimport_sign_cert_for_auth_key(self):
        main = MainController(self)
        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')
        ca_name = main.config.get('ca.ssh_host')
        ss_id = xroad.split_xroad_subsystem(main.config.get('ss2.server_id'))
        ca_ssh_client = ssh_client.SSHClient(main.config.get('ca.ssh_host'), main.config.get('ca.ssh_user'),
                                      main.config.get('ca.ssh_pass'))
        token_name = main.config.get('utimaco.token_name')

        try:
            main.reload_webdriver(ss2_host, ss2_user, ss2_pass)
            main.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
            main.wait_until_visible(type=By.XPATH, element=KEY_TABLE_ROW_BY_LABEL_XPATH.format(AUTH_KEY_LABEL)).click()
            generate_auth_csr(main, ca_name=ca_name)
            import_auth_cert_from_token(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass, ss_id, ca_ssh_client, cert_type='sign')
        finally:
            reset_hard_token(main, token_name)
            main.tearDown()

    def test_bimport_auth_cert(self):
        main = MainController(self)
        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')
        ca_name = main.config.get('ca.ssh_host')
        ca_ssh_client = ssh_client.SSHClient(main.config.get('ca.ssh_host'), main.config.get('ca.ssh_user'),
                                             main.config.get('ca.ssh_pass'))
        ss_id = xroad.split_xroad_subsystem(main.config.get('ss2.server_id'))
        token_name = main.config.get('utimaco.token_name')

        try:
            main.reload_webdriver(ss2_host, ss2_user, ss2_pass)
            main.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
            main.wait_until_visible(type=By.XPATH, element=KEY_TABLE_ROW_BY_LABEL_XPATH.format(AUTH_KEY_LABEL)).click()
            generate_auth_csr(main, ca_name=ca_name)
            import_auth_cert_from_token(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass, ca_ssh_client=ca_ssh_client, ss_id=ss_id)
        finally:
            main.wait_until_visible(type=By.ID, element=DELETE_BTN_ID).click()
            confirm_dialog_click(main)
            reset_hard_token(main, token_name)
            main.tearDown()

