import traceback
import sys

import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_client, ssh_user_actions, ssh_server_actions, xroad
from view_models import popups as popups, members_table

USERNAME = 'username'
PASSWORD = 'password'


def test_test(ssh_host, ssh_username, ssh_password, users, client_id, client_name, client_name2):
    test_name = 'CHANGING DATABASE ROWS WITH INTERFACE, SECURITY SERVER'

    def test_case(self):
        error = False
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name
        client['name2'] = client_name2
        self.users = users

        try:
            add_users_to_system(self, ssh_host, ssh_username, ssh_password)

            # Users actions and saving times
            before_created_at = ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password)
            user_1_actions(self, client)
            after_created_at = ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password)
            user_2_actions(self, client)
            after_edited_at = ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password)
            user_3_actions(self, client)
            after_deleted_at = ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password)

            # self.log('Waiting 30 for database changes')
            # time.sleep(30)

            client = get_client(ssh_host, users['databaseuser'][USERNAME], users['databaseuser'][PASSWORD])
            output = []

            try:
                output, out_error = ssh_server_actions.get_history_for_user(client, users['databaseuser'][USERNAME],
                                                                            users['databaseuser']['db_name'],
                                                                            users['user1'][USERNAME], 2)

                for data in get_formated_data(output):
                    self.is_true(before_created_at <= datetime.datetime.strptime(data['timestamp'],
                                                                                 "%Y-%m-%d %H:%M:%S.%f") <= after_created_at,
                                 test_name, 'Database rows have not been changed for user1',
                                 'Testing if database rows have been changed for user1'
                                 )

                output, out_error = ssh_server_actions.get_history_for_user(client, users['databaseuser'][USERNAME],
                                                                            users['databaseuser']['db_name'],
                                                                            users['user2'][USERNAME], 2)
                for data in get_formated_data(output):
                    self.is_true(after_created_at <= datetime.datetime.strptime(data['timestamp'],
                                                                                "%Y-%m-%d %H:%M:%S.%f") <= after_edited_at,
                                 test_name, 'Database rows have not been changed for user2',
                                 'Testing if database rows have been changed for user2'
                                 )

                output, out_error = ssh_server_actions.get_history_for_user(client, users['databaseuser'][USERNAME],
                                                                            users['databaseuser']['db_name'],
                                                                            users['user3'][USERNAME], 3)
                for data in get_formated_data(output):
                    self.is_true(after_edited_at <= datetime.datetime.strptime(data['timestamp'],
                                                                               "%Y-%m-%d %H:%M:%S.%f") <= after_deleted_at,
                                 test_name, 'Database rows have not been changed for user3',
                                 'Testing if database rows have been changed for user3'
                                 )

            except:
                self.log('Could not parse string {0}, {1}'.format(output, out_error))
                error = True
            finally:
                self.log('Closing client')
                client.close()
                if error:
                    traceback.print_exc()
                    assert False

        except:
            traceback.print_exc(file=sys.stdout)
            remove_added_data(self, client)
        finally:
            remove_users_from_system(self, ssh_host, ssh_username, ssh_password)

    return test_case


def remove_added_data(self, client):
    user_3_actions(self, client)


def user_1_actions(self, client):
    self.log('Log in with user1')
    self.logout()
    self.login(username=self.users['user1'][USERNAME], password=self.users['user1'][PASSWORD])
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()

    member_name_area = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID)
    select = Select(
        self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    member_code_area = self.wait_until_visible(type=By.ID,
                                               element=members_table.ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID)

    self.log('Write {0} to MEMBER NAME area'.format(client['name']))
    self.input(member_name_area, client['name'])
    self.members_current_name = client['name']
    self.log('Select {0} class to member'.format(client['class']))
    select.select_by_visible_text(client['class'])
    self.log('Write {0} to MEMBER CODE area'.format(client['code']))
    self.input(member_code_area, client['code'])
    self.log('Click OK')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()


def user_2_actions(self, client):
    self.log('Log in with user2')
    self.logout()
    self.login(username=self.users['user2'][USERNAME], password=self.users['user2'][PASSWORD])
    member_row = added_member_row(self, client)
    if member_row:
        member_row.click()
    else:
        self.log('Could not find row')
    self.log('Opening client details')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.log('Click on "EDIT" BUTTON')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_NAME_EDIT_BTN_XPATH).click()
    # Select name area
    member_name_area = self.wait_until_visible(type=By.XPATH,
                                               element=members_table.MEMBER_EDIT_NAME_POPUP_EDIT_NAME_AREA_XPATH)
    self.log('Changing name')
    self.input(member_name_area, client['name2'])
    self.members_current_name = client['name2']
    self.log('Saving name by clicking "OK"')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH).click()


def user_3_actions(self, client):
    self.log('Log in with user3')
    self.logout()
    self.login(username=self.users['user3'][USERNAME], password=self.users['user3'][PASSWORD])
    member_row = added_member_row(self, client)
    if member_row:
        member_row.click()
    else:
        self.log('Could not find row')
        pass
    self.log('Opening client details')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.log('Deleting client')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    popups.confirm_dialog_click(self)
    self.log('CLIENT DELETED')
    self.gui_data_deleted = True


def added_member_row(self, client):
    self.log('Finding added client')
    self.wait_jquery()
    self.wait_until_visible(type=By.CSS_SELECTOR, element=members_table.MEMBERS_TABLE_ROWS_CSS)
    table_rows = self.by_css(members_table.MEMBERS_TABLE_ROWS_CSS, multiple=True)

    for row in table_rows:
        if (row.find_elements_by_css_selector('td')[0].text == self.members_current_name) & \
                (row.find_elements_by_css_selector('td')[1].text == client['class']) & \
                (row.find_elements_by_css_selector('td')[2].text == client['code']):
            return row


def add_users_to_system(self, ssh_host, ssh_username, ssh_password):
    client = get_client(ssh_host, ssh_username, ssh_password)
    try:
        ssh_user_actions.add_user(client=client, username=self.users['user1'][USERNAME],
                                  password=self.users['user1'][PASSWORD],
                                  group=self.users['user1']['group'])
        ssh_user_actions.add_user(client=client, username=self.users['user2'][USERNAME],
                                  password=self.users['user2'][PASSWORD],
                                  group=self.users['user2']['group'])
        ssh_user_actions.add_user(client=client, username=self.users['user3'][USERNAME],
                                  password=self.users['user3'][PASSWORD],
                                  group=self.users['user3']['group'])
        ssh_user_actions.add_user(client, self.users['databaseuser'][USERNAME], self.users['databaseuser'][PASSWORD])
    finally:
        client.close()


def remove_users_from_system(self, ssh_host, ssh_username, ssh_password):
    client = get_client(ssh_host, ssh_username, ssh_password)
    try:
        ssh_user_actions.delete_user(client, username=self.users['user1'][USERNAME])
        ssh_user_actions.delete_user(client, username=self.users['user2'][USERNAME])
        ssh_user_actions.delete_user(client, username=self.users['user3'][USERNAME])
        ssh_user_actions.delete_user(client, username=self.users['databaseuser'][USERNAME])
    finally:
        client.close()


def get_client(ssh_host, ssh_username, ssh_password):
    return ssh_client.SSHClient(ssh_host, username=ssh_username, password=ssh_password)


def get_formated_data(output):
    data = []
    for line in output:
        splitted_line = line.split(',')
        data.append({'operation': splitted_line[0],
                     'table_name': splitted_line[1],
                     'timestamp': splitted_line[2]})
    return data
