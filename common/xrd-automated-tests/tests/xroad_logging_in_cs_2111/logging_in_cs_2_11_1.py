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
    def test_case(self):
        self.users = users
        user = users['user1']
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name
        client['name2'] = client_name2

        ssh_client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
        self.log('Adding users to system')
        add_users_to_system(self, ssh_client)

        error = False
        try:

            check_login(self, ssh_client, None, users['user1'])

            add_member_to_cs(self, ssh_client, user, member=client)
            add_subsystem_to_member(self, ssh_client, user, member=client)
            change_member_name(self, ssh_client, user, member=client)

            user = users['user2']
            check_login(self, ssh_client, logout_user=users['user1'], login_user=user)
            add_group(self, ssh_client, user, group)
            add_client_to_group(self, ssh_client, user, member=client, group=group)
            self.driver.get(self.url)
            register_subsystem_to_security_server(self, ssh_client, user, member=client, server_id=server_id)
            user = users['user3']
            check_login(self, ssh_client, logout_user=users['user2'], login_user=user)
            remove_subsystem_registration_request(self, ssh_client, user, server_id)
            delete_client(self, ssh_client, user, member=client)

        except:
            traceback.print_exc()
            error = True
        finally:
            try:
                if error:
                    try:
                        delete_client(self, ssh_client, user, member=client)
                    except:
                        self.log('Deleting client failed')

                    try:
                        self.reset_webdriver(self.config.get('cs.host'), self.config.get('cs.user'),
                                             self.config.get('cs.pass'))
                        self.wait_jquery()
                        self.log('REVOKING REQUESTS')
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
                                self.log('Revoke requests')
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
                        self.log('Deleting client failed')
            except:
                self.log('Deleting client failed')
            try:
                remove_group(self, group)
            except:
                self.log('Deleting group failed')
            self.log('Close client')
            ssh_client.close()
            if error:
                assert False

    return test_case


def add_member_to_cs(self, ssh_client, user, member):
    self.log('Wait for the "ADD" button and click')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()
    self.log('Wait for the popup to be visible')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_XPATH)
    self.log('Enter {0} to "member name" area'.format(member['name']))
    input_name = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID)
    # input_name.send_keys(member['name'])
    self.input(input_name, member['name'])
    self.log('Select {0} from "class" dropdown'.format(member['class']))
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=members_table.ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    select.select_by_visible_text(member['class'])
    self.log('Enter {0} to "member code" area'.format(member['code']))
    input_code = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID)
    # input_code.send_keys(member['code'])
    self.input(input_code, member['code'])
    self.log('Click "OK" to add member')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    bool_value, data, date_time = check_logs_for(ssh_client, ADD_MEMBER, user[USERNAME])
    self.is_true((bool_value & (str(data['data']['memberCode']) == member['code'])), test_name,
                 'CHECK LOGS FAILED FOR ADDING  CLIENT', 'CHECK LOGS FOR ADDING MEMBER')


def add_subsystem_to_member(self, ssh_client, user, member):
    self.driver.get(self.url)
    self.wait_jquery()
    open_member_details(self, member=member)
    self.log('Open Subsystem Tab')
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()
    self.wait_jquery()
    self.log('Open Add new Subsystem to member')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_SUBSYSTEM_BTN_ID).click()
    self.log('Insert "sub" to "Subsystem Code" area')
    subsystem_input = self.wait_until_visible(type=By.ID, element=members_table.SUBSYSTEM_CODE_AREA_ID)
    self.input(subsystem_input, member['subsystem'])
    self.log('Confirm adding subsystem, click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_OK_BTN_XPATH).click()
    bool_value, data, date_time = check_logs_for(ssh_client, ADD_SUBSYSTEM, user[USERNAME])
    self.is_true((bool_value & (str(data['data']['memberCode']) == member['code'])), test_name,
                 'CHECK LOGS FAILED FOR ADDING  SUBSYSTEM', 'CHECK LOGS FOR ADDING SUBSYSTEM')


def change_member_name(self, ssh_client, user, member):
    self.driver.get(self.url)
    self.log('CHANGE MEMBER NAME LOG TEST')
    open_member_details(self, member=member)
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_NAME_EDIT_BTN_XPATH).click()
    self.wait_jquery()
    edit_member_area = self.wait_until_visible(type=By.XPATH,
                                               element=members_table.MEMBER_EDIT_NAME_POPUP_EDIT_NAME_AREA_XPATH)
    edit_member_area.clear()
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    time.sleep(5)
    error = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
    self.is_equal(error, 'Missing parameter: memberName', test_name,
                  'ERROR MESSAGE IS NOT SHOWN, MESSAGE: {0}'.format(error),
                  'CHECK IF ERROR MESSAGE IS SHOWN, EXPECTED {0}'.format('Missing parameter: memberName'))

    bool_value, data, date_time = check_logs_for(ssh_client, EDIT_MEMBER_NAME_FAILED, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'CHECK LOGS FAILED FOR CHANGING NAME CHANGE FAILURE', 'CHECK LOGS FOR MEMBER NAME CHANGE FAILURE')

    member['name'] = member['name2']
    self.input(edit_member_area, member['name'])
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    bool_value, data, date_time = check_logs_for(ssh_client, EDIT_MEMBER_NAME, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'CHECK LOGS FAILED FOR CHANGING NAME CHANGE', 'CHECK LOGS FOR MEMBER NAME CHANGE')


def add_group(self, ssh_client, user, group):
    self.log('ADD GROUP TEST')
    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    self.log('Click "ADD" to add new group')
    self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).click()
    self.log('CLick on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    bool_value, data, date_time = check_logs_for(ssh_client, ADD_GLOBAL_GROUP_FAILED, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'CHECK LOGS FAILED FOR ADD GROUP CHANGE FAILURE', 'CHECK LOGS FOR ADD GROUP FAILURE')

    self.log('Send {0} to code area input'.format(group))
    group_code_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_CODE_AREA_ID)
    self.input(group_code_input, group)
    self.log('Send {0} to code descriptionz input'.format(group))
    group_description_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DESCRIPTION_AREA_ID)
    self.input(group_description_input, group)

    self.log('CLick on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    bool_value, data, date_time = check_logs_for(ssh_client, ADD_GLOBAL_GROUP, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'CHECK LOGS FAILED FOR ADD GROUP CHANGE', 'CHECK LOGS FOR ADD GROUP')


def add_client_to_group(self, ssh_client, user, member, group):
    self.driver.get(self.url)
    self.wait_jquery()
    self.log('ADD CLIENT TO GROUP TEST')
    open_member_details(self, member=member)
    self.wait_until_visible(type=By.XPATH, element=members_table.GLOBAL_GROUP_TAB).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_TO_GLOBAL_GROUP_BTN_ID).click()
    self.wait_jquery()
    time.sleep(10)
    select = Select(self.wait_until_visible(type=By.ID, element=members_table.GROUP_SELECT_ID))
    select.select_by_visible_text(group)
    self.wait_until_visible(type=By.XPATH, element=members_table.GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    bool_value, data, date_time = check_logs_for(ssh_client, ADD_MEMBER_TO_GROUP, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'CHECK LOGS FAILED FOR  ADDING MEMBER TO GROUP GROUP', 'CHECK LOGS FOR ADDING MEMBER TO GROUP GROUP')


def register_subsystem_to_security_server(self, ssh_client, user, member, server_id):
    self.driver.get(self.url)
    self.wait_jquery()
    self.log('REGISTER CLIENT TO SECURITY SERVER TEST')
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
    self.log('Open security servers clients tab')
    table = self.wait_until_visible(type=By.ID, element=cs_security_servers.MEMBERS_TABLE_ID)
    self.wait_jquery()
    members_table.get_row_by_columns(table,
                                     [member['name'], member['code'], member['class'], member['subsystem'],
                                      ssh_server_actions.get_server_name(self),
                                      'SUBSYSTEM']).click()
    self.wait_jquery()
    time.sleep(1)
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SELECT_MEMBER_BTN_XPATH).click()
    self.wait_jquery()
    self.log('Register client to security server')
    self.wait_until_visible(type=By.ID,
                            element=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID).click()
    self.wait_jquery()
    bool_value, data, date_time = check_logs_for(ssh_client, REGISTER_MEMBER_AS_SEC_SERVER_CLIENT, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'CHECK LOGS FAILED FOR REGISTERING CLIENT TO SECURITY SERVER',
                 'CHECK LOGS FOR REGISTERING CLIENT TO SECURITY SERVER',
                 )


def remove_subsystem_registration_request(self, ssh_client, user, server_id):
    self.driver.get(self.url)
    self.wait_jquery()
    self.log('REMOVE CLIENT REGISTRATION REQUEST')
    self.log('Open Security server details popup')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.get_row_by_td_text(server_id)).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENT_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_MANAGEMENT_REQUESTS_TAB).click()
    self.wait_jquery()
    self.log('Open management requests tab')
    table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITYSERVER_MANAGEMENT_REQUESTS_TABLE_ID)
    self.wait_jquery()
    tr = table.find_elements_by_tag_name('tr')[1]
    self.log('Clicking request index')
    tr.find_element_by_tag_name('a').click()
    self.log('Revoke request by clicking "REVOKE" button')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.REVOKE_MANAGEMENT_REQUEST_BTN_XPATH).click()
    self.log('Confirm revoking request')
    popups.confirm_dialog_click(self)
    bool_value, data, date_time = check_logs_for(ssh_client, REVOKE_CLIENT_REGISTRATION_REQUEST, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'CHECK LOGS FAILED FOR REVOKING REQUEST', 'CHECK LOGS FOR REVOKING REQUEST',
                 )


def remove_group(self, group):
    self.log('REMOVE GROUP')
    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    self.log('Select added group')
    table = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_TABLE_ID)
    rows = table.find_elements_by_tag_name('tr')
    for row in rows:
        if row.text != '':
            if row.find_element_by_tag_name('td').text == group:
                row.click()
                self.wait_jquery()
    self.log('Open group details')
    self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.log('Click on "DELETE GROUP" button')
    self.wait_until_visible(type=By.XPATH, element=groups_table.DELETE_GROUP_BTN_ID).click()
    self.wait_jquery()
    self.log('Confirm deletion')
    popups.confirm_dialog_click(self)


def delete_client(self, ssh_client, user, member):
    self.driver.get(self.url)
    self.log('DELETING MEMBER TEST')
    self.wait_jquery()
    open_member_details(self, member=member)
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.wait_jquery()
    popups.confirm_dialog_click(self)
    time.sleep(10)
    bool_value, data, date_time = check_logs_for(ssh_client, DELETE_MEMBER, user[USERNAME])
    self.is_true(bool_value, test_name,
                 'CHECK LOGS FAILED FOR DELETING CLIENT', 'CHECK LOGS FOR DELETING CLIENT')


def add_users_to_system(self, ssh_client):
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
    if logout_user is not None:
        self.log('CHECKING LOG OUT')
        self.logout()
        bool_value, data, date_time = check_logs_for(ssh_client, LOGOUT, logout_user[USERNAME])
        self.is_true(bool_value, test_name,
                     'CHECK LOGS FAILED FOR LOG OUT', 'CHECK LOGS FOR LOG OUT',
                     )
    if login_user is not None:
        self.log('CHECKING LOG IN')
        if logout_user is None:
            self.logout()
        self.login(login_user[USERNAME], login_user[PASSWORD])
        bool_value, data, date_time = check_logs_for(ssh_client=ssh_client, event=LOGIN, user=login_user[USERNAME])
        self.is_true(bool_value, test_name,
                     'CHECK LOGS FAILED FOR LOG IN',
                     'CHECK LOGS FOR LOG IN')


def check_logs_for(ssh_client, event, user):
    print 'checking logs for {0}'.format(event)
    print 'Waiting 15 second for logs sync'
    time.sleep(15)
    log = ssh_server_actions.get_log_lines(ssh_client, LOG_FILE_LOCATION, 1)
    date_time = datetime.strptime(' '.join([log['date'], log['time']]), "%Y-%m-%d %H:%M:%S")
    datetime.strptime(datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S.000000"), '%Y-%m-%d %H:%M:%S.%f')
    print log['data']
    return (str(log['msg_service']) == MSG_SERVICE_CENTER) & (str(log['data']['event']) == event) & \
           (str(log['data']['user']) == user), log['data'], date_time


def open_member_details(self, member):
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()
    row = members_table.get_row_by_columns(table, [member['name'], member['class'], member['code']])
    if row is None:
        pass
    row.click()
    self.wait_jquery()
    self.log('Open Member Details')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()
