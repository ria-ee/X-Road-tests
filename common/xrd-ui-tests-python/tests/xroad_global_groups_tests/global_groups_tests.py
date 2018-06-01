import re
import time
from datetime import datetime

from selenium.webdriver.common.by import By

import tests.xroad_parse_users_inputs.xroad_parse_user_inputs as user_input_check
from helpers import auditchecker
from helpers import ssh_server_actions, xroad
from tests.xroad_add_to_acl_218 import add_to_acl
from tests.xroad_add_to_acl_218.add_to_acl import restore_original_subject_list
from view_models import members_table, sidebar, groups_table, popups, messages, log_constants, \
    sidebar as sidebar_constants, clients_table_vm
from view_models.cs_security_servers import MEMBER_TABLE_CLICK_MEMBER
from view_models.groups_table import MEMBER_COUNT_REGEX, GLOBAL_GROUP_TR, GROUP_DETAILS_BTN_ID, \
    GROUP_DESCRIPTION_INPUT_ID, GROUP_DETAILS_MEMBER_COUNT_ID, GROUP_MEMBERS_TR, MEMBER_ROW_DATE_REGEX, \
    GROUP_DETAILS_REMOVE_ALL, GROUP_DETAILS_REMOVE_SELECTED_MEMBERS, GROUP_EDIT_DESCRIPTION_BTN_ID, \
    GROUP_EDIT_DESCRIPTION_TEXTAREA_ID, GLOBAL_GROUP_BY_GROUP_CODE_XPATH, GLOBAL_GROUP_COLS_BY_CSS, GROUP_ROW_BY_TEXT
from view_models.log_constants import *
from view_models.members_table import GLOBAL_GROUP_TAB, MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH, \
    ADD_MEMBER_TO_GLOBAL_GROUP_BTN_ID, GROUP_POPUP_OK_BTN_XPATH, GROUP_SELECT_ID, DELETE_MEMBER_FROM_GLOBAL_GROUP_BTN_ID
from view_models.messages import NOTICE_MESSAGE_CSS, DESCRIPTION_CHANGED_SUCCESSFULLY, ERROR_MESSAGE_CSS, \
    INPUT_EXCEEDS_255_CHARS, MISSING_PARAMETER, ADD_MEMBER_TO_GLOBAL_GROUP, MEMBER_DELETED_FROM_GLOBAL_GROUP, \
    MEMBER_ADDED_TO_GLOBAL_GROUP
from view_models.popups import confirm_dialog_click, GROUP_EDIT_POPUP_OK_BTN_XPATH
from view_models.sidebar import GLOBAL_GROUPS_CSS
from view_models.timestamp_services import DATE_REGEX


def add_member_to_group(self, client, group, ss2_host, ss2_user, ss2_pass,
                        wsdl_url, service_name, identifier, testclient=None, log_checker=None):
    """
    SERVICE_33 Add Members to a Global Group
    :param wsdl_url: str - wsdl url
    :param service_name: str - service name
    :param identifier: str - central server identifier
    :param testclient: obj - soapclient instance
    :param ss2_pass: str - security server password
    :param ss2_user: str - security server username
    :param ss2_host: str - security server host
    :param client: dict - client information
    :param self: mainController instance
    :param client_name: str - client name
    :param client_subsystem: str - client subsystem
    :param group: str - group name
    :return:
    """
    current_log_lines = None
    if log_checker is not None:
        current_log_lines = log_checker.get_line_count()
    subject_list = ['GLOBALGROUP : {0} : {1}'.format(identifier, group)]
    client_name = client['name']
    client_subsystem = client['subsystem']
    '''Open group details'''
    self.wait_until_visible(type=By.XPATH,
                            element=groups_table.GLOBAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(group)).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.log('SERVICE_33 1. Add members to global group button is pressed')
    self.wait_until_visible(type=By.ID, element=groups_table.GLOBAL_GROUP_ADD_MEMBERS_BTN_ID).click()
    self.wait_jquery()
    self.log('SERVICE_33 2. Addable subject is selected from subjects list')
    srch_input = self.wait_until_visible(type=By.XPATH,
                                         element=groups_table.GROUP_MEMBERS_ADD_SEARCH_INPUT_XPATH)
    self.input(element=srch_input, text=client_subsystem)
    self.wait_until_visible(type=By.XPATH, element=groups_table.GROUP_MEMBERS_ADD_SEARCH_BUTTON_XPATH).click()

    self.wait_jquery()
    self.wait_until_visible(
        type=By.XPATH, element=groups_table.MEMBER_ROW_BY_TWO_COLUMNS_XPATH.format(client_name,
                                                                                   client_subsystem)).click()
    self.log('SERVICE_33 2. Add button is clicked')
    self.wait_until_visible(type=By.ID, element=groups_table.GROUP_MEMBERS_ADD_BUTTON_ID).click()
    if current_log_lines is not None:
        expected_log_msg = ADD_MEMBERS_TO_GLOBAL_GROUP
        self.log('SERVICE_33 4. System logs the event "{0}"'.format(expected_log_msg))
        time.sleep(1)
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)
    if testclient is not None:
        test_configure_service_acl = add_to_acl.test_add_subjects(case=self, client=client,
                                                                  client_name=client_name,
                                                                  wsdl_url=wsdl_url,
                                                                  service_name=service_name,
                                                                  service_subjects=subject_list,
                                                                  remove_data=False,
                                                                  allow_remove_all=False,
                                                                  remove_current=True)
        self.log('Wait until servers synced')
        time.sleep(120)
        self.log('Add global group to {0} service ACL'.format(service_name))
        self.reload_webdriver(ss2_host, ss2_user, ss2_pass)
        current_subjects = test_configure_service_acl()

        self.log('SERVICE_33 3. System adds group members to the global group. '
                 'Added group members will inherit all access rights granted for the group')
        self.log('Testing by querying service, in which ACL only global group exists')
        self.is_true(testclient.check_success(), msg='Query as global group member failed')

        self.log('Restore service ACL')
        clients_table_vm.open_client_popup_services(self, client_name=client_name,
                                                    client_id=xroad.get_xroad_id(client))

        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        self.wait_until_visible(services_table)

        '''Find the WSDL, expand it and select service'''
        clients_table_vm.client_services_popup_open_wsdl_acl(self, services_table=services_table,
                                                             service_name=service_name,
                                                             wsdl_url=wsdl_url)

        self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_ADD_SUBJECTS_BTN_CSS, type=By.ID,
                                timeout=20)
        self.log('Restore {0} acl'.format(service_name))
        restore_original_subject_list(self, current_subjects, subject_list, allow_remove_all=False,
                                      remove_duplicates=True)


def add_group(self, group, check_global_groups_inputs=False, cs_ssh_host=None, cs_ssh_user=None,
              cs_ssh_pass=None):
    """
    SERVICE_32 Adds a new global group to the system. First tries to add with empty values, then with the correct ones.
    Checks if the action was logged.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param user: dict - user data
    :param group: str - group name
    :param check_global_groups_inputs bool - condition to check user inputs or not
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :return: None
    """

    def enter_global_group_data():
        """
        :return: None
        """
        # Start adding new group
        self.log('Click "ADD" to add new group')
        self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).click()

        # Fill in required fields and try again
        self.log('Add new group, fill in required fields')
        self.log('Send {0} to code area input'.format(group))
        group_code_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_CODE_AREA_ID)
        self.input(group_code_input, group)
        self.log('Send {0} to code description input'.format(group))
        group_description_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DESCRIPTION_AREA_ID)
        self.input(group_description_input, group)

    if check_global_groups_inputs:
        '''SERVICE_32 step 3 System verifies global groups inputs in the central server'''

        # SERVICE_32 3. System verifies global groups inputs in the central server
        self.log('*** SERVICE_32_3 / XTKB-56')
        # Open global groups
        self.log('Open Global Groups tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()
        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)

        # Loop through data from the groups_table.py
        counter = 1
        for group_data in groups_table.GROUP_DATA:
            if cs_ssh_host is not None:
                current_log_lines = log_checker.get_line_count()
            # Set necessary parameters
            code = group_data[0]
            description = group_data[1]
            error = group_data[2]
            error_message = group_data[3]
            error_message_label = group_data[4]
            whitespaces = group_data[5]

            # Start adding new group
            enter_global_group(self, code, description, cs_ssh_host=cs_ssh_host, cs_ssh_user=cs_ssh_user,
                               cs_ssh_pass=cs_ssh_pass)

            # Verify group code and description
            user_input_check.error_messages(self, error, error_message, error_message_label)

            if error:
                # Close a pop-up window , if there is a error message
                if cs_ssh_host is not None:
                    logs_found = log_checker.check_log(log_constants.ADD_GLOBAL_GROUP_FAILED,
                                                       from_line=current_log_lines + 1)
                    self.is_true(logs_found)
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH,
                                        element=groups_table.NEW_GROUP_POPUP_CANCEL_BTN_XPATH).click()
                self.wait_jquery()
            else:
                # Verify that the added global group code exists
                self.log('Find added code text - ' + code.strip())
                global_croup_code = self.wait_until_visible(type=By.XPATH,
                                                            element=groups_table.
                                                            get_clobal_group_code_description_by_text(code.strip()))
                global_croup_code = global_croup_code.text
                # Verify that the added global group description exists
                self.log('Find added description text - ' + description.strip())
                global_croup_description = self.wait_until_visible(type=By.XPATH,
                                                                   element=groups_table.
                                                                   get_clobal_group_code_description_by_text(
                                                                       description.strip()))
                global_croup_description = global_croup_description.text
                self.log('Found global group code - ' + code)
                self.log('Found global group description - ' + description)

                if whitespaces:
                    user_input_check.find_text_with_whitespaces(self, code, global_croup_code)
                    user_input_check.find_text_with_whitespaces(self, description, global_croup_description)
                else:
                    assert code in global_croup_code
                    assert description in global_croup_description

                # Delete added global group
                remove_group(self, code, cs_ssh_host=cs_ssh_host, cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass)

            counter += 1
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()

        '''SERVICE_32 step 4a insert a group code that already exists'''
        '''Start adding new group'''
        enter_global_group_data()
        self.log('Click on "OK" to add new group')
        self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        '''Start adding new group with same code, that already exists'''
        enter_global_group_data()
        self.log('Click on "CANCEL" to terminate the use case')
        self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_jquery()

        '''Start adding new group with same code, that already exists, one more time'''
        enter_global_group_data()

        '''We're looking for "Add global group failed" log'''
        self.logdata = [log_constants.ADD_GLOBAL_GROUP_FAILED]

        self.log('Click on "OK" to add new group')
        self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        '''Check error message'''
        user_input_check.error_messages(self, True, messages.GLOBAL_GROUP_ALREADY_TAKEN, group)
        self.log('Click on "CANCEL" to terminate the use case')
        self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_jquery()

        '''We're looking for "Add global group failed" log'''
        if cs_ssh_host is not None:
            '''Check logs for entries'''
            self.log('SERVICE_32 6 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.
                         format(self.logdata, log_checker.found_lines))

        '''Delete added global group'''
        remove_group(self, group, cs_ssh_host=cs_ssh_host, cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass)

    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    '''We're looking for "Add global group" log'''
    self.logdata = [log_constants.ADD_GLOBAL_GROUP]

    if cs_ssh_host is not None:
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
        current_log_lines = log_checker.get_line_count()

    enter_global_group_data()

    self.log('Click on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    if cs_ssh_host is not None:
        '''Check logs for entries'''
        self.log('SERVICE_32 6 - checking logs for: {0}'.format(self.logdata))
        logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
        self.is_true(logs_found,
                     msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                               log_checker.found_lines))


def remove_group(self, group, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None):
    """
    SERVICE_39 Removes a global group from the system.
    :param cs_ssh_pass: central server ssh password
    :param cs_ssh_user: central server ssh user
    :param cs_ssh_host: central server ssh host
    :param self: MainController object
    :param group: str - group name
    :return: None
    """
    '''Auditchecker instance'''
    current_log_lines = None
    if cs_ssh_host is not None:
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        current_log_lines = log_checker.get_line_count()
    '''Open global groups'''
    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    '''Find and select the group'''
    self.log('Select added group')
    self.wait_until_visible(type=By.XPATH,
                            element=groups_table.GLOBAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(group.strip())).click()
    '''Open group details and delete the group'''
    self.log('Open group details')
    self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.log('SERVICE_39 1. Click on "DELETE GROUP" button')
    self.wait_until_visible(type=By.XPATH, element=groups_table.DELETE_GROUP_BTN_ID).click()
    self.wait_jquery()
    self.log('SERVICE_39 3a. Group deletion is canceled')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
    self.log('SERVICE_39 1. Click on "DELETE GROUP" button')
    self.wait_until_visible(type=By.XPATH, element=groups_table.DELETE_GROUP_BTN_ID).click()
    self.wait_jquery()
    self.log('SERVICE_39 3. Confirm group deletion')
    popups.confirm_dialog_click(self)
    expected_log_msg = log_constants.DELETE_GLOBAL_GROUP
    self.log('SERVICE_39 4. System logs the event "{0}"'.format(expected_log_msg))
    if current_log_lines is not None:
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg='{} not found in logs'.format(expected_log_msg))


def check_logs_for(ssh_client, event, user):
    """
    Checks if an event for user was logged in the system.
    :param ssh_client: SSHClient object
    :param event: str - event to look for in the logs
    :param user: str - username to look for in the logs
    :return: bool - True if event was logged; False otherwise
    """
    print 'Checking logs for {0}'.format(event)
    # Wait 15 seconds for sync
    time.sleep(15)
    log = ssh_server_actions.get_log_lines(ssh_client, LOG_FILE_LOCATION, 1)
    date_time = datetime.strptime(' '.join([log['date'], log['time']]), "%Y-%m-%d %H:%M:%S")
    datetime.strptime(datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S.000000"), '%Y-%m-%d %H:%M:%S.%f')
    return (str(log['msg_service']) == MSG_SERVICE_CENTER) & (str(log['data']['event']) == event) & \
           (str(log['data']['user']) == user), log['data'], date_time


def open_member_details(self, member):
    """
    Opens member details in the user interface.
    :param self: MainController object
    :param member: dict - member data
    :return: None
    """
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()
    row = members_table.get_row_by_columns(table, [member['name'], member['class'], member['code']])
    if row is None:
        self.log('Member not found')
        pass
    '''Click the row. Raises an exception if member was not found. This can be caught outside of this function if 
    necessary.'''
    self.click(row)
    self.wait_jquery()
    self.log('Open Member Details')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()


def enter_global_group(self, code, description, cs_ssh_host=None, cs_ssh_user=None,
                       cs_ssh_pass=None):
    """
    :param self: MainController object
    :param code: str - Group code
    :param description: str - Group description
    :param cs_ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param cs_ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :return:
    """
    self.wait_jquery()
    # Start adding new group
    self.log('Click "ADD" to add new group')
    self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).click()

    # Add new group
    self.log('Add new group, fill in required fields')
    self.log('Send {0} to code area input'.format(code))
    group_code_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_CODE_AREA_ID)
    self.input(group_code_input, code)
    self.log('Send {0} to code description input'.format(description))
    group_description_input = self.wait_until_visible(type=By.ID, element=groups_table.
                                                      GROUP_DESCRIPTION_AREA_ID)
    self.input(group_description_input, description)

    '''We're looking for "Add global group failed" log'''
    self.logdata = [log_constants.ADD_GLOBAL_GROUP_FAILED]
    if cs_ssh_host is not None:
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user,
                                                password=cs_ssh_pass)
        current_log_lines = log_checker.get_line_count()

    self.log('Click on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    try:
        '''We're looking for "Add global group failed" log'''
        if cs_ssh_host is not None:
            '''Check logs for entries'''
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.
                         format(self.logdata, log_checker.found_lines))
            self.log('SERVICE_32 6 - checking logs for: {0}'.format(self.logdata))
    except:
        pass


def test_view_global_groups(self):
    def view_global_groups():
        self.log('SERVICE_30 1. Opening global groups view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()
        self.log('SERVICE_30 2. System displays the list of global groups')
        global_group_rows = self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_GROUP_TR, multiple=True)
        for global_group_row in global_group_rows:
            self.log('Get global group row columns')
            tds = global_group_row.find_elements_by_tag_name('td')
            self.log('SERVICE_30 2. The code of the global group is displayed')
            self.is_true(len(tds[0].text) > 1)
            self.log('SERVICE_30 2. The description of the global group is displayed')
            self.is_true(len(tds[1].text) > 1)
            self.log('SERVICE_30 2. The number of members in the global group is displayed')
            self.is_true(re.match(MEMBER_COUNT_REGEX, tds[2].text))
            self.log('SERVICE_30 2. The date and time of when the global group was updated is displayed')
            self.is_true(re.match(DATE_REGEX, tds[3].text))

    return view_global_groups


def test_view_global_group_details(self):
    def view_global_group_details():
        self.log('Opening global groups view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()
        self.log('Click on global group row')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_GROUP_TR).click()
        self.log('SERVICE_31 1. Opening group details')
        self.wait_until_visible(type=By.ID, element=GROUP_DETAILS_BTN_ID).click()
        self.log('SERVICE_31 2. System displays the details of the global group')
        self.log('SERVICE_31 2. The description of the global group is visible')
        self.is_true(len(self.wait_until_visible(type=By.ID, element=GROUP_DESCRIPTION_INPUT_ID).text) > 0)
        self.log('SERVICE_31 2. The number of group members is visible')
        group_member_count_with_parenthesis = self.by_id(GROUP_DETAILS_MEMBER_COUNT_ID).text
        group_member_count = int(re.search(MEMBER_COUNT_REGEX, group_member_count_with_parenthesis).group(0))
        self.is_not_none(group_member_count)
        self.log('SERVICE_31 2. The list of the members of the group is visible')
        group_members = self.wait_until_visible(type=By.CSS_SELECTOR, element=GROUP_MEMBERS_TR, multiple=True)
        self.log('Checking if member row count is same as group member count')
        self.is_equal(group_member_count, len(group_members))
        for i in range(0, group_member_count):
            self.log('Get member row columns')
            member_row_cols = group_members[i].find_elements_by_tag_name('td')
            self.log('SERVICE_31 2. The group member name is visible')
            self.is_true(len(member_row_cols[0].text) > 0)
            self.log('SERVICE_31 2. The X-Road identifier of the group member is visible')
            for j in range(1, len(member_row_cols) - 1):
                self.is_true(len(member_row_cols[j].text) > 0)
            self.log('SERVICE_31 2. The date and time of when the member was added to the global group is visible')
            self.is_true(re.match(MEMBER_ROW_DATE_REGEX, member_row_cols[-1].text))

    return view_global_group_details


def test_remove_from_global_group(self, group, log_checker, delete_member=None,
                                  testclient=None):
    def remove_from_global_group():
        self.log('Testing by querying service, in which ACL only global group exists')
        self.is_true(testclient.check_success(), msg='Query as global group member failed')

        current_log_lines = log_checker.get_line_count()
        self.log('Opening global groups view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()
        self.log('Opening group details')
        self.wait_until_visible(type=By.XPATH,
                                element=groups_table.GLOBAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(group)).click()
        self.wait_until_visible(type=By.ID, element=GROUP_DETAILS_BTN_ID).click()
        if delete_member:
            self.log('SERVICE_34 2. Selecting subjects to be removed from the group')
            self.wait_until_visible(
                type=By.XPATH, element=groups_table.MEMBER_ROW_BY_TWO_COLUMNS_XPATH.format(delete_member['name'],
                                                                                           delete_member[
                                                                                               'subsystem'])).click()
            self.log('SERVICE_34 2. Clicking "Remove selected" button')
            self.wait_until_visible(type=By.ID, element=GROUP_DETAILS_REMOVE_SELECTED_MEMBERS).click()
        else:
            self.log('SERVICE_34 2. Clicking "Remove all" button')
            self.wait_until_visible(type=By.ID, element=GROUP_DETAILS_REMOVE_ALL).click()

        self.wait_jquery()
        confirm_dialog_click(self)
        expected_log_msg = REMOVE_MEMBERS_FROM_GLOBAL_GROUP
        self.log('SERVICE_34 4. System logs the event "{}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)
        self.log('Waiting servers sync')
        time.sleep(120)
        self.log('SERVICE_34 3. System removes the selected members from the global group.\n'
                 'The access rights granted for the group will not be available for the removed members.')
        self.log('Testing query to service where the only access right is global group')
        self.is_true(testclient.check_fail())

    return remove_from_global_group


def restore_acl(self, client_name, client, service_name, wsdl_url, subject_list):
    def restore(current_subjects):
        clients_table_vm.open_client_popup_services(self, client_name=client_name,
                                                    client_id=xroad.get_xroad_id(client))

        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        self.wait_until_visible(services_table)

        '''Find the WSDL, expand it and select service'''
        clients_table_vm.client_services_popup_open_wsdl_acl(self, services_table=services_table,
                                                             service_name=service_name,
                                                             wsdl_url=wsdl_url)

        self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_ADD_SUBJECTS_BTN_CSS, type=By.ID,
                                timeout=20)
        self.log('Restore {0} acl'.format(service_name))
        restore_original_subject_list(self, current_subjects, subject_list, allow_remove_all=False,
                                      remove_duplicates=True)

    return restore


def test_edit_global_group_description(self, group_code, log_checker=None):
    def edit_global_group_desc(new_group_description, check_inputs=False):
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.log('Open global groups view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()
        self.log('Click on global group with code "{}"'.format(group_code))
        self.wait_until_visible(type=By.XPATH,
                                element=groups_table.GLOBAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(group_code)).click()
        self.log('Open group details')
        self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DETAILS_BTN_ID).click()
        self.wait_jquery()
        self.log('SERVICE_35 1. Clicking on description "edit" button')
        self.wait_until_visible(type=By.ID, element=GROUP_EDIT_DESCRIPTION_BTN_ID).click()
        description_value = self.wait_until_visible(type=By.ID, element=GROUP_EDIT_DESCRIPTION_TEXTAREA_ID)
        if check_inputs:
            self.log('SERVICE_35 2. Inserting empty string to description')
            self.input(description_value, '')
            self.by_xpath(GROUP_EDIT_POPUP_OK_BTN_XPATH).click()
            self.wait_jquery()
            expected_error_msg = MISSING_PARAMETER.format('description')
            self.log('SERVICE_35 3a.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            expected_log_msg = EDIT_GLOBAL_GROUP_DESCRIPTION_FAILED
            self.log('SERVICE_35 3a.2 System logs the event "{}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            current_log_lines = log_checker.get_line_count()

            test_256_len = 'A' * 256
            self.log('SERVICE_35 2. Inserting 256 length string to description')
            self.input(description_value, test_256_len)
            self.by_xpath(GROUP_EDIT_POPUP_OK_BTN_XPATH).click()
            self.wait_jquery()
            expected_error_msg = INPUT_EXCEEDS_255_CHARS.format('description')
            self.log('SERVICE_35 3a.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            self.log('SERVICE_35 3a.2 System logs the event "{}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            self.log('SERVICE_35 2. Inserting {} length string(starting and ending with whitespaces) '
                     'to description'.format(len(new_group_description)))
        else:
            self.log('SERVICE_35 2. Inserting {} string to description'.format(new_group_description))
        self.input(description_value, new_group_description)
        self.log('Click on "OK"')
        self.by_xpath(GROUP_EDIT_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
        self.log('SERVICE_35 4. System saves the global group description to the system configuration')
        group_description = self.wait_until_visible(type=By.ID, element=GROUP_DESCRIPTION_INPUT_ID).text
        self.log(
            'Checking if group description is max length(255 chars) string without starting and ending whitespaces')
        self.is_equal(new_group_description.strip(), group_description)
        expected_notice_msg = DESCRIPTION_CHANGED_SUCCESSFULLY
        self.log('Checking if notice message is equal to {}'.format(expected_notice_msg))
        notice_message = self.wait_until_visible(type=By.CSS_SELECTOR, element=NOTICE_MESSAGE_CSS).text
        self.is_equal(DESCRIPTION_CHANGED_SUCCESSFULLY, notice_message)
        if current_log_lines is not None:
            expected_log_msg = EDIT_GLOBAL_GROUP_DESCRIPTION
            self.log('SERVICE_35 5. System logs the event {}'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

    return edit_global_group_desc


def test_member_add_to_global_group(self, member_name, client_code, global_group, log_checker=None):
    def member_add_to_global_group():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.log('Find member "{}" row'.format(member_name))
        member_row = self.wait_until_visible(type=By.XPATH, element=MEMBER_TABLE_CLICK_MEMBER.format(member_name))
        self.log('Open member details')
        self.click(member_row)
        self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
        self.wait_jquery()
        self.log('Open global groups tab')
        self.wait_until_visible(type=By.XPATH, element=GLOBAL_GROUP_TAB).click()
        self.log('SERVICE_37 1. Clicking "Add global group" button')
        self.wait_until_visible(type=By.XPATH, element=ADD_MEMBER_TO_GLOBAL_GROUP_BTN_ID).click()
        self.log('SERVICE_37 2. Selecting global group "{}" from the list'.format(global_group))
        self.select(type=By.ID, element=GROUP_SELECT_ID, value=global_group)
        self.log('Click on "OK"')
        self.wait_until_visible(type=By.XPATH, element=GROUP_POPUP_OK_BTN_XPATH).click()
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=NOTICE_MESSAGE_CSS).text
        expected_notice_msg = MEMBER_ADDED_TO_GLOBAL_GROUP.format(client_code, global_group)
        self.log('SERVICE_37 3. System displays the message: "{}"'.format(expected_notice_msg))
        self.is_equal(expected_notice_msg, notice_msg)
        if current_log_lines is not None:
            expected_log_msg = ADD_MEMBER_TO_GLOBAL_GROUP

            self.log('SERVICE_37 4. System logs the event "{}"'.format(expected_log_msg))
            try:
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
            except:
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)

    return member_add_to_global_group


def test_member_remove_from_global_group(self, member_name, client_code, group_name, log_checker=None):
    def member_remove_from_global_group():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.log('Find member "{}" row'.format(member_name))
        member = self.wait_until_visible(type=By.XPATH, element=MEMBER_TABLE_CLICK_MEMBER.format(member_name))
        self.log('Open member details')
        member.click()
        self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
        self.wait_jquery()
        self.log('Open global groups tab')
        self.wait_until_visible(type=By.XPATH, element=GLOBAL_GROUP_TAB).click()
        self.wait_jquery()
        self.log('Click on group "{}" row'.format(group_name))
        self.wait_until_visible(type=By.XPATH, element=GROUP_ROW_BY_TEXT.format(group_name)).click()
        self.log('SERVICE_38 1. Click on "Delete" button')
        self.wait_until_visible(type=By.XPATH, element=DELETE_MEMBER_FROM_GLOBAL_GROUP_BTN_ID).click()
        self.log('Confirm deletion')
        confirm_dialog_click(self)
        self.wait_jquery()
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=NOTICE_MESSAGE_CSS).text
        expected_notice_msg = MEMBER_DELETED_FROM_GLOBAL_GROUP.format(client_code, group_name)
        self.log('SERVICE_38 2. System displays the notice message "{}"'.format(expected_notice_msg))
        self.is_equal(expected_notice_msg, notice_msg)
        if current_log_lines is not None:
            expected_log_msg = REMOVE_MEMBER_FROM_GLOBAL_GROUP
            self.log('SERVICE_38 3. System logs the event "{}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

    return member_remove_from_global_group
