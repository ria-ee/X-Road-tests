import time
import traceback
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_server_actions, ssh_user_actions, xroad
from tests.xroad_add_to_acl_218 import add_to_acl_2_1_8
from tests.xroad_ss_client_sertification_213 import client_certification_2_1_3
from view_models import popups as popups, members_table, clients_table_vm as clients_table, sidebar, \
    keys_and_certificates_table
from view_models.log_constants import *

USERNAME = 'username'
PASSWORD = 'password'

test_name = 'LOGGING IN SECURITY SERVER'


def test_test(ssh_host, ssh_username, ssh_password,
              cs_host, cs_username, cs_password,
              sec_host, sec_username, sec_password,
              users, client_id, client_name, wsdl_url):
    def test_case(self):
        error = False
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name
        try:
            self.log('Add member to central server')
            add_member_to_cs(self, member=client)

            self.log('Add all needed users to Security Server system')
            add_users_to_system(ssh_host, ssh_username, ssh_password, users)

            self.log('Wait 120 seconds before continuing with security server')
            time.sleep(120)

            self.log('USER 1 ACTIONS')
            user = users['user1']

            self.log('Add client to security server')
            add_client_to_ss(self=self, sec_host=sec_host, sec_username=user[USERNAME],
                             sec_password=user[PASSWORD], ssh_host=ssh_host, ssh_username=ssh_username,
                             ssh_password=ssh_password, client=client)

            self.log('Add group to previously added client')
            add_group_to_client(self=self, sec_host=sec_host, sec_username=user[USERNAME], sec_password=user[PASSWORD],
                                ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password, client=client)

            self.log('USER 2 ACTIONS')
            self.logout(sec_host)
            self.login(username=user[USERNAME], password=user[PASSWORD])
            user = users['user2']
            certify_client_in_ss(self, ssh_host, ssh_username, ssh_password, sec_host, user[USERNAME], user[PASSWORD],
                                 users, client)
            self.url = cs_host

            self.logout(sec_host)
            self.login(users['user2'][USERNAME], users['user2'][PASSWORD])
            self.log('USER 3 ACTIONS')
            user = users['user3']
            add_services_to_client(self, ssh_host, ssh_username, ssh_password, sec_host, user[USERNAME], user[PASSWORD],
                                   users, client, wsdl_url)
            enable_service(self, client, wsdl_url)
        except:
            traceback.print_exc()
            error = True

        finally:
            remove_data(self=self, ssh_host=ssh_host, ssh_username=ssh_username, ssh_password=ssh_password,
                        cs_host=cs_host, cs_username=cs_username, cs_password=cs_password, sec_host=sec_host,
                        sec_username=sec_username, sec_password=sec_password, users=users, client=client)
            if error:
                assert False

    return test_case


def remove_data(self, ssh_host, ssh_username, ssh_password, cs_host, cs_username, cs_password, sec_host, sec_username,
                sec_password, users, client):
    try:
        remove_member(self, cs_host, cs_username, cs_password, member=client)
    except:
        self.log('ERROR {0}'.format(traceback.format_exc()))
        self.log('Removing member failed')

    try:
        self.reset_webdriver(sec_host, sec_username, sec_password)

        remove_certificate(self, client)
    except:
        self.log('ERROR {0}'.format(traceback.format_exc()))
        self.log('Removing certicate failed')

    try:
        self.reset_webdriver(sec_host, sec_username, sec_password)

        remove_client(self, client)
    except:
        self.log('ERROR {0}'.format(traceback.format_exc()))
        self.log('Removing client failed')

    try:
        remove_users_from_system(ssh_host, ssh_username, ssh_password, users)
    except:
        self.log('ERROR {0}'.format(traceback.format_exc()))
        self.log('Removing users failed')


def add_client_to_ss(self, sec_host, sec_username, sec_password,
                     ssh_host, ssh_username, ssh_password, client):
    self.driver.get(sec_host)
    self.login(username=sec_username, password=sec_password)
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGIN, sec_username)

    self.is_true(bool_value)

    self.log('Click on "ADD CLIENT" button')
    self.wait_until_visible(type=By.ID, element=clients_table.ADD_CLIENT_BTN_ID).click()
    self.log('Wait till ADD CLIENT dialog')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_XPATH)

    self.log('Select {0} from "CLIENT CLASS" dropdown'.format(client['class']))
    member_class = Select(self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    member_class.select_by_visible_text(client['class'])

    self.log('Insert {0} to "MEMBER CODE" area'.format(client['code']))
    member_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
    # member_code.send_keys(client['code'])
    self.input(member_code, client['code'])

    self.log('Insert {0} into "SUBSYSTEM CODE" area'.format(client['subsystem']))
    member_sub_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_ID)
    # member_sub_code.send_keys(client['subsystem'])
    self.input(member_sub_code, client['subsystem'])

    self.log('Click "OK" to add client')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_CLIENT,
                                                     sec_username)

    self.is_true(bool_value, test_name, 'CHECKING LOGS FAILED FOR ADDING CLIENT', 'CHECK LOGS FOR ADDING CLIENT ')

    time.sleep(5)
    self.log('Confirm registration')
    popups.confirm_dialog_click(self)


def add_group_to_client(self, sec_host, sec_username, sec_password, ssh_host, ssh_username, ssh_password, client):
    # self.driver.get(sec_host + 'login/logout')
    self.logout(sec_host)
    self.login(sec_username, sec_password)
    self.log('Waiting 120 seconds for changes')
    time.sleep(120)
    self.driver.refresh()
    self.wait_jquery()
    time.sleep(5)
    self.log('Select added client')
    added_client_row(self, client).find_element_by_css_selector(clients_table.LOCAL_GROUPS_TAB_CSS).click()
    self.log('click OK')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_GROUP_ADD_BTN_ID).click()
    self.log('Confirm popup')
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    time.sleep(5)

    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_GROUP_FAILED,
                                                     sec_username)

    self.is_true(bool_value, test_name, 'CHECKING LOGS FAILED FOR ADDING GROUP',
                 'CHECK LOGS FOR ADDING GROUP TO CLIENT'
                 )


def certify_client_in_ss(self, ssh_host, ssh_username, ssh_password, sec_host, sec_username, sec_password, users,
                         client):
    self.logout(sec_host)
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGOUT,
                                                     users['user1'][USERNAME])
    self.is_true(bool_value, test_name, 'CHECKING LOGS FAILED FOR LOG OUT', 'CHECK LOGS FOR LOG OUT CLIENT ')

    self.driver.get(sec_host)
    self.login(username=sec_username, password=sec_password)
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGIN, sec_username)
    self.is_true(bool_value, test_name, 'CHECKING LOGS FAILED FOR LOG IN', 'CHECK LOGS FOR LOG IN CLIENT ')

    self.log('Create sign certificate')
    self.driver.get(sec_host)
    self.wait_jquery()
    self.url = sec_host
    client_certification_2_1_3.test(client_code=client['code'], client_class=client['class'])(self)


def get_current_time(ssh_host, ssh_password, ssh_username):
    return ssh_server_actions.get_server_time(ssh_host, ssh_username, ssh_password).replace(microsecond=0)


def add_member_to_cs(self, member):
    self.log('Wait for the "ADD" button and click')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()
    self.log('Wait for the popup to be visible')
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


def add_services_to_client(self, ssh_host, ssh_username, ssh_password, sec_host, sec_username, sec_password, users,
                           client, wsdl_url):
    self.logout(sec_host)
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGOUT,
                                                     users['user2'][USERNAME])
    self.is_true(bool_value, test_name, 'CHECKING LOGS FAILED FOR LOG OUT', 'CHECK LOGS FOR LOG OUT CLIENT')

    self.logout(sec_host)
    self.login(username=sec_username, password=sec_password)
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, LOGIN, sec_username)
    self.is_true(bool_value, test_name, 'CHECKING LOGS FAILED FOR LOG IN', 'CHECK LOGS FOR LOG IN CLIENT')

    self.log('ADDING NOT A WSDL URL')
    self.wait_jquery()
    added_client_row(self=self, client=client).find_element_by_css_selector(clients_table.SERVICES_TAB_CSS).click()
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ADD_WSDL_BTN_ID).click()
    wsdl_area = self.wait_until_visible(type=By.ID, element=popups.ADD_WSDL_POPUP_URL_ID)
    # wsdl_area.send_keys('http://neti.ee')
    self.input(wsdl_area, 'http://neti.ee')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_WSDL_FAILED,
                                                     sec_username)
    self.is_true(bool_value, test_name, 'CHECKING LOGS FAILED FOR ADDING FALSE WSDL URL',
                 'CHECK LOGS FOR ADDING FALSE WSDL URL')

    self.log('ADDING CORRECT WSDL URL')
    wsdl_area.clear()
    self.input(wsdl_area, wsdl_url)
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_OK_BTN_XPATH).click()
    self.log('Waiting 60 seconds for changes')
    time.sleep(60)
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, ADD_WSDL, sec_username)
    self.is_true(bool_value, test_name, 'CHECKING LOGS FAILED FOR ADDING CORRECT WSDL URL',
                 'CHECK LOGS FOR ADDING CORRECT WSDL URL')

    services_list = clients_table.client_services_popup_get_services_rows(self=self, wsdl_url=wsdl_url)
    services_list[0].click()
    self.log('Open edit wsdl service popup')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()
    self.log('EDIT SERVICE PARAMETERS')
    timeout_area = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_TIMEOUT_ID)
    # timeout_area.clear()
    # timeout_area.send_keys('55')
    self.input(timeout_area, '55')
    self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
    bool_value, log_data, date_time = check_logs_for(self, ssh_host, ssh_username, ssh_password, EDIT_SERVICE_PARAMS,
                                                     sec_username)
    self.is_true(bool_value, test_name,
                 'CHECKING LOGS FAILED FOR EDITING WSDL SERVICE PARAMETER',
                 'CHECK LOGS FOR EDITING WSDL SERVICE PARAMETER')

    self.log('EDIT ACCESS RIGHT FOR SERVICE')
    # added_client_id = ' : '.join([client['type'], ssh_server_actions.get_server_name(self), client['class'],
    #                               client['code'], client['subsystem']])
    subject = ' : '.join([client['type'], ssh_server_actions.get_server_name(self), 'COM',
                          'CLIENT3', client['subsystem']])
    self.driver.get(sec_host)

    client_to_add = {'instance': ssh_server_actions.get_server_name(self), 'class': client['class'],
                     'code': client['code'], 'subsystem': client['subsystem']}

    add_to_acl_2_1_8.test_add_subjects(client=client_to_add, wsdl_index=0, service_index=0,
                                       service_subjects=[subject], remove_data=False,
                                       allow_remove_all=True, case=self)


def enable_service(self, client, wsdl_url):
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.CLIENTS_BTN_CSS)
    added_client_row(self, client).find_element_by_css_selector(clients_table.SERVICES_TAB_CSS).click()
    services_list = clients_table. \
        client_services_popup_get_services_rows(self=self, wsdl_url=wsdl_url)
    services_list[0].click()
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()


def added_client_row(self, client):
    self.log('Finding added client')

    self.added_client_id = ' : '.join([client['type'], ssh_server_actions.get_server_name(self), client['class'],
                                       client['code'], client['subsystem']])
    table_rows = self.by_css(clients_table.CLIENT_ROW_CSS, multiple=True)
    client_row_index = clients_table.find_row_by_client(table_rows, client_id=self.added_client_id)
    return table_rows[client_row_index]


def add_users_to_system(ssh_host, ssh_username, ssh_password, users):
    client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
    try:
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
        client.close()


def remove_users_from_system(ssh_host, ssh_username, ssh_password, users):
    client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
    try:
        ssh_user_actions.delete_user(client, username=users['user1'][USERNAME])
        ssh_user_actions.delete_user(client, username=users['user2'][USERNAME])
        ssh_user_actions.delete_user(client, username=users['user3'][USERNAME])
    finally:
        client.close()


def remove_member(self, cent_host, cent_username, cent_password, member):
    self.reset_webdriver(cent_host, cent_username, cent_password)

    self.log('Wait for members table')
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.log('Get row by row values')
    row = members_table.get_row_by_columns(table, [member['name'], member['class'], member['code']])
    if row is None:
        self.log('Did not find member row')
        raise
    row.click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.log('Confirm deleting member')
    popups.confirm_dialog_click(self)


def remove_client(self, client):
    self.wait_jquery()
    self.log('Opening client details')
    added_client_row(self, client).find_element_by_css_selector(clients_table.DETAILS_TAB_CSS).click()
    self.wait_jquery()
    time.sleep(1)
    self.log('Unregister Client')
    is_delete_needed = False
    try:
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
        popups.confirm_dialog_click(self)
    except:
        is_delete_needed = True
        self.log('Not unregistering')
        self.wait_jquery()
        traceback.print_exc()

    try:
        self.log('Deleting client')
        if is_delete_needed:
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
        self.wait_jquery()
        popups.confirm_dialog_click(self)
    except:
        traceback.print_exc()
    self.log('CLIENT DELETED')


def remove_certificate(self, client):
    self.log('REMOVE CERTIFICATE')
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
    time.sleep(10)
    s_client = ssh_server_actions.get_client(ssh_host, ssh_username, ssh_password)
    log = ssh_server_actions.get_log_lines(s_client, self.xroad_audit_log, 1)
    s_client.close()
    self.log(log)
    date_time = datetime.strptime(' '.join([log['date'], log['time']]), "%Y-%m-%d %H:%M:%S")
    datetime.strptime(datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S.000000"), '%Y-%m-%d %H:%M:%S.%f')
    return (log['msg_service'] == 'X-Road Proxy UI') & (log['data']['event'] == event) & \
           (log['data']['user'] == user), log['data'], date_time
