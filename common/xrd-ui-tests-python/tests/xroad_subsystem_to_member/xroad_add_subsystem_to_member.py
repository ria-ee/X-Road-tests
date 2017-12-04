from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import auditchecker
from view_models import sidebar as sidebar_constants, members_table, messages, log_constants


def test_add_subsystem():
    def test_case(self):
        cs_ssh_host = self.config.get('cs.ssh_host')
        cs_ssh_user = self.config.get('cs.ssh_user')
        cs_ssh_pass = self.config.get('cs.ssh_pass')

        member_name = 'TEST_SUB_NAME'
        member_class = 'GOV'
        member_code = 'TEST_SUB_CODE'
        subsystem_text = 'test_subsystem_text'
        subsystem_inputs = [['', None, None, None, None],
                            [256 * 'T', True, "Parameter '{0}' input exceeds 255 characters", "subsystemCode", None],
                            ['test_subsystem', None, None, None, None],
                            ['    test_subsystem     ', None, None, None, True],
                            [255 * 't', None, None, None, None]
                            ]

        '''Add member'''
        add_cs_member(self, member_name, member_class, member_code)
#######################################################################################################################
        self.log('TEST - 1')

        '''MEMBER_56/4 System verifies that a subsystem with the inserted code is not already saved for this 
        X-Road member in the system configuration.'''
        self.log('''MEMBER_56/4 System verifies that a subsystem with the inserted code is not already saved for this 
        X-Road member in the system configuration.''')
        add_subsystem_to_member(self, member_name, subsystem_text)
        self.log('''Click on "OK" button''')
        self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_OK_BTN_XPATH).click()

        '''Close the member details pop up window'''
        self.log('Click on "CLOSE" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH) \
            .click()

        add_subsystem_to_member(self, member_name, subsystem_text)
        self.log('''Click on "OK" button''')
        self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_OK_BTN_XPATH).click()

        '''MEMBER_56/4a The X-Road member already has a subsystem with the inserted code.'''
        self.log('''MEMBER_56/4a The X-Road member already has a subsystem with the inserted code.''')
        '''MEMBER_56/4a1 System displays the error message "Failed to add subsystem: Subsystem 'X' already exists", 
        where "X" is the inserted subsystem code.'''
        self.log('''MEMBER_56/4a1 System displays the error message''')
        error_messages(self, True, "Failed to add subsystem: Subsystem '{0}' already exists.", 'test_subsystem_text')

        '''MEMBER_56/4a.3a CS administrator selects to terminate the use case.'''
        self.log('MEMBER_56/4a.3a CS administrator selects to terminate the use case, by Clicking on "CANCEL" button')
        self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_CANCEL_BTN_XPATH).click()

        '''Delete added subsystem'''
        delete_subsystem(self, subsystem_text)

        self.log('Click on "CLOSE" button')
        self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH).click()

        '''MEMBER 56/3 System parses the user input'''
        '''MEMBER 54/1 System removes leading and trailing whitespaces.'''
        '''MEMBER 54/2 System verifies that the mandatory fields are filled.'''
        '''MEMBER 54/1 System verifies that the user input does not exceed 255 characters.'''
        counter = 2
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
        for subsystem_input in subsystem_inputs:
            current_log_lines = log_checker.get_line_count()
            subsystem = subsystem_input[0]
            error_exists = subsystem_input[1]
            error_message = subsystem_input[2]
            error_message_label = subsystem_input[3]
            whitespaces = subsystem_input[4]

            self.log('TEST - {0}'.format(counter))
            if subsystem == '':
                '''Add a Subsystem to an X-Road Member'''
                add_subsystem_to_member(self, member_name, subsystem)

                self.log("System verifies that if 'Subsystem Code' text field is empty, "
                         "then user can't click on 'OK' button")
                self.wait_jquery()
                ok_button = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_OK_BTN_XPATH)
                ok_button_status = ok_button.is_enabled()
                assert ok_button_status is False
                self.log("'OK' button is disabled")
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_CANCEL_BTN_XPATH).click()
            else:
                '''Add a Subsystem to an X-Road Member'''
                add_subsystem_to_member(self, member_name, subsystem)

                self.log('''Click on "OK" button''')
                self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_OK_BTN_XPATH).click()

                '''Verify error message'''
                error_messages(self, error_exists, error_message, error_message_label)

                if error_exists:
                    '''MEMBER_56/3a.2 & 4a.2 System logs the event "Add subsystem failed" to the audit log.'''
                    self.log('''MEMBER_56/3a.2 & 4a.2 System logs the event "Add subsystem failed" to the audit log.''')
                    logs_found = log_checker.check_log(log_constants.ADD_SUBSYSTEM_FAILED,
                                                       from_line=current_log_lines + 1)
                    self.is_true(logs_found, msg="Add subsystem failed")

                    '''MEMBER_56/3a.3a CS administrator selects to terminate the use case.'''
                    self.log('MEMBER_56/3a.3a CS administrator selects to terminate the use case, '
                             'by clicking on "CANCEL" button')
                    self.wait_until_visible(type=By.XPATH,
                                            element=members_table.SUBSYSTEM_POPUP_CANCEL_BTN_XPATH).click()
                else:
                    '''Verify that the added subsystem exists'''
                    self.log('Find added subsystem (string length = {0})- {1}'.format(len(subsystem.strip()),
                                                                                      subsystem.strip()))
                    found_subsystem = self.wait_until_visible(type=By.XPATH,
                                                              element=members_table.
                                                              get_subsystem_row_by_name(subsystem.strip()))
                    found_subsystem = found_subsystem.text
                    if whitespaces:
                        find_text_with_whitespaces(self, subsystem, found_subsystem)
                    else:
                        assert subsystem in found_subsystem
                        self.log('Found subsystem - ' + found_subsystem)

                    '''MEMBER_56/6 System logs the event "Add subsystem" to the audit log.'''
                    self.log('''MEMBER_56/6 System logs the event "Add subsystem" to the audit log.''')
                    logs_found = log_checker.check_log(log_constants.ADD_SUBSYSTEM,
                                                       from_line=current_log_lines + 1)
                    self.is_true(logs_found, msg="Add subsystem")

                    '''Delete added subsystem'''
                    delete_subsystem(self, subsystem.strip())

            self.log('Click on "CLOSE" button')
            self.wait_jquery()
            self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH) \
                .click()
            counter += 1
#######################################################################################################################
        '''Delete added member'''
        delete_added_member(self, member_name)
    return test_case


def add_cs_member(self, member_name, member_class, member_code):
    """
    Add central server member
    :param self: MainController object
    :param member_name: str - Member name
    :param member_class: str - Member class
    :param member_code: str - Member code
    :return:
    """
    '''MEMBER_10/1 CS administrator selects to add an X-Road member.'''
    self.log('''MEMBER_10/1 CS administrator selects to add an X-Road member.''')
    self.wait_jquery()
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.MEMBERS_CSS).click()

    self.wait_jquery()
    self.log('Click on "ADD" button')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()

    '''MEMBER_10 2 CS administrator inserts the name of the organization'''
    self.log('''MEMBER_10 2 CS administrator inserts the name of the organization (string length = {0}) - {1}'''
             .format(len(member_name), member_name))
    input_name = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID)
    self.input(input_name, member_name)

    '''MEMBER_10 2 CS administrator inserts the X-Road member class of the organization'''
    self.log('''MEMBER_10 2 CS administrator inserts the X-Road member class of the organization (string length = {0}) 
    - {1}'''.format(len(member_class), member_class))
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=members_table.ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    select.select_by_visible_text(member_class)

    '''MEMBER_10 2 CS administrator inserts the X-Road member code of the organization.'''
    self.log('''MEMBER_10 2 CS administrator inserts the X-Road member code of the organization. (string length = {0}) 
    - {1}'''.format(len(member_code), member_code))
    input_code = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member_code)

    self.log('Click "OK" to add member')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()

    '''Close the member details pop up window'''
    self.log('Click on "CLOSE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH) \
        .click()


def delete_added_member(self, member_name):
    """
    Delete the member row from the list.
    :param self: MainController object
    :param member_name: str - member name
    :return: None
    """
    self.wait_jquery()
    self.log('Click member name - ' + member_name + ' - in members table')
    self.wait_until_visible(type=By.XPATH, element=members_table.get_member_data_from_table(1, member_name)).click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.log('Click on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DELETE_CONFIRM_BTN_ID).click()


def add_subsystem_to_member(self, member_name, subsystem_text):
    """
    Add a subsystem to an X-Road Member
    :param self: MainController object
    :param member_name: str - member name
    :param subsystem_text: str - subsystem
    :return: None
    """
    self.wait_jquery()
    '''Open member details'''
    self.log('Click member name - ' + member_name + ' - in members table')
    self.wait_until_visible(type=By.XPATH, element=members_table.get_member_data_from_table(1, member_name)).click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    '''Open subsystem tab'''
    self.log('Click on "Subsystem" tab')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()

    '''MEMBER_56/1 CS administrator selects to add a subsystem to an X-Road member.'''
    self.log('MEMBER_56/1 CS administrator selects to add a subsystem to an X-Road member, '
             'by clicking on "ADD buton"')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_SUBSYSTEM_BTN_ID).click()

    '''MEMBER_56/2 CS administrator inserts the code of the subsystem..'''
    self.log('MEMBER_56/2 CS administrator inserts the code of the subsystem, '
             'by inserting (string length = {0}) - {1} - to the "Subsystem code" text field'
             .format(len(subsystem_text), subsystem_text))
    self.wait_jquery()
    subsystem_text_field = self.wait_until_visible(type=By.ID, element=members_table.SUBSYSTEM_CODE_AREA_ID)
    self.input(subsystem_text_field, subsystem_text)


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


def delete_subsystem(self, subsystem):
    """
    Function deletes added subsystem
    :param self: MainController object
    :param subsystem: str - Added subsystem
    :return: None
    """
    self.wait_jquery()
    self.log('Click on subsystem - {0} - row'.format(subsystem))
    self.wait_until_visible(type=By.XPATH, element=members_table.get_subsystem_row_by_name(subsystem)).click()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.DELETE_SUBSYSTEM_BTN_ID).click()
    self.log('Click on "CONFIRM" button')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.CONFIRM_DELETE_SUBSYSTEM_BTN_XPATH).click()


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
