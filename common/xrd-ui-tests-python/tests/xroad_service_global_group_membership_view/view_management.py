# coding=utf-8
from selenium.webdriver.common.by import By
from view_models import popups, cs_security_servers, members_table
from time import gmtime, strftime, mktime
import datetime
from selenium.webdriver.support.select import Select
from helpers import ssh_server_actions


def test_verify_local_group_client(case, ss_client_name=None, test_group_name=None, subsystem=None):
    '''

    :param case: MainController object
    :param ss_client_name: string client name information
    :param test_group_name: string client group_name information
    :param subsystem: string client subsystem information
    :return:
    '''

    self = case

    def global_group_client():
        global_group_conf(self, ss_client_name=ss_client_name, test_group_name=test_group_name,
                     subsystem=subsystem)

    return global_group_client


def global_group_conf(self, ss_client_name=None, test_group_name=None, subsystem=None):
    '''
    :param self: MainController object
    :param ss_client_name: string client name information
    :param test_group_name: string client group_name information
    :param subsystem: string client subsystem information
    :return:
    '''

    '''Find a member and click on it'''
    self.wait_until_visible(type=By.XPATH,
                            element=cs_security_servers.MEMBER_TABLE_CLICK_MEMBER.format(ss_client_name)).click()

    '''Clic on "DETAILS" button'''
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()

    self.log('SERVICE_36: 1.CS administrator selects to view the list of global groups an X-Road member belongs to '
             '(as a member or as a subsystem).')
    self.wait_until_visible(type=By.XPATH, element=members_table.GLOBAL_GROUP_TAB).click()

    '''Get date and time before clicking on "ADD" button'''
    ssh_host = self.config.get('cs.ssh_host')
    ssh_user = self.config.get('cs.ssh_user')
    ssh_pass = self.config.get('cs.ssh_pass')

    ssh_client = ssh_server_actions.get_client(ssh_host, ssh_user, ssh_pass)
    before_date_and_time = ssh_client.exec_command('date +"%Y-%m-%d %H:%M:%S"', sudo=True)
    before_date_and_time = before_date_and_time[0][0].encode('utf-8').split()
    before_time = before_date_and_time[1]
    ssh_client.close()

    before_time_timestamp = mktime(datetime.datetime.strptime(before_time, "%H:%M:%S").timetuple())

    '''Add member to global group'''
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_TO_GLOBAL_GROUP_BTN_ID).click()
    self.wait_jquery()

    '''Set settings and values'''
    select = Select(
        self.wait_until_visible(type=By.ID, element=members_table.MEMBER_DETAILS_GLOBAL_GROUP_MEMBERS_ADD_BTN))
    select.select_by_visible_text(subsystem)

    '''Set settings and values'''
    select = Select(self.wait_until_visible(type=By.ID, element=members_table.GROUP_SELECT_ID))
    select.select_by_visible_text(test_group_name)
    self.wait_until_visible(type=By.XPATH, element=members_table.GROUP_POPUP_OK_BTN_XPATH).click()

    '''Get date and time after clicking on "ADD" button'''
    ssh_client = ssh_server_actions.get_client(ssh_host, ssh_user, ssh_pass)
    date_and_time = ssh_client.exec_command('date +"%Y-%m-%d %H:%M:%S"', sudo=True)
    date_and_time = date_and_time[0][0].encode('utf-8').split()
    creation_date = date_and_time[0]
    creation_time = date_and_time[1]
    ssh_client.close()

    created_time_timestamp = mktime(datetime.datetime.strptime(creation_time, "%H:%M:%S").timetuple())

    self.wait_jquery()

    self.log('Click "Global group membership" tab')
    self.wait_until_visible(type=By.XPATH, element=members_table.GLOBAL_GROUP_TAB).click()

    self.log('SERVICE_36: 2. Details button verification')
    group_details_btn = self.wait_until_visible(type=By.CSS_SELECTOR, element='.open_details').is_enabled()
    self.is_true(group_details_btn,
                 msg='Details button not found')

    '''Get table text'''
    table = self.wait_until_visible(type=By.XPATH, element=members_table.GLOBAL_GROUP_MEMBERSHIP_TABLE_XPATH).text
    new_table_row = []
    table_row = table.split('\n')
    for row in table_row:
        row = row.encode('utf-8')
        row = row.split()
        new_table_row.append(row)
    group = new_table_row[1][0]
    subsystems = new_table_row[1][1]
    date = new_table_row[1][2]
    time = new_table_row[1][3]

    time_timestamp = mktime(datetime.datetime.strptime(time, "%H:%M:%S").timetuple())

    self.log('SERVICE_36: 2. The global group code')
    self.is_equal(test_group_name, group,
                  msg='The global group code is wrong')
    self.log('SERVICE_36: 2. The code of the members subsystem, if the member has joined the group as a subsystem.')
    self.is_equal(subsystem, subsystems,
                  msg='Subsystem is wrong')

    self.log('SERVICE_36: 2. The date and time of when the member was added to the group')
    assert before_time_timestamp < time_timestamp and time_timestamp <= created_time_timestamp

    self.log('SERVICE_36: 2. The date and time of when the member was added to the group')
    self.is_equal(creation_date, date,
                  msg='Creation time is wrong')

    '''Click on row'''
    self.wait_until_visible(type=By.XPATH, element=members_table.GLOBAL_GROUP_MEMBERSHIP_TABLE_XPATH).click()
    self.wait_jquery()

    self.log('SERVICE_36: 2. "Delete" button verification')
    delete_btn = self.wait_until_visible(type=By.XPATH,
                                         element=members_table.DELETE_MEMBER_FROM_GLOBAL_GROUP_BTN_ID).is_enabled()
    self.is_true(delete_btn,
                 msg='"Delete" button not found')
    self.log('SERVICE_36: 2. "Add" button verification')
    add_btn = self.wait_until_visible(type=By.XPATH,
                                      element=members_table.ADD_MEMBER_TO_GLOBAL_GROUP_BTN_ID).is_enabled()
    self.is_true(add_btn,
                 msg='"Add" button not found')

    '''Delete global group member'''
    self.wait_until_visible(type=By.XPATH, element=members_table.DELETE_MEMBER_FROM_GLOBAL_GROUP_BTN_ID).click()

    '''Confirm'''
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()
