import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import auditchecker
from view_models import sidebar as sidebar_constants, clients_table_vm, members_table, \
    keys_and_certificates_table as keyscertificates_constants, popups as popups, messages, \
    groups_table, central_services, log_constants
from view_models.clients_table_vm import DETAILS_TAB_CSS
from view_models.log_constants import ADD_MEMBER_FAILED, EDIT_MEMBER_NAME_FAILED, GENERATE_KEY_FAILED, ADD_WSDL_FAILED, \
    EDIT_MEMBER_NAME
from view_models.messages import get_error_message


def test_key_label_inputs():
    def test_case(self):
        parse_key_label_inputs(self)

    return test_case


def test_csr_inputs():
    def test_case(self):
        parse_csr_inputs(self)

    return test_case


def test_ss_client_inputs():
    def test_case(self):
        """
        MEMBER_47 step 3 System verifies security server client input
        :param self: MainController object
        :return: None
        """
        '''Open security server clients tab'''
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        '''Loop through clients members and subsystems codes and expected results'''
        counter = 1
        for add_client_data in clients_table_vm.MEMBER_SUBSYSTEM_CODE_AND_RESULTS:
            member_code = add_client_data[0]
            subsystem_code = add_client_data[1]
            error = add_client_data[2]
            error_message = add_client_data[3]
            error_message_label = add_client_data[4]
            whitespaces = add_client_data[5]

            self.log('TEST-{0}'.format(counter))
            '''Add client'''
            add_ss_client(self, member_code, subsystem_code)

            '''Verify error messages'''
            error_messages(self, error, error_message, error_message_label)

            if error:
                '''MEMBER 47/3a3a SS administrator selects to terminate the use case.'''
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_CANCEL_BTN_XPATH).click()
            else:
                self.log('Click on "CONTINUE" button')
                self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
                self.log('Click on "CONFIRM" button')
                popups.confirm_dialog_click(self)

                '''MEMBER 54 2. System verifies that mandatory fields are filled.'''
                self.log('''MEMBER 54 2. System verifies that mandatory fields are filled.''')
                '''MEMBER 54 3. System verifies that the user input does not exceed 255 characters.'''
                self.log('''MEMBER 54 3. System verifies that the user input does not exceed 255 characters.''')

                self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
                self.wait_jquery()
                client_id = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                                    get_client_id_by_member_code_subsystem_code(member_code.strip(),
                                                                                                subsystem_code.strip()))

                client_id_text = client_id.text
                self.log(client_id_text)

                if whitespaces:
                    '''MEMBER 54 1. System removes leading and trailing whitespaces.'''
                    self.log('''MEMBER 54 1. System removes leading and trailing whitespaces.''')
                    find_text_with_whitespaces(self, member_code, client_id_text)
                    find_text_with_whitespaces(self, subsystem_code, client_id_text)
                else:
                    assert member_code and subsystem_code in client_id_text

                '''Delete the added client'''
                delete_added_client(self, client_id)
            counter += 1

        self.wait_jquery()

    return test_case


def test_edit_wsdl_inputs():
    def test_case(self):
        """
        SERVICE_09 step 3 Verifies WSDL url
        :param self: MainController object
        :return: None
        """
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        member_code = clients_table_vm.ONE_SS_CLIENT[0]
        subsystem_code = clients_table_vm.ONE_SS_CLIENT[1]

        '''Add client'''
        add_ss_client(self, member_code, subsystem_code)

        self.wait_jquery()
        self.log('Click on "CONTINUE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

        self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
        client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(member_code,
                                                                                         subsystem_code))
        counter = 1
        management_wsdl_url = self.config.get('wsdl.management_service_wsdl_url')
        cs_host = self.config.get('cs.ssh_host')
        ss_2_ssh_host = self.config.get('ss2.ssh_host')
        ss_2_ssh_user = self.config.get('ss2.ssh_user')
        ss_2_ssh_pass = self.config.get('ss2.ssh_pass')
        self.wait_jquery()
        self.log("Open client details")
        client_row.find_element_by_css_selector(DETAILS_TAB_CSS).click()
        add_wsdl_url(self, management_wsdl_url)
        self.wait_jquery()
        '''Open WSDL URL services'''
        self.log('Click on added wsdl url - {0}'.format(management_wsdl_url))
        self.wait_until_visible(type=By.XPATH,
                                element=popups.get_wsdl_url_row(management_wsdl_url)).click()
        self.wait_jquery()
        self.log('Click on "CLOSE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        log_checker = auditchecker.AuditChecker(host=ss_2_ssh_host, username=ss_2_ssh_user, password=ss_2_ssh_pass)

        '''Loop through wsdl url's'''
        for wsdl_data in clients_table_vm.WSDL_DATA:
            current_log_lines = log_checker.get_line_count()
            wsdl_url = wsdl_data[0].format(management_wsdl_url, cs_host)
            error = wsdl_data[1]
            error_message = wsdl_data[2]
            error_message_label = wsdl_data[3]
            whitespaces = wsdl_data[4]

            '''Generate long inputs'''
            long_wsdl_url = wsdl_url.split('#')
            try:
                if long_wsdl_url[1] == '255':
                    multiplier = int(long_wsdl_url[1]) - len(long_wsdl_url[0]) - len(long_wsdl_url[2])
                    wsdl_url = long_wsdl_url[0] + multiplier * 'A' + long_wsdl_url[2]
                elif long_wsdl_url[1] == '256':
                    multiplier = int(long_wsdl_url[1]) - len(long_wsdl_url[0]) - len(long_wsdl_url[2])
                    wsdl_url = long_wsdl_url[0] + multiplier * 'A' + long_wsdl_url[2]
            except:
                pass

            self.log('TEST - {0}'.format(counter))

            self.log("Open client details")
            client_row.find_element_by_css_selector(DETAILS_TAB_CSS).click()

            self.wait_jquery()
            self.log("Open 'Services' tab")
            self.wait_until_visible(type=By.XPATH, element=clients_table_vm.SERVICES_TAB_XPATH).click()

            self.wait_jquery()
            '''SERVICE 09/1 SS administrator selects to edit the URL of a WSDL.'''
            self.log('Click on "Edit" button')
            self.wait_until_visible(type=By.ID, element=popups.EDIT_WSDL_BUTTON_ID).click()
            self.wait_jquery()
            '''SERVICE 09/2 SS administrator inserts the new URL of the WSDL.'''
            self.log('Enter wsdl url (string length = {0}) - {1}'.format(len(wsdl_url), wsdl_url))
            url_field = self.wait_until_visible(type=By.ID, element=popups.EDIT_WSDL_POPUP_URL_ID)
            self.input(url_field, wsdl_url)

            self.wait_jquery()
            self.log('Click on "OK" button')
            self.wait_until_visible(type=By.XPATH, element=popups.EDIT_WSDL_POPUP_OK_BTN_XPATH).click()

            '''SERVICE 09/3 System parses the user input:'''
            '''Verify error messages'''
            error_messages(self, error, error_message, error_message_label)
            self.wait_jquery()

            if error:
                '''SERVICE 09/3a3a SS administrator selects to terminate the use case.'''
                logs_found = log_checker.check_log(log_constants.EDIT_WSDL_FAILED, from_line=current_log_lines + 1)
                self.is_true(logs_found, msg="Edit wsdl failed not found in audit log")
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH, element=popups.EDIT_WSDL_POPUP_CANCEL_BTN_XPATH).click()
            else:
                '''SERVICE 11 2. System verifies that mandatory fields are filled.'''
                self.log('''SERVICE 11 2. System verifies that mandatory fields are filled.''')
                '''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.'''
                self.log('''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.''')
                self.log('Find added WSDL URL row number - ' + wsdl_url)
                found_wsdl_url = self.wait_until_visible(type=By.CSS_SELECTOR,
                                                         element=popups.CLIENT_DETAILS_POPUP_WSDL_CSS)
                found_wsdl_url = found_wsdl_url.text

                if whitespaces:
                    '''SERVICE 11 1. System removes leading and trailing whitespaces.'''
                    self.log('''SERVICE 11 1. System removes leading and trailing whitespaces.''')
                    find_text_with_whitespaces(self, wsdl_url, found_wsdl_url)
                else:
                    assert wsdl_url in found_wsdl_url
                    self.log('Found WSDL URL - ' + found_wsdl_url)

            '''Close details window'''
            self.log('Click on "CLOSE" button')
            self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()
            counter += 1

        '''Delete added client'''
        client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(member_code,
                                                                                         subsystem_code))
        delete_added_client(self, client_row)

    return test_case


def test_disable_wsdl_inputs():
    def test_case(self):
        """
        SERVICE_13 step 4 Verifies WSDL url
        :param self: MainController object
        :return: None
        """
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        member_code = clients_table_vm.ONE_SS_CLIENT[0]
        subsystem_code = clients_table_vm.ONE_SS_CLIENT[1]

        '''Add client'''
        add_ss_client(self, member_code, subsystem_code)

        self.log('Click on "CONTINUE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

        self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
        client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(member_code,
                                                                                         subsystem_code))
        self.wait_jquery()
        '''Add wsdl url'''
        self.log("Open client details")
        client_row.find_element_by_css_selector(DETAILS_TAB_CSS).click()
        add_wsdl_url(self, self.config.get('wsdl.management_service_wsdl_url'))

        self.log('Click on WSDL url row')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=popups.CLIENT_DETAILS_POPUP_WSDL_CSS).click()

        wsdl_disabled = True
        counter = 1
        ss_2_ssh_host = self.config.get('ss2.ssh_host')
        ss_2_ssh_user = self.config.get('ss2.ssh_user')
        ss_2_ssh_pass = self.config.get('ss2.ssh_pass')
        log_checker = auditchecker.AuditChecker(host=ss_2_ssh_host, username=ss_2_ssh_user, password=ss_2_ssh_pass)
        '''Loop through inputs and expected results'''
        for wsdl_disable_notice in clients_table_vm.WSDL_DISABLE_NOTICES:
            current_log_lines = log_checker.get_line_count()
            notice = wsdl_disable_notice[0]
            error = wsdl_disable_notice[1]
            error_message = wsdl_disable_notice[2]
            error_message_label = wsdl_disable_notice[3]

            self.log('TEST - {0}'.format(counter) + str(counter) + '. Notice == "' + notice + '"')

            if wsdl_disabled:
                self.log('Click on "ENABLE" button')
                self.wait_until_visible(type=By.ID,
                                        element=popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()

            '''SERVICE_13/1 SS administrator selects to disable a WSDL.'''
            self.log('Click on "DISABLE" button')
            self.wait_until_visible(type=By.ID,
                                    element=popups.CLIENT_DETAILS_POPUP_DISABLE_WSDL_BTN_ID).click()
            '''SERVICE_13/2 System asks for notice message that will be sent as a response to service clients trying 
            to access services described in the WSDL'''
            '''SERVICE_13/3 SS administrator inserts the message.'''
            self.log('Add notice (string length = {0})- "{1}"'.format(len(notice), notice))
            notice_field = self.wait_until_visible(type=By.ID,
                                                   element=popups.DISABLE_WSDL_POPUP_NOTICE_ID)
            self.input(notice_field, notice)
            self.log('Click on "OK" button')
            self.wait_until_visible(type=By.XPATH,
                                    element=popups.DISABLE_WSDL_POPUP_OK_BTN_XPATH).click()

            '''SERVICE 13/4 System parses the user input:'''
            '''Verify error messages'''
            error_messages(self, error, error_message, error_message_label)
            if error:
                self.log('SERVICE_13 4a2 audit log contains disable wsdl failed when disabling fails')
                logs_found = log_checker.check_log(log_constants.DISABLE_WSDL_FAILED, from_line=current_log_lines + 1)
                self.is_true(logs_found, msg="Disable wsdl failed not found in audit log")
                '''SERVICE 13/4a.3a SS administrator selects to terminate the use case.'''
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.XPATH,
                                        element=popups.DISABLE_WSDL_POPUP_CANCEL_BTN_XPATH).click()
                wsdl_disabled = False
            else:
                wsdl_disabled = True

        self.wait_jquery()
        self.log('Click on "CLOSE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        self.log('Delete added client')
        delete_added_client(self, client_row)
        counter += 1

    return test_case


def edit_service(self, service_url, service_timeout=None, verify_tls=None):
    '''
    Tries to enter WSDL url to "Edit WSDL Parameters" dialog URL input field and press "OK"
    :param self:
    :param url: str - URL that contains the WSDL
    :param clear_field: Boolean - clear the field before entering anything
    :return:
    '''

    self.log('Setting new service URL with timeout {1}: {0}'.format(service_timeout, service_url))

    # Find the "Edit Service Parameters" dialog. Because this function can be called from a state where the dialog is open and
    # a state where it is not, we'll first check if the dialog is open. If it is not, we'll click the "Edit"
    # button to open it.
    wsdl_dialog = self.by_xpath(popups.EDIT_SERVICE_POPUP_XPATH)

    # Open the dialog if it is not already open
    if not wsdl_dialog.is_displayed():
        # Find "Edit" button and click it.
        edit_wsdl_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID)
        edit_wsdl_button.click()

        # Find the dialog and wait until it is visible.
        self.wait_until_visible(wsdl_dialog)

    # Now an "Edit Service Parameters" dialog with a URL prompt should be open. Let's try to set the service URL.

    # Find the URL input element
    service_url_input = self.by_id(popups.EDIT_SERVICE_POPUP_URL_ID)
    service_timeout_input = self.by_id(popups.EDIT_SERVICE_POPUP_TIMEOUT_ID)

    # Enter the service URL.
    self.input(service_url_input, service_url)

    # Set service timeout if specified
    if service_timeout is not None:
        # UC SERVICE_timeout_input.clear()
        # UC SERVICE_timeout_input.send_keys(service_timeout)
        self.input(service_timeout_input, service_timeout)

    # Set "Verify TLS" if specified
    if verify_tls is not None:
        service_tls_checkbox = self.wait_until_visible(popups.EDIT_SERVICE_POPUP_TLS_ENABLED_XPATH, By.XPATH)
        checked = service_tls_checkbox.get_attribute('checked')

        if ((checked != '' and checked is not None) and not verify_tls) or (checked is None and verify_tls):
            service_tls_checkbox.click()

    # Find the "OK" button in "Edit WSDL Parameters" dialog
    wsdl_dialog_ok_button = self.by_xpath(popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH)
    wsdl_dialog_ok_button.click()

    # Clicking the button starts an ajax query. Wait until request is complete.
    self.wait_jquery()

    warning_message = messages.get_warning_message(self)  # Warning message
    error_message = messages.get_error_message(self)  # Error message (anywhere)

    return warning_message, error_message


def test_edit_address_service():
    def test_case(self):
        """
        SERVICE_19 step 3 verifies address of a service
        :param self: MainController object
        :return: None
        """
        ss_2_ssh_host = self.config.get('ss2.ssh_host')
        ss_2_ssh_user = self.config.get('ss2.ssh_user')
        ss_2_ssh_pass = self.config.get('ss2.ssh_pass')

        '''Open security server clients tab'''
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        '''Get parameters member_code and subsystem_code from clients_table_vm.py'''
        member_code = clients_table_vm.ONE_SS_CLIENT[0]
        subsystem_code = clients_table_vm.ONE_SS_CLIENT[1]

        '''Add client of the security service'''
        add_ss_client(self, member_code, subsystem_code)

        '''Confirm added client'''
        self.log('Click on "CONTINUE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

        self.wait_jquery()
        '''Get a client id as a parameter'''
        self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
        client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(member_code,
                                                                                         subsystem_code))
        self.wait_jquery()
        '''Add a wsdl url'''
        self.log("Open client details")
        client_row.find_element_by_css_selector(DETAILS_TAB_CSS).click()

        add_wsdl_url(self, self.config.get('wsdl.management_service_wsdl_url'))

        '''Open WSDL URL services'''
        self.log('Open WSDL URL services, clicking on "+"')
        self.wait_until_visible(type=By.CLASS_NAME, element=popups.CLIENT_DETAILS_POPUP_WSDL_URL_DETAILS_CLASS).click()

        counter = 1
        cs_service_url = self.config.get('cs.service_url')
        log_checker = auditchecker.AuditChecker(host=ss_2_ssh_host, username=ss_2_ssh_user, password=ss_2_ssh_pass)

        '''Loop through data from the clients_table_vm.py'''
        for service_url_data in clients_table_vm.SERVICE_URLS_DATA:
            current_log_lines = log_checker.get_line_count()
            '''Set necessary parameters'''
            service_url = service_url_data[0].format(cs_service_url)
            error = service_url_data[1]
            error_message = service_url_data[2]
            error_message_label = service_url_data[3]
            whitespaces = service_url_data[4]

            '''Generate long inputs'''
            long_service_url = service_url.split('#')

            try:
                if long_service_url[1] == '255' or long_service_url[1] == '256':
                    multiplier = int(long_service_url[1]) - len(long_service_url[0]) - len(long_service_url[2])
                    service_url = long_service_url[0] + multiplier * 'A' + long_service_url[2]
            except:
                pass

            self.log('TEST - {0}'.format(counter))

            '''Activate a authCertDeletion service row'''
            self.log('Click on authCertDeletion service row')
            self.wait_until_visible(type=By.XPATH, element=popups.
                                    CLIENT_DETAILS_POPUP_WSDL_SERVICES_AUTHCERTDELETION_XPATH).click()

            '''SERVICE_19/1 SS administrator selects to edit the address of a service.'''
            self.log('Click on "EDIT" button')
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()

            '''SERVICE_19/2 SS administrator inserts the address.'''
            self.log('Enter service URL (string length = {0}) - {1}'.format(len(service_url), service_url))
            entered_service_url = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_URL_ID)
            self.input(entered_service_url, service_url)

            self.log('Click on "OK" button')
            self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()

            '''SERVICE_19/2 System parses the user input'''
            '''Check for the error messages'''
            error_messages(self, error, error_message, error_message_label)

            if error:
                '''SERVICE 19/3a.2 System logs the event "Edit service parameters failed" to the audit log.'''
                logs_found = log_checker.check_log(log_constants.EDIT_SERVICE_PARAMS_FAILED,
                                                   from_line=current_log_lines + 1)
                self.is_true(logs_found, msg="Edit service parameters failed not found in audit log")
                '''SERVICE 19/3a.3a SS administrator selects to terminate the use case.'''
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_CANCEL_BTN_XPATH).click()
            else:
                '''SERVICE 11 2. System verifies that mandatory fields are filled.'''
                self.log('''SERVICE 11 2. System verifies that mandatory fields are filled.''')
                '''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.'''
                self.log('''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.''')
                self.log('Find added service url text - ' + service_url.strip())
                get_srervice_url = clients_table_vm.find_service_url_by_text(self, service_url.strip())
                get_srervice_url = get_srervice_url.text
                self.log('Found service URL - ' + get_srervice_url)

                if whitespaces:
                    '''SERVICE 11 1. System removes leading and trailing whitespaces.'''
                    self.log('''SERVICE 11 1. System removes leading and trailing whitespaces.''')
                    find_text_with_whitespaces(self, service_url, get_srervice_url)
                else:
                    assert service_url in get_srervice_url
                    self.log('Found service URL - ' + get_srervice_url)

            counter += 1

        '''Close a pop-up window of the client details'''
        self.wait_jquery()


        '''SERVICE_19/1 SS administrator selects to edit the address of a service.'''
        self.log('Click on "EDIT" button')
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()

        '''SERVICE_19/2 SS administrator inserts the address.'''
        self.log('Enter service URL (string length = {0}) - {1}'.format(len(service_url), service_url))

        wsdl_correct_url = self.config.get('wsdl.remote_path').format(
            self.config.get('wsdl.service_wsdl'))  # Correct URL that returns a WSDL file
        self.log('Replace url with https version')
        service_url_input = self.by_id(popups.EDIT_SERVICE_POPUP_URL_ID)

        self.log('Replace url with https version')
        wsdl_correct_url_https = wsdl_correct_url.replace('http:', 'https:')
        self.input(service_url_input, wsdl_correct_url_https)
        self.log('SERVICE_19 5. System sets the TLS certification verification to "true" when url starts with https')
        service_tls_checkbox = self.by_xpath(popups.EDIT_SERVICE_POPUP_TLS_ENABLED_XPATH)
        self.is_equal('true', service_tls_checkbox.get_attribute('checked'))
        self.log('Click OK')
        self.by_xpath(popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
        self.log('Click on edit button again')
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()
        self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_XPATH)
        self.log('Replace url with http version')
        self.input(service_url_input, wsdl_correct_url)
        self.log('SERVICE_19 5a. System sets the TLS certification verification to "false" when url starts with http')
        self.is_false(self.by_id(popups.EDIT_SERVICE_POPUP_TLS_ID).is_enabled())
        self.by_xpath(popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
        self.log('Click on "CLOSE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        '''Delete added client'''
        delete_added_client(self, client_row)
        counter += 1

    return test_case


def test_cs_member_inputs():
    def test_case(self):
        """
        MEMBER_10 step 3, 4 and 6 System verifies added member in central server
        :param self: MainController object
        :return: None
        """

        '''Loop through member names, classes, codes and expected results'''
        counter = 1
        log_checker = auditchecker.AuditChecker(host=self.config.get('cs.ssh_host'),
                                                username=self.config.get('cs.ssh_user'),
                                                password=self.config.get('cs.ssh_pass'))
        for member in members_table.ADD_MEMBER_TEXTS_AND_RESULTS:
            current_log_lines = log_checker.get_line_count()
            member_name = member[0]
            member_class = member[1]
            member_code = member[2]
            error = member[3]
            error_message = member[4]
            error_message_label = member[5]
            whitespaces = member[6]
            self.log('TEST- {0}'.format(str(counter)))

            '''Add cs member'''
            add_cs_member(self, member_name, member_class, member_code)

            '''Verify error messages'''
            error_messages(self, error, error_message, error_message_label)

            if error:
                expected_log_msg = ADD_MEMBER_FAILED
                self.log('MEMBER_10 3a.2 System logs the event "{0}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
                '''MEMBER 10/3a3a SS administrator selects to terminate the use case.'''
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_CANCEL_BTN_XPATH).click()
                if counter == 10:
                    '''delete added member'''
                    delete_added_member(self, member_name.strip())
            else:
                '''MEMBER 10/6 System displays the message: "Successfully added X-Road member with member class 'X' and 
                member code 'Y'.", where "X" is the inserted member class and "Y" the inserted member code.'''
                self.log('''MEMBER 10/6 System displays the message: "Successfully added X-Road member with 
                member class 'X' and member code 'Y'.", where "X" is the inserted member class and "Y" 
                the inserted member code.''')
                self.wait_jquery()
                confirmation_message = messages.get_notice_message(self)
                self.log('Compare confirmation message to the expected confirmation message')
                assert confirmation_message in "Successfully added X-Road member with member class '" + member_class + \
                                               "' and member code '" + member_code.strip() + "'."
                self.log(confirmation_message)

                '''Close the member details pop up window'''
                self.log('Click on "CLOSE" button')
                self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH) \
                    .click()

                self.wait_jquery()
                '''MEMBER 54 2. System verifies that mandatory fields are filled.'''
                self.log('''MEMBER 54 2. System verifies that mandatory fields are filled.''')
                '''MEMBER 54 3. System verifies that the user input does not exceed 255 characters.'''
                self.log('''MEMBER 54 3. System verifies that the user input does not exceed 255 characters.''')

                '''Verify that the added member name exists in the member table'''
                self.log('Find member name - ' + member_name + ' - in members table')
                get_member_name = self.by_xpath(element=members_table.
                                                get_member_data_from_table(1, member_name.strip()))
                get_member_name = get_member_name.text
                '''Verify that the added member class exists in the member table'''
                self.log('Find member class - ' + member_class + ' - in members table')
                get_member_class = self.by_xpath(element=members_table.
                                                 get_member_data_from_table(2, member_class.strip()))
                get_member_class = get_member_class.text
                '''Verify that the added member code exists in the member table'''
                self.log('Find member code - ' + member_code + ' - in members table')
                get_member_code = self.by_xpath(element=members_table.
                                                get_member_data_from_table(3, member_code.strip()))
                get_member_code = get_member_code.text

                if whitespaces:
                    '''MEMBER 54 1. System removes leading and trailing whitespaces.'''
                    self.log('''MEMBER 54 1. System removes leading and trailing whitespaces.''')
                    find_text_with_whitespaces(self, member_name, get_member_name)
                    find_text_with_whitespaces(self, member_code, get_member_code)
                else:
                    assert member_name in get_member_name
                    assert member_class in get_member_class
                    assert member_code in get_member_code

                if counter == 9:
                    pass
                else:
                    '''delete added member'''
                    delete_added_member(self, member_name.strip())

            counter += 1

    return test_case


def test_edit_cs_member_inputs():
    def test_case(self):
        """
        MEMBER_11 step 3 System verifies changed member name in the central server
        :param self: MainController object
        :return: None
        """

        '''Add cs member'''
        add_cs_member(self, members_table.CS_MEMBER_NAME_CLASS_CODE[0],
                      members_table.CS_MEMBER_NAME_CLASS_CODE[1],
                      members_table.CS_MEMBER_NAME_CLASS_CODE[2])
        added_member_name = members_table.CS_MEMBER_NAME_CLASS_CODE[0]
        log_checker = auditchecker.AuditChecker(host=self.config.get('cs.ssh_host'),
                                                username=self.config.get('cs.ssh_user'),
                                                password=self.config.get('cs.ssh_pass'))
        '''Close the member details pop up window'''
        self.log('Click on "CLOSE" button')
        self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH) \
            .click()

        '''Loop through member names and expected results'''
        counter = 1
        for member in members_table.CHANGE_MEMBER_TEXTS_AND_RESULTS:
            current_log_lines = log_checker.get_line_count()
            new_member_name = member[0]
            error = member[1]
            error_message = member[2]
            error_message_label = member[3]
            whitespaces = member[4]

            self.log('TEST - {0}'.format(counter))
            self.wait_jquery()
            self.log('Click member name - ' + added_member_name + ' - in members table')
            self.wait_until_visible(type=By.XPATH,
                                    element=members_table.get_member_data_from_table(1, added_member_name)).click()
            self.log('Click on "DETAILS" button')
            self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
            '''MEMBER_11/1 CS administrator selects to edit the name of an X-Road member.'''
            self.log('Click on "EDIT" button')
            self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_NAME_EDIT_BTN_XPATH).click()
            '''MEMBER_11/2 CS administrator inserts the name.'''
            self.log(
                'Edit member name with (string length = {0}) - "{1}"'.format(len(new_member_name), new_member_name))
            edit_member_name = self.wait_until_visible(type=By.XPATH, element=members_table.
                                                       MEMBER_EDIT_NAME_POPUP_EDIT_NAME_AREA_XPATH)
            self.input(edit_member_name, new_member_name)
            self.log('Click on "OK" button')
            self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH).click()

            '''MEMBER 11 / 3 System parses the user input'''
            '''Check for the error messages'''
            error_messages(self, error, error_message, error_message_label)

            if error:
                expected_log_msg = EDIT_MEMBER_NAME_FAILED
                self.log('MEMBER_11 3.a.2 System logs the event {0}'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
                '''MEMBER_11/3a.3a SS administrator selects to terminate the use case.'''
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_CANCEL_BTN_XPATH) \
                    .click()
                self.wait_jquery()
                self.log('Click on "Close" button')
                self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH) \
                    .click()

            else:
                added_member_name = new_member_name.strip()
                '''Close the member details pop up window'''
                self.wait_jquery()
                self.log('Click on "CLOSE" button')
                self.wait_until_visible(type=By.XPATH,
                                        element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH).click()
                self.wait_jquery()

                expected_log_msg = EDIT_MEMBER_NAME
                self.log('MEMBER_11 5. System logs the event {0}'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)

                '''MEMBER 54 2. System verifies that mandatory fields are filled.'''
                self.log('''MEMBER 54 2. System verifies that mandatory fields are filled.''')
                '''MEMBER 54 2. System verifies that the user input does not exceed 255 characters.'''
                self.log('''MEMBER 54 3. System verifies that the user input does not exceed 255 characters.''')
                '''Verify that the added member name exists in the member table'''
                self.log('Find member name - ' + added_member_name + ' - in members table')
                get_member_name = self.by_xpath(element=members_table.get_member_data_from_table(1, added_member_name))
                get_member_name = get_member_name.text

                if whitespaces:
                    '''MEMBER 54 1. System removes leading and trailing whitespaces.'''
                    self.log('''SERVICE 11 1. System removes leading and trailing whitespaces.''')
                    find_text_with_whitespaces(self, new_member_name, get_member_name)
                else:
                    assert new_member_name in get_member_name

            counter += 1
        '''Delete added member'''
        delete_added_member(self, added_member_name)

    return test_case


def test_global_groups_inputs():
    def test_case(self):
        parse_global_groups_inputs(self)

    return test_case


def test_central_service_inputs():
    def test_case(self):
        """
        SERVICE_41 step 3 System verifies added central services
        :param self: MainController object
        :return: None
        """

        cs_ssh_host = self.config.get('cs.ssh_host')
        cs_ssh_user = self.config.get('cs.ssh_user')
        cs_ssh_pass = self.config.get('cs.ssh_pass')

        '''Loop through data from the groups_table.py'''
        counter = 1
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
        for group_data in central_services.NEW_CENTRAL_SERVICE_DATA:
            current_log_lines = log_checker.get_line_count()
            '''Set parameters'''
            cs_code = group_data[0]
            code = group_data[1]
            version = group_data[2]
            provider_name = group_data[3]
            provider_code = group_data[4]
            provider_class = group_data[5]
            provider_subsystem = group_data[6]
            error = group_data[7]
            error_message = group_data[8]
            error_message_label = group_data[9]
            whitespaces = group_data[10]

            self.log('TEST - {0}'.format(counter))

            if not error:
                '''Get provider parameters from the system'''
                get_provider_parameter = get_provider_parameters(self)
                provider_code = get_provider_parameter[0]
                provider_class = get_provider_parameter[1]
                provider_subsystem = get_provider_parameter[2]
                code = get_provider_parameter[3]
                provider_name = get_provider_parameter[4]

                if whitespaces:
                    provider_subsystem = '{0}{1}{0}'.format('   ', provider_subsystem)
                    code = '{0}{1}{0}'.format('   ', code)
                    provider_name = '{0}{1}{0}'.format('   ', provider_name)
                    provider_code = '{0}{1}{0}'.format('   ', provider_code)

            '''Open central services'''
            self.log('Open Central Cervices tab')
            self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CENTRAL_SERVICES_CSS).click()
            self.wait_jquery()

            '''Start adding central service'''
            add_central_service(self, cs_code, code, version, provider_name, provider_code, provider_class,
                                provider_subsystem)

            '''Verify error messages'''
            error_messages(self, error, error_message, error_message_label)

            if error:
                '''SERVICE_41 3a2 System logs the event "Add central service failed" to the audit log.'''
                logs_found = log_checker.check_log(log_constants.ADD_CENTRAL_SERVICE_FAILED,
                                                   from_line=current_log_lines + 1)
                self.is_true(logs_found, msg="Add central service failed not found in audit log")
                '''SERVICE_41 3a3a CS administrator selects to terminate the use case.'''
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_CANCEL_BUTTON_ID).click()
            else:
                '''SERVICE 11 2. System verifies that mandatory fields are filled.'''
                self.log('''SERVICE 11 2. System verifies that mandatory fields are filled.''')
                '''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.'''
                self.log('''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.''')
                '''Verify that the added member name exists in the member table'''
                self.log('Find added code text - ' + cs_code.strip())
                cs_code_in = self.wait_until_visible(type=By.XPATH,
                                                     element=central_services.get_central_service_text(cs_code.strip()))
                self.log('Find added code text - ' + code.strip())
                code_in = self.wait_until_visible(type=By.XPATH,
                                                  element=central_services.get_central_service_text(code.strip()))
                self.log('Find added code text - ' + version.strip())
                version_in = self.wait_until_visible(type=By.XPATH,
                                                     element=central_services.get_central_service_text(version.strip()))
                self.log('Find added code text - ' + provider_code.strip())
                provider_code_in = self.wait_until_visible(type=By.XPATH,
                                                           element=central_services.
                                                           get_central_service_text(provider_code.strip()))
                self.log('Find added code text - ' + provider_class.strip())
                self.wait_until_visible(type=By.XPATH,
                                        element=central_services.get_central_service_text(provider_class.strip()))
                self.log('Find added code text - ' + provider_subsystem.strip())
                provider_subsystem_in = self.wait_until_visible(type=By.XPATH,
                                                                element=central_services.
                                                                get_central_service_text(provider_subsystem.strip()))

                cs_code_text = cs_code_in.text
                code_text = code_in.text
                version_text = version_in.text
                provider_code_text = provider_code_in.text
                provider_subsystem_text = provider_subsystem_in.text

                if whitespaces:
                    '''SERVICE_11 1. System removes leading and trailing whitespaces.'''
                    self.log('''SERVICE 11 1. System removes leading and trailing whitespaces.''')
                    find_text_with_whitespaces(self, cs_code, cs_code_text)
                    find_text_with_whitespaces(self, code, code_text)
                    find_text_with_whitespaces(self, version, version_text)
                    find_text_with_whitespaces(self, provider_code, provider_code_text)
                    find_text_with_whitespaces(self, provider_subsystem, provider_subsystem_text)
                else:
                    assert cs_code in cs_code_text
                    assert code in code_text
                    assert version in version_text
                    assert provider_code in provider_code_text
                    assert provider_subsystem in provider_subsystem_text

                '''Delete added central service'''
                self.log('Delete added central service')
                self.log('Click on added central service row')
                cs_code_in.click()
                self.wait_jquery()
                self.log('Click on "DELETE" button')
                self.wait_until_visible(type=By.ID, element=central_services.SERVICE_DELETE_BUTTON_ID).click()
                self.log('Click on "CONFIRM" button')
                popups.confirm_dialog_click(self)

            counter += 1

    return test_case


def test_edited_central_service_inputs():
    def test_case(self):
        """
        SERVICE_42 step 3 System verifies changed Implementing Service
        :param self: MainController object
        :return: None
        """

        cs_ssh_host = self.config.get('cs.ssh_host')
        cs_ssh_user = self.config.get('cs.ssh_user')
        cs_ssh_pass = self.config.get('cs.ssh_pass')

        get_provider_parameter = get_provider_parameters(self)
        provider_code = get_provider_parameter[0]
        provider_class = get_provider_parameter[1]
        provider_subsystem = get_provider_parameter[2]
        code = get_provider_parameter[3]
        provider_name = get_provider_parameter[4]

        '''Open central services'''
        self.log('Open Central Cervices tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CENTRAL_SERVICES_CSS).click()
        self.wait_jquery()

        '''Start adding central service'''
        self.log('Add central service')
        add_central_service(self, central_services.CENTRAL_SERVICE[0], code,
                            central_services.CENTRAL_SERVICE[2], provider_name,
                            provider_code, provider_class,
                            provider_subsystem)

        '''Loop through data from the groups_table.py'''
        counter = 1
        log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
        for group_data in central_services.EDIT_CENTRAL_SERVICE_DATA:
            current_log_lines = log_checker.get_line_count()
            '''Set parameters'''
            cs_code = group_data[0]
            code = group_data[1]
            version = group_data[2]
            provider_name = group_data[3]
            provider_code = group_data[4]
            provider_class = group_data[5]
            provider_subsystem = group_data[6]
            error = group_data[7]
            error_message = group_data[8]
            error_message_label = group_data[9]
            whitespaces = group_data[10]

            if not error:
                '''Get provider parameters from the system'''
                get_provider_parameter = get_provider_parameters(self)
                provider_code = get_provider_parameter[0]
                provider_class = get_provider_parameter[1]
                provider_subsystem = get_provider_parameter[2]
                code = get_provider_parameter[3]
                provider_name = get_provider_parameter[4]

                if whitespaces:
                    provider_subsystem = '{0}{1}{0}'.format('   ', provider_subsystem)
                    code = '{0}{1}{0}'.format('   ', code)
                    provider_name = '{0}{1}{0}'.format('   ', provider_name)
                    provider_code = '{0}{1}{0}'.format('   ', provider_code)

            '''Open central services'''
            self.log('Open Central Cervices tab')
            self.wait_until_visible(type=By.CSS_SELECTOR,
                                    element=sidebar_constants.CENTRAL_SERVICES_CSS).click()
            self.wait_jquery()

            self.log('TEST - {0}'.format(counter))

            self.log('Click on added central service row')
            cs_code_row = self.wait_until_visible(type=By.XPATH,
                                                  element=central_services.get_central_service_text('CS_CODE'))
            self.click(cs_code_row)

            '''SSERVICE_42/1 CS administrator selects to edit the implementing service of a central service.'''
            self.log('Click on "EDIT" button')
            self.wait_until_visible(type=By.ID, element=central_services.SERVICE_EDIT_BUTTON_ID).click()

            self.log('Click on "CLEAR" button')
            self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_CLEAR_BUTTON_ID).click()

            '''SSERVICE_42/2 CS administrator inserts the X-Road identifier of the implementing service and the name 
            of the service provider.'''
            '''Add code'''
            self.log('Add  code (string length = {0}) - {1}'.format(len(code), code))
            self.wait_jquery()
            code_input = self.wait_until_visible(type=By.ID,
                                                 element=popups.CENTRAL_SERVICE_POPUP_TARGET_CODE_ID)
            self.input(code_input, code)

            '''Add version'''
            self.log('Add  version (string length = {0}) - {1}'.format(len(version), version))
            self.wait_jquery()
            version_input = self.wait_until_visible(type=By.ID,
                                                    element=popups.CENTRAL_SERVICE_POPUP_TARGET_VERSION_ID)
            self.input(version_input, version)

            '''Add provider name'''
            self.log('Add  provider name (string length = {0}) - {1}'.format(len(provider_name), provider_name))
            self.wait_jquery()
            provider_name_input = self.wait_until_visible(type=By.ID,
                                                          element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_ID)
            self.input(provider_name_input, provider_name)

            '''Add provider code'''
            self.log('Add  provider code (string length = {0}) - {1}'.format(len(provider_code), provider_code))
            self.wait_jquery()
            provider_code_input = self.wait_until_visible(type=By.ID,
                                                          element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CODE_ID)
            self.input(provider_code_input, provider_code)

            '''Add provider class'''
            self.log('Select ' + provider_class + ' from "class" dropdown')
            select = Select(self.wait_until_visible(type=By.ID,
                                                    element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CLASS_ID))
            select.select_by_visible_text(provider_class)

            '''Add provider subsystem'''
            self.log('Add  provider subsystem (string length = {0}) - {1}'.format(len(provider_subsystem),
                                                                                  provider_subsystem))
            self.wait_jquery()
            provider_subsystem_input = self.wait_until_visible(type=By.ID,
                                                               element=popups.
                                                               CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_SUBSYSTEM_ID)
            self.input(provider_subsystem_input, provider_subsystem)

            '''Click on 'OK' button'''
            self.log('Click on "OK" button')
            self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID).click()

            '''Verify error messages'''
            error_messages(self, error, error_message, error_message_label)

            if error:
                '''SERVICE 42/3a.2 System logs the event "Edit central service failed" to the audit log.'''
                logs_found = log_checker.check_log(log_constants.EDIT_CENTRAL_SERVICE_FAILED,
                                                   from_line=current_log_lines + 1)
                self.is_true(logs_found, msg="Edit central service failed not found in audit log")
                '''SERVICE 42/3a.3a CS administrator selects to terminate the use case.'''
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_CANCEL_BUTTON_ID).click()
            else:
                self.wait_jquery()
                '''SERVICE 11 2. System verifies that mandatory fields are filled.'''
                self.log('''SERVICE 11 2. System verifies that mandatory fields are filled.''')
                '''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.'''
                self.log('''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.''')
                '''Verify that the added member name exists in the member table'''
                self.log('Find added code text - ' + code.strip())
                code_in = self.wait_until_visible(type=By.XPATH,
                                                  element=central_services.get_central_service_text(code.strip()))
                self.log('Find added code text - ' + version.strip())
                version_in = self.wait_until_visible(type=By.XPATH,
                                                     element=central_services.get_central_service_text(version.strip()))
                self.log('Find added code text - ' + provider_code.strip())
                provider_code_in = self.wait_until_visible(type=By.XPATH,
                                                           element=central_services.
                                                           get_central_service_text(provider_code.strip()))
                self.log('Find added code text - ' + provider_class.strip())
                self.wait_until_visible(type=By.XPATH,
                                        element=central_services.get_central_service_text(provider_class.strip()))
                self.log('Find added code text - ' + provider_subsystem.strip())
                provider_subsystem_in = self.wait_until_visible(type=By.XPATH,
                                                                element=central_services.
                                                                get_central_service_text(provider_subsystem.strip()))

                code_text = code_in.text
                version_text = version_in.text
                provider_code_text = provider_code_in.text
                provider_subsystem_text = provider_subsystem_in.text

                if whitespaces:
                    '''SERVICE_11 1. System removes leading and trailing whitespaces.'''
                    self.log('''SERVICE 11 1. System removes leading and trailing whitespaces.''')
                    find_text_with_whitespaces(self, code, code_text)
                    find_text_with_whitespaces(self, version, version_text)
                    find_text_with_whitespaces(self, provider_code, provider_code_text)
                    find_text_with_whitespaces(self, provider_subsystem, provider_subsystem_text)
                else:
                    assert code in code_text
                    assert version in version_text
                    assert provider_code in provider_code_text
                    assert provider_subsystem in provider_subsystem_text

            counter += 1

        '''Delete added central service'''
        self.log('Delete added central service')
        self.log('Click on added central service row')
        cs_row = self.wait_until_visible(type=By.XPATH, element=central_services.
                                         get_central_service_text(central_services.CENTRAL_SERVICE[0].strip()))
        self.click(cs_row)
        self.wait_jquery()
        self.log('Click on "DELETE" button')
        self.wait_until_visible(type=By.ID, element=central_services.SERVICE_DELETE_BUTTON_ID).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

    return test_case


def test_edit_time_out_value_service():
    def test_case(self):
        """
        SERVICE_21 step 3 verifies timeout of a service
        :param self: MainController object
        :return: None
        """
        ss_2_ssh_host = self.config.get('ss2.ssh_host')
        ss_2_ssh_user = self.config.get('ss2.ssh_user')
        ss_2_ssh_pass = self.config.get('ss2.ssh_pass')

        '''Open security server clients tab'''
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        '''Get parameters member_code and subsystem_code from clients_table_vm.py'''
        member_code = clients_table_vm.ONE_SS_CLIENT[0]
        subsystem_code = clients_table_vm.ONE_SS_CLIENT[1]

        '''Add client of the security service'''
        add_ss_client(self, member_code, subsystem_code)

        '''Confirm added client'''
        self.log('Click on "CONTINUE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

        self.wait_jquery()
        '''Get a client id as a parameter'''
        self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
        client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(member_code,
                                                                                         subsystem_code))
        self.wait_jquery()
        '''Add a wsdl url'''
        self.log("Open client details")
        client_row.find_element_by_css_selector(DETAILS_TAB_CSS).click()

        add_wsdl_url(self, self.config.get('wsdl.management_service_wsdl_url'))

        '''Open WSDL URL services'''
        self.log('Open WSDL URL services, clicking on "+"')
        self.wait_until_visible(type=By.CLASS_NAME, element=popups.CLIENT_DETAILS_POPUP_WSDL_URL_DETAILS_CLASS).click()

        counter = 1
        log_checker = auditchecker.AuditChecker(host=ss_2_ssh_host, username=ss_2_ssh_user, password=ss_2_ssh_pass)

        '''Loop through data from the clients_table_vm.py'''
        for service_timeout_data in clients_table_vm.SERVICE_TIMEOUTS_DATA:
            current_log_lines = log_checker.get_line_count()
            '''Set necessary parameters'''
            repeat_timeout_value_multiplier = service_timeout_data[0]
            service_timeout = service_timeout_data[1]
            error = service_timeout_data[2]
            error_message = service_timeout_data[3]
            error_message_label = service_timeout_data[4]
            whitespaces = service_timeout_data[5]

            '''Generate long inputs'''
            try:
                if repeat_timeout_value_multiplier > 0:
                    multiplier = int(repeat_timeout_value_multiplier) - len(service_timeout)
                    service_timeout = service_timeout + multiplier * '1'
            except:
                pass

            self.log('Test-{0}. Service timeout == "{1}"'.format(counter, service_timeout))

            '''Activate a authCertDeletion service row'''
            self.log('Click on authCertDeletion service row')
            self.wait_until_visible(type=By.XPATH, element=popups.
                                    CLIENT_DETAILS_POPUP_WSDL_SERVICES_AUTHCERTDELETION_XPATH).click()
            '''SERVICE 21 / 1 SS administrator selects to edit the timeout value of a service.'''
            self.log('Click on "EDIT" button')
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()

            '''SERVICE 21 / 2 SS administrator inserts the timeout value.'''
            self.log('Enter service timeout (string length = {0}) - {1}'.format(len(service_timeout), service_timeout))
            entered_service_timeout = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_TIMEOUT_ID)
            self.input(entered_service_timeout, service_timeout)

            self.log('Get service url to find the row later')
            entered_service_url = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_URL_ID)
            entered_service_url_value = entered_service_url.get_attribute('value')

            self.log('Click on "OK" button')
            self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()

            '''SERVICE 21 / 3 System parses the user input'''
            '''Check for the error messages'''
            error_messages(self, error, error_message, error_message_label)
            self.log('SERVICE_21 5. System saves the inserted service timeout value to the system configuration.')

            if error:
                '''SERVICE 21/3a.2 System logs the event "Edit service parameters failed" to the audit log.'''
                logs_found = log_checker.check_log(log_constants.EDIT_SERVICE_PARAMS_FAILED,
                                                   from_line=current_log_lines + 1)
                self.is_true(logs_found, msg="Edit service paramters failed not found in audit log")
                '''SERVICE 21/3a.3a SS administrator selects to terminate the use case.'''
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_CANCEL_BTN_XPATH).click()
            else:

                '''SERVICE 11 2. System verifies that mandatory fields are filled.'''
                self.log('''SERVICE 11 2. System verifies that mandatory fields are filled.''')
                '''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.'''
                self.log('''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.''')
                '''Verify that the added service url exists'''
                self.log('Find added service timeout text - {0}'.format(service_timeout))
                get_service_timeout = clients_table_vm.find_service_timeout_by_text(self, entered_service_url_value,
                                                                                    service_timeout.strip())
                get_service_timeout = get_service_timeout.text
                self.log('Found service timeout - {0}'.format(get_service_timeout))

                self.log('SERVICE_21 5. System saves the inserted service timeout value to the system configuration.')

                '''Verify that there is not inputs with whitespaces'''
                if whitespaces:
                    '''SERVICE 11 1. System removes leading and trailing whitespaces.'''
                    self.log('''SERVICE 11 1. System removes leading and trailing whitespaces.''')
                    find_text_with_whitespaces(self, service_timeout, get_service_timeout)
                else:
                    assert service_timeout in get_service_timeout
                    self.log('Found service with timeout- ' + get_service_timeout)

        ''' SERVICE_21 6. System logs the event Edit service parameters to the audit log. '''
        logs_found = log_checker.check_log(log_constants.EDIT_SERVICE_PARAMS,
                                           from_line=current_log_lines + 1)

        self.is_true(logs_found, msg="Edit service paramters not found in audit log")

        '''Activate a authCertDeletion service row'''
        self.log('Click on authCertDeletion service row')
        self.wait_until_visible(type=By.XPATH, element=popups.
                                CLIENT_DETAILS_POPUP_WSDL_SERVICES_AUTHCERTDELETION_XPATH).click()
        '''SERVICE 21 / 1 SS administrator selects to edit the timeout value of a service.'''
        self.log('Click on "EDIT" button')
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()
        entered_service_timeout = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_TIMEOUT_ID)
        self.log('SERVICE_21 4a. The inserted timeout value is 0')
        self.input(entered_service_timeout, '0')

        self.log('Click on "OK" button')
        self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
        warning = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.WARNING_MESSAGE_CSS).text
        expected_warning_message = messages.SERVICE_EDIT_INFINITE_TIMEOUT_WARNING
        self.log('SERVICE_21 4a.1 System displays a warning message "{0}"'.format(
            messages.SERVICE_EDIT_INFINITE_TIMEOUT_WARNING))
        self.is_equal(expected_warning_message, warning)

        '''Click "Cancel" button'''
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CANCEL_XPATH).click()
        self.log('Click on "OK" button')
        self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
        '''Click continue button'''
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.wait_jquery()
        '''Get timeout value'''
        timeout_value = self.wait_until_visible(type=By.XPATH,
                                                element=popups.CLIENT_DETAILS_POPUP_WSDL_SERVICES_AUTHCERTDELETION_XPATH2).text
        '''Verify timeout value'''
        self.is_equal(timeout_value, '0',
                      msg='Timeout value is wrong')

        '''Close a pop-up window of the client details'''
        self.wait_jquery()
        self.log('Click on "CLOSE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        '''Delete added client'''
        delete_added_client(self, client_row)

        counter += 1

    return test_case


def test_added_wsdl_inputs():
    def test_case(self):
        """
        SERVICE_08 step 3 Add WSDL input parsing
        :param self: MainController object
        :return: None
        """
        ss_2_ssh_host = self.config.get('ss2.ssh_host')
        ss_2_ssh_user = self.config.get('ss2.ssh_user')
        ss_2_ssh_pass = self.config.get('ss2.ssh_pass')

        '''Open security server clients tab'''
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        member_code = clients_table_vm.ONE_SS_CLIENT[0]
        subsystem_code = clients_table_vm.ONE_SS_CLIENT[1]

        '''Add client'''
        add_ss_client(self, member_code, subsystem_code)

        self.log('Click on "CONTINUE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

        self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
        client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(member_code,
                                                                                         subsystem_code))
        counter = 1
        management_wsdl_url = self.config.get('wsdl.management_service_wsdl_url')
        cs_host = self.config.get('cs.ssh_host')

        log_checker = auditchecker.AuditChecker(host=ss_2_ssh_host, username=ss_2_ssh_user, password=ss_2_ssh_pass)
        '''Loop through wsdl url's'''
        for wsdl_data in clients_table_vm.WSDL_DATA_ADDING:
            current_log_lines = log_checker.get_line_count()
            wsdl_url = wsdl_data[0].format(management_wsdl_url, cs_host)
            error = wsdl_data[1]
            error_message = wsdl_data[2]
            error_message_label = wsdl_data[3]
            whitespaces = wsdl_data[4]

            '''Generate long inputs'''
            long_wsdl_url = wsdl_url.split('#')
            try:
                if long_wsdl_url[1] == '255':
                    multiplier = int(long_wsdl_url[1]) - len(long_wsdl_url[0]) - len(long_wsdl_url[2])
                    wsdl_url = long_wsdl_url[0] + multiplier * 'A' + long_wsdl_url[2]
                elif long_wsdl_url[1] == '256':
                    multiplier = int(long_wsdl_url[1]) - len(long_wsdl_url[0]) - len(long_wsdl_url[2])
                    wsdl_url = long_wsdl_url[0] + multiplier * 'A' + long_wsdl_url[2]
            except:
                pass

            self.log('Test-' + str(counter) + '. WSDL URL == "' + wsdl_url + '"')

            self.log("Open client details")
            client_row.find_element_by_css_selector(DETAILS_TAB_CSS).click()

            '''SERVICE 08 / 1 SS administrator selects to add a WSDL.'''
            '''SERVICE 08 / 2 SS administrator inserts the URL of the WSDL.'''
            add_wsdl_url(self, wsdl_url)

            '''SERVICE 21 / 2 System parses the user input'''
            '''Check for the error messages'''
            error_messages(self, error, error_message, error_message_label)

            self.wait_jquery()
            if error:
                '''SERVICE 08/3a.2 System logs the event "Add WSDL failed" to the audit log.'''
                expected_log_msg = ADD_WSDL_FAILED
                self.log('SERVICE_08 3a.2 System logs the event "{0}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg,
                                                   from_line=current_log_lines + 1)
                self.is_true(logs_found, msg='{0} not found in audit log'.format(expected_log_msg))
                self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_CANCEL_BTN_XPATH).click()
            else:
                '''SERVICE 11 2. System verifies that mandatory fields are filled.'''
                self.log('''SERVICE 11 2. System verifies that mandatory fields are filled.''')
                '''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.'''
                self.log('''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.''')
                '''Verify that the added WSDL URL exists'''
                self.log('Find added WSDL URL row number - ' + wsdl_url)
                found_wsdl_url = self.wait_until_visible(type=By.CSS_SELECTOR,
                                                         element=popups.CLIENT_DETAILS_POPUP_WSDL_CSS)
                found_wsdl_url = found_wsdl_url.text
                if whitespaces:
                    '''SERVICE 11 1. System removes leading and trailing whitespaces.'''
                    self.log('''SERVICE 11 1. System removes leading and trailing whitespaces.''')
                    find_text_with_whitespaces(self, wsdl_url, found_wsdl_url)
                else:
                    assert wsdl_url in found_wsdl_url
                    self.log('Found WSDL URL - ' + found_wsdl_url)

            self.log('Click on "CLOSE" button')
            self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(member_code,
                                                                                         subsystem_code))
        self.log('Delete added client')
        delete_added_client(self, client_row)
        counter += 1

    return test_case


def parse_user_selection(self, element, start_nr):
    """
    Verify user selections
    :param self: MainController object
    :param element: webelement
    :param start_nr: int
    :return:
    """

    self.log('SS 41/1 System removes leading and trailing whitespaces.')
    self.log('SS 41/2 System verifies that mandatory fields are filled.')
    self.log('SS 41/3 System verifies that the user input does not exceed 255 characters.')
    element_exists = True
    while element_exists:
        try:
            self.wait_jquery()
            element_text = self.by_xpath(keyscertificates_constants.get_csr_data(element, start_nr))
            element_text = element_text.text
            element_without_whitespaces = element_text.strip()

            if element_text == '' or len(element_text) > 265 or len(element_text) != len(element_without_whitespaces):
                condition = False
            else:
                condition = True
            element_exists = True
            self.log('Selected text (string length = {0})- {1}'.format(len(element_text), element_text))
        except:
            element_exists = False
            break

        assert condition is True
        start_nr += 1


def error_messages(self, error, error_message, error_message_label):
    """
    Function Check for the error messages
    :param self: MainController object
    :param error: bool - Must there be a error message, True if there is and False if not
    :param error_message: str - Expected error message
    :param error_message_label: str - label for a expected error message
    :return:
    """
    if error:
        '''System displays the error message'''
        '''Get a error message, compare it with expected error message and close error message'''
        self.log('Get the error message')
        self.wait_jquery()
        get_error_message = messages.get_error_message(self)
        self.log('Found error message - {}'.format(get_error_message))
        self.log('Expected error message  - {}'.format(error_message.format(error_message_label)))

        self.log('Compare error message to the expected error message')
        assert get_error_message in error_message.format(error_message_label)

        self.log('Close the error message')
        messages.close_error_messages(self)
    else:
        '''Verify that there is not error messages'''
        self.log('Verify that there is not error messages')
        get_error_message = messages.get_error_message(self)
        if get_error_message is None:
            error = False
        else:
            error = True
        assert error is False


def find_text_with_whitespaces(self, added_text, expected_text):
    """
    Verifies, that there is not inputs with whitespaces
    :param self: MainController object
    :param added_text: str - added text
    :param expected_text: str - expected text
    :return: None
    """
    try:
        '''Compare added text and displayed text'''
        self.log('Compare added text and displayed text')
        self.log("'" + added_text + "' is not in '" + expected_text + "'")
        assert added_text in expected_text
        whitespace = True
    except:
        '''Compare added text without whitespaces and displayed text'''
        self.log('Compare added text without whitespaces and displayed text')
        self.log("'" + added_text.strip() + "' is in'" + expected_text + "'")
        assert added_text.strip() in expected_text
        whitespace = False
    assert whitespace is False


def add_key_label(self, key_label):
    """
    Add central key label
    :param self: MainController object
    :param key_label: str - key label
    :return:
    """
    '''SS 28/1 SS administrator selects to generate a key on a security token.'''
    self.log('SS 28/1 SS administrator selects to generate a key on a security token.')
    self.wait_jquery()
    self.log('Click on softtoken row')
    time.sleep(3)
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_ROW_XPATH).click()
    self.log('Click on "Generate key" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATEKEY_BTN_ID).click()
    '''SS 28/2 System prompts for the label of the key.'''
    self.log('SS 28/2 System prompts for the label of the key.')

    '''SS 28/3 SS administrator inserts the label value (not required, may be left blank).'''
    self.log('SS 28/3 SS administrator inserts the label value (not required, may be left blank).')
    self.log('Insert (string length = {0}) - {1} - to "LABEL" area'.format(len(key_label), key_label))
    key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
    self.input(key_label_input, key_label)
    self.wait_jquery()
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()


def add_cs_member(self, member_name, member_class, member_code):
    """
    Add central server member
    :param self: MainController object
    :param member_name: str - Member name
    :param member_class: str - Member class
    :param member_code: str - Member code
    :return:
    """
    '''MEMBER_10/1 CS administrator selects to add an X-Road member.'''
    self.log('''MEMBER_10/1 CS administrator selects to add an X-Road member.''')
    self.wait_jquery()
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.MEMBERS_CSS).click()

    self.wait_jquery()
    self.log('Click on"ADD" button')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()

    '''MEMBER_10 2 CS administrator inserts the name of the organization'''
    self.log('''MEMBER_10 2 CS administrator inserts the name of the organization (string length = {0}) - {1}'''
             .format(len(member_name), member_name))
    input_name = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID)
    self.input(input_name, member_name)

    '''MEMBER_10 2 CS administrator inserts the X-Road member class of the organization'''
    self.log('''MEMBER_10 2 CS administrator inserts the X-Road member class of the organization (string length = {0}) 
    - {1}'''.format(len(member_class), member_class))
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=members_table.ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    select.select_by_visible_text(member_class)

    '''MEMBER_10 2 CS administrator inserts the X-Road member code of the organization.'''
    self.log('''MEMBER_10 2 CS administrator inserts the X-Road member code of the organization. (string length = {0}) 
    - {1}'''.format(len(member_code), member_code))
    input_code = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member_code)

    self.log('Click "OK" to add member')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()


def add_ss_client(self, member_code, subsystem_code):
    """
    Add security server client
    :param self: MainController object
    :param member_code: str
    :param subsystem_code: str
    :return:
    """
    '''Add a client'''
    self.log('Click on "ADD CLIENT" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

    '''MEMBER_47/2 SS administrator inserts the X-Road identifier of the client.'''
    self.log('''MEMBER_47/2 SS administrator inserts the X-Road identifier of the client.''')
    self.log('Insert (string length = {0}) - {1} -  to  "MEMBER CODE" area'.format(len(member_code), member_code))
    input_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member_code)

    self.log(
        'Insert (string length = {0}) - {1} -  to  "SUBSYSTEM CODE" area'.format(len(subsystem_code), subsystem_code))
    subsystem_input = self.wait_until_visible(type=By.XPATH,
                                              element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_XPATH)
    self.input(subsystem_input, subsystem_code)

    self.wait_jquery()
    '''Save the client data'''
    self.log('Click on "OK" button')
    time.sleep(1.5)
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()


def add_wsdl_url(self, wsdl_url):
    """
    Add wsdl url to the client
    :param self: MainController object
    :param wsdl_url: str
    :return:
    """
    self.wait_jquery()
    self.log("Open 'Services' tab")
    self.wait_until_visible(type=By.XPATH, element=clients_table_vm.SERVICES_TAB_XPATH).click()
    self.log('Click on "Add WSDL" button')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ADD_WSDL_BTN_ID).click()
    self.log('Enter WSDL URL - ' + wsdl_url)
    wsdl_url_element = self.wait_until_visible(type=By.ID, element=popups.ADD_WSDL_POPUP_URL_ID)
    self.input(wsdl_url_element, wsdl_url)
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()



def get_provider_parameters(self):
    '''Get provider class and code fromm config.ini'''
    central_service_provider_2_id = self.config.get('ss1.management_id')
    central_service_provider_2_id = central_service_provider_2_id.split(' : ')
    provider_code = central_service_provider_2_id[2]
    provider_class = central_service_provider_2_id[1]

    self.wait_jquery()
    '''Open central services'''
    self.log('Open MEMBERS tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.MEMBERS_CSS).click()

    self.wait_jquery()
    self.log('Click member name - ' + provider_code + ' - in members table')
    self.wait_until_visible(type=By.XPATH,
                            element=members_table.get_member_data_from_table(3, provider_code)).click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.log('Click on "Used servers" tab')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.USED_SERVERS_TAB).click()
    self.wait_jquery()

    provider_subsystem = self.by_xpath(members_table.get_member_used_servers(1, 2))
    provider_subsystem = provider_subsystem.text

    code = self.by_xpath(members_table.get_member_used_servers(1, 3))
    code = code.text
    provider_name = code
    self.log('Click on "Used servers" tab')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH) \
        .click()
    return [provider_code, provider_class, provider_subsystem, code, provider_name]


def add_central_service(self, cs_code, code, version, provider_name, provider_code, provider_class, provider_subsystem):
    """
    Add central service
    :param self: MainController object
    :param cs_code: str
    :param code: str
    :param version: str
    :param provider_name: str
    :param provider_code: str
    :param provider_class: str
    :param provider_subsystem: str
    :return: None
    """

    '''SERVICE_41/1 CS administrator selects to add a central service.'''
    self.log('Click "ADD" to add new central service')
    self.wait_until_visible(type=By.ID, element=central_services.SERVICE_ADD_BUTTON_ID).click()

    '''SERVICE_41/2 CS administrator inserts the following information'''
    self.log('Add central service code (string length = {0}) - {1}'.format(len(cs_code), cs_code))
    self.wait_jquery()
    cs_code_input = self.wait_until_visible(type=By.ID,
                                            element=popups.CENTRAL_SERVICE_POPUP_CENTRAL_SERVICE_CODE_ID)
    self.input(cs_code_input, cs_code)

    '''Add code'''
    self.log('Add  code (string length = {0}) - {1}'.format(len(code), code))
    self.wait_jquery()
    code_input = self.wait_until_visible(type=By.ID,
                                         element=popups.CENTRAL_SERVICE_POPUP_TARGET_CODE_ID)
    self.input(code_input, code)

    '''Add version'''
    self.log('Add  version (string length = {0}) - {1}'.format(len(version), version))
    self.wait_jquery()
    version_input = self.wait_until_visible(type=By.ID,
                                            element=popups.CENTRAL_SERVICE_POPUP_TARGET_VERSION_ID)
    self.input(version_input, version)

    '''Add provider name'''
    self.log('Add  provider name (string length = {0}) - {1}'.format(len(provider_name), provider_name))
    self.wait_jquery()
    provider_name_input = self.wait_until_visible(type=By.ID,
                                                  element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_ID)
    self.input(provider_name_input, provider_name)

    '''Add provider code'''
    self.log('Add  provider code (string length = {0}) - {1}'.format(len(provider_code), provider_code))
    self.wait_jquery()
    provider_code_input = self.wait_until_visible(type=By.ID,
                                                  element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CODE_ID)
    self.input(provider_code_input, provider_code)

    '''Add provider class'''
    self.log('Select ' + provider_class + ' from "class" dropdown')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CLASS_ID))
    select.select_by_visible_text(provider_class)

    '''Add provider subsystem'''
    self.log('Add  provider subsystem (string length = {0}) - {1}'.format(len(provider_subsystem), provider_subsystem))
    self.wait_jquery()
    provider_subsystem_input = self.wait_until_visible(type=By.ID,
                                                       element=popups.
                                                       CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_SUBSYSTEM_ID)
    self.input(provider_subsystem_input, provider_subsystem)

    '''Click on 'OK' button'''
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID).click()


def delete_added_member(self, member_name):
    """
    Delete the member row from the list.
    :param self: MainController object
    :param member_name: str - member name
    :return: None
    """
    self.wait_jquery()
    self.log('Click member name - ' + member_name + ' - in members table')
    self.wait_until_visible(type=By.XPATH, element=members_table.get_member_data_from_table(1, member_name)).click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.log('Click on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DELETE_CONFIRM_BTN_ID).click()


def delete_added_client(self, client_row):
    """
    Delete the client row from the list.
    :param self: MainController object
    :param client: str - client id:
    :return: None
    """
    self.log('''Delete added client''')
    self.log("Open client details")
    client_row.find_element_by_css_selector(DETAILS_TAB_CSS).click()
    try:
        self.log('Click on "UNREGISTER" button')
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)
    except:
        self.log('Click on "DELETE" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)


def delete_added_key_label(self):
    """
    Delete the key row from the list.
    :param self: MainController object
    :return: None
    """
    self.log('Delete added key')
    self.wait_jquery()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()
    self.log('Click on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()
    self.log('Added key is deleted')


def parse_key_label_inputs(self):
    """
    SS_28_4 System verifies entered key label
    :param self: MainController object
    :return: None
    """

    ss_2_ssh_host = self.config.get('ss2.ssh_host')
    ss_2_ssh_user = self.config.get('ss2.ssh_user')
    ss_2_ssh_pass = self.config.get('ss2.ssh_pass')

    '''Open the keys and certificates tab'''
    self.log('Open keys and certificates tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()

    '''Loop through different key label names and expected results'''
    counter = 1
    log_checker = auditchecker.AuditChecker(host=ss_2_ssh_host, username=ss_2_ssh_user, password=ss_2_ssh_pass)
    for key_name in keyscertificates_constants.KEY_LABEL_TEXT_AND_RESULTS:
        current_log_lines = log_checker.get_line_count()

        input_text = key_name[0]
        error = key_name[1]
        error_message = key_name[2]
        error_message_label = key_name[3]
        whitespaces = key_name[4]

        self.log('TEST-{0}'.format(str(counter)))

        '''SS 28/1 SS administrator selects to generate a key on a security token.'''
        add_key_label(self, input_text)

        if len(input_text) > 255:
            '''SS 41 3a. The user input exceeds 255 characters.'''
            self.log('''SS 41 3a. The user input exceeds 255 characters.''')
            '''SS 41 3a1. Use case terminates with the error message "Parameter "X" input exceeds 255 characters"
            (where "X" is the name of the parameter).'''
            self.log('''SS 41 3a1. Use case terminates with the error message "Parameter "X" input exceeds 255 characters" 
            (where "X" is the name of the parameter).''')

        '''Verify error messages'''
        error_messages(self, error, error_message, error_message_label)

        if error:
            expected_log_msg = GENERATE_KEY_FAILED
            self.log('SS_28 4a.2 System logs the event "{0}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found, msg="Key generation failed not found in audit log")
            '''SS 28 3a. SS administrator cancels the key generation. Use case terminates.'''
            self.log('Click on "Cancel" button')
            self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_CANCEL_BTN_XPATH).click()
        else:
            '''SS 41 2. System verifies that mandatory fields are filled.'''
            self.log('''SS 41 2. System verifies that mandatory fields are filled.''')
            '''SS 41 3. System verifies that the user input does not exceed 255 characters.'''
            self.log('''SS 41 3. System verifies that the user input does not exceed 255 characters.''')

            self.log('Find entered key label name')
            key_label_name = self.wait_until_visible(type=By.XPATH,
                                                     element=keyscertificates_constants.
                                                     get_text(input_text.strip()))
            key_label_name = key_label_name.text

            if input_text == '':
                '''Verify that added key label can be empty and system generates kay label name'''
                self.log('Find generated key label name')
                self.wait_jquery()
                unsaved_key_names = self.wait_until_visible(type=By.XPATH, element='//tr[contains(@class, "unsaved")]',
                                                            multiple=True)
                generated_key_name = False
                for key_name_hash in unsaved_key_names:
                    key_name_hash = key_name_hash.text.encode('utf-8').split()
                    key_name_hash = key_name_hash[1]

                    self.log('Generated key label name - ' + key_name_hash)
                    '''Verify that system generates key label name'''
                    reg_ex = r'^[A-Z0-9]*'
                    rex_ex_compare = re.findall(reg_ex, key_name_hash)
                    try:
                        if len(key_name_hash) == 40 and key_name_hash == rex_ex_compare[0]:
                            generated_key_name = True
                            break
                    except:
                        generated_key_name = False

                assert generated_key_name is True

            elif whitespaces:
                '''SS 41 1. System removes leading and trailing whitespaces.'''
                self.log('''SS 41 1. System removes leading and trailing whitespaces.''')
                find_text_with_whitespaces(self, input_text, key_label_name)
            else:
                assert input_text in key_label_name

            '''Delete the added key label'''
            delete_added_key_label(self)
        counter += 1

    self.wait_jquery()


def parse_csr_inputs(self):
    """
    SS_29_5 System verifies entered CSR
    :param self: MainController object
    :return: None
    """

    '''Open the keys and certificates tab'''
    self.log('Open keys and certificates tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
    time.sleep(5)

    '''Generate key from softtoken'''
    add_key_label(self, keyscertificates_constants.KEY_LABEL_TEXT)

    '''SS 29/1 SS administrator selects to generate a certificate signing request for a key.'''
    self.log('''SS 29/1 SS administrator selects to generate a certificate signing request for a key.''')
    self.log('Click on "GENERATE CSR" button')
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATECSR_BTN_ID).click()

    '''Verify user selections'''
    self.log('Verify Usage: selections')
    parse_user_selection(self, keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_USAGE_DROPDOWN_ID, 1)
    self.log('Verify Client: selections')
    parse_user_selection(self, keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CLIENT_DROPDOWN_ID, 1)
    self.log('Verify Certification Service: selections')
    parse_user_selection(self, keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID, 2)
    self.log('Verify CSR Format: selections')
    parse_user_selection(self, keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID, 1)

    '''SS 29/4b SS administrator cancels the generation of the CSR. Use case terminates.'''
    self.log('''SS 29/4b SS administrator cancels the generation of the CSR. Use case terminates.''')
    self.log('Click on "CANCEL" button')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_CANCEL_BTN_XPATH).click()

    '''Delete the added key label'''
    delete_added_key_label(self)


def enter_global_group(self, code, description):
    """
    :param self: MainController object
    :param code: str - Group code
    :param description: str - Group description
    :return:
    """
    self.wait_jquery()
    '''SERVICE_32/1 CS administrator selects to add a global group.'''
    self.log('Click "ADD" to add new group')
    self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).click()

    '''SERVICE_32/2 CS administrator inserts the code and description of the group.'''
    self.log('Insert (string length = {0}) - {1} - to code area input'.format(len(code), code))
    group_code_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_CODE_AREA_ID)
    self.input(group_code_input, code)
    self.log('Insert (string length = {0}) - {1} - to code description input'.format(len(description), description))
    group_description_input = self.wait_until_visible(type=By.ID, element=groups_table.
                                                      GROUP_DESCRIPTION_AREA_ID)
    self.input(group_description_input, description)

    self.log('Click on "OK" to add new group')
    self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()


def delete_global_group(self, code):
    """
    :param self: MainController object
    :param code: str - Group code
    :return:
    """
    '''Delete added global group'''
    self.log('Delete added global group')
    self.log('Click on added global group row')
    self.wait_until_visible(type=By.XPATH, element=groups_table.
                            get_clobal_group_code_description_by_text(code.strip())).click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID,
                            element=groups_table.GROUP_DETAILS_BTN_ID).click()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH,
                            element=groups_table.DELETE_GROUP_BTN_ID).click()
    self.log('Click on "CONFIRM" button')
    popups.confirm_dialog_click(self)


def parse_global_groups_inputs(self):
    """
    SERVICE_32 step 3 System verifies global groups inputs in the central server
    :param self: MainController object
    :return: None
    """

    '''Open Global Groups tab'''
    self.wait_jquery()
    self.log('Open Global Groups tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.GLOBAL_GROUPS_CSS).click()
    self.wait_jquery()

    '''Loop through data from the groups_table.py'''
    counter = 1
    for group_data in groups_table.GROUP_DATA:
        '''Set necessary parameters'''
        code = group_data[0]
        description = group_data[1]
        error = group_data[2]
        error_message = group_data[3]
        error_message_label = group_data[4]
        whitespaces = group_data[5]

        self.log('TEST - {0}'.format(counter))
        '''Start adding new group'''
        enter_global_group(self, code, description)

        '''Verify error messages'''
        error_messages(self, error, error_message, error_message_label)

        if error:
            '''SERVICE_32/3a.3a CS administrator selects to terminate the use case.'''
            self.log('Click on "Cancel" button')
            self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_CANCEL_BTN_XPATH).click()
            self.wait_jquery()
        else:
            '''SERVICE 11 2. System verifies that mandatory fields are filled.'''
            self.log('''SERVICE 11 2. System verifies that mandatory fields are filled.''')
            '''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.'''
            self.log('''SERVICE 11 3. System verifies that the user input does not exceed 255 characters.''')
            '''Verify that the added member name exists in the member table'''
            self.log('Find added code text - ' + code.strip())
            global_croup_code = self.wait_until_visible(type=By.XPATH,
                                                        element=groups_table.
                                                        get_clobal_group_code_description_by_text(code.strip()))
            global_croup_code = global_croup_code.text

            self.log('Find added description text - ' + description.strip())
            global_croup_description = self.wait_until_visible(type=By.XPATH,
                                                               element=groups_table.
                                                               get_clobal_group_code_description_by_text(
                                                                   description.strip()))
            global_croup_description = global_croup_description.text
            self.log('Found global group code - ' + code)
            self.log('Found global group description - ' + description)

            if whitespaces:
                '''SERVICE_11 1. System removes leading and trailing whitespaces.'''
                self.log('''SERVICE 11 1. System removes leading and trailing whitespaces.''')
                find_text_with_whitespaces(self, code, global_croup_code)
                find_text_with_whitespaces(self, description, global_croup_description)
            else:
                assert code in global_croup_code
                assert description in global_croup_description

            '''Delete added global group'''
            delete_global_group(self, code)

        counter += 1
