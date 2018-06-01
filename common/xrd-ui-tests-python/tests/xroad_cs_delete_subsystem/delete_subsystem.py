from selenium.webdriver.common.by import By

from view_models import popups
from view_models.groups_table import GLOBAL_GROUP_TR_BY_TD_TEXT_XPATH
from view_models.log_constants import DELETE_SUBSYSTEM
from view_models.members_table import get_row_by_columns, MEMBERS_TABLE_ID, MEMBERS_DETATILS_BTN_ID, SUBSYSTEM_TAB, \
    SUBSYSTEM_TR_BY_CODE_XPATH, DELETE_SUBSYSTEM_BTN_ID
from view_models.popups import CONFIRM_POPUP_CANCEL_BTN_XPATH
from view_models.sidebar import GLOBAL_GROUPS_CSS, MEMBERS_CSS


def test_delete_subsystem(self, client, global_group=None, try_cancel=False, log_checker=None):
    def delete_subsystem():
        current_log_lines = None
        group_member_count = None
        if log_checker:
            current_log_lines = log_checker.get_line_count()
        if global_group:
            self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_GROUPS_CSS).click()
            group_member_count = self.wait_until_visible(type=By.XPATH,
                                                         element=GLOBAL_GROUP_TR_BY_TD_TEXT_XPATH.format(
                                                             global_group)).find_elements_by_tag_name('td')[2].text

        self.reload_webdriver(self.url)
        # Open the members table
        self.log('Open members table')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=MEMBERS_CSS).click()
        self.wait_jquery()

        table = self.wait_until_visible(type=By.ID, element=MEMBERS_TABLE_ID)
        self.wait_jquery()

        # Open client details
        self.log('Open client details')
        get_row_by_columns(table, [client['name'], client['class'], client['code']]).click()
        self.wait_until_visible(type=By.ID, element=MEMBERS_DETATILS_BTN_ID).click()
        self.wait_jquery()

        # Open subsystems tab
        self.log('Open subsystems tab')
        self.wait_until_visible(type=By.XPATH, element=SUBSYSTEM_TAB).click()
        self.wait_jquery()

        self.wait_jquery()

        subsys_row = self.wait_until_visible(type=By.XPATH, element=SUBSYSTEM_TR_BY_CODE_XPATH.format(
            client['subsystem_code']))
        self.click(subsys_row)

        # Click "Delete"
        self.log('MEMBER_14 1. Subsystem delete button is clicked')
        self.wait_until_visible(type=By.XPATH, element=DELETE_SUBSYSTEM_BTN_ID).click()
        self.log('MEMBER_14 2. System prompts for confirmation')
        if try_cancel:
            self.log('MEMBER_14 3a. Subsystem deletion is canceled')
            self.wait_until_visible(type=By.XPATH, element=CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            self.wait_until_visible(type=By.XPATH, element=DELETE_SUBSYSTEM_BTN_ID).click()

        self.log('MEMBER_14 3. Subsystem deletion is confirmed')
        popups.confirm_dialog_click(self)
        self.wait_jquery()

        if current_log_lines:
            expected_log_msg = DELETE_SUBSYSTEM
            self.log('MEMBER_14 6. System logs the event {0}'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

        try:
            self.log('MEMBER_14 5. System deletes the subsystem from the system configuration')
            self.by_xpath(SUBSYSTEM_TR_BY_CODE_XPATH.format(client['subsystem_code']))
            raise AssertionError('Subsystem not deleted')
        except:
            pass

        if group_member_count:
            popups.close_all_open_dialogs(self)
            self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_GROUPS_CSS).click()
            self.log('MEMBER_14 4. Subsystem, which was deleted is removed from global group')
            group_member_count_after = self.wait_until_visible(type=By.XPATH,
                                                               element=GLOBAL_GROUP_TR_BY_TD_TEXT_XPATH.format(
                                                                   global_group)).find_elements_by_tag_name('td')[
                2].text
            self.is_true(group_member_count > group_member_count_after)

    return delete_subsystem
