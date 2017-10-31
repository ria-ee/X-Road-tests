from selenium.webdriver.common.by import By

from helpers import ssh_server_actions, ssh_client
from tests.xroad_ss_client_certification_213.client_certification_2_1_3 import generate_csr, delete_csr, \
    test_generate_csr_and_import_cert, delete_cert_from_key, delete_all_but_one_sign_keys, delete_all_auth_keys
from view_models import keys_and_certificates_table, sidebar


def test_delete_csr_key_has_more_items(self, sshclient, log_checker, client_code, client_class):
    """
    SS_39 4. Delete CSR from System Configuration deletes only csr when key has other items
    :param self: obj - mainController instance
    :param sshclient: obj- sshclient instance
    :param log_checker: obj - logchecker instance
    :param client_code: str - client code
    :param client_class: str - client class
    :return:
    """

    def delete_csr_key_has_more_items():
        self.log('Generate CSR which will be deleted')
        generate_csr(self, client_code=client_code,
                     client_class=client_class, server_name=ssh_server_actions.get_server_name(self),
                     key_label=keys_and_certificates_table.SIGNING_KEY_LABEL, generate_key=False)
        delete_csr(self, sshclient, log_checker, key_has_other_cert_or_csr=True)

    return delete_csr_key_has_more_items


def test_delete_only_cert_from_only_key(self, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass):
    """
    SS_39 4b. Delete Cert also deletes key and token from configuration when cert is keys only item and token has no other keys
    :param self: mainController instance
    :param ss2_ssh_host:  security server ssh host
    :param ss2_ssh_user:  security server ssh user
    :param ss2_ssh_pass:  security server ssh pass
    :return:
    """

    def delete_cert_key_has_more_items():
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.KEYS_AND_CERTIFICATES_TABLE_ID)
        self.log('Delete all auth keys present')
        delete_all_auth_keys(self)()
        self.log('Delete all sign keys, but one')
        delete_all_but_one_sign_keys(self)()
        self.log('SS_39 4b Delete only certificate from only key in token')
        delete_cert_from_key(self, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass, one_cert=True)()

    return delete_cert_key_has_more_items


def test_delete_cert_key_has_more_items(self, client_code, client_class, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass):
    """
    SS_39 4. Delete Cert deletes only cert when key has other items
    :param self: obj - mainController instance
    :param client_code: client code
    :param client_class:  client class
    :param ss2_ssh_host:  security server ssh host
    :param ss2_ssh_user:  security server ssh user
    :param ss2_ssh_pass:  security server ssh pass
    :return:
    """

    def delete_cert_key_has_more_items():
        test_generate_csr_and_import_cert(client_code=client_code, client_class=client_class, ss2_ssh_host=ss2_ssh_host,
                                          ss2_ssh_user=ss2_ssh_user,
                                          ss2_ssh_pass=ss2_ssh_pass,
                                          key_label=keys_and_certificates_table.SIGNING_KEY_LABEL, generate_key=False,
                                          cancel_key_generation=False,
                                          cancel_csr_generation=False, generate_same_csr_twice=False)(self)
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.KEY_TABLE_CERT_ROW_BY_LABEL_XPATH.format(
                                    'sign')).click()
        delete_cert_from_key(self, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)()

    return delete_cert_key_has_more_items


def test_delete_only_csr_from_only_key(self, client_code, client_class, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass):
    """
    SS_39 4b. Delete CSR also deletes key and token from configuration when CSR is keys only item and token has no other keys
    :param self: obj - mainController instance
    :param client_code:  str - client code
    :param client_class: str - client class
    :param ss2_ssh_host:  str - security server ssh host
    :param ss2_ssh_user:  str - security server ssh user
    :param ss2_ssh_pass:  str - security server ssh pass
    :return:
    """

    def delete_csr_only_key():
        generate_csr(self, client_code=client_code,
                     client_class=client_class, server_name=ssh_server_actions.get_server_name(self),
                     key_label=keys_and_certificates_table.SIGNING_KEY_LABEL, generate_key=False)
        sshclient = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        delete_csr(self, sshclient, only_item_and_key=True)

    return delete_csr_only_key
