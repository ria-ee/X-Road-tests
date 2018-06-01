from selenium.webdriver.common.by import By

from view_models import messages, cs_security_servers, sidebar, members_table, keys_and_certificates_table, popups
from view_models.log_constants import REVOKE_AUTH_REGISTRATION_REQUEST, REVOKE_CLIENT_REGISTRATION_REQUEST


def revoke_requests(self, try_cancel=False, auth=False, log_checker=None):
    """
    Revoke management requests that are in waiting state.
    :param try_cancel:  bool|False - cancels revoke before confirming
    :param auth: bool|False - request type auth
    :param log_checker: obj|None - auditchecker instance
    :param self: MainController object
    :return: None
    """
    current_log_lines = None
    if log_checker is not None:
        current_log_lines = log_checker.get_line_count()
    # Client/cert successful revoke message
    success_message = messages.AUTH_REQUEST_REVOKE_SUCCESSFUL_NOTICE if auth \
        else messages.REQUEST_REVOKE_SUCCESSFUL_NOTICE
    # Client/cert delete request selector
    deletion_request_selector = cs_security_servers.MANAGEMENT_REQUESTS_CERT_DELETION_XPATH if auth \
        else cs_security_servers.MANAGEMENT_REQUESTS_CLIENT_DELETION_XPATH
    # Client/cert details dialog selector
    details_dialog_selector = cs_security_servers.CERT_DELETION_REQUEST_DETAILS_DIALOG_ID if auth \
        else cs_security_servers.CLIENT_DELETION_REQUEST_DETAILS_DIALOG_ID
    # Client/cert details dialog comment selector
    delete_request_comment = cs_security_servers.REVOKE_CERT_DELETE_REQUEST_COMMENT if auth \
        else cs_security_servers.REVOKE_CLIENT_DELETE_REQUEST_COMMENT
    # Client/cert registration request selector
    reg_request_selector = cs_security_servers.REVOKE_CERT_MANAGEMENT_REQUEST_BTN_XPATH if auth \
        else cs_security_servers.REVOKE_CLIENT_MANAGEMENT_REQUEST_BTN_XPATH
    self.log('MEMBER_39 Revoke a Registration Request')
    self.log('Open management requests tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()
    self.wait_jquery()

    self.log('Find request with waiting status')
    td = self.wait_until_visible(type=By.XPATH, element=members_table.get_requests_row_by_td_text(
        keys_and_certificates_table.WAITING_STATE))
    # Waiting request id
    request_id = td.find_elements_by_tag_name('td')[0].text
    self.log('Click on waiting request')
    td.click()
    self.log('Open request details')
    self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
    self.wait_jquery()

    self.log('MEMBER_39 1. Click on revoke button')
    self.wait_until_visible(type=By.XPATH,
                            element=reg_request_selector).click()
    self.wait_jquery()

    self.log('MEMBER_39 2. System prompts for confirmation')
    if try_cancel:
        self.log('MEMBER_39 3a request revoking is canceled')
        self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_jquery()
        self.log('Click on revoke button again')
        self.wait_until_visible(type=By.XPATH,
                                element=reg_request_selector).click()
        self.wait_jquery()

    self.log('MEMBER_39 3. Confirm request revocation')
    popups.confirm_dialog_click(self)
    self.wait_jquery()
    expected_success_msg = success_message.format(request_id)
    self.log('MEMBER_39 6. System displays the message "{0}"'.format(expected_success_msg))
    notice_msg = messages.get_notice_message(self)
    self.is_equal(expected_success_msg, notice_msg)
    self.log('MEMBER_39 5. System sets the state of registration request to revoked')
    first_revoked_request_id = self.by_xpath(members_table.get_requests_row_by_td_text(
        keys_and_certificates_table.REVOKED_STATE)).find_element_by_tag_name('td').text
    self.is_equal(request_id, first_revoked_request_id)
    self.log('MEMBER_39 5. System creates a deletion request with revoked request id')
    self.by_xpath(deletion_request_selector).click()
    self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
    # Request details dialog element
    client_deletion_details_dialog = self.wait_until_visible(type=By.ID, element=details_dialog_selector)
    # Request details comment field text
    comment = client_deletion_details_dialog.find_element_by_class_name(
        cs_security_servers.CLIENT_DELETION_REQUEST_DETAILS_DIALOG_COMMENTS_INPUT_CLASS).text
    self.is_equal(comment, delete_request_comment.format(request_id))
    if current_log_lines is not None:
        if auth:
            expected_log_msg = REVOKE_AUTH_REGISTRATION_REQUEST
        else:
            expected_log_msg = REVOKE_CLIENT_REGISTRATION_REQUEST
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found, msg='MEMBER_39 log check failed')
