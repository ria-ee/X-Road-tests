import os
import time

from selenium.webdriver.common.by import By

from helpers import ssh_server_actions, xroad, auditchecker
from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import add_client_to_ss, \
    login_with_logout, add_sub_as_client_to_member, approve_requests, login
from tests.xroad_global_groups_tests import global_groups_tests
from tests.xroad_logging_in_cs_2111.logging_in_cs import add_member_to_cs, add_group, \
    add_client_to_group, delete_client
from tests.xroad_ss_client_certification_213 import client_certification
from view_models import popups, sidebar, groups_table, cs_security_servers, members_table, keys_and_certificates_table, \
    messages, log_constants
from view_models.cs_security_servers import SECURITY_SERVER_TABLE_CSS
from view_models.log_constants import APPROVE_CLIENT_REGISTRATION_REQUST, ADD_SECURITY_SERVER
from view_models.messages import CERTIFICATE_IMPORT_SUCCESSFUL, CERTIFICATE_ADDING_NEW_SERVER_REQUEST_ADDED_NOTICE


def test_deleting_member_with_global_group(cs_ssh_host, cs_ssh_username, cs_ssh_password, client, user, test_group):
    """
    Delete member in central server, which has global group test
    :param cs_ssh_host: string - central server ssh host
    :param cs_ssh_username: string - central server ssh username
    :param cs_ssh_password:  string - central server ssh password
    :param client: dict - member info
    :param user: dict - user, under which the changes are made
    :param test_group: - test group name
    :return:
    """

    def deleting_member_with_global_group(self):
        ssh_client = ssh_server_actions.get_client(cs_ssh_host, cs_ssh_username, cs_ssh_password)

        # MEMBER_10 Add new X-Road Member
        self.log('MEMBER_10 Add new X-Road Member')
        add_member_to_cs(self, ssh_client, user, member=client)
        popups.close_all_open_dialogs(self)

        # SERVICE_32 add new group
        self.log('SERVICE_32 add new group')
        add_group(self, ssh_client, user, group=test_group)

        # SERVICE_33 add the new subsystem to the new group
        self.log('SERVICE_33 add the new subsystem to the new group')
        add_client_to_group(self, ssh_client, user, member=client, group=test_group)

        self.log('MEMBER_26 6.a Delete member in global group from central server')
        delete_client(self, ssh_client, user, member=client)
        self.wait_jquery()

        self.log('MEMBER_36 6.a1 System removes the member from global groups')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()

        member_count_after_deletion = self.wait_until_visible(type=By.XPATH,
                                                              element=groups_table.get_global_group_member_count_by_code(
                                                                  test_group)).text
        self.is_equal(member_count_after_deletion, '0', msg='Global group member count not 0 after deleting member')

    return deleting_member_with_global_group


def test_deleting_member_with_subsystem_registered_as_client_to_ss(case, cs_member_name, cs_new_member,
                                                                   ss1_client, cs_ssh_host,
                                                                   cs_ssh_username, cs_ssh_password, user):
    """
    Delete member in central server with subsystem registered as security server client test
    :param case:
    :param cs_member_name: str - new member name
    :param cs_new_member: dict - member to add
    :param ss1_client: dict - ss1 client info
    :param cs_ssh_host: str - central server ssh host
    :param cs_ssh_username: str - central server ssh username
    :param cs_ssh_password: str - central server ssh password
    :param user:
    :return:
    """
    self = case
    cs_member = {'name': cs_member_name, 'class': cs_new_member['class'], 'code': cs_new_member['code']}
    ss1_instance = ss1_client['instance']

    def deleting_member_with_subsystem_registered_as_client_to_ss():
        self.log('MEMBER_26 5a The member\'s subsystems are clients of security servers')
        ssh_client = ssh_server_actions.get_client(cs_ssh_host, cs_ssh_username, cs_ssh_password)

        # MEMBER_26 Delete the member from central server
        self.log('MEMBER_26 Delete the member from central server')
        delete_client(self, ssh_client, user, member=cs_member)

        self.log('Open management requests')
        self.by_css(sidebar.MANAGEMENT_REQUESTS_CSS).click()
        requests_table = self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_TABLE_ID)
        self.wait_jquery()
        self.log('Find first table row and click on it')
        requests_table.find_element_by_tag_name('tbody').find_element_by_tag_name('tr').click()
        self.log('Open request details')
        self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
        '''Request details dialog element'''
        client_deletion_details_dialog = self.wait_until_visible(type=By.ID,
                                                                 element=cs_security_servers.CLIENT_DELETION_REQUEST_DETAILS_DIALOG_ID)
        '''Request details comment field text'''
        comment = client_deletion_details_dialog.find_element_by_class_name(
            cs_security_servers.CLIENT_DELETION_REQUEST_DETAILS_DIALOG_COMMENTS_INPUT_CLASS).text
        self.log('Check if request details is about subsystem deletion')
        expected_deletion_comment = messages.SUBSYSTEM_DELETION_COMMENT.format(ss1_instance, ss1_client['class'],
                                                                               ss1_client['code'],
                                                                               ss1_client['subsystem'])
        self.log('MEMBER_26 5a.1 System creates and saves a security server '
                 'client deletion request with the comment \n"{0}"'.format(expected_deletion_comment))
        self.is_equal(comment,
                      expected_deletion_comment,
                      msg='Subsystem deletion comment not correct')

    return deleting_member_with_subsystem_registered_as_client_to_ss


def remove_client_and_key_from_ss(case, ss1_host, ss1_username, ss1_password, ss1_client_name, ss1_client):
    """
    Removes client and key from security server
    :param case:
    :param ss1_host: str - security server host
    :param ss1_username: str - security server username
    :param ss1_password:  str - security server password
    :param ss1_client_name:  str - security server client name
    :param ss1_client:  dict - security server client info
    :return:
    """
    self = case
    ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                   'subsystem_code': ss1_client['subsystem']}

    def remove_client_and_key():
        '''Open securtiy server homepage'''
        self.reload_webdriver(url=ss1_host, username=ss1_username, password=ss1_password)
        '''Remove added client'''
        client_registration_in_ss.remove_client(self, client=ss_1_client, delete_cert=True)
        '''Remove added client certificate'''
        client_registration_in_ss.remove_certificate(self, client=ss_1_client)

    return remove_client_and_key


def test_deleting_member_with_security_server(self, cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                                              client, user):
    """
    Delete member with security server test
    :param case:
    :param cs_ssh_host: str - central server ssh host
    :param cs_ssh_user: str - central server ssh username
    :param cs_ssh_pass: str - central server ssh password
    :param client: dict - client info
    :param user: dict - username, under which the changes are made
    :return:
    """

    def delete_member_with_security_server():
        self.log('MEMBER_26 4a. Delete member from central server, which has owned security server')
        ssh_client = ssh_server_actions.get_client(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        delete_client(self, ssh_client, user, member=client)

        self.log('MEMBER_26 4a.1 System deletes the security server')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
        try:
            self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
            self.by_xpath(members_table.get_row_by_td_text(client['name']))
            assert False
        except:
            pass

    return delete_member_with_security_server


def test_add_security_server_to_member(case, cs_host, cs_username, cs_password, cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                                       client, cert_path, check_inputs=False, verify_cert=False,
                                       cert_used_already=False, check_server=False):
    """
    MEMBER_12 ALL steps
    Adds security server to member in central server
    :param case:
    :param cs_host: str - central server host
    :param cs_username:  str - central server username
    :param cs_password:  str - central server password
    :param cs_ssh_host:  str - central server ssh host
    :param cs_ssh_user:  str - central server ssh username
    :param cs_ssh_pass:  str - central server ssh password
    :param client:  dict - client info
    :param cert_path:  str - cert filename
    :param verify_cert:  for cert verification
    :param cert_used_already:  for checking cert error
    :param check_server:  for checking server error
    :return:
    """
    self = case
    local_cert_path = self.get_download_path(cert_path)
    file_abs_path = os.path.abspath(local_cert_path)

    def add_security_server_to_member():
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
        current_log_lines = log_checker.get_line_count()
        self.log('Open central server homepage')
        self.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
        self.log('Open added member details')
        global_groups_tests.open_member_details(self, client)
        self.wait_jquery()
        self.log('Open owned servers tab')
        self.by_xpath(cs_security_servers.SERVER_MANAGEMENT_OWNED_SERVERS_TAB).click()
        self.log('MEMBER_12 1. Click on add owned servers button')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=cs_security_servers.ADD_OWNED_SERVER_BTN_CSS).click()
        self.log('MEMBER_12 2. Check if fields are prefilled')
        self.is_equal(client['name'], self.wait_until_visible(type=By.ID,
                                                              element=cs_security_servers.OWNED_SERVERS_UPLOAD_OWNER_NAME_ID).text)
        self.is_equal(client['class'], self.wait_until_visible(type=By.ID,
                                                               element=cs_security_servers.OWNED_SERVERS_UPLOAD_OWNER_CLASS_ID).text)
        self.is_equal(client['code'], self.wait_until_visible(type=By.ID,
                                                              element=cs_security_servers.OWNED_SERVERS_UPLOAD_OWNER_CODE_ID).text)
        self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
        server_code_input = self.wait_until_visible(type=By.ID,
                                                    element=cs_security_servers.OWNED_SERVERS_SERVER_CODE_INPUT_ID)
        self.log('Submit button disabled when fields are empty')
        self.is_false(self.by_id(cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).is_enabled())
        '''Upload button'''
        file_upload = self.by_id(cs_security_servers.OWNED_SERVERS_UPLOAD_CERT_BTN_ID)
        self.log('Uploading certificate to central server')
        if verify_cert:
            wrong_local_cert_path = self.get_download_path('test')
            wrong_file_abs_path = os.path.abspath(wrong_local_cert_path)
            self.log('MEMBER_12 6a The uploaded file is not in PEM or DER format')
            xroad.fill_upload_input(self, file_upload, wrong_file_abs_path)
            expected_error_msg = messages.AUTH_CERT_IMPORT_FILE_FORMAT_ERROR
            self.log('MEMBER_12 6a.1 System displays the "{0}" error message'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)

            error_local_cert_path = self.get_download_path(os.getcwd() + '/error.pem')
            error_file_abs_path = os.path.abspath(error_local_cert_path)
            self.log('MEMBER_12 6b. The uploaded certificate is not an authentication certificate.')
            xroad.fill_upload_input(self, file_upload, error_file_abs_path)
            expected_error_msg = messages.AUTH_CERT_IMPORT_FILE_CANNOT_BE_USED
            self.log('MEMBER_12 6b.1 System displays the "{0}" error message'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            test_add_security_server_to_member(self, cs_host, cs_username, cs_password, cs_ssh_host, cs_ssh_user,
                                               cs_ssh_pass, client, cert_path, check_inputs=True)()
            return

        xroad.fill_upload_input(self, file_upload, file_abs_path)
        self.log('MEMBER_12 4. Uploading the authentication certificate from the local file system')
        self.wait_jquery()
        expected_notice_msg = CERTIFICATE_IMPORT_SUCCESSFUL
        self.log('MEMBER_12 6. System verifies the uploaded certificate and displays the message "{0}"'.format(
            expected_notice_msg))
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
        self.is_equal(expected_notice_msg, notice_msg)
        if check_inputs:
            self.log('MEMBER_12 7, 7.a. System parses the user input ')
            self.log('Submit button disabled when one field is empty')
            self.is_false(self.by_id(cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).is_enabled())
            self.log('MEMBER_12 7.a. Error is shown when input is 256 char long')
            self.input(element=server_code_input, text='A' * 256)
            self.log('Submit server registration form')
            self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
            '''Expected error message'''
            expected_error_msg = messages.INPUT_EXCEEDS_255_CHARS.format('serverCode')
            self.log('MEMBER_12 7.a.1 System displays the "{0}" error message'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            '''Expected log message'''
            expected_log_msg = log_constants.ADD_SECURITY_SERVER_FAILED
            self.log('MEMBER_12 7a.2. System logs the event {0}'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines)
            self.is_true(logs_found)
            self.log('MEMBER_12 7a.3. The server code is reinserted. '
                     'This time 255 chars, starting and ending with whitespace')
            name_255 = ' {0} '.format('A' * 255)
            self.input(element=server_code_input, text=name_255)
            self.log('Submit server registration form')
            self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
            expected_notice_msg = CERTIFICATE_ADDING_NEW_SERVER_REQUEST_ADDED_NOTICE.format(
                '{0}/{1}/{2}/{3}'.format(client['instance'], client['class'], client['code'], name_255.strip()))
            self.log('MEMBER_12 11. System displays the message "{0}"'.format(expected_notice_msg))
            notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
            self.is_equal(expected_notice_msg, notice_msg)
            self.log('Revoke added security server request')
            self.reload_webdriver(cs_host, cs_username, cs_password)
            client_registration_in_ss.revoke_requests(self, auth=True)
            self.log('Add server to member without input parsing check')
            test_add_security_server_to_member(self, cs_host, cs_username, cs_password, cs_ssh_host, cs_ssh_user,
                                               cs_ssh_pass, client, cert_path)()
            return

        if cert_used_already:
            current_log_lines = log_checker.get_line_count()
            self.input(element=server_code_input, text='test')
            self.log('Click ok')
            self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
            self.wait_jquery()
            'Get error message'
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            expected_error_msg = messages.AUTH_CERT_ALREADY_REGISTRED
            self.is_true(error_msg.startswith(expected_error_msg))

            '''Expected log message'''
            expected_log_msg = log_constants.ADD_SECURITY_SERVER_FAILED
            self.log('MEMBER_12 8a.1. System logs the event {0}'.format(expected_log_msg))
            self.log('MEMBER_12 8a.2. System logs the event "Add security server failed" to the audit log')

            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines)
            self.is_true(logs_found)

            test_add_security_server_to_member(self, cs_host, cs_username, cs_password, cs_ssh_host, cs_ssh_user,
                                               cs_ssh_pass, client, cert_path, check_server=True)()
            return

        if check_server:
            current_log_lines = log_checker.get_line_count()
            self.log('Insert server code to server code field')
            self.input(element=server_code_input, text=client['name'])
            self.log('Click ok')
            self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
            self.wait_jquery()
            'Get error message'
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            expected_error_msg = messages.SECURITY_SERVER_CODE_ALREADY_REGISTRED.format(client['class'], client['code'],
                                                                                        client['name'])
            self.is_equal(expected_error_msg, error_msg)

            '''Expected log message'''
            expected_log_msg = log_constants.ADD_SECURITY_SERVER_FAILED
            self.log('MEMBER_12 9a.1. System logs the event {0}'.format(expected_log_msg))
            self.log('MEMBER_12 9a.2. System logs the event "Add security server failed" to the audit log')

            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines)
            self.is_true(logs_found)

            return

        self.log('MEMBER_12 3. Insert server code to server code field')
        self.input(element=server_code_input, text=client['name'])
        self.log('MEMBER_12 5. Registration request is submitted')
        self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
        self.wait_jquery()
        self.log('Check if certificate adding request is present')
        expected_notice_msg = CERTIFICATE_ADDING_NEW_SERVER_REQUEST_ADDED_NOTICE.format(
            '{0}/{1}/{2}/{3}'.format(client['instance'], client['class'], client['code'], client['name']))
        self.log('MEMBER_12 11. System displays the message \n"{0}"'.format(expected_notice_msg))
        self.is_equal(expected_notice_msg, messages.get_notice_message(self))
        expected_log_msg = ADD_SECURITY_SERVER
        self.log('MEMBER_12 12. Check if log contains "{0}" event'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg="Add security server log message not found")

        current_log_lines = log_checker.get_line_count()
        approve_requests(self, use_case='MEMBER_36 ', cancel_confirmation=True)
        expected_log_msg = APPROVE_CLIENT_REGISTRATION_REQUST
        self.log('MEMBER_36 7. System logs the event {0}'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg='"Approve client registration request" event not found in log"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
        self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
        self.wait_jquery()
        self.log('MEMBER_36 4a. System saves the security server information found in the registration request to the '
                 'system configuration as an owned security server of the X-Road member')
        ss_table = self.wait_until_visible(type=By.CSS_SELECTOR, element=SECURITY_SERVER_TABLE_CSS)
        self.is_not_none(members_table.get_row_by_columns(ss_table, [client['name'], client['name'], client['class'],
                                                                     client['code']]))

    return add_security_server_to_member


def add_central_server_member_delete_global_error_cert(case, cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                                                       client, ss2_host,
                                                       ss2_username, ss2_password, user):
    """
    Restores security server after member being deleted in central server
    :param case:
    :param cs_ssh_host: str - central server ssh host
    :param cs_ssh_user: str - central server ssh username
    :param cs_ssh_pass: str - central server ssh password
    :param ca_ssh_host: str - ca ssh host
    :param ca_ssh_user: str - ca ssh username
    :param ca_ssh_pass: str - ca ssh password
    :param client: dict - client info
    :param ss2_host: str - security server 2 host
    :param ss2_username: str - security server 2 username
    :param ss2_password: str - security server 2 password
    :param ss2_ssh_host: str - security server 2 ssh host
    :param cert_path: str - certificate filename
    :param user: dict - user, under which the changes are made
    :return:
    """
    self = case
    sync_timeout = 120

    def add_cs_member_delete_global_error_cert():
        ssh_client = ssh_server_actions.get_client(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        self.log('Open members page')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()

        #MEMBER_10 Add new X-Road Member
        self.log('MEMBER_10 Add new X-Road Member')
        add_member_to_cs(self, ssh_client, user, member=client)

        self.log('Wait until servers have synchronized')
        time.sleep(sync_timeout)
        self.log('Open security server, which was deleted from central server')
        self.reload_webdriver(url=ss2_host, username=ss2_username, password=ss2_password)
        self.log('Open keys and certificates')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.KEYS_AND_CERTIFICATES_TABLE_ID)
        self.wait_jquery()
        self.log('Click on the certificate, which has global error status and delete it')
        self.by_xpath(keys_and_certificates_table.GLOBAL_ERROR_CERTIFICATE_ROW_XPATH).click()
        self.by_id(keys_and_certificates_table.DELETE_BTN_ID).click()
        popups.confirm_dialog_click(self)
        self.wait_jquery()

    return add_cs_member_delete_global_error_cert


def setup_member_with_subsystem_as_ss_client(case, cs_host, cs_username, cs_password, cs_member_name, cs_new_member,
                                             ss1_host, ss1_username,
                                             ss1_password, ss1_client,
                                             ss1_server_name, ss1_client_name):
    """
    Adds member in central server who has subsystem as security server client
    :param case:
    :param cs_host: str - central server host
    :param cs_username: str - central server username
    :param cs_password:  str - central server password
    :param cs_member_name:  str - central server member name
    :param cs_new_member:  dict - central server new member info
    :param ss1_host: str - security server host
    :param ss1_username: str - security server username
    :param ss1_password: str - security server password
    :param ss1_client: dict - security server client info
    :param ss1_server_name: str - security server name
    :param ss1_client_name:  str - security server client name
    :return:
    """
    self = case
    sync_retry = 30
    sync_timeout = 120
    wait_input = 2

    cs_member = {'name': cs_member_name, 'class': cs_new_member['class'], 'code': cs_new_member['code']}

    ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                   'subsystem_code': ss1_client['subsystem']}

    def setup_member_with_subsystem():
        self.log('Login to central server')
        login(self, host=cs_host, username=cs_username, password=cs_password)
        self.log('Adding new member to central server')
        client_registration_in_ss.add_member_to_cs(self, cs_member)
        self.log('Login to security server')
        login(self, host=ss1_host, username=ss1_username, password=ss1_password)
        self.log('Wait until data is synced between servers')
        time.sleep(sync_timeout)
        self.log('Add member as client to security server')
        add_client_to_ss(self, ss_1_client, retry_interval=sync_retry, retry_timeout=sync_timeout,
                         wait_input=wait_input)
        self.log('Navigate to security server homepage')
        self.driver.get(ss1_host)
        self.log('Certificate added client')
        client_certification.test_generate_csr_and_import_cert(client_code=ss_1_client['code'],
                                                               client_class=ss_1_client['class'])(self)
        self.log('Log out and log in to central server')
        login_with_logout(self, cs_host, cs_username, cs_password)
        self.log('Add subsystem to client')
        add_sub_as_client_to_member(self, ss1_server_name, ss_1_client, wait_input=wait_input,
                                    step='Adding subsystem')

        self.log('Approve the registration requests')
        approve_requests(self, '2.2.1-5 ', cancel_confirmation=False)

    return setup_member_with_subsystem
