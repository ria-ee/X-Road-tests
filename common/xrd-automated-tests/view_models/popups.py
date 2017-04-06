from selenium.webdriver.common.by import By

GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID = 'label'

FILE_UPLOAD_BROWSE_BUTTON_ID = 'file_upload_button'
FILE_UPLOAD_SUBMIT_BUTTON_ID = 'file_upload_submit'

GENERATE_KEY_POPUP = '//div[@aria-describedby="generate_key_dialog"]'
GENERATE_KEY_POPUP_OK_BTN_XPATH = GENERATE_KEY_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
GENERATE_KEY_POPUP_CANCEL_BTN_XPATH = GENERATE_KEY_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="CANCEL"]'

CONFIRM_POPUP = '//div[@aria-describedby="confirm"]'
CONFIRM_POPUP_OK_BTN_XPATH = CONFIRM_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Confirm"]'
CONFIRM_POPUP_CANCEL_BTN_XPATH = CONFIRM_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'
CONFIRM_POPUP_TEXT_AREA_ID = 'confirm'

ALL_OPEN_POPUPS_CSS = '.ui-dialog:not([style*="display: none"])'
POPUP_HEADER_CLOSE_BUTTON_CSS = 'button.ui-action-close'

CLIENT_DETAILS_POPUP = '//div[@aria-describedby="client_details_dialog"]'
CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID = 'services'
CLIENT_DETAILS_POPUP_WSDL_CSS = '#services .wsdl'
CLIENT_DETAILS_POPUP_SERVICE_ROWS_CSS = '#services tbody tr'
CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS = '.closed'
CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID = 'service_params'
CLIENT_DETAILS_POPUP_ADD_WSDL_BTN_ID = 'wsdl_add'
CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID = 'wsdl_enable'
CLIENT_DETAILS_POPUP_DISABLE_WSDL_BTN_ID = 'wsdl_disable'
CLIENT_DETAILS_POPUP_DELETE_WSDL_BTN_ID = 'wsdl_delete'
CLIENT_DETAILS_POPUP_REFRESH_WSDL_BTN_ID = 'wsdl_refresh'
CLIENT_DETAILS_POPUP_SERVICES_TABLE_CONTENT_CSS = 'tbody tr.service'
CLIENT_DETAILS_POPUP_SERVICE_CODE_REGEX = '^(([^.]+)\.([^ ]+)) \(([0-9]+)\)$'
CLIENT_DETAILS_POPUP_ACCESS_RIGHTS_BTN_ID = 'service_acl'
CLIENT_DETAILS_POPUP_ACL_SUBJECTS_ADD_BTN_ID = 'acl_subjects_add'
CLIENT_DETAILS_POPUP_ACL_SUBJECTS_REMOVE_SELECTED_BTN_ID = 'service_acl_subjects_remove_selected'
CLIENT_DETAILS_POPUP_ACL_SUBJECTS_REMOVE_ALL_BTN_ID = 'service_acl_subjects_remove_all'
CLIENT_DETAILS_POPUP_ACL_SUBJECTS_OPEN_CLIENTS_SERVICES_ID = 'acl_subject_open_services'
CLIENT_DETAILS_POPUP_ACL_SUBJECTS_TABLE_ID = 'acl_subjects'
CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_TABLE_ID = 'subjects'
CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_XROAD_ID_ELEMENTS_CSS = '#subjects tbody tr span.xroad-id'
CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_FIRST_SUBJECT_ROW_CSS = '#subjects tbody tr'
CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_ADD_SUBJECTS_BTN_CSS = 'service_acl_subjects_add'
CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID = 'client_delete'
CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID = 'client_unregister'
CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_CONNECTION_TYPE_ID = 'connection_type'
CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_CONNECTION_TYPE_SAVE_BTN_ID = 'internal_connection_type_edit'
CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_ADD_CERTIFICATE_BTN_ID = 'internal_cert_add'
CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_DELETE_CERTIFICATE_BTN_ID = 'internal_cert_delete'
CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_TLS_CERTS_CSS = '#internal_certs tbody td'
CLIENT_DETAILS_POPUP_WSDL_REGEX = 'WSDL( DISABLED|) \({0}\)$'  # {0} is replaced with WSDL URL
CLIENT_DETAILS_POPUP_WSDL_URL_REGEX = 'WSDL( DISABLED|) \((.*)\)$'  # {0} is replaced with WSDL URL
CLIENT_DETAILS_POPUP_CLIENT_ID_XPATH = '//div[@data-name="client_details_dialog"]//*[@class="xroad-id"]'
CLIENT_DETAILS_POPUP_GROUP_ADD_BTN_ID = 'group_add'

CENTRAL_SERVICE_POPUP = '//div[@aria-describedby="central_service_details_dialog"]'
CENTRAL_SERVICE_POPUP_CENTRAL_SERVICE_CODE_ID = 'central_service_details_service_code'
CENTRAL_SERVICE_POPUP_TARGET_CODE_ID = 'central_service_details_target_code'
CENTRAL_SERVICE_POPUP_TARGET_VERSION_ID = 'central_service_details_service_version'
CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_ID = 'central_service_details_target_provider_name'
CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CODE_ID = 'central_service_details_target_provider_code'
CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CLASS_ID = 'central_service_details_target_provider_class'
CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_SUBSYSTEM_ID = 'central_service_details_target_provider_subsystem'
# CENTRAL_SERVICE_POPUP_SEARCH_BUTTON_ID = 'central_service_details_search_provider'
CENTRAL_SERVICE_POPUP_OK_BUTTON_ID = 'central_service_save_ok'

GROUP_ADD_POPUP_XPATH = '//div[@data-name="group_add_dialog"]'
GROUP_ADD_POPUP_CODE_AREA_ID = 'add_group_code'
GROUP_ADD_POPUP_CODE_DESCRIPTION_ID = 'add_group_description'
GROUP_ADD_POPUP_OK_BTN_XPATH = GROUP_ADD_POPUP_XPATH + '//button[@data-name="ok"]'

ADD_WSDL_POPUP_XPATH = '//div[@data-name="wsdl_add_dialog"]'
ADD_WSDL_POPUP_URL_ID = 'wsdl_add_url'
ADD_WSDL_POPUP_CANCEL_BTN_XPATH = ADD_WSDL_POPUP_XPATH + '//button[@data-name="cancel"]'
ADD_WSDL_POPUP_OK_BTN_XPATH = ADD_WSDL_POPUP_XPATH + '//button[@data-name="ok"]'

EDIT_WSDL_POPUP_XPATH = '//div[@data-name="wsdl_params_dialog"]'
EDIT_WSDL_POPUP_URL_ID = 'params_wsdl_url'
EDIT_WSDL_POPUP_CANCEL_BTN_XPATH = EDIT_WSDL_POPUP_XPATH + '//button[@data-name="cancel"]'
EDIT_WSDL_POPUP_OK_BTN_XPATH = EDIT_WSDL_POPUP_XPATH + '//button[@data-name="ok"]'

DISABLE_WSDL_POPUP_XPATH = '//div[@data-name="wsdl_disable_dialog"]'
DISABLE_WSDL_POPUP_NOTICE_ID = 'wsdl_disabled_notice'
DISABLE_WSDL_POPUP_CANCEL_BTN_XPATH = DISABLE_WSDL_POPUP_XPATH + '//button[@data-name="cancel"]'
DISABLE_WSDL_POPUP_OK_BTN_XPATH = DISABLE_WSDL_POPUP_XPATH + '//button[@data-name="ok"]'

EDIT_SERVICE_POPUP_XPATH = '//div[@data-name="service_params_dialog"]'
EDIT_SERVICE_POPUP_URL_ID = 'params_url'
EDIT_SERVICE_POPUP_TIMEOUT_ID = 'params_timeout'
EDIT_SERVICE_POPUP_TLS_ID = 'params_sslauth'
EDIT_SERVICE_POPUP_TLS_ENABLED_XPATH = '//input[@id="params_sslauth" and not(@disabled)]'
EDIT_SERVICE_POPUP_CANCEL_BTN_XPATH = EDIT_SERVICE_POPUP_XPATH + '//button[@data-name="cancel"]'
EDIT_SERVICE_POPUP_OK_BTN_XPATH = EDIT_SERVICE_POPUP_XPATH + '//button[@data-name="ok"]'

ACL_SUBJECTS_SEARCH_POPUP = '//div[@aria-describedby="acl_subjects_search_dialog"]'
ACL_SUBJECTS_SEARCH_POPUP_SEARCH_BTN_CSS = '#acl_subjects_search_simple_search_tab .search'
ACL_SUBJECTS_SEARCH_POPUP_SEARCH_SUBJECTS_TABLE = '#acl_subjects_search tbody'
ACL_SUBJECTS_SEARCH_POPUP_SEARCH_SUBJECTS_SELECTABLE_TABLE = '#acl_subjects_search tbody tr.selectable'
ACL_SUBJECTS_SEARCH_POPUP_NEXT_BTN_ID = 'acl_subjects_search_next'
ACL_SUBJECTS_SEARCH_POPUP_CLOSE_BTN_XPATH = ACL_SUBJECTS_SEARCH_POPUP + '//button[contains(@class, "ui-action-close")]'
ACL_SUBJECTS_SEARCH_POPUP_RESULTS_TABLE_ID = 'acl_subjects_search'
ACL_SUBJECTS_SEARCH_POPUP_ADD_SELECTED_TO_ACL_BUTTON_ID = 'acl_subjects_search_add_selected'
ACL_SUBJECTS_SEARCH_POPUP_ADD_ALL_TO_ACL_BUTTON_ID = 'acl_subjects_search_add_all'

ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP = '//div[@aria-describedby="acl_subject_open_services_add_dialog"]'
ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ALL_SERVICES_TABLE_ID = 'services_all'
ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_OPEN_SERVICES_TABLE_ID = 'services_open'
ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_SERVICES_SELECTABLE_TABLE_CSS = '#services_all tr.selectable'
ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ADD_SERVICES_BTN_ID = 'acl_subject_open_services_add'
ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ADD_ALL_TO_ACL_BTN_ID = 'acl_subject_open_services_add_all'
ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ADD_SELECTED_TO_ACL_BTN_ID = 'acl_subject_open_services_add_selected'
ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_REMOVE_ALL_SERVICES_BTN_ID = 'acl_subject_open_services_remove_all'

ACL_SUBJECT_OPEN_SERVICES_POPUP = '//div[@aria-describedby="acl_subject_open_services_dialog"]'
ACL_SUBJECT_OPEN_SERVICES_POPUP_CLOSE_SERVICES_BTN_XPATH = ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP + \
                                                           '//div[@class= "ui-dialog-buttonset"]//button[@data-name="close"]'

ADD_CLIENT_POPUP_XPATH = '//div[@aria-describedby="client_add_dialog"]'
ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID = 'add_member_class'
ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID = 'add_member_code'
ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_CSS = '#client_add_dialog #add_subsystem_code'
ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_ID = 'add_subsystem_code'
ADD_CLIENT_POPUP_OK_BTN_XPATH = ADD_CLIENT_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'

WARNING_POPUP = '//div[@aria-describedby="warning"]'
WARNING_POPUP_CONTINUE_XPATH = WARNING_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Continue"]'
WARNING_POPUP_CANCEL_XPATH = WARNING_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'

XROAD_ID_BY_INDEX_XPATH = '(.//span[@class="xroad-id"])[{0}]'  # Needs to be used with .format(index_string)
XROAD_ID_BY_NAME_XPATH = u'.//span[@class="xroad-id"][text()="{0}"]'  # Needs to be used with .format(xroad_id)
XROAD_ID_SELECTABLE_ROW_CSS = 'tr.selectable span.xroad-id'

CONSOLE_OUTPUT_DIALOG_XPATH = '//div[@aria-describedby="console_output_dialog"]'
CONSOLE_OUTPUT_DIALOG_TEXT_CSS = '#command_console_output'
CONSOLE_OUTPUT_DIALOG_OK_BTN_XPATH = CONSOLE_OUTPUT_DIALOG_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'

YESNO_POPUP_XPATH = '//div[@aria-describedby="yesno"]'
YESNO_POPUP_YES_BTN_XPATH = YESNO_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="Yes"]'
YESNO_POPUP_NO_BTN_XPATH = YESNO_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="No"]'

FILE_UPLOAD_ID = 'file_upload_button'


def confirm_dialog_click(self):
    # A dialog box should open. Wait until the button "Confirm" is visible, then click it.
    confirm_button = self.wait_until_visible('button#confirm', type=By.CSS_SELECTOR)
    confirm_button.click()
    self.wait_jquery()


def yes_dialog_click(self):
    # A dialog box should open. Wait until the button "Confirm" is visible, then click it.
    self.wait_until_visible(type=By.XPATH, element=YESNO_POPUP_YES_BTN_XPATH).click()


def no_dialog_click(self):
    # A dialog box should open. Wait until the button "Confirm" is visible, then click it.
    self.wait_until_visible(type=By.XPATH, element=YESNO_POPUP_NO_BTN_XPATH).click()


def open_client_search_list_from_acl_subjects_popup(self):
    print 'Open add new services to subjects dialog'
    # Wait for the element and click
    self.wait_until_visible(type=By.ID, element=CLIENT_DETAILS_POPUP_ACL_SUBJECTS_ADD_BTN_ID).click()
    self.wait_jquery()
    print 'Click on search'
    # Wait for the element and click
    self.wait_until_visible(type=By.CSS_SELECTOR, element=ACL_SUBJECTS_SEARCH_POPUP_SEARCH_BTN_CSS).click()
    print 'Waiting on clients table to load'
    # Waiting for searched list to appear
    self.wait_jquery()
    table = self.wait_until_visible(type=By.CSS_SELECTOR,
                                    element=ACL_SUBJECTS_SEARCH_POPUP_SEARCH_SUBJECTS_SELECTABLE_TABLE)
    return table


# Add services to clients tests helper methods

def select_rows_from_services_table(table, rows_to_select):
    """

    :param table: table to select rows from
    :param rows_to_select: list of rows to select or 0 for selecting all rows
    :return: list of open services. Rows' first td element text
    """
    is_click = True
    rows_selected = []
    selectable_rows = table.find_elements(By.CLASS_NAME, "selectable")
    rows = table.find_elements(By.TAG_NAME, "tr")
    if rows_to_select == 0:
        is_click = False
        rows_to_select = list(range(1, len(rows)))
    for row in rows_to_select:
        if row > 0 & row < len(rows):
            row_to_select = rows[row]
            if row_to_select in selectable_rows:
                rows_selected.append(row_to_select.find_element(By.TAG_NAME, 'td').text)
            if is_click:
                row_to_select.click()
    return rows_selected


def open_services_table_rows(self):
    """

    :param self: MainController class object
    :return: list of open services. Rows' first td element text
    """
    self.wait_jquery()
    open_services_table = self.wait_until_visible(type=By.ID,
                                                  element=ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_OPEN_SERVICES_TABLE_ID)
    open_rows_codes = []
    for row in open_services_table.find_elements(By.CSS_SELECTOR, "tbody tr"):
        open_rows_codes.append(row.find_element(By.TAG_NAME, 'td').text)
    return open_rows_codes


def close_console_output_dialog(self):
    ok_button = self.by_xpath(CONSOLE_OUTPUT_DIALOG_OK_BTN_XPATH)
    if ok_button.is_displayed():
        ok_button.click()


def close_all_open_dialogs(self):
    """

    Closes all open dialogs by searching for non-hidden ones, sorting the by z-index and clicking the "X" button in
    dialog header.

    :param self:
    :return:
    """
    # Find all open dialogs
    open_dialogs = self.by_css(ALL_OPEN_POPUPS_CSS, multiple=True)
    dialogs = []

    # Add the dialogs to a list of objects with their z-index
    for dialog in open_dialogs:
        z_index = int(dialog.value_of_css_property('z-index'))
        dialogs.append({'z-index': z_index, 'dialog': dialog})

    # Sort the dialogs by z-index (highest to lowest)
    dialogs.sort(key=lambda k: k['z-index'], reverse=True)

    # Start from the topmost (highest z-index) dialog and close it, keep going until the last visible dialog has been
    # closed.
    for data in dialogs:
        dialog = data['dialog']
        # Find the close button ("X") and click it.
        close_button = dialog.find_element_by_css_selector(POPUP_HEADER_CLOSE_BUTTON_CSS)
        close_button.click()
