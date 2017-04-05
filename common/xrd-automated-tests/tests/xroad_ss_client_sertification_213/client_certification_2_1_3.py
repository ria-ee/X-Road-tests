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
        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        server_name = ssh_server_actions.get_server_name(self)

        path_wildcard = self.get_download_path('*')

        for fpath in glob.glob(path_wildcard):
            try:
                os.remove(fpath)
            except:
                pass

        generate_csr(self, client_code, client_class, server_name)

        file_path = glob.glob(self.get_download_path('_'.join(['*', server_name, client_class, client_code]) + '.der'))[
            0]

        client = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                      self.config.get('ca.ssh_pass'))

        local_cert_path = self.get_download_path(cert_path)

        get_cert(client, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)

        file_cert_path = glob.glob(local_cert_path)[0]

        import_cert(self, file_cert_path)
        check_import(self, client_class, client_code)

    return test_case


def failing_tests():
    def fail_test_case(self):
        self.log('FAILURES FOR CREATING CERTIFICATES')
        self.log('Adding testing client')
        client = {'name': 'failure', 'class': 'COM', 'code': 'failure', 'subsystem_code': 'failure'}
        try:

            add_client(self, client)
            self.log('Waiting 60 for changes')
            time.sleep(60)

            not_valid_ca_error(self, client)
            wrong_cert_type_error(self, client)
            no_key_error(self, client)
            no_client_for_certificate_error(self, client)
            wrong_format_error(self)
            already_existing_error(self, client)
        except:
            traceback.print_exc()
        finally:
            remove_client(self, client)

    def add_client(self, client):

        self.driver.get(self.url)
        self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

        self.log('Select ' + client['class'] + ' from "CLIENT CLASS" dropdown')
        member_class = Select(
            self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID))
        member_class.select_by_visible_text(client['class'])

        self.log('Insert ' + client['code'] + ' into "CLIENT CODE" area')
        member_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
        # member_code.send_keys(client['code'])
        self.input(member_code, client['code'])

        self.log('Insert ' + client['subsystem_code'] + ' into "SUBSYSTEM CODE" area')
        member_sub_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_ID)
        # member_sub_code.send_keys(client['subsystem_code'])
        self.input(member_sub_code, client['subsystem_code'])

        self.log('Click "OK" to add client')
        self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
        try:
            if self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP):
                self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        except:
            self.log('no warning')
        self.wait_jquery()
        time.sleep(2)
        popups.confirm_dialog_click(self)

    def remove_client(self, client):
        self.log('removing client')
        self.driver.get(self.url)
        self.wait_jquery()
        client_row = added_client_row(self, client)
        client_row.find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS).click()
        try:
            self.log('Unregister button')
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
            self.wait_jquery()
            self.log('Confirm unregistering')
            popups.confirm_dialog_click(self)
            self.wait_jquery()
            time.sleep(3)
            self.log('Confirm deleting')
            popups.confirm_dialog_click(self)
        except:
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
            self.wait_jquery()
            popups.confirm_dialog_click(self)

    def remove_certificate(self, client):
        self.log('REMOVE CERTIFICATE')
        self.log('Click on generated key row')
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.get_generated_key_row_xpath(client['code'],
                                                                                               client[
                                                                                                   'class'])).click()
        self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()
        popups.confirm_dialog_click(self)

    def not_valid_ca_error(self, client):
        error = False
        try:
            remote_csr_path = 'temp.der'
            cert_path = 'temp.pem'

            local_cert_path = self.get_download_path(cert_path)

            server_name = ssh_server_actions.get_server_name(self)
            for fpath in glob.glob(self.get_download_path('*')):
                os.remove(fpath)
            generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
            file_path = \
                glob.glob(
                    self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]
            sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                             self.config.get('ca.ssh_pass'))

            get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
            time.sleep(6)
            file_cert_path = glob.glob(local_cert_path)[0]

            # # remove ca
            self.log('Removing ca from central server')
            self.logout(self.config.get('cs.host'))
            self.login(self.config.get('cs.user'), self.config.get('cs.pass'))

            self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CERTIFICATION_SERVICES_CSS).click()

            table = self.wait_until_visible(type=By.ID, element=certification_services.CERTIFICATION_SERVICES_TABLE_ID)
            rows = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

            for row in rows:
                if self.config.get('ca.ssh_host') in row.text:
                    row.click()
                    self.wait_until_visible(type=By.ID, element=certification_services.DELETE_BTN_ID).click()
                    popups.confirm_dialog_click(self)

            self.log('Wait 240 seconds for changes ')
            time.sleep(240)
            self.log('waiting over')
            self.driver.refresh()
            self.wait_jquery()
            import_cert(self, file_cert_path)
            self.wait_jquery()
            time.sleep(2)

            assert messages.get_error_message(self) == messages.CA_NOT_VALID_AS_SERVICE
        except:
            traceback.print_exc(file=sys.stdout)
            error = True
        finally:
            # # Add CA
            self.log('Add CA to central server')

            self.driver.get(self.config.get('cs.host'))

            if not login.check_login(self, self.config.get('cs.user')):
                self.login(self.config.get('cs.user'), self.config.get('cs.pass'))

            sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'),
                                             self.config.get('ca.ssh_user'),
                                             self.config.get('ca.ssh_pass'))

            target_ca_cert_path = self.get_download_path("ca.pem")
            target_ocsp_cert_path = self.get_download_path("ocsp.pem")
            get_ca_certificate(sshclient, 'ca.cert.pem', target_ca_cert_path)
            get_ca_certificate(sshclient, 'ocsp.cert.pem', target_ocsp_cert_path)
            sshclient.close()

            self.driver.get(self.config.get('cs.host'))

            self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CERTIFICATION_SERVICES_CSS).click()
            self.wait_jquery()
            time.sleep(3)

            table = self.wait_until_visible(type=By.ID, element=certification_services.CERTIFICATION_SERVICES_TABLE_ID)
            rows = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

            if self.config.get('ca.ssh_host') not in map(lambda x: x.text, rows):
                self.wait_until_visible(type=By.ID, element=certification_services.ADD_BTN_ID).click()
                import_cert_btn = self.wait_until_visible(type=By.ID,
                                                          element=certification_services.IMPORT_CA_CERT_BTN_ID)

                xroad.fill_upload_input(self, import_cert_btn, target_ca_cert_path)

                self.wait_until_visible(type=By.ID, element=certification_services.SUBMIT_CA_CERT_BTN_ID).click()

                profile_info_area = self.wait_until_visible(type=By.CSS_SELECTOR,
                                                            element=certification_services.CETIFICATE_PROFILE_INFO_AREA_CSS)

                self.input(profile_info_area,
                           'ee.ria.xroad.common.certificateprofile.impl.EjbcaCertificateProfileInfoProvider')

                self.wait_until_visible(type=By.ID, element=certification_services.SUBMIT_CA_SETTINGS_BTN_ID).click()
                self.wait_jquery()
                self.wait_until_visible(type=By.XPATH, element=certification_services.OCSP_RESPONSE_TAB).click()

                self.log('Add OCSP responder')
                self.wait_until_visible(type=By.ID, element=certification_services.OCSP_RESONDER_ADD_BTN_ID).click()

                import_cert_btn = self.wait_until_visible(type=By.ID,
                                                          element=certification_services.IMPORT_OCSP_CERT_BTN_ID)

                xroad.fill_upload_input(self, import_cert_btn, target_ocsp_cert_path)

                url_area = self.wait_until_visible(type=By.ID, element=certification_services.OCS_RESPONSE_URL_AREA_ID)

                self.input(url_area, self.config.get('ca.ocs_host'))

                self.wait_until_visible(type=By.ID,
                                        element=certification_services.SUBMIT_OCSP_CERT_AND_URL_BTN_ID).click()

            self.driver.get(self.url)

            self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()

            remove_certificate(self, client)

            self.log('Wait 120 seconds for changes ')
            time.sleep(120)
            self.log('waiting over')
            if error:
                assert False

    def wrong_cert_type_error(self, client):
        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        get_cert(sshclient, 'sign-auth', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)
        assert messages.get_error_message(
            self) == messages.CERTIFICATE_NOT_SIGNING_KEY

        popups.close_all_open_dialogs(self)
        remove_certificate(self, client)

    def no_key_error(self, client):

        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        remove_certificate(self, client)

        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        assert messages.get_error_message(self) == messages.NO_KEY_FOR_CERTIFICATE

    def no_client_for_certificate_error(self, client):
        self.driver.get(self.url)
        self.wait_jquery()

        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        remove_client(self, client)

        import_cert(self, file_cert_path)
        self.wait_jquery()
        time.sleep(3)

        assert messages.NO_CLIENT_FOR_CERTIFICATE in messages.get_error_message(self)

        popups.close_all_open_dialogs(self)

        remove_certificate(self, client)

        self.driver.get(self.url)
        self.wait_jquery()
        add_client(self, client)
        time.sleep(60)

    def wrong_format_error(self):
        self.driver.get(self.url)
        self.wait_jquery()

        path = self.get_temp_path('INFO')
        temp_path = glob.glob(path)[0]

        import_cert(self, temp_path)
        self.wait_jquery()
        time.sleep(3)

        assert messages.get_error_message(self) == messages.WRONG_FORMAT_CERTIFICATE

    def already_existing_error(self, client):
        self.driver.get(self.url)
        self.wait_jquery()

        remote_csr_path = 'temp.der'
        cert_path = 'temp.pem'

        local_cert_path = self.get_download_path(cert_path)

        server_name = ssh_server_actions.get_server_name(self)

        for fpath in glob.glob(self.get_download_path('*')):
            os.remove(fpath)

        generate_csr(self, client['code'], client['class'], ssh_server_actions.get_server_name(self))
        file_path = \
            glob.glob(self.get_download_path('_'.join(['*', server_name, client['class'], client['code']]) + '.der'))[0]
        sshclient = ssh_client.SSHClient(self.config.get('ca.ssh_host'), self.config.get('ca.ssh_user'),
                                         self.config.get('ca.ssh_pass'))

        get_cert(sshclient, 'sign-sign', file_path, local_cert_path, cert_path, remote_csr_path)
        time.sleep(6)
        file_cert_path = glob.glob(local_cert_path)[0]

        import_cert(self, file_cert_path)

        import_cert(self, file_cert_path)

        self.wait_jquery()
        time.sleep(3)

        assert messages.CERTIFICATE_ALREADY_EXISTS in messages.get_error_message(self)

        popups.close_all_open_dialogs(self)

        remove_certificate(self, client)

    return fail_test_case


def get_ca_certificate(client, cert, target_path):
    sftp = client.get_client().open_sftp()
    sftp.get('/home/ca/CA/certs/' + cert, target_path)
    sftp.close()


# This requires the user to have sudo rights without password prompt
def get_cert(client, service, file_path, local_path, remote_cert_path, remote_csr_path):
    client.exec_command('rm temp*')
    sftp = client.get_client().open_sftp()
    sftp.put(file_path, remote_csr_path)
    client.exec_command('cat ' + remote_csr_path + ' | ' + service + ' > ' + remote_cert_path)
    time.sleep(3)
    sftp.get(remote_cert_path, local_path)
    sftp.close()
    client.close()


def generate_csr(self, client_code, client_class, server_name):
    client = ':'.join([server_name, client_class, client_code, '*'])
    self.log('Open keys and certificates tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
    time.sleep(5)
    self.wait_jquery()
    self.log('Click on softoken row')
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_ROW_XPATH).click()
    self.log('Click on "Generate key" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATEKEY_BTN_ID).click()
    self.log(
        'Insert ' + keyscertificates_constants.KEY_LABEL_TEXT + '_' + client_code + '_' + client_class + ' to "LABEL" area')
    key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
    self.input(key_label_input, keyscertificates_constants.KEY_LABEL_TEXT + '_' + client_code + '_' + client_class)

    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    self.log('Click on generated key row')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.get_generated_key_row_xpath(client_code,
                                                                                           client_class)).click()
    self.log('Click on "GENERATE CSR" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATECSR_BTN_ID).click()

    self.log('Change CSR format')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID))
    assert 'DER' in map(lambda x: x.text, select.options)
    assert 'PEM' in map(lambda x: x.text, select.options)
    select.select_by_visible_text('DER')

    self.log('Select "certification service"')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID))
    self.wait_jquery()
    time.sleep(5)
    options = filter(lambda y: str(y) is not '', map(lambda x: x.text, select.options))
    assert len(filter(lambda x: self.config.get('ca.ssh_host').upper() in x, options)) == 1
    filter(lambda x: self.config.get('ca.ssh_host').upper() in x.text, select.options).pop().click()

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
    self.log('Check Instance Identifier')
    assert self.wait_until_visible(type=By.XPATH,
                                   element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_C_XPATH).get_attribute(
        'value') == server_name
    self.log('Check Member Class')
    assert self.wait_until_visible(type=By.XPATH,
                                   element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_O_XPATH).get_attribute(
        'value') == client_class
    self.log('Check Member Code')
    assert self.wait_until_visible(type=By.XPATH,
                                   element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_CN_XPATH).get_attribute(
        'value') == client_code

    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()


def delete_added_key(self, client_code, client_class):
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
    self.log('Open keys and certificates tab')
    self.driver.get(self.url)
    self.wait_jquery()

    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.IMPORT_BTN_ID).click()

    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.IMPORT_CERTIFICATE_POPUP_XPATH)
    file_abs_path = os.path.abspath(cert_path)
    time.sleep(3)
    file_upload = self.wait_until_visible(type=By.ID, element=popups.FILE_UPLOAD_ID)
    xroad.fill_upload_input(self, file_upload, file_abs_path)
    time.sleep(1)
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.FILE_IMPORT_OK_BTN_ID).click()
    self.wait_jquery()


def check_import(self, client_class, client_code):
    self.wait_jquery()
    td = self.wait_until_visible(type=By.XPATH,
                                 element=keyscertificates_constants.get_generated_row_row_by_td_text(
                                     ' : '.join([client_class, client_code])))
    tds = td.find_element_by_xpath(".//ancestor::tr").find_elements_by_tag_name('td')
    self.log('CHECK FOR OCSP RESPONSE AND STATUS: {0}'.format(
        (str(tds[2].text) == 'good') & (str(tds[4].text) == 'registered')))
    assert ((str(tds[2].text) == 'good') & (str(tds[4].text) == 'registered'))


def added_client_row(self, client):
    self.log('Finding added client')

    self.added_client_id = ' : '.join(
        ['SUBSYSTEM', ssh_server_actions.get_server_name(self), client['class'], client['code'],
         client['subsystem_code']])
    table_rows = self.by_css(clients_table_vm.CLIENT_ROW_CSS, multiple=True)
    client_row_index = clients_table_vm.find_row_by_client(table_rows, client_id=self.added_client_id)
    return table_rows[client_row_index]
