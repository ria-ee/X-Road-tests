from selenium.webdriver.common.by import By

from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import added_client_row
from view_models import popups, clients_table_vm
from view_models.clients_table_vm import DETAILS_TAB_CSS, get_client_row_element
from view_models.log_constants import UNREGISTER_CLIENT, UNREGISTER_CLIENT_FAILED
from view_models.messages import UNREGISTER_CLIENT_SEND_REQUEST_FAIL, ERROR_MESSAGE_CSS
from view_models.popups import CONFIRM_POPUP_CANCEL_BTN_XPATH, confirm_dialog_click
from view_models.sidebar import CLIENTS_BTN_CSS


def test_unregister_client(self, client, try_cancel=False, log_checker=None):
    def unregister_client():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.log('Open "Security servers tab"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=CLIENTS_BTN_CSS).click()
        self.wait_jquery()
        deletion_in_progress_state_rows = self.js('return $(".fail").length')

        self.log('Opening client details')
        get_client_row_element(self, client).find_element_by_css_selector(DETAILS_TAB_CSS).click()
        self.wait_jquery()

        self.log('MEMBER_52 1. Unregister Client')
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
        self.wait_jquery()
        self.log('MEMBER_52 2. System prompts for confirmation')
        if try_cancel:
            self.log('MEMBER_52 3a. Confirmation dialog is canceled')
            self.wait_until_visible(type=By.XPATH, element=CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            self.log('MEMBER_52 1. Unregister Client button is pressed again')
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
            self.wait_jquery()
        self.log('MEMBER_52 3. Confirmation dialog is confirmed')
        popups.confirm_dialog_click(self)
        deletion_in_progress_state_rows_after_unregister = self.js('return $(".fail").length')
        self.log('MEMBER_52 7. System sets the state of the client to deletion in progress')
        self.is_true(deletion_in_progress_state_rows_after_unregister > deletion_in_progress_state_rows)
        if current_log_lines:
            expected_log_msg = UNREGISTER_CLIENT
            self.log('MEMBER_52 8. System logs the event "{}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

    return unregister_client


def unregister_client_fail(self, client, client_path=None, log_checker=None, request_fail=False):
    def unreg_client():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.log('Open client details')
        self.wait_jquery()

        row_element = added_client_row(self, client).find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS)
        self.wait_until_visible(element=row_element)
        self.click(row_element)
        self.wait_jquery()

        self.log('MEMBER_52 1. Click unregister button')
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
        self.wait_jquery()
        self.log('MEMBER_52 3. Confirm unregister confirmation popup')
        confirm_dialog_click(self)
        if request_fail:
            service_path = '{}/clientDeletion'.format(client_path)
            expected_error_msg = UNREGISTER_CLIENT_SEND_REQUEST_FAIL.format(service_path)
            self.log('MEMBER_52 5a.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
        if current_log_lines is not None:
            expected_log_msg = UNREGISTER_CLIENT_FAILED
            self.log('MEMBER_52 5a.2 System logs the event {} to the audit log'.format(expected_log_msg))
            logs_found = log_checker.check_log(UNREGISTER_CLIENT_FAILED, from_line=current_log_lines + 1)
            self.is_true(logs_found)

    return unreg_client
