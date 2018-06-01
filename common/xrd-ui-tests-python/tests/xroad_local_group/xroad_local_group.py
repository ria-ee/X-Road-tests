from selenium.webdriver.common.by import By

from helpers import auditchecker, xroad, soaptestclient
from view_models import sidebar as sidebar_constants, clients_table_vm, popups, members_table, messages, log_constants

from view_models import groups_table
from view_models.groups_table import GROUP_DETAILS_BTN_ID
from view_models.log_constants import ADD_GROUP_FAILED, ADD_GROUP
from view_models.messages import MISSING_PARAMETER, INPUT_EXCEEDS_255_CHARS, GROUP_ALREADY_EXISTS_ERROR, \
    get_error_message


def test_add_member_to_local_group(client_name=None, subsystem=None):
    def test_case(self):

        members_name_and_subs = {}
        added_local_group_code = 'test_local_group_code'
        added_local_group_description = 'test_local_group_description'

        self.log('''Open Members tab''')
        self.wait_jquery()
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.MEMBERS_CSS).click()

        self.log('''Get member names and their subsystems from the central server''')
        self.wait_jquery()

        members = self.wait_until_visible(type=By.CSS_SELECTOR, element='#members tbody tr', multiple=True)
        for member in members:
            members_subsystems = []

            self.log('''Double click on member "{0}" row'''.format(member.text))
            # member_row = self.wait_until_visible(type=By.XPATH, element=members_table.
            #                                      get_member_data_from_table(1, member.text))
            # self.double_click(member_row)

            member.click()

            # Open the client details and subsystem tab
            self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
            self.wait_jquery()



            self.log('Click on "Subsystem" tab')
            self.wait_jquery()
            self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()

            self.log('Get subsystems for member')
            self.wait_jquery()
            subsystem_codes = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_CODE_XPATH,
                                                      multiple=True)

            '''Loop through subsystem codes and if there are any, add them to the list'''
            for subsystem_code in subsystem_codes:
                if subsystem_code.text.encode('utf-8') != 'No (matching) records':
                    members_subsystems.append(subsystem_code.text.encode('utf-8'))

            '''Add member and member subsystem codes list to the dictionary'''
            if len(members_subsystems) > 0:
                members_name_and_subs[member.find_element_by_tag_name('td').text] = members_subsystems

            self.log('''Click on "CLOSE" button''')
            self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH) \
                .click()

        self.log('''Dictionary with central server members and subsystem codes:
        {0}'''.format(members_name_and_subs))
        #######################################################################################################################
        self.log('Open security server')
        url = self.config.get('ss2.host')
        username = self.config.get('ss2.user')
        password = self.config.get('ss2.pass')
        self.reload_webdriver(url, username, password)
        test_service_2_url = self.config.get('services.test_service_2_url')

        ss_client_id = self.config.get('ss2.client_id')

        '''Add a local group'''
        add_local_group(self, added_local_group_code, added_local_group_description, ss_client_id, client_name=client_name, subsystem=subsystem)

        self.log('Click on "CLOSE" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        '''Add a local group to service'''

        add_local_group_to_service_url(self, ss_client_id, test_service_2_url, added_local_group_description)
        #######################################################################################################################
        '''Add members to local group'''
        self.log('Click on "Local groups" tab')
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_LOCAL_GROUPS_TAB_XPATH).click()

        self.log('Click on a added local group code - {0}'.format(added_local_group_code))
        added_local_group_row = self.wait_until_visible(type=By.XPATH, element=popups.
                                                        get_local_group_row_by_code(added_local_group_code))

        self.click(added_local_group_row)
        self.wait_until_visible(type=By.ID,
                                element=groups_table.GROUP_DETAILS_BTN_ID).click()
        self.log('Click on "ADD MEMBERS" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID).click()

        self.log('Click on "SEARCH" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DETAILS_BUTTON_SEARCH_XPATH).click()

        self.wait_jquery()
        #######################################################################################################################
        ss_host = self.config.get('ss2.ssh_host')
        ss_host_user = self.config.get('ss2.ssh_user')
        ss_host_psw = self.config.get('ss2.ssh_pass')

        log_checker = auditchecker.AuditChecker(host=ss_host, username=ss_host_user, password=ss_host_psw)

        self.log('Get founded members and members subsystem codes')
        founded_members_and_subsystems = {}
        founded_members = self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_FOUNDED_MEMBERS_XPATH,
                                                  multiple=True)
        founded_subsystems = self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_FOUNDED_SUBSYSTEMS_XPATH,
                                                     multiple=True)
        '''Loop through founded members and subsystem codes'''
        founded_ids = []
        for members_subs_counter in range(len(founded_members)):
            founded_id = founded_subsystems[members_subs_counter].text.encode('utf-8')

            founded_ids.append(founded_id)
            founded_sub = founded_id.split(' : ')
            founded_sub = founded_sub[-1]
            founded_member = founded_members[members_subs_counter].text.encode('utf-8')
            '''Add founded members and subsystem codes to the dictionary'''
            if founded_member in founded_members_and_subsystems:
                founded_members_and_subsystems[founded_member].append(founded_sub)
            else:
                founded_members_and_subsystems[founded_member] = [founded_sub]

        self.log('''Dictionary with founded members and subsystem codes: 
        {0}'''.format(founded_members_and_subsystems))
        '''SERVICE_26/2 ...It is possible to add only X-Road members' subsystems to the group...'''
        self.log('''Compare central server members and subsystems with these, what can add to the local group''')
        compared_members_subsystems = False
        for member_name in founded_members_and_subsystems:
            compared_members_subsystems = False
            if sorted(founded_members_and_subsystems[member_name]) == sorted(members_name_and_subs[member_name]):
                compared_members_subsystems = True
        assert compared_members_subsystems is True
        #######################################################################################################################
        for member_id in founded_ids:
            requesting_id = member_id.find(':')
            requesting_id = member_id[requesting_id + 2:]

            if requesting_id == self.config.get('ss2.client2_id'):
                soap_request(self, ss_client_id, requesting_id, request_success=False)

            current_log_lines = log_checker.get_line_count()
            self.log('''SERVICE_26/1 SS administrator selects to add group members to the local group.
             SERVICE_26/2 ...SS administrator selects subsystems and adds them to the local group...
             By clicking on founded member id - "{0}" ...'''.format(member_id))
            self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_FOUNDED_MEMBER_ID_XPATH
                                    .format(member_id)).click()
            self.log('... and clicking on "ADD SELECTED TO GROUP" button')
            self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_ADD_SELECTED_TO_GROUP_BTN_ID).click()

            self.wait_jquery()

            self.log('''SERVICE_26/4 System logs the event "Add members to group" to the audit log.''')
            logs_found = log_checker.check_log(log_constants.ADD_MEMBER_TO_LOCAL_GROUP,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found, msg="Add members to group")

            if requesting_id == self.config.get('ss2.client2_id'):
                soap_request(self, ss_client_id, requesting_id, request_success=True)

            self.log('Click on "ADD MEMBERS" button')
            self.wait_jquery()
            self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID).click()

            self.log('Click on "SEARCH" button')
            self.wait_jquery()
            self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DETAILS_BUTTON_SEARCH_XPATH).click()

        self.log('''SERVICE_26/2 ...and it is possible to add only those subsystems that are not already members of 
        this group...., by verifying that there no members in the members search table''')
        verify_empty_search_table(self)

        verify_added_members(self, founded_ids, members_name_and_subs)
        ########################################################################################################################
        self.log('Click on "REMOVE ALL MEMBERS" button')
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_REMOVE_ALL_MEMBERS_BTN_ID).click()

        self.log('Click on "ADD MEMBERS" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID).click()

        self.log('Click on "SEARCH" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DETAILS_BUTTON_SEARCH_XPATH).click()

        self.log('Click on "ADD ALL TO GROUP" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_ADD_ALL_TO_GROUP_BTN_ID).click()

        self.log('Click on "ADD MEMBERS" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID).click()

        self.log('''Verify that there no members in the members search table''')
        verify_empty_search_table(self)

        verify_added_members(self, founded_ids, members_name_and_subs)
        ########################################################################################################################
        '''Delete local group'''
        delete_local_group(self)

        self.log('Click on "CLOSE" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

    return test_case


def test_edit_local_group_description():
    def test_case(self):

        added_local_group_code = 'test_local_group_code'
        added_local_group_description = 'test_local_group_description'
        descriptions = [['', True, "Missing parameter: {0}", "description", None],
                        [256 * 'T', True, "Parameter '{0}' input exceeds 255 characters", "description", None],
                        ['test_description', None, None, None, None],
                        ['    description_test     ', None, None, None, True],
                        [255 * 't', None, None, None, None]
                        ]
        ss_client_id = self.config.get('ss2.client_id')

        client_name = self.config.get('ss2.client_name')
        subsystem_row = xroad.split_xroad_subsystem(self.config.get('ss2.client_id'))
        subsystem = subsystem_row['subsystem']

        '''Add a local group'''
        add_local_group(self, added_local_group_code, added_local_group_description, ss_client_id, client_name, subsystem)

        ss_host = self.config.get('ss2.ssh_host')
        ss_host_user = self.config.get('ss2.ssh_user')
        ss_host_psw = self.config.get('ss2.ssh_pass')

        log_checker = auditchecker.AuditChecker(host=ss_host, username=ss_host_user, password=ss_host_psw)
        counter = 1
        for description_input in descriptions:
            description = description_input[0]
            error_exists = description_input[1]
            error_message = description_input[2]
            error_message_label = description_input[3]
            whitespaces = description_input[4]

            current_log_lines = log_checker.get_line_count()

            self.log('Double click on a added local group code - {0}'.format(added_local_group_code))
            added_local_group_row = self.wait_until_visible(type=By.XPATH, element=popups.
                                                            get_local_group_row_by_code(added_local_group_code))


            '''Click on local group row'''
            self.click(added_local_group_row)
            '''Click on "Details" button'''
            self.wait_until_visible(type=By.ID, element=GROUP_DETAILS_BTN_ID).click()

            self.log('TEST - {0}'.format(counter))
            self.log('SERVICE_28/1 SS administrator selects to edit the description of a local group, '
                     'by clicking on "EDIT" button')
            self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_EDIT_DESCRIPTION_BTN_XPATH).click()

            self.log('SERVICE_28/2 SS administrator inserts the description, '
                     'by inserting (string length = {0}) - {1} - to the "Edit Description" text field'
                     .format(len(description), description))
            description_text_field = self.wait_until_visible(type=By.ID,
                                                             element=popups.LOCAL_GROUP_EDIT_DESCRIPTION_TEXT_FIELD_ID)
            self.input(description_text_field, description)

            self.log('Click on "OK" button')
            self.wait_jquery()
            self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_EDIT_DESCRIPTION_OK_BTN_XPATH).click()

            self.log('SERVICE_28/3 System parses the user input')
            '''Verify error message'''
            error_messages(self, error_exists, error_message, error_message_label)

            if error_exists:
                self.log('SERVICE_28/3a.1 System displays the termination message from the parsing process.')
                self.log('SERVICE_28/3a.2 System logs the event "Edit group description failed" to the audit log..')

                logs_found = log_checker.check_log(log_constants.EDIT_GROUP_DESCRIPTION_FAILED,
                                                   from_line=current_log_lines + 1)
                self.is_true(logs_found, msg="Edit group description failed")

                self.log('SERVICE_28/3a.3a CS administrator selects to terminate the use case, '
                         'by clicking on "CANCEL" button')
                self.wait_until_visible(type=By.XPATH,
                                        element=popups.LOCAL_GROUP_EDIT_DESCRIPTION_CANCEL_BTN_XPATH).click()
                self.log('Click on "CLOSE" button')
                self.wait_jquery()
                self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DETAILS_CLOSE_BTN_XPATH).click()

            else:
                self.wait_jquery()
                self.log('SERVICE_28/4 System saves the local group description to the system configuration.')
                self.log('Find edited description (string length = {0})- {1}'.format(len(description.strip()),
                                                                                     description.strip()))
                edited_text = self.wait_until_visible(type=By.ID, element=popups.
                                                      LOCAL_GROUP_DESCRIPTION_TEXT_FIELD_ID)
                edited_text = edited_text.text

                if whitespaces:
                    find_text_with_whitespaces(self, description, edited_text)
                else:
                    assert description in edited_text
                    self.log('Found description - ' + edited_text)

                self.log('Click on "CLOSE" button')
                self.wait_jquery()
                self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DETAILS_CLOSE_BTN_XPATH).click()

                self.log('Find edited description in the client details table (string length = {0})- {1}'
                         .format(len(description.strip()), description.strip()))
                edited_text = self.wait_until_visible(type=By.XPATH, element=popups.
                                                      LOCAL_GROUP_EDITED_DESCRIPTION_CLIENT_DETAILS_XPATH
                                                      .format(description.strip()))
                edited_text = edited_text.text

                if whitespaces:
                    find_text_with_whitespaces(self, description, edited_text)
                else:
                    assert description in edited_text
                    self.log('Found description - ' + edited_text)

                self.log('''SERVICE_28/5 System logs the event "Edit group description" to the audit log.''')
                logs_found = log_checker.check_log(log_constants.EDIT_GROUP_DESCRIPTION,
                                                   from_line=current_log_lines + 1)
                self.is_true(logs_found, msg="Edit group description")

            counter += 1

        self.log('Double click on a added local group code - {0}'.format(added_local_group_code))
        added_local_group_row = self.wait_until_visible(type=By.XPATH, element=popups.
                                                        get_local_group_row_by_code(added_local_group_code))
        self.click(added_local_group_row)
        self.wait_until_visible(type=By.ID, element=GROUP_DETAILS_BTN_ID).click()
        '''Delete local group'''
        delete_local_group(self)

        self.log('Click on "CLOSE" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

    return test_case


def test_remove_member_from_local_group():
    def test_case(self):
        added_local_group_code = 'test_local_group_code'
        added_local_group_description = 'test_local_group_description'
        test_service_2_url = self.config.get('services.test_service_2_url')
        ss_client_id = self.config.get('ss2.client_id')
        requesting_id = self.config.get('ss2.client2_id')

        ss_host = self.config.get('ss2.ssh_host')
        ss_host_user = self.config.get('ss2.ssh_user')
        ss_host_psw = self.config.get('ss2.ssh_pass')

        log_checker = auditchecker.AuditChecker(host=ss_host, username=ss_host_user, password=ss_host_psw)
        current_log_lines = log_checker.get_line_count()
        client_name = self.config.get('ss2.client_name')
        subsystem_row = xroad.split_xroad_subsystem(self.config.get('ss2.client_id'))
        subsystem = subsystem_row['subsystem']


        '''Add a local group'''
        add_local_group(self, added_local_group_code, added_local_group_description, ss_client_id, client_name, subsystem)

        self.log('Click on "CLOSE" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        '''Add a local group to service'''
        add_local_group_to_service_url(self, ss_client_id, test_service_2_url, added_local_group_description)

        '''Add members to local group'''
        self.log('Click on "Local groups" tab')
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_LOCAL_GROUPS_TAB_XPATH).click()

        self.log('Click on a added local group code - {0}'.format(added_local_group_code))
        added_local_group_row = self.wait_until_visible(type=By.XPATH, element=popups.
                                                        get_local_group_row_by_code(added_local_group_code))
        '''Click on local group row'''
        self.click(added_local_group_row)
        '''Click on "Details" button'''
        self.wait_until_visible(type=By.ID, element=GROUP_DETAILS_BTN_ID).click()

        self.log('Click on "ADD MEMBERS" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID).click()

        self.log('Click on "SEARCH" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DETAILS_BUTTON_SEARCH_XPATH).click()
        self.wait_jquery()

        self.log('Find member id - "{0}" - and click on it.'.format(requesting_id))
        members_partial_id = self.wait_until_visible(type=By.XPATH, element=popups
                                                     .LOCAL_GROUP_FOUNDED_MEMBER_ID_PARTIAL_XPATH
                                                     .format(requesting_id))
        member_id = members_partial_id.text
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_FOUNDED_MEMBER_ID_XPATH
                                .format(member_id)).click()

        self.log('Click on "ADD SELECTED TO GROUP" button')
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_ADD_SELECTED_TO_GROUP_BTN_ID).click()

        self.log('Request with added member should sucsess')
        soap_request(self, ss_client_id, requesting_id, request_success=True)

        self.log('Click on "ADD MEMBERS" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID).click()

        self.log('Click on "SEARCH" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DETAILS_BUTTON_SEARCH_XPATH).click()

        self.log('Click on "ADD ALL TO GROUP" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_ADD_ALL_TO_GROUP_BTN_ID).click()

        self.log('SERVICE_27 1 SS administrator selects to remove subjects from a local group.')
        self.log('SERVICE_27 2 SS administrator selects group members... by clicking on added member id - "{0}"'
                 .format(requesting_id))
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_TABLE_SUB_IN_ID_XPATH.format(requesting_id)) \
            .click()

        self.log('SERVICE_27 2 ...and removes them from the local group, by clicking on button '
                 '"REMOVE SELECTED MEMBERS".')
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_REMOVE_SELECTED_MEMBERS_BTN_ID).click()

        self.log('SERVICE_27 3 System removes group members from the local group.')
        self.wait_jquery()
        try:
            self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_TABLE_SUB_IN_ID_XPATH
                                    .format(requesting_id))
            member_removed = False
        except:
            member_removed = True
        assert member_removed is True

        self.log('SERVICE_27 4 System logs the event "Remove members from group" to the audit log.')
        logs_found = log_checker.check_log(log_constants.REMOVE_MEMBERS_FROM_GROUP, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg="Remove members from group")

        self.log('SERVICE_27 3 The access rights granted for the group will not be available '
                 'for the removed group members. Request should fail')
        soap_request(self, ss_client_id, requesting_id, request_success=False)

        self.log('SERVICE_27 2 ...and removes them from the local group, '
                 'by clicking on button "REMOVE ALL MEMBERS" button')
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_REMOVE_ALL_MEMBERS_BTN_ID).click()

        self.log('SERVICE_27 4 System logs the event "Remove members from group" to the audit log.')
        logs_found = log_checker.check_log(log_constants.REMOVE_MEMBERS_FROM_GROUP, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg="Remove members from group")

        self.log('SERVICE_27 3 System removes group members from the local group.')
        members_table_is_empty = self.wait_until_visible(type=By.XPATH,
                                                         element=popups
                                                         .LOCAL_GROUP_EMPTY_MEMBERS_TABLE_XPATH).is_displayed()
        assert members_table_is_empty is True

        '''Delete local group'''
        delete_local_group(self)

        self.log('Click on "CLOSE" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

    return test_case


def test_delete_local_group(client_name=None, subsystem=None):
    def test_case(self):
        added_local_group_code = 'test_local_group_code'
        added_local_group_description = 'test_local_group_description'
        test_service_2_url = self.config.get('services.test_service_2_url')
        ss_client_id = self.config.get('ss2.client_id')
        requesting_id = self.config.get('ss2.client2_id')

        ss_host = self.config.get('ss2.ssh_host')
        ss_host_user = self.config.get('ss2.ssh_user')
        ss_host_psw = self.config.get('ss2.ssh_pass')

        log_checker = auditchecker.AuditChecker(host=ss_host, username=ss_host_user, password=ss_host_psw)
        current_log_lines = log_checker.get_line_count()

        '''Add a local group'''
        add_local_group(self, added_local_group_code, added_local_group_description, ss_client_id, client_name=client_name, subsystem=subsystem)

        self.log('Click on "CLOSE" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        '''Add a local group to service'''
        add_local_group_to_service_url(self, ss_client_id, test_service_2_url, added_local_group_description)

        '''Add members to local group'''
        self.log('Click on "Local groups" tab')
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_LOCAL_GROUPS_TAB_XPATH).click()

        self.log('Click on a added local group code - {0}'.format(added_local_group_code))
        self.wait_jquery()
        added_local_group_row = self.wait_until_visible(type=By.XPATH, element=popups.
                                                        get_local_group_row_by_code(added_local_group_code))

        self.click(added_local_group_row)
        self.wait_until_visible(type=By.ID, element=GROUP_DETAILS_BTN_ID).click()



        self.log('Click on "ADD MEMBERS" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID).click()

        self.log('Click on "SEARCH" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DETAILS_BUTTON_SEARCH_XPATH).click()
        self.wait_jquery()

        self.log('Find member id - "{0}" - and click on it.'.format(requesting_id))
        members_partial_id = self.wait_until_visible(type=By.XPATH, element=popups
                                                     .LOCAL_GROUP_FOUNDED_MEMBER_ID_PARTIAL_XPATH
                                                     .format(requesting_id))
        member_id = members_partial_id.text
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_FOUNDED_MEMBER_ID_XPATH
                                .format(member_id)).click()

        self.log('Click on "ADD SELECTED TO GROUP" button')
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_ADD_SELECTED_TO_GROUP_BTN_ID).click()

        self.log('Request with added member should sucsess')
        soap_request(self, ss_client_id, requesting_id, request_success=True)

        self.log('SERVICE_29/1 SS administrator selects to delete a local group, '
                 'by clicking on "DELETE GROUP" button.')
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DELETE_GROUP_BTN_ID).click()

        self.log('SERVICE_29/2 System prompts for confirmation to delete the local group.')
        self.wait_jquery()
        confirm_pop_up_displayed = self.wait_until_visible(type=By.XPATH,
                                                           element=popups.LOCAL_GROUP_DELETE_CONFIRM_POP_UP_XPATH) \
            .is_displayed()
        assert confirm_pop_up_displayed is True

        self.log('SS administrator terminates the use case, by clicking on "CANCEL" button.')
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DELETE_GROUP_CANCEL_BTN_XPATH).click()

        self.log('SERVICE_29/1 SS administrator selects to delete a local group, '
                 'by clicking on "DELETE GROUP" button.')
        self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DELETE_GROUP_BTN_ID).click()

        self.log('SERVICE_29/3 SS administrator confirms, by clicking on "CONFIRM" button')
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DELETE_GROUP_CONFIRM_BTN_XPATH).click()

        self.log('SERVICE_29/4 System deletes the local group from the system configuration, '
                 'by verifying that local group table is empty')
        self.wait_jquery()
        group_table_is_empty = self.wait_until_visible(type=By.XPATH,
                                                       element=popups.LOCAL_GROUP_EMPTY_TABLE_XPATH).is_displayed()
        assert group_table_is_empty is True

        self.log('SERVICE_29/4 The access rights that were granted for the group will not be available '
                 'for the X-Road subsystems that were the members of this group. Request should fail')
        soap_request(self, ss_client_id, requesting_id, request_success=False)

        self.log('SERVICE_29/5 System logs the event "Delete group" to the audit log.')
        logs_found = log_checker.check_log(log_constants.DELETE_GROUP, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg="Delete group")

        self.log('Click on "CLOSE" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

    return test_case


def add_local_group(self, local_group_code, local_group_description, ss_client_id, client_name, subsystem):
    """
    Add local group
    :param self: MainController object
    :param local_group_code: str
    :param local_group_description: str
    :param ss_client_id: str
    :return: None
    """
    self.log('Open clients details, by double clicking on client id')




    client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(client_name,subsystem))


    client_row.find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS).click()

    self.log('Click on "Local groups" tab')
    self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_LOCAL_GROUPS_TAB_XPATH).click()

    self.log('SERVICE_25 1. Click on "ADD GROUP" button')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_GROUP_ADD_BTN_ID).click()

    if len(local_group_code) > 15:
        self.log('SERVICE_25 2. Insert {} length code for the new local group'.format(len(local_group_code.strip())))
    else:
        self.log('SERVICE_25 2. Insert "Code" for the new local group - "{0}"'.format(local_group_code))
    new_group_code = self.wait_until_visible(type=By.ID, element=popups.GROUP_ADD_POPUP_CODE_AREA_ID)
    self.input(new_group_code, local_group_code)

    if len(local_group_description) > 15:
        self.log('SERVICE_25 2. Insert {} length description for the new local group'.format(len(local_group_description.strip())))
    else:
        self.log('SERVICE_25 2. Insert "Description" for the new local group - "{0}"'.format(local_group_description))
    new_group_description = self.wait_until_visible(type=By.ID, element=popups.GROUP_ADD_POPUP_CODE_DESCRIPTION_ID)
    self.input(new_group_description, local_group_description)

    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()


def delete_local_group(self):
    """
    Delete local group
    :param self: MainController object
    :return: None
    """
    self.log('Delete local group by clicking on "DELETE GROUP" button...')
    self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DELETE_GROUP_BTN_ID).click()
    self.log('... and clicking on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DELETE_GROUP_CONFIRM_BTN_XPATH).click()


def verify_empty_search_table(self):
    """
    Verifyies that there are not members in a local group members search table
    :param self: MainController object
    :return: None
    """
    searc_members_table_is_empty = self.wait_until_visible(type=By.XPATH,
                                                           element=popups.LOCAL_GROUP_EMPTY_MEMBERS_SEARCH_TABLE_XPATH) \
        .is_displayed()
    assert searc_members_table_is_empty is True
    self.log('Members search table is empty')

    self.log('Click on "CANCEL" button')
    self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_SEARCH_MEMBERS_TABLE_CANCEL_BTN_XPATH).click()


def verify_added_members(self, founded_ids, members_name_and_subs):
    """
    Verifyies that added members count is equalt to the members count in a local group table and added members are in a
    local group table
    :param self:
    :param founded_ids: list with founded member id's
    :param members_name_and_subs: dictionary with central service member codes and subsystems
    :return: None
    """
    self.log('SERVICE_26/3 System adds group members to the local group, '
             'by verifying that added members count is equalt to the members count in a local group table ')
    group_members_count = self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_MEMBERS_COUNT_ID)
    group_members_count = int(group_members_count.text)
    assert group_members_count is len(founded_ids)
    self.log('There were added "{0}" members to a local group'.format(group_members_count))

    self.log('And by verifying that added members are in a local group table')
    '''Loop through central server members and subsystems dictionary and verify that they are in a 
    local group table'''
    for local_member in members_name_and_subs:
        self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_TABLE_MEMBERS_NAME_XPATH
                                .format(local_member))
        for sub in members_name_and_subs[local_member]:
            self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_TABLE_SUB_IN_ID_XPATH
                                    .format(sub))
            self.log('In a local group table, a member - "{0}" - id contains subsystem - "{1}'
                     .format(local_member, sub))


def error_messages(self, error, error_message, error_message_label):
    """
    Function Check for the error messages
    :param self: MainController object
    :param error: bool - Must there be a error message, True if there is and False if not
    :param error_message: str - Expected error message
    :param error_message_label: str - label for a expected error message
    :return:
    """
    if error:
        '''System displays the error message'''
        '''Get a error message, compare it with expected error message and close error message'''
        self.log('Get the error message')
        self.wait_jquery()
        get_error_message = messages.get_error_message(self)
        self.log('Found error message - ' + get_error_message)
        self.log('Expected error message  - ' + error_message.format(error_message_label))

        self.log('Compare error message to the expected error message')
        assert get_error_message in error_message.format(error_message_label)

        self.log('Close the error message')
        messages.close_error_messages(self)
    else:
        '''Verify that there is not error messages'''
        self.log('Verify that there is not error messages')
        get_error_message = messages.get_error_message(self)
        if get_error_message is None:
            error = False
        else:
            error = True
        assert error is False


def find_text_with_whitespaces(self, added_text, expected_text):
    """
    Verifies, that there is not inputs with whitespaces
    :param self: MainController object
    :param added_text: str - added text
    :param expected_text: str - expected text
    :return: None
    """
    try:
        '''Compare added text and displayed text'''
        self.log('Compare added text and displayed text')
        self.log("'" + added_text + "' is not in '" + expected_text + "'")
        assert added_text in expected_text
        whitespace = True
    except:
        '''Compare added text without whitespaces and displayed text'''
        self.log('Compare added text without whitespaces and displayed text')
        self.log("'" + added_text.strip() + "' is in'" + expected_text + "'")
        assert added_text.strip() in expected_text
        whitespace = False
    assert whitespace is False


def soap_request(self, client_id, requester_id, request_success=None):
    """
    Test client to send SOAP queries to the test services. Uses XML ElementTree for parsing XML and UUID to generate
    unique IDs for requests.
    :param self: MainController object
    :param client_id: str
    :param requester_id: str
    :param request_success: str
    :return: None
    """
    faults_unsuccessful = ['Server.ServerProxy.AccessDenied']
    # These faults are checked when we need the result to be successful. Otherwise the checking function returns False.
    faults_successful = ['Server.ServerProxy.ServiceFailed.NetworkError']

    query_url = self.config.get('ss2.service_path')
    query_filename = self.config.get('services.request_template_filename')
    query = self.get_xml_query(query_filename)

    service_name = self.config.get('services.test_service_2')

    # Immediate queries, no delay needed, no retry allowed.
    sync_retry = 0
    sync_max_seconds = 0

    client = xroad.split_xroad_id(client_id)
    requester = xroad.split_xroad_subsystem(requester_id, member_type='SUBSYSTEM')

    testclient_params = {
        'xroadProtocolVersion': self.config.get('services.xroad_protocol'),
        'xroadIssue': self.config.get('services.xroad_issue'),
        'xroadUserId': self.config.get('services.xroad_userid'),
        'serviceMemberInstance': client['instance'],
        'serviceMemberClass': client['class'],
        'serviceMemberCode': client['code'],
        'serviceSubsystemCode': client['subsystem'],
        'serviceCode': xroad.get_service_name(service_name),
        'serviceVersion': xroad.get_service_version(service_name),
        'memberInstance': requester['instance'],
        'memberClass': requester['class'],
        'memberCode': requester['code'],
        'subsystemCode': requester['subsystem'],
        'requestBody': self.config.get('services.testservice_2_request_body')
    }

    testclient_http = soaptestclient.SoapTestClient(url=query_url, body=query,
                                                    retry_interval=sync_retry, fail_timeout=sync_max_seconds,
                                                    faults_successful=faults_successful,
                                                    faults_unsuccessful=faults_unsuccessful, params=testclient_params)

    if request_success:
        self.is_true(testclient_http.check_success(), msg='Test query succeeded')
    else:
        self.is_true(testclient_http.check_fail(), msg='Test query failed')


def add_local_group_to_service_url(self, ss_client_id, test_service_2_url, added_local_group_description):
    """
    Add local group to a ACL
    :param self: MainController object
    :param ss_client_id: str - client id
    :param test_service_2_url: str - test service url
    :param added_local_group_description: str - local group description
    :return: None
    """
    '''Add a local group to service'''
    self.log('Open clients details, by double clicking on client id')
    ss_client_id_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.get_client_id(ss_client_id))

    client_name = self.config.get('ss2.client_name')
    subsystem_row = xroad.split_xroad_subsystem(self.config.get('ss2.client_id'))
    subsystem = subsystem_row['subsystem']


    client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(client_name,subsystem))


    client_row.find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS).click()


    self.log('Click on "Services" tab')
    self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_SERVICES_TAB_XPATH).click()

    self.log('Click on WSDL "+"')
    self.wait_until_visible(type=By.CLASS_NAME, element=popups.CLIENT_DETAILS_POPUP_WSDL_URL_DETAILS_CLASS).click()

    self.log('Click on service url - {0}'.format(test_service_2_url))
    self.wait_until_visible(type=By.XPATH, element=popups.get_service_url_row(test_service_2_url)).click()

    self.log('Click on "ACCESS RIGHTS" button')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ACCESS_RIGHTS_BTN_ID).click()

    self.log('Click on "ADD SUBJECTS" button')
    self.wait_until_visible(type=By.ID, element=popups.
                            CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_ADD_SUBJECTS_BTN_CSS).click()

    self.log('Click on "SEARCH" button')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=popups.ACL_SUBJECTS_SEARCH_POPUP_SEARCH_BTN_CSS).click()

    self.log('Click on "{0}" row'.format(added_local_group_description))
    self.wait_until_visible(type=By.XPATH, element=popups.
                            ACL_ADD_SUBJECTS_BY_NAME_XPATH.format(added_local_group_description)).click()

    self.log('Click on "ADD SELECTED TO ACL" button')
    self.wait_until_visible(type=By.ID, element=popups.ACL_SUBJECTS_SEARCH_POPUP_ADD_SELECTED_TO_ACL_BUTTON_ID) \
        .click()

    self.log('Click on "CLOSE" button')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=popups.ACL_FOR_SERVICE_CLOSE_BTN_XPATH).click()


def add_group_to_client(self, client_id, log_checker=None, subsystem=None, client_name=None):
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
    current_log_lines = None
    if log_checker:
        current_log_lines = log_checker.get_line_count()
    code_255_len = ' {0} '.format('A' * 255)
    code_255_len_stripped = code_255_len.strip()
    code_256_len = 'A' * 256
    local_group_test_data = [
        ['', 'asd', MISSING_PARAMETER.format('add_group_code'), ADD_GROUP_FAILED, 'Missing code'],
        ['asd', '', MISSING_PARAMETER.format('add_group_description'), ADD_GROUP_FAILED, 'Missing description'],
        [code_256_len, 'asd', INPUT_EXCEEDS_255_CHARS.format('add_group_code'), ADD_GROUP_FAILED, 'Too long code'],
        ['asd', code_256_len, INPUT_EXCEEDS_255_CHARS.format('add_group_description'), ADD_GROUP_FAILED,
         'Too long description'],
        [code_255_len, code_255_len, None, ADD_GROUP, 'Max length code and description'],
        [code_255_len_stripped, code_255_len_stripped, GROUP_ALREADY_EXISTS_ERROR, ADD_GROUP_FAILED, 'Group exists.']
    ]
    for local_group_data in local_group_test_data:
        local_group_code = local_group_data[0]
        local_group_description = local_group_data[1]
        error = local_group_data[2]
        log = local_group_data[3]
        log_msg = local_group_data[4]
        use_case = 'SERVICE_25 3a'
        if error is GROUP_ALREADY_EXISTS_ERROR:
            use_case = 'SERVICE_25 4a'
            error = error.format(code_255_len_stripped)
        self.log('{} user input parsing: "{}"'.format(use_case, log_msg))
        add_local_group(self, local_group_code, local_group_description, client_id, subsystem=subsystem, client_name=client_name)
        self.wait_jquery()
        self.log('Checking error message')
        error_msg = get_error_message(self)
        self.is_equal(error, error_msg)
        popups.close_all_open_dialogs(self)
        if current_log_lines:
            self.log('{}.2 Checking log for event "{}"'.format(use_case, log))
            logs_found = log_checker.check_log(log, from_line=current_log_lines + 1)
            self.is_true(logs_found)

    '''Get client row'''
    client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                         get_client_id_by_member_code_subsystem_code(client_name, subsystem))

    '''Click on "Details" button'''

    client_row.find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS).click()


    self.log('Click on "Local groups" tab')
    self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_LOCAL_GROUPS_TAB_XPATH).click()

    self.wait_jquery()
    self.log('Double click on a added max length local group code')
    added_local_group_row = self.wait_until_visible(type=By.XPATH, element=popups.
                                                    get_local_group_row_by_code(code_255_len_stripped))
    self.click(added_local_group_row)

    '''Click on "Details" button'''
    self.wait_until_visible(type=By.ID, element=GROUP_DETAILS_BTN_ID).click()
    self.wait_jquery()

    '''Delete local group'''
    delete_local_group(self)
    self.wait_jquery()
