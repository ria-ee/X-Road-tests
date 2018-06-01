# coding=utf-8

from selenium.webdriver.common.by import By

from helpers import xroad, auditchecker
from view_models import log_constants, clients_table_vm, popups
from view_models.clients_table_vm import DETAILS_TAB_CSS
from view_models.log_constants import REGISTER_CLIENT

def add_ss_client(self, member_code, member_class, subsystem_code):
    """
    Try to add security server client
    :param self: MainController object
    :param member_code: str - member code
    :param member_class: str - member class
    :param subsystem_code: str - member subsystem code
    :return: None
    """
    # Add a client
    self.log('Click on "ADD CLIENT" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

    # Add a member
    self.log('Set member code: {0}'.format(member_code))
    input_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member_code)

    # Set member class
    self.log('Set member class: {0}'.format(member_class))
    self.select(element=popups.ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID, type=By.ID, value=member_class)

    # Add a subsystem code
    self.log('Set subsystem code: {0}'.format(subsystem_code))
    subsystem_input = self.wait_until_visible(type=By.XPATH,
                                              element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_XPATH)
    self.input(subsystem_input, subsystem_code)

    # Save the client data
    self.log('Try to save client data')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()

    self.wait_jquery()


def edit_client(self, client_row):
    """
    Opens the edit dialog for a client specified by the table row element.
    :param self: MainController object
    :param client_row: WebElement - client row
    :return: None
    """
    self.log('Open client details')
    client_row.find_element_by_css_selector(DETAILS_TAB_CSS).click()
    self.wait_jquery()


def unregister_client(self, delete=False):
    """
    Unregisters a client that is registered or has the registration request sent.
    :param self: MainController object
    :param delete: bool - delete the client after unregistering
    :return: None
    """
    self.log('Click on "Unregister" button')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
    self.log('Confirm deregistration')
    popups.confirm_dialog_click(self)
    if delete:
        # Delete the client after unregistering
        self.log('Confirm deletion')
        popups.confirm_dialog_click(self)
    else:
        # Close (cancel) the topmost dialog
        self.log('Cancel deletion')
        popups.close_all_open_dialogs(self, limit=1)
        self.wait_jquery()


def delete_client(self, unregister=False):
    """
    Deletes the client.
    :param self: MainController object
    :param unregister: bool - unregister the client before deleting
    :return: None
    """
    if unregister:
        unregister_client(self, delete=False)
    self.log('Click on "Delete" button')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
    self.wait_jquery()
    self.log('Confirm deletion')
    popups.confirm_dialog_click(self)


def test_delete_client(case, client=None, client_id=None, ssh_host=None, ssh_user=None, ssh_pass=None,
                       test_cancel=False, signature_deletion=False):
    """
    UC MEMBER_53 main test function. Tries to delete a security server client and checks logs if ssh_host is set.
    :param client: dict|None - client data; this or client_id is required
    :param client_id: str|None - client data as string; this or client is required
    :param ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :param test_cancel: bool - add a step where the administrator does not confirm deletion at first
    :param signature_deletion: bool - when asked about deleting the signatures, confirm it if True
    """
    self = case

    def delete_client():
        # UC MEMBER_53 1 - select to delete a security server client
        self.log('MEMBER_53 1 - select to delete a security server client')

        self.logdata = []

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_user, password=ssh_pass)
            current_log_lines = log_checker.get_line_count()

        if client is None:
            client_data = xroad.split_xroad_subsystem(client_id)
        else:
            client_data = client

        # Find the client and click on it
        client_row = clients_table_vm.get_client_row_element(self, client=client_data)
        edit_client(self, client_row)

        # Click the delete button
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
        self.wait_jquery()

        # UC MEMBER_53 2 - system prompts for confirmation
        self.log('MEMBER_53 2 - system prompts for confirmation')

        if test_cancel:
            # UC MEMBER_53 3a - user cancels the deletion, nothing should be deleted
            self.log('MEMBER_53 3a - not confirming')
            popups.close_all_open_dialogs(self)
            self.wait_jquery()

            # Start editing the client again; if the client was erroneously deleted, we will get an exception here
            client_row = clients_table_vm.get_client_row_element(self, client=client_data)
            edit_client(self, client_row)

            # Click the delete button again
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
            self.wait_jquery()

        # UC MEMBER_53 3 - confirm deletion
        self.log('MEMBER_53 3 - confirm the deletion')
        popups.confirm_dialog_click(self)

        # Check if we have been asked to verify another confirmation.
        if signature_deletion is not None:
            # UC MEMBER_53 4 - system verifies that the signature certificates are not used any more and asks for confirmation
            self.log(
                'MEMBER_53 4 - system verifies that the signature certificates are not used any more and asks for confirmation')
            self.is_true(popups.confirm_dialog_visible(self),
                         msg='Signature certificate deletion confirmation popup not shown')

            if signature_deletion:
                # UC MEMBER_53 5 - confirm
                self.log('MEMBER_53 5 - confirm removing associated signature certificates')
                popups.confirm_dialog_click(self)
            else:
                # UC MEMBER_53 5a - do not confirm
                self.log('MEMBER_53 5a - do not confirm deletion of associated signature certificates')

        # Wait for data
        self.wait_jquery()

        # UC MEMBER_53 7 - check if the client has been removed from the list
        self.log('MEMBER_53 7 - check if the client has been removed from the list')
        try:
            clients_table_vm.get_client_row_element(self, client=client_data)
            # If we got here, the client is still there
            self.is_true(False, msg='MEMBER_53 7 - the client is still in the list')
        except RuntimeError:
            # We were expecting an exception, so everything is fine.
            pass

        # Add expected log entry
        self.logdata.append(log_constants.DELETE_CLIENT)

        if ssh_host is not None:
            # UC MEMBER_53 8 -  Check logs for entries
            self.log('MEMBER_53 8 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.log_output))

    return delete_client


def test_register_client(case, client=None, client_id=None, log_checker=None):
    """
    MEMBER_48 main test function. Tries to register a security server client.
    :param client: dict|None - client data; this or client_id is required
    :param client_id: str|None - client data as string; this or client is required
    :param log_checker: obj|None - auditchecker instance if checking logs
    """
    self = case

    def t_register_client():
        # UC MEMBER_48 1 - select to register security server client
        self.log('MEMBER_48 1 - select to register security server client')
        current_log_lines = None
        if log_checker:
            current_log_lines = log_checker.get_line_count()

        self.logdata = []

        if client is None:
            client_data = xroad.split_xroad_subsystem(client_id)
        else:
            client_data = client

        # Find the client and click on it
        client_row = clients_table_vm.get_client_row_element(self, client=client_data)
        edit_client(self, client_row)

        # Click the "register" button
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_REGISTER_BUTTON_ID).click()
        self.wait_jquery()

        self.log('MEMBER_48 2 - system verifies that the selected subsystem exists in the global configuration')
        # If the subsystem does not exist in the global configuration, we need to confirm submitting it.
        self.log('MEMBER_48 2a. The subsystem does not exist in the global configuration'
                 'MEMBER_48 2a.1 System prompts for registration confirmation')

        self.log('MEMBER_48 2a - confirm submitting a new subsystem')
        popups.confirm_dialog_click(self)

        # UC MEMBER_48 3 - system creates an X-Road SOAP request
        # UC MEMBER_48 4 - system sends the request to management services
        self.log('MEMBER_48 3, 4 are done in the background and if they fail, step 5 will fail.')
        self.log('MEMBER_48 5 - system receives a response and verifies that it was not an error message')

        # Check for success scenario if not instructed to wait for an error
        # UC MEMBER_48 6 - Check if client status is "registration in progress"
        self.log('MEMBER_48 6 - Check if client status is "registration in progress"')
        # client_row = clients_table_vm.get_client_row_element(self, client=client_data)
        status_title = get_client_status(self, client=client_data)
        self.is_equal(status_title, clients_table_vm.CLIENT_STATUS_REGISTRATION,
                      msg='MEMBER_48 6 - Expected client status "{0}", found "{1}"'.format(
                          clients_table_vm.CLIENT_STATUS_REGISTRATION, status_title))

        expected_log_msg = REGISTER_CLIENT
        self.log('MEMBER_48 7. System logs the event "{0}"'.format(expected_log_msg))
        self.logdata.append(expected_log_msg)

        if current_log_lines:
            # UC MEMBER_48 7 -  Check logs for entries
            self.log('MEMBER_48 7 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.log_output))

    return t_register_client


def get_client_status(self, client):
    """
    Returns the client registration status (example: "saved")
    :param self: MainController object
    :param client: dict - client data
    :return: str|None - client status, None if client not found
    """
    try:
        client_row = clients_table_vm.get_client_row_element(self, client=client)
        status_title = self.by_css('.status', parent=client_row).get_attribute('title')
        return status_title
    except RuntimeError:
        return None
