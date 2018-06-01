# coding=utf-8
import time
from collections import Counter

from selenium.webdriver.common.by import By

from helpers import xroad, ssh_client, auditchecker
from tests.xroad_cs_ca import ca_management
from tests.xroad_cs_ca.ca_management import edit_ca_settings
from tests.xroad_ss_client_certification_213 import client_certification as client_certification
from view_models import popups, messages, sidebar, certification_services, log_constants
from view_models.certification_services import OCSP_RESPONSE_TAB, get_ocsp_by_td_text
from view_models.sidebar import CERTIFICATION_SERVICES_CSS


def open_ocsp_responders(self):
    '''
    Selects the OCSP responders tab in CA settings dialog.
    :param self: MainController object
    :return: None
    '''
    # Open the "OCSP responders" tab
    self.by_xpath(certification_services.OCSP_RESPONSE_TAB).click()
    self.wait_jquery()


def select_ocsp_responder(self, ocsp_url):
    '''
    Finds and selects an OCSP responder from the list of responders. If not found, raises an AssertionError.
    :param self: MainController object
    :param ocsp_url: str - OCSP responder URL
    :return: None
    '''
    # Find the OCSP responder
    # ocsp_url = ocsp_url.strip('/')
    ocsp_cell = self.by_xpath(certification_services.get_ocsp_by_td_text(ocsp_url))
    self.is_not_none(ocsp_cell, msg='OCSP responder "{0}" not found in the table'.format(ocsp_url))

    # Click on the OCSP responder
    ocsp_cell.click()


def open_ocsp_responder_settings(self, ocsp_url):
    '''
    Selects an OCSP responder from the list, then opens its settings view.
    :param self: MainController object
    :param ocsp_url: str - OCSP responder URL
    :return: None
    '''
    # Select the OCSP responder from the list
    select_ocsp_responder(self, ocsp_url)

    # Click "Edit"
    self.by_id(certification_services.OCSP_RESPONDER_EDIT_BTN_ID).click()
    self.wait_jquery()


def save_ocsp_responder(self, close_errors=False):
    '''
    Tries to save OCSP responder settings.
    :param self: MainController object
    :param close_errors: bool - close error/warning messages if any are displayed
    :return: (str|None, str|None, str|None) - warning message, error message, console output if shown, None if not shown
    '''
    # Click "OK" to try to save the settings.
    self.by_xpath(certification_services.OCSP_SETTINGS_POPUP_OK_BTN_XPATH).click()

    # Clicking the button starts an ajax query. Wait until request is complete.
    self.wait_jquery()

    # Get error messages if any
    console_output = messages.get_console_output(self)  # Console message (displayed if WSDL validator gives a warning)
    warning_message = messages.get_warning_message(self)  # Warning message
    error_message = messages.get_error_message(self)  # Error message (anywhere)

    if console_output is not None:
        popups.close_console_output_dialog(self)

    # Close all error messages
    if close_errors:
        messages.close_error_messages(self)

    return warning_message, error_message, console_output


def set_ocsp_responder(self, ocsp_url):
    '''
    Tries to enter OCSP responder URL to settings dialog.
    :param self: MainController object
    :param url: str - OCSP responder URL
    :return: None
    '''

    self.log('Setting OCSP URL: {0}'.format(ocsp_url))

    url_input = self.by_id(certification_services.OCSP_RESPONDER_URL_AREA_ID)
    self.input(url_input, ocsp_url)


def set_ocsp_responder_certificate(self, certificate_filename):
    '''
    Uploads an OCSP responder certificate in OCSP responder settings dialog.
    :param self: MainController object
    :param certificate_filename: str - pathname of the certificate to upload
    :return: None
    '''
    # Import OCSP certificate
    import_cert_btn = self.wait_until_visible(type=By.ID,
                                              element=certification_services.IMPORT_OCSP_CERT_BTN_ID)

    xroad.fill_upload_input(self, import_cert_btn, certificate_filename)
    # Small delay to allow JS to react
    time.sleep(0.5)

    # Filling the upload input starts an ajax query. Wait for it to finish.
    self.wait_jquery()


def delete_ocsp_responder(self, ocsp_url):
    '''
    Deletes an OCSP responder from the responders list.
    :param self: MainController object
    :param ocsp_url: str - OCSP responder URL to delete
    :return: None
    '''
    # Select the OCSP responder from the list
    select_ocsp_responder(self, ocsp_url)

    # Click "Delete"
    self.by_id(certification_services.OCSP_RESPONDER_DELETE_BTN_ID).click()

    # Wait until the table is refreshed
    self.wait_jquery()


def configure_ocsp_responder(self, ocsp_url, certificate_filename=None, invalid_certificate_filename=None,
                             invalid_url='invalid url', check_errors=True, log_success=None,
                             log_fail=None):
    '''
    Configures an OCSP responder URL and certificate. If invalid_certificate_filename is set, first tries this one and
    checks for correct error message.
    :param self: MainController object
    :param ocsp_url: str - OCSP responder URL
    :param certificate_filename: str - pathname of the correct certificate to upload
    :param invalid_certificate_filename: str|None - pathname of the invalid certificate to upload, None to skip this
    :param invalid_url: str - invalid URL to test during configuring
    :param check_errors: bool - True to check for error scenarios, False otherwise
    :param log_success: str - audit.log message for successful configuration
    :param log_fail: str - audit.log message for unsuccessful configuration
    :return: None
    '''
    # UC TRUST_10 2 - set OCSP URL
    self.log('TRUST_10 2 - setting OCSP URL')
    set_ocsp_responder(self, ocsp_url)

    # UC TRUST_10 3 - upload certificate
    if certificate_filename is not None or invalid_certificate_filename is not None:
        self.log('TRUST_10 3 - upload certificate')

        # UC TRUST_10 4 - verify if certificate is DER/PEM
        if invalid_certificate_filename is not None:
            self.log('TRUST_10 4a - upload invalid certificate')
            set_ocsp_responder_certificate(self, invalid_certificate_filename)
            error = messages.get_error_message(self)
            self.is_not_none(error, msg='Set invalid OCSP certificate: no error shown')
            self.is_equal(error, messages.WRONG_FORMAT_OCSP_CERTIFICATE,
                          msg='Set invalid OCSP certificate: wrong error shown : {0}'.format(error))
            messages.close_error_messages(self)
        if certificate_filename is not None:
            self.log('TRUST_10 4 - upload working certificate')
            set_ocsp_responder_certificate(self, certificate_filename)
            error = messages.get_error_message(self)
            warning = messages.get_warning_message(self)
            console = messages.get_console_output(self)
            self.is_none(error, msg='Got error for valid OCSP certificate: {0}'.format(error))
            self.is_none(warning, msg='Got warning for valid OCSP certificate: {0}'.format(warning))
            self.is_none(console, msg='Got console output for valid OCSP certificate: {0}'.format(console))
            messages.close_error_messages(self)
    else:
        # UC TRUST_10 3a - skip certificate upload
        self.log('TRUST_10 3a - skipping certificate upload')

    if check_errors:
        self.log('TRUST_10 5 (parse user input), 5a (user input parsing failed), 6a (try to save malformed URL)')

        # Use SS_41 to check input parsing, finish with space-padded data
        successes, errors, final_url = check_inputs(self,
                                                    input_element=certification_services.OCSP_RESPONDER_URL_AREA_ID,
                                                    final_value=ocsp_url, label_name='url',
                                                    save_btn=certification_services.OCSP_SETTINGS_POPUP_OK_BTN_XPATH,
                                                    input_element_type=By.ID, save_btn_type=By.XPATH,
                                                    invalid_input=invalid_url)

        # Save logged error messages and successes for later checking
        self.logdata += [log_fail] * errors
        self.logdata += [log_success] * successes
    else:
        self.log('TRUST_10 6 - setting OCSP URL: {0}'.format(ocsp_url))

        # Try to save OCSP responder
        set_ocsp_responder(self, ocsp_url)
        warning, error, console = save_ocsp_responder(self)

        self.is_none(error, msg='Set OCSP responder URL: got error for URL {0}'.format(ocsp_url))
        self.is_none(warning, msg='Set OCSP responder URL: got warning for URL {0}'.format(ocsp_url))
        self.is_none(console, msg='Set OCSP responder URL: got console output for URL {0}'.format(ocsp_url))

        # Save data for checking the logs later
        self.logdata.append(log_success)


def ca_get_certificates(self, ssh_host, ssh_user, ssh_pass, filenames):
    '''
    Downloads specified certificates from the Certification Authority over an SSH connection. Files will be downloaded
    to the configured download directory.
    :param self: MainController object
    :param ssh_host: str - SSH hostname
    :param ssh_user: str - SSH username
    :param ssh_pass: str - SSH password
    :param filenames: [str] - list of filenames to download from the CA
    :return: None
    '''

    # Create SSH connection to CA
    sshclient = ssh_client.SSHClient(ssh_host, ssh_user, ssh_pass)
    # Get CA certificates using SSH
    for cert_filename in filenames:
        local_path = self.get_download_path(cert_filename)
        client_certification.get_ca_certificate(sshclient, cert_filename, local_path)

    # Close SSH connection
    sshclient.close()


def test_edit_ocsp_responder(case, ca_name, ocsp_url, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None,
                             certificate_filename=None, invalid_certificate_filename=None):
    '''
    Main test function for editing an OCSP responder (UC TRUST_10).
    :param case: MainController object
    :param ca_name: str - Certificate Authority name
    :param ocsp_url: str - OCSP responder URL
    :param cs_ssh_host: str - SSH hostname for Central Server
    :param cs_ssh_user: str - SSH username for Central Server
    :param cs_ssh_pass: str - SSH password for Central Server
    :param certificate_filename: str - pathname of the correct certificate to upload
    :param invalid_certificate_filename: str - pathname of the invalid certificate to check
    :return:
    '''
    self = case

    def edit_ocsp_responder():
        self.logdata = []

        # Only check logs if cs_ssh_host is set
        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()

        # UC TRUST_10 1 - select to edit OCSP
        self.log('UC TRUST_10 1 - select to edit OCSP responder for CA: {0}'.format(ca_name))

        # Open "Certification services"
        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        # Edit CA
        ca_management.edit_ca_settings(self, ca_name)

        # Open "OCSP responders" tab
        open_ocsp_responders(self)

        # Edit the OCSP responder
        open_ocsp_responder_settings(self, ocsp_url)

        # Configure OCSP responder settings
        configure_ocsp_responder(self, ocsp_url=ocsp_url, certificate_filename=certificate_filename,
                                 invalid_certificate_filename=invalid_certificate_filename,
                                 log_success=log_constants.EDIT_OCSP, log_fail=log_constants.EDIT_OCSP_FAILED)

        # Edit the OCSP responder
        open_ocsp_responder_settings(self, ocsp_url)

        # Configure OCSP responder settings
        configure_ocsp_responder(self, ocsp_url=ocsp_url, certificate_filename=certificate_filename,
                                 log_success=log_constants.EDIT_OCSP, log_fail=log_constants.EDIT_OCSP_FAILED,
                                 check_errors=False)

        if cs_ssh_host is not None:
            self.log('TRUST_10 5a, 6a, 8 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.found_lines))

        popups.close_all_open_dialogs(self)

    return edit_ocsp_responder


def test_add_ocsp_responder(case, ca_name, ocsp_url, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None,
                            certificate_filename=None, invalid_certificate_filename=None):
    '''
    Main test function for adding an OCSP responder (UC TRUST_10).
    :param case: MainController object
    :param ca_name: str - Certificate Authority name
    :param ocsp_url: str - OCSP responder URL
    :param cs_ssh_host: str - SSH hostname for Central Server
    :param cs_ssh_user: str - SSH username for Central Server
    :param cs_ssh_pass: str - SSH password for Central Server
    :param certificate_filename: str - pathname of the correct certificate to upload
    :param invalid_certificate_filename: str - pathname of the invalid certificate to check
    :return:
    '''
    self = case

    def add_ocsp_responder():
        self.logdata = []

        # Only check logs if cs_ssh_host is set
        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()

        # UC TRUST_10 1 - select to add OCSP
        self.log('UC TRUST_10 1 - select to add OCSP responder for CA: {0}'.format(ca_name))

        # Open "Certification services"
        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        # Edit CA
        ca_management.edit_ca_settings(self, ca_name)

        # Open "OCSP responders" tab
        open_ocsp_responders(self)

        # Click "Add"
        self.by_id(certification_services.OCSP_RESPONDER_ADD_BTN_ID).click()
        self.wait_jquery()

        # Configure OCSP responder settings
        configure_ocsp_responder(self, ocsp_url=ocsp_url, certificate_filename=certificate_filename,
                                 invalid_certificate_filename=invalid_certificate_filename,
                                 log_success=log_constants.ADD_OCSP, log_fail=log_constants.ADD_OCSP_FAILED)

        # Remove the newly added responder and then add another one without checking error scenarios
        delete_ocsp_responder(self, ocsp_url=ocsp_url)
        self.logdata.append('*')

        # Click "Add"
        self.by_id(certification_services.OCSP_RESPONDER_ADD_BTN_ID).click()
        self.wait_jquery()

        # Configure OCSP responder settings
        configure_ocsp_responder(self, ocsp_url=ocsp_url, certificate_filename=certificate_filename,
                                 log_success=log_constants.ADD_OCSP,
                                 log_fail=log_constants.ADD_OCSP_FAILED, check_errors=False)

        # Check logs for entries if cs_ssh_host is set
        if cs_ssh_host is not None:
            self.log('TRUST_10 5a, 6a, 8 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.log_output))

        popups.close_all_open_dialogs(self)

    return add_ocsp_responder


def test_delete_ocsp_responder(case, ca_name, ocsp_url, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None):
    '''
    Main test function for deleting an OCSP responder (UC TRUST_11).
    :param case: MainController object
    :param ca_name: str - Certificate Authority name
    :param ocsp_url: str - OCSP responder URL
    :param cs_ssh_host: str - SSH hostname for Central Server
    :param cs_ssh_user: str - SSH username for Central Server
    :param cs_ssh_pass: str - SSH password for Central Server
    :return:
    '''
    self = case

    def del_ocsp_responder():
        self.logdata = []

        # Only check logs if cs_ssh_host is set
        if cs_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=cs_ssh_host, username=cs_ssh_user, password=cs_ssh_pass)
            current_log_lines = log_checker.get_line_count()

        # UC TRUST_10 1 - select to add OCSP
        self.log('UC TRUST_11 1 - select to delete OCSP responder {1} for CA: {0}'.format(ca_name, ocsp_url))

        # Open "Certification services"
        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        # Edit CA
        ca_management.edit_ca_settings(self, ca_name)

        # Open "OCSP responders" tab
        open_ocsp_responders(self)

        # Get the list of current OCSP responders
        responders_initial = Counter(certification_services.get_ocsp_responders(self))

        # Remove the newly added responder and then add another one without checking error scenarios
        delete_ocsp_responder(self, ocsp_url=ocsp_url)
        self.logdata.append('Delete OCSP responder')

        # UC TRUST_11 1 - check if OCSP responder was deleted from the table
        self.log('UC TRUST_11 2 - check if OCSP responder was deleted from the table: {0}'.format(ocsp_url))

        # Get the list of OCSP responders to compare with previous ones
        responders_new = Counter(certification_services.get_ocsp_responders(self))

        # Get the difference between the initial and current OCSP responder lists
        responders_diff = list((responders_initial - responders_new).elements())

        self.not_equal(len(responders_diff), 0, msg='OCSP responder was not deleted')
        self.is_equal(len(responders_diff), 1,
                      msg='More than one OCSP responder has been deleted, diff: {0}'.format(responders_diff))
        self.is_equal(responders_diff[0], ocsp_url,
                      msg='Wrong OCSP responder was deleted: {0}'.format(responders_diff[0]))

        # Check logs for entries if cs_ssh_host is set
        if cs_ssh_host is not None:
            self.log('TRUST_11 3 - checking logs for: {0}'.format(self.logdata))
            logs_found = log_checker.check_log(self.logdata, from_line=current_log_lines + 1)
            self.is_true(logs_found,
                         msg='Some log entries were missing. Expected: "{0}", found: "{1}"'.format(self.logdata,
                                                                                                   log_checker.log_output))

        popups.close_all_open_dialogs(self)

    return del_ocsp_responder


def check_inputs(self, input_element, final_value, save_btn, label_name='label', input_element_type=By.ID,
                 save_btn_type=By.XPATH, invalid_input='invalid input'):
    '''
    Tries to enter different erroneous values to an input field and check if the error messages were correct.
    :param self: MainController object
    :param input_element: str - input element ID, XPath, or CSS selector
    :param final_value: str - correct value to be entered as a final step
    :param save_btn: str - save/OK button ID, XPath, or CSS selector
    :param label_name: str - input label internal name, used in some error messages
    :param input_element_type: By - input element selector type, default is By.ID
    :param save_btn_type: By - input element selector type, default is By.XPATH
    :param invalid_input: str - invalid input value (for classes, URLs, etc)
    :return: (int, int, str) - number of successful save attempts, number of unsuccessful save attempts, final saved value;
                                numbers are used for counting the success/failure log entries.
    '''
    error_count = 0
    success_count = 0
    URL_TEXT_AND_RESULTS = [
        [256 * 'S', messages.INPUT_DATA_TOO_LONG.format(label_name), False],
        [invalid_input, messages.INVALID_URL.format(invalid_input), True],
        [' ', messages.MISSING_PARAMETER.format(label_name), False],
        ['', True, False],
        ['   {0}   ', None, True]
    ]

    self.log('SS_28_4 System verifies entered text')

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


def test_view_ocsp_responder(self, ca_name, ocsp_url):
    def view_ocsp_responder():
        self.log('Open certification services view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=CERTIFICATION_SERVICES_CSS).click()
        self.wait_jquery()
        self.log('Open CA settings')
        edit_ca_settings(self, ca_name)
        self.log('TRUST_05 1. Open OCSP Responders tab')
        self.wait_until_visible(type=By.XPATH, element=OCSP_RESPONSE_TAB).click()
        self.wait_jquery()
        self.log('TRUST_05 2. System displays the URL({}) of the OCSP server'.format(ocsp_url))
        self.is_not_none(self.wait_until_visible(type=By.XPATH, element=get_ocsp_by_td_text(ocsp_url)))

    return view_ocsp_responder
