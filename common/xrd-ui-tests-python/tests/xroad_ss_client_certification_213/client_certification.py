import datetime
import glob
import os
import time
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import tests.xroad_parse_users_inputs.xroad_parse_user_inputs as user_input_check
from helpers import ssh_client, ssh_server_actions, xroad, login, auditchecker
from helpers.ssh_server_actions import get_key_conf_keys_count, get_key_conf_token_count, get_key_conf_csr_count
from tests.xroad_configure_service_222.wsdl_validator_errors import wait_until_server_up
from tests.xroad_global_groups_tests import global_groups_tests
from view_models import sidebar as sidebar_constants, keys_and_certificates_table as keyscertificates_constants, \
    popups as popups, certification_services, clients_table_vm, messages, keys_and_certificates_table, \
    ss_system_parameters, log_constants, cs_security_servers
from view_models.log_constants import ADD_AUTH_CERTIFICATE_FOR_SECURITY_SERVER_FAILED, GENERATE_KEY_FAILED, \
    GENERATE_CSR_FAILED, GENERATE_KEY, GENERATE_CSR, DELETE_KEY, DELETE_CSR, IMPORT_CERTIFICATE_FROM_FILE, \
    IMPORT_CERTIFICATE_FROM_FILE_FAILED, ENABLE_CERTIFICATE
from view_models.members_table import SS_DETAILS_AUTH_CERT_TAB_XPATH, MEMBER_FIRST_OWNED_SERVER_DETAILS_CSS, \
    SS_DETAILS_ADD_AUTH_CERT_BTN_ID, ADD_AUTH_CERT_UPLOAD_BTN_ID, ADD_AUTH_CERT_SUBMIT_BTN_ID, \
    ADD_AUTH_CERT_CANCEL_BTN_XPATH
from view_models.messages import ERROR_MESSAGE_CSS, AUTH_CERT_IMPORT_FILE_FORMAT_ERROR, \
    CERT_ALREADY_SUBMITTED_ERROR_BEGINNING


def test_generate_csr_and_import_cert(client_code, client_class, usage_auth=False, key_label=None, check_inputs=False,
                                      check_success=True,
                                      ss2_ssh_host=None, ss2_ssh_user=None, ss2_ssh_pass=None,
                                      delete_csr_before_import=False, generate_key=True, cancel_key_generation=True,
                                      cancel_csr_generation=True, generate_same_csr_twice=True):
    def test_case(self):
        '''
        SS_28 (Generate a Key) / SS_29 (Generate a Certificate Signing Request) / SS_30 (Import a Certificate from
        Local File System) success scenarios. Failure scenarios are tested in another function.
        :param self: MainController object
        :return: None
        '''

        # UC SS_28 (Generate a Key) / SS_29 (Generate a Certificate Signing Request) / SS_30 (Import a Certificate from Local File System)
        # Failure scenarios (SS_xx extensions) are tested under failing_tests()
        self.log('*** SS_28 / SS_29 / SS_30')

        # Set certificate filenames
        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        server_name = ssh_server_actions.get_server_name(self)

        # Get files to be removed (some may be left from previous runs)
        path_wildcard = self.get_download_path('*')

        # Loop over the files and remove them
        for fpath in glob.glob(path_wildcard):
            try:
                os.remove(fpath)
            except:
                pass

        # UC SS_28 Generate a Key
        self.log('*** SS_28 Generate a Key')

        # UC SS_28 1. Select to generate a key on a security token.
        self.log('SS_28 1. Select to generate a key on a security token.')

        # Generate key for authentication device and generate certificate request for the key and save it to local system
        self.log('Generate key and certificate request using that key')

        log_checker = None
        if ss2_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
            current_log_lines = log_checker.get_line_count()
        generate_csr(self, client_code=client_code, client_class=client_class,
                     server_name=server_name,
                     key_label=key_label, check_inputs=check_inputs,
                     cancel_key_generation=cancel_key_generation,
                     cancel_csr_generation=cancel_csr_generation,
                     generate_same_csr_twice=generate_same_csr_twice,
                     generate_key=generate_key,
                     log_checker=log_checker)

        if delete_csr_before_import:
            self.log('SS_30 15a. No CSR notice corresponding to imported cert exist in system configuration')
            sshclient = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
            delete_csr(self, sshclient, log_checker, client_code, client_class)

        # Get the certificate request path
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client_class, client_code]) + '.der'))[
                0]

        # Create an SSH connection to CA
        client = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                      self.config.get('ca.ssh_pass'))

        # Get the certificate local path
        local_cert_path = self.get_download_path(cert_path)

        # UC SS_29/SS_30 Upload certificate request to CA and get the signing certificate from CA
        self.log('SS_29/SS_30 Upload certificate request to CA and get the siging certificate')
        get_cert(client, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)

        file_cert_path = glob.glob(local_cert_path)[0]

        # UC SS_30 Import the certificate to security server
        self.log('*** SS_30 Import certificate to security server')
        import_cert(self, file_cert_path)

        if check_success:
            '''Check if import succeeded'''
            if log_checker is not None:
                time.sleep(5)
                expected_log_msg = IMPORT_CERTIFICATE_FROM_FILE
                self.log('SS_30 16. System logs the event "{0}" to the audit log'.format(expected_log_msg))
                log_check = log_checker.check_log(expected_log_msg,
                                                  from_line=current_log_lines + 1, strict=False)
                self.is_true(log_check)
            self.log('SS_30 16. Check if import succeeded')
            check_import(self, client_class, client_code)

    return test_case


def test_configuration(ssh_host, ssh_username, ssh_password, client_code, client_class):
    def check_configuration(self):
        # UC SS_29 9. Check if the configuration contains information about the generated CSR
        self.log('SS_29 9. Check if the configuration contains information about the generated CSR')

        # Create an SSH connection to the security server
        client = ssh_client.SSHClient(ssh_host, ssh_username, ssh_password)
        key_label = keyscertificates_constants.KEY_LABEL_TEXT + '_' + client_code + '_' + client_class
        filename = keyscertificates_constants.KEY_CONFIG_FILE

        result, error = client.exec_command('cat {0}'.format(filename), True)

        # Check that reading the configuration succeeded
        self.is_not_none(result, msg='SS_29 9. Failed to read configuration from {0}'.format(filename))

        result = '\n'.join(result)

        # Assertion that checks if there is a label with our CSR information in the config XML
        self.is_true(('<label>{0}</label>'.format(key_label) in result),
                     msg='SS_29 9. Configuration does not contain information about the generated CSR')

    return check_configuration


def delete_csr(self, sshclient, log_checker=None, client_code=None, client_class=None, key_has_other_cert_or_csr=False,
               only_item_and_key=False):
    """
    SS_39 Delete CSR from System Configuration
    :param sshclient:
    :param ss_ssh_pass: security server ssh pass
    :param ss_ssh_user: security server ssh user
    :param ss_ssh_host: security server ssh host
    :param self: main instance
    :param client_code: client code of the key, which csr will be deleted
    :param client_class: client class of the key, which csr will be deleted
    :param log_checker: log checker instance for checking audit log
    :return:
    """
    self.log('Wait until keyconf is updated')
    time.sleep(120)
    self.log('Get signing keys count in system configuration')
    signing_keys_count = get_key_conf_keys_count(sshclient, "SIGNING")
    self.log('Get token count in system configuration')
    token_count = get_key_conf_token_count(sshclient)
    self.log('Get csr count in system configuration')
    csr_count = get_key_conf_csr_count(sshclient)
    if log_checker is not None:
        current_log_lines = log_checker.get_line_count()
    '''Row, which is in table after key row'''
    if client_class is not None and client_code is not None:
        csr_row = self.wait_until_visible(type=By.XPATH,
                                          element=keys_and_certificates_table.get_generated_key_row_csr_xpath(
                                              client_code,
                                              client_class))
    else:
        csr_row = self.wait_until_visible(type=By.CSS_SELECTOR,
                                          element=keys_and_certificates_table.CERT_REQUESTS_TABLE_ROW_CSS)
    '''Click on the csr row'''
    csr_row.click()
    self.log('SS_39 Delete Certificate Signing Request Notice from System Configuration')
    self.log('SS_39 1. Click on the delete button to delete CSR')
    self.by_id(keys_and_certificates_table.DELETE_BTN_ID).click()
    self.log('SS_39 2. System prompts for confirmation')
    self.log('SS_39 3. Confirmation popup is confirmed')
    popups.confirm_dialog_click(self)
    if log_checker is not None:
        expected_log_msg = DELETE_CSR
        self.log('SS_39 5. System logs the event "{0}" in the audit log'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg="{0} not found in audit log".format(expected_log_msg))
    self.log('Wait until System Configuration is updated')
    time.sleep(120)
    self.log('SS_39 4. System deletes the CSR from system configuration')
    signing_keys_count_after_deletion = get_key_conf_keys_count(sshclient, "SIGNING")
    self.log('Get token count in system configuration')
    token_count_after_deletion = get_key_conf_token_count(sshclient)
    self.log('Get key count in system configuration')
    csr_count_after = get_key_conf_csr_count(sshclient)
    if key_has_other_cert_or_csr:
        self.log('SS_39 4. System deletes only CSR when key has more certificates or csrs')
        self.is_equal(signing_keys_count, signing_keys_count_after_deletion)
        self.is_true(csr_count_after < csr_count)
    elif only_item_and_key:
        self.log('SS_39 4b.1 System deletes CSR, key and cert when csr is keys last item and key is last token item')
        self.is_true(signing_keys_count_after_deletion < signing_keys_count)
        self.is_true(token_count_after_deletion < token_count)
        self.is_true(csr_count_after < csr_count)
    else:
        self.log('SS_39 4a.1 System deletes the CSR and key from system when key has no more certificates and csrs')
        self.is_true(signing_keys_count > signing_keys_count_after_deletion)
        self.is_true(csr_count_after < csr_count)


def register_cert(self, ssh_host, ssh_user, ssh_pass, cs_host, client, ca_ssh_host, ca_ssh_user, ca_ssh_pass, cert_path,
                  check_inputs=False):
    """
    SS_34 Register an Authentication Certificate
    :param cert_path:
    :param ca_ssh_pass:
    :param ca_ssh_user:
    :param ca_ssh_host:
    :param client:
    :param cs_host:
    :param self: MainController instance
    :param ssh_host: ssh host of the security server
    :param ssh_user: ssh user of the security server
    :param ssh_pass: ssh password of the security server
    :param check_inputs: bool|False: checking input parsing
    :return:
    """

    def register():
        log_checker = auditchecker.AuditChecker(ssh_host, ssh_user, ssh_pass)
        current_log_lines = log_checker.get_line_count()
        time.sleep(3)
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()
        self.log('Click on the key, which certificate was just deleted')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=keys_and_certificates_table.UNSAVED_KEY_CSS).click()
        self.log('Generate new auth certificate for the key')
        generate_auth_csr(self, ca_name=ca_ssh_host, change_usage=True)
        '''Current time'''
        now_date = datetime.datetime.now()
        '''Downloaded csr file name'''
        file_name = 'auth_csr_' + now_date.strftime('%Y%m%d') + '_securityserver_{0}_{1}_{2}_{3}.der'. \
            format(client['instance'], client['class'], client['code'], client['name'])
        '''Downloaded csr file path'''
        file_path = glob.glob(self.get_download_path('_'.join(['*']) + file_name))[0]
        '''SSH client instance for ca'''
        sshclient = ssh_server_actions.get_client(ca_ssh_host, ca_ssh_user, ca_ssh_pass)
        '''Remote csr path'''
        remote_csr_path = 'temp.der'
        '''Local cert path'''
        local_cert_path = self.get_download_path(cert_path)
        self.log('Getting certificate from ca')
        get_cert(sshclient, 'sign-auth', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        import_cert(self, local_cert_path)
        self.log('Click on the imported certificate row')
        self.log('SS_30 14a.1. Imported auth cert is disabled and its state is "saved" ')
        self.wait_until_visible(type=By.XPATH, element=keys_and_certificates_table.SAVED_CERTIFICATE_ROW_XPATH).click()
        self.log('SS_34 1. Clicking "register" button')
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.REGISTER_BTN_ID).click()
        self.log('SS_34 2. System prompts for DNS name/IP address of the security server')
        address_input = self.wait_until_visible(type=By.ID,
                                                element=keys_and_certificates_table.REGISTER_DIALOG_ADDRESS_INPUT_ID)
        '''SS_34 4. System parses the user input'''
        if check_inputs:
            self.log('SS_34 4. System parses the user input')
            self.log('Trying to register with empty address')
            self.by_xpath(popups.REGISTRATION_DIALOG_OK_BUTTON_XPATH).click()
            self.log('SS_34 4a.1 System displays the termination message from the parsing process')
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(messages.MISSING_PARAMETER.format('address'), error_msg)
            messages.close_error_messages(self)
            expected_log_event = log_constants.REGISTER_AUTH_CERT_FAILED
            self.log('SS_34 4a.2 System logs the event {0}'.format(expected_log_event))
            logs_found = log_checker.check_log(expected_log_event, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            current_log_lines = log_checker.get_line_count()

            invalid_host_address = ':'
            self.log('Trying to register with invalid address')
            self.input(element=address_input, text=invalid_host_address)
            self.by_xpath(popups.REGISTRATION_DIALOG_OK_BUTTON_XPATH).click()
            self.log('SS_34 5a.1 System displays the error message')
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(messages.INVALID_HOST_ADDRESS, error_msg)
            messages.close_error_messages(self)
            self.log('SS_34 5a.2 System logs the event {0}'.format(expected_log_event))
            logs_found = log_checker.check_log(expected_log_event, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            current_log_lines = log_checker.get_line_count()

            input_256_char = 'A' * 256
            self.log('Trying to register with too long address(256 chars)')
            self.input(element=address_input, text=input_256_char)
            self.by_xpath(popups.REGISTRATION_DIALOG_OK_BUTTON_XPATH).click()
            self.log('SS_34 4a.1 System displays the termination message from the parsing process')
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(messages.INPUT_EXCEEDS_255_CHARS.format('address'), error_msg)
            messages.close_error_messages(self)
            self.log('SS_34 4a.2 System logs the event {0}'.format(expected_log_event))
            logs_found = log_checker.check_log(log_constants.REGISTER_AUTH_CERT_FAILED, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            current_log_lines = log_checker.get_line_count()

            input_255_char = ' {0} '.format('C' * 255)
            self.log('SS_34 4. Trying to register with max length address(255 chars)')
            self.log('SS_34 6a. Creating or sending the error message failed')
            self.input(element=address_input, text=input_255_char)
            hosts_replacement = 'cs.asd'
            self.log('Replacing central server in hosts file, so the request wont make it to the central server')
            self.ssh_client = ssh_client.SSHClient(ssh_host, ssh_user, ssh_pass)
            self.ssh_client.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(cs_host, hosts_replacement, '/etc/hosts'),
                sudo=True)
            try:
                self.log('Clicking submit button')
                self.by_xpath(popups.REGISTRATION_DIALOG_OK_BUTTON_XPATH).click()
                self.wait_jquery()
                self.log('SS_34 6a.1 System displays the error message')
                error_msg = messages.get_error_message(self)
                self.is_equal(messages.FAILED_TO_REGISTER_HOST_NOT_KNOWN_ERROR.format(cs_host), error_msg)
                messages.close_error_messages(self)
                self.log('SS_34 6a.2 System logs the event {0}'.format(expected_log_event))
                logs_found = log_checker.check_log(expected_log_event, from_line=current_log_lines + 1)
                self.is_true(logs_found)
                current_log_lines = log_checker.get_line_count()
            except Exception as error:
                self.log(error)
                self.log('Adding max length address without central server failed')
                assert False
            finally:
                self.log('Restore hosts file')
                self.ssh_client.exec_command(
                    'sed -i -e "s/{0}/{1}/g" {2}'.format(hosts_replacement, cs_host, '/etc/hosts'),
                    sudo=True)
        time.sleep(10)
        self.log('SS_34 3. The DNS name of the server is inserted')
        self.input(element=address_input, text=ssh_host)
        self.log('Click ok')
        self.by_xpath(popups.REGISTRATION_DIALOG_OK_BUTTON_XPATH).click()
        self.wait_jquery()
        self.log('SS_34 8. System displays the message {0}'.format(messages.REQUEST_SENT_NOTICE))
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
        self.is_equal(messages.REQUEST_SENT_NOTICE, notice_msg)
        self.log('SS_34 8. System sets the registration state of the cert to "registration in progress"')
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.REG_IN_PROGRESS_CERTIFICATE_ROW_XPATH)
        expected_log_event = log_constants.REGISTER_AUTH_CERT
        self.log('SS_34 9. System logs the event {0}'.format(expected_log_event))
        logs_found = log_checker.check_log(expected_log_event, from_line=current_log_lines + 1)
        self.is_true(logs_found)

    return register


def test_add_cert_to_ss(self, cs_host, cs_username, cs_password, client, cert_path, cs_ssh_host, cs_ssh_user,
                        cs_ssh_pass, cancel_cert_registration=False, file_format_errors=False,
                        add_existing_error=False):
    """
    MEMBER_23 Create an Authentication Certificate Registration Request
    :param self: mainController instance
    :param cs_host: central server host
    :param cs_username: central server username
    :param cs_password: central server password
    :param client: client information
    :param cert_path: cert filename
    :return:
    """
    log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
    current_log_lines = log_checker.get_line_count()
    self.log('Open central server homepage')
    self.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
    self.log('Open added member details')
    global_groups_tests.open_member_details(self, client)
    self.wait_jquery()
    self.log('Open owned servers tab')
    self.by_xpath(cs_security_servers.SERVER_MANAGEMENT_OWNED_SERVERS_TAB).click()
    self.log('Open owned server details')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=MEMBER_FIRST_OWNED_SERVER_DETAILS_CSS).click()
    self.wait_jquery()

    self.wait_until_visible(type=By.XPATH, element=SS_DETAILS_AUTH_CERT_TAB_XPATH).click()
    self.log('MEMBER_23 1. Add authentication cert button is clicked')
    self.wait_until_visible(type=By.ID, element=SS_DETAILS_ADD_AUTH_CERT_BTN_ID).click()
    if cancel_cert_registration:
        self.log('MEMBER_23 3a. Authentication cert registration creation is canceled')
        self.wait_until_visible(type=By.XPATH, element=ADD_AUTH_CERT_CANCEL_BTN_XPATH).click()
        self.log('MEMBER_23 1. Add authentication cert button is clicked again')
        self.wait_until_visible(type=By.ID, element=SS_DETAILS_ADD_AUTH_CERT_BTN_ID).click()
    self.log('MEMBER_23 3. Authentication cert is uploaded from local filesystem')
    upload = self.wait_until_visible(type=By.ID, element=ADD_AUTH_CERT_UPLOAD_BTN_ID)
    local_cert_path = self.get_download_path(cert_path)
    file_abs_path = os.path.abspath(local_cert_path)
    if file_format_errors:
        self.log('MEMBER_23 4a. The uploaded file is not in PEM or DER format')
        not_existing_file_with_wrong_extension = 'C:\\file.asd'
        xroad.fill_upload_input(self, upload, not_existing_file_with_wrong_extension)
        expected_msg = AUTH_CERT_IMPORT_FILE_FORMAT_ERROR
        self.log('MEMBER 23 4a.1 System displays the error message {0}'.format(expected_msg))
        error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
        self.is_equal(expected_msg, error_msg)
        messages.close_error_messages(self)
    xroad.fill_upload_input(self, upload, file_abs_path)
    if add_existing_error:
        self.log('MEMBER 23 5a. The auth certificate is already registered or '
                 'submitted for registration with authenticaion registration request')
        self.wait_until_visible(type=By.ID, element=ADD_AUTH_CERT_SUBMIT_BTN_ID).click()
        self.wait_jquery()
        expected_msg = CERT_ALREADY_SUBMITTED_ERROR_BEGINNING
        self.log('MEMBER 23 5a.1 System displays the error message {0}'.format(expected_msg))
        error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
        self.is_true(error_msg.startswith(expected_msg))
        expected_log_msg = ADD_AUTH_CERTIFICATE_FOR_SECURITY_SERVER_FAILED
        self.log('MEMBER 23 5a.2 System logs the event {0}'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)
        return
    self.wait_jquery()
    expected_msg = messages.CERTIFICATE_IMPORT_SUCCESSFUL
    self.log('MEMBER_23 4. System displays the message {0}'.format(expected_msg))
    import_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
    self.is_equal(expected_msg, import_msg)
    self.log('Submit authentication cert button is pressed')
    self.wait_until_visible(type=By.ID, element=ADD_AUTH_CERT_SUBMIT_BTN_ID).click()
    self.wait_jquery()
    expected_msg = messages.get_cert_adding_existing_server_req_added_notice(client)
    self.log('MEMBER_23 7. System displays the message {0}'.format(expected_msg))
    import_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
    self.is_equal(expected_msg, import_msg)
    expected_log_msg = log_constants.ADD_AUTH_CERTIFICATE_FOR_SECURITY_SERVER
    self.log('MEMBER_23 8. System logs the event "{0}"'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)


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
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        '''Current log lines'''
        current_log_lines = log_checker.get_line_count()
        self.log('Wait until keyconf is updated')
        time.sleep(120)
        '''Find not active certs in keyconf file'''
        keyconf_before = get_disabled_certs(sshclient)
        registration_in_progress_row = self.wait_until_visible(type=By.XPATH,
                                                               element=keys_and_certificates_table.OCSP_DISABLED_CERT_ROW)
        '''Get the cert key label'''
        key_label = registration_in_progress_row.find_element_by_xpath('../preceding::tr[2]//td').text.split(' ')[1]
        '''Click on the certificate'''
        registration_in_progress_row.click()
        self.log('SS_32 1. "Activate a certificate" button is clicked')
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.ACTIVATE_BTN_ID).click()
        self.log('Waiting until keyconf is updated')
        time.sleep(120)
        '''Find not active certs in keyconf file'''
        keyconf_after = get_disabled_certs(sshclient)
        '''Check if keyconf is different than before'''
        self.log('SS_32 2. System activates the certificate')
        self.not_equal(keyconf_before, keyconf_after)

        if not registered:
            self.log('Wait until OCSP response is present')
            time.sleep(120)
            self.driver.refresh()
            self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.KEYS_AND_CERTIFICATES_TABLE_ID)
            '''Activated cert'''
            activated_cert = self.by_xpath(keys_and_certificates_table.CERT_BY_KEY_LABEL.format(key_label))
            self.log('SS_32 2. System displays the latest OCSP response value')
            self.is_true(
                len(activated_cert.find_element_by_class_name(
                    keys_and_certificates_table.OCSP_RESPONSE_CLASS_NAME).text) > 0)
        expected_log_msg = ENABLE_CERTIFICATE
        self.log('SS_32 3. System logs the event "{0}" to the audit log'.format(expected_log_msg))
        time.sleep(1.5)
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1,
                                           strict=False)
        self.is_true(logs_found)
        self.log('Hard refresh server OCSP')
        ssh_server_actions.refresh_ocsp(sshclient)

    return activate


def disable_cert(self, ss_host, ss_user, ss_pass, ss_ssh_host, ss_ssh_user, ss_ssh_pass):
    """
    SS_33: Disable a certificate
    :param self: mainController instance
    :param ss_host: security server host
    :param ss_user: security server username
    :param ss_pass: security server password
    :param ss_ssh_host: security server ssh host
    :param ss_ssh_user: security server ssh user
    :param ss_ssh_pass: security server ssh pass
    :return:
    """

    def disable():
        '''Log checker instance'''
        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        current_log_lines = log_checker.get_line_count()
        '''Security server SSH client instance'''
        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        '''Find not active certs in keyconf file'''
        keyconf_before = get_disabled_certs(sshclient)
        '''Open security server homepage'''
        self.reload_webdriver(ss_host, ss_user, ss_pass)
        '''Open keys and certificates view'''
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        '''Find first auth type keys certificate'''
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.CERT_BY_KEY_LABEL.format('auth')).click()
        self.log('SS_33 1. Certificate disable button is clicked')
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DISABLE_BTN_ID).click()
        self.wait_jquery()
        self.log('SS_33 2. System sets the OCSP status to disabled')
        cert = self.wait_until_visible(type=By.XPATH,
                                       element=keys_and_certificates_table.CERT_BY_KEY_LABEL.format('auth'))
        status = cert.find_element_by_class_name(keys_and_certificates_table.OCSP_RESPONSE_CLASS_NAME).text
        self.is_equal(keys_and_certificates_table.OCSP_DISABLED_RESPONSE, status)
        self.log('SS_33 3. System logs {0}'.format(log_constants.DISABLE_CERT))
        logs_found = log_checker.check_log(log_constants.DISABLE_CERT, from_line=current_log_lines + 1)
        self.is_true(logs_found)
        self.log('Wait until keyconf is updated')
        time.sleep(120)
        '''Find not active certs in keyconf file'''
        self.log('SS_33 2. System disables the certificate')
        keyconf_after = get_disabled_certs(sshclient)
        self.not_equal(keyconf_before, keyconf_after)

    return disable


def get_disabled_certs(sshclient):
    return sshclient.exec_command(
        'grep active=\\\"false\\\" {0}'.format(keys_and_certificates_table.KEY_CONFIG_FILE), sudo=True)


def check_import_fail_log(self, log_checker, current_log_lines, step):
    expected_log_msg = IMPORT_CERTIFICATE_FROM_FILE_FAILED
    self.log('SS_30 {0} System logs the event "{1}" to the audit log. '.format(step, expected_log_msg))
    fail_log_present = log_checker.check_log(expected_log_msg,
                                             from_line=current_log_lines + 1, strict=False)
    self.is_true(fail_log_present)
    return log_checker.get_line_count()


def failing_tests(file_client_name, file_client_class, file_client_code, file_client_instance, ca_name, ss2_ssh_host,
                  ss2_ssh_user, ss2_ssh_pass):
    def fail_test_case(self):
        self.log('Adding testing client')
        client = {'name': 'failure', 'class': 'COM', 'code': 'failure', 'subsystem_code': 'failure'}
        error = False
        try:
            '''Add a temporary client for testing the failure scenarios'''
            add_client(self, client)
            '''Log checker instance'''
            log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
            current_log_lines = log_checker.get_line_count()

            '''SS_30 11a import an expired cert'''
            self.log('SS_30 11a import an expired cert')
            test_expired_cert_error(self, client)
            current_log_lines = check_import_fail_log(self, log_checker, current_log_lines, step="11a.2")

            '''SS_30 10a cert by not approved ca'''
            self.log('SS_30 10a cert by not approved ca')
            not_valid_ca_error(self, client)
            self.log('SS_30 10a.2 System logs the event "{0}" to the audit log. '.format(
                log_constants.IMPORT_CERTIFICATE_FROM_FILE_FAILED))
            current_log_lines = check_import_fail_log(self, log_checker, current_log_lines, step="10a.2")

            '''SS_30 9a import an authentication certificate for a signing key'''
            self.log('SS_30 9a import an authentication certificate for a signing key')
            wrong_cert_type_error(self, client)
            current_log_lines = check_import_fail_log(self, log_checker, current_log_lines, step="9a.2")

            '''SS_30 7a cert by not approved ca'''
            self.log('SS_30 7a cert by not approved ca')
            no_key_error(self, client)
            current_log_lines = check_import_fail_log(self, log_checker, current_log_lines, step="7a.2")

            '''SS_30 6a cert by not approved ca'''
            self.log('SS_30 6a cert by not approved ca')
            no_client_for_certificate_error(self, client)
            current_log_lines = check_import_fail_log(self, log_checker, current_log_lines, step="6a.2")

            '''SS_30 4a cert is not in valid format'''
            self.log('SS_30 4a cert is not in valid format')
            wrong_format_error(self)
            current_log_lines = check_import_fail_log(self, log_checker, current_log_lines, step="4a.2")

            '''SS_30 8a cert already exists'''
            self.log('SS_30 8a cert already exists')
            already_existing_error(self, client)
            current_log_lines = check_import_fail_log(self, log_checker, current_log_lines, step="8a.2")

            '''SS_30 9b import a signing certificate for an authentication key'''
            self.log('SS_30 9b import a signing certificate for an authentication key')
            sign_cert_instead_auth_cert(self, file_client_name, file_client_class, file_client_code,
                                        file_client_instance, ca_name=ca_name)
            check_import_fail_log(self, log_checker, current_log_lines, step="9b.2")

        except:
            '''Exception occured, print traceback'''
            traceback.print_exc()
            error = True

        finally:
            '''Always remove the temporary client'''
            remove_client(self, client)
            if error:
                raise RuntimeError('Failure testing FAILED')

    def add_client(self, client):
        '''
        Add a temporary client for testing.
        :param self: MainController object
        :param client: client information
        :return: None
        '''

        # Start adding client
        self.driver.get(self.url)
        self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

        # Set client class, code, subsystem information
        self.log('Select {0} from "CLIENT CLASS" dropdown'.format(client['class']))
        member_class = Select(
            self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID))
        member_class.select_by_visible_text(client['class'])

        self.log('Insert {0} into "CLIENT CODE" area'.format(client['code']))
        member_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
        self.input(member_code, client['code'])

        self.log('Insert {0} into "SUBSYSTEM CODE" area'.format(client['subsystem_code']))
        member_sub_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_ID)
        self.input(member_sub_code, client['subsystem_code'])

        # Save client data
        self.log('Click "OK" to add client')
        self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
        try:
            # If we get a warning, click "Continue"
            self.log('Confirming warning')
            if self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP):
                self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        except:
            # If no warning, there is still no problem.
            self.log('No warning')
        self.wait_jquery()
        time.sleep(2)
        # Confirm adding the client
        popups.confirm_dialog_click(self)

    def remove_client(self, client):
        '''
        Remove the temporary client.
        :param self: MainController object
        :param client: client data
        :return:
        '''
        self.log('Removing client from server')
        self.driver.get(self.url)
        self.wait_jquery()

        # Find client and click on the table row
        client_row = added_client_row(self, client)
        client_row.find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS).click()
        try:
            # Click the "Unregister" button
            self.log('Finding and clicking unregister button')
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
            self.wait_jquery()

            # Confirm unregistering
            self.log('Confirm unregistering')
            popups.confirm_dialog_click(self)
            self.wait_jquery()
            time.sleep(3)

            # Confirm deletion
            self.log('Confirm deleting')
            popups.confirm_dialog_click(self)
        except:
            # Exception may occur if the client has not been fully registered. As we still need to remove
            # temporary data, delete the client anyway.
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
            self.wait_jquery()

            # Confirm deletion
            popups.confirm_dialog_click(self)

    def remove_certificate(self, client):
        '''
        Remove certificate from server.
        :param self: MainController object
        :param client: client data
        :return: None
        '''
        self.log('REMOVE CERTIFICATE')

        # Click on generated key row
        self.log('Click on generated key row')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.get_generated_key_row_xpath(client['code'],
                                                                                               client[
                                                                                                   'class'])).click()
        # Click on Delete button and confirm deletion.
        self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()
        popups.confirm_dialog_click(self)

    def test_expired_cert_error(self, client):
        flag_to_replace = '-days 7300'
        replacement = '-startdate 120815080000Z -enddate 120815090000Z'
        try:
            remote_csr_path = 'temp.der'
            cert_path = 'temp.pem'

            '''Get local certificate path'''
            local_cert_path = self.get_download_path(cert_path)

            server_name = ssh_server_actions.get_server_name(self)

            '''Remove temporary files'''
            for fpath in glob.glob(self.get_download_path('*')):
                os.remove(fpath)

            '''Generate CSR for the client'''
            generate_csr(self, client_code=client['code'], client_class=client['class'],
                         server_name=ssh_server_actions.get_server_name(self),
                         check_inputs=False)
            file_path = \
                glob.glob(
                    self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]

            '''Create a new SSH connection to CA'''
            sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                             self.config.get('ca.ssh_pass'))
            sshclient.exec_command(
                command='sed -i -e "s/{0}/{1}/g" /home/ca/CA/sign.sh'.format(flag_to_replace, replacement), sudo=True)

            '''Get the signing certificate from our CSR'''
            get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
            time.sleep(6)
            file_cert_path = glob.glob(local_cert_path)[0]

            '''Try to import the certificate'''
            import_cert(self, file_cert_path)
            self.wait_jquery()
            time.sleep(2)

            expected_error_msg = messages.CERTIFICATE_NOT_VALID
            self.log('SS_30 11a.1 System displays the error message {0}'.format(expected_error_msg))
            self.is_equal(expected_error_msg, messages.get_error_message(self))
        except:
            assert False
        finally:
            self.log('Restore ca signing script')
            sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                             self.config.get('ca.ssh_pass'))
            sshclient.exec_command(
                command='sed -i -e "s/{0}/{1}/g" /home/ca/CA/sign.sh'.format(replacement, flag_to_replace), sudo=True)
            popups.close_all_open_dialogs(self)
            remove_certificate(self, client)

    def not_valid_ca_error(self, client):
        '''
        Test for trying to add a certificate that was not issued by a valid certification authority (SS_30 10a)
        Expectation: certificate not added.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # UC SS_30 10a. Certificate is issued by a certification authority that is not in the allow list
        self.log('SS_30 10a. Certificate is issued by a certification authority that is not in the allow list')
        error = False
        try:
            remote_csr_path = 'temp.der'
            cert_path = 'temp.pem'

            # Get local certificate path
            local_cert_path = self.get_download_path(cert_path)

            server_name = ssh_server_actions.get_server_name(self)

            # Remove temporary files
            for fpath in glob.glob(self.get_download_path('*')):
                os.remove(fpath)

            # Generate CSR for the client
            self.log('Generate CSR for the client')
            generate_csr(self, client_code=client['code'], client_class=client['class'],
                         server_name=ssh_server_actions.get_server_name(self),
                         check_inputs=False)
            file_path = \
                glob.glob(
                    self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]

            # Create a new SSH connection to CA
            sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                             self.config.get('ca.ssh_pass'))

            # Get the signing certificate from our CSR
            self.log('Get the signing certificate from the certificate request')
            get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
            time.sleep(6)
            file_cert_path = glob.glob(local_cert_path)[0]

            # Remove CA from central server
            self.log('Removing ca from central server')

            # Relogin
            self.logout(self.config.get('cs.host'))
            self.login(self.config.get('cs.user'), self.config.get('cs.pass'))

            # Go to certification services in the UI
            self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CERTIFICATION_SERVICES_CSS).click()

            table = self.wait_until_visible(type=By.ID, element=certification_services.CERTIFICATION_SERVICES_TABLE_ID)
            rows = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

            # Find our CA and remove it
            for row in rows:
                if self.config.get('ca.name') in row.text:
                    row.click()
                    self.wait_until_visible(type=By.ID, element=certification_services.DELETE_BTN_ID).click()
                    popups.confirm_dialog_click(self)

            self.log('Wait 120 seconds for changes')
            time.sleep(120)
            self.log('Reloading page after changes')

            # Reload page and wait until additional data is loaded using jQuery
            self.driver.refresh()
            self.wait_jquery()

            # Try to import the certificate
            self.log('Trying to import certificate')
            import_cert(self, file_cert_path)
            self.wait_jquery()
            time.sleep(2)

            # Check if we got an error message
            self.log('SS_30 10a.1. System displays the error message {0}'.format(messages.CA_NOT_VALID_AS_SERVICE))
            self.is_equal(messages.CA_NOT_VALID_AS_SERVICE, messages.get_error_message(self))
        except:
            # Test failed

            self.log('SS_30 10a failed')
            # Print traceback
            traceback.print_exc()
            error = True
        finally:
            # After testing, re-add the CA and restore the state the server was in
            self.log('Restore: Restoring previous state')

            # Login to Central Server
            self.driver.get(self.config.get('cs.host'))

            if not login.check_login(self, self.config.get('cs.user')):
                self.login(self.config.get('cs.user'), self.config.get('cs.pass'))

            # Create SSH connection to CA
            sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'),
                                             self.config.get('ca.ssh_user'),
                                             self.config.get('ca.ssh_pass'))

            target_ca_cert_path = self.get_download_path("ca.pem")
            target_ocsp_cert_path = self.get_download_path("ocsp.pem")

            # Get CA certificates using SSH
            self.log('Restore: Getting CA certificates')
            get_ca_certificate(sshclient, 'ca.cert.pem', target_ca_cert_path)
            get_ca_certificate(sshclient, 'ocsp.cert.pem', target_ocsp_cert_path)
            sshclient.close()

            # Go to Central Server UI main page
            self.driver.get(self.config.get('cs.host'))

            self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CERTIFICATION_SERVICES_CSS).click()
            self.wait_jquery()
            time.sleep(3)

            table = self.wait_until_visible(type=By.ID, element=certification_services.CERTIFICATION_SERVICES_TABLE_ID)
            rows = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

            # If CA server is not listed, re-add it
            if self.config.get('ca.ssh_host') not in map(lambda x: x.text, rows):
                self.log('Restore: CA not found, re-adding')
                self.wait_until_visible(type=By.ID, element=certification_services.ADD_BTN_ID).click()
                import_cert_btn = self.wait_until_visible(type=By.ID,
                                                          element=certification_services.IMPORT_CA_CERT_BTN_ID)

                # Upload CA certificate and submit the form
                xroad.fill_upload_input(self, import_cert_btn, target_ca_cert_path)

                self.wait_until_visible(type=By.ID, element=certification_services.SUBMIT_CA_CERT_BTN_ID).click()

                # Set CA additional information
                profile_info_area = self.wait_until_visible(type=By.CSS_SELECTOR,
                                                            element=certification_services.CERTIFICATE_PROFILE_INFO_AREA_CSS)

                ca_profile_class = self.config.get('ca.profile_class')
                self.input(profile_info_area, ca_profile_class)

                # Save the settings
                self.wait_until_visible(type=By.ID, element=certification_services.SUBMIT_CA_SETTINGS_BTN_ID).click()
                self.wait_jquery()

                # Open OCSP tab
                self.wait_until_visible(type=By.XPATH, element=certification_services.OCSP_RESPONSE_TAB).click()

                self.log('Restore: Add OCSP responder')
                self.wait_until_visible(type=By.ID, element=certification_services.OCSP_RESPONDER_ADD_BTN_ID).click()

                # Import OCSP certificate
                import_cert_btn = self.wait_until_visible(type=By.ID,
                                                          element=certification_services.IMPORT_OCSP_CERT_BTN_ID)

                xroad.fill_upload_input(self, import_cert_btn, target_ocsp_cert_path)

                url_area = self.wait_until_visible(type=By.ID,
                                                   element=certification_services.OCSP_RESPONDER_URL_AREA_ID)

                self.input(url_area, self.config.get('ca.ocs_host'))

                # Save OCSP information
                self.wait_until_visible(type=By.ID,
                                        element=certification_services.SUBMIT_OCSP_CERT_AND_URL_BTN_ID).click()

            # Reload CS main page
            self.driver.get(self.url)

            # Open keys and certificates
            self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()

            # Remove the testing certificate
            remove_certificate(self, client)

            self.log('Restore: Wait 120 seconds for changes')
            time.sleep(120)
            if error:
                # If, at some point, we got an error, fail the test now
                assert False, 'SS_30 10a test failed'

    def wrong_cert_type_error(self, client):
        '''
        Test that tries to import a wrong type of certificate to the server. This certificate should not be imported.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # UC SS_30 9a Certificate is not a signing certificate
        self.log('SS_30 9a test importing a certificate that is not a signing certificate')
        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        # Set local path for certificate
        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        # Remove temporary files
        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        # Generate CSR for the client
        self.log('SS_30 9a. Generate CSR for the client')
        generate_csr(self, client_code=client['code'], client_class=client['class'],
                     server_name=ssh_server_actions.get_server_name(self),
                     check_inputs=False)
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]

        # Create SSH connection to CA
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        # Get an authentication certificate instead of signing certificate.
        self.log('SS_30 9a. Get the authentication certificate')
        get_cert(sshclient, 'sign-auth', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        # Try to import certificate
        self.log('SS_30 9a. Trying to import authentication certificate as signing certificate. Should fail.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        self.log('SS_30 9a.1. System displays the error message {0}'.format(messages.CERTIFICATE_NOT_SIGNING_KEY))
        self.is_equal(messages.CERTIFICATE_NOT_SIGNING_KEY, messages.get_error_message(self))

        self.log('SS_30 9a. Remove test data')
        popups.close_all_open_dialogs(self)
        remove_certificate(self, client)

    def no_key_error(self, client):
        '''
        Try to import certificate that does not have a corresponding key in the server. Should fail.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # UC SS_30 7a. Key used for requesting the certificate is not found
        self.log('SS_30 7a. Test importing a certificate that does not have a corresponding key')
        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        # Get local certificate path
        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        # Remove temporary files
        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        # Generate CSR
        self.log('SS_30 7a. Generate CSR for the client')
        generate_csr(self, client_code=client['code'], client_class=client['class'],
                     server_name=ssh_server_actions.get_server_name(self),
                     check_inputs=False)
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        # Get the signing certificate from CA
        self.log('SS_30 7a. Getting signing certificate from the CA')
        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        # Remove the certificate and key from the server
        self.log('SS_30 7a. Remove the key from the server')
        remove_certificate(self, client)

        # Try to import the certificate that does not have a key any more
        self.log('SS_30 7a. Try to import the certificate. Should fail.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        self.log('SS_30 7a.1. System displays the error message {0}'.format(messages.NO_KEY_FOR_CERTIFICATE))
        self.is_equal(messages.NO_KEY_FOR_CERTIFICATE, messages.get_error_message(self))
        self.log('SS_30 7a.1. Got an error message, test succeeded')

    def no_client_for_certificate_error(self, client):
        '''
        Try to import a certificate that is issued to a non-existing client. Should fail.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # UC SS_30 6a. Client set in the certificate is not in the system
        self.log('SS_30 6a. Import a certificate that is issued to a non-existing client.')

        self.driver.get(self.url)
        self.wait_jquery()

        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        # Get the local path of the certificate
        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        # Remove temporary files
        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        # Generate CSR for the client
        self.log('SS_30 6a. Generate CSR for the client')
        generate_csr(self, client_code=client['code'], client_class=client['class'],
                     server_name=ssh_server_actions.get_server_name(self),
                     check_inputs=False)
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]

        # Create an SSH connection to CA
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        # Get the signing certificate from CA
        self.log('SS_30 6a. Get the signing certificate from CA')
        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        # Remove the test client.
        self.log('SS_30 6a. Removing test client.')
        remove_client(self, client)

        # Try to import the certificate. Should fail.
        self.log('SS_30 6a. Import a certificate that is issued to the client that was just removed. Should fail.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        self.log('SS_30 6a.1. System displays the error message {0}'.format(messages.NO_CLIENT_FOR_CERTIFICATE))
        self.is_true(messages.get_error_message(self).startswith(messages.NO_CLIENT_FOR_CERTIFICATE))
        self.log('SS_30 6a.1. Got an error, test succeeded.')

        popups.close_all_open_dialogs(self)

        # Remove the certificate from the server
        self.log('SS_30 6a. Removing the certificate.')
        remove_certificate(self, client)

        self.driver.get(self.url)
        self.wait_jquery()

        # Restore the client
        self.log('SS_30 6a. Restoring the client.')
        add_client(self, client)

        # Wait until data updated
        time.sleep(60)

    def wrong_format_error(self):
        '''
        Test importing a certificate that is in a wrong format (not DER/PEM). Should fail.
        :param self: MainController object
        :return: None
        '''

        # UC SS_30 4a. Try to import a non-DER and non-PEM certificate. Should fail.
        self.log('SS_30 4a. Trying to import a non-DER and non-PEM certificate')

        self.driver.get(self.url)
        self.wait_jquery()

        # Get a text file
        path = self.get_temp_path('INFO')
        temp_path = glob.glob(path)[0]

        # Try to import the text file as a certificate. Should fail.
        self.log('SS_30 4a. Trying to import a non-PEM/non-DER file. Should fail.')
        import_cert(self, temp_path)
        self.wait_jquery()
        time.sleep(3)

        self.log('SS_30 4a.1. System displays the error message {0}'.format(messages.WRONG_FORMAT_CERTIFICATE))
        self.is_equal(messages.WRONG_FORMAT_CERTIFICATE, messages.get_error_message(self))
        self.log('SS_30 4a.1. Got an error, test succeeded.')

    def already_existing_error(self, client):
        '''
        Test importing a certificate that already exists. Should not be added as a duplicate.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # UC SS_30 8a. Try to import a certificate that has already been added.
        self.log('SS_30 8a. Try to import a certificate that has already been added.')

        self.driver.get(self.url)
        self.wait_jquery()

        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        # Get local certificate path
        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        # Generate CSR for the client
        self.log('SS_30 8a. Generate CSR for the client')
        generate_csr(self, client_code=client['code'], client_class=client['class'],
                     server_name=ssh_server_actions.get_server_name(self),
                     check_inputs=False)
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]

        # Open an SSH connection to CA
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        # Get the signing certificate from CA
        self.log('SS_30 8a. Get signing certificate from CA')
        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        # Import the signing certificate. Should succeed.
        self.log('SS_30 8a. Import the signing certificate.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        # Import the same signing certificate. Should fail.
        self.log('SS_30 8a. Import the same signing certificate. Should fail.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        self.log('SS_30 8a.1. System displays the error message {0}'.format(messages.CERTIFICATE_ALREADY_EXISTS))
        self.is_true(messages.get_error_message(self).startswith(messages.CERTIFICATE_ALREADY_EXISTS))
        self.log('SS_30 8a.1. Got an error for duplicate certificate, test succeeded')

        popups.close_all_open_dialogs(self)

        # Remove the certificate
        self.log('SS_30 8a. Removing the test certificate')
        remove_certificate(self, client)

    def sign_cert_instead_auth_cert(self, file_client_name, file_client_class, file_client_code, file_client_instance,
                                    ca_name):
        '''
        Test that tries to import a wrong type of certificate to the server. This certificate should not be imported.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # UC SS_30 9b. Certificate is not a signing certificate

        self.log('SS_30 9b. Test importing a certificate that is not a signing certificate')
        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        now_date = datetime.datetime.now()
        file_name = 'auth_csr_' + now_date.strftime('%Y%m%d') + '_securityserver_{0}_{1}_{2}_{3}.der'. \
            format(file_client_instance, file_client_class, file_client_code, file_client_name)
        print(file_name)
        # Set local path for certificate
        local_cert_path = self.get_download_path(cert_path)

        # Remove temporary files
        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        # Open the keys and certificates tab
        self.log('Open keys and certificates tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()

        # Add new key
        self.log('Add new key label name - ' + keyscertificates_constants.KEY_LABEL_TEXT)
        user_input_check.add_key_label(self, keyscertificates_constants.KEY_LABEL_TEXT)

        self.wait_jquery()

        # Generate a authentication certificate
        generate_auth_csr(self, ca_name=ca_name)

        file_path = \
            glob.glob(self.get_download_path('_'.join(['*']) + file_name))[0]
        self.log(file_path)
        # Create SSH connection to CA
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        # Get an signing certificate instead of authentication certificate.
        self.log('SS_30 9b. Get the signing certificate')

        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)

        # Try to import certificate
        self.log('SS_30 9b. Trying to import authentication certificate as signing certificate. Should fail.')
        import_cert(self, local_cert_path)
        self.wait_jquery()

        error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
        self.log('SS_30 9b.1. System displays the error message {0}'.format(messages.SIGN_CERT_INSTEAD_AUTH_CERT))
        self.is_equal(messages.SIGN_CERT_INSTEAD_AUTH_CERT, error_msg)

        self.log('SS_30 9b. Certificate not accepted, test succeeded')

        self.log('SS_30 9b. Remove test data')
        popups.close_all_open_dialogs(self)
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.get_text(keyscertificates_constants.
                                                                                           KEY_LABEL_TEXT)).click()
        # Delete the added key label
        user_input_check.delete_added_key_label(self)

    return fail_test_case


def get_ca_certificate(client, cert, target_path):
    '''
    Saves a certificate from the CA to local machine.
    :param client: SSHClient object
    :param cert: str - certificate filename
    :param target_path: str - target filename (full path)
    :return:
    '''
    sftp = client.get_client().open_sftp()
    sftp.get('/home/ca/CA/certs/' + cert, target_path)
    sftp.close()


def put_file_in_ss(client, local_path, remote_path):
    sftp = client.get_client().open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()


def get_cert(client, service, file_path, local_path, remote_cert_path, remote_csr_path, convert_der=False, close_client=True):
    '''
    Gets the certificate (sign or auth) from the CA.

    NB! This requires the user to have sudo rights without password prompt.
    :param client: SSHClient object
    :param service: str - service type: sign-sign (signing certificates) or sign-auth (authentication certificates)
    :param file_path: str - local CSR path (input)
    :param local_path: str - local certificate path (output)
    :param remote_cert_path: str - remote certificate path (output)
    :param remote_csr_path: str - remote CSR path (input)
    :return: None
    '''
    # Remove temporary files
    client.exec_command('rm temp*')
    sftp = client.get_client().open_sftp()

    # Upload CSR
    sftp.put(file_path, remote_csr_path)

    # Execute signing service and save the output to file
    client.exec_command('cat ' + remote_csr_path + ' | ' + service + ' > ' + remote_cert_path)
    time.sleep(3)

    if convert_der:
        new_cert_path = remote_cert_path.replace('.pem', '.der')
        client.exec_command('openssl x509 -outform der -in {0} -out {1}'.format(remote_cert_path, new_cert_path))
        remote_cert_path = new_cert_path

    # Download certificate
    sftp.get(remote_cert_path, local_path)

    # Close the connection
    sftp.close()
    if close_client:
        client.close()


def revoke_certs(client, certs, ca_path='/home/ca/CA', revoke_script='./revoke.sh'):
    '''
    Revokes specified certificates in CA.
    :param client: SSHClient object
    :param certs: [str]|str - certificate filename or list of filenames to revoke
    :param remote_cert_path: str - base path of the certificates to revoke; will be prepended to filenames
    :param revoke_script: str - revoke script executable
    :return:
    '''
    if not isinstance(certs, list):
        certs = [certs]

    for cert_path in certs:
        # Revoke the certificate
        client.exec_command('cd {0} && {1} {2}'.format(ca_path, revoke_script, cert_path))


def generate_csr(self, client_code, client_class, server_name, client_ss_name=None, check_inputs=False,
                 cancel_key_generation=False,
                 cancel_csr_generation=False, generate_same_csr_twice=False, generate_key=True, key_label=None,
                 log_checker=None):
    """
    Generates the CSR (certificate request) for a client.
    :param self: MainController object
    :param client_code: str - client XRoad code
    :param client_class: str - client XRoad class
    :param server_name: str - X-Road instance
    :param client_ss_name: str - client's security server name
    :param check_inputs: bool - parameter for starting checking user inputs or not
    :return:
    """

    # Generate XRoad ID for the client
    client = ':'.join([server_name, client_class, client_code, '*'])
    if log_checker is not None:
        current_log_lines = log_checker.get_line_count()
    '''Key label'''
    if key_label is None:
        key_label = keyscertificates_constants.KEY_LABEL_TEXT + '_' + client_code + '_' + client_class
    # UC SS_28 4. System verifies entered key label
    if check_inputs:
        user_input_check.parse_key_label_inputs(self)
        user_input_check.parse_csr_inputs(self)

    # Open the keys and certificates tab
    self.log('Open keys and certificates tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()

    if generate_key:
        keys_before = len(
            self.wait_until_visible(type=By.CSS_SELECTOR,
                                    element=keyscertificates_constants.GENERATED_KEYS_TABLE_ROW_CSS,
                                    multiple=True))
        # Generate key from softtoken
        self.log('Click on softtoken row')
        self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_ROW_XPATH).click()
        self.log('Click on "Generate key" button')
        self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATEKEY_BTN_ID).click()

        # UC SS_28 2. System prompts for label.
        self.log('SS_28 2. System prompts for label.')

        # UC SS_28 3a. Key generation is cancelled
        self.log('UC SS_28 3a. Key generation is cancelled')
        if cancel_key_generation:
            # Cancel key generation
            self.log('Click on "Cancel" button')
            self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_CANCEL_BTN_XPATH).click()
            self.wait_jquery()
            # Get number of keys in table after canceling
            self.wait_until_visible(type=By.CSS_SELECTOR,
                                    element=keyscertificates_constants.GENERATED_KEYS_TABLE_ROW_CSS)
            self.wait_jquery()
            keys_after_canceling = len(
                self.wait_until_visible(type=By.CSS_SELECTOR,
                                        element=keyscertificates_constants.GENERATED_KEYS_TABLE_ROW_CSS, multiple=True))
            # Check if number of keys in table is same as before
            self.is_equal(keys_before, keys_after_canceling,
                          msg='Number of keys after cancelling {0} not equal to number of keys before {1}'.format(
                              keys_before, keys_after_canceling))

            # Generate key from softtoken again
            self.log('Click on softtoken row')
            self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_ROW_XPATH).click()
            self.log('Click on "Generate key" button')
            self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATEKEY_BTN_ID).click()

        # UC SS_28 3. Enter key label.
        self.log('SS_28 3. Insert {0} to "LABEL" area'.format(key_label))
        key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
        self.input(key_label_input, key_label)

        # Save the key data
        self.log('Click on "OK" button')
        self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        if log_checker is not None:
            expected_log_msg = GENERATE_KEY
            self.log('SS_28 6. System logs the event "{0}" to the audit log'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            current_log_lines = log_checker.get_line_count()

    # UC SS_28 5. Check if the generated key exists.
    self.log('SS_28 5. Check if the generated key exists.')

    # Click on the key
    self.log('Click on generated key row')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.KEY_TABLE_ROW_BY_LABEL_XPATH.format(key_label)).click()
    # Number of csr before generation and cancelling
    number_of_cert_requests_before = len(
        self.by_css(keyscertificates_constants.CERT_REQUESTS_TABLE_ROW_CSS,
                    multiple=True))

    # UC SS_29 1. Select to generate a CSR for the key
    self.log('SS_29 1. Select to generate a CSR for the key')

    # Generate the CSR from the key.
    self.log('Click on "GENERATE CSR" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATECSR_BTN_ID).click()

    # UC SS_29 4b CSR generation is cancelled
    self.log('UC SS_29 4b CSR generation is cancelled')
    if cancel_csr_generation:
        self.log('Select "certification service"')
        select = Select(self.wait_until_visible(type=By.ID,
                                                element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID))
        self.wait_jquery()

        options = filter(lambda y: str(y) is not '', map(lambda x: x.text, select.options))

        # UC SS_29 2. Check if CA can be chosen
        self.log('SS_29 2. Check 1: CA can be chosen')
        filter(lambda x: self.config.get('ca.name').upper() in x.text, select.options).pop().click()

        self.log('Click on "OK" button')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH).click()
        self.log('Click on "Cancel" button')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_CANCEL_BTN_XPATH).click()

        self.log('Click on "Cancel" button')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_CANCEL_BTN_XPATH).click()
        self.log("Get number of CSR after canceling")
        number_of_cert_requests_after_canceling = len(
            self.by_css(keyscertificates_constants.CERT_REQUESTS_TABLE_ROW_CSS,
                        multiple=True))
        self.is_equal(number_of_cert_requests_before, number_of_cert_requests_after_canceling,
                      msg='Number of cert requests after cancelling {0} not same as before {1}'.format(
                          number_of_cert_requests_after_canceling, number_of_cert_requests_before))

        self.log('Click on "GENERATE CSR" button')
        self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATECSR_BTN_ID).click()

    # Change CSR format
    self.log('Change CSR format')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID))

    # UC SS_29 2. Check if DER and PEM exist in format selection
    self.log('SS_29 2. Check if DER and PEM exist in format selection')
    assert 'DER' in map(lambda x: x.text, select.options)
    assert 'PEM' in map(lambda x: x.text, select.options)
    select.select_by_visible_text('DER')

    # UC SS_29 2. Check that the certification authority can be chosen
    self.log('SS_29 2. Check that the certification authority can be chosen')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID))
    self.wait_jquery()

    options = filter(lambda y: str(y) is not '', map(lambda x: x.text, select.options))
    # Assertion for CA check 1
    assert len(filter(lambda x: self.config.get('ca.name').upper() in x, options)) == 1
    filter(lambda x: self.config.get('ca.name').upper() in x.text, select.options).pop().click()

    # UC SS_29 2. Choose client
    self.log('SS_29 2. Choose client')

    # Select client from the list
    self.log('Select "{0}"'.format(client))
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CLIENT_DROPDOWN_ID))
    select.select_by_visible_text(client)
    self.wait_jquery()

    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # UC SS_29 3. Check CSR fields
    self.log('SS_29 3. Check CSR fields')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_XPATH)

    xroad_harmonized = self.config.get_bool('config.harmonized_environment', False)
    check_field_CN = client_code
    if xroad_harmonized:
        # If we are using X-Road harmonized environment, C=Country Code (FI), O=Organization name (needs to be filled),
        # serial number (name="serialNumber") = XRD1/xroad-lxd-ss0/GOV = instance/server/class, and CN=Member Code (CLIENT1)

        if client_ss_name is not None:
            # UC SS_29 3. Check that the serial number matches
            serial_number = '{0}/{1}/{2}'.format(server_name, client_ss_name, client_code)
            self.log('SS_29 3. Check serial number, look for {0}'.format(serial_number))
            assert self.wait_until_visible(type=By.XPATH,
                                           element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_SERIAL_NUMBER_XPATH).get_attribute(
                'value') == serial_number

        self.log('SS_29 4. Fill organization name field: {0}'.format(client_class))
        o_field = self.wait_until_visible(type=By.XPATH,
                                          element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_O_XPATH)
        self.input(o_field, client_class)
    else:
        # For testing previous versions without harmonized environment
        check_field_C = server_name

        # UC SS_29 3. Check that the instance identifier matches
        self.log('SS_29 3. Check Instance Identifier')
        assert self.wait_until_visible(type=By.XPATH,
                                       element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_C_XPATH).get_attribute(
            'value') == check_field_C

        # UC SS_29 3. Check that the member class matches
        self.log('SS_29 3. Check Member Class')
        assert self.wait_until_visible(type=By.XPATH,
                                       element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_O_XPATH).get_attribute(
            'value') == client_class

    # UC SS_29 3. Check that the member code matches
    self.log('SS_29 3. Check Member Code')
    cn_value = self.wait_until_visible(type=By.XPATH,
                                       element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_CN_XPATH).get_attribute(
        'value')
    self.is_equal(check_field_CN, cn_value)
    self.log('SS_29 3. Client data correct')

    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # UC SS_29 6-8. System verified the info and generates the file.
    self.log('SS_29 6-8, 11. System verified the info and generates the file. File is downloaded to system.')

    if log_checker is not None:
        expected_log_msg = GENERATE_CSR
        self.log('SS_29 9, 10. System logs the event "{0}" to the audit log'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

    self.log('SS_29 7a the token information is already saved in the system configuration')
    if generate_same_csr_twice:
        '''CSR requests in table after first request generation'''
        number_of_cert_requests_after_confirming = len(
            self.by_css(keyscertificates_constants.CERT_REQUESTS_TABLE_ROW_CSS, multiple=True))
        self.is_true(number_of_cert_requests_before < number_of_cert_requests_after_confirming)
        self.log('SS_29 8a the key information is already saved in the system configuration')
        self.log('Check if key usage is set to sign from previous csr generation')
        key_usage = self.wait_until_visible(type=By.XPATH,
                                            element=keys_and_certificates_table.get_generated_key_row_key_usage_xpath(
                                                client_code, client_class)).text
        self.is_equal(keys_and_certificates_table.KEY_USAGE_TYPE_SIGN, key_usage)

        self.log('Generate CSR again')
        generate_csr(self, client_code=client_code, client_class=client_class, server_name=server_name,
                     check_inputs=False, cancel_key_generation=False,
                     cancel_csr_generation=False, generate_same_csr_twice=False, generate_key=False)

        self.log('Check if CSR requests in table is same as before')
        keys_after_another_csr_generation = len(self.wait_until_visible(type=By.CSS_SELECTOR,
                                                                        element=keys_and_certificates_table.CERT_REQUESTS_TABLE_ROW_CSS,
                                                                        multiple=True))
        self.is_equal(number_of_cert_requests_after_confirming, keys_after_another_csr_generation)


def delete_added_key(self, client_code, client_class, cancel_deletion=False, log_checker=None):
    '''
    Delete the CSR from the list.
    :param self: MainController object
    :param client_code: str - client XRoad code
    :param client_class: str - client XRoad class
    :param cancel_deletion: bool|None - cancel deletion before confirming
    :return: None
    '''

    # UC SS_36 Delete a Key from a Software Token
    self.log('*** SS_36 Delete a Key from a Software Token')

    if log_checker is not None:
        '''Current log lines count'''
        current_log_lines = log_checker.get_line_count()
    self.wait_jquery()
    '''Close all open dialogs'''
    popups.close_all_open_dialogs(self)

    # UC SS_36 1. Select to delete a key.
    self.log('SS_36 1. Select to delete a key.')

    '''Open the keys and certificates tab'''
    self.log('Open keys and certificates tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()

    '''Wait until keys and certificates table visible'''
    self.wait_until_visible(type=By.CSS_SELECTOR, element=keys_and_certificates_table.GENERATED_KEYS_TABLE_ROW_CSS)
    '''Find number of keys in table'''
    num_of_keys_before = len(self.by_css(keys_and_certificates_table.GENERATED_KEYS_TABLE_ROW_CSS, multiple=True))

    self.log('Delete added CSR')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.get_generated_key_row_xpath(client_code,
                                                                                           client_class)).click()
    '''Deleting generated key'''
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()

    # UC SS_36 2. System prompts for confirmation
    self.log('SS_36 2. System prompts for confirmation')

    # UC SS_36 3a. Deletion process is cancelled
    self.log('SS_36 3a. Deletion process is cancelled')

    if cancel_deletion:
        '''cancel key deletion'''
        self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()

        '''Find number of keys after canceling deletion'''
        num_of_keys_after_canceling = len(
            self.by_css(keys_and_certificates_table.GENERATED_KEYS_TABLE_ROW_CSS, multiple=True))

        '''Check if the amount of keys is same as before'''
        self.is_equal(num_of_keys_before, num_of_keys_after_canceling,
                      msg='Number of keys after canceling {0} differs, should be {1}'.format(
                          num_of_keys_after_canceling,
                          num_of_keys_before))
        '''delete generated key again'''
        self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()

    # UC SS_36 3. Confirm deletion
    self.log('SS_36 3. Confirm deletion')

    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # UC SS_36 4. Key is deleted from the token
    self.log('SS_36 4. Key is deleted from the token')

    if log_checker is not None:
        expected_log_msg = DELETE_KEY
        self.log('SS_36 5. System logs the event "{0}" to the audit log'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)


def import_cert(self, cert_path):
    '''
    Import certificate to the server.
    :param self: MainController object
    :param cert_path: str - certificate path
    :return: None
    '''

    # UC SS_30 1. Select to import certificate file
    self.log('SS_30 1. Select to import certificate file')

    self.log('Open keys and certificates tab')
    self.driver.get(self.url)
    self.wait_jquery()

    # Go to keys and certificates and click "Import"
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()

    # UC SS_30 2. Select the file from the local file system.
    self.log('SS_30 2. Select the file from the local file system.')

    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.IMPORT_BTN_ID).click()

    # Upload the local file to security server
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.IMPORT_CERTIFICATE_POPUP_XPATH)
    file_abs_path = os.path.abspath(cert_path)
    time.sleep(3)
    file_upload = self.wait_until_visible(type=By.ID, element=popups.FILE_UPLOAD_ID)

    # Fill in the filename
    xroad.fill_upload_input(self, file_upload, file_abs_path)
    time.sleep(1)

    # Start importing and wait until it finishes
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.FILE_IMPORT_OK_BTN_ID).click()
    self.wait_jquery()

    # UC SS_30 3-15 System actions and checks with the certificate
    self.log('SS_30 3-15 System actions and checks with the certificate')


def check_import(self, client_class, client_code):
    '''
    Check if import succeeded. Raises an exception if not.
    :param self: MainController object
    :param client_class: str - client XRoad class
    :param client_code: str - client XRoad code
    :return: None
    '''
    # UC SS_30 13-14. Check if certificate import succeeded
    self.wait_jquery()
    time.sleep(0.5)
    td = self.wait_until_visible(type=By.XPATH,
                                 element=keyscertificates_constants.get_generated_row_row_by_td_text(
                                     ' : '.join([client_class, client_code])))
    tds = td.find_element_by_xpath(".//ancestor::tr").find_elements_by_tag_name('td')
    self.log('SS_30 13-14. Check for OCSP response and status: {0}'.format(
        (str(tds[2].text) == 'good') & (str(tds[4].text) == 'registered')))


def added_client_row(self, client):
    '''
    Get the added client row from the table.
    :param self: MainController object
    :param client: client data
    :return: WebDriverElement - client row
    '''
    self.log('Finding added client')

    self.added_client_id = ' : '.join(
        ['SUBSYSTEM', ssh_server_actions.get_server_name(self), client['class'], client['code'],
         client['subsystem_code']])
    table_rows = self.by_css(clients_table_vm.CLIENT_ROW_CSS, multiple=True)
    client_row_index = clients_table_vm.find_row_by_client(table_rows, client_id=self.added_client_id)
    return table_rows[client_row_index]


def generate_auth_csr(self, ca_name, change_usage=True):
    """
    Generates the CSR (certificate request) for a client.
    :param change_usage: bool - when True changes usage to auth
    :param self: MainController object
    :param ca_name: str - CA display name
    :return:
    """

    # Generate the CSR from the key.
    self.log('Click on "GENERATE CSR" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATECSR_BTN_ID).click()

    self.wait_jquery()
    if change_usage:
        self.log('Change CSR usage')
        select = Select(self.wait_until_visible(type=By.ID,
                                                element=keyscertificates_constants.
                                                GENERATE_CSR_SIGNING_REQUEST_USAGE_DROPDOWN_ID))
        select.select_by_visible_text('Auth')

    # Check that the certification authority can be chosen
    self.log('Select "certification service"')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.
                                            GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID))
    select.select_by_visible_text(ca_name)

    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.
                                            GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID))
    select.select_by_visible_text('DER')

    self.wait_jquery()
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH).click()

    self.wait_jquery()
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH).click()

    self.wait_jquery()


def test_import_cert_global_conf_expired(self, ss_host, ss_username, ss_pass, ss2_client, log_checker):
    """
    Tests adding certificate, when global configuration is expired
    :param self: obj - mainController instance
    :param ss_host: str - security server host
    :param ss_username: str - security server username
    :param ss_pass: str - security server password
    :param ss2_client: dict - security server client info
    :param log_checker: obj - security server log checker instance
    :return:
    """

    def ss_global_conf_expired():
        current_log_lines = log_checker.get_line_count()
        self.log('Opening security server page')
        self.reload_webdriver(url=ss_host, username=ss_username, password=ss_pass)
        self.log('Check if global configuration expired notification is shown')
        self.is_equal(self.by_id('alerts').text, messages.GLOBAL_CONF_EXPIRED_MESSAGE,
                      msg='Global configuration expired notification not shown')
        self.log('Import certificate, expecting error')
        test_generate_csr_and_import_cert(client_code=ss2_client['code'],
                                          client_class=ss2_client['class'],
                                          check_success=False)(self)
        self.wait_jquery()
        self.log('Waiting until error message is visible')
        message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
        expected_error_msg = messages.CERTIFICATE_IMPORT_EXPIRED_GLOBAL_CONF_ERROR
        self.log('SS_30 3a.1 System displays the error message "{0}"'.format(expected_error_msg))
        self.is_equal(expected_error_msg, message)
        expected_log_msg = log_constants.IMPORT_CERTIFICATE_FROM_FILE_FAILED
        self.log('SS_30 3a.2 System logs the event "{0}" in audit log'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found)

    return ss_global_conf_expired


def expire_global_conf(self, sshclient):
    def expire_conf():
        self.log('Stop configuration client service')
        sshclient.exec_command('service xroad-confclient stop', sudo=True)
        self.log('Wait 11 minutes, so the global configuration has expired for sure')
        time.sleep(ss_system_parameters.GLOBAL_CONF_EXPIRATION_TIME_IN_SECONDS)

    return expire_conf


def start_xroad_conf_client(self, sshclient):
    def start_conf_client():
        self.log('Start xroad-confclient service')
        sshclient.exec_command('service xroad-confclient start', sudo=True)
        self.log('Close ssh connection')
        sshclient.close()

    return start_conf_client


def test_generate_key_timed_out(self, ss_host, ss_username, ss_pass, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass):
    def generate_key_timed_out():
        log_checker = auditchecker.AuditChecker(host=ss2_ssh_host, username=ss2_ssh_user, password=ss2_ssh_pass)
        current_log_lines = log_checker.get_line_count()
        self.ssh_client = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        self.log('Open security server page')
        self.reload_webdriver(ss_host, ss_username, ss_pass)
        self.log('Open keys and certificates tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()
        self.log('Click on softtoken row')
        self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_ROW_XPATH).click()
        self.log('Click on "Generate key" button')
        self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATEKEY_BTN_ID).click()
        self.log('Stop xroad signer service')
        self.ssh_client.exec_command(command='service xroad-signer stop', sudo=True)
        self.ssh_client.close()
        self.log('Wait until service has stopped')
        wait_until_server_up(ss_host)
        self.log('Confirm key generation popup')
        self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()
        error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS, timeout=300).text
        self.log('SS_28 5a.1 System displays the error message describing the encountered error')
        try:
            self.is_equal(messages.KEY_GENERATION_TIMEOUT_ERROR, error_msg)
        except AssertionError:
            self.is_equal(messages.SERVER_UNREACHABLE_ERROR, error_msg)
        expected_log_msg = GENERATE_KEY_FAILED
        self.log('SS_28 5a.2 System logs the event "{0}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

    return generate_key_timed_out


def start_xroad_signer_service(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass):
    self = main

    def start_xroad_signer():
        self.ssh_client = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        self.log('Starting xroad signer service')
        self.ssh_client.exec_command(command='service xroad-signer start', sudo=True)
        self.ssh_client.close()

    return start_xroad_signer


def test_generate_csr_timed_out(self, ss_host, ss_username, ss_pass, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass):
    def generate_csr_timed_out():
        self.log('SS_29 6a csr generation fails when token service is unavailable')
        log_checker = auditchecker.AuditChecker(host=ss2_ssh_host, username=ss2_ssh_user, password=ss2_ssh_pass)
        current_log_lines = log_checker.get_line_count()
        self.ssh_client = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        self.log('Open security server page')
        self.reload_webdriver(ss_host, ss_username, ss_pass)
        self.log('Open keys and certificates')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()
        self.log('Click on softtoken row')
        self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_ROW_XPATH).click()
        self.log('Click on "Generate key" button')
        self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATEKEY_BTN_ID).click()
        key_label = 'testKey'
        self.log('Insert ' + key_label + ' to "LABEL" area')
        key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
        self.input(key_label_input, key_label)

        '''Save the key data'''
        self.log('Click on "OK" button')
        self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        self.log('Click on "Generate CSR" button')
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.GENERATECSR_BTN_ID).click()

        self.log('Wait until CSR generation popup is visible')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_XPATH)

        self.log('Select certification authority')
        select = Select(self.wait_until_visible(type=By.ID,
                                                element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID))
        filter(lambda x: self.config.get('ca.name').upper() in x.text, select.options).pop().click()

        self.log('Click "OK"')
        self.by_xpath(keys_and_certificates_table.GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH).click()

        self.log('Stop xroad signer service')
        self.ssh_client.exec_command(command='service xroad-signer stop', sudo=True)
        self.ssh_client.close()

        self.log('Wait until service has stopped')
        wait_until_server_up(ss_host)

        self.log('Click "OK" to start csr generation')
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH).click()

        self.log('Wait until csr generation times out and error is displayed')
        error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS, timeout=300).text
        self.log('SS_29 6a. System displays the error message describing the encountered error')
        try:
            self.is_equal(messages.KEY_GENERATION_TIMEOUT_ERROR, error_msg)
        except AssertionError:
            self.is_equal(messages.SERVER_UNREACHABLE_ERROR, error_msg)
        expected_log_msg = GENERATE_CSR_FAILED
        self.log('SS_29 6a.2 System logs the event "{0}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)
        self.log('SS_29 6a.3a Cancel CSR generation')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.GENERATE_CSR_SIGNING_REQUEST_POPUP_CANCEL_BTN_XPATH).click()

    return generate_csr_timed_out


def delete_added_key_after_service_up(self, ss_host):
    """Deletes currently selected key after checking that server is up"""
    self.log('Wait until server responds')
    wait_until_server_up(ss_host)
    self.log('Click "Delete" button')
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
    self.log('Confirm deletion')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()


def unregister_cert(self, ss2_host, ss2_username, ss2_password, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass,
                    no_valid_cert=False, request_fail=False):
    """
    SS_38 Unregister an Authentication Certificate
    :param self:
    :param ss2_host: security server host
    :param ss2_username: security server username
    :param ss2_password: security server password
    :param ss2_ssh_host: security server ssh host
    :param ss2_ssh_user: security server ssh user
    :param ss2_ssh_pass: security server ssh pass
    :param no_valid_cert: check "no valid auth cert" error
    :param request_fail: check request sending error
    :return:
    """

    def unregister():
        log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        current_log_lines = log_checker.get_line_count()
        self.reload_webdriver(ss2_host, ss2_username, ss2_password)
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.CERT_BY_KEY_LABEL.format('auth')).click()

        self.log('SS_38 1. Unregister button is clicked')
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.UNREGISTER_BTN_ID).click()
        self.log('SS_38 3a. Unregister process is canceled')
        self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        self.log('SS_38 1. Unregister button is clicked')
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.UNREGISTER_BTN_ID).click()
        self.log('SS_38 3. Confirming unregistering confirmation popup')
        popups.confirm_dialog_click(self)

        '''SS_38 4a. There is no valid authentication certificate for the security server'''
        if no_valid_cert:
            expected_msg = messages.UNREGISTER_CERT_FAIL_NO_VALID_CERT
            self.log('SS_38 4a.1 System displays the error message "{0}"'.format(expected_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(expected_msg, error_msg)
            expected_log_msg = log_constants.UNREGISTER_AUTH_CERT_FAILED
            self.log('SS_38 4a.2 System displays the error message "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            return
        if request_fail:
            expected_warning_msg = messages.CERTIFICATE_DELETION_REQUEST_SENDING_FAILED
            expected_error_msg = messages.UNREGISTER_CERT_REQUEST_SENDING_FAILED
            self.log('SS_38 6a.1 System displays the warning message: {0}'.format(expected_warning_msg))
            warning_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.WARNING_MESSAGE_CSS).text
            self.is_equal(expected_warning_msg, warning_msg)
            self.log('SS_38 6a.1 System displays the error message: {0}'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_true(error_msg.startswith(expected_error_msg))
            expected_log_msg = log_constants.UNREGISTER_AUTH_CERT_FAILED
            self.log('SS_38 6a.2 System logs the event {0}'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            current_log_lines = log_checker.get_line_count()
            self.log('SS_38 6a.3a Deletion is canceled')
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CANCEL_XPATH).click()
            self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.UNREGISTER_BTN_ID).click()
            popups.confirm_dialog_click(self)
            self.log('SS_38 6a.3 Deletion is confirmed')
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
            self.log('SS_38 6a.4 System sets the status of the cert to "deletion in progress"')
            self.wait_until_visible(type=By.XPATH,
                                    element=keys_and_certificates_table.DEL_IN_PROGRESS_CERTIFICATE_ROW_XPATH)
            expected_log_msg = log_constants.SKIP_UNREG_OF_AUTH_CERT
            self.log('SS_38 6a.5 System logs the event {0}'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            return
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
        self.log('SS_38 8. System displays the message "{0}"'.format(messages.REQUEST_SENT_NOTICE))
        self.is_equal(messages.REQUEST_SENT_NOTICE, notice_msg)
        self.log('SS_38 9. System sets the registration status to "deletion in progress"')
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.DEL_IN_PROGRESS_CERTIFICATE_ROW_XPATH)
        expected_log_msg = log_constants.UNREGISTER_AUTH_CERT
        self.log('SS_38 10. System logs the event "{0}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

    return unregister


def log_out_token(self):
    def log_out():
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_until_visible(type=By.CLASS_NAME, element='deactivate_token').click()

    return log_out


def log_in_token(self):
    def log_in():
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_until_visible(type=By.CLASS_NAME, element='activate_token').click()
        PIN_input = self.wait_until_visible(type=By.ID, element='activate_token_pin')
        self.input(PIN_input, '1234')
        self.by_xpath('//div[@aria-describedby="activate_token_dialog"]//span[contains(text(), "OK")]').click()

    return log_in


def delete_all_auth_keys(self):
    def delete_auth_certs():
        while True:
            try:
                auth_key = self.by_xpath(keys_and_certificates_table.KEY_TABLE_ROW_BY_LABEL_XPATH.format('auth'))
                auth_key.click()
                self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
                popups.confirm_dialog_click(self)
                self.wait_jquery()
            except:
                return

    return delete_auth_certs


def delete_active_cert(self):
    def del_active():
        certs = self.by_css('.cert-active', multiple=True)
        for cert in certs:
            cert.click()
            self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
            popups.confirm_dialog_click(self)
            self.wait_jquery()

    return del_active


def delete_all_but_one_sign_keys(self):
    def delete_sign_certs():
        sign_keys = self.by_css('.key', multiple=True)
        for sign_key in sign_keys[:-1]:
            sign_key.click()
            self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
            popups.confirm_dialog_click(self)
            self.wait_jquery()

    return delete_sign_certs


def delete_cert(self):
    def del_cert():
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.DEL_IN_PROGRESS_CERTIFICATE_ROW_XPATH).click()
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
        popups.confirm_dialog_click(self)

    return del_cert


def delete_cert_from_key(self, ssh_host, ssh_user, ssh_pass, one_cert=False, auth=False, client_code=None,
                         client_class=None,
                         cancel_deleting=False, only_cert=False):
    """
    SS_39 Delete Certificate from System Configuration
    :param self: mainController instance
    :param ssh_host: ssh host
    :param ssh_user: ssh user
    :param ssh_pass: ssh pass
    :return:
    """

    def del_cert():
        sshclient = ssh_client.SSHClient(ssh_host, ssh_user, ssh_pass)
        time.sleep(120)
        self.log('Get all keys count in system configuration')
        keys_before = get_key_conf_keys_count(sshclient, '.*')
        self.log('Get token count in system configuration')
        token_count = get_key_conf_token_count(sshclient)
        log_checker = auditchecker.AuditChecker(ssh_host, ssh_user, ssh_pass)
        current_log_lines = log_checker.get_line_count()
        if auth:
            self.wait_until_visible(type=By.XPATH,
                                    element=keys_and_certificates_table.DEL_IN_PROGRESS_CERTIFICATE_ROW_XPATH).click()
        elif one_cert:
            self.wait_until_visible(type=By.CSS_SELECTOR, element=keys_and_certificates_table.CERT_ACTIVE_CSS).click()
        elif client_code is not None and client_class is not None:
            self.wait_until_visible(type=By.XPATH,
                                    element=keys_and_certificates_table.get_generated_key_row_cert_xpath(client_code,
                                                                                                         client_class)).click()
        self.log('SS_39 1. Certificate deletion button is pressed')
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
        self.log('SS_39 2. System prompts for confirmation')
        if cancel_deleting:
            self.log('SS_39 3a. Confirmation popup is canceled')
            self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
        self.log('SS_39 3. Confirmation popup is confirmed')
        popups.confirm_dialog_click(self)
        expected_log_msg = log_constants.DELETE_CERT
        self.log('SS_39 5. System logs the event {}'.format(expected_log_msg))
        logs_found = log_checker.check_log(log_constants.DELETE_CERT, from_line=current_log_lines + 1)
        self.is_true(logs_found)
        self.log('Waiting until keyconf updated')
        time.sleep(120)
        self.log('Get all keys count in system configuration')
        keys_after = get_key_conf_keys_count(sshclient, '.*')
        if only_cert:
            self.log(
                'SS_39 4a. The key, which had no more certificates and/or CSR-s is deleted from system configuration')
            self.is_true(keys_after < keys_before)
        elif one_cert:
            self.log('SS_39 4b. The key, the token and cert is deleted from system configuration')
            self.log('Get token count in system configuration')
            token_count_after = get_key_conf_token_count(sshclient)
            self.is_true(token_count_after < token_count)
        else:
            self.log('SS_39 4. Only the cert is deleted from system configuration')
            self.is_equal(keys_before, keys_after)

    return del_cert


def delete_cert_from_ss(self, client, cs_ssh_host, cs_ssh_user, cs_ssh_pass):
    """
    MEMBER_24 Create and Authentication Certificate Deletion Request
    :param self: mainController instance
    :param client: client to delete
    :return:
    """

    def del_cert_from_ss():
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        current_log_lines = log_checker.get_line_count()
        self.log('open added member details')
        global_groups_tests.open_member_details(self, client)
        self.wait_jquery()
        self.log('Open owned servers tab')
        self.by_xpath(cs_security_servers.SERVER_MANAGEMENT_OWNED_SERVERS_TAB).click()
        self.wait_until_visible(type=By.CSS_SELECTOR, element='.open_details').click()
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SECURITYSERVER_AUTH_CERT_TAB_XPATH).click()
        self.wait_jquery()
        self.wait_until_visible(type=By.CSS_SELECTOR,
                                element=cs_security_servers.SECURITYSERVER_AUTH_CERT_ROW_CSS).click()
        self.log('MEMBER_24 1. Auth certificate deletion button is clicked')
        self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITYSERVER_AUTH_CERT_DELETE_BTN_ID).click()
        self.log('MEMBER_24 2. System displays the prefilled auth certificate registration request')
        owner_name = self.wait_until_visible(type=By.ID,
                                             element=cs_security_servers.DELETION_REQUEST_OWNER_NAME_ID).text
        self.is_equal(owner_name, client['name'])
        owner_class = self.wait_until_visible(type=By.ID,
                                              element=cs_security_servers.DELETION_REQUEST_OWNER_CLASS_ID).text
        self.is_equal(owner_class, client['class'])
        owner_code = self.wait_until_visible(type=By.ID,
                                             element=cs_security_servers.DELETION_REQUEST_OWNER_CODE_ID).text
        self.is_equal(owner_code, client['code'])
        server_code = self.wait_until_visible(type=By.ID,
                                              element=cs_security_servers.DELETION_REQUEST_SERVER_CODE_ID).text
        self.is_equal(server_code, client['name'])
        self.log('MEMBER_24 3.a Deletion request creation is canceled')
        self.wait_until_visible(type=By.XPATH, element=cs_security_servers.DELETION_REQUEST_CANCEL_BTN_XPATH).click()
        self.log('MEMBER_24 1. Auth certificate deletion button is clicked')
        self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITYSERVER_AUTH_CERT_DELETE_BTN_ID).click()
        self.log('MEMBER_24 3. Submit button is pressed')
        self.wait_until_visible(type=By.XPATH, element=cs_security_servers.DELETION_REQUEST_SUBMIT_BTN_XPATH).click()
        expected_notice_msg = messages.get_auth_cert_del_req_added_message(client)
        self.log('MEMBER_24 5. System displays the message: {0}'.format(expected_notice_msg))
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
        self.is_equal(expected_notice_msg, notice_msg)
        expected_log_msg = log_constants.DELETE_AUTH_CERT
        self.log('MEMBER_24 6. System logs the event "{}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)

    return del_cert_from_ss
