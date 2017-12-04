import re

from selenium.webdriver.common.by import By

GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID = 'label'

FILE_UPLOAD_BROWSE_BUTTON_ID = 'file_upload_button'
FILE_UPLOAD_SUBMIT_BUTTON_ID = 'file_upload_submit'
FILE_UPLOAD_CANCEL_BTN_XPATH = '//button[@data-name="cancel"]'

GENERATE_KEY_POPUP = '//div[@aria-describedby="generate_key_dialog"]'
GENERATE_KEY_POPUP_OK_BTN_XPATH = GENERATE_KEY_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
GENERATE_KEY_POPUP_CANCEL_BTN_XPATH = GENERATE_KEY_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'

KEY_DETAILS_POPUP = '//div[@aria-describedby="key_details_dialog"]'
KEY_DETAILS_POPUP_FRIENDLY_NAME = KEY_DETAILS_POPUP + '//input[@name="friendly_name"]'
KEY_DETAILS_TOKEN_INFO_XPATH = KEY_DETAILS_POPUP + '//div[@class="dialog-body"]//pre'
KEY_DETAILS_POPUP_POPUP_CANCEL_BTN_XPATH = KEY_DETAILS_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'
KEY_DETAILS_POPUP_POPUP_OK_BTN_XPATH = KEY_DETAILS_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'

TOKEN_DETAILS_POPUP = '//div[@aria-describedby="token_details_dialog"]'
TOKEN_DETAILS_FRIENDLY_NAME = TOKEN_DETAILS_POPUP + '//input[@name="friendly_name"]'
TOKEN_DETAILS_TOKEN_INFO_XPATH = TOKEN_DETAILS_POPUP + '//div[@class="dialog-body"]//pre'
TOKEN_DETAILS_POPUP_POPUP_CANCEL_BTN_XPATH = TOKEN_DETAILS_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'

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
CLIENT_DETAILS_POPUP_REGISTER_BUTTON_ID = 'client_register'
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
CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH = '//div[@class="ui-dialog-buttonset"]//button[span="Close"]'
CLIENT_DETAILS_POPUP_WSDL_URL_DETAILS_CLASS = 'closed'
CLIENT_DETAILS_POPUP_WSDL_SERVICES_AUTHCERTDELETION_XPATH = '//table[@id="services"]//td[text()="authCertDeletion (0)"]'
CLIENT_DETAILS_POPUP_LOCAL_GROUPS_TAB_XPATH = '//li[@aria-controls="local_groups_tab"]'
CLIENT_DETAILS_POPUP_SERVICES_TAB_XPATH = '//li[@aria-controls="services_tab"]'

LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID = 'group_members_add'
LOCAL_GROUP_DETAILS_BUTTON_REMOVE_SELECTED_MEMBERS = 'group_members_remove_selected'
LOCAL_GROUP_DETAILS_BUTTON_SEARCH_XPATH = '//div[@id="members_search_simple_search_tab"]//button[text()="Search"]'
LOCAL_GROUP_FOUNDED_MEMBERS_XPATH = '//table[@id="members_search"]//tbody/tr/td[1]'
LOCAL_GROUP_FOUNDED_SUBSYSTEMS_XPATH = '//table[@id="members_search"]//tbody/tr/td[2]'
LOCAL_GROUP_FOUNDED_MEMBER_ID_XPATH = '//table[@id="members_search"]//tbody/tr/td[2]/span[text()="{0}"]'
LOCAL_GROUP_FOUNDED_MEMBER_ID_PARTIAL_XPATH = '//table[@id="members_search"]//tbody/tr/td[2]/span[contains(text(), "{0}")]'
LOCAL_GROUP_ADD_GROUP_MEMBERS_XPATH = '//table[@id="group_members"]//tbody/tr/td[1]'
LOCAL_GROUP_ADD_GROUP_MEMBERS_ID_XPATH = '//table[@id="group_members"]//tbody/tr/td[2]'
LOCAL_GROUP_ADD_GROUP_MEMBERS_DATE_XPATH = '//table[@id="group_members"]//tbody/tr/td[3]'

LOCAL_GROUP_ADD_SELECTED_TO_GROUP_BTN_ID = 'group_members_add_selected'
LOCAL_GROUP_EMPTY_MEMBERS_SEARCH_TABLE_XPATH = '//table[@id="members_search"]//td[@class="dataTables_empty"]'
LOCAL_GROUP_EMPTY_MEMBERS_TABLE_XPATH = '//table[@id="group_members"]//td[@class="dataTables_empty"]'
LOCAL_GROUP_EMPTY_TABLE_XPATH = '//table[@id="groups"]//td[@class="dataTables_empty"]'
LOCAL_GROUP_SEARCH_MEMBERS_TABLE_CANCEL_BTN_XPATH = '//div[@aria-describedby="group_members_add_dialog"]//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'
LOCAL_GROUP_MEMBERS_COUNT_ID = 'group_details_member_count'
LOCAL_GROUP_TABLE_MEMBERS_NAME_XPATH = '//table[@id="group_members"]//td[text()="{0}"]'
LOCAL_GROUP_TABLE_SUB_IN_ID_XPATH = '//table[@id="group_members"]//span[contains(text(), "{0}")]'
LOCAL_GROUP_REMOVE_ALL_MEMBERS_BTN_ID = 'group_members_remove_all'
LOCAL_GROUP_REMOVE_SELECTED_MEMBERS_BTN_ID = 'group_members_remove_selected'
LOCAL_GROUP_ADD_ALL_TO_GROUP_BTN_ID = 'group_members_add_all'
LOCAL_GROUP_DELETE_GROUP_BTN_ID = 'group_delete'
LOCAL_GROUP_DELETE_GROUP_CONFIRM_BTN_XPATH = '//button[@id="confirm"]'
LOCAL_GROUP_DELETE_GROUP_CANCEL_BTN_XPATH = '//div[@aria-describedby="confirm"]//button/span[text()="Cancel"]'
LOCAL_GROUP_EDIT_DESCRIPTION_BTN_XPATH = '//div[@id="group_details_dialog"]//button[@id="edit"]'
LOCAL_GROUP_EDIT_DESCRIPTION_TEXT_FIELD_ID = 'group_description_edit'
LOCAL_GROUP_EDIT_DESCRIPTION_OK_BTN_XPATH = '//div[@aria-describedby="group_description_edit_dialog"]//span[text()="OK"]'
LOCAL_GROUP_EDIT_DESCRIPTION_CANCEL_BTN_XPATH = '//div[@aria-describedby="group_description_edit_dialog"]//span[text()="Cancel"]'
LOCAL_GROUP_DETAILS_CLOSE_BTN_XPATH = '//div[@aria-describedby="group_details_dialog"]//div[@class="ui-dialog-buttonset"]//button/span[text()="Close"]'
LOCAL_GROUP_DESCRIPTION_TEXT_FIELD_ID = 'group_details_description'
LOCAL_GROUP_EDITED_DESCRIPTION_CLIENT_DETAILS_XPATH = '//table[@id="groups"]//tr//td[text()="{0}"]'
LOCAL_GROUP_DELETE_CONFIRM_POP_UP_XPATH = '//div[@aria-describedby="confirm"]'

WSDL_SERVICE_CODE_REGEX = '\w+\.[\w\d]+\s\(\d+\)'
WSDL_SERVICE_CODE_DATE_REGEX = '\d{4}-\d{2}-\d{2}'
WSDL_SERVICE_URL_REGEX = 'http[s]?://.+'
WSDL_SERVICE_TIMEOUT_REGEX = '\d+'
XROAD_IDENTIFIER_REGEX = '(.+:){4}.+'

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
CENTRAL_SERVICE_POPUP_CANCEL_BUTTON_ID = 'central_service_cancel'
CENTRAL_SERVICE_POPUP_CLEAR_BUTTON_ID = 'central_service_details_clear_search'

GROUP_ADD_POPUP_XPATH = '//div[@data-name="group_add_dialog"]'
GROUP_EDIT_POPUP_XPATH = '//div[@data-name="group_description_edit_dialog"]'
GROUP_ADD_POPUP_CODE_AREA_ID = 'add_group_code'
GROUP_ADD_POPUP_CODE_DESCRIPTION_ID = 'add_group_description'
GROUP_ADD_POPUP_OK_BTN_XPATH = GROUP_ADD_POPUP_XPATH + '//button[@data-name="ok"]'
GROUP_EDIT_POPUP_OK_BTN_XPATH = GROUP_EDIT_POPUP_XPATH + '//button[@data-name="ok"]'

REGISTRATION_DIALOG_OK_BUTTON_XPATH = '//div[@id="register_dialog"]/following::div[2]//button[@data-name="ok"]'
ADD_WSDL_POPUP_XPATH = '//div[@data-name="wsdl_add_dialog"]'
ADD_WSDL_POPUP_URL_ID = 'wsdl_add_url'
ADD_WSDL_POPUP_CANCEL_BTN_XPATH = ADD_WSDL_POPUP_XPATH + '//button[@data-name="cancel"]'
ADD_WSDL_POPUP_OK_BTN_XPATH = ADD_WSDL_POPUP_XPATH + '//button[@data-name="ok"]'

EDIT_WSDL_POPUP_XPATH = '//div[@data-name="wsdl_params_dialog"]'
EDIT_WSDL_BUTTON_ID = 'service_params'
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
EDIT_SERVICE_POPUP_TIMEOUT_APPLY_ALL_CHECKBOX_ID = 'params_timeout_all'
EDIT_SERVICE_POPUP_URL_APPLY_ALL_CHECKBOX_ID = 'params_url_all'
EDIT_SERVICE_POPUP_TLS_APPLY_ALL_CHECKBOX_ID = 'params_sslauth_all'
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
ACL_SUBJECTS_SEARCH_POPUP_CANCEL_BTN_XPATH = ACL_SUBJECTS_SEARCH_POPUP + '//button[text()="Cancel"]'
ACL_ADD_SUBJECTS_BY_NAME_XPATH = '//table[@id="acl_subjects_search"]//td[text()="{0}"]'

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
ACL_FOR_SERVICE_CLOSE_BTN_XPATH = '//div[@aria-describedby="service_acl_dialog"]//div[@class="ui-dialog-buttonset"]/button[span="Close"]'

ADD_CLIENT_POPUP_XPATH = '//div[@aria-describedby="client_add_dialog"]'
ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID = 'add_member_class'
ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID = 'add_member_code'
ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_CSS = '#client_add_dialog #add_subsystem_code'
ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_XPATH = '//div[not(contains(@style,"display:none")) and contains(@id, "client_add_dialog")]//input[@id="add_subsystem_code"]'
ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_ID = 'add_subsystem_code'
ADD_CLIENT_POPUP_OK_BTN_XPATH = ADD_CLIENT_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
ADD_CLIENT_POPUP_CANCEL_BTN_XPATH = ADD_CLIENT_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'

WARNING_POPUP = '//div[@aria-describedby="warning"]'
WARNING_POPUP_CONTINUE_XPATH = WARNING_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Continue"]'
WARNING_POPUP_CANCEL_XPATH = WARNING_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'

SECURITY_SERVER_EDIT_POPUP = '//div[@aria-describedby="securityserver_edit_dialog"]'
SECURITY_SERVER_EDIT_POPUP_CANCEL_XPATH = SECURITY_SERVER_EDIT_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Close"]'

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
TOKEN_DETAILS_POPUP_KEY_LABEL_AREA_ID = 'friendly_name'
TOKEN_DETAILS_POPUP = '//div[@aria-describedby="token_details_dialog"]'
TOKEN_DETAILS_POPUP_OK_BTN_XPATH = TOKEN_DETAILS_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
TOKEN_DETAILS_POPUP_CANCEL_BTN_XPATH = TOKEN_DETAILS_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'

TOKEN_LOGIN_POPUP = '//div[@aria-describedby="activate_token_dialog"]'
TOKEN_LOGIN_OK_BTN_XPATH = TOKEN_LOGIN_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
TOKEN_LOGIN_CANCEL_BTN_XPATH = TOKEN_LOGIN_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'
TOKEN_LOGIN_CLOSE_BTN_XPATH = TOKEN_LOGIN_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Close"]'

TOKEN_PIN_LABEL_AREA = 'activate_token_pin'

MEMBER_DETAILS_MANAGEMENT_REGQUEST_ID_REGEX = '[0-9]'
MEMBER_DETAILS_MANAGEMENT_REGQUEST_CREATED_REGEX = '(\d{4}[-]?\d{1,2}[-]?\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})'
MEMBER_DETAILS_MANAGEMENT_REQUEST_TYPE = '(\D)'
MEMBER_DETAILS_MANAGEMENT_REQUEST_STATUS = '(\D+)'

LOCAL_GROUP_POPUP = '//div[@aria-describedby="group_details_dialog"]'
LOCAL_GROUP_DELETE_GROUP_BTN_XPATH = LOCAL_GROUP_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Delete Group"]'
LOCAL_GROUPS_TAB = '//a[@href="#local_groups_tab"]'

def confirm_dialog_visible(self):
    # Check if anything with a "Confirm" button is visible
    try:
        self.by_css('button#confirm')
        return True
    except:
        return False


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
    print('Open add new services to subjects dialog')
    # Wait for the element and click
    self.wait_until_visible(type=By.ID, element=CLIENT_DETAILS_POPUP_ACL_SUBJECTS_ADD_BTN_ID).click()
    self.wait_jquery()
    print('Click on search')
    # Wait for the element and click
    self.wait_until_visible(type=By.CSS_SELECTOR, element=ACL_SUBJECTS_SEARCH_POPUP_SEARCH_BTN_CSS).click()
    print('Waiting on clients table to load')
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
    date_regex = '\d{4}-\d{2}-\d{2}'
    self.wait_jquery()
    self.log('SERVICE_02 1. Viewing Access Rights of a Service client')
    open_services_table = self.wait_until_visible(type=By.ID,
                                                  element=ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_OPEN_SERVICES_TABLE_ID)
    open_rows_codes = []
    self.log('SERVICE_02 2. System displays the list of security server clients services to '
             'which the service client has access rights for.')
    for row in open_services_table.find_elements(By.CSS_SELECTOR, "tbody tr"):
        tds = row.find_elements_by_tag_name('td')
        service_code = tds[0].text
        title = tds[1].text
        access_rights_date = tds[2].text
        self.log('SERVICE_02 2. The code of the service is displayed: {}'.format(service_code))
        self.is_not_none(service_code)
        self.log('SERVICE_02 2. The title of the service is displayed: {}'.format(title))
        self.is_not_none(title)
        self.log('SERVICE_02 2. The date of when the access right of this service '
                 'was granted to the service client: \n{}'.format(access_rights_date))
        self.is_true(re.match(date_regex, access_rights_date))
        open_rows_codes.append(service_code)
    return open_rows_codes


def close_console_output_dialog(self):
    ok_button = self.by_xpath(CONSOLE_OUTPUT_DIALOG_OK_BTN_XPATH)
    if ok_button.is_displayed():
        ok_button.click()


def close_all_open_dialogs(self, limit=0):
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
    count = 0
    for data in dialogs:
        dialog = data['dialog']
        # Find the close button ("X") and click it.
        close_button = dialog.find_element_by_css_selector(POPUP_HEADER_CLOSE_BUTTON_CSS)
        close_button.click()
        count += 1
        if limit > 0 and count >= limit:
            break


def get_wsdl_url_row(wsdl_url):
    return "//td[text()='WSDL DISABLED ({0})']".format(wsdl_url)


def get_local_group_row_by_code(code):
    return "//table[@id='groups']//td[text()='{0}']".format(code)


def get_service_url_row(service_url):
    return "//table[@id='services']//td[text()='{0}']".format(service_url)
