from selenium.webdriver.common.by import By

from view_models import popups
from view_models.cs_security_servers import SECURITY_SERVER_CLIENT_DETAILS_BTN_ID, SECURITY_SERVER_DELETE_BTN_ID, \
    MANAGEMENT_REQUESTS_CLIENT_DELETION_XPATH, MANAGEMENT_REQUESTS_CERT_DELETION_XPATH, \
    CLIENT_DELETION_REQUEST_COMMENTS_INPUT_XPATH, \
    AUTH_CERT_DELETION_REQUEST_COMMENTS_INPUT_XPATH
from view_models.log_constants import DELETE_SECURITY_SERVER
from view_models.members_table import get_row_by_td_text, MANAGEMENT_REQUEST_DETAILS_BTN_ID
from view_models.popups import CONFIRM_POPUP_CANCEL_BTN_XPATH, confirm_dialog_click
from view_models.sidebar import SECURITY_SERVERS_CSS, MANAGEMENT_REQUESTS_CSS


def delete_member_ss(self, server_name, try_cancel=False, log_checker=None):
    def delete_ss():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.log('Open security servers tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=SECURITY_SERVERS_CSS).click()
        self.wait_jquery()
        self.log('Click on security server {0}'.format(server_name))
        self.wait_until_visible(type=By.XPATH, element=get_row_by_td_text(server_name)).click()
        self.log('Open security server client details')
        self.wait_until_visible(type=By.ID, element=SECURITY_SERVER_CLIENT_DETAILS_BTN_ID).click()
        self.log('MEMBER_25 1. Security server delete button is clicked')
        self.wait_until_visible(type=By.ID, element=SECURITY_SERVER_DELETE_BTN_ID).click()
        self.log('MEMBER_25 2. System prompts for confirmation')
        if try_cancel:
            self.log('MEMBER_25 3a. Cancel button is pressed')
            self.wait_until_visible(type=By.XPATH, element=CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            self.log('Delete button is clicked again')
            self.wait_until_visible(type=By.ID, element=SECURITY_SERVER_DELETE_BTN_ID).click()
        self.log('MEMBER_25 3. Confirmation popup is confirmed')
        confirm_dialog_click(self)
        if current_log_lines is not None:
            expected_log_msg = DELETE_SECURITY_SERVER
            self.log('MEMBER_25 7. System logs the event {0}'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
        self.log('Open center server management requests tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=MANAGEMENT_REQUESTS_CSS).click()
        self.log('MEMBER_25 4a.1 System creates and saves a security server client deletion request')
        self.wait_until_visible(type=By.XPATH, element=MANAGEMENT_REQUESTS_CLIENT_DELETION_XPATH).click()
        self.wait_until_visible(type=By.ID, element=MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
        client_del_req_comment = self.wait_until_visible(type=By.XPATH,
                                                         element=CLIENT_DELETION_REQUEST_COMMENTS_INPUT_XPATH).text
        self.is_true(client_del_req_comment.endswith('deletion'))
        popups.close_all_open_dialogs(self)
        self.log('MEMBER_25 5a.1 System creates and saves a security server cert deletion request')
        self.wait_until_visible(type=By.XPATH, element=MANAGEMENT_REQUESTS_CERT_DELETION_XPATH).click()
        self.wait_until_visible(type=By.ID, element=MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
        cert_del_req_comment = self.wait_until_visible(type=By.XPATH,
                                                       element=AUTH_CERT_DELETION_REQUEST_COMMENTS_INPUT_XPATH).text
        self.log('Check if cert and client deletion comments are same')
        self.is_equal(client_del_req_comment, cert_del_req_comment)

    return delete_ss
