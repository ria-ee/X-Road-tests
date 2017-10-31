from selenium.webdriver.common.by import By

from view_models.keys_and_certificates_table import SUBMITTED_FOR_APPROVAL_STATE, DECLINED_STATE
from view_models.log_constants import DECLINE_REGISTRATION_REQUEST
from view_models.members_table import get_requests_row_by_td_text, MANAGEMENT_REQUEST_DETAILS_BTN_ID, \
    DECLINE_REQUEST_BTN_XPATH
from view_models.messages import NOTICE_MESSAGE_CSS, DECLINED_REQUEST_NOTICE
from view_models.popups import confirm_dialog_click, CONFIRM_POPUP_CANCEL_BTN_XPATH
from view_models.sidebar import MANAGEMENT_REQUESTS_CSS


def decline_request(self, try_cancel=False, log_checker=None):
    def decline():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.wait_until_visible(type=By.CSS_SELECTOR, element=MANAGEMENT_REQUESTS_CSS).click()
        self.wait_jquery()
        td = self.by_xpath(get_requests_row_by_td_text(SUBMITTED_FOR_APPROVAL_STATE))
        request_id = td.find_elements_by_tag_name('td')[0].text
        td.click()
        self.wait_until_visible(type=By.ID, element=MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
        self.log('MEMBER_38 1. Registration request decline button is pressed')
        self.wait_until_visible(type=By.XPATH, element=DECLINE_REQUEST_BTN_XPATH).click()
        self.log('MEMBER_38 2. System prompts for confirmation')
        if try_cancel:
            self.log('MEMBER_38 3a. Registration request decline is canceled')
            self.wait_until_visible(type=By.XPATH, element=CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            self.log('Press decline button again')
            self.wait_until_visible(type=By.XPATH, element=DECLINE_REQUEST_BTN_XPATH).click()
        self.log('MEMBER_38 3. Registration request decline is confirmed')
        confirm_dialog_click(self)
        self.log('MEMBER_38 4. System sets the state of the request to declined')
        first_declined_request_id = self.by_xpath(get_requests_row_by_td_text(
            DECLINED_STATE)).find_element_by_tag_name('td').text
        self.is_equal(request_id, first_declined_request_id)
        expected_msg = DECLINED_REQUEST_NOTICE.format(request_id)
        self.log('MEMBER_38 5. System displays the message {0}'.format(expected_msg))
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=NOTICE_MESSAGE_CSS).text
        self.is_equal(expected_msg, notice_msg)

        if current_log_lines is not None:
            expected_log_msg = DECLINE_REGISTRATION_REQUEST
            self.log('MEMBER_38 6. System logs the event {0}'.format(expected_log_msg))
            check_log = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(check_log)

    return decline
