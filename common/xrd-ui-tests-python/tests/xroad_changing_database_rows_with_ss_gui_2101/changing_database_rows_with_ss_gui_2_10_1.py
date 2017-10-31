import traceback
import time

import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_client, ssh_user_actions, ssh_server_actions, xroad
from view_models import popups as popups, clients_table_vm as clients_table_vm, messages

USERNAME = 'username'
PASSWORD = 'password'


def test_test(ssh_host, ssh_username, ssh_password, users, client_id):
    '''
    MainController test function. Checks security server UI edits against corresponding database changes.
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :param users: dict - dictionary of users to be added
    :param client_id: str - client XRoad ID
    :return:
    '''
    test_name = '2.10.1 CHANGING DATABASE ROWS WITH INTERFACE, SECURITY SERVER'

    def test_case(self):
        # TEST PLAN 2.10.1 changing database rows with interface, security server
        self.log('*** 2.10.1 / XT-514')

        error = False
        client = xroad.split_xroad_subsystem(client_id)

        # TEST PLAN 2.10.1-1, 2.10.1-2 add new users to system and set them to be registration officers
        self.log('2.10.1-1, 2.10.1-2 add new users to system and set them to be registration officers')
        add_users_to_system(ssh_host, ssh_username, ssh_password, users)

        db_user = users['databaseuser'][USERNAME]
        db_name = users['databaseuser']['db_name']
        try:
            # Users actions and saving times
            before_created_at = ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password)

            # TEST PLAN 2.10.1-3, 2.10.1-4 log in with user1, add new client
            self.log('2.10.1-3, 2.10.1-4 log in with user1, add new client')
            user_1_actions(self, users['user1'], client)
            after_created_at = ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password)

            # TEST PLAN 2.10.1-5, 2.10.1-6 log in with user2, edit client
            self.log('2.10.1-5, 2.10.1-6 log in with user2, edit client')
            user_2_actions(self, users['user2'], client)
            after_edited_at = ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password)

            # TEST PLAN 2.10.1-7, 2.10.1-8 log in with user3, delete client
            self.log('2.10.1-7, 2.10.1-8 log in with user3, delete client')
            user_3_actions(self, users['user3'], client)
            after_deleted_at = ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password)

            # TEST PLAN 2.10.1-9 connect to database and check for user action rows
            self.log('2.10.1-9 connect to database and check for user action rows')
            sshclient = get_client(ssh_host, users['databaseuser'][USERNAME], users['databaseuser'][PASSWORD])
            try:

                sshclient.exec_command(
                    'psql -U {0} -d {1} -c "delete from identifier where membercode like \'{2}\' and subsystemcode like \'{3}\'"'.format(
                        db_user, db_name, client['code'], client['subsystem']))

                output, out_error = ssh_server_actions.get_history_for_user(sshclient, db_user, db_name,
                                                                            users['user1'][USERNAME], 1)

                for data in get_formatted_data(output):
                    self.is_true(before_created_at <= datetime.datetime.strptime(data['timestamp'],
                                                                                 "%Y-%m-%d %H:%M:%S.%f") <= after_created_at,
                                 test_name, 'Database rows have not been changed for user1',
                                 'Testing if database rows have been changed for user1'
                                 )

                output, out_error = ssh_server_actions.get_history_for_user(sshclient, db_user, db_name,
                                                                            users['user2'][USERNAME], 1)
                for data in get_formatted_data(output):
                    self.is_true(after_created_at <= datetime.datetime.strptime(data['timestamp'],
                                                                                "%Y-%m-%d %H:%M:%S.%f") <= after_edited_at,
                                 test_name,
                                 'Database rows have not been changed for user2',
                                 'Testing if database rows have been changed for user2'
                                 )

                output, out_error = ssh_server_actions.get_history_for_user(sshclient, db_user, db_name,
                                                                            users['user3'][USERNAME], 1)
                for data in get_formatted_data(output):
                    self.is_true(after_edited_at <= datetime.datetime.strptime(data['timestamp'],
                                                                               "%Y-%m-%d %H:%M:%S.%f") <= after_deleted_at,
                                 test_name,
                                 'Database rows have not been changed for user3',
                                 'Testing if database rows have been changed for user3'
                                 )
            except:
                traceback.print_exc()
                error = True
            finally:
                if not error:
                    self.log('Closing client')
                    sshclient.close()

        except:
            traceback.print_exc()

            remove_added_data(self, users, client)
            error = True
        finally:
            if error:
                remove_users_from_system(ssh_host, ssh_username, ssh_password, users)
                assert False, '2.10.1 failed'

    return test_case


def remove_added_data(self, users, client):
    '''
    Removes data added during testing.
    :param self: MainController object
    :param users: dict - user data
    :param client: dict - client data
    :return: None
    '''
    user_3_actions(self, users['user3'], client)


def user_1_actions(self, user, client):
    '''
    Executes actions with user1.
    :param self: MainController object
    :param user: dict - user data
    :param client: dict - client data
    :return: None
    '''
    # TEST PLAN 2.10.1-3 log in with user1
    self.log('2.10.1-3 log in with user1')

    self.driver.get(self.url)
    self.login(username=user[USERNAME], password=user[PASSWORD])

    # TEST PLAN 2.10.1-4 add new client
    self.log('2.10.1-4 add new client')

    # Click on "ADD CLIENT BUTTON"
    self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()
    # wait until visible 'Member Code' textarea
    member_code_area = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
    # wait until visible 'subsystem area' textarea
    subsystem_code_area = self.wait_until_visible(type=By.ID,
                                                  element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_ID)
    self.log('Write {0} to MEMBER CODE area'.format(client['code']))

    self.input(member_code_area, client['code'])
    self.log('Write {0} to SUBSYTEM CODE area'.format(client['subsystem']))

    self.input(subsystem_code_area, client['subsystem'])
    self.log('Click on OK')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    time.sleep(5)

    warning_message = messages.get_warning_message(self)
    self.log('Warning message: {0}'.format(warning_message))
    if warning_message is not None:
        self.log('Ignore warning and click continue')
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.wait_jquery()
    self.log('Client created')

    self.log('Cancel client registration')
    time.sleep(2)
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
    self.wait_jquery()
    # Save client id as variable
    self.added_client_id = ' : '.join(
        [client['type'], ssh_server_actions.get_server_name(self), client['class'], client['code'],
         client['subsystem']])


def user_2_actions(self, user, client):
    '''
    Executes actions with user2.
    :param self: MainController object
    :param user: dict - user data
    :param client: dict - client data
    :return: None
    '''
    # TEST PLAN 2.10.1-5 log out, then log in with user2
    self.log('2.10.1-5 log out, then log in with user2')

    self.logout()
    self.login(username=user[USERNAME], password=user[PASSWORD])

    # TEST PLAN 2.10.1-6 edit client
    self.log('2.10.1-6 edit client')

    client_row = added_client_row(self=self, client=client)
    self.log('Opening Internal Servers Tab')
    client_row.find_element_by_css_selector(clients_table_vm.INTERNAL_CERTS_TAB_CSS).click()
    self.wait_jquery()
    self.log('Select HTTPS from dropdown')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_CONNECTION_TYPE_ID))
    select.select_by_visible_text('HTTPS')
    self.log('Save state with HTTPS selected')
    self.wait_until_visible(type=By.ID,
                            element=popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_CONNECTION_TYPE_SAVE_BTN_ID).click()
    self.wait_jquery()


def user_3_actions(self, user, client):
    '''
    Executes actions with user3.
    :param self: MainController object
    :param user: dict - user data
    :param client: dict - client data
    :return: None
    '''
    # TEST PLAN 2.10.1-7 log out, log in with user3
    self.log('2.10.1-7 log out, then log in with user3')

    if self.driver is None:
        return

    self.logout()
    self.login(username=user[USERNAME], password=user[PASSWORD])

    # TEST PLAN 2.10.1-8 delete client
    self.log('2.10.1-8 delete client')

    client_row = added_client_row(self=self, client=client)
    self.log('Opening client details')
    client_row.find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS).click()
    self.wait_jquery()
    self.log('Deleting client')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
    popups.confirm_dialog_click(self)
    self.log('CLIENT DELETED')


def added_client_row(self, client):
    '''
    Finds client row from table and returns it.
    :param self: MainController object
    :param client: dict - client data
    :return: WebDriverElement - client row
    '''
    self.log('Finding added client')
    self.wait_jquery()
    self.added_client_id = ' : '.join(
        [client['type'], ssh_server_actions.get_server_name(self), client['class'], client['code'],
         client['subsystem']])
    table_rows = self.by_css(clients_table_vm.CLIENT_ROW_CSS, multiple=True)
    client_row_index = clients_table_vm.find_row_by_client(table_rows, client_id=self.added_client_id)
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
    client = get_client(ssh_host, ssh_username, ssh_password)
    try:
        ssh_user_actions.add_user(client=client, username=users['user1'][USERNAME], password=users['user1'][PASSWORD],
                                  group=users['user1']['group'])
        ssh_user_actions.add_user(client=client, username=users['user2'][USERNAME], password=users['user2'][PASSWORD],
                                  group=users['user2']['group'])
        ssh_user_actions.add_user(client=client, username=users['user3'][USERNAME], password=users['user3'][PASSWORD],
                                  group=users['user3']['group'])
        ssh_user_actions.add_user(client, users['databaseuser'][USERNAME], users['databaseuser'][PASSWORD])
    finally:
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
    client = get_client(ssh_host, ssh_username, ssh_password)
    try:
        ssh_user_actions.delete_user(client, username=users['user1']['username'])
        ssh_user_actions.delete_user(client, username=users['user2']['username'])
        ssh_user_actions.delete_user(client, username=users['user3']['username'])
        ssh_user_actions.delete_user(client, username=users['databaseuser'][USERNAME])
    finally:
        client.close()


def get_client(ssh_host, ssh_username, ssh_password):
    '''
    Creates a new SSH connection.
    :param ssh_host: str - SSH server hostname
    :param ssh_username: str - SSH username
    :param ssh_password: str - SSH password
    :return: SSHClient object
    '''
    return ssh_client.SSHClient(ssh_host, username=ssh_username, password=ssh_password)


def get_formatted_data(output):
    '''
    Returns log data as list of dictionaries.
    :param output: [str] log data
    :return: [dict] - formatted data
    '''
    data = []
    for line in output:
        splitted_line = line.split(',')
        data.append({'table_name': splitted_line[0],
                     'operation': splitted_line[1],
                     'timestamp': splitted_line[2]})
    return data
