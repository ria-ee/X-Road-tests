from selenium.webdriver.common.by import By

from view_models.cs_security_servers import SECURITY_SERVER_MANAGEMENT_PROVIDER_NAME_ID, \
    MANAGEMENT_REG_REQUEST_SERVER_NAME_ID, \
    MANAGEMENT_REG_REQUEST_SERVER_CLASS_ID, MANAGEMENT_REG_REQUEST_SERVER_CODE_ID, \
    MANAGEMENT_REG_REQUEST_SUBSYSTEM_CODE_ID, SECURITY_SERVER_MANAGEMENT_PROVIDER_ID, \
    MANAGEMENT_REQUESTS_APPROVED_XPATH, CLIENT_REGISTRATION_REQUEST_POPUP_COMMENT_XPATH
from view_models.log_constants import REGISTER_MANAGEMENT_SERVICE_PROVIDER
from view_models.members_table import SELECT_SECURITY_SERVER_BTN_ID, CLIENT_REGISTRATION_SUBMIT_BTN_ID, \
    USED_SERVERS_SEARCH_BTN_ID, CLIENT_REGISTRATION_CANCEL_BTN_XPATH, MANAGEMENT_REQUEST_DETAILS_BTN_ID
from view_models.messages import NOTICE_MESSAGE_CSS, MANAGEMENT_SERVICE_REGISTERED, MANAGEMENT_SERVICE_ADDED_COMMENT
from view_models.sidebar import SYSTEM_SETTINGS_BTN_CSS, MANAGEMENT_REQUESTS_CSS
from view_models.ss_system_parameters import SECURITY_SERVER_TR_BY_TEXT, REGISTER_MANAGEMENT_SERVICE_BTN_ID


def register_management_service(self, server_name, try_cancel=False, log_checker=None):
    def management_service():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.wait_until_visible(type=By.CSS_SELECTOR, element=SYSTEM_SETTINGS_BTN_CSS).click()
        self.wait_jquery()
        provider_name = self.wait_until_visible(type=By.ID, element=SECURITY_SERVER_MANAGEMENT_PROVIDER_NAME_ID).text
        provider_id = self.wait_until_visible(type=By.ID, element=SECURITY_SERVER_MANAGEMENT_PROVIDER_ID).get_attribute(
            'value').split('/')
        member_class = provider_id[1]
        member_code = provider_id[2]
        subsystem_code = provider_id[3]
        self.log('MEMBER_57 1. Registration button is clicked')
        self.wait_until_visible(type=By.ID, element=REGISTER_MANAGEMENT_SERVICE_BTN_ID).click()
        self.log('MEMBER_57 2. System displays a security server client registration request, '
                 'prefilling the client\'s values with the management service provider\'s information.')
        self.is_equal(provider_name,
                      self.wait_until_visible(type=By.ID, element=MANAGEMENT_REG_REQUEST_SERVER_NAME_ID).text)
        self.is_equal(member_class,
                      self.wait_until_visible(type=By.ID, element=MANAGEMENT_REG_REQUEST_SERVER_CLASS_ID).text)
        self.is_equal(member_code,
                      self.wait_until_visible(type=By.ID, element=MANAGEMENT_REG_REQUEST_SERVER_CODE_ID).text)
        self.is_equal(subsystem_code,
                      self.wait_until_visible(type=By.ID,
                                              element=MANAGEMENT_REG_REQUEST_SUBSYSTEM_CODE_ID).get_attribute('value'))
        if try_cancel:
            self.log('MEMBER_57 3a. Registration process is canceled')
            self.wait_until_visible(type=By.XPATH, element=CLIENT_REGISTRATION_CANCEL_BTN_XPATH).click()
            self.log('Registration button is clicked again')
            self.wait_until_visible(type=By.ID, element=REGISTER_MANAGEMENT_SERVICE_BTN_ID).click()
        self.log('Search for security servers button is pressed')
        self.wait_until_visible(type=By.ID, element=USED_SERVERS_SEARCH_BTN_ID).click()
        self.log('MEMBER_57 3. Security server is selected from the list and the request is submitted')
        self.wait_until_visible(type=By.XPATH, element=SECURITY_SERVER_TR_BY_TEXT.format(server_name)).click()
        self.wait_until_visible(type=By.ID, element=SELECT_SECURITY_SERVER_BTN_ID).click()
        self.wait_until_visible(type=By.ID, element=CLIENT_REGISTRATION_SUBMIT_BTN_ID).click()
        expected_notice_msg = MANAGEMENT_SERVICE_REGISTERED
        self.log('MEMBER_57 5. System displays the message: "{0}"'.format(expected_notice_msg))
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=NOTICE_MESSAGE_CSS).text
        self.is_true(expected_notice_msg, notice_msg)
        if current_log_lines is not None:
            log_msg = REGISTER_MANAGEMENT_SERVICE_PROVIDER
            self.log('MEMBER_57 7. System logs the event {0}'.format(log_msg))
            logs_found = log_checker.check_log(log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
        self.log('Open management requests tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=MANAGEMENT_REQUESTS_CSS).click()
        self.log('Open first approved request details')
        self.wait_until_visible(type=By.XPATH, element=MANAGEMENT_REQUESTS_APPROVED_XPATH).click()
        self.wait_until_visible(type=By.ID, element=MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
        self.log('MEMBER_57 4. System saves the security server client registration request '
                 'and sets the status of the request to approved')
        last_approved_request_comment = self.wait_until_visible(type=By.XPATH,
                                                                element=CLIENT_REGISTRATION_REQUEST_POPUP_COMMENT_XPATH).text
        self.is_equal(MANAGEMENT_SERVICE_ADDED_COMMENT, last_approved_request_comment)

    return management_service
