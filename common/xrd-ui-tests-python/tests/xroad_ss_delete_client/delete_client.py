from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import added_client_row
from view_models import popups, sidebar
from view_models.clients_table_vm import DETAILS_TAB_CSS, get_client_row_element
from view_models.keys_and_certificates_table import get_generated_key_row_cert_xpath
from view_models.log_constants import DELETE_CLIENT
from view_models.popups import CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID


def remove_client(self, client, delete_cert=False, cancel_deletion=False, deny_cert_deletion=False, log_checker=None):
    """
    Removes a client.
    :param cancel_deletion: bool - cancel delete confirmation popup before confirming
    :param delete_cert: bool - confirm certificate deletion
    :param self: MainController object
    :param client: dict - client data
    :return: None
    """
    current_log_lines = None
    if log_checker is not None:
        current_log_lines = log_checker.get_line_count()
    # Open security servers tab
    self.log('Open "Security servers tab"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.CLIENTS_BTN_CSS).click()
    self.wait_jquery()

    # Edit client details
    self.log('Opening client details')
    get_client_row_element(self, client).find_element_by_css_selector(DETAILS_TAB_CSS).click()
    self.wait_jquery()

    self.wait_until_visible(type=By.ID, element=CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()

    self.log('MEMBER_53 1. Client deletion process is started')
    self.wait_jquery()
    self.log('MEMBER_53 2. System prompts for confirmation')
    if cancel_deletion:
        self.log('MEMBER_53 3.a Client deletion is canceled')
        self.by_xpath(popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        self.by_id(popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
        self.wait_jquery()
    self.log('MEMBER_53 3. Client deletion is confirmed')
    popups.confirm_dialog_click(self)
    self.wait_jquery()
    # Certificate deletion
    if delete_cert:
        self.wait_jquery()
        self.log('MEMBER_53 4. System verifies that the signature certificates associated with the client '
                 'have no other users and asks for confirmation to delete the client\'s signature certificates')
        self.wait_until_visible(type=By.XPATH, element=popups.YESNO_POPUP_XPATH, timeout=60)
        self.log('MEMBER_53 5. Certificate deletion is confirmed')
        self.by_xpath(popups.YESNO_POPUP_YES_BTN_XPATH).click()
        self.wait_jquery()
        self.log('Open "Keys and Certificates tab"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()
        # Get the other next tr from client key
        expected_next_tr = self.by_xpath(get_generated_key_row_cert_xpath(
            client['code'],
            client['class']))
        """Check if tr has not cert-active class,
        which means that the key has no cert and deletion was successful"""
        self.is_true('cert-active' not in expected_next_tr.get_attribute('class').split(' '))
    elif deny_cert_deletion:
        self.log('MEMBER_53 5a. Deny certificate deletion')
        self.wait_until_visible(type=By.XPATH, element=popups.YESNO_POPUP_XPATH, timeout=60)
        self.by_xpath(popups.YESNO_POPUP_NO_BTN_XPATH).click()
        self.wait_jquery()
        self.log('Open Keys and Certificates tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()
        self.log('Checking if cert is still active')
        expected_next_tr = self.by_xpath(get_generated_key_row_cert_xpath(
            client['code'],
            client['class']))
        self.is_true('cert-active' in expected_next_tr.get_attribute('class').split(' '))
    self.log('CLIENT DELETED')
    try:
        self.log('Open "Security servers tab"')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.CLIENTS_BTN_CSS).click()
        get_client_row_element(self, client)
        raise AssertionError('Client was not deleted')
    except:
        pass
    if current_log_lines is not None:
        logs_found = log_checker.check_log(DELETE_CLIENT, from_line=current_log_lines + 1, strict=False)
        self.is_true(logs_found)
