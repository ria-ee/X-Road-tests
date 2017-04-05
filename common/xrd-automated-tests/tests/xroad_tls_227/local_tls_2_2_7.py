import tarfile
from view_models import popups, clients_table_vm, sidebar, ss_system_parameters
from helpers import xroad, soaptestclient
import os, time
from selenium.webdriver.common.by import By
from requests.exceptions import SSLError
from tests.xroad_configure_service_222 import configure_service_2_2_2

# These faults are checked when we need the result to be unsuccessful. Otherwise the checking function returns True.
# faults_unsuccessful = ['Server.ServerProxy.ServiceDisabled', 'Client.InternalError', 'Server.ClientProxy.SslAuthenticationFailed']
faults_unsuccessful = ['Server.ClientProxy.SslAuthenticationFailed']
# These faults are checked when we need the result to be successful. Otherwise the checking function returns False.
faults_successful = ['Server.ServerProxy.AccessDenied', 'Server.ServerProxy.UnknownService',
                     'Server.ServerProxy.ServiceDisabled', 'Server.ClientProxy.*', 'Client.*']


def test_delete_tls(case, client, requester):
    self = case

    ss1_host = self.config.get('ss1.host')
    ss1_user = self.config.get('ss1.user')
    ss1_pass = self.config.get('ss1.pass')

    ss2_host = self.config.get('ss2.host')
    ss2_user = self.config.get('ss2.user')
    ss2_pass = self.config.get('ss2.pass')

    client_id = xroad.get_xroad_subsystem(client)
    requester_id = xroad.get_xroad_subsystem(requester)

    testservice_name = self.config.get('services.test_service')
    wsdl_url = self.config.get('wsdl.remote_path').format(self.config.get('wsdl.service_wsdl'))
    new_service_url = self.config.get('services.test_service_url')

    def delete_tls():
        self.reload_webdriver(url=ss1_host, username=ss1_user, password=ss1_pass)

        self.log('*** local_tls')
        self.log('2.2.7-delete setting {0} connection type to HTTP'.format(client_id))

        # Open "Security Server Clients" page
        self.by_css(sidebar.CLIENTS_BTN_CSS).click()

        # Wait until list is loaded
        self.wait_jquery()

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_internal_servers(self, client_id=client_id)

        # Set connection type to HTTPS_NO_AUTH (SSLNOAUTH)
        # case.assertEqual(clients_table_vm.client_servers_popup_set_connection(self, 'NOSSL'), True,
        #                  msg='2.2.7-delete-2 Failed to set connection type')
        self.is_true(clients_table_vm.client_servers_popup_set_connection(self, 'NOSSL'),
                     msg='2.2.7-delete-2 Failed to set connection type')

        # Delete all internal certificates
        clients_table_vm.client_servers_popup_delete_tls_certs(self)

        # Switch to Security server 2
        self.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)

        # Open "Security Server Clients" page
        self.by_css(sidebar.CLIENTS_BTN_CSS).click()

        # Wait until list is loaded
        self.wait_jquery()

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_id=requester_id)

        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_url=wsdl_url,
                                                                          service_name=testservice_name)

        # Click on the service row to select it
        service_row.click()

        # Open service parameters by finding the "Edit" button and clicking it.
        edit_service_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)

        # Click the "Edit" button to open "Edit Service Parameters" popup
        edit_service_button.click()

        warning, error = configure_service_2_2_2.edit_service(self, service_url=new_service_url)
        # case.assertIsNone(error, msg='2.2.7-14 Got error when trying to update service URL')
        case.is_none(error, msg='2.2.7-14 Got error when trying to update service URL')

        # Click tab "Internal Servers"
        self.by_css(clients_table_vm.INTERNAL_CERTS_TAB_TITLE_CSS).click()

        # Wait until everything is loaded.
        self.wait_jquery()

        # Delete all internal certificates
        clients_table_vm.client_servers_popup_delete_tls_certs(self)

    return delete_tls


def test_tls(case, client, requester):
    self = case
    # certs_download_filename = 'certs.tar.gz'
    # certs_ss1_filename = 'certs_ss1.tar.gz'
    # certs_ss2_filename = 'certs_ss2.tar.gz'
    # verify_cert_filename = 'cert.pem'
    # client_cert_filename = 'mock.crt'
    # client_key_filename = 'mock.key'
    # mock_cert_filename = 'mockservice.crt'
    certs_download_filename = self.config.get('certs.downloaded_ss_certs_filename')
    certs_ss1_filename = self.config.get('certs.ss1_certs')
    certs_ss2_filename = self.config.get('certs.ss2_certs')
    verify_cert_filename = self.config.get('certs.server_cert_filename')
    client_cert_filename = self.config.get('certs.client_cert_filename')
    client_key_filename = self.config.get('certs.client_key_filename')
    mock_cert_filename = self.config.get('certs.service_cert_filename')

    download_check_interval = 1  # Seconds
    download_time_limit = self.config.get('certs.cert_download_time_limit')
    delete_created_files = False

    sync_retry = self.config.get('services.request_sync_delay')
    sync_max_seconds = self.config.get('services.request_sync_timeout')

    # service = helper.split_xroad_data('KS1 : COM : CLIENT3 : testservice : bodyMassIndex.v1')
    # client = helper.split_xroad_data('KS1 : COM : CLIENT3 : sub')

    client_id = xroad.get_xroad_subsystem(client)
    requester_id = xroad.get_xroad_subsystem(requester)

    ss1_host = self.config.get('ss1.host')
    ss1_user = self.config.get('ss1.user')
    ss1_pass = self.config.get('ss1.pass')

    ss2_host = self.config.get('ss2.host')
    ss2_user = self.config.get('ss2.user')
    ss2_pass = self.config.get('ss2.pass')

    wsdl_url = self.config.get('wsdl.remote_path').format(self.config.get('wsdl.service_wsdl'))
    testservice_name = self.config.get('services.test_service')  # 'xroadGetRandom.v1'
    new_service_url = self.config.get('services.test_service_url_ssl')  # 'https://localhost:18086/xroadGetRandom'

    query_url = self.config.get('ss1.service_path')
    query_url_ssl = self.config.get('ss1.service_path_ssl')
    query_filename = self.config.get('services.testservice_request_filename')
    query = self.get_xml_query(query_filename)
    client_cert_path = self.get_cert_path(client_cert_filename)
    client_key_path = self.get_cert_path(client_key_filename)
    mock_cert_path = self.get_cert_path(mock_cert_filename)

    ss2_certs_directory = self.config.get('certs.ss2_certificate_directory')

    testclient_http = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                    retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                    faults_successful=faults_successful,
                                                    faults_unsuccessful=faults_unsuccessful)
    testclient_https = soaptestclient.SoapTestClient(url=query_url_ssl, body=query,
                                                     retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                     server_certificate=self.get_download_path(verify_cert_filename),
                                                     faults_successful=faults_successful,
                                                     faults_unsuccessful=faults_unsuccessful)
    testclient_https_ss2 = soaptestclient.SoapTestClient(url=query_url_ssl, body=query,
                                                         retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                         server_certificate=self.get_download_path(
                                                             os.path.join(ss2_certs_directory, verify_cert_filename)),
                                                         client_certificate=(client_cert_path, client_key_path),
                                                         faults_successful=faults_successful,
                                                         faults_unsuccessful=faults_unsuccessful)

    def local_tls():
        """
        :param self: MainController class object
        :return: None
        ''"""

        self.log('*** local_tls')

        self.reload_webdriver(url=ss1_host, username=ss1_user, password=ss1_pass)

        certs_filename = self.get_download_path(certs_download_filename)

        ss1_filename = self.get_download_path(certs_ss1_filename)
        ss2_filename = self.get_download_path(certs_ss2_filename)

        ss2_certs_directory_abs = self.get_download_path(ss2_certs_directory)

        # Create directory if not exists
        if not os.path.isdir(ss2_certs_directory_abs):
            os.mkdir(ss2_certs_directory_abs)

        # Remove old files if they exist
        # for filename in [certs_filename, ss1_filename, ss2_filename]:
        #     if os.path.isfile(filename):
        #         try:
        #             os.remove(filename)
        #         except:
        #             pass
        self.remove_files([certs_filename, ss1_filename, ss2_filename, ss2_certs_directory_abs])

        created_files = [certs_filename]

        self.start_mock_service()

        # '''
        # TEST PLAN 2.2.7-1 generate new internal TLS key.
        self.log('2.2.7-1 generate new internal TLS key.')

        # Click "System Parameters" in sidebar
        self.by_css(sidebar.SYSTEM_PARAMETERS_BTN_CSS).click()

        # Click "Generate New TLS Key" button
        self.wait_until_visible(ss_system_parameters.GENERATE_INTERNAL_TLS_KEY_BUTTON_ID, type=By.ID).click()

        # A confirmation dialog should open. Confirm the question.
        popups.confirm_dialog_click(self)

        # Wait until the TLS certificate has been generated.
        self.wait_jquery()

        self.log('2.2.7-1 new key has been generated, downloading certificate')

        # If file already exists, delete it first
        if os.path.isfile(certs_filename):
            os.remove(certs_filename)

        # Find and click the "Export" button. Download should start automatically.
        self.by_id(ss_system_parameters.EXPORT_INTERNAL_TLS_CERT_BUTTON_ID).click()

        # Check if file exists every 0.5 seconds or until limit has passed.
        start_time = time.time()
        while True:
            if os.path.isfile(certs_filename):
                break
            if time.time() - start_time > download_time_limit:
                # Raise AssertionError
                raise AssertionError('Download time limit of {0} seconds passed for file {1}'.format(
                    download_time_limit, certs_download_filename))
            time.sleep(download_check_interval)

        os.rename(certs_filename, ss1_filename)

        created_files.append(ss1_filename)
        self.log('2.2.7-1 certificate archive has been downloaded, extracting')

        # We're here, so download succeeded.
        # Extract the archive (tgz format) to downloads directory.
        with tarfile.open(ss1_filename, 'r:gz') as tar:
            # tarfile.extractall does not overwrite files so we need to extract them one by one.
            for fileobj in tar:
                filename = os.path.join(os.path.dirname(fileobj.name), os.path.basename(fileobj.name))
                file_target = self.get_download_path(filename)
                if os.path.isfile(file_target):
                    os.remove(file_target)
                created_files.append(file_target)
                tar.extract(fileobj, self.get_download_path())

        self.log('2.2.7-1 certificate archive has been extracted')

        self.log('2.2.7-2 setting {0} connection type to HTTPS_NO_AUTH'.format(client_id))

        # Open "Security Server Clients" page
        self.by_css(sidebar.CLIENTS_BTN_CSS).click()

        # Wait until list is loaded
        self.wait_jquery()

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_internal_servers(self, client_id=client_id)

        # Set connection type to HTTPS_NO_AUTH (SSLNOAUTH)
        # case.assertEqual(clients_table_vm.client_servers_popup_set_connection(self, 'SSLNOAUTH'), True,
        #                  msg='2.2.7-2 Failed to set connection type')
        case.is_true(clients_table_vm.client_servers_popup_set_connection(self, 'SSLNOAUTH'),
                     msg='2.2.7-2 Failed to set connection type')
        # time.sleep(auth_update_delay)

        # TEST PLAN 2.2.7-3 test query from TS1:CLIENT1:sub to test service. Query should fail.
        self.log('2.2.7-3 test query {0} to test service. Query should fail.'.format(query_filename))

        # case.assertEqual(testclient_http.check_fail(), True, msg='2.2.7-3 test query succeeded')
        case.is_true(testclient_http.check_fail(), msg='2.2.7-3 test query succeeded')

        # TEST PLAN 2.2.7-4/5 test query to test service using SSL and client certificate. Query should succeed.
        self.log('2.2.7-4/5 test query to test service using SSL and client certificate. Query should succeed.')
        # case.assertEqual(testclient_https.check_success(), True, msg='2.2.7-5 test query failed')
        case.is_true(testclient_https.check_success(), msg='2.2.7-5 test query failed')

        self.log('2.2.7-6 setting {0} connection type to HTTPS'.format(client_id))

        # Set connection type to HTTPS (SSLAUTH)
        # case.assertEqual(clients_table_vm.client_servers_popup_set_connection(self, 'SSLAUTH'), True,
        #                  msg='2.2.7-6 Failed to set connection type')
        case.is_true(clients_table_vm.client_servers_popup_set_connection(self, 'SSLAUTH'),
                     msg='2.2.7-6 Failed to set connection type')
        # time.sleep(auth_update_delay)

        # TEST PLAN 2.2.7-7 test query to test service using SSL and client certificate. Query should fail.
        self.log('2.2.7-7 test query to test service using SSL and client certificate. Query should fail.')
        # case.assertEqual(testclient_https.check_fail(), True, msg='2.2.7-7 test query succeeded')
        case.is_true(testclient_https.check_fail(), msg='2.2.7-7 test query succeeded')

        # TEST PLAN 2.2.7-8 upload certificate to TS1 client CLIENT1:sub
        self.log('2.2.7-8 upload certificate to TS1 client {0}'.format(client_id))

        # Find the "Add" button and click it.
        self.by_id(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_ADD_CERTIFICATE_BTN_ID).click()

        # Get the upload button
        upload_button = self.by_id(popups.FILE_UPLOAD_BROWSE_BUTTON_ID)
        xroad.fill_upload_input(self, upload_button, client_cert_path)

        submit_button = self.by_id(popups.FILE_UPLOAD_SUBMIT_BUTTON_ID)
        submit_button.click()

        # TEST PLAN 2.2.7-9 test query to test service using SSL and client certificate. Query should succeed.
        self.log('2.2.7-9 test query to test service using SSL and client certificate. Query should succeed.')

        # Set client certificate and key
        testclient_https.client_certificate = (client_cert_path, client_key_path)

        # case.assertEqual(testclient_https.check_success(), True, msg='2.2.7-9 test query failed')
        case.is_true(testclient_https.check_success(), msg='2.2.7-9 test query failed')

        # TEST PLAN 2.2.7-10 set test client to use TS2 TLS certificate
        self.log('2.2.7-10 set test client to use TS2 TLS certificate')

        # First, get the certificate. For this, we need to get webdriver to go to TS2
        self.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)

        # Click "System Parameters" in sidebar
        self.by_css(sidebar.SYSTEM_PARAMETERS_BTN_CSS).click()

        self.wait_jquery()

        self.log('2.2.7-10 downloading TS2 certificate')

        if os.path.isfile(certs_filename):
            os.remove(certs_filename)

        # Find and click the "Export" button. Download should start automatically.
        self.by_id(ss_system_parameters.EXPORT_INTERNAL_TLS_CERT_BUTTON_ID).click()

        # Check if file exists every 0.5 seconds or until limit has passed.
        start_time = time.time()
        while True:
            if os.path.isfile(certs_filename):
                break
            if time.time() - start_time > download_time_limit:
                # Raise AssertionError
                raise AssertionError('Download time limit of {0} seconds passed for file {1}'.format(
                    download_time_limit, certs_download_filename))
            time.sleep(download_check_interval)

        os.rename(certs_filename, ss2_filename)

        created_files.append(ss2_filename)
        self.log('2.2.7-10 certificate archive has been downloaded, extracting')

        # We're here, so download succeeded.

        # Extract the archive (tgz format) to downloads directory.
        with tarfile.open(ss2_filename, 'r:gz') as tar:
            # tarfile.extractall does not overwrite files so we need to extract them one by one.
            for fileobj in tar:
                filename = self.get_download_path(os.path.join(ss2_certs_directory, os.path.dirname(fileobj.name),
                                                               os.path.basename(fileobj.name)))
                file_target = self.get_download_path(filename)
                if os.path.isfile(file_target):
                    os.remove(file_target)
                created_files.append(file_target)
                tar.extract(fileobj, self.get_download_path(ss2_certs_directory))

        self.log('2.2.7-10 certificate archive has been extracted')

        # TEST PLAN 2.2.7-11 test query to test service using SSL and TS2 certificate. Query should fail.
        self.log('2.2.7-11 test query to test service using SSL and client certificate, verify TS2. Query should fail.')

        try:
            testclient_https_ss2.check_fail()
            # case.assertEqual(True, False, msg='2.2.7-11 test query failed but not with an SSLError.')
            case.is_true(False, msg='2.2.7-11 test query failed but not with an SSLError.')
        except SSLError:
            # We're actually hoping for SSLError so we're good.
            pass

        # TEST PLAN 2.2.7-12/13 test query to test service using SSL and TS1 certificate. Query should succeed.
        self.log(
            '2.2.7-12/13 test query to test service using SSL and client certificate, verify TS1. Query should succeed.')

        # case.assertEqual(testclient_https.check_success(), True, msg='2.2.7-13 test query failed')
        case.is_true(testclient_https.check_success(), msg='2.2.7-13 test query failed')

        # TEST PLAN 2.2.7-14 TS2 test service is configured from http to https. TLS check disabled.
        self.log(
            '2.2.7-14 TS2 test service is configured from http to https. TLS check disabled.'.format(new_service_url))

        # Open "Security Server Clients" page
        self.by_css(sidebar.CLIENTS_BTN_CSS).click()

        # Wait until list is loaded
        self.wait_jquery()

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_id=requester_id)

        # Find the service under the specified WSDL in service list (and expand the WSDL services list if not open yet)
        service_row = clients_table_vm.client_services_popup_find_service(self, wsdl_url=wsdl_url,
                                                                          service_name=testservice_name)

        # Click on the service row to select it
        service_row.click()

        # Open service parameters by finding the "Edit" button and clicking it.
        edit_service_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)

        # Click the "Edit" button to open "Edit Service Parameters" popup
        edit_service_button.click()

        warning, error = configure_service_2_2_2.edit_service(self, service_url=new_service_url, verify_tls=False)
        # case.assertIsNone(error, msg='2.2.7-14 Got error when trying to update service URL')
        case.is_none(error, msg='2.2.7-14 Got error when trying to update service URL')

        # TEST PLAN 2.2.7-15 test query to test service using SSL and TS1 certificate. Query should succeed.
        self.log('2.2.7-15 test query to test service using SSL and client certificate. Query should succeed.')
        # case.assertEqual(testclient_https.check_success(), True, msg='2.2.7-15 test query failed')
        case.is_true(testclient_https.check_success(), msg='2.2.7-15 test query failed')

        # TEST PLAN 2.2.7-16 TS2 test service is as https with TLS certificate check enabled.

        # Click the "Edit" button to open "Edit Service Parameters" popup
        edit_service_button.click()

        configure_service_2_2_2.edit_service(self, service_url=new_service_url, verify_tls=True)
        # '''

        # TEST PLAN 2.2.7-17 test query to test service using SSL and TS1 certificate. Query should succeed.
        self.log('2.2.7-17 test query to test service using SSL and client certificate. Query should fail.')

        case.is_true(testclient_https.check_fail(faults=['Server.ServerProxy.ServiceFailed.SslAuthenticationFailed']),
                     msg='2.2.7-17 test query succeeded')

        # TEST PLAN 2.2.7-18 import test service TLS certificate to security server TS2
        self.log('2.2.7-18 import test service TLS certificate to security server TS2')

        # Click tab "Internal Servers"
        self.by_css(clients_table_vm.INTERNAL_CERTS_TAB_TITLE_CSS).click()

        # Wait until everything is loaded.
        self.wait_jquery()

        # Find the "Add" button and click it.
        self.by_id(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_ADD_CERTIFICATE_BTN_ID).click()

        # Get the upload button
        upload_button = self.by_id(popups.FILE_UPLOAD_BROWSE_BUTTON_ID)
        xroad.fill_upload_input(self, upload_button, mock_cert_path)

        submit_button = self.by_id(popups.FILE_UPLOAD_SUBMIT_BUTTON_ID)
        submit_button.click()

        self.log('2.2.7-19 test query to test service using SSL and client certificate. Query should succeed.')

        case.is_true(testclient_https.check_success(), msg='2.2.7-19 test query failed')

        # Remove all created files
        if delete_created_files:
            self.log('2.2.7 removing downloaded files')
            self.remove_files(created_files)

    return local_tls
