# coding=utf-8

import re

from selenium.webdriver.common.by import By

from helpers import xroad, auditchecker
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs as parse_input
from view_models import messages, log_constants, clients_table_vm, popups, sidebar
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
    self.double_click(client_row)
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


def test_add_client(case, client_name, client=None, client_id=None, duplicate_client=None, check_errors=False,
                    unregistered_member=None,
                    ssh_host=None, ssh_user=None, ssh_pass=None, client_unregistered = False):
    """
    UC MEMBER_47 main test method. Tries to add a new client to a security server and check logs if
    ssh_host is set.
    :param case: MainController object
    :param client_name: str - existing client name
    :param client: dict|None - existing client and new subsystem data; this or client_id is required
    :param client_id: str|None - existing client and new subsystem data as string; this or client is required
    :param duplicate_client: dict|None - if set, existing client subsystem data (used for checking error messages)
    :param check_errors: bool - True to check for error scenarios, False otherwise
    :param unregistered_member: dict|None - if set, used for checking for correct messages when the member is unregistered
    :param ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :param client_unregistered: bool|None - if True, client will always be confirmed (skip a few tests)
    :return:
    """
    self = case

    def create_registration_request():
        # UC MEMBER_47 1 - select to add a security server client
        self.log('MEMBER_47 1 - select to add a security server client')

        self.logdata = []

        if client is None:
            client_data = xroad.split_xroad_subsystem(client_id)
        else:
            client_data = client

        client_data['name'] = client_name

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_user, password=ssh_pass)
            current_log_lines = log_checker.get_line_count()

        check_values = []

        # Create a list of erroneous and/or testing values to be entered as client
        check_value_errors = [
            [['', client_data['class'], ''], 'Missing parameter: {0}', False],
            [['', client_data['class'], client_data['subsystem']], 'Missing parameter: {0}', False],
            [[client_data['code'], client_data['class'], ''], 'Missing parameter: {2}', False],
            [[256 * 'A', client_data['class'], client_data['subsystem']],
             "Parameter '{0}' input exceeds 255 characters", False],
            [[client_data['code'], client_data['class'], 256 * 'A'], "Parameter '{2}' input exceeds 255 characters",
             False],
            [[256 * 'A', client_data['class'], 256 * 'A'], "Parameter '{0}' input exceeds 255 characters", False],
            [['   {0}   '.format(client_data['code']), client_data['class'],
              '   {0}   '.format(client_data['subsystem'])], None, True, True if client_unregistered else False],
        ]

        check_value_final = [
            [client_data['code'], client_data['class'], client_data['subsystem']], None, False,
             True if client_unregistered else False
        ]

        # UC MEMBER_47 2, 3 - insert the X-Road identifier of the client and parse the user input
        self.log('MEMBER_47 2, 3, 4 - insert the X-Road identifier of the client and parse the user input')

        if check_errors:
            # UC MEMBER_47 3a - check for erroneous inputs / parse user input
            check_values += check_value_errors
            self.log('MEMBER_47 3a - check for erroneous inputs')
        if duplicate_client is not None:
            # UC MEMBER_47 4 - verify that a client does not already exist
            self.log('MEMBER_47 4a - verify that the client does not already exist')
            check_values += [[['{0}'.format(duplicate_client['code']), duplicate_client['class'],
                               '{0}'.format(duplicate_client['subsystem'])], 'Client already exists', False]]

        # Try adding the client with different parameters (delete all added clients)
        add_clients(self, check_values, instance=client_data['instance'], delete=True)

        if unregistered_member is not None:
            unregistered_members = [
                [unregistered_member['code'], unregistered_member['class'], unregistered_member['subsystem']], None,
                False, True]
            add_clients(self, [unregistered_members], instance=client_data['instance'], delete=True)

        # Finish with adding a correct client
        add_clients(self, [check_value_final], instance=client_data['instance'], delete=False)

        if ssh_host is not None:
            # UC MEMBER_47 3a, 4a, 7 -  Check logs for entries
            self.log('MEMBER_47 3a, 4a, 7 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.log_output))

    return create_registration_request


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


def test_register_client(case, client=None, client_id=None, system_exists=True, ssh_host=None, ssh_user=None,
                         ssh_pass=None,
                         test_cancel=False, check_errors=True):
    """
    MEMBER_48 main test function. Tries to register a security server client.
    :param client: dict|None - client data; this or client_id is required
    :param client_id: str|None - client data as string; this or client is required
    :param system_exists: bool - True if the subsystem should exist in the global configuration; False otherwise
    :param ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :param test_cancel: bool - add a step where the administrator does not confirm registration; used only when system_exists=False
    :param check_errors: bool - expect an error when registering
    """
    self = case

    def t_register_client():
        # UC MEMBER_48 1 - select to register security server client
        self.log('MEMBER_48 1 - select to register security server client')

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

        # Click the "register" button
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_REGISTER_BUTTON_ID).click()
        self.wait_jquery()

        self.log('MEMBER_48 2 - system verifies that the selected subsystem exists in the global configuration')
        # If the subsystem does not exist in the global configuration, we need to confirm submitting it.
        if not system_exists:
            self.log('MEMBER_48 2a. The subsystem does not exist in the global configuration'
                     'MEMBER_48 2a.1 System prompts for registration confirmation')
            if test_cancel:
                self.log('MEMBER_48 2a.2a Canceling registration confirmation popup')
                popups.close_all_open_dialogs(self)
                self.wait_jquery()

                self.log('Opening client edit popup')
                client_row = clients_table_vm.get_client_row_element(self, client=client_data)
                edit_client(self, client_row)

                self.log('Click on register button')
                self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_REGISTER_BUTTON_ID).click()
                self.wait_jquery()

            self.log('MEMBER_48 2a - confirm submitting a new subsystem')
            popups.confirm_dialog_click(self)

        # UC MEMBER_48 3 - system creates an X-Road SOAP request
        # UC MEMBER_48 4 - system sends the request to management services
        self.log('MEMBER_48 3, 4 are done in the background and if they fail, step 5 will fail.')
        self.log('MEMBER_48 5 - system receives a response and verifies that it was not an error message')

        # Check for success scenario if not instructed to wait for an error
        if not check_errors:
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
        else:
            # UC MEMBER_48 3-5a creating or sending the request failed, or the response was an error message
            self.log('MEMBER_48 3-5a creating or sending the request failed, or the response was an error message')
            error_message = messages.get_error_message(self)
            self.is_not_none(error_message, msg='MEMBER_48 3-5a - error message was not displayed')
            self.is_true(re.match(messages.CLIENT_REGISTRATION_FAIL_REGEX, error_message),
                         msg='MEMBER_48 3-5a - got invalid error message: {0}'.format(error_message))

        if ssh_host is not None:
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


def add_clients(self, check_values, instance=None, delete=False):
    """
    Tries to add a client with different values. Deletes the added client if instructed to.
    :param self: MainController object
    :param check_values: [list] - list of client parameters, see source code for example
    :param instance: str - instance identifier
    :param delete: bool - delete all successfully added clients after adding them
    :return: (int, int) - number of successful additions, number of unsuccessful additions
    """
    # Open security server clients tab
    self.log('Open security server clients tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.CLIENTS_BTN_CSS).click()

    labels = ['add_member_code', 'add_member_class', 'add_subsystem_code']

    # Loop through clients members and subsystems codes and expected results
    counter = 1
    count_success = 0
    count_fail = 0
    for add_client_data in check_values:
        values = add_client_data[0]
        error_message = add_client_data[1]
        whitespaces = add_client_data[2]
        confirm_client = False
        if len(add_client_data) > 3:
            confirm_client = add_client_data[3]

        member_code = values[0]
        member_class = values[1]
        subsystem_code = values[2]

        self.log(
            'Test inputs {0}, set member="{1}", class="{2}", subsystem="{3}"'.format(counter, member_code, member_class,
                                                                                     subsystem_code))
        # Add client
        add_ss_client(self, member_code, member_class, subsystem_code)

        # Verify code, subsystem
        error = error_message is not None
        if error_message is not None and error_message is not True:
            error_message = error_message.format(*labels)

        # Get the error message if any
        ui_error = messages.get_error_message(self)

        # Expecting error
        if error:
            if ui_error is not None:
                self.is_equal(ui_error, error_message, msg='Wrong error message, expected: {0}'.format(error_message))
            else:
                if error_message == True:
                    self.is_not_none(ui_error, msg='Expected failure but succeeded')
                else:
                    self.is_not_none(ui_error, msg='No error message, expected: {0}'.format(error_message))

            messages.close_error_messages(self)

            count_fail += 1

            self.logdata.append(log_constants.ADD_CLIENT_FAILED)

            self.log('Click on "Cancel" button')
            self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_CANCEL_BTN_XPATH).click()
        else:
            # Not expecting an error
            self.is_none(ui_error, msg='Got error message for: "{0}"'.format(values))

            count_success += 1

            client_confirm_ok = True

            # Confirming a non-existant member
            if confirm_client:
                try:
                    # UC MEMBER_47 5a - member with the inserted identifier does not exist, ask for confirmation before continuing
                    self.log(
                        'MEMBER_47 5a - member with the inserted identifier does not exist, ask for confirmation before continuing')
                    continue_button = self.by_xpath(popups.WARNING_POPUP_CONTINUE_XPATH)
                    continue_button.click()
                    self.wait_jquery()

                    client_confirm_ok = True
                except:
                    client_confirm_ok = False

            self.logdata.append(log_constants.ADD_CLIENT)

            # Cancel the registration request, we're only saving the client, not registering them.
            popups.close_all_open_dialogs(self)
            self.wait_jquery()

            # Create client data dictionary used for later functions.
            added_client_data = {'instance': instance,
                                 'class': member_class.strip(),
                                 'code': member_code.strip(),
                                 'subsystem': subsystem_code.strip()}

            self.log('Find added member {0} : {1} : {2}'.format(member_code, member_class, subsystem_code))
            client_xpath = clients_table_vm.get_client_subsystem_xpath(self, added_client_data)
            client_id = self.wait_until_visible(type=By.XPATH, element=client_xpath)
            client_id_text = client_id.text

            if whitespaces:
                parse_input.find_text_with_whitespaces(self, member_code, client_id_text)
                parse_input.find_text_with_whitespaces(self, subsystem_code, client_id_text)
            else:
                self.is_true(member_code in client_id_text and subsystem_code in client_id_text,
                             msg='Client should have been added but not found.')

            # UC MEMBER_47 6 - Check if client status is "saved"
            self.log('MEMBER_47 6 - Check if client status is "saved"')
            client_row = clients_table_vm.get_client_row_element(self, client=added_client_data)
            status_title = get_client_status(self, client=added_client_data)

            self.is_equal(status_title, clients_table_vm.CLIENT_STATUS_SAVED,
                          'MEMBER_47 6 - Expected client status "{0}", found "{1}"'.format(
                              clients_table_vm.CLIENT_STATUS_SAVED,
                              status_title))

            if delete:
                # Delete the added client
                edit_client(self, client_row)
                delete_client(self)
                self.logdata.append(log_constants.DELETE_CLIENT)

            if confirm_client and not client_confirm_ok:
                self.is_true(False, msg='MEMBER_47 5a Non-existant member confirmation dialog was not displayed')

        counter += 1

    self.wait_jquery()
    return count_success, count_fail
