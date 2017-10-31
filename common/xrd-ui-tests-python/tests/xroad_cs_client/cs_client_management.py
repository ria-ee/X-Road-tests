# coding=utf-8

from view_models import messages, sidebar, log_constants, cs_security_servers
from selenium.webdriver.common.by import By
from helpers import xroad, auditchecker


def open_servers_clients(self, code):
    '''
    Open security servers and their clients in UI.
    :param self: MainController object
    :param code: str - server name
    :return: None
    '''
    self.log('Open Security servers')
    self.reset_page()
    self.wait_jquery()
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
    self.wait_jquery()

    # Get the table
    table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
    self.wait_jquery()

    # Find the client and click on it
    self.log('Click on client row')
    rows = table.find_elements_by_tag_name('tr')
    for row in rows:
        if row.text is not u'':
            if row.find_element_by_tag_name('td').text == code:
                row.click()

    # Open details
    self.log('Click on Details button')
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENT_DETAILS_BTN_ID).click()
    self.wait_jquery()

    # Open clients tab
    self.log('Click on clients tab')
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_CLIENT_TAB).click()
    self.wait_jquery()


def search_and_select_client(self, client):
    '''
    Opens the client search dialog and selects a specified client from the displayed list.
    :param self: MainController object
    :param client: dict - client data
    :return: None
    '''
    # Search for the client
    self.log('Click on search client')
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SEARCH_BTN_ID).click()
    self.wait_jquery()

    # Get the table and look for the client
    table = self.wait_until_visible(type=By.XPATH, element=cs_security_servers.MEMBERS_SEARCH_TABLE_XPATH)
    rows = table.find_elements_by_tag_name('tr')
    self.log('Finding client from table')
    for row in rows:
        tds = row.find_elements_by_tag_name('td')
        if tds[0].text is not u'':
            if (tds[0].text == client['name']) & (tds[1].text == client['code']) & (tds[2].text == client['class']) & (
                        tds[3].text == u''):
                row.click()
                break

    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SELECT_MEMBER_BTN_XPATH).click()
    self.wait_jquery()


def fill_server_data(self, server_code, server_owner=None):
    '''
    Checks if server data was prefilled in the request dialog and fills in the data that was not.
    :param self: MainController object
    :param server_code: str - server code
    :param server_owner: dict|None - server owner data; filled only if specified
    :return: None
    '''

    server_owner_code = self.by_id(cs_security_servers.SECURITYSERVER_CLIENT_SERVER_OWNER_CODE_ID)
    server_owner_class = self.by_id(cs_security_servers.SECURITYSERVER_CLIENT_SERVER_OWNER_CLASS_ID)
    server_owner_name = self.by_id(cs_security_servers.SECURITYSERVER_CLIENT_SERVER_OWNER_NAME_ID)
    server_code_element = self.by_id(cs_security_servers.SECURITYSERVER_CLIENT_SERVER_CODE_ID)
    if server_owner is not None:
        if server_owner_code.tag_name == 'input':
            self.input(server_owner_code, server_owner['code'])
        if server_owner_class.tag_name == 'input':
            self.input(server_owner_class, server_owner['class'])
        if server_owner_name.tag_name == 'input':
            self.input(server_owner_name, server_owner['subsystem'])
    if server_code_element.tag_name == 'input':
        self.input(server_owner_name, server_code)


def start_adding_client(self, client):
    '''
    Opens the "Add client" dialog, searches for and selects the specified client.
    :param self: MainController object
    :param client: dict - client data
    :return: None
    '''
    # Start adding new client
    self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_CLIENT_TO_SECURITYSERVER_BTN_ID).click()
    self.wait_jquery()

    # Click "Search" and select the client
    search_and_select_client(self, client)


def add_subsystem_to_client(self, server_code, client, server=None, check_errors=True, duplicate_client=None):
    """
    Adds a subsystem to server client.
    :param self: MainController object
    :param server_code: str - server code
    :param client: dict - client data
    :param server: dict - server owner data
    :param check_errors: bool - test error scenarios; False speeds the test up
    :return: None
    """
    log_success = log_constants.REGISTER_MEMBER_AS_SEC_SERVER_CLIENT
    log_fail = log_constants.REGISTER_MEMBER_AS_SEC_SERVER_CLIENT_FAILED

    # Open clients list for server
    open_servers_clients(self, server_code)

    # Add new subsystem as client
    self.log('Add new client')
    start_adding_client(self, client)

    # UC MEMBER_15 2 display the registration request and check if the known values are prefilled
    self.log('MEMBER_15 2 - display the registration request and check if the known values are prefilled')

    # Wait until the first element has been displayed, as this means that the request itself is shown.
    client_name_text = self.wait_until_visible(cs_security_servers.SECURITYSERVER_CLIENT_NAME_ID, type=By.ID).text
    client_class_text = self.by_id(cs_security_servers.SECURITYSERVER_CLIENT_CLASS_ID).text
    client_code_text = self.by_id(cs_security_servers.SECURITYSERVER_CLIENT_CODE_ID).text

    self.is_equal(client_name_text, client['name'],
                  msg='Wrong client name displayed. Expected "{0}", found "{1}"'.format(client['name'],
                                                                                        client_name_text))
    self.is_equal(client_class_text, client['class'],
                  msg='Wrong client class displayed. Expected "{0}", found "{1}"'.format(client['class'],
                                                                                         client_class_text))
    self.is_equal(client_code_text, client['code'],
                  msg='Wrong client code displayed. Expected "{0}", found "{1}"'.format(client['code'],
                                                                                        client_code_text))

    # MEMBER_15 3 - enter remaining data
    self.log('MEMBER_15 3 - enter "{0}" to subsystem code area'.format(client['subsystem']))

    # Fill other server-related data that has not already been prefilled
    fill_server_data(self, server_code, server)

    # Get the subsystem input field
    subsystem_input = self.wait_until_visible(type=By.ID, element=cs_security_servers.SUBSYSTEM_CODE_AREA_ID)

    if check_errors:
        # UC MEMBER_15 4 (parse user input), 4a (user input parsing failed), 4 (correct data)
        self.log(
            'MEMBER_15 4a (user input parsing failed), 4 (correct data), 5')

        # Use UC SS_41 to check input parsing, finish with space-padded data
        successes, errors, final_name = check_inputs(self,
                                                     input_element=cs_security_servers.SUBSYSTEM_CODE_AREA_ID,
                                                     final_value=client['subsystem'], label_name='subsystemCode',
                                                     save_btn=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID,
                                                     input_element_type=By.ID, save_btn_type=By.ID)

        # Save logged error messages and successes for later checking
        self.logdata += [log_fail] * errors
        self.logdata += [log_success] * successes
    else:
        # UC MEMBER_15 4, 5 - parse and add correct data
        self.log('MEMBER_15 4, 5 - add correct data')

        # Clear the input and set value
        self.input(subsystem_input, client['subsystem'])
        self.wait_jquery()

        # Submit the form
        self.wait_until_visible(type=By.ID,
                                element=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID).click()
        self.wait_jquery()

        # Add success to expected log entries
        self.logdata.append(log_success)

    client_path = xroad.get_xroad_path(client)
    server_path = xroad.get_xroad_path(server)

    # UC MEMBER_15 8, 9 check if the correct success message was displayed
    self.log('MEMBER_15 8, 9 - check for correct success message')

    expected_message = messages.CLIENT_REGISTRATION_SUCCESS.format(client_path, server_path)
    success_message = messages.get_notice_message(self)
    self.log('Found success message: {0}, expected'.format(success_message, expected_message))
    self.is_equal(success_message, expected_message,
                  msg='Wrong message displayed, expected: {0}'.format(expected_message))

    # Check if we get an error when trying to add a client that already exists
    if duplicate_client is not None:
        # MEMBER_15 5a - check if an error message is displayed when trying to create a request with the same data
        self.log(
            'MEMBER_15 5a - check if an error message is displayed when trying to create a request for an existing client')

        duplicate_client_path = xroad.get_xroad_path(duplicate_client)

        # Open the add dialog and select the same client
        start_adding_client(self, duplicate_client)

        # Clear the input and set value
        self.input(subsystem_input, duplicate_client['subsystem'])
        self.wait_jquery()

        # Submit the form
        self.wait_until_visible(type=By.ID,
                                element=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID).click()
        self.wait_jquery()

        # Get the displayed error message
        error_message = messages.get_error_message(self)
        expected_message = messages.CLIENT_REGISTRATION_ALREADY_REGISTERED.format(duplicate_client_path, server_path)
        self.log(
            'Found error: {0}, expected {1}'.format(error_message, expected_message))
        self.is_equal(error_message, expected_message,
                      msg='Wrong error displayed, expected: {0}'.format(expected_message))

        # Add failure to expected log entries
        self.logdata.append(log_fail)

        # Close the error message
        messages.close_error_messages(self)

        # Close the popup itself
        request_popup = self.by_xpath(cs_security_servers.NEW_CLIENT_REGISTRATION_REQUEST_POPUP_XPATH)
        self.by_css(cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_CANCEL_BTN_CSS, parent=request_popup).click()
        self.wait_jquery()

    if check_errors:
        # MEMBER_15 6a - check if an error message is displayed when trying to create a request with the added data
        self.log(
            'MEMBER_15 6a - check if an error message is displayed when trying to create a request with the added data')

        # Open the add dialog and select the same client
        start_adding_client(self, client)

        # Clear the input and set value
        self.input(subsystem_input, client['subsystem'])
        self.wait_jquery()

        # Submit the form
        self.wait_until_visible(type=By.ID,
                                element=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID).click()
        self.wait_jquery()

        # Get the displayed error message
        error_message = messages.get_error_message(self)
        expected_message = messages.CLIENT_REGISTRATION_ALREADY_REQUESTED.format(client_path, server_path)
        self.log('Found error: {0}, expected {1}'.format(error_message, messages.CLIENT_REGISTRATION_ALREADY_REQUESTED))
        self.is_true(error_message.startswith(expected_message),
                     msg='Wrong error displayed, expected: {0}'.format(expected_message))

        # Add failure to expected log entries
        self.logdata.append(log_fail)

        messages.close_error_messages(self)

        # Close the popup itself
        request_popup = self.by_xpath(cs_security_servers.NEW_CLIENT_REGISTRATION_REQUEST_POPUP_XPATH)
        self.by_css(cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_CANCEL_BTN_CSS, parent=request_popup).click()
        self.wait_jquery()


def test_create_registration_request(case, server, client_name, client=None, client_id=None, duplicate_client=None,
                                     ssh_host=None,
                                     ssh_user=None, ssh_pass=None):
    '''
    UC MEMBER_15 main test method. Tries to create a registration request for a subsystem and check logs if
    cs_ssh_host is set.
    :param case: MainController object
    :param server: dict - X-Road security server data
    :param client_name: str - existing client name
    :param client: dict|None - existing client and new subsystem data; this or client_id is required
    :param client_id: str|None - existing client and new subsystem data as string; this or client is required
    :param duplicate_client: dict|None - if set, existing client subsystem data (used for checking error messages)
    :param ssh_host: str|None - if set, Central Server SSH host for checking the audit.log; if None, no log check
    :param ssh_user: str|None - CS SSH username, needed if cs_ssh_host is set
    :param ssh_pass: str|None - CS SSH password, needed if cs_ssh_host is set
    :return:
    '''
    self = case

    def create_registration_request():
        self.logdata = []

        if client is None:
            client_data = xroad.split_xroad_subsystem(client_id)
        else:
            client_data = client

        client_data['name'] = client_name

        server_code = server['subsystem']

        if ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ssh_host, username=ssh_user, password=ssh_pass)
            current_log_lines = log_checker.get_line_count()

        # UC MEMBER_15 1 - select to create a security server registration request for a subsystem
        self.log('UC MEMBER_15 1 - select to create a security server registration request for a subsystem')
        add_subsystem_to_client(self, server_code, client_data, duplicate_client=duplicate_client, server=server)

        if ssh_host is not None:
            # UC MEMBER_15 4a, 5a, 6a, 10 Check logs for entries
            self.log('MEMBER_15 4a, 5a, 6a, 10 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.log_output))

    return create_registration_request


def check_inputs(self, input_element, final_value, save_btn, label_name='cert_profile_info', input_element_type=By.ID,
                 save_btn_type=By.XPATH):
    '''
    Tries to enter different erroneous values to an input field and check if the error messages were correct.
    :param self: MainController object
    :param input_element: str - input element ID, XPath, or CSS selector
    :param final_value: str - correct value to be entered as a final step
    :param save_btn: str - save/OK button ID, XPath, or CSS selector
    :param label_name: str - input label internal name, used in some error messages
    :param input_element_type: By - input element selector type, default is By.ID
    :param save_btn_type: By - input element selector type, default is By.XPATH
    :return: (int, int, str) - number of successful save attempts, number of unsuccessful save attempts, final saved value;
                                numbers are used for counting the success/failure log entries.
    '''
    error_count = 0
    success_count = 0
    URL_TEXT_AND_RESULTS = [
        [256 * 'S', messages.INPUT_DATA_TOO_LONG.format(label_name), False],
        ['   {0}   ', None, True]
    ]

    self.log('MEMBER_54 System verifies entered text')

    # Loop through different key label names and expected results
    counter = 1
    for data in URL_TEXT_AND_RESULTS:
        input_text = data[0].format(final_value, label_name)
        error_message = data[1]
        whitespaces = data[2]
        error = error_message is not None
        if error_message is not None and error_message is not True:
            error_message = error_message.format(input_text)
        if whitespaces:
            input_text_stripped = input_text.strip(' ')
        else:
            input_text_stripped = input_text

        self.log('Test-' + str(counter) + '. set - "' + input_text + '"')

        # Fill field
        input_field = self.wait_until_visible(element=input_element, type=input_element_type)
        self.input(input_field, input_text)

        try:
            # Click "OK" to try to save the settings.
            self.wait_until_visible(element=save_btn, type=save_btn_type).click()

            # Clicking the button starts an ajax query. Wait until request is complete.
            self.wait_jquery()
        except:
            self.is_equal(error_message, True, msg='Got an exception trying to save data')
            continue

        # Get the error message if any
        ui_error = messages.get_error_message(self)

        # Expecting error
        if error:
            if ui_error is not None:
                error_count += 1
                self.is_equal(ui_error, error_message, msg='Wrong error message, expected: {0}'.format(error_message))
            else:
                # Did not get an error.
                input_field = self.wait_until_visible(element=input_element, type=input_element_type)
                # URL input is not visible so the dialog has been closed = expected an error but data was saved instead
                if not input_field.is_displayed():
                    if error_message == True:
                        self.is_not_none(ui_error, msg='Expected failure but succeeded')
                    else:
                        self.is_not_none(ui_error, msg='No error message, expected: {0}'.format(error_message))

            messages.close_error_messages(self)
        else:
            self.is_none(ui_error, msg='Got error message for: "{0}"'.format(input_text))

            success_count += 1
        counter += 1

    self.wait_jquery()
    return success_count, error_count, input_text_stripped
