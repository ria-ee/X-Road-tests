# coding=utf-8
import datetime
import glob
import os
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_client, ssh_server_actions, xroad, auditchecker
from tests.xroad_global_groups_tests import global_groups_tests
from tests.xroad_parse_users_inputs.xroad_parse_user_inputs import parse_csr_inputs, parse_key_label_inputs
from view_models import sidebar, keys_and_certificates_table as keyscertificates_constants, \
    popups as popups, clients_table_vm, messages, keys_and_certificates_table, log_constants, cs_security_servers


def test_generate_csr_and_import_cert(client_code, client_class, check_inputs=False, check_success=True,
                                      ss2_ssh_host=None, ss2_ssh_user=None, ss2_ssh_pass=None,
                                      delete_csr_before_import=False):
    def test_case(self):

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

        # Generate key for authentication device and generate certificate request for the key and save it to local system
        self.log('Generate key and certificate request using that key')
        log_checker = None
        if ss2_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
            current_log_lines = log_checker.get_line_count()
        generate_csr(self, client_code, client_class, server_name, check_inputs=check_inputs,
                     cancel_key_generation=True,
                     cancel_csr_generation=True,
                     generate_same_csr_twice=True,
                     log_checker=log_checker)

        # '''SS_30 15a No CSR notice corresponding to imported cert exist in system configuration'''
        # if delete_csr_before_import:
        #     self.log('SS_30 15a No CSR notice corresponding to imported cert exist in system configuration')
        #     delete_csr(self, client_code, client_class, log_checker)

        # Get the certificate request path
        file_path = glob.glob(self.get_download_path('_'.join(['*', server_name, client_class, client_code]) + '.der'))[
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
            # Check if import succeeded
            if log_checker is not None:
                time.sleep(5)
                self.log('SS_30 16. System logs the event "Import certificate from file" to the audit log')
                log_check = log_checker.check_log(log_constants.IMPORT_CERTIFICATE_FROM_FILE,
                                                  from_line=current_log_lines + 1, strict=False)
                self.is_true(log_check)
            self.log('SS_30 16. Check if import succeeded')
            check_import(self, client_class, client_code)

    return test_case


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
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        self.wait_until_visible(type=By.XPATH, element="//span[contains(.,'auth')]").click()

        self.log('Generate new auth certificate for the key')
        generate_auth_csr(self, ca_name=ca_ssh_host, change_usage=False)
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
                        cs_ssh_pass):
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
    self.wait_until_visible(type=By.CSS_SELECTOR, element='.open_details').click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element='//*[@href="#server_auth_certs_tab"]').click()
    self.log('MEMBER_23 1. Add authentication cert button is clicked')
    self.wait_until_visible(type=By.ID, element='securityserver_authcert_add').click()
    self.log('MEMBER_23 3. Authentication cert is uploaded from local filesystem')
    upload = self.wait_until_visible(type=By.ID, element='securityserver_auth_cert_upload_button')
    local_cert_path = self.get_download_path(cert_path)
    file_abs_path = os.path.abspath(local_cert_path)
    xroad.fill_upload_input(self, upload, file_abs_path)
    self.wait_jquery()
    expected_msg = messages.CERTIFICATE_IMPORT_SUCCESSFUL
    self.log('MEMBER_23 4. System displays the message {0}'.format(expected_msg))
    import_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
    self.is_equal(expected_msg, import_msg)
    self.log('Submit authentication cert button is pressed')
    self.wait_until_visible(type=By.ID, element='auth_cert_add_submit').click()
    self.wait_jquery()
    expected_msg = messages.get_cert_adding_existing_server_req_added_notice(client)
    self.log('MEMBER_23 7. System displays the message {0}'.format(expected_msg))
    import_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
    self.is_equal(expected_msg, import_msg)
    expected_log_msg = log_constants.ADD_AUTH_CERTIFICATE_FOR_SECURITY_SERVER
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

    self.log('SS_32 Activate a Certificate')
    '''Security server log checker instance'''
    log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
    '''Security server SSH client instance'''
    sshclient = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
    '''Open keys and certificates view'''
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    '''Current log lines'''
    current_log_lines = log_checker.get_line_count()
    self.log('Wait until keyconf is updated')

    '''Get disabled cert xpath'''
    registration_in_progress_row2 = self.wait_until_visible(type=By.XPATH,
                                                            element=keys_and_certificates_table.OCSP_DISABLED_CERT_ROW2)
    '''Get test of disabled cert'''
    current_cert_row = registration_in_progress_row2.text

    '''Split row to get certificate number'''
    splitted_row = current_cert_row.split()

    authkey_number = splitted_row[0] + " " + splitted_row[1]

    '''Generate new xpath for row'''
    xpath_cert_row = keys_and_certificates_table.get_cert_row(authkey_number)

    registration_in_progress_row = self.wait_until_visible(type=By.XPATH,
                                                           element=xpath_cert_row)

    '''Click on the certificate'''
    registration_in_progress_row.click()

    # self.log('SS_32 1. "Activate a certificate" button is clicked')
    time.sleep(1)
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.ACTIVATE_BTN_ID).click()

    self.log('Hard refresh server OCSP')
    ssh_server_actions.refresh_ocsp(sshclient)

    return xpath_cert_row


def check_import_fail_log(self, log_checker, current_log_lines, step):
    self.log('SS_30 {0} System logs the event "{1}" to the audit log. '.format(step,
                                                                               log_constants.IMPORT_CERTIFICATE_FROM_FILE_FAILED))
    fail_log_present = log_checker.check_log(log_constants.IMPORT_CERTIFICATE_FROM_FILE_FAILED,
                                             from_line=current_log_lines + 1, strict=False)
    self.is_true(fail_log_present)
    return log_checker.get_line_count()


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


def get_cert(client, service, file_path, local_path, remote_cert_path, remote_csr_path):
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

    # Download certificate
    sftp.get(remote_cert_path, local_path)

    # Close the connection
    sftp.close()
    client.close()


def generate_csr(self, client_code, client_class, server_name, check_inputs=False, cancel_key_generation=False,
                 cancel_csr_generation=False, generate_same_csr_twice=False, generate_key=True, log_checker=None):
    """
    Generates the CSR (certificate request) for a client.
    :param self: MainController object
    :param client_code: str - client XRoad code
    :param client_class: str - client XRoad class
    :param server_name: str - server name
    :param check_inputs: bool - parameter for starting checking user inputs or not
    :return:
    """

    # Generate XRoad ID for the client
    client = ':'.join([server_name, client_class, client_code, '*'])
    if log_checker is not None:
        current_log_lines = log_checker.get_line_count()
    '''Key label'''
    key_label = keyscertificates_constants.KEY_LABEL_TEXT + '_' + client_code + '_' + client_class
    # SS_28 4. System verifies entered key label
    if check_inputs:
        parse_key_label_inputs(self)
        parse_csr_inputs(self)

    # Open the keys and certificates tab
    self.log('Open keys and certificates tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
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

        # UC SS_28 3a key generation is cancelled
        self.log('UC SS_28 3a key generation is cancelled')
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

        self.log(
            'Insert ' + key_label + ' to "LABEL" area')
        key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
        self.input(key_label_input, key_label)

        # Save the key data
        self.log('Click on "OK" button')
        self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
        '''SS_28 6 System logs the event "Generate key" to the audit log'''
        if log_checker is not None:
            self.log('SS_28 6 System logs the event "Generate key" to the audit log')
            logs_found = log_checker.check_log(log_constants.GENERATE_KEY, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                             log_constants.GENERATE_KEY,
                             log_checker.found_lines))
            current_log_lines = log_checker.get_line_count()

    # Key should be generated now. Click on it.
    self.log('Click on generated key row')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.get_generated_key_row_xpath(client_code,
                                                                                           client_class)).click()
    # Number of csr before generation and cancelling
    number_of_cert_requests_before = len(
        self.by_css(keyscertificates_constants.CERT_REQUESTS_TABLE_ROW_CSS,
                    multiple=True))
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
        filter(lambda x: self.config.get('ca.ssh_host').upper() in x.text, select.options).pop().click()

        self.log('Click on "OK" button')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH).click()
        self.log('Click on "Cancel" button')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_CANCEL_BTN_XPATH).click()

        self.log('Click on "Cancel" button')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_CANCEL_BTN_XPATH).click()
        self.log("Get number of csr after canceling")
        number_of_cert_requests_after_canceling = len(
            self.by_css(keyscertificates_constants.CERT_REQUESTS_TABLE_ROW_CSS,
                        multiple=True))
        self.is_equal(number_of_cert_requests_before, number_of_cert_requests_after_canceling,
                      msg='Number of cert requests after cancelling {0} not same as before {1}'.format(
                          number_of_cert_requests_after_canceling, number_of_cert_requests_before))

        self.log('Click on "GENERATE CSR" button')
        self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATECSR_BTN_ID).click()

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
    assert len(filter(lambda x: self.config.get('ca.ssh_host').upper() in x, options)) == 1
    filter(lambda x: self.config.get('ca.ssh_host').upper() in x.text, select.options).pop().click()

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

    # UC SS_29 3. Check that the instance identifier matches
    self.log('SS_29 3. Check Instance Identifier')
    assert self.wait_until_visible(type=By.XPATH,
                                   element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_C_XPATH).get_attribute(
        'value') == server_name

    # UC SS_29 3. Check that the member class matches
    self.log('SS_29 3. Check Member Class')
    assert self.wait_until_visible(type=By.XPATH,
                                   element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_O_XPATH).get_attribute(
        'value') == client_class

    # UC SS_29 3. Check that the member code matches
    self.log('SS_29 3. Check Member Code')
    assert self.wait_until_visible(type=By.XPATH,
                                   element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_CN_XPATH).get_attribute(
        'value') == client_code
    self.log('SS_29 3. Client data correct')

    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    '''SS_29 10 System logs the event "Generate CSR" to the audit log'''
    if log_checker is not None:
        self.log('SS_28 6 System logs the event "Generate CSR" to the audit log')
        logs_found = log_checker.check_log(log_constants.GENERATE_CSR, from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         log_constants.GENERATE_CSR,
                         log_checker.found_lines))

    '''SS_29 7a the token information is already saved in the system configuration'''
    self.log('SS_29 7a the token information is already saved in the system configuration')
    if generate_same_csr_twice:
        '''SS_29 8a the key information is already saved in the system configuration'''

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
        generate_csr(self, client_code, client_class, server_name, check_inputs=False, cancel_key_generation=False,
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
    if log_checker is not None:
        '''Current log lines count'''
        current_log_lines = log_checker.get_line_count()
    self.wait_jquery()
    '''Close all open dialogs'''
    popups.close_all_open_dialogs(self)

    '''Open the keys and certificates tab'''
    self.log('Open keys and certificates tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
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

    '''UC SS_36 3a deletion process is cancelled'''
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

    '''Confirm'''
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()

    self.wait_jquery()
    '''SS_36 5 System logs the event "Delete key from token" to the audit log'''
    if log_checker is not None:
        self.log('SS_36 5 System logs the event "Delete key from token" to the audit log')
        logs_found = log_checker.check_log(log_constants.DELETE_KEY, from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                         log_constants.DELETE_KEY,
                         log_checker.found_lines))


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
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
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
        time.sleep(5)
        current_log_lines = log_checker.get_line_count()
        self.reload_webdriver(ss2_host, ss2_username, ss2_password)
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
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


def no_connection_test(self, registration_in_progress_row):
    '''Click "Keys and Certificates" button" '''
    self.log('Click "Keys and Certificates" button"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()

    '''Get certificate xpath'''
    cert_row = self.wait_until_visible(type=By.XPATH,
                                       element=registration_in_progress_row)
    '''Click on certificate row'''
    cert_row.click()

    self.log('SS_42 Unregister button is clicked')
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.UNREGISTER_BTN_ID).click()
    self.log('SS_42 Confirming unregistering confirmation popup')
    popups.confirm_dialog_click(self)

    '''Error message to compare'''
    expected_error_msg = messages.UNREGISTER_CERT_REQUEST_SENDING_FAILED
    '''Get error message'''
    self.log('SS_42 3. The response was an error message.')
    error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
    '''Compare messages'''
    self.is_true(error_msg.startswith(expected_error_msg))

    '''Click conitnue'''
    self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()


    self.log('SS_42 4. System sets the registration status of the authentication certificate to “deletion in progress”.')
    self.log('Click "Deletion in progress" and delete cert')

    deletion_progress = self.wait_until_visible(type=By.XPATH,
                            element=keys_and_certificates_table.DEL_IN_PROGRESS_CERTIFICATE_ROW_XPATH).is_enabled()

    self.log('"Deletion in progress" button verification"')
    self.is_true(deletion_progress,
                 msg='Status "Deletion in progress" not found')



    self.log('SS_42 4. click "Deletion in progress" and delete cert')

    self.wait_until_visible(type=By.XPATH,
                            element=keys_and_certificates_table.DEL_IN_PROGRESS_CERTIFICATE_ROW_XPATH).click()
    '''Click Delete'''
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()

    '''Confirm delete'''
    popups.confirm_dialog_click(self)


def test_disable_wsdl(case, ssh_host=None, ssh_username=None, ssh_password=None, client=None, wsdl_url=None):
    self = case

    def disable_wsdl():
        clients = xroad.split_xroad_subsystem(client)
        '''Find the WSDL, expand it and select service '''
        clients_table_vm.open_client_popup_services(self, client=clients)

        # Find the service under the specified WSDL in service list
        wsdl_element = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=None,
                                                                          wsdl_url=wsdl_url)

        self.by_id(popups.CLIENT_DETAILS_POPUP_DISABLE_WSDL_BTN_ID).click()
        # Wait until the "Disable WSDL" dialog opens.
        self.wait_until_visible(popups.DISABLE_WSDL_POPUP_XPATH, type=By.XPATH)  # Get the OK button
        disable_dialog_ok_button = self.by_xpath(popups.DISABLE_WSDL_POPUP_OK_BTN_XPATH)

        # Get the disabled notice input.
        disable_notice_input = self.by_id(popups.DISABLE_WSDL_POPUP_NOTICE_ID)
        # Click "OK" button to save the data
        disable_dialog_ok_button.click()
        self.wait_jquery()
        time.sleep(2)
        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        wsdl_element = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=None,
                                                                          wsdl_url=wsdl_url)
        '''Get wsdl row text'''
        wsdl_text = wsdl_element.find_elements_by_tag_name('td')[1].text
        '''Check wsdl disabled matches'''
        wsdl_disabled = re.match(popups.CLIENT_DETAILS_POPUP_WSDL_URL_REGEX, wsdl_text)

        '''Verify wsdl is disabled'''
        self.is_true(wsdl_disabled,
                     msg='wsdl is not disabled')

    return disable_wsdl


def test_enable_wsdl(case, ssh_host=None, ssh_username=None, ssh_password=None, client=None, wsdl_url=None):
    self = case

    def enable_wsdl():
        clients = xroad.split_xroad_subsystem(client)
        '''Find the WSDL, expand it and select service '''
        clients_table_vm.open_client_popup_services(self, client=clients)

        # Find the service under the specified WSDL in service list
        wsdl_element = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=None,
                                                                          wsdl_url=wsdl_url)

        # Find and click the "Enable" button to enable the WSDL.
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()

        self.wait_jquery()
        '''Wait wsdl row to load'''
        time.sleep(2)

        # Find the WSDL row and check if it has class 'disabled'. If it does, it is not enabled. If not, everything worked.
        wsdl_element = clients_table_vm.client_services_popup_select_wsdl(self, wsdl_index=None,
                                                                          wsdl_url=wsdl_url)
        '''Get wsdl row text'''
        wsdl_text = wsdl_element.find_elements_by_tag_name('td')[1].text
        '''Check disabled not on wsdl row'''
        wsdl_is_enabled = 'disabled' not in wsdl_text

        '''Verify wsdl is enabled'''
        self.is_true(wsdl_is_enabled,
                     msg='wsdl is not enabled')

    return enable_wsdl


def wsdl_disabled_error_test(self, registration_in_progress_row):
    '''Click "Keys and Certificates" button" '''
    self.log('Click "Keys and Certificates" button"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()

    '''Get certificate xpath'''
    cert_row = self.wait_until_visible(type=By.XPATH,
                                       element=registration_in_progress_row)
    '''Click on certificate row'''
    cert_row.click()

    self.log('SS_42 Unregister button is clicked')
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.UNREGISTER_BTN_ID).click()
    self.log('SS_42 Confirming unregistering confirmation popup')
    popups.confirm_dialog_click(self)
    '''Error message to compare'''
    self.log('UC SS_42 1-2a. The creating or sending of the deletion request failed.')
    error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
    if messages.AUTHCERT_DELETION_DISABLED not in error_msg:
        raise Exception('Services/authCertDeletion is no disabled')

    '''Click continue'''
    self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()

    self.log('SS_42 4. System sets the registration status of the authentication certificate to “deletion in progress”.')
    self.log('Click "Deletion in progress" and delete cert')

    deletion_progress = self.wait_until_visible(type=By.XPATH,
                            element=keys_and_certificates_table.DEL_IN_PROGRESS_CERTIFICATE_ROW_XPATH).is_enabled()

    self.log('"Deletion in progress" button verification"')
    self.is_true(deletion_progress,
                 msg='Status "Deletion in progress" not found')


    '''Waiting for deletion in progress row'''
    self.wait_until_visible(type=By.XPATH,
                            element=keys_and_certificates_table.DEL_IN_PROGRESS_CERTIFICATE_ROW_XPATH).click()
    '''Click Delete button'''
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
    '''Confirm Delete'''
    popups.confirm_dialog_click(self)
