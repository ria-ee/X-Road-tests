import glob
import os
import sys
import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_client, ssh_server_actions, xroad, login
from view_models import sidebar as sidebar_constants, keys_and_certificates_table as keyscertificates_constants, \
    popups as popups, certification_services, clients_table_vm, messages


def test(client_code, client_class):
    def test_case(self):
        '''
        Test 2.1.3 success scenarios. Failure scenarios are tested in another function.
        :param self: MainController object
        :return: None
        '''

        # TEST PLAN 2.1.3 security server client certification
        # Failure scenarios (2.1.3.1) are tested under failing_tests()
        self.log('*** 2.1.3 / XT-457')

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

        # TEST PLAN 2.1.3-1 generate key for authentication device, and
        # TEST PLAN 2.1.3-2 generate certificate request for the key and save it to local system
        self.log('2.1.3-1, 2.1.3-2 generate key and certificate request using that key')
        generate_csr(self, client_code, client_class, server_name)

        # Get the certificate request path
        file_path = glob.glob(self.get_download_path('_'.join(['*', server_name, client_class, client_code]) + '.der'))[
            0]

        # Create an SSH connection to CA
        client = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                      self.config.get('ca.ssh_pass'))

        # Get the certificate local path
        local_cert_path = self.get_download_path(cert_path)

        # TEST PLAN 2.1.3-3 upload certificate request to CA and get the signing certificate from CA
        self.log('2.1.3-3 upload certificate request to CA and get the siging certificate')
        get_cert(client, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)

        file_cert_path = glob.glob(local_cert_path)[0]

        # TEST PLAN 2.1.3-4 import the certificate to security server
        self.log('2.1.3-4 import certificate to security server')
        import_cert(self, file_cert_path)

        # Check if import succeeded
        self.log('2.1.3-4 check if import succeeded')
        check_import(self, client_class, client_code)

    return test_case


def failing_tests():
    def fail_test_case(self):
        '''
        Tests all failure scenarios of 2.1.3 (2.1.3.1)
        :param self: MainController object
        :return: None
        '''

        # TEST PLAN 2.1.3.1 failure scenarios
        self.log('2.1.3.1 failure scenarios')
        self.log('Adding testing client')
        client = {'name': 'failure', 'class': 'COM', 'code': 'failure', 'subsystem_code': 'failure'}
        try:
            # Add a temporary client for testing the failure scenarios
            add_client(self, client)

            self.log('Waiting 60 seconds for changes')
            time.sleep(60)

            # TEST PLAN 2.1.3.1-1 certificate is issued by a certification authority that is not in the allow list
            not_valid_ca_error(self, client)

            # TEST PLAN 2.1.3.1-2 certificate is not a signing certificate
            wrong_cert_type_error(self, client)

            # TEST PLAN 2.1.3.1-3 key used for requesting the certificate is not found
            no_key_error(self, client)

            # TEST PLAN 2.1.3.1-4 client set in the certificate is not in the system
            no_client_for_certificate_error(self, client)

            # TEST PLAN 2.1.3.1-5 certificate is in a wrong format (not PEM or DER)
            wrong_format_error(self)

            # TEST PLAN 2.1.3.1-6 certificate is already saved in the system
            already_existing_error(self, client)
        except:
            # Exception occured, print traceback
            traceback.print_exc()
        finally:
            # Always remove the temporary client
            remove_client(self, client)

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

    def not_valid_ca_error(self, client):
        '''
        Test for trying to add a certificate that was not issued by a valid certification authority (2.1.3.1-1)
        Expectation: certificate not added.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # TEST PLAN 2.1.3.1-1 certificate is issued by a certification authority that is not in the allow list
        self.log('2.1.3.1-1 certificate is issued by a certification authority that is not in the allow list')
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
            self.log('2.1.3.1-1 Generate CSR for the client')
            generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
            file_path = \
                glob.glob(
                    self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]

            # Create a new SSH connection to CA
            sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                             self.config.get('ca.ssh_pass'))

            # Get the signing certificate from our CSR
            self.log('2.1.3.1-1 Get the signing certificate from the certificate request')
            get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
            time.sleep(6)
            file_cert_path = glob.glob(local_cert_path)[0]

            # Remove CA from central server
            self.log('2.1.3.1-1 Removing ca from central server')

            # Relogin
            self.logout(self.config.get('cs.host'))
            self.login(self.config.get('cs.user'), self.config.get('cs.pass'))

            # Go to certification services in the UI
            self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CERTIFICATION_SERVICES_CSS).click()

            table = self.wait_until_visible(type=By.ID, element=certification_services.CERTIFICATION_SERVICES_TABLE_ID)
            rows = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

            # Find our CA and remove it
            for row in rows:
                if self.config.get('ca.ssh_host') in row.text:
                    row.click()
                    self.wait_until_visible(type=By.ID, element=certification_services.DELETE_BTN_ID).click()
                    popups.confirm_dialog_click(self)

            self.log('Wait 240 seconds for changes')
            time.sleep(240)
            self.log('Reloading page after changes')

            # Reload page and wait until additional data is loaded using jQuery
            self.driver.refresh()
            self.wait_jquery()

            # Try to import the certificate
            self.log('2.1.3.1-1 Trying to import certificate')
            import_cert(self, file_cert_path)
            self.wait_jquery()
            time.sleep(2)

            # Check if we got an error message
            assert messages.get_error_message(self) == messages.CA_NOT_VALID_AS_SERVICE
            self.log('2.1.3.1-1 got correct error message')
        except:
            # Test failed

            self.log('2.1.3.1-1 failed')
            # Print traceback
            traceback.print_exc()
            error = True
        finally:
            # After testing, re-add the CA and restore the state the server was in
            self.log('2.1.3.1-1-del restoring previous state')

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
            self.log('2.1.3.1-1-del Getting CA certificates')
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
                self.log('2.1.3.1-1-del CA not found, re-adding')
                self.wait_until_visible(type=By.ID, element=certification_services.ADD_BTN_ID).click()
                import_cert_btn = self.wait_until_visible(type=By.ID,
                                                          element=certification_services.IMPORT_CA_CERT_BTN_ID)

                # Upload CA certificate and submit the form
                xroad.fill_upload_input(self, import_cert_btn, target_ca_cert_path)

                self.wait_until_visible(type=By.ID, element=certification_services.SUBMIT_CA_CERT_BTN_ID).click()

                # Set CA additional information
                profile_info_area = self.wait_until_visible(type=By.CSS_SELECTOR,
                                                            element=certification_services.CETIFICATE_PROFILE_INFO_AREA_CSS)

                self.input(profile_info_area,
                           'ee.ria.xroad.common.certificateprofile.impl.EjbcaCertificateProfileInfoProvider')

                # Save the settings
                self.wait_until_visible(type=By.ID, element=certification_services.SUBMIT_CA_SETTINGS_BTN_ID).click()
                self.wait_jquery()

                # Open OCSP tab
                self.wait_until_visible(type=By.XPATH, element=certification_services.OCSP_RESPONSE_TAB).click()

                self.log('2.1.3.1-1-del Add OCSP responder')
                self.wait_until_visible(type=By.ID, element=certification_services.OCSP_RESONDER_ADD_BTN_ID).click()

                # Import OCSP certificate
                import_cert_btn = self.wait_until_visible(type=By.ID,
                                                          element=certification_services.IMPORT_OCSP_CERT_BTN_ID)

                xroad.fill_upload_input(self, import_cert_btn, target_ocsp_cert_path)

                url_area = self.wait_until_visible(type=By.ID, element=certification_services.OCS_RESPONSE_URL_AREA_ID)

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

            self.log('Wait 120 seconds for changes')
            time.sleep(120)
            if error:
                # If, at some point, we got an error, fail the test now
                assert False, '2.1.3.1-1 test failed'

    def wrong_cert_type_error(self, client):
        '''
        Test that tries to import a wrong type of certificate to the server. This certificate should not be imported.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # TEST PLAN 2.1.3.1-2 certificate is not a signing certificate

        self.log('2.1.3.1-2 test importing a certificate that is not a signing certificate')
        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        # Set local path for certificate
        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        # Remove temporary files
        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        # Generate CSR for the client
        self.log('2.1.3.1-2 generate CSR for the client')
        generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]

        # Create SSH connection to CA
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        # Get an authentication certificate instead of signing certificate.
        self.log('2.1.3.1-2 get the authentication certificate')
        get_cert(sshclient, 'sign-auth', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        # Try to import certificate
        self.log('2.1.3.1-2 trying to import authentication certificate as signing certificate. Should fail.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)
        assert messages.get_error_message(
            self) == messages.CERTIFICATE_NOT_SIGNING_KEY
        self.log('2.1.3.1-2 certificate not accepted, test succeeded')

        self.log('2.1.3.1-2 remove test data')
        popups.close_all_open_dialogs(self)
        remove_certificate(self, client)

    def no_key_error(self, client):
        '''
        Try to import certificate that does not have a corresponding key in the server. Should fail.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # TEST PLAN 2.1.3.1-3 key used for requesting the certificate is not found
        self.log('2.1.3.1-3 test importing a certificate that does not have a corresponding key')
        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        # Get local certificate path
        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        # Remove temporary files
        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        # Generate CSR
        self.log('2.1.3.1-3 generate CSR for the client')
        generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        # Get the signing certificate from CA
        self.log('2.1.3.1-3 getting signing certificate from the CA')
        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        # Remove the certificate and key from the server
        self.log('2.1.3.1-3 remove the key from the server')
        remove_certificate(self, client)

        # Try to import the certificate that does not have a key any more
        self.log('2.1.3.1-3 try to import the certificate. Should fail.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        assert messages.get_error_message(self) == messages.NO_KEY_FOR_CERTIFICATE
        self.log('2.1.3.1-3 got an error message, test succeeded')

    def no_client_for_certificate_error(self, client):
        '''
        Try to import a certificate that is issued to a non-existing client. Should fail.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # TEST PLAN 2.1.3.1-4 client set in the certificate is not in the system
        self.log('2.1.3.1-4 import a certificate that is issued to a non-existing client.')

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
        self.log('2.1.3.1-4 generate CSR for the client')
        generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]

        # Create an SSH connection to CA
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        # Get the signing certificate from CA
        self.log('2.1.3.1-4 get the signing certificate from CA')
        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        # Remove the test client.
        self.log('2.1.3.1-4 removing test client.')
        remove_client(self, client)

        # Try to import the certificate. Should fail.
        self.log('2.1.3.1-4 import a certificate that is issued to the client that was just removed. Should fail.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        assert messages.NO_CLIENT_FOR_CERTIFICATE in messages.get_error_message(self)
        self.log('2.1.3.1-4 got an error, test succeeded.')

        popups.close_all_open_dialogs(self)

        # Remove the certificate from the server
        self.log('2.1.3.1-4 removing the certificate.')
        remove_certificate(self, client)

        self.driver.get(self.url)
        self.wait_jquery()

        # Restore the client
        self.log('2.1.3.1-4 restoring the client.')
        add_client(self, client)

        # Wait until data updated
        time.sleep(60)

    def wrong_format_error(self):
        '''
        Test importing a certificate that is in a wrong format (not DER/PEM). Should fail.
        :param self: MainController object
        :return: None
        '''

        # TEST PLAN 2.1.3.1-5 try to import a non-DER and non-PEM certificate. Should fail.
        self.log('2.1.3.1-5 trying to import a non-DER and non-PEM certificate')

        self.driver.get(self.url)
        self.wait_jquery()

        # Get a text file
        path = self.get_temp_path('INFO')
        temp_path = glob.glob(path)[0]

        # Try to import the text file as a certificate. Should fail.
        self.log('2.1.3.1-5 trying to import a non-PEM/non-DER file. Should fail.')
        import_cert(self, temp_path)
        self.wait_jquery()
        time.sleep(3)

        assert messages.get_error_message(self) == messages.WRONG_FORMAT_CERTIFICATE
        self.log('2.1.3.1-5 got an error, test succeeded.')

    def already_existing_error(self, client):
        '''
        Test importing a certificate that already exists. Should not be added as a duplicate.
        :param self: MainController object
        :param client: client data
        :return: None
        '''

        # TEST PLAN 2.1.3.1-6 try to import a certificate that has already been added.
        self.log('2.1.3.1-6 try to import a certificate that has already been added.')

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
        self.log('2.1.3.1-6 generate CSR for the client')
        generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]

        # Open an SSH connection to CA
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        # Get the signing certificate from CA
        self.log('2.1.3.1-6 get signing certificate from CA')
        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        # Import the signing certificate. Should succeed.
        self.log('2.1.3.1-6 import the signing certificate.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        # Import the same signing certificate. Should fail.
        self.log('2.1.3.1-6 import the same signing certificate. Should fail.')
        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        assert messages.CERTIFICATE_ALREADY_EXISTS in messages.get_error_message(self)
        self.log('2.1.3.1-6 got an error for duplicate certificate, test succeeded')

        popups.close_all_open_dialogs(self)

        # Remove the certificate
        self.log('2.1.3.1-6 removing the test certificate')
        remove_certificate(self, client)

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


def generate_csr(self, client_code, client_class, server_name):
    '''
    Generates the CSR (certificate request) for a client.
    :param self: MainController object
    :param client_code: str - client XRoad code
    :param client_class: str - client XRoad class
    :param server_name: str - server name
    :return:
    '''

    # Generate XRoad ID for the client
    client = ':'.join([server_name, client_class, client_code, '*'])

    # Open the keys and certificates tab
    self.log('Open keys and certificates tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
    time.sleep(5)
    self.wait_jquery()

    # Generate key from softtoken
    self.log('Click on softtoken row')
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_ROW_XPATH).click()
    self.log('Click on "Generate key" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATEKEY_BTN_ID).click()

    # Enter data (key label)
    self.log(
        'Insert ' + keyscertificates_constants.KEY_LABEL_TEXT + '_' + client_code + '_' + client_class + ' to "LABEL" area')
    key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
    self.input(key_label_input, keyscertificates_constants.KEY_LABEL_TEXT + '_' + client_code + '_' + client_class)

    # Save the key data
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # Key should be generated now. Click on it.
    self.log('Click on generated key row')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.get_generated_key_row_xpath(client_code,
                                                                                           client_class)).click()

    # Generate the CSR from the key.
    self.log('Click on "GENERATE CSR" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATECSR_BTN_ID).click()

    self.log('Change CSR format')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID))

    # TEST PLAN 2.1.3-2 check 2: Check that DER and PEM are in the key list
    assert 'DER' in map(lambda x: x.text, select.options)
    assert 'PEM' in map(lambda x: x.text, select.options)
    self.log('2.1.3-2 check 2 DER and PEM exist in options')
    select.select_by_visible_text('DER')

    # TEST PLAN 2.1.3-2 check 1: Check that the certification authority can be chosen
    self.log('Select "certification service"')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID))
    self.wait_jquery()
    time.sleep(5)
    options = filter(lambda y: str(y) is not '', map(lambda x: x.text, select.options))
    # Assertion for 2.1.3-2 check 1
    assert len(filter(lambda x: self.config.get('ca.ssh_host').upper() in x, options)) == 1
    self.log('2.1.3-2 check 1 CA can be chosen')
    filter(lambda x: self.config.get('ca.ssh_host').upper() in x.text, select.options).pop().click()

    # Select client from the list
    self.log('Select "Client"')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CLIENT_DROPDOWN_ID))
    select.select_by_visible_text(client)
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    self.log('CHECK CSR FIELDS')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_XPATH)

    # TEST PLAN 2.1.3-2 check 3: Check that the instance identifier matches
    self.log('Check Instance Identifier')
    assert self.wait_until_visible(type=By.XPATH,
                                   element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_C_XPATH).get_attribute(
        'value') == server_name

    # TEST PLAN 2.1.3-2 check 3: Check that the member class matches
    self.log('Check Member Class')
    assert self.wait_until_visible(type=By.XPATH,
                                   element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_O_XPATH).get_attribute(
        'value') == client_class

    # TEST PLAN 2.1.3-2 check 3: Check that the member code matches
    self.log('Check Member Code')
    assert self.wait_until_visible(type=By.XPATH,
                                   element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_CN_XPATH).get_attribute(
        'value') == client_code
    self.log('2.1.3-2 check 3 client data correct')

    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()


def delete_added_key(self, client_code, client_class):
    '''
    Delete the CSR from the list.
    :param self: MainController object
    :param client_code: str - client XRoad code
    :param client_class: str - client XRoad class
    :return: None
    '''
    self.log('Delete added CSR')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.get_generated_key_row_xpath(client_code,
                                                                                           client_class)).click()
    # deleting generated key
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()
    # Confirm
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()


def import_cert(self, cert_path):
    '''
    Import certificate to the server.
    :param self: MainController object
    :param cert_path: str - certificate path
    :return: None
    '''

    # TEST PLAN 2.1.3-4 import certificate
    self.log('Open keys and certificates tab')
    self.driver.get(self.url)
    self.wait_jquery()

    # Go to keys and certificates and click "Import"
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
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
    # TEST PLAN 2.1.3-4 check if certificate import succeeded
    self.wait_jquery()
    td = self.wait_until_visible(type=By.XPATH,
                                 element=keyscertificates_constants.get_generated_row_row_by_td_text(
                                     ' : '.join([client_class, client_code])))
    tds = td.find_element_by_xpath(".//ancestor::tr").find_elements_by_tag_name('td')
    self.log('2.1.3-4 check for OCSP response and status: {0}'.format(
        (str(tds[2].text) == 'good') & (str(tds[4].text) == 'registered')))
    assert ((str(tds[2].text) == 'good') & (str(tds[4].text) == 'registered'))


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
