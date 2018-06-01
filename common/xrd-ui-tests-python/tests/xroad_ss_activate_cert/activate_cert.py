import time

from selenium.webdriver.common.by import By

from helpers import auditchecker, ssh_client, ssh_server_actions
from tests.xroad_ss_client_certification_213.client_certification import get_disabled_certs
from view_models.keys_and_certificates_table import OCSP_DISABLED_CERT_ROW, ACTIVATE_BTN_ID, \
    KEYS_AND_CERTIFICATES_TABLE_ID, CERT_BY_KEY_LABEL, OCSP_RESPONSE_CLASS_NAME
from view_models.log_constants import ENABLE_CERTIFICATE
from view_models.sidebar import KEYSANDCERTIFICATES_BTN_CSS


def activate_cert(self, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass, registered=False):
    """
    SS_32 Activate a Certificate
    :param self: mainController instance
    :param ss2_ssh_host: security server ssh host
    :param ss2_ssh_user: security server ssh user
    :param ss2_ssh_pass: security server ssh pass
    :return:
    """

    def activate():
        self.log('SS_32 Activate a Certificate')
        '''Security server log checker instance'''
        log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        '''Security server SSH client instance'''
        sshclient = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        '''Open keys and certificates view'''
        self.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
        '''Current log lines'''
        current_log_lines = log_checker.get_line_count()
        self.log('Wait until keyconf is updated')
        last_update_ago = int(sshclient.exec_command('echo $(($(date +"%s")-$(sudo date +"%s" -r {})))'.format('/etc/xroad/signer/keyconf.xml'), sudo=True)[0][0])
        wait_seconds = 61 - last_update_ago
        time.sleep(wait_seconds)
        '''Find not active certs in keyconf file'''
        keyconf_before = get_disabled_certs(sshclient)
        disabled_row = self.wait_until_visible(type=By.XPATH, element=OCSP_DISABLED_CERT_ROW)
        '''Get the cert key label'''
        key_label = disabled_row.find_element_by_xpath('../preceding::tr[2]//td').text.split(' ')[1]
        '''Click on the certificate'''
        self.click(disabled_row)
        self.log('SS_32 1. "Activate a certificate" button is clicked')
        self.wait_until_visible(type=By.ID, element=ACTIVATE_BTN_ID).click()
        self.log('Waiting until keyconf is updated')
        last_update_ago = int(sshclient.exec_command('echo $(($(date +"%s")-$(sudo date +"%s" -r {})))'.format('/etc/xroad/signer/keyconf.xml'), sudo=True)[0][0])
        wait_seconds = 61 - last_update_ago
        time.sleep(wait_seconds)
        '''Find not active certs in keyconf file'''
        keyconf_after = get_disabled_certs(sshclient)
        '''Check if keyconf is different than before'''
        self.log('SS_32 2. System activates the certificate')
        self.not_equal(keyconf_before, keyconf_after)

        if not registered:
            self.reset_page()
            self.wait_until_visible(type=By.ID, element=KEYS_AND_CERTIFICATES_TABLE_ID)
            self.wait_jquery()
            '''Activated cert'''
            activated_cert = self.by_xpath(CERT_BY_KEY_LABEL.format(key_label))
            self.log('SS_32 2. System displays the latest OCSP response value')
            self.is_true(
                len(activated_cert.find_element_by_class_name(
                    OCSP_RESPONSE_CLASS_NAME).text) > 0)
        expected_log_msg = ENABLE_CERTIFICATE
        self.log('SS_32 3. System logs the event "{0}" to the audit log'.format(expected_log_msg))
        time.sleep(1.5)
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1,
                                           strict=False)
        self.is_true(logs_found)
        self.log('Hard reresh server OCSP')
        ssh_server_actions.refresh_ocsp(sshclient)

    return activate
