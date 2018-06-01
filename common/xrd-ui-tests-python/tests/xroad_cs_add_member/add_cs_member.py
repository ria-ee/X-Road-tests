from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from tests.xroad_changing_database_rows_with_cs_gui_291.changing_database_rows_with_cs_gui import added_member_row
from view_models import members_table, popups
from view_models.log_constants import ADD_MEMBER, ADD_MEMBER_FAILED
from view_models.messages import MEMBER_ALREADY_EXISTS_ERROR, ERROR_MESSAGE_CSS


def add_member_to_cs(self, member, log_checker=None, exists=False):
    """
    Adds a member to Central Server.
    :param self: MainController object
    :param member: dict - member data
    :return: None
    """
    current_log_lines = None
    if log_checker is not None:
        current_log_lines = log_checker.get_line_count()
    self.log('MEMBER_10. Add member to Central Server')
    # UC MEMBER_10 1. Select to add an X-Road member
    self.log('MEMBER_10 1. Select to add an X-Road member')

    self.log('Wait for the "ADD" button and click')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()
    self.log('Wait for the popup to be visible')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_XPATH)

    # UC MEMBER_10 2. Fill in the data.
    self.log('MEMBER_10 2. Enter ' + member['name'] + ' to "member name" area')
    input_name = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID)
    self.input(input_name, member['name'])
    self.log('MEMBER_10 2. Select ' + member['class'] + ' from "class" dropdown')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=members_table.ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    select.select_by_visible_text(member['class'])
    self.log('MEMBER_10 2. Enter ' + member['code'] + ' to "member code" area')
    input_code = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member['code'])
    self.log('Click "OK" to add member')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    if exists:
        expected_error_msg = MEMBER_ALREADY_EXISTS_ERROR.format(member['class'], member['code'])
        self.log('MEMBER_10 4a.1 System displays the error message "{0}"'.format(expected_error_msg))
        error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
        self.is_equal(expected_error_msg, error_msg)

        if current_log_lines:
            expected_log_msg = ADD_MEMBER_FAILED
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.log('MEMBER_10 4a.3 CS System logs the event "{0}"'.format(expected_log_msg))
            self.is_true(logs_found)
    else:
        popups.close_all_open_dialogs(self)

        # UC MEMBER_10 4-5. System verifies unique member and saves the data
        self.log('MEMBER_10 4-5. System verifies unique member and saves the data')
        self.members_current_name = member['name']
        member_row = added_member_row(self, member)
        self.is_not_none(member_row, msg='Member not found in members table')

        expected_log_msg = ADD_MEMBER
        if current_log_lines:
            try:
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found,
                         msg='{0} not found in audit log'.format(expected_log_msg),
                         log_message='MEMBER_10 7. System logs the event "{0}"'.format(expected_log_msg))
            except:
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found,
                             msg='{0} not found in audit log'.format(expected_log_msg),
                             log_message='MEMBER_10 7. System logs the event "{0}"'.format(expected_log_msg))
