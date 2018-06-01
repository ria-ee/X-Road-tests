import os

import sys
from selenium.webdriver.common.by import By

from helpers import auditchecker, xroad
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import approve_requests
from tests.xroad_cs_revoke_requests.revoke_requests import revoke_requests
from tests.xroad_global_groups_tests import global_groups_tests
from view_models import cs_security_servers, messages, log_constants, sidebar, members_table
from view_models.cs_security_servers import SECURITY_SERVER_TABLE_CSS
from view_models.log_constants import ADD_SECURITY_SERVER
from view_models.messages import CERTIFICATE_IMPORT_SUCCESSFUL, CERTIFICATE_ADDING_NEW_SERVER_REQUEST_ADDED_NOTICE, \
    close_error_messages


def test_add_owned_server(case, cs_host, cs_username, cs_password, cs_ssh_host, cs_ssh_user, cs_ssh_pass,
                          client, cert_path, server_name=None, check_inputs=False, verify_cert=False,
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

    def add_owned_server():
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
        server_code_input = self.wait_until_visible(type=By.ID,
                                                    element=cs_security_servers.OWNED_SERVERS_SERVER_CODE_INPUT_ID)
        self.log('Submit button disabled when fields are empty')
        self.is_false(self.by_id(cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).is_enabled())
        '''Upload button'''
        file_upload = self.by_id(cs_security_servers.OWNED_SERVERS_UPLOAD_CERT_BTN_ID)
        self.log('Uploading certificate to central server')
        if verify_cert:
            if sys.platform == 'windows':
                wrong_local_cert_path = self.get_download_path('test')
                wrong_file_abs_path = os.path.abspath(wrong_local_cert_path)
            else:
                wrong_file_abs_path = '/dev/null'
            self.log('MEMBER_12 6a The uploaded file is not in PEM or DER format')
            xroad.fill_upload_input(self, file_upload, wrong_file_abs_path)
            expected_error_msg = messages.AUTH_CERT_IMPORT_FILE_FORMAT_ERROR
            self.log('MEMBER_12 6a.1 System displays the "{0}" error message'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            close_error_messages(self)

            error_local_cert_path = self.get_download_path(os.getcwd() + '/error.pem')
            error_file_abs_path = os.path.abspath(error_local_cert_path)
            self.log('MEMBER_12 6b. The uploaded certificate is not an authentication certificate.')
            xroad.fill_upload_input(self, file_upload, error_file_abs_path)
            expected_error_msg = messages.AUTH_CERT_IMPORT_FILE_CANNOT_BE_USED
            self.log('MEMBER_12 6b.1 System displays the "{0}" error message'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
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
            revoke_requests(self, auth=True)
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
            return

        if check_server:
            current_log_lines = log_checker.get_line_count()
            self.log('Insert server code to server code field')
            self.input(element=server_code_input, text=server_name)
            self.log('Click ok')
            self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
            self.wait_jquery()
            'Get error message'
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            expected_error_msg = messages.SECURITY_SERVER_CODE_ALREADY_REGISTRED.format(client['class'], client['code'],
                                                                                        server_name)
            self.is_equal(expected_error_msg, error_msg)

            '''Expected log message'''
            expected_log_msg = log_constants.ADD_SECURITY_SERVER_FAILED
            self.log('MEMBER_12 9a.1. System logs the event {0}'.format(expected_log_msg))
            self.log('MEMBER_12 9a.2. System logs the event "Add security server failed" to the audit log')

            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines)
            self.is_true(logs_found)
            return

        self.log('MEMBER_12 3. Insert server code to server code field')
        self.input(element=server_code_input, text=server_name)
        self.log('MEMBER_12 5. Registration request is submitted')
        self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_OWNED_SERVER_SUBMIT_BUTTON_ID).click()
        self.wait_jquery()
        self.log('Check if certificate adding request is present')
        expected_notice_msg = CERTIFICATE_ADDING_NEW_SERVER_REQUEST_ADDED_NOTICE.format(
            '{0}/{1}/{2}/{3}'.format(client['instance'], client['class'], client['code'], server_name))
        self.log('MEMBER_12 11. System displays the message \n"{0}"'.format(expected_notice_msg))
        self.is_equal(expected_notice_msg, messages.get_notice_message(self))
        expected_log_msg = ADD_SECURITY_SERVER
        self.log('MEMBER_12 12. Check if log contains "{0}" event'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg="Add security server log message not found")

        approve_requests(self, use_case='MEMBER_36 ', cancel_confirmation=True, log_checker=log_checker)
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
        self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
        self.wait_jquery()
        self.log('MEMBER_36 4a. System saves the security server information found in the registration request to the '
                 'system configuration as an owned security server of the X-Road member')
        ss_table = self.wait_until_visible(type=By.CSS_SELECTOR, element=SECURITY_SERVER_TABLE_CSS)
        self.is_not_none(members_table.get_row_by_columns(ss_table, [server_name, client['name'], client['class'],
                                                                     client['code']]))

    return add_owned_server
