# coding=utf-8
import datetime
import glob
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_client, ssh_server_actions, xroad, auditchecker
from tests.xroad_parse_users_inputs.xroad_parse_user_inputs import parse_csr_inputs, parse_key_label_inputs
from view_models import sidebar, keys_and_certificates_table as keyscertificates_constants, \
    popups as popups, clients_table_vm, messages, keys_and_certificates_table, log_constants, cs_security_servers
from selenium.common.exceptions import ElementNotVisibleException
from view_models import sidebar, keys_and_certificates_table as keyscertificates_constants, \
    popups as popups, clients_table_vm, messages, keys_and_certificates_table, log_constants, cs_security_servers
from view_models.keys_and_certificates_table import SUBJECT_DISTINGUISHED_NAME_POPUP_O_XPATH

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

        # UC SS_30. Import the certificate to security server
        self.log('SS_30. Import certificate to security server')
        import_cert(self, file_cert_path)

        if check_success:
            # Check if import succeeded
            if log_checker is not None:
                time.sleep(5)
                self.log('SS_30 16. System logs the event "Import certificate from file" to the audit log')
                log_check = log_checker.check_log(log_constants.IMPORT_CERTIFICATE_FROM_FILE,
                                                  from_line=current_log_lines + 1, strict=False)
                self.is_true(log_check)
            self.log('SS_30. Check if import succeeded')
            check_import(self, client_class, client_code)

    return test_case


def register_cert(self, ssh_host, ssh_user, ssh_pass, client, ca_ssh_host, ca_ssh_user, ca_ssh_pass, cert_path,
                  check_inputs=False, ca_name=None):
    """
    SS_34 Register an Authentication Certificate
    :param cert_path:
    :param ca_ssh_pass:
    :param ca_ssh_user:
    :param ca_ssh_host:
    :param client:
    :param self: MainController instance
    :param ssh_host: ssh host of the security server
    :param ssh_user: ssh user of the security server
    :param ssh_pass: ssh password of the security server
    :param check_inputs: bool|False: checking input parsing
    :return:
    """

    def register():

        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        '''Click on Token row'''
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.HARDTOKEN_TABLE_ROW_XPATH4).click()
        self.wait_jquery()
        self.log('Verify that "Generate key" button is disabled')
        '''Verify that "Generate key" button is disabled'''
        self.wait_until_visible(
            self.by_id(keys_and_certificates_table.GENERATEKEY_BTN_ID)).click()

        self.log(
            'Insert delete to "LABEL" area')
        key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
        self.input(key_label_input, 'delete')

        '''Save the key data'''
        self.log('Click on "OK" button')
        self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        self.log('Generate new auth certificate for the key')
        generate_auth_csr(self, ca_name=ca_name, organization='o', change_usage=False)
        '''Current time'''
        now_date = datetime.datetime.now()
        '''Downloaded csr file name'''

        file_name = 'sign_csr_' + now_date.strftime('%Y%m%d') + '_member_{0}_{1}_{2}.der'. \
            format(client['instance'], client['class'], client['code'])
        '''Downloaded csr file path'''
        file_path = glob.glob(self.get_download_path('_'.join(['*']) + file_name))[0]
        '''SSH client instance for ca'''

        sshclient = ssh_server_actions.get_client(ca_ssh_host, ca_ssh_user, ca_ssh_pass)
        '''Remote csr path'''
        remote_csr_path = 'temp.der'
        '''Local cert path'''
        local_cert_path = self.get_download_path(cert_path)
        self.log('Getting certificate from ca')
        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)

        import_cert(self, local_cert_path)

        self.wait_jquery()
        time.sleep(3)
        self.wait_until_visible(type=By.XPATH,
                                element=keys_and_certificates_table.HARD_TOKEN_CERT_BY_KEY_LABEL.format(
                                    'delete')).click()

        self.wait_jquery()

    return register


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
    # UC SS_28 4. System verifies entered key label
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
        filter(lambda x: self.config.get('ca.ssh_host').upper() in x.text.upper(), select.options).pop().click()

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
    filter(lambda x: self.config.get('ca.ssh_host').upper() in x.text.upper(), select.options).pop().click()

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
    self.log('CHECK CSR FIELDS')
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


def generate_auth_csr(self, ca_name, organization='o', change_usage=True):
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
    select.select_by_visible_text('Xroad Test CA CN')

    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.
                                            GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID))
    select.select_by_visible_text('DER')

    self.wait_jquery()
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH).click()

    self.wait_jquery()

    self.wait_jquery()
    if organization:
        organization_input = self.wait_until_visible(type=By.XPATH, element=SUBJECT_DISTINGUISHED_NAME_POPUP_O_XPATH)
        self.input(organization_input, organization)

    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH).click()

    self.wait_jquery()



def delete_cert(self, ssh_host, ssh_user, ssh_pass):
    log_checker = auditchecker.AuditChecker(ssh_host, ssh_user, ssh_pass)
    current_log_lines = log_checker.get_line_count()

    self.log('SS_40 1. SS administrator selects to delete a certificate from a hardware token.')
    '''Click Delete'''
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
    self.wait_jquery()
    self.log('SS_40 2. System prompts for confirmation.')
    self.log('SS_40 3a. SS administrator terminates the use case.')

    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
    self.wait_jquery()

    '''Click delete button'''
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
    self.wait_jquery()

    self.log('SS_40 3. SS administrator confirms.')
    '''Confirm delete'''
    popups.confirm_dialog_click(self)
    self.wait_jquery()

    self.log('SS_40 4. System deletes the certificate from the token.')

    '''Verify Token key deletion'''
    try:
        element = self.driver.find_element_by_xpath(keys_and_certificates_table.HARD_TOKEN_CERT_BY_KEY_LABEL.format('delete'))
        if element.is_displayed():
            raise RuntimeError('Token certificate is not deleted')
    except ElementNotVisibleException:
        pass

    expected_log_msg = log_constants.DELETE_CERT
    self.log('SS_40 5. System logs the event {}'.format(expected_log_msg))
    logs_found = log_checker.check_log(log_constants.DELETE_CERT, from_line=current_log_lines + 1)
    self.is_true(logs_found)

    '''Delete token key'''
    '''Click on key'''
    self.wait_until_visible(type=By.XPATH,
                            element=keys_and_certificates_table.KEY_TABLE_ROW_BY_LABEL_XPATH.format(
                                'delete')).click()
    '''Click delete button'''
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
    self.wait_jquery()

    '''Confirm delete'''
    popups.confirm_dialog_click(self)
    self.wait_jquery()