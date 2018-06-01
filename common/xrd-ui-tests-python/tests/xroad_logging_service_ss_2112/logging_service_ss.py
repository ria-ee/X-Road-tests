import time
import traceback
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_server_actions, ssh_user_actions, xroad, auditchecker
from tests.xroad_add_to_acl_218 import add_to_acl
from tests.xroad_ss_client_certification_213 import client_certification
from view_models import popups as popups, members_table, clients_table_vm as clients_table, sidebar, \
    keys_and_certificates_table, messages, groups_table
from view_models.log_constants import *
from view_models.messages import MISSING_PARAMETER, INPUT_EXCEEDS_255_CHARS
from helpers import ssh_client

USERNAME = 'username'
PASSWORD = 'password'

test_name = 'LOGGING IN SECURITY SERVER'


def test_test(ssh_host, ssh_username, ssh_password,
              cs_host, cs_username, cs_password,
              sec_host, sec_username, sec_password,
              ca_ssh_host, ca_ssh_username, ca_ssh_password,
              users, client_id, client_name, wsdl_url):
    '''
    MainController test function. Tests maintenance actions and logging in central server.
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :param cs_host: str - central server hostname
    :param cs_username: str - central server UI username
    :param cs_password: str - central server UI password
    :param sec_host: str - security server hostname
    :param sec_username: str - security server UI username
    :param sec_password: str - security server UI password
    :param ca_ssh_host: str - CA SSH server hostname
    :param ca_ssh_username: str - CA SSH username
    :param ca_ssh_password: str - CA SSH password
    :param users: dict - dictionary of users to be added
    :param client_id: str - client XRoad ID
    :param client_name: str - client name
    :param wsdl_url: str - WSDL URL
    :return:
    '''

    def test_case(self):
        # MEMBER_10 / MEMBER_47 / SERVICE_25 / SERVICE_08 Logging maintenance actions in security server
        self.log('*** MEMBER_10 / MEMBER_47 / SERVICE_25 / SERVICE_08')
        error = False
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name
        try:
            # MEMBER_10 Add new member to central server
            self.log('MEMBER_10 Add new member to central server')
            add_member_to_cs(self, member=client)

            # SSH: Add users to Security Server with service administrator rights
            self.log('SSH: Add users to Security Server with service administrator rights')
            add_users_to_system(ssh_host, ssh_username, ssh_password, users)

            self.log('Wait 120 seconds before continuing with security server')
            time.sleep(120)

            self.log('USER 1 ACTIONS')
            user = users['user1']

            # SS_01, MEMBER_47. Log in to security server UI as user1; add new subsystem as client
            self.log('SS_01, MEMBER_47. Log in to security server UI as user1; add new subsystem as client')
            add_client_to_ss(self=self, sec_host=sec_host, sec_username=user[USERNAME],
                             sec_password=user[PASSWORD], ssh_host=ssh_host, ssh_username=ssh_username,
                             ssh_password=ssh_password, client=client)

            self.log('SERVICE_25 Add a Local Group for a Security Server Client')
            add_group_to_client(self=self, sec_host=sec_host, sec_username=user[USERNAME], sec_password=user[PASSWORD],
                                ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password, client=client)

            self.log('Log out and log in')
            self.logout(sec_host)
            self.login(username=user[USERNAME], password=user[PASSWORD])
            user = users['user2']

            # SS_02, SS_01 Log out, log in as user2, certify client
            self.log('SS_02, SS_01 Log out, log in as user2, certify client')
            certify_client_in_ss(self, sec_host, user[USERNAME], user[PASSWORD],
                                 client, users, ssh_host, ssh_username, ssh_password)
            self.url = cs_host

            self.logout(sec_host)
            self.login(users['user2'][USERNAME], users['user2'][PASSWORD])

            # SERVICE_08 Log in as user3 and add WSDL to client
            self.log('SERVICE_08 Add WSDL to client')
            user = users['user3']
            add_services_to_client(self, ssh_host, ssh_username, ssh_password, sec_host, user[USERNAME], user[PASSWORD],
                                   users, client, wsdl_url)

            # SERVICE_12 Enable WSDL
            self.log('SERVICE_12 Enable WSDL')
            enable_service(self, client, wsdl_url)
        except:
            traceback.print_exc()
            error = True
        finally:
            # Remove added data
            remove_data(self=self, ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password,
                        cs_host=cs_host, cs_username=cs_username, cs_password=cs_password, sec_host=sec_host,
                        ca_ssh_host=ca_ssh_host, ca_ssh_username=ca_ssh_username, ca_ssh_password=ca_ssh_password,
                        sec_username=sec_username, sec_password=sec_password, users=users, client=client)
            if error:
                assert False, 'MEMBER_10 / MEMBER_47 / SERVICE_25 / SERVICE_08 failed'

    return test_case


def remove_data(self, ssh_host, ssh_username, ssh_password, cs_host, cs_username, cs_password, sec_host, sec_username,
                sec_password, ca_ssh_host, ca_ssh_username, ca_ssh_password, users, client):
    '''
    Removes data (both full or partial) created during testing.
    :param self: MainController object
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :param cs_host: str - central server hostname
    :param cs_username: str - central server UI username
    :param cs_password: str - central server UI password
    :param sec_host: str - security server hostname
    :param sec_username: str - security server UI username
    :param sec_password: str - security server UI password
    :param ca_ssh_host: str - CA SSH server hostname
    :param ca_ssh_username: str - CA SSH username
    :param ca_ssh_password: str - CA SSH password
    :param users: dict - dictionary of users to be added
    :param client: dict - client data
    :return: None
    '''

    self.log('MEMBER_26 Removing test data')
    # Try to remove member
    try:
        self.log('MEMBER_26 Removing member')
        remove_member(self, cs_host, cs_username, cs_password, member=client)
    except:
        self.log('MEMBER_26 ERROR {0}'.format(traceback.format_exc()))
        self.log('MEMBER_26 Removing member failed')

    # Try to remove certificate
    try:
        self.log('Removing certificate')
        self.reset_webdriver(sec_host, sec_username, sec_password)
        certs_to_revoke = remove_certificate(self, client)

        # Revoke the certificates
        try:
            # Connect to CA over SSH
            try:
                ca_ssh_client = ssh_client.SSHClient(host=ca_ssh_host, username=ca_ssh_username,
                                                     password=ca_ssh_password)
            except:
                ca_ssh_client = None

            if ca_ssh_client is not None:
                self.log('Revoking certificate in CA')
                client_certification.revoke_certs(ca_ssh_client, certs_to_revoke)
        except:
            self.log('Could not revoke certificates in CA')
    except:
        self.log('ERROR {0}'.format(traceback.format_exc()))
        self.log('Removing certicate failed')

    # Try to remove client
    try:
        self.log('MEMBER_53 Removing client')
        self.reset_webdriver(sec_host, sec_username, sec_password)
        remove_client(self, client)
    except:
        self.log('MEMBER_53 ERROR {0}'.format(traceback.format_exc()))
        self.log('MEMBER_53 Removing client failed')

    # Try to remove users
    try:
        self.log('SSH: Removing users')
        remove_users_from_system(ssh_host, ssh_username, ssh_password, users)
    except:
        self.log('SSH: ERROR {0}'.format(traceback.format_exc()))
        self.log('SSH: Removing users failed')


def add_client_to_ss(self, sec_host, sec_username, sec_password,
                     ssh_host, ssh_username, ssh_password, client):
    '''
    Logs in to security server as user, adds a new subsystem as a client. Checks if the actions were logged.
    :param self: MainController object
    :param sec_host: str - security server hostname
    :param sec_username: str - security server UI username
    :param sec_password: str - security server UI password
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH server username
    :param ssh_password: str - SSH server password
    :param client: dict - client data
    :return: None
    '''

    # SS_01 1-4. Log in to security server
    self.log('SS_01 1-3. Log in to security server')
    self.go(sec_host)
    self.login(username=sec_username, password=sec_password)

    # SS_01 4. Check logs for login
    self.log('SS_01 4. Check logs for login.')
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGIN, sec_username)
    self.is_true(bool_value, msg='SS_01 4. Login check failed.')

    # MEMBER_47 1. Select to add a security server client
    self.log('MEMBER_47 1. Select to add a security server client')
    self.click(self.wait_until_visible(type=By.ID, element=clients_table.ADD_CLIENT_BTN_ID))
    self.log('Wait until ADD CLIENT dialog is open')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_XPATH)

    # MEMBER_47 2. Insert the client identifier
    self.log('MEMBER_47 2. Insert the client identifier')
    self.log('Select {0} from "CLIENT CLASS" dropdown'.format(client['class']))
    member_class = Select(self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    member_class.select_by_visible_text(client['class'])

    self.log('Insert {0} to "MEMBER CODE" area'.format(client['code']))
    member_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
    self.input(member_code, client['code'])

    self.log('Insert {0} into "SUBSYSTEM CODE" area'.format(client['subsystem']))
    member_sub_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_ID)
    self.input(member_sub_code, client['subsystem'])

    # Save data
    self.log('Click "OK" to add client')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH))
    self.wait_jquery()

    # MEMBER_47 4-6. System verifies new client and saves it
    self.log('MEMBER_47 4-6. System verifies new client and saves it')

    time.sleep(3)
    # MEMBER_47 7. Log check for adding client
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_CLIENT,
                                                     sec_username)

    self.is_true(bool_value, test_name, 'MEMBER_47 7. Log check for adding client - check failed',
                 'MEMBER_47 7. Log check for adding client')

    time.sleep(5)
    # MEMBER_47 5a. Confirm new client registration
    self.log('MEMBER_47 5a. Confirm new client registration')
    popups.confirm_dialog_click(self)


def add_group_to_client(self, sec_host, sec_username, sec_password, ssh_host, ssh_username, ssh_password, client):
    '''
    Adds local group to client and checks logs for this action.
    :param self: MainController object
    :param sec_host: str - security server hostname
    :param sec_username: str - security server UI username
    :param sec_password: str - security server UI password
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH server username
    :param ssh_password: str - SSH server password
    :param client: dict - client data
    :return: None
    '''

    self.log('SERVICE_25 3a user input parsing terminates with error message(empty code error)')
    log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_username, password=ssh_password)
    current_log_lines = log_checker.get_line_count()
    self.logout(sec_host)
    self.login(sec_username, sec_password)
    self.log('Waiting 120 seconds for changes')
    time.sleep(120)
    self.driver.refresh()
    self.wait_jquery()
    time.sleep(5)
    self.log('Open client local groups tab')
    self.click(added_client_row(self, client).find_element_by_css_selector(clients_table.LOCAL_GROUPS_TAB_CSS))
    self.log('Check if local groups table is empty and contains expected message')
    self.is_not_none(self.by_xpath(groups_table.LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH.format('No (matching) records')))
    self.log('SERVICE_25 1. Click on group add button')
    self.click(self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_GROUP_ADD_BTN_ID))
    self.log('Confirm group adding popup')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH))
    self.wait_jquery()
    expected_error_msg = MISSING_PARAMETER.format('add_group_code')
    self.log('SERVICE_25 3a.1 System displays the error message "{0}"'.format(expected_error_msg))
    error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
    self.is_equal(expected_error_msg, error_message)
    time.sleep(5)
    expected_log_msg = ADD_GROUP_FAILED
    self.log('SERVICE_25 3a.2 System logs the event "{0}"'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)

    self.log('SERVICE_25 3a user input parsing terminates with error message(empty description)')
    messages.close_error_messages(self)
    group_add_code_input = self.by_id(popups.GROUP_ADD_POPUP_CODE_AREA_ID)
    code_256_len = 'A' * 256
    self.log('SERVICE_25 2. Filling group adding popup with "{0}"'.format(code_256_len))
    self.input(element=group_add_code_input, text=code_256_len)
    self.log('Confirm group adding popup')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH))
    self.wait_jquery()
    expected_error_msg = MISSING_PARAMETER.format('add_group_description')
    self.log('SERVICE_25 3a.1 System displays the error message "{0}"'.format(expected_error_msg))
    error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
    self.is_equal(expected_error_msg, error_message)
    time.sleep(5)
    expected_log_msg = ADD_GROUP_FAILED
    self.log('SERVICE_25 3a.2 System logs the event "{0}"'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)

    self.log('SERVICE_25 3a user input parsing terminates with error message(code 256 chars)')
    messages.close_error_messages(self)
    group_add_description_input = self.by_id(popups.GROUP_ADD_POPUP_CODE_DESCRIPTION_ID)
    self.input(element=group_add_description_input, text='asd')
    self.log('Confirm group adding popup')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH))
    self.wait_jquery()
    expected_error_msg = INPUT_EXCEEDS_255_CHARS.format('add_group_code')
    self.log('SERVICE_25 3a.1 System displays the error message "{0}"'.format(expected_error_msg))
    error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
    self.is_equal(expected_error_msg, error_message)
    time.sleep(5)
    expected_log_msg = ADD_GROUP_FAILED
    self.log('SERVICE_25 3a.2 System logs the event "{0}"'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)

    self.log('SERVICE_25 3a user input parsing terminates with error message(description 256 chars)')
    messages.close_error_messages(self)
    self.input(element=group_add_code_input, text='asd')
    self.input(element=group_add_description_input, text=code_256_len)
    self.log('Confirm group adding popup')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH))
    self.wait_jquery()
    expected_error_msg = INPUT_EXCEEDS_255_CHARS.format('add_group_description')
    self.log('SERVICE_25 3a.1 System displays the error message "{0}"'.format(expected_error_msg))
    error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
    self.is_equal(expected_error_msg, error_message)
    time.sleep(5)
    expected_log_msg = ADD_GROUP_FAILED
    self.log('SERVICE_25 3a.2 System logs the event "{0}"'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)

    self.log('SERVICE_25 Add a local group for a security server client'
             '(255 chars code and description, ending and starting with whitespaces)')
    current_log_lines = log_checker.get_line_count()
    code_255_len = ' {0} '.format('A' * 255)
    group_name = code_255_len
    self.log('SERVICE_25 2. Filling group adding popup with "{0}"'.format(group_name))
    self.input(element=group_add_code_input, text=group_name)
    self.input(element=group_add_description_input, text=group_name)
    self.log('Confirm group adding popup')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH))
    self.wait_jquery()
    self.log('SERVICE_25 5. System saves the information about the local group to the system configuration')
    try:
        self.by_xpath(groups_table.LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(group_name))
    except:
        pass
    self.is_not_none(self.by_xpath(groups_table.LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(group_name.strip())))
    group_name = group_name.strip()
    expected_log_msg = ADD_GROUP
    self.log('SERVICE_25 6. System logs the event "{0}"'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)

    self.log('SERVICE_25 4a. Adding group with already existing group info')
    current_log_lines = log_checker.get_line_count()
    self.click(self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_GROUP_ADD_BTN_ID))
    self.log('Filling group adding popup with already existing group info')
    group_add_code_input = self.by_id(popups.GROUP_ADD_POPUP_CODE_AREA_ID)
    self.input(element=group_add_code_input, text=group_name)
    group_add_description_input = self.by_id(popups.GROUP_ADD_POPUP_CODE_DESCRIPTION_ID)
    self.input(element=group_add_description_input, text=group_name)
    self.log('Confirm popup')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH))
    self.wait_jquery()
    expected_error_msg = messages.GROUP_ALREADY_EXISTS_ERROR.format(group_name)
    error_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
    self.log('SERVICE_25 4a.1 System displays the error message "{0}"'.format(expected_error_msg))
    self.is_equal(expected_error_msg, error_message)
    expected_log_msg = ADD_GROUP_FAILED
    self.log('SERVICE_25 4a.2 System logs the event "{0}"'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)

    self.log('SERVICE_25 4a.3 Group code is reinserted')
    current_log_lines = log_checker.get_line_count()
    group_name = 'testgroup1'
    self.log('Trying to add group with code "{0}"'.format(group_name))
    self.input(element=group_add_code_input, text=group_name)
    group_add_description_input = self.by_id(popups.GROUP_ADD_POPUP_CODE_DESCRIPTION_ID)
    self.input(element=group_add_description_input, text=group_name)
    self.log('Confirm popup')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH))
    self.wait_jquery()
    self.log('Check if local groups table contains new added group')
    self.is_not_none(self.by_xpath(groups_table.LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(group_name)))
    self.log('Check if number of groups is equal to 2(2 successful addings)')
    self.is_equal(2, len(
        self.by_css(element=groups_table.LOCAL_GROUP_ROW_CSS, multiple=True)))
    expected_log_msg = ADD_GROUP
    self.log('SERVICE_25 6. System logs the event "{0}"'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)


def certify_client_in_ss(self, sec_host, sec_username, sec_password,
                         client, users=None, ssh_host=None, ssh_username=None, ssh_password=None):
    '''
    Logs out and in, checks logs for these actions; certifies a client in security server.
    :param self: MainController object
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH server username
    :param ssh_password: str - SSH server password
    :param sec_host: str - security server hostname
    :param sec_username: str - security server UI username
    :param sec_password: str - security server UI password
    :param users: dict - user data
    :param client: dict - client data
    :return: None
    '''

    # SS_02 1-2 Log out from the UI
    self.log('SS_02 1-2 Log out from the UI')

    self.logout(sec_host)
    if ssh_host is not None:
        bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGOUT,
                                                         users['user1'][USERNAME])
        self.is_true(bool_value, test_name, 'SS_02 3. Log check for logout - check failed',
                     'SS_02 3. Log check for logout')

    # SS_01 1-3 Log in to SS UI
    self.log('SS_01 1-3 Log in to SS UI')

    self.go(sec_host)
    self.login(username=sec_username, password=sec_password)
    if ssh_host is not None:
        bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGIN,
                                                         sec_username)
        self.is_true(bool_value, test_name, 'SS_01 4. Log check for login - check failed',
                     'SS_01 4. Log check for login')

    # SS_SS_28 / SS_29 / SS_30 Certification
    self.log('Create sign certificate')
    self.go(sec_host)
    self.wait_jquery()
    self.url = sec_host
    client_certification.test_generate_csr_and_import_cert(client_code=client['code'],
                                                           client_class=client['class'])(self)


def get_current_time(ssh_host, ssh_password, ssh_username):
    '''
    Gets current time from SSH server.
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH server username
    :param ssh_password: str - SSH server password
    :return: datetime - current time
    '''
    return ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password).replace(microsecond=0)


def add_member_to_cs(self, member):
    '''
    MEMBER_10 Add a new member to central server.
    :param self: MainController object
    :param member: dict - member data
    :return: None
    '''
    self.log('MEMBER_10 1. Select to add an X-Road member')
    self.click(self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID))
    self.log('Wait for the popup to be visible')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_XPATH)
    self.log('MEMBER_10 2. Insert member information.')
    self.log('Enter {0} to "member name" area'.format(member['name']))
    input_name = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID)
    self.input(input_name, member['name'])
    self.log('Select {0} from "class" dropdown'.format(member['class']))
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=members_table.ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    select.select_by_visible_text(member['class'])
    self.log('Enter {0} to "member code" area'.format(member['code']))
    input_code = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member['code'])
    self.click(self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH))
    self.log('MEMBER_10 4, 5. System verifies the new member and saves it.')


def add_services_to_client(self, ssh_host, ssh_username, ssh_password, sec_host, sec_username, sec_password, users,
                           client, wsdl_url):
    # SS_02, SS_01. Logout user2 and login as user3
    self.log('SS_02, SS_01. Logout user2 and login as user3')
    self.logout(sec_host)
    # SS_02 4. Logout logging check
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGOUT,
                                                     users['user2'][USERNAME])
    self.is_true(bool_value, test_name, 'SS_02 3. Logout logging check - check failed',
                 'SS_02 3. Logout logging check')

    # Login as user3
    self.login(username=sec_username, password=sec_password)
    # SS_01 4. Login logging check
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGIN, sec_username)
    self.is_true(bool_value, test_name, 'SS_01 4. Login logging check - check failed',
                 'SS_01 4. Login logging check')

    # SERVICE_08 Add a WSDL to a Security Server Client (5a - invalid WSDL)
    self.log('SERVICE_08 Add a WSDL to a Security Server Client (5a - invalid WSDL)')
    self.wait_jquery()
    self.click(added_client_row(self=self, client=client).find_element_by_css_selector(clients_table.SERVICES_TAB_CSS))

    # SERVICE_08 1. Select to add WSDL
    self.log('SERVICE_08 1. Select to add WSDL')
    self.click(self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ADD_WSDL_BTN_ID))
    wsdl_area = self.wait_until_visible(type=By.ID, element=popups.ADD_WSDL_POPUP_URL_ID)

    # SERVICE_08 2. Insert WSDL URL
    self.log('SERVICE_08 2. Insert WSDL URL')

    self.input(wsdl_area, self.config.get('wsdl.remote_path').format(''))  # URL that does not return a WSDL file

    # SERVICE_08 4, 5, 5a. Verify unique URL, download WSDL and try to read information; download and parse WSDL fails
    self.log(
        'SERVICE_08 4, 5, 5a. Verify unique URL, download WSDL and try to read information; download and parse WSDL ')

    self.click(self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_OK_BTN_XPATH))
    self.wait_jquery()

    # SERVICE_08 5a.2. Log check for trying to add invalid WSDL
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_WSDL_FAILED,
                                                     sec_username)
    self.is_true(bool_value, test_name, 'SERVICE_08 5a.2. Log check for trying to add invalid WSDL - check failed',
                 'SERVICE_08 5a.2. Log check for trying to add invalid WSDL')

    # SERVICE_08 5a.3. Select to reinsert correct WSDL URL
    self.log('SERVICE_08 5a.3. Select to reinsert correct WSDL URL')
    wsdl_area.clear()
    self.input(wsdl_area, wsdl_url)
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_OK_BTN_XPATH))

    # SERVICE_08 4, 5, 6, 7 Verify unique WSDL, download, read information, validate, save services
    self.log('SERVICE_08 4, 5, 6, 7 Verify unique WSDL, download, read information, validate, save services')

    self.log('Waiting 60 seconds for changes')
    time.sleep(60)

    # SERVICE_08 10. Log check for adding correct WSDL
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_WSDL, sec_username)
    self.is_true(bool_value, test_name, 'SERVICE_08 10. Log check for adding correct WSDL - check failed',
                 'SERVICE_08 10. Log check for adding correct WSDL')

    # SERVICE_19 / SERVICE_20 / SERVICE_21 Edit service URL, TLS, and timeout
    self.log('SERVICE_19 / SERVICE_20 / SERVICE_21 Edit service URL, TLS, and timeout')

    # SERVICE_21 1. Select to edit the timeout of a service.
    self.log('SERVICE_21 1. Select to edit the timeout of a service.')
    services_list = clients_table.client_services_popup_get_services_rows(self=self, wsdl_url=wsdl_url)
    self.click(services_list[0])
    self.log('Open edit WSDL service popup')
    self.click(self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID))
    self.log('Editing service parameters')
    timeout_area = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_TIMEOUT_ID)

    # SERVICE_21 2. Insert the timeout value.
    self.log('SERVICE_21 2. Insert the timeout value.')
    self.input(timeout_area, '55')

    # SERVICE_21 4, 5. Verify timeout and save the information.
    self.log('SERVICE_21 4, 5. Verify timeout and save the information.')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH))
    # SERVICE_21 6. Log check for editing service parameters
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, EDIT_SERVICE_PARAMS,
                                                     sec_username)
    self.is_true(bool_value, test_name,
                 'SERVICE_21 6. Log check for editing service parameters - check failed',
                 'SERVICE_21 6. Log check for editing service parameters')

    # SERVICE_19 1. Select to change URL and TLS verification option of a service
    self.log('SERVICE_19 1. Select to change URL and TLS verification option of a service')

    self.wait_jquery()
    self.click(self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID))
    self.log('Editing service parameters')
    service_url_input = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_URL_ID)

    # SERVICE_19 2. Insert the URL
    self.log('SERVICE_19 2. Insert the URL')
    self.input(service_url_input, self.config.get('services.test_service_url_ssl'))

    # SERVICE_19 4-6 verify URL, verify protocol, save the address
    self.log('SERVICE_19 4-6 verify URL, verify protocol, save the address')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH))
    self.wait_jquery()

    # SERVICE_20 1. Select to change TLS option of a service
    self.log('SERVICE_20 1. Select to change TLS option of a service')
    self.click(self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID))
    self.click(self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_TLS_ID))

    # SERVICE_20 2. System saves TLS info
    self.log('SERVICE_20 2. System saves TLS info')
    self.click(self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH))
    expected_log_msg = EDIT_SERVICE_PARAMS
    self.log('SERVICE_20 3. System logs "{0}" when TLS option changed'.format(expected_log_msg))
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, expected_log_msg,
                                                     sec_username)
    self.is_true(bool_value)

    # SERVICE_17 Add service subjects
    self.log('SERVICE_17 Add service subjects')

    self.go(sec_host)
    client_to_add = {'instance': ssh_server_actions.get_server_name(self), 'class': client['class'],
                     'code': client['code'], 'subsystem': client['subsystem']}
    subject = xroad.split_xroad_subsystem(self.config.get('ss1.client_id'))
    acl_subject = ' : '.join([subject['type'], subject['instance'], subject['class'],
                              subject['code'], client['subsystem']])

    add_to_acl.test_add_subjects(client=client_to_add, wsdl_index=0, service_index=0,
                                 service_subjects=[acl_subject], remove_data=False,
                                 allow_remove_all=True, case=self)


def enable_service(self, client, wsdl_url):
    '''
    SERVICE_12 Enables a service.
    :param self: MainController object
    :param client: dict - client data
    :param wsdl_url: str - WSDL URL
    :return: None
    '''
    # Find the client and open services
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.CLIENTS_BTN_CSS)
    self.click(added_client_row(self, client).find_element_by_css_selector(clients_table.SERVICES_TAB_CSS))
    self.wait_jquery()

    clients_table.client_services_popup_select_wsdl(self, wsdl_url=wsdl_url)
    # SERVICE_13 1. Select to enable the first service
    self.log('SERVICE_13 1. Select to enable the first service')
    self.wait_jquery()

    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()
    # SERVICE_13 2. System activates the WSDL
    self.log('SERVICE_13 2. System activates the WSDL')


def added_client_row(self, client):
    '''
    Finds client row from table and returns it.
    :param self: MainController object
    :param client: dict - client data
    :return: WebDriverElement - client row
    '''
    self.log('Finding added client')

    self.added_client_id = ' : '.join([client['type'], ssh_server_actions.get_server_name(self), client['class'],
                                       client['code'], client['subsystem']])
    table_rows = self.by_css(clients_table.CLIENT_ROW_CSS, multiple=True)
    client_row_index = clients_table.find_row_by_client(table_rows, client_id=self.added_client_id)
    return table_rows[client_row_index]


def add_users_to_system(ssh_host, ssh_username, ssh_password, users):
    '''
    Adds test users to system over SSH connection.
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :param users: dict - user data
    :return: None
    '''
    # Create new SSH connection
    client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
    try:
        # Add users
        user = users['user1']
        ssh_user_actions.add_user(client=client, username=user[USERNAME], password=user[PASSWORD],
                                  group=user['group'])
        user = users['user2']
        ssh_user_actions.add_user(client=client, username=user[USERNAME], password=user[PASSWORD],
                                  group=user['group'])
        user = users['user3']
        ssh_user_actions.add_user(client=client, username=user[USERNAME], password=user[PASSWORD],
                                  group=user['group'])
    finally:
        # Close SSH connection
        client.close()


def remove_users_from_system(ssh_host, ssh_username, ssh_password, users):
    '''
    Removes created users from the system.
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :param users: dict - user data
    :return: None
    '''
    client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
    try:
        ssh_user_actions.delete_user(client, username=users['user1'][USERNAME])
        ssh_user_actions.delete_user(client, username=users['user2'][USERNAME])
        ssh_user_actions.delete_user(client, username=users['user3'][USERNAME])
    finally:
        client.close()


def remove_member(self, cent_host, cent_username, cent_password, member):
    '''
    Removes member from the system.
    :param self: MainController object
    :param cent_host: str - central server hostname
    :param cent_username: str - central server UI username
    :param cent_password: str - central server UI password
    :param member: dict - member data
    :return: None
    '''
    self.reset_webdriver(cent_host, cent_username, cent_password)

    # Find members table
    self.log('Wait for members table')
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)

    # Get member row
    self.log('Get row by row values')
    row = members_table.get_row_by_columns(table, [member['name'], member['class'], member['code']])
    if row is None:
        self.log('Did not find member row')
        raise AssertionError

    # MEMBER_26 1. Select to delete a member
    self.log('MEMBER_26 1. Select to delete a member')

    # Click on the row, open details and delete member
    self.click(row)
    self.log('Click on "DETAILS" button')
    self.click(self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID))
    self.log('Click on "DELETE" button')
    self.click(self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH))

    # MEMBER_26 2. System prompts for confirmation
    self.log('MEMBER_26 2. System prompts for confirmation')

    # MEMBER_26 3. Confirm
    self.log('MEMBER_26 3. Confirm')

    popups.confirm_dialog_click(self)


def remove_client(self, client):
    '''
    Removes client from the system.
    :param self: MainController object
    :param client: dict - client data
    :return: None
    '''
    self.wait_jquery()

    # Open client details and unregister client
    self.log('Opening client details')
    self.click(added_client_row(self, client).find_element_by_css_selector(clients_table.DETAILS_TAB_CSS))
    self.wait_jquery()
    time.sleep(1)
    self.log('MEMBER_52 1-6. Unregister Client')
    is_delete_needed = False
    try:
        # Try to unregister
        self.click(self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID))
        popups.confirm_dialog_click(self)
    except:
        # Unregister failed
        is_delete_needed = True
        self.log('MEMBER_52 Not unregistering')
        self.wait_jquery()

    try:
        # Try to delete
        self.log('MEMBER_53 1-7 Deleting client')
        if is_delete_needed:
            self.click(self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID))
        self.wait_jquery()
        popups.confirm_dialog_click(self)
    except:
        # Delete failed
        traceback.print_exc()
    self.log('MEMBER_53 CLIENT DELETED')


def remove_certificate(self, client):
    '''
    Removes certificate from client.
    :param self: MainController object
    :param client: dict - client data
    :return: None
    '''
    self.log('Open "Keys and Certificates tab"')
    self.click(self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS))
    self.wait_jquery()

    certs_to_revoke = ssh_server_actions.get_valid_certificates(self, client)

    self.log('Click on generated key row')
    self.click(self.wait_until_visible(type=By.XPATH,
                                       element=keys_and_certificates_table.get_generated_key_row_xpath(client['code'],
                                                                                                       client[
                                                                                                           'class'])))
    self.click(self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID))
    popups.confirm_dialog_click(self)
    self.wait_jquery()

    return certs_to_revoke


def check_logs_for(self, ssh_host, ssh_username, ssh_password, event, user):
    '''
    Checks if an event for user was logged in the system.
    :param self: MainController object
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :param event: str - event to look for in the logs
    :param user: str - username to look for in the logs
    :return: bool - True if event was logged; False otherwise
    '''
    time.sleep(10)
    s_client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
    log = ssh_server_actions.get_log_lines(s_client, self.xroad_audit_log, 1)
    s_client.close()
    self.log(log)
    date_time = datetime.strptime(' '.join([log['date'], log['time']]), "%Y-%m-%d %H:%M:%S")
    datetime.strptime(datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S.000000"), '%Y-%m-%d %H:%M:%S.%f')
    return (log['msg_service'] == 'X-Road Proxy UI') & (log['data']['event'] == event) & \
           (log['data']['user'] == user), log['data'], date_time
