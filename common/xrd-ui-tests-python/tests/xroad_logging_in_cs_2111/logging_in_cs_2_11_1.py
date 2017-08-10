import time
import traceback
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_server_actions, ssh_user_actions, xroad
from view_models import members_table, sidebar, groups_table, cs_security_servers, popups, messages
from view_models.log_constants import *

USERNAME = 'username'
PASSWORD = 'password'

test_name = 'LOGGING IN CENTRAL SERVER'


def test_test(ssh_host, ssh_username, ssh_password, users, client_id, client_name, client_name2, group, server_id):
    '''
    MainController test function. Tests maintentance actions and logging in central server.
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
        # TEST PLAN 2.11.1 logging maintenance actions in central server
        self.log('*** 2.11.1 / XT-518')

        # Save users to MainController
        self.users = users

        # Get the first user
        user = users['user1']

        # Extract client parameters from ID, save names
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name
        client['name2'] = client_name2

        # Create SSH session
        ssh_client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
        self.log('Adding users to system')

        # Add test users to the system so the test can be run separately from others
        add_users_to_system(self, ssh_client)

        # By default, there is no error.
        error = False

        try:
            # TEST PLAN 2.11.1-1 log in to central server UI as user1
            self.log('2.11.1-1 logging in to central server as user1')
            check_login(self, ssh_client, None, users['user1'])

            # TEST PLAN 2.11.1-2 adding new member to central server
            self.log('2.11.1-2 adding new member to central server')
            add_member_to_cs(self, ssh_client, user, member=client)

            # TEST PLAN 2.11.1-3 adding new subsystem to the member
            self.log('2.11.1-3 adding new subsystem to the member')
            add_subsystem_to_member(self, ssh_client, user, member=client)

            # TEST PLAN 2.11.1-4, 2.11.1-5 change member name (empty and non-empty)
            self.log('2.11.1-4, 2.11.1-5 change member name (empty and non-empty)')
            change_member_name(self, ssh_client, user, member=client)

            # TEST PLAN 2.11.1-6 log out and then log in to central server UI as user2
            self.log('2.11.1-6 logging out, then logging in as user2')
            user = users['user2']
            check_login(self, ssh_client, logout_user=users['user1'], login_user=user)

            # TEST PLAN 2.11.1-7, 2.11.1-8 add new group (failure and success test)
            self.log('2.11.1-7, 2.11.1-8 add new group (failure and success test)')
            add_group(self, ssh_client, user, group)

            # TEST PLAN 2.11.1-9 add the new subsystem to the new group
            self.log('2.11.1-9 add the subsystem to the new group')
            add_client_to_group(self, ssh_client, user, member=client, group=group)

            # TEST PLAN 2.11.1-10 add new registration request for the new subsystem
            self.log('2.11.1-10 add new registration request for the new subsystem')
            self.driver.get(self.url)
            register_subsystem_to_security_server(self, ssh_client, user, member=client, server_id=server_id)
            self.log('wait 120 for effect')
            time.sleep(120)
            # TEST PLAN 2.11.1-11 log out, then log in to central server as user3
            self.log('2.11.1-11 log out, then log in to central server as user3')
            user = users['user3']
            check_login(self, ssh_client, logout_user=users['user2'], login_user=user)

            # TEST PLAN 2.11.1-12 remove the registration request for the new subsystem
            self.log('2.11.1-12 remove the registration request for the new subsystem')
            remove_subsystem_registration_request(self, ssh_client, user, server_id)

            # TEST PLAN 2.11.1-13 delete the member from central server
            self.log('2.11.1-13 delete the member from central server')
            delete_client(self, ssh_client, user, member=client)

            # TEST PLAN 2.11.1-14 checks are done in the corresponding functions.
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
                        self.log('2.11.1-del remove member')
                        delete_client(self, ssh_client, user, member=client)
                    except:
                        self.log('2.11.1-del removing member failed')

                    # Revoke all requests (loop until done)
                    try:
                        self.log('2.11.1-del revoking requests')
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
                                self.log('2.11.1-del revoking request')
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
                        self.log('2.11.1-del Deleting client failed')
            except:
                self.log('2.11.1-del Deleting client failed')
            try:
                self.log('2.11.1-del Deleting group')
                remove_group(self, group)
            except:
                self.log('2.11.1-del Deleting group failed')
            self.log('2.11.1-del closing SSH connection')
            ssh_client.close()
            if error:
                # Got an error before, fail the test
                assert False, '2.11.1 failed'

    return test_case


def add_member_to_cs(self, ssh_client, user, member):
    '''
    Adds a new member to central server and checks logs for this action.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param member: dict - member data
    :return: None
    '''

    # Open add dialog
    self.log('Wait for the "ADD" button and click')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()
    self.log('Wait for the popup to be visible')
    self.wait_jquery()

    # Enter data
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

    # Save data
    self.log('Click "OK" to add member')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # TEST PLAN 2.11.1-14 check logs for added member
    bool_value, data, date_time = check_logs_for(ssh_client, ADD_MEMBER, user[USERNAME])
    self.is_true((bool_value & (str(data['data']['memberCode']) == member['code'])), test_name,
                 '2.11.1-2/2.11.1-14 checking logs for added member - check failed',
                 '2.11.1-2/2.11.1-14 checking logs for added member')


def add_subsystem_to_member(self, ssh_client, user, member):
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

    # Open subsystem tab
    self.log('Open Subsystem tab')
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()
    self.wait_jquery()

    # Add new subsystem
    self.log('Open Add new Subsystem to member')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_SUBSYSTEM_BTN_ID).click()

    # Enter data
    self.log('Insert "sub" to "Subsystem Code" area')
    subsystem_input = self.wait_until_visible(type=By.ID, element=members_table.SUBSYSTEM_CODE_AREA_ID)
    self.input(subsystem_input, member['subsystem'])

    # Save data
    self.log('Confirm adding subsystem, click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_OK_BTN_XPATH).click()

    # TEST PLAN 2.11.1-14 check logs for added subsystem
    bool_value, data, date_time = check_logs_for(ssh_client, ADD_SUBSYSTEM, user[USERNAME])
    self.is_true((bool_value & (str(data['data']['memberCode']) == member['code'])), test_name,
                 '2.11.1-3/2.11.1-14 check logs for added subsystem - check failed',
                 '2.11.1-3/2.11.1-14 check logs for added subsystem')


def change_member_name(self, ssh_client, user, member):
    '''
    Change existing member name. First try to set an empty name, then try with the correct one.
    Checks if the action was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param member: dict - member data
    :return: None
    '''
    self.driver.get(self.url)
    # TEST PLAN 2.11.1-4 change member name and set an empty name
    self.log('2.11.1-4 change member name, set empty name')

    # Open member details and edit member
    open_member_details(self, member=member)
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_NAME_EDIT_BTN_XPATH).click()
    self.wait_jquery()

    # Set empty name
    edit_member_area = self.wait_until_visible(type=By.XPATH,
                                               element=members_table.MEMBER_EDIT_NAME_POPUP_EDIT_NAME_AREA_XPATH)
    edit_member_area.clear()

    # Try to save
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    time.sleep(5)

    # Get error message
    error = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text

    # TEST PLAN 2.11.1-4 check if correct error message is shown
    self.is_equal(error, 'Missing parameter: memberName', test_name,
                  '2.11.1-4 error message is not shown, message: {0}'.format(error),
                  '2.11.1-4 check if error message is shown, expected: {0}'.format('Missing parameter: memberName'))

    # TEST PLAN 2.11.1-14 check logs for editing member name failure
    bool_value, data, date_time = check_logs_for(ssh_client, EDIT_MEMBER_NAME_FAILED, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-4/2.11.1-14 log check for member name change failure - check failed',
                 '2.11.1-4/2.11.1-14 log check for member name change failure')

    # TEST PLAN 2.11.1-5 change member name and set a correct new name
    self.log('2.11.1-5 change member name, set new name')
    member['name'] = member['name2']
    self.input(edit_member_area, member['name'])
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    # TEST PLAN 2.11.1-14 check logs for successful member name change
    bool_value, data, date_time = check_logs_for(ssh_client, EDIT_MEMBER_NAME, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-5/2.11.1-14 log check for member name change - check failed',
                 '2.11.1-5/2.11.1-14 log check for member name change')


def add_group(self, ssh_client, user, group):
    '''
    Adds a new global group to the system. First tries to add with empty values, then with the correct ones.
    Checks if the action was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param group: str - group name
    :return: None
    '''
    # TEST PLAN 2.11.1-7 try to add new group, leave required fields empty
    self.log('2.11.1-7 add new group, leave required fields empty')
    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    # Start adding new group
    self.log('Click "ADD" to add new group')
    self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).click()
    self.log('Click on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # TEST PLAN 2.11.1-14 check logs for group add failure
    bool_value, data, date_time = check_logs_for(ssh_client, ADD_GLOBAL_GROUP_FAILED, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-7/2.11.1-14 log check for trying to add group - check failed',
                 '2.11.1-7/2.11.1-14 log check for trying to add group')

    # TEST PLAN 2.11.1-8 fill in required fields and try again
    self.log('2.11.1-8 add new group, fill in required fields')
    self.log('Send {0} to code area input'.format(group))
    group_code_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_CODE_AREA_ID)
    self.input(group_code_input, group)
    self.log('Send {0} to code description input'.format(group))
    group_description_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DESCRIPTION_AREA_ID)
    self.input(group_description_input, group)

    self.log('Click on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # TEST PLAN 2.11.1-14 check if adding group actions have been logged
    bool_value, data, date_time = check_logs_for(ssh_client, ADD_GLOBAL_GROUP, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-8/2.11.1-14 log check for added group - check failed',
                 '2.11.1-8/2.11.1-14 log check for added group')


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

    # Add member to global group
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_TO_GLOBAL_GROUP_BTN_ID).click()
    self.wait_jquery()
    time.sleep(10)

    # Set settings and values
    select = Select(self.wait_until_visible(type=By.ID, element=members_table.GROUP_SELECT_ID))
    select.select_by_visible_text(group)
    self.wait_until_visible(type=By.XPATH, element=members_table.GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # TEST PLAN 2.11.1-14 check logs for adding member to group
    bool_value, data, date_time = check_logs_for(ssh_client, ADD_MEMBER_TO_GROUP, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-9/2.11.1-14 check logs for adding member to group - check failed',
                 '2.11.1-9/2.11.1-14 check logs for adding member to group')


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

    # Register the client
    self.log('Register client to security server')
    self.wait_until_visible(type=By.ID,
                            element=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID).click()
    self.wait_jquery()

    # TEST PLAN 2.11.1-14 check if registering client to security server was logged
    bool_value, data, date_time = check_logs_for(ssh_client, REGISTER_MEMBER_AS_SEC_SERVER_CLIENT, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-10/2.11.1-14 log check for registering client to security server - check failed',
                 '2.11.1-10/2.11.1-14 log check for registering client to security server',
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
    self.log('2.11.1-12: Open Security server details popup')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.get_row_by_td_text(server_id)).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENT_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_MANAGEMENT_REQUESTS_TAB).click()
    self.wait_jquery()

    # Open management requests
    self.log('2.11.1-12: Open management requests tab')
    table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITYSERVER_MANAGEMENT_REQUESTS_TABLE_ID)
    self.wait_jquery()

    # Get the latest requests
    tr = table.find_elements_by_tag_name('tr')[1]
    self.log('2.11.1-12: Clicking request index')
    tr.find_element_by_tag_name('a').click()

    # Revoke the request
    self.log('2.11.1-12: Revoke request by clicking "REVOKE" button')
    self.wait_jquery()
    time.sleep(10)
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.REVOKE_MANAGEMENT_REQUEST_BTN_XPATH).click()

    # Confirm
    self.log('2.11.1-12: Confirm revoking request')
    popups.confirm_dialog_click(self)

    # TEST PLAN 2.11.1-14 check if revoking the request was logged
    bool_value, data, date_time = check_logs_for(ssh_client, REVOKE_CLIENT_REGISTRATION_REQUEST, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-12/2.11.1-14 log check for revoking request - check failed',
                 '2.11.1-12/2.11.1-14 log check for revoking request',
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
    self.log('Click on "DELETE GROUP" button')
    self.wait_until_visible(type=By.XPATH, element=groups_table.DELETE_GROUP_BTN_ID).click()
    self.wait_jquery()
    self.log('Confirm deletion')
    popups.confirm_dialog_click(self)


def delete_client(self, ssh_client, user, member):
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
    # Delete the member
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.wait_jquery()
    # Confirm deletion
    popups.confirm_dialog_click(self)
    time.sleep(10)

    # TEST PLAN 2.11.1-13/2.11.1-14 check if deleting the member was logged
    bool_value, data, date_time = check_logs_for(ssh_client, DELETE_MEMBER, user[USERNAME])
    self.is_true(bool_value, test_name,
                 '2.11.1-13/2.11.1-14 log check for deleting the member - check failed',
                 '2.11.1-13/2.11.1-14 log check for deleting the member')


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
    # TEST PLAN 2.11.1-14 login and logout checks (all users)

    if logout_user is not None:
        self.log('Checking logout')
        self.logout()

        # Check logs
        bool_value, data, date_time = check_logs_for(ssh_client, LOGOUT, logout_user[USERNAME])
        self.is_true(bool_value, test_name,
                     'Log check for logging out - check failed', 'Log check for logging out',
                     )
    if login_user is not None:
        self.log('Checking login')
        if logout_user is None:
            # Log out the previous user if not yet logged out
            self.logout()

        # Log in the new user
        self.login(login_user[USERNAME], login_user[PASSWORD])

        # Check logs
        bool_value, data, date_time = check_logs_for(ssh_client=ssh_client, event=LOGIN, user=login_user[USERNAME])
        self.is_true(bool_value, test_name,
                     'Log check for logging in - check failed',
                     'Log check for logging in')


def check_logs_for(ssh_client, event, user):
    '''
    Checks if an event for user was logged in the system.
    :param ssh_client: SSHClient object
    :param event: str - event to look for in the logs
    :param user: str - username to look for in the logs
    :return: bool - True if event was logged; False otherwise
    '''
    print 'Checking logs for {0}'.format(event)
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
