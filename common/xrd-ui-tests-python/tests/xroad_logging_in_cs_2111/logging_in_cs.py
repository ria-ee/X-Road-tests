import time
import traceback
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_server_actions, ssh_user_actions, xroad
from view_models import members_table, sidebar, groups_table, cs_security_servers, popups, messages
from view_models.log_constants import *
from view_models.messages import MEMBER_ALREADY_EXISTS_ERROR

USERNAME = 'username'
PASSWORD = 'password'

test_name = 'Logging in Central Server'


def test_test(ssh_host, ssh_username, ssh_password, users, client_id, client_name, client_name2, group, server_id,
              existing_client_id, existing_client_name):
    '''
    MainController test function. Tests maintentance actions and logging in central server.
    :param existing_client_name:  str - existing client name
    :param existing_client_id: str - existing client id
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :param users: dict - dictionary of users to be added
    :param client_id: str - client XRoad ID
    :param client_name: str - client name
    :param client_name2: str - second client name
    :param group: str - group name
    :param server_id: str - server identifier
    :return:
    '''

    def test_case(self):
        # UC MEMBER_10/MEMBER_11/MEMBER_15/MEMBER_39/MEMBER_26 Logging maintenance actions in Central Server
        self.log('*** MEMBER_10/MEMBER_11/MEMBER_15/MEMBER_39/MEMBER_26 Logging maintenance actions in Central Server')

        # Save users to MainController
        self.users = users

        # Get the first user
        user = users['user1']

        # Extract client parameters from ID, save names
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name
        client['name2'] = client_name2

        existing_client = xroad.split_xroad_subsystem(existing_client_id)
        existing_client['name'] = existing_client_name

        # Create SSH session
        ssh_client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
        self.log('SSH: Adding users to system')

        # Add test users to the system so the test can be run separately from others
        add_users_to_system(self, ssh_client)

        # By default, there is no error.
        error = False

        try:
            # UC CS_01. Log in to central server as user1
            self.log('CS_01. Log in to central server as user1')
            check_login(self, ssh_client, None, users['user1'])

            # UC MEMBER_10 Add an X-Road Member
            self.log('MEMBER_10 Add an X-Road Member')
            add_member_to_cs(self, ssh_client, user, member=client, existing_client=existing_client,
                             with_extensions=True)

            # UC MEMBER_56 Adding new subsystem to the member
            self.log('MEMBER_56 Adding new subsystem to the member')
            add_subsystem_to_member(self, ssh_client=ssh_client, user=user, member=client)

            # UC MEMBER_11 Change member name
            self.log('MEMBER_11 Change member name')
            change_member_name(self, ssh_client, user, member=client)

            # UC CS_02/CS_01 Log out, then log in to central server UI as user2
            self.log('CS_02/CS_01 Log out, then log in as user2')
            user = users['user2']
            check_login(self, ssh_client, logout_user=users['user1'], login_user=user)

            # UC SERVICE_32 Add new group (failure and success test)
            self.log('SERVICE_32 Add new group (failure and success test)')
            add_group(self, ssh_client, user, group, try_empty=True)

            # UC SERVICE_33 Add the new subsystem to the new group
            self.log('SERVICE_33 Add the new subsystem to the new group')
            add_client_to_group(self, ssh_client, user, member=client, group=group)

            # UC MEMBER_15 Add new registration request for the new subsystem
            self.log('MEMBER_15 Add new registration request for the new subsystem')
            self.driver.get(self.url)
            register_subsystem_to_security_server(self, ssh_client, user, member=client, server_id=server_id)

            self.log('Wait 120 seconds for sync')
            time.sleep(120)

            # UC CS_02/CS_01 log out, then log in to central server UI as user3
            self.log('CS_02/CS_01 log out, then log in as user3')
            user = users['user3']
            check_login(self, ssh_client, logout_user=users['user2'], login_user=user)

            # UC MEMBER_39 Revoke the registration request for the new subsystem
            self.log('MEMBER_39 Revoke the registration request for the new subsystem')
            remove_subsystem_registration_request(self, ssh_client, user, server_id)

            # UC MEMBER_26 Delete the member from central server
            self.log('MEMBER_26 Delete the member from central server')
            delete_client(self, ssh_client, user, member=client, cancel_deletion=True)
        except:
            # Had an error, set error to be True and print traceback.
            traceback.print_exc()
            self.save_exception_data(exctrace=traceback)
            error = True
        finally:
            # Always remove data
            try:
                # Remove test data that may have been partially created on error
                if error:
                    # Remove member
                    try:
                        # UC MEMBER_26 Delete the member from central server
                        self.log('MEMBER_26 Delete the member from central server')
                        delete_client(self, ssh_client, user, member=client)
                    except:
                        self.log('MEMBER_26 Deleting member failed')

                    # Revoke all requests (loop until done)
                    try:
                        self.log('MEMBER_39 Revoking requests')
                        self.reset_webdriver(self.config.get('cs.host'), self.config.get('cs.user'),
                                             self.config.get('cs.pass'))
                        self.wait_jquery()
                        self.wait_until_visible(type=By.CSS_SELECTOR,
                                                element=sidebar.MANAGEMENT_REQUESTS_CSS).click()
                        self.wait_jquery()
                        time.sleep(5)

                        try:
                            td = self.by_xpath(members_table.get_requests_row_by_td_text('SUBMITTED FOR APPROVAL'))
                        except:
                            td = None

                        try:
                            while td is not None:
                                td.click()
                                self.wait_until_visible(type=By.ID,
                                                        element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
                                self.wait_jquery()
                                time.sleep(1)
                                self.log('MEMBER_39 Revoking request')
                                self.wait_until_visible(type=By.XPATH,
                                                        element=members_table.DECLINE_REQUEST_BTN_XPATH).click()
                                self.wait_jquery()
                                popups.confirm_dialog_click(self)
                                time.sleep(5)
                                try:
                                    td = self.by_xpath(
                                        members_table.get_requests_row_by_td_text('SUBMITTED FOR APPROVAL'))
                                except:
                                    td = None
                        except:
                            traceback.print_exc()


                    except:
                        self.log('MEMBER_39 Revoking requests and deleting client failed')
            except:
                self.log('Deleting client failed')
            try:
                self.log('SERVICE_39 Deleting global group')
                remove_group(self, group)
            except:
                self.log('SERVICE_39 Deleting group failed')
            self.log('Closing SSH connection')
            ssh_client.close()
            if error:
                # Got an error before, fail the test
                assert False, 'Test failed'

    return test_case


def add_member_to_cs(self, ssh_client, user, member, existing_client=None, with_extensions=False):
    '''
    Adds a new member to central server and checks logs for this action.
    :param with_extensions:
    :param existing_client:
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param member: dict - member data
    :return: None
    '''

    '''Open add dialog'''
    self.log('MEMBER_10 1. Add member button is pressed')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()
    self.log('Wait for the popup to be visible')
    self.wait_jquery()
    if with_extensions:
        self.log('MEMBER_10 4.a member with the inserted class and code already exists')
        self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_XPATH)
        '''Existing member parameters'''
        existing_member_name = existing_client['name']
        existing_member_class = existing_client['class']
        existing_member_code = existing_client['code']
        self.log('MEMBER_10 2. Member adding popup is filled')
        self.log('Enter {0} to "member name" area'.format(existing_member_name))
        input_name = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID)
        self.input(input_name, existing_member_name)
        self.log('Select {0} from "class" dropdown'.format(existing_member_class))
        select = Select(self.wait_until_visible(type=By.ID,
                                                element=members_table.ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID))
        select.select_by_visible_text(existing_member_class)
        self.log('Enter {0} to "member code" area'.format(existing_member_code))
        input_code = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID)
        self.input(input_code, existing_member_code)

        self.log('Click OK')
        self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        expected_error_msg = MEMBER_ALREADY_EXISTS_ERROR.format(existing_member_class, existing_member_code)
        self.log('MEMBER_10 4a.1 System displays the error message "{0}"'.format(expected_error_msg))
        error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
        self.is_equal(expected_error_msg, error_msg)

        expected_log_msg = ADD_MEMBER_FAILED
        bool_value, data, date_time = check_logs_for(ssh_client, expected_log_msg, user[USERNAME])
        self.is_true(bool_value, test_name=test_name,
                     msg='{0} not found in audit log'.format(expected_log_msg),
                     log_message='MEMBER_10 4a.3 CS System logs the event "{0}"'.format(expected_log_msg))

    self.log('MEMBER_10 2. Filling member adding popup')
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
    self.wait_jquery()

    expected_log_msg = ADD_MEMBER
    bool_value, data, date_time = check_logs_for(ssh_client, expected_log_msg, user[USERNAME])
    self.is_true((bool_value & (str(data['data']['memberCode']) == member['code'])), test_name,
                 msg='{0} not found in audit log'.format(expected_log_msg),
                 log_message='MEMBER_10 7. System logs the event "{0}"'.format(expected_log_msg))


def add_subsystem_to_member(self, member, user=None, ssh_client=None):
    '''
    Adds a subsystem to an existing member. Checks if the action was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param member: dict - member data
    :return: None
    '''

    # Open member details
    self.driver.get(self.url)
    self.wait_jquery()
    open_member_details(self, member=member)

    # UC MEMBER_56 1. Select to add a subsystem to X-Road member
    self.log('MEMBER_56 1. Select to add a subsystem to X-Road member')

    # Open subsystem tab
    self.log('Open Subsystem tab')
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()
    self.wait_jquery()

    # Add new subsystem
    self.log('Open Add new Subsystem to member')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_SUBSYSTEM_BTN_ID).click()

    # UC MEMBER_56 2. Enter subsystem code
    self.log('MEMBER_56 2. Enter subsystem code')
    subsystem_input = self.wait_until_visible(type=By.ID, element=members_table.SUBSYSTEM_CODE_AREA_ID)
    self.input(subsystem_input, member['subsystem'])

    # Save data
    self.log('Confirm adding subsystem, click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_OK_BTN_XPATH).click()

    # UC MEMBER_56 4, 5. System verifies new subsystem and saves it
    self.log('MEMBER_56 4, 5. System verifies new subsystem and saves it')

    if ssh_client is not None:
        # UC MEMBER_56 check logs for added subsystem
        bool_value, data, date_time = check_logs_for(ssh_client, ADD_SUBSYSTEM, user[USERNAME])
        self.is_true((bool_value & (str(data['data']['memberCode']) == member['code'])), test_name,
                     'MEMBER_56 6. Check logs for added subsystem - check failed',
                     'MEMBER_56 6. Check logs for added subsystem')


def change_member_name(self, ssh_client, user, member):
    """
    Change existing member name.
    Checks if the action was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param member: dict - member data
    :return: None
    """
    self.driver.get(self.url)
    open_member_details(self, member=member)
    self.log('MEMBER_11 1. Clicking edit member name button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_NAME_EDIT_BTN_XPATH).click()
    self.wait_jquery()

    edit_member_area = self.wait_until_visible(type=By.XPATH,
                                               element=members_table.MEMBER_EDIT_NAME_POPUP_EDIT_NAME_AREA_XPATH)
    self.log('MEMBER_11 2. New member name is inserted')
    member['name'] = member['name2']
    self.input(edit_member_area, member['name'])
    self.log('Clicking OK')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # UC MEMBER_11 4. System saves the changes
    self.log('MEMBER_11 4. System saves the changes')

    expected_log_msg = EDIT_MEMBER_NAME
    bool_value, data, date_time = check_logs_for(ssh_client, expected_log_msg, user[USERNAME])
    self.is_true(bool_value, test_name,
                 log_message='MEMBER_11 5. System logs the event "{0}"'.format(expected_log_msg),
                 msg='MEMBER_11 5. "{0}" not found in audit log'.format(expected_log_msg))


def add_group(self, ssh_client, user, group, try_empty=False):
    '''
    Adds a new global group to the system. First tries to add with empty values, then with the correct ones.
    Checks if the action was logged.
    :param try_empty: bool - try adding group with empty fields
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param group: str - group name
    :return: None
    '''
    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    # UC SERVICE_32 1. Select to add global group
    self.log('SERVICE_32 1. Select to add global group')
    self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).click()

    if try_empty:
        # UC SERVICE_32 3a. Leave required fields empty
        self.log('SERVICE_32 3a. Leave required fields empty')
        self.log('Click on "OK" to add new group')
        self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        # UC SERVICE_32 Check logs for group add failure
        bool_value, data, date_time = check_logs_for(ssh_client, ADD_GLOBAL_GROUP_FAILED, user[USERNAME])
        self.is_true(bool_value, test_name,
                     'SERVICE_32 3a.2. Log check for trying to add group - check failed',
                     'SERVICE_32 3a.2. Log check for trying to add group')

    # UC SERVICE_32 2, 3. Fill in required fields
    self.log('SERVICE_32 2, 3. Fill in required fields')

    self.log('Send {0} to code area input'.format(group))
    group_code_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_CODE_AREA_ID)
    self.input(group_code_input, group)
    self.log('Send {0} to code description input'.format(group))
    group_description_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DESCRIPTION_AREA_ID)
    self.input(group_description_input, group)

    self.log('Click on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # UC SERVICE_32 4, 5. System verifies new group and saves it
    self.log('SERVICE_32 4, 5. System verifies new group and saves it')

    # UC SERVICE_32 6. Check global group adding in logs
    bool_value, data, date_time = check_logs_for(ssh_client, ADD_GLOBAL_GROUP, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'SERVICE_32 6. Log check for added group - check failed',
                 'SERVICE_32 6. Log check for added group')


def add_client_to_group(self, ssh_client, user, member, group):
    '''
    Adds a member to a group and checks if it was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param member: dict - member data
    :param group: str - group name
    :return: None
    '''
    self.driver.get(self.url)
    self.wait_jquery()

    # Open member details
    open_member_details(self, member=member)
    self.wait_until_visible(type=By.XPATH, element=members_table.GLOBAL_GROUP_TAB).click()
    self.wait_jquery()

    # UC SERVICE_33 1. Select to add group members to global group
    self.log('SERVICE_33 1. Select to add group members to global group')

    # Add member to global group
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_TO_GLOBAL_GROUP_BTN_ID).click()
    self.wait_jquery()
    time.sleep(10)

    # UC SERVICE_33 2. Select subjects and add them to group
    self.log('SERVICE_33 2. Select subjects and add them to group')

    # Set settings and values
    select = Select(self.wait_until_visible(type=By.ID, element=members_table.GROUP_SELECT_ID))
    select.select_by_visible_text(group)
    self.wait_until_visible(type=By.XPATH, element=members_table.GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # UC SERVICE_33 3. System adds the members to group.
    self.log('SERVICE_33 3. System adds the members to group.')

    bool_value, data, date_time = check_logs_for(ssh_client, ADD_MEMBER_TO_GROUP, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'SERVICE_33 4. Check logs for adding member to group - check failed',
                 'SERVICE_33 4. Check logs for adding member to group')


def register_subsystem_to_security_server(self, ssh_client, user, member, server_id):
    '''
    Registers a subsystem to security server and checks if it was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param member: dict - member and subsystem data
    :param server_id: str - server identifier
    :return: None
    '''
    # Go to UI main page
    self.driver.get(self.url)
    self.wait_jquery()

    # Open security server details
    self.log('Open Security server details popup')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.get_row_by_td_text(server_id)).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENT_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_CLIENT_TAB).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_CLIENT_TO_SECURITYSERVER_BTN_ID).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SEARCH_BTN_ID).click()
    self.wait_jquery()

    # Open clients tab
    self.log('Open security servers clients tab')
    table = self.wait_until_visible(type=By.ID, element=cs_security_servers.MEMBERS_TABLE_ID)
    self.wait_jquery()

    # Find the member from the table and click the row
    members_table.get_row_by_columns(table,
                                     [member['name'], member['code'], member['class'], member['subsystem'],
                                      ssh_server_actions.get_server_name(self),
                                      'SUBSYSTEM']).click()
    self.wait_jquery()
    time.sleep(1)
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SELECT_MEMBER_BTN_XPATH).click()
    self.wait_jquery()

    # UC MEMBER_15 1. Select to create a registration request
    self.log('MEMBER_15 1. Select to create a registration request')
    self.wait_until_visible(type=By.ID,
                            element=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID).click()
    self.wait_jquery()

    # UC MEMBER_15 5-8. Check if request can be sent.
    self.log('MEMBER_15 5-8. Check if request can be sent.')

    # UC MEMBER_15 Check if registering client to security server was logged
    bool_value, data, date_time = check_logs_for(ssh_client, REGISTER_MEMBER_AS_SEC_SERVER_CLIENT, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'MEMBER_15 10. Log check for registering client to security server - check failed',
                 'MEMBER_15 10. Log check for registering client to security server',
                 )


def remove_subsystem_registration_request(self, ssh_client, user, server_id):
    """
    Revokes a registration request for a client and checks if it was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param server_id: str - server identifier
    :return:
    """

    # Go to UI main page
    self.driver.get(self.url)
    self.wait_jquery()

    # Open security server details popup
    self.log('Open Security server details popup')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.get_row_by_td_text(server_id)).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENT_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_MANAGEMENT_REQUESTS_TAB).click()
    self.wait_jquery()

    # Open management requests
    self.log('Open management requests tab')
    table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITYSERVER_MANAGEMENT_REQUESTS_TABLE_ID)
    self.wait_jquery()

    # Get the latest requests
    tr = table.find_elements_by_tag_name('tr')[1]
    self.log('Clicking request index')
    tr.find_element_by_tag_name('a').click()

    # UC MEMBER_39 1. Select to revoke registration request
    self.log('MEMBER_39 1. Select to revoke registration request')
    self.wait_jquery()
    time.sleep(10)
    self.wait_until_visible(type=By.XPATH,
                            element=cs_security_servers.REVOKE_CLIENT_MANAGEMENT_REQUEST_BTN_XPATH).click()

    # UC MEMBER_39 2. System prompts for confirmation
    self.log('MEMBER_39 2. System prompts for confirmation')

    # UC MEMBER_39 3. Confirm revoking request
    self.log('MEMBER_39 3. Confirm revoking request')
    popups.confirm_dialog_click(self)

    # UC MEMBER_39 4, 5. System creates a deletion request and revokes the registration request
    self.log('MEMBER_39 4, 5. System creates a deletion request and revokes the registration request')

    # UC MEMBER_39 Check if revoking the request was logged
    bool_value, data, date_time = check_logs_for(ssh_client, REVOKE_CLIENT_REGISTRATION_REQUEST, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'MEMBER_39 4 7. Log check for revoking request - check failed',
                 'MEMBER_39 4 7. Log check for revoking request',
                 )


def remove_group(self, group):
    '''
    Removes a global group from the system.
    :param self: MainController object
    :param group: str - group name
    :return: None
    '''
    # Open global groups
    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    # Find and select the group
    self.log('Select added group')
    table = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_TABLE_ID)
    rows = table.find_elements_by_tag_name('tr')
    for row in rows:
        if row.text != '':
            if row.find_element_by_tag_name('td').text == group:
                row.click()
                self.wait_jquery()

    # Open group details and delete the group
    self.log('Open group details')
    self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DETAILS_BTN_ID).click()
    self.wait_jquery()

    # UC SERVICE_39 1. Select to delete a global group
    self.log('SERVICE_39 1. Select to delete a global group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.DELETE_GROUP_BTN_ID).click()
    self.wait_jquery()

    # UC SERVICE_39 2. System prompts for confirmation
    self.log('SERVICE_39 2. System prompts for confirmation')

    # UC SERVICE_39 3. Confirm deletion
    self.log('SERVICE_39 3. Confirm deletion')
    popups.confirm_dialog_click(self)


def delete_client(self, ssh_client, user, member, cancel_deletion=False):
    '''
    Deletes a member from the system. Checks if the action was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param member: dict - member data
    :return: None
    '''
    self.driver.get(self.url)
    self.wait_jquery()
    # Open member details
    open_member_details(self, member=member)

    # UC MEMBER_26 1. Select to delete the member
    self.log('MEMBER_26 1. Select to delete the member')

    # Delete the member
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.wait_jquery()
    '''MEMBER_26 3a cancel central server member deletion'''
    if cancel_deletion:
        self.log('Cancel member deletion')
        self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        self.log('Click delete button again')
        self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()

    # UC MEMBER_26 2. System prompts for confirmation
    self.log('MEMBER_26 2. System prompts for confirmation')

    # UC MEMBER_26 3. Confirm deletion
    self.log('MEMBER_26 3. Confirm deletion')

    popups.confirm_dialog_click(self)
    time.sleep(10)

    # UC MEMBER_26 4-7. System verifies that the member can be deleted and deletes it.
    self.log('MEMBER_26 4-7. System verifies that the member can be deleted and deletes it.')

    # UC MEMBER_26 8. Check if deleting the member was logged
    bool_value, data, date_time = check_logs_for(ssh_client, DELETE_MEMBER, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'MEMBER_26 8. Log check for deleting the member - check failed',
                 'MEMBER_26 8. Log check for deleting the member')


def add_users_to_system(self, ssh_client):
    '''
    Adds test users to system over SSH connection.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :return:
    '''
    user = self.users['user1']
    ssh_user_actions.add_user(client=ssh_client, username=user[USERNAME], password=user[PASSWORD],
                              group=user['group'])
    user = self.users['user2']
    ssh_user_actions.add_user(client=ssh_client, username=user[USERNAME], password=user[PASSWORD],
                              group=user['group'])
    user = self.users['user3']
    ssh_user_actions.add_user(client=ssh_client, username=user[USERNAME], password=user[PASSWORD],
                              group=user['group'])


def check_login(self, ssh_client, logout_user=None, login_user=None):
    '''
    Login function that also checks if it succeeded. If specified, first logs the user out from existing session.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param logout_user: dict|None - user data for user that should be logged out; None if logout is not necessary
    :param login_user: dict|None - user data for user logging in; None if login not necessary
    :return: None
    '''
    # Login and logout checks (all users)

    if logout_user is not None:
        self.log('CS_02 1-2. Checking logout')
        self.logout()

        # Check logs
        bool_value, data, date_time = check_logs_for(ssh_client, LOGOUT, logout_user[USERNAME])
        self.is_true(bool_value, test_name,
                     'CS_02 3. Log check for logging out - check failed', 'CS_02 3. Log check for logging out',
                     )
    if login_user is not None:
        self.log('CS_01 1-4. Checking login')
        if logout_user is None:
            # Log out the previous user if not yet logged out
            self.logout()

        # Log in the new user
        self.login(login_user[USERNAME], login_user[PASSWORD])

        # Check logs
        bool_value, data, date_time = check_logs_for(ssh_client=ssh_client, event=LOGIN, user=login_user[USERNAME])
        self.is_true(bool_value, test_name,
                     'CS_01 4. Log check for logging in - check failed',
                     'CS_01 4. Log check for logging in')


def check_logs_for(ssh_client, event, user):
    '''
    Checks if an event for user was logged in the system.
    :param ssh_client: SSHClient object
    :param event: str - event to look for in the logs
    :param user: str - username to look for in the logs
    :return: bool - True if event was logged; False otherwise
    '''
    print('Checking logs for {0}'.format(event))
    # Wait 15 seconds for sync
    time.sleep(15)
    log = ssh_server_actions.get_log_lines(ssh_client, LOG_FILE_LOCATION, 1)
    date_time = datetime.strptime(' '.join([log['date'], log['time']]), "%Y-%m-%d %H:%M:%S")
    datetime.strptime(datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S.000000"), '%Y-%m-%d %H:%M:%S.%f')
    return (str(log['msg_service']) == MSG_SERVICE_CENTER) & (str(log['data']['event']) == event) & \
           (str(log['data']['user']) == user), log['data'], date_time


def open_member_details(self, member):
    '''
    Opens member details in the user interface.
    :param self: MainController object
    :param member: dict - member data
    :return: None
    '''
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()
    row = members_table.get_row_by_columns(table, [member['name'], member['class'], member['code']])
    if row is None:
        self.log('Member not found')
        pass
    # Click the row. Raises an exception if member was not found. This can be caught outside of this function if necessary.
    row.click()
    self.wait_jquery()
    self.log('Open Member Details')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()
