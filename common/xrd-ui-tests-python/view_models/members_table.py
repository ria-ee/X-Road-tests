ADD_MEMBER_TEXTS_AND_RESULTS = [['', '', '', True, 'Missing parameter: {0}', 'memberClass', False],
                                ['MEMBER_TEST', '', 'TEST_MEMBER', True, 'Missing parameter: {0}', 'memberClass', False],
                                ['MEMBER_TEST', 'GOV', '', True, 'Missing parameter: {0}', 'memberCode', False],
                                ['', 'GOV', 'MEMBER_TEST', True, 'Missing parameter: {0}', 'memberName', False],
                                [256 * 'A', 'GOV', 'MEMBER_TEST', True, "Parameter '{0}' input exceeds 255 characters", 'memberName', False],
                                ['MEMBER_TEST', 'GOV', 256 * 'T', True, "Parameter '{0}' input exceeds 255 characters", 'memberCode', False],
                                ['MEMBER_TEST', 'GOV', 'TEST_MEMBER', False, None, None, False],
                                [255 * 'A', 'GOV', 255 * 'T', False, None, None, False],
                                ['   MEMBER_TEST   ', 'GOV', '   TEST_MEMBER   ', False, None, None, True],
                                ['MEMBER_TEST', 'GOV', 'TEST_MEMBER', True, "Failed to add member: Member with class 'GOV' and code 'TEST_MEMBER' already exists", None, False]
                                ]
CS_MEMBER_NAME_CLASS_CODE = ['MEMBER_TEST', 'GOV', 'TEST_MEMBER']

CHANGE_MEMBER_TEXTS_AND_RESULTS = [['', True, 'Missing parameter: {0}', 'memberName', False],
                                   [256 * 'A', True, "Parameter '{0}' input exceeds 255 characters", 'memberName', False],
                                   ['TEST_MEMBER', False, None, None, False],
                                   [255 * 'T', False, None, None, False],
                                   ['   MEMBER_TEST    ', False, None, None, True]
                                   ]

ADD_MEMBER_POPUP_XPATH = '//div[@aria-describedby="member_add_dialog"]'
ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID = 'member_add_name'
ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID = 'member_add_class'
ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID = 'member_add_code'
ADD_MEMBER_POPUP_OK_BTN_XPATH = ADD_MEMBER_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
ADD_MEMBER_POPUP_CANCEL_BTN_XPATH = ADD_MEMBER_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'

ADD_MEMBER_BTN_ID = 'member_add'
MEMBERS_DETATILS_BTN_ID = 'member_details'
MEMBER_EDIT_DELETE_BTN_XPATH = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="member_edit_delete"]'
MEMBER_NAME_EDIT_BTN_XPATH = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="member_edit_change_name"]'
MEMBER_EDIT_NAME_POPUP_EDIT_NAME_AREA_XPATH = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//input[@id="member_edit_name_new"]'


MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH = '//div[@data-name="member_edit_dialog"]//div[@class="ui-dialog-buttonset"]//button[span="Close"]'
MEMBER_DELETE_CONFIRM_BTN_ID = '//div[@aria-describedby="confirm"]//div[@class="ui-dialog-buttonset"]//button[span="Confirm"]'

MEMBER_EDIT_POPUP_XPATH = '//div[@aria-describedby="member_name_edit_dialog"]'
MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH = MEMBER_EDIT_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
MEMBER_EDIT_NAME_POPUP_CANCEL_BTN_XPATH = MEMBER_EDIT_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'

MEMBERS_TABLE_ID = 'members'
MANAGEMENT_REQUEST_TABLE_ID = 'management_requests_all'
MEMBERS_TABLE_ROWS_CSS = '#members tbody tr'
MANAGEMENT_REQUEST_DETAILS_BTN_ID = 'request_details'
APPROVE_REQUEST_BTN_XPATH = '//div[not(contains(@style,"display: none")) and contains(@data-name, "reg_request_edit_dialog")]//button[span= "Approve"]'
DECLINE_REQUEST_BTN_XPATH = '//div[not(contains(@style,"display: none")) and contains(@data-name, "reg_request_edit_dialog")]//button[span= "Decline"]'

NEW_CLIENT_REGISTRATION_REQUEST_POPUP_XPATH = '//div[@aria-describedby="member_used_server_register_dialog"]'
CLIENT_REGISTRATION_SUBSYSTEM_CODE_AREA_ID = 'used_server_subsystem_code'
USED_SERVERS_SEARCH_BTN_ID = 'used_server_server_search'
CLIENT_REGISTRATION_SUBMIT_BTN_ID = 'member_used_server_register_submit'
CLIENT_REGISTRATION_CANCEL_BTN_XPATH = NEW_CLIENT_REGISTRATION_REQUEST_POPUP_XPATH + '//span[text()="Cancel"]'
SECURITY_SERVERS_TABLE_ROWS_XPATH = '//div[@id ="used_server_search_all_wrapper"]//table//tbody'
SELECT_SECURITY_SERVER_BTN_ID = 'member_securityserver_search_select'

'''
MEMBER POPUP
'''
OWNED_SERVERS_TAB = '//li[@aria-controls="member_owned_servers_tab"]'
SUBSYSTEM_TAB = '//li[@aria-controls="member_subsystems_tab"]'
USED_SERVERS_TAB = '//li[@aria-controls="member_used_servers_tab"]'
GLOBAL_GROUP_TAB = '//li[@aria-controls="member_group_membership_tab"]'
MANAGEMENT_REQUESTS_TAB = '//li[@aria-controls="member_management_requests_tab"]'

ADD_SUBSYSTEM_BTN_ID = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="add_subsystem"]'
DELETE_SUBSYSTEM_BTN_ID = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="delete_subsystem"]'
REGISTER_SECURITYSERVER_CLIENT_ADD_BTN_ID = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="register_securityserver_client"]'
ADD_MEMBER_TO_GLOBAL_GROUP_BTN_ID = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="add_global_group_membership"]'

SUBSYSTEM_POPUP_XPATH = '//div[@aria-describedby="subsystem_add_dialog"]'
GROUP_POPUP_XPATH = '//div[@aria-describedby="member_to_group_add_dialog"]'
GROUP_POPUP_OK_BTN_XPATH = GROUP_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
SUBSYSTEM_CODE_AREA_ID = 'subsystem_add_code'
SUBSYSTEM_POPUP_OK_BTN_XPATH = SUBSYSTEM_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
SUBSYSTEM_TABLE_XPATH = '//table[contains(@class, "member_subsystems")]//tbody'

GROUP_SELECT_ID = 'member_to_group_add_select_group'

CLIENT_REGISTRATION_REQUEST_EDIT_POPUP_XPATH = '//div[@aria-describedby="client_reg_request_edit_dialog"]'
CLIENT_REGISTRATION_REQUEST_EDIT_POPUP_OK_BTN_XPATH = CLIENT_REGISTRATION_REQUEST_EDIT_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="Close"]'
CLIENT_REQUEST_NAME_AREA_XPATH = CLIENT_REGISTRATION_REQUEST_EDIT_POPUP_XPATH + '//p[not(contains(@style,"display:none")) and contains(@class, "client_details_name")]'
CLIENT_REQUEST_CLASS_AREA_XPATH = CLIENT_REGISTRATION_REQUEST_EDIT_POPUP_XPATH + '//p[not(contains(@style,"display:none")) and contains(@class, "client_details_class")]'
CLIENT_REQUEST_CODE_AREA_XPATH = CLIENT_REGISTRATION_REQUEST_EDIT_POPUP_XPATH + '//p[not(contains(@style,"display:none")) and contains(@class, "client_details_code")]'
CLIENT_REQUEST_SUB_CODE_AREA_XPATH = CLIENT_REGISTRATION_REQUEST_EDIT_POPUP_XPATH + '//p[not(contains(@style,"display:none")) and contains(@class, "client_details_subsystem_code")]'

MEMBER_FIRST_OWNED_SERVER_DETAILS_CSS = '.open_details'
SS_DETAILS_AUTH_CERT_TAB_XPATH = '//*[@href="#server_auth_certs_tab"]'
SS_DETAILS_ADD_AUTH_CERT_BTN_ID = 'securityserver_authcert_add'
ADD_AUTH_CERT_UPLOAD_BTN_ID = 'securityserver_auth_cert_upload_button'
ADD_AUTH_CERT_SUBMIT_BTN_ID = 'auth_cert_add_submit'
ADD_AUTH_CERT_CANCEL_BTN_XPATH = '//div[@aria-describedby="auth_cert_add_dialog"]//span[contains(text(), "Cancel")]'
SUBSYSTEM_TR_BY_CODE_XPATH = '//tr[contains(., "{0}")]'

USED_SERVERS_TABLE_XPATH = '//table[contains(@class, "member_used_servers")]//tbody'
MEMBER_MANAGEMENT_TABLE_XPATH = '//table[contains(@class, "member_management_requests")]//tbody'
DELETE_REGISTER_SECURITYSERVER_CLIENT_BTN_ID = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="remove_securityserver_client"]'




def get_requests_row_by_td_text(text):
    return '//table[@id = "management_requests_all"]//tbody//tr//td[contains(text(), "' + text + '")]/parent:: *'


def get_row_by_td_text(text):
    return '//table[contains(@id, "securityservers")]//tr//td[contains(text(), \"' + text + '\")]'


def get_row_by_columns(table, values):
    """
    Finds row from members table and returns it
    :param table: members table
    :param values: list of member values, ordered as: [name, class,  code]
    :return: row
    """
    rows = table.find_elements_by_tag_name('tr')
    for row in rows:
        if row.text == ' '.join(values):
            return row
    return None


def get_member_data_from_table(nr, text):
    return "//table[@id='members']//td[" + str(nr) + "][text()='" + text + "']"


def get_member_used_servers(row, column):
    return "//div[@id='member_used_servers_tab']//tr[{0}]/td[{1}]".format(row, column)
