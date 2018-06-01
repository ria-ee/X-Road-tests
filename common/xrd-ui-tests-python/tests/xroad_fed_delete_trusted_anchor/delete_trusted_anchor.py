from selenium.webdriver.common.by import By

from view_models.global_configuration import TRUSTED_ANCHORS_TAB_CSS
from view_models.log_constants import DELETE_TRUSTED_ANCHOR
from view_models.messages import NOTICE_MESSAGE_CSS, DELETE_ANCHOR_SUCCESS_MSG
from view_models.popups import CONFIRM_POPUP_CANCEL_BTN_XPATH, CONFIRM_POPUP_OK_BTN_XPATH
from view_models.sidebar import GLOBAL_CONFIGURATION_CSS
from view_models.trusted_anchor import DELETE_BTN_XPATH, TRUSTED_ANCHOR_BY_IDENTIFIER_XPATH, INSTANCE_IDENTIFIER


def test_delete_trusted_anchor(self, cancel=False, log_checker=None):
    def delete_trusted_anchor():
        current_log_lines = None
        if log_checker:
            current_log_lines = log_checker.get_line_count()
        self.log('Open global configuration view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_CONFIGURATION_CSS).click()
        self.log('Open "Trusted anchors" tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=TRUSTED_ANCHORS_TAB_CSS).click()
        self.wait_jquery()
        self.log('FED_07 1. "Delete a trusted anchor" button is clicked')
        filter(lambda x: x.size['height'] > 0, self.by_xpath(DELETE_BTN_XPATH, multiple=True))[0].click()
        self.log('FED_07 2. System prompts for confirmation')
        if cancel:
            self.log('FED_07 3a Canceling trusted anchor deletion')
            self.wait_until_visible(type=By.XPATH, element=CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            self.log('Checking if anchor is still present')
            self.wait_until_visible(type=By.XPATH,
                                    element=TRUSTED_ANCHOR_BY_IDENTIFIER_XPATH.format(INSTANCE_IDENTIFIER))
            return
        self.log('FED_07 3. Confirming anchor deletion')
        self.wait_until_visible(type=By.XPATH, element=CONFIRM_POPUP_OK_BTN_XPATH).click()
        expected_msg = DELETE_ANCHOR_SUCCESS_MSG.format(INSTANCE_IDENTIFIER)
        self.log('FED_07 4. System deletes the selected configuration anchor and displays the messsage: "{}"'.format(
            expected_msg))
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=NOTICE_MESSAGE_CSS).text
        self.is_equal(expected_msg, notice_msg)
        if current_log_lines:
            expected_log_msg = DELETE_TRUSTED_ANCHOR
            self.log('FED_07 5. System logs the event "{}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
        try:
            self.by_xpath(TRUSTED_ANCHOR_BY_IDENTIFIER_XPATH.format(INSTANCE_IDENTIFIER))
            raise AssertionError('Anchor was not deleted')
        except:
            pass

    return delete_trusted_anchor
