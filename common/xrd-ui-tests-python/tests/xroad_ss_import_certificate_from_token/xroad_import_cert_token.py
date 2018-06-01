import glob
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_client, auditchecker
from helpers.ssh_server_actions import get_server_name
from tests.xroad_ss_client_certification_213.client_certification import get_cert, put_file_in_ss
from view_models.keys_and_certificates_table import HARDTOKEN_BY_LABEL_XPATH, GENERATEKEY_BTN_ID, GENERATECSR_BTN_ID, \
    GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID, GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH, \
    SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH, GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID, DELETE_BTN_ID, \
    GENERATE_CSR_SIGNING_REQUEST_CLIENT_DROPDOWN_ID, CERT_INACTIVE_ROW_BY_DATA_ID, \
    HARDTOKEN_NEXT_NOT_EMPTY_TR, CERT_BY_KEY_AND_FRIENDLY_NAME, OCSP_CERT_FRIENDLY_NAME, HARDTOKEN_CERT_IMPORT_BTN, \
    HARDTOKEN_KEY, CERT_INACTIVE_ROW_BY_DATA_ID_IMPORT_BTN, KEY_CSR_BY_KEY_LABEL_XPATH, KEY_USAGE_CLASS
from view_models.log_constants import IMPORT_CERTIFICATE_FROM_TOKEN, IMPORT_CERTIFICATE_FROM_TOKEN_FAILED
from view_models.messages import ERROR_MESSAGE_CSS, CERTIFICATE_ALREADY_EXISTS, \
    CERTIFICATE_IMPORT_EXPIRED_GLOBAL_CONF_ERROR, CERTIFICATE_NOT_SIGNING_KEY, CA_NOT_VALID_AS_SERVICE, \
    IMPORT_CERT_KEY_NOT_FOUND_ERROR, NO_CLIENT_FOR_CERTIFICATE, CERTIFICATE_NOT_VALID, SIGN_CERT_INSTEAD_AUTH_CERT
from view_models.popups import GENERATE_KEY_POPUP_OK_BTN_XPATH, confirm_dialog_click
from view_models.sidebar import KEYSANDCERTIFICATES_BTN_CSS


def generate_certs_to_hsm(self, ca_ssh_host, ca_ssh_user, ca_ssh_pass, ss_ssh_host, ss_ssh_user, ss_ssh_pass,
                          token_name):
    def generate_certs():
        self.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
        self.log('Click on {0} token'.format(token_name))
        self.wait_until_visible(type=By.XPATH, element=HARDTOKEN_BY_LABEL_XPATH.format(
            token_name)).click()
        self.log('Generate key on token')
        self.wait_until_visible(type=By.ID, element=GENERATEKEY_BTN_ID).click()
        self.log('Confirm key generation')
        self.wait_until_visible(type=By.XPATH, element=GENERATE_KEY_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
        self.log('Generate CSR on key')
        self.wait_until_visible(type=By.ID, element=GENERATECSR_BTN_ID).click()

        client_select = Select(self.wait_until_visible(type=By.ID,
                                                       element=GENERATE_CSR_SIGNING_REQUEST_CLIENT_DROPDOWN_ID))
        filter(lambda x: 'test' in x.text, client_select.options)[0].click()
        self.wait_jquery()
        ca_select = Select(
            self.wait_until_visible(type=By.ID, element=GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID))
        self.wait_jquery()
        ca_select.select_by_value(ca_ssh_host)
        format_select = Select(
            self.wait_until_visible(type=By.ID, element=GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID))
        format_select.select_by_value('DER')
        self.by_xpath(GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH).click()
        self.wait_until_visible(type=By.XPATH, element=SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=DELETE_BTN_ID).click()
        confirm_dialog_click(self)

        server_name = get_server_name(self)
        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'
        time.sleep(3)
        file_path = glob.glob(self.get_download_path('_'.join(['*', server_name, 'COM', 'test']) + '.der'))[
            0]

        client = ssh_client.SSHClient(ca_ssh_host, ca_ssh_user, ca_ssh_pass)

        local_cert_path = self.get_download_path(cert_path)
        local_auth_cert_path = self.get_download_path('auth_{0}'.format(cert_path))
        local_expired_cert_path = self.get_download_path('expired_{0}'.format(cert_path))

        self.log('Get certs from CA')
        get_cert(client, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path, convert_der=True,
                 close_client=False)
        get_cert(client, 'sign-auth', file_path, local_auth_cert_path, cert_path, remote_csr_path, convert_der=True,
                 close_client=False)
        get_expired_cert(client, 'sign-sign', file_path, local_expired_cert_path, cert_path, remote_csr_path,
                         convert_der=True)
        ss_ssh_client = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        ss_cert_path = '/tmp/cert.der'
        ss_auth_cert_path = '/tmp/auth_cert.der'
        ss_expired_cert_path = '/tmp/expired_cert.der'

        self.log('Put certs in ss')
        put_file_in_ss(ss_ssh_client, local_cert_path, ss_cert_path)
        put_file_in_ss(ss_ssh_client, local_auth_cert_path, ss_auth_cert_path)
        put_file_in_ss(ss_ssh_client, local_expired_cert_path, ss_expired_cert_path)

        self.log('Import certs to HSM')
        existing_cert_id = import_cert_with_p11tool(ss_ssh_client, ss_cert_path, key_id='999')
        working_cert_id = import_cert_with_p11tool(ss_ssh_client, ss_cert_path, key_id='123')
        auth_cert_id = import_cert_with_p11tool(ss_ssh_client, ss_auth_cert_path, key_id='456')
        expired_cert_id = import_cert_with_p11tool(ss_ssh_client, ss_expired_cert_path, key_id='789')
        return working_cert_id, auth_cert_id, expired_cert_id, existing_cert_id

    return generate_certs


def import_cert_with_p11tool(client, cert_path, key_id):
    client.exec_command('p11tool2 slot=0 LoginUser=1234 CertAttr=CKA_ID={0} PubKeyAttr=CKA_ID={0} '
                        'ImportCert={1}'.format(key_id, cert_path))
    return '3{0}3{1}3{2}'.format(key_id[0], key_id[1], key_id[2])


def test_import_cert_from_token(self, ss_ssh_host, ss_ssh_user, ss_ssh_pass, token_name=None,
                                ss_host=None, ss_user=None, ss_pass=None, auth_cert_sign_key_error=False,
                                global_conf_error=False, already_exists_error=False, no_ca_error=False,
                                no_key_error=False, no_client_error=False, expired_cert_error=False):
    def test_import_from_token(working_cert_id=None, auth_cert_id=None, expired_cert_id=None, existing_cert_id=None):
        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        self.log('Open keys and certificates tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
        current_log_lines = log_checker.get_line_count()
        if no_client_error:
            self.log('SS_31 4a. Importing certificate for not existing client')
            self.wait_until_visible(type=By.XPATH, element=HARDTOKEN_CERT_IMPORT_BTN).click()
            expected_error_msg = NO_CLIENT_FOR_CERTIFICATE
            self.log('SS_31 4a.1 System displays the error message "{0}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_true(error_msg.startswith(expected_error_msg))
            expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN_FAILED
            self.log('SS_31 4a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            return
        if no_ca_error:
            self.log('SS_31 8a. Importing a certificate from not approved CA')
            self.wait_until_visible(type=By.XPATH, element=HARDTOKEN_CERT_IMPORT_BTN).click()
            expected_error_msg = CA_NOT_VALID_AS_SERVICE
            self.log('SS_31 8a.1 System displays the error message "{0}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN_FAILED
            self.log('SS_31 8a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            return
        if global_conf_error:
            self.log('SS_31 2a. Importing a certificate, global configuration expired')
            self.wait_until_visible(type=By.XPATH, element=HARDTOKEN_CERT_IMPORT_BTN).click()
            expected_error_msg = CERTIFICATE_IMPORT_EXPIRED_GLOBAL_CONF_ERROR
            self.log('SS_31 2a.1 System displays the error message "{0}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN_FAILED
            self.log('SS_31 2a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(IMPORT_CERTIFICATE_FROM_TOKEN_FAILED, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            return
        if no_key_error:
            old_driver = self.driver
            self.log('Deleting key in another session')
            delete_key_in_another_window(self, ss_host, ss_user, ss_pass, token_name)
            self.driver = old_driver
            self.log('SS_31 5a. Importing certificate to not existing key')
            self.wait_until_visible(type=By.XPATH, element=HARDTOKEN_CERT_IMPORT_BTN).click()
            expected_error_msg =  IMPORT_CERT_KEY_NOT_FOUND_ERROR
            self.log('SS_31 5a.1 System displays the error message "{0}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN_FAILED
            self.log('SS_31 5a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            return
        self.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
        registered_cert_count = get_registered_certs_count(self)
        key_usage_sign_count = get_sign_keys_count(self)
        self.log('SS_31 1. Importing signing certificate from token')
        self.wait_until_visible(type=By.XPATH,
                                element=CERT_INACTIVE_ROW_BY_DATA_ID_IMPORT_BTN.format(existing_cert_id)).click()
        self.wait_jquery()
        registered_cert_count_after = get_registered_certs_count(self)
        self.log('SS_31 11. System sets the registration state to "registered"')
        self.is_true(registered_cert_count_after > registered_cert_count)
        self.log('SS_31 10a. The usage of the key is undefined')
        self.log('SS_31 10a.1 System assings the usage of the key according to the usage of the imported cert(sign)')
        self.log('SS_31 13a No CSR notice corresponding to imported certificae exist')
        key_usage_sign_count_after = get_sign_keys_count(self)
        self.is_true(key_usage_sign_count < key_usage_sign_count_after)
        expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN
        self.log('Waiting for log event')
        time.sleep(60)
        self.log('SS_31 14. System logs the event "{0}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

        if auth_cert_sign_key_error:
            current_log_lines = log_checker.get_line_count()
            self.log('SS_31 7a. Importing authentication certificate for signing key')
            self.wait_until_visible(type=By.XPATH,
                                    element=CERT_INACTIVE_ROW_BY_DATA_ID_IMPORT_BTN.format(auth_cert_id)).click()
            expected_error_msg = CERTIFICATE_NOT_SIGNING_KEY
            self.log('SS_31 7a.1 System displays the error message {0}'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN_FAILED
            self.log('SS_31 7a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
        if already_exists_error:
            current_log_lines = log_checker.get_line_count()
            self.driver.refresh()
            self.log('SS_31 6a. Importing already existing certificate')
            self.wait_until_visible(type=By.XPATH,
                                    element=CERT_INACTIVE_ROW_BY_DATA_ID_IMPORT_BTN.format(working_cert_id)).click()
            expected_error_msg = CERTIFICATE_ALREADY_EXISTS
            self.log('SS_31 6a.1 System displays the error message "{0}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_true(error_msg.startswith(expected_error_msg))
            expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN_FAILED
            self.log('SS_31 6a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
        if expired_cert_error:
            current_log_lines = log_checker.get_line_count()
            self.log('SS_31 9a. Importing expired certificate')
            self.wait_until_visible(type=By.XPATH,
                                    element=CERT_INACTIVE_ROW_BY_DATA_ID_IMPORT_BTN.format(expired_cert_id)).click()
            expected_error_msg = CERTIFICATE_NOT_VALID
            self.log('SS_31 9a.1 System displays the error message "{0}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN_FAILED
            self.log('SS_31 9a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(IMPORT_CERTIFICATE_FROM_TOKEN_FAILED, from_line=current_log_lines + 1)
            self.is_true(logs_found)

    return test_import_from_token


def delete_key_in_another_window(self, ss_host, ss_user, ss_pass, token_name):
    self.reset_webdriver(url=ss_host, username=ss_user, password=ss_pass, close_previous=False)
    self.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_until_visible(type=By.XPATH,
                            element=HARDTOKEN_KEY.format(token_name)).click()

    self.wait_until_visible(type=By.ID, element=DELETE_BTN_ID).click()
    confirm_dialog_click(self)
    self.wait_until_visible(type=By.CSS_SELECTOR, element='.key.unsaved').click()
    self.wait_until_visible(type=By.ID, element=DELETE_BTN_ID).click()
    confirm_dialog_click(self)
    self.tearDown()


def get_expired_cert(sshclient, service, file_path, local_cert_path, remote_cert_path, remote_csr_path,
                     convert_der=False):
    flag_to_replace = '-days 7300'
    replacement = '-startdate 120815080000Z -enddate 120815090000Z'
    sshclient.exec_command(
        command='sed -i -e "s/{0}/{1}/g" /home/ca/CA/sign.sh'.format(flag_to_replace, replacement), sudo=True)

    get_cert(sshclient, service, file_path, local_cert_path, remote_cert_path, remote_csr_path, convert_der=convert_der,
             close_client=False)

    sshclient.exec_command(
        command='sed -i -e "s/{0}/{1}/g" /home/ca/CA/sign.sh'.format(replacement, flag_to_replace), sudo=True)


def import_auth_cert_from_token(self, ss_ssh_host, ss_ssh_user, ss_ssh_pass, ss_id, ca_ssh_client, cert_type='auth'):
    remote_csr_path = 'temp.der'
    cert_path = 'temp.pem'
    time.sleep(3)
    file_path = glob.glob(
        self.get_download_path(
            '_'.join(['*', ss_id['instance'], ss_id['class'], ss_id['code'], ss_id['subsystem']]) + '.der')
    )[0]

    log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
    current_log_lines = log_checker.get_line_count()
    local_cert_path = self.get_download_path(cert_path)

    self.log('Getting {0} cert from CA'.format(cert_type))
    get_cert(ca_ssh_client, 'sign-{0}'.format(cert_type), file_path, local_cert_path, cert_path, remote_csr_path,
             convert_der=True,
             close_client=False)
    ss_ssh_client = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
    ss_cert_path = '/tmp/cert.der'
    self.log('Upload cert to security server')
    put_file_in_ss(ss_ssh_client, local_cert_path, ss_cert_path)
    self.log('Import cert to hardware token')
    uploaded_key_id = import_cert_with_p11tool(ss_ssh_client, ss_cert_path, key_id='479')
    self.log('Waiting until signer update')
    time.sleep(60)
    self.log('Refreshing page')
    self.reset_page()
    self.log('Find cert by key id {0}'.format(uploaded_key_id))
    new_cert_row = self.wait_until_visible(type=By.XPATH, element=CERT_INACTIVE_ROW_BY_DATA_ID.format(uploaded_key_id))
    self.log('Find cert id')
    cert_name = new_cert_row.find_element_by_class_name(OCSP_CERT_FRIENDLY_NAME).text
    self.log('SS_31 1. Importing a certificate from a security token')
    csr_count_before_import = len(self.wait_until_visible(type=By.CLASS_NAME, element='cert-request', multiple=True))
    new_cert_row.find_element_by_tag_name('button').click()
    self.wait_jquery()

    if cert_type == 'sign':
        expected_error_msg = SIGN_CERT_INSTEAD_AUTH_CERT
        self.log('SS_31 7b.1 System displays the error message "{0}"'.format(expected_error_msg))
        error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
        self.is_equal(expected_error_msg, error_msg)
        expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN_FAILED
        self.log('SS_31 7b.2 System logs the event "{0}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)
        return

    self.log('SS_31 15. Imported certificate CSR is deleted from system')
    try:
        csr_count_after_import = len(self.wait_until_visible(type=By.CLASS_NAME, element='cert-request', multiple=True))
        self.is_true(csr_count_before_import > csr_count_after_import)
    except:
        pass

    self.log('Find the imported cert row')
    imported_cert_row = self.wait_until_visible(type=By.XPATH,
                                                element=CERT_BY_KEY_AND_FRIENDLY_NAME.format('authkey', cert_name))
    expected_cert_state = 'disabled'
    self.log('SS_31 11a.1 System sets the certificate state to "{0}"'.format(expected_cert_state))
    imported_cert_row_ocsp = imported_cert_row.find_elements_by_tag_name('td')[2].text
    self.is_equal(expected_cert_state, imported_cert_row_ocsp)
    expected_reg_state = 'saved'
    self.log('SS_31 11a.1 System sets the certificate registration state to "{0}"'.format(expected_reg_state))
    imported_cert_row_status = imported_cert_row.find_elements_by_tag_name('td')[4].text
    self.is_equal(expected_reg_state, imported_cert_row_status)
    time.sleep(60)
    expected_log_msg = IMPORT_CERTIFICATE_FROM_TOKEN
    self.log('SS_31 13a. No CSR notice corresponding to the imported certificate exist int he system configuration')
    self.log('SS_31 14. System logs the event {0}'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)
    self.click(imported_cert_row)


def reset_hard_token(self, token_name):
    try:
        next_row = self.wait_until_visible(type=By.XPATH,
                                           element=HARDTOKEN_NEXT_NOT_EMPTY_TR.format(token_name))

        while 'Token' not in next_row.text:
            self.click(next_row)
            self.wait_until_visible(type=By.ID, element=DELETE_BTN_ID).click()
            confirm_dialog_click(self)
            next_row = self.wait_until_visible(type=By.XPATH,
                                               element=HARDTOKEN_NEXT_NOT_EMPTY_TR.format(token_name))
    except:
        pass


def get_sign_keys_count(self):
    keys = self.wait_until_visible(type=By.CLASS_NAME, element=KEY_USAGE_CLASS, multiple=True)
    sign_keys = filter(lambda x: x.text == 'sign', keys)
    return len(sign_keys)


def get_registered_certs_count(self):
    certs = self.by_css('.cert-active', multiple=True)
    registered_certs = 0
    for cert in certs:
        tds = cert.find_elements_by_tag_name('td')
        if tds[4].text == 'registered':
            registered_certs += 1
    return registered_certs
