import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import xroad
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs as parse_input
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import get_expected_warning_messages, \
    added_client_row, disable_management_wsdl, enable_management_wsdl, remove_client
from tests.xroad_ss_client.ss_client_management import get_client_status, edit_client, delete_client
from view_models import clients_table_vm, members_table, popups, log_constants, messages, sidebar
from view_models.log_constants import ADD_CLIENT_FAILED, ADD_CLIENT
from view_models.messages import REGISTRATION_REQUEST_SENDING_FAILED, get_error_message, CLIENT_ALREADY_EXISTS_ERROR
from view_models.popups import CONFIRM_POPUP_CANCEL_BTN_XPATH

test_name = 'CLIENT REGISTRATION IN SECURITY SERVER'


def add_client_to_ss(self, client, retry_interval=0, retry_timeout=0, step='x.x.x-y: '):
    """
    Adds a client to security server.
    :param self: MainController object
    :param client: dict - client data
    :param retry_interval: int - retry interval in seconds (if changes have not yet propagated)
    :param retry_timeout: int - retry timeout in seconds
    :param step: str - prefix to be added to logs
    :return: None
    """
    self.log('MEMBER_47 1. Select to add a new client')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

    # UC MEMBER_47 2. Insert the X-Road identifier
    self.log('MEMBER_47 2. Insert the X-Road identifier')

    self.log(step + 'Click on "SELECT CLIENT FROM GLOBAL LIST" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.SELECT_CLIENT_FROM_GLOBAL_LIST_BTN_ID).click()
    self.wait_jquery()

    # Allow listing of global clients
    c_box = self.wait_until_visible(type=By.ID, element=clients_table_vm.SHOW_ONLY_LOCAL_CLIENTS_CHECKBOX_ID)
    if c_box.is_selected():
        c_box.click()
    start_time = time.time()
    while True:
        # Loop until timeout or success
        try:
            # If retry_interval set, sleep for a while
            if retry_interval > 0:
                self.log(step + 'Waiting {0} before searching'.format(retry_interval))
                time.sleep(retry_interval)

            # Try to find our client from global list
            self.log(step + 'Searching global list for clients')

            self.wait_until_visible(type=By.XPATH, element=clients_table_vm.GLOBAL_CLIENT_LIST_SEARCH_BTN_XPATH).click()
            self.wait_jquery()

            table = self.wait_until_visible(type=By.ID, element=clients_table_vm.GLOBAL_CLIENTS_TABLE_ID)
            self.wait_jquery()

            self.log(step + 'Searching for client row')

            # Try to get the row associated with the client. If not found, we'll get an exception.
            member_row = members_table.get_row_by_columns(table, [client['name'], client['class'], client['code']])

            self.wait_jquery()
            self.click(member_row)
            # If we got here, client was found
            self.log(step + 'Found client row')
            break
        except:
            # Check if timeout
            if time.time() > start_time + retry_timeout:
                # Got a timeout, raise exception
                if retry_timeout > 0:
                    self.log(step + 'Timeout while waiting')
                raise
            # No timeout, continue loop
            self.log(step + 'Client row not found')

    # Click "OK"
    self.wait_jquery()

    self.log(step + 'Confirm popup')
    self.wait_until_visible(type=By.XPATH, element=clients_table_vm.SELECT_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # Enter data to form
    subsystem_input = self.wait_until_visible(type=By.XPATH,
                                              element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_XPATH)
    self.wait_jquery()

    self.input(subsystem_input, client['subsystem_code'], click=False)

    # Try to add client
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # Confirm the popup that should have opened
    warning = self.wait_until_visible(type=By.ID, element=popups.CONFIRM_POPUP_TEXT_AREA_ID).text
    self.wait_jquery()

    # UC MEMBER_47 4, 5, 6. Verify that client does not exist in SS but exists in CS and save the client
    self.log('MEMBER_47 4, 5, 6. Verify that client does not exist in SS but exists in CS and save the client')

    self.log('MEMBER_47 5. An X-Road member with the inserted identifier does not exist')

    self.log('MEMBER_47 5a.1 When adding client with not existing subsystem, a warning is shown')
    self.is_true(warning in get_expected_warning_messages(client), test_name,
                 step + 'WARNING NOT CORRECT: {0}'.format(warning),
                 step + 'EXPECTED WARNING MESSAGE: "{0}" GOT: "{1}"'
                 .format(get_expected_warning_messages(client), warning))

    self.log('MEMBER_47 5a.2 Warning popup is confirmed')
    popups.confirm_dialog_click(self)

    # Check status
    self.log(step + 'ADDING CLIENT TO SECURITY SERVER STATUS TEST')
    status_title = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
    try:
        self.is_equal(status_title, 'registration in progress', test_name,
                      step + 'TITLE NOT CORRECT: {0}'.format(status_title),
                      step + 'EXPECTED STATUS TITLE: {0}'.format('registration in progress'))
    except:
        time.sleep(5)
        pass


def add_client_to_ss_by_hand(self, client, check_send_errors=False, log_checker=None, sec_1_host=None, sec_1_user=None,
                             sec_1_pass=None,
                             management_wsdl_url=None, management_client_id=None, exists_error=False,
                             cancel_registration=False):
    """
    Adds a client to security server without searching for it in lists.
    :param self: MainController object
    :param client: dict - client data
    :return: None
    """
    current_log_lines = None
    if log_checker:
        current_log_lines = log_checker.get_line_count()
    add_ss_client(self, client['code'], client['class'], client['subsystem_code'])
    if exists_error:
        self.log('MEMBER_47 4a Verify that the client does not already exist')
        expected_log_msg = CLIENT_ALREADY_EXISTS_ERROR
        self.log('MEMBER_47 4a.1 System displays the error message "{}"'.format(expected_log_msg))
        error_msg = get_error_message(self)
        self.is_true(expected_log_msg, error_msg)
        if current_log_lines:
            expected_log_msg = ADD_CLIENT_FAILED
            self.log('MEMBER_47 4a.1 System displays the error message "{}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            return
    if check_send_errors:
        new_driver = None
        old_driver = self.driver

        self.log('MEMBER_48 4a. sending of the registration request failed')
        try:
            self.reset_webdriver(sec_1_host, sec_1_user, sec_1_pass, close_previous=False)
            disable_management_wsdl(self, management_client_id, management_wsdl_url)()
            new_driver = self.driver
            self.driver = old_driver
            # Continue warning popup when visible
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
            self.wait_jquery()
            popups.confirm_dialog_click(self)

            self.log('MEMBER_48 4a.1 System displays the error message: '
                     '"Failed to send registration request: X", where X is description of the error')
            # Wait until error message is visible
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS,
                                                timeout=60).text
            # Check if error message is as expected
            self.is_true(re.match(REGISTRATION_REQUEST_SENDING_FAILED, error_msg))

            self.log('MEMBER_48 4a.2 System logs the event "Register client failed" to the audit log')
            # Check if "Register client failed" is in audit log
            logs_found = log_checker.check_log(log_constants.REGISTER_CLIENT_FAILED,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found, msg='"Register client failed" event not found in log"')
        finally:
            self.driver = new_driver
            self.reload_webdriver(sec_1_host, sec_1_user, sec_1_pass)
            enable_management_wsdl(self, management_client_id, management_wsdl_url)()
            self.tearDown()
            self.driver = old_driver
            # Removing added client
            remove_client(self=self, client=client)
            return

    warning = self.wait_until_visible(type=By.ID, element=popups.CONFIRM_POPUP_TEXT_AREA_ID).text
    self.is_true(warning in get_expected_warning_messages(client))

    # UC MEMBER_48 1. Register the client by confirming the registration popup
    self.log('MEMBER_48 1. Register the client by confirming the registration popup')
    if cancel_registration:
        self.wait_until_visible(type=By.XPATH, element=CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_jquery()
        status_title = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
        self.log('Status title: {0}'.format(status_title))
        self.is_equal(clients_table_vm.CLIENT_STATUS_SAVED, status_title.lower())
    else:
        popups.confirm_dialog_click(self)
        self.wait_jquery()

        # UC MEMBER_48 2-5 System verifies existing subsystem, creates and sends SOAP request, receives success response
        self.log(
            'MEMBER_48 2-5 System verifies existing subsystem, creates and sends SOAP request, receives success response')

        # Try to find the client in client list and check the status
        self.log(
            'MEMBER_47 6 / MEMBER_48 6. Verify that the client has been added and check that the status is {0}.'.format(
                'registration in progress'))
        status_title = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
        self.log('Status title: {0}'.format(status_title))
        if status_title.lower() == clients_table_vm.CLIENT_STATUS_SAVED:
            # Something is wrong, status should be "registration in progress". Set the exception to be raised
            # later but go on with the current test.
            self.log('MEMBER_47 6. WARNING: status should be "registration in progress" but is "saved"')
            self.log('MEMBER_47 6. WARNING: CONTINUING TEST WITH STATUS "saved"')
            status_title = 'registration in progress'
            self.exception = True

        self.is_equal(status_title, 'registration in progress', test_name,
                      'MEMBER_48 6. TITLE NOT CORRECT: {0}'.format(status_title),
                      'MEMBER_48 6. EXPECTED MESSAGE: {0}'.format('registration in progress')
                      )
    if current_log_lines:
        self.log('MEMBER_47 7. System logs the event "Add client"')
        logs_found = log_checker.check_log(ADD_CLIENT, from_line=current_log_lines + 1, strict=False)
        self.is_true(logs_found, msg='"Add client" event not found in log')
        # UC MEMBER_48 7. System logs the event "Register client" to the audit log
        if not cancel_registration:
            self.log('MEMBER_48 7. System logs the event "Register client" to the audit log')
            time.sleep(3)
            logs_found = log_checker.check_log(log_constants.REGISTER_CLIENT,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found, msg='"Register client" event not found in log"')


def test_add_client(case, client_name, client=None, client_id=None, duplicate_client=None, check_errors=False,
                    log_checker=None, delete_added=False, check_status=clients_table_vm.CLIENT_STATUS_SAVED):
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
    :param delete_added: bool|None - if True, added clients will be deleted
    :param check_status: str|False - status to check for after registering client, False to skip this check
    :return:
    """
    self = case

    def create_registration_request():
        # UC MEMBER_47 1 - select to add a security server client
        self.log('MEMBER_47 1 - select to add a security server client')
        current_log_lines = None

        self.logdata = []

        if client is None:
            client_data = xroad.split_xroad_subsystem(client_id)
        else:
            client_data = client

        client_data['name'] = client_name

        if log_checker:
            current_log_lines = log_checker.get_line_count()

        check_values = []

        # Create a list of erroneous and/or testing values to be entered as client
        check_value_errors = [
            [['', client_data['class'], ''], 'Missing parameter: {0}', False],
            [['', client_data['class'], client_data['subsystem']], 'Missing parameter: {0}', False],
            # [[client_data['code'], client_data['class'], ''], 'Missing parameter: {2}', False],
            [[256 * 'A', client_data['class'], client_data['subsystem']],
             "Parameter '{0}' input exceeds 255 characters", False],
            [[client_data['code'], client_data['class'], 256 * 'A'], "Parameter '{2}' input exceeds 255 characters",
             False],
            [[256 * 'A', client_data['class'], 256 * 'A'], "Parameter '{0}' input exceeds 255 characters", False],
            [['   {0}   '.format(client_data['code']), client_data['class'],
              '   {0}   '.format(client_data['subsystem'])], CLIENT_ALREADY_EXISTS_ERROR, True]
        ]

        # UC MEMBER_47 2, 3 - insert the X-Road identifier of the client and parse the user input
        self.log('MEMBER_47 2, 3, 4 - insert the X-Road identifier of the client and parse the user input')

        if check_errors:
            # UC MEMBER_47 3a - check for erroneous inputs / parse user input
            check_values += check_value_errors
            self.log('MEMBER_47 3a - check for erroneous inputs')
        else:
            check_values += [
                [[client_data['code'], client_data['class'], client_data['subsystem']], None, False]
            ]
        if duplicate_client:
            # UC MEMBER_47 4 - verify that a client does not already exist
            self.log('MEMBER_47 4a - verify that the client does not already exist')
            check_values += [[['{0}'.format(duplicate_client['code']), duplicate_client['class'],
                               '{0}'.format(duplicate_client['subsystem'])], 'Client already exists', False]]

        # Try adding the client with different parameters (delete all added clients)
        add_clients(self, check_values, instance=client_data['instance'], delete=delete_added,
                    unregister_before_delete=delete_added,
                    check_status=check_status)

        if current_log_lines:
            # UC MEMBER_47 3a, 4a, 7 -  Check logs for entries
            self.log('MEMBER_47 3a, 4a, 7 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.log_output))

    return create_registration_request


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
    self.log('MEMBER_47 1. Click on "ADD CLIENT" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

    # Add a member
    self.log('MEMBER_47 2. Set member code: {0}'.format(member_code))
    input_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member_code)

    # Set member class
    self.log('MEMBER_47 2. Set member class: {0}'.format(member_class))
    self.select(element=popups.ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID, type=By.ID, value=member_class)

    # Add a subsystem code
    self.log('MEMBER_47 2. Set subsystem code: {0}'.format(subsystem_code))
    subsystem_input = self.wait_until_visible(type=By.XPATH,
                                              element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_XPATH)
    self.input(subsystem_input, subsystem_code)

    time.sleep(1.5)
    # Save the client data
    self.log('Click "OK"')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()

    self.wait_jquery()


def add_clients(self, check_values, instance=None, delete=False, unregister_before_delete=False,
                check_status=clients_table_vm.CLIENT_STATUS_SAVED):
    """
    Tries to add a client with different values. Deletes the added client if instructed to.
    :param self: MainController object
    :param check_values: [list] - list of client parameters, see source code for example
    :param instance: str - instance identifier
    :param delete: bool - delete all successfully added clients after adding them
    :param unregister_before_delete: bool - unregister the client before deleting
    :param check_status: str|False - status to check for after registering client, False to skip this check
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
        self.log(check_values.index(add_client_data))
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

            client_row = clients_table_vm.get_client_row_element(self, client=added_client_data)
            if check_status != False:
                # UC MEMBER_47 6 - Check if client status is "saved"
                self.log('MEMBER_47 6 - Check if client status is "{}"'.format(check_status))
                status_title = get_client_status(self, client=added_client_data)

                self.is_equal(status_title, check_status,
                              'MEMBER_47 6 - Expected client status "{0}", found "{1}"'.format(
                                  check_status,
                                  status_title))
            else:
                self.log('Skipping status check (MEMBER_47 6)')

            if delete:
                # Delete the added client
                edit_client(self, client_row)
                delete_client(self, unregister=unregister_before_delete)
                self.logdata.append(log_constants.DELETE_CLIENT)

            if confirm_client and not client_confirm_ok:
                self.is_true(False, msg='MEMBER_47 5a Non-existent member confirmation dialog was not displayed')

        counter += 1

    self.wait_jquery()
    return count_success, count_fail
