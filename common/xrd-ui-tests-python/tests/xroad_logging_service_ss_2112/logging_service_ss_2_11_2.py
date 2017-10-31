import time
import traceback
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_server_actions, ssh_user_actions, xroad, auditchecker
from tests.xroad_add_to_acl_218 import add_to_acl_2_1_8
from tests.xroad_ss_client_certification_213 import client_certification_2_1_3
from view_models import popups as popups, members_table, clients_table_vm as clients_table, sidebar, \
    keys_and_certificates_table, messages, groups_table
from view_models.log_constants import *
from view_models.messages import MISSING_PARAMETER, INPUT_EXCEEDS_255_CHARS

USERNAME = 'username'
PASSWORD = 'password'

test_name = 'LOGGING IN SECURITY SERVER'


def test_test(ssh_host, ssh_username, ssh_password,
              cs_host, cs_username, cs_password,
              sec_host, sec_username, sec_password,
              users, client_id, client_name, wsdl_url):
    '''
    MainController test function. Tests maintentance actions and logging in central server.
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :param cs_host: str - central server hostname
    :param cs_username: str - central server UI username
    :param cs_password: str - central server UI password
    :param sec_host: str - security server hostname
    :param sec_username: str - security server UI username
    :param sec_password: str - security server UI password
    :param users: dict - dictionary of users to be added
    :param client_id: str - client XRoad ID
    :param client_name: str - client name
    :param wsdl_url: str - WSDL URL
    :return:
    '''

    def test_case(self):
        # TEST PLAN 2.11.2 logging maintenance actions in security server
        self.log('*** 2.11.2 / XT-519')
        error = False
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name
        try:
            # TEST PLAN 2.11.2-1 adding new member to central server
            self.log('2.11.2-1 adding new member to central server')
            add_member_to_cs(self, member=client)

            # TEST PLAN 2.11.2-2 add users to Security Server with service administrator rights
            self.log('2.11.2-2 add users to Security Server with service administrator rights')
            add_users_to_system(ssh_host, ssh_username, ssh_password, users)

            self.log('Wait 120 seconds before continuing with security server')
            time.sleep(120)

            self.log('USER 1 ACTIONS')
            user = users['user1']

            # TEST PLAN 2.11.2-3, 2.11.2-4 log in to security server UI as user1; add new subsystem as client
            self.log('2.11.2-3, 2.11.2-4 log in to security server UI as user1; add new subsystem as client')
            add_client_to_ss(self=self, sec_host=sec_host, sec_username=user[USERNAME],
                             sec_password=user[PASSWORD], ssh_host=ssh_host, ssh_username=ssh_username,
                             ssh_password=ssh_password, client=client)

            self.log('SERVICE_25 Add a Local Group for a Security Server Client')
            add_group_to_client(self=self, sec_host=sec_host, sec_username=user[USERNAME], sec_password=user[PASSWORD],
                                ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password, client=client)

            self.logout(sec_host)
            self.login(username=user[USERNAME], password=user[PASSWORD])
            user = users['user2']

            # TEST PLAN 2.11.2-6, 2.11.2-7 log in as user2, certify client
            self.log('2.11.2-6, 2.11.2-7 log in as user2, certify client')
            certify_client_in_ss(self, sec_host, user[USERNAME], user[PASSWORD],
                                 client, users, ssh_host, ssh_username, ssh_password)
            self.url = cs_host

            self.logout(sec_host)
            self.login(users['user2'][USERNAME], users['user2'][PASSWORD])

            # TEST PLAN 2.11.2-8, 2.11.2-9, 2.11.2-10, 2.11.2-11, 2.11.2-12 log in as user3 and add WSDL to client
            self.log('2.11.2-8, 2.11.2-9, 2.11.2-10, 2.11.2-11, 2.11.2-12 add WSDL to client')
            user = users['user3']
            add_services_to_client(self, ssh_host, ssh_username, ssh_password, sec_host, user[USERNAME], user[PASSWORD],
                                   users, client, wsdl_url)

            # TEST PLAN 2.11.2-13 enable WSDL
            self.log('2.11.2-13 enable WSDL')
            enable_service(self, client, wsdl_url)

            # TEST PLAN 2.11.2-14 checks are done in the corresponding functions.
        except:
            traceback.print_exc()
            error = True

        finally:
            # Remove added data
            remove_data(self=self, ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password,
                        cs_host=cs_host, cs_username=cs_username, cs_password=cs_password, sec_host=sec_host,
                        sec_username=sec_username, sec_password=sec_password, users=users, client=client)
            if error:
                assert False, '2.11.2 failed'

    return test_case


def remove_data(self, ssh_host, ssh_username, ssh_password, cs_host, cs_username, cs_password, sec_host, sec_username,
                sec_password, users, client):
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
    :param users: dict - dictionary of users to be added
    :param client: dict - client data
    :return: None
    '''

    self.log('2.11.2-del removing test data')
    # Try to remove member
    try:
        self.log('2.11.2-del removing member')
        remove_member(self, cs_host, cs_username, cs_password, member=client)
    except:
        self.log('2.11.2-del ERROR {0}'.format(traceback.format_exc()))
        self.log('2.11.2-del Removing member failed')

    # Try to remove certificate
    try:
        self.log('2.11.2-del removing certificate')
        self.reset_webdriver(sec_host, sec_username, sec_password)
        remove_certificate(self, client)
    except:
        self.log('2.11.2-del ERROR {0}'.format(traceback.format_exc()))
        self.log('2.11.2-del Removing certicate failed')

    # Try to remove client
    try:
        self.log('2.11.2-del removing client')
        self.reset_webdriver(sec_host, sec_username, sec_password)
        remove_client(self, client)
    except:
        self.log('2.11.2-del ERROR {0}'.format(traceback.format_exc()))
        self.log('2.11.2-del Removing client failed')

    # Try to remove users
    try:
        self.log('2.11.2-del removing users')
        remove_users_from_system(ssh_host, ssh_username, ssh_password, users)
    except:
        self.log('2.11.2-del ERROR {0}'.format(traceback.format_exc()))
        self.log('2.11.2-del Removing users failed')


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

    # TEST PLAN 2.11.2-3 log in to security server
    self.log('2.11.2-3 log in to security server')
    self.driver.get(sec_host)
    self.login(username=sec_username, password=sec_password)

    # TEST PLAN 2.11.2-3/2.11.2-14 check logs for login
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGIN, sec_username)
    self.is_true(bool_value)

    # Add client
    self.log('Click on "ADD CLIENT" button')
    self.wait_until_visible(type=By.ID, element=clients_table.ADD_CLIENT_BTN_ID).click()
    self.log('Wait until ADD CLIENT dialog is open')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_XPATH)

    # Set data
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
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    time.sleep(3)
    # TEST PLAN 2.11.2-4/2.11.2-14 check logs for adding client
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_CLIENT,
                                                     sec_username)

    self.is_true(bool_value, test_name, '2.11.2-4/2.11.2-14 log check for adding client - check failed',
                 '2.11.2-4/2.11.2-14 log check for adding client')

    time.sleep(5)
    self.log('Confirm registration')
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
    added_client_row(self, client).find_element_by_css_selector(clients_table.LOCAL_GROUPS_TAB_CSS).click()
    self.log('Check if local groups table is empty and contains expected message')
    self.is_not_none(self.by_xpath(groups_table.LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH.format('No (matching) records')))
    self.log('SERVICE_25 1. Click on group add button')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_GROUP_ADD_BTN_ID).click()
    self.log('Confirm group adding popup')
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()
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
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()
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
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()
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
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()
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
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()
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
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_GROUP_ADD_BTN_ID).click()
    self.log('Filling group adding popup with already existing group info')
    group_add_code_input = self.by_id(popups.GROUP_ADD_POPUP_CODE_AREA_ID)
    self.input(element=group_add_code_input, text=group_name)
    group_add_description_input = self.by_id(popups.GROUP_ADD_POPUP_CODE_DESCRIPTION_ID)
    self.input(element=group_add_description_input, text=group_name)
    self.log('Confirm popup')
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()
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
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()
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
    self.logout(sec_host)
    if ssh_host is not None:
        bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGOUT,
                                                         users['user1'][USERNAME])
        self.is_true(bool_value, test_name, '2.11.2-6/2.11.2-14 log check for logout - check failed',
                     '2.11.2-6/2.11.2-14 log check for logout')

    self.driver.get(sec_host)
    self.login(username=sec_username, password=sec_password)
    if ssh_host is not None:
        bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGIN,
                                                         sec_username)
        self.is_true(bool_value, test_name, '2.11.2-6/2.11.2-14 log check for login - check failed',
                     '2.11.2-6/2.11.2-14 log check for login')

    # TEST PLAN 2.11.2-7 certification
    self.log('2.11.2-7 Create sign certificate')
    self.driver.get(sec_host)
    self.wait_jquery()
    self.url = sec_host
    client_certification_2_1_3.test_generate_csr_and_import_cert(client_code=client['code'],
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
    Adds a new member to central server.
    :param self: MainController object
    :param member: dict - member data
    :return: None
    '''
    self.log('Wait for the "ADD" button and click')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()
    self.log('Wait for the popup to be visible')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_XPATH)
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
    self.log('Click "OK" to add member')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()


def add_services_to_client(self, ssh_host, ssh_username, ssh_password, sec_host, sec_username, sec_password, users,
                           client, wsdl_url):
    # TEST PLAN 2.11.2-8 logout user2 and login as user3
    self.log('2.11.2-8 logout user2 and login as user3')
    self.logout(sec_host)
    # TEST PLAN 2.11.2-14 logout logging check
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGOUT,
                                                     users['user2'][USERNAME])
    self.is_true(bool_value, test_name, '2.11.2-8/2.11.2-14 logout logging check - check failed',
                 '2.11.2-8/2.11.2-14 logout logging check')

    # Login as user3
    self.login(username=sec_username, password=sec_password)
    # TEST PLAN 2.11.2-14 login logging check
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGIN, sec_username)
    self.is_true(bool_value, test_name, '2.11.2-8/2.11.2-14 login logging check - check failed',
                 '2.11.2-8/2.11.2-14 login logging check')
    # TEST PLAN 2.11.2-9 trying to add invalid WSDL to client
    self.log('2.11.2-9 trying to add invalid WSDL to client')
    self.wait_jquery()
    added_client_row(self=self, client=client).find_element_by_css_selector(clients_table.SERVICES_TAB_CSS).click()
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ADD_WSDL_BTN_ID).click()
    wsdl_area = self.wait_until_visible(type=By.ID, element=popups.ADD_WSDL_POPUP_URL_ID)
    self.input(wsdl_area, self.config.get('wsdl.remote_path').format(''))  # URL that does not return a WSDL file
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # TEST PLAN 2.11.2-14 log check for trying to add invalid WSDL
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_WSDL_FAILED,
                                                     sec_username)
    self.is_true(bool_value, test_name, '2.11.2-9/2.11.2-14 log check for trying to add invalid WSDL - check failed',
                 '2.11.2-9/2.11.2-14 log check for trying to add invalid WSDL')

    # TEST PLAN 2.11.2-10 trying to add correct WSDL to client
    self.log('2.11.2-10 trying to add correct WSDL to client')
    wsdl_area.clear()
    self.input(wsdl_area, wsdl_url)
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_OK_BTN_XPATH).click()
    self.log('Waiting 60 seconds for changes')
    time.sleep(60)
    # TEST PLAN 2.11.2-14 log check for adding correct WSDL
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_WSDL, sec_username)
    self.is_true(bool_value, test_name, '2.11.2-10/2.11.2-14 log check for adding correct WSDL - check failed',
                 '2.11.2-10/2.11.2-14 log check for adding correct WSDL')

    # TEST PLAN 2.11.2-11 edit service parameters
    self.log('2.11.2-11 edit service parameters')
    services_list = clients_table.client_services_popup_get_services_rows(self=self, wsdl_url=wsdl_url)
    services_list[0].click()
    self.log('Open edit wsdl service popup')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()
    self.log('Editing service parameters')
    timeout_area = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_TIMEOUT_ID)
    self.input(timeout_area, '55')
    self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
    # TEST PLAN 2.11.2-14 log check for editing service parameters
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, EDIT_SERVICE_PARAMS,
                                                     sec_username)
    self.is_true(bool_value, test_name,
                 '2.11.2-11/2.11.2-14 log check for editing service parameters - check failed',
                 '2.11.2-11/2.11.2-14 log check for editing service parameters')

    self.log('Change service url protocol to https, so TLS checkbox can be changed')
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()
    self.log('Editing service parameters')
    service_url_input = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_URL_ID)
    self.input(service_url_input, self.config.get('services.test_service_url_ssl'))
    self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    self.log('Open edit wsdl service popup')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()
    self.log('Editing service parameters')
    self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_TLS_ID).click()
    self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
    expected_log_msg = EDIT_SERVICE_PARAMS
    self.log('SERVICE_20 3. System logs "{0}" when TLS option changed'.format(expected_log_msg))
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, expected_log_msg,
                                                     sec_username)
    self.is_true(bool_value)

    # TEST PLAN 2.11.2-12 set service access rights
    self.log('2.11.2-12 set service access rights')
    self.driver.get(sec_host)

    client_to_add = {'instance': ssh_server_actions.get_server_name(self), 'class': client['class'],
                     'code': client['code'], 'subsystem': client['subsystem']}
    subject = xroad.split_xroad_subsystem(self.config.get('ss1.client_id'))
    acl_subject = ' : '.join([subject['type'], subject['instance'], subject['class'],
                              subject['code'], client['subsystem']])

    add_to_acl_2_1_8.test_add_subjects(client=client_to_add, wsdl_index=0, service_index=0,
                                       service_subjects=[acl_subject], remove_data=False,
                                       allow_remove_all=True, case=self)


def enable_service(self, client, wsdl_url):
    '''
    Enables a service.
    :param self: MainController object
    :param client: dict - client data
    :param wsdl_url: str - WSDL URL
    :return: None
    '''
    # Find the client and open services
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.CLIENTS_BTN_CSS)
    added_client_row(self, client).find_element_by_css_selector(clients_table.SERVICES_TAB_CSS).click()
    services_list = clients_table. \
        client_services_popup_get_services_rows(self=self, wsdl_url=wsdl_url)
    # Enable the first service
    services_list[0].click()
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()


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
        raise

    # Click on the row, open details and delete member
    row.click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.log('Confirm deleting member')
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
    added_client_row(self, client).find_element_by_css_selector(clients_table.DETAILS_TAB_CSS).click()
    self.wait_jquery()
    time.sleep(1)
    self.log('Unregister Client')
    is_delete_needed = False
    try:
        # Try to unregister
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
        popups.confirm_dialog_click(self)
    except:
        # Unregister failed
        is_delete_needed = True
        self.log('Not unregistering')
        self.wait_jquery()

    try:
        # Try to delete
        self.log('Deleting client')
        if is_delete_needed:
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
        self.wait_jquery()
        popups.confirm_dialog_click(self)
    except:
        # Delete failed
        traceback.print_exc()
    self.log('CLIENT DELETED')


def remove_certificate(self, client):
    '''
    Removes certificate from client.
    :param self: MainController object
    :param client: dict - client data
    :return: None
    '''
    self.log('Open "Keys and Certificates tab"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.log('Click on generated key row')
    self.wait_until_visible(type=By.XPATH,
                            element=keys_and_certificates_table.get_generated_key_row_xpath(client['code'],
                                                                                            client[
                                                                                                'class'])).click()
    self.wait_until_visible(type=By.ID, element=keys_and_certificates_table.DELETE_BTN_ID).click()
    popups.confirm_dialog_click(self)
    self.wait_jquery()


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
