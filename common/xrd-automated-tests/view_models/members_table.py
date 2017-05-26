ADD_MEMBER_POPUP_XPATH = '//div[@aria-describedby="member_add_dialog"]'
ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID = 'member_add_name'
ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID = 'member_add_class'
ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID = 'member_add_code'
ADD_MEMBER_POPUP_OK_BTN_XPATH = ADD_MEMBER_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'

ADD_MEMBER_BTN_ID = 'member_add'
MEMBERS_DETATILS_BTN_ID = 'member_details'
MEMBER_EDIT_DELETE_BTN_XPATH = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="member_edit_delete"]'
MEMBER_NAME_EDIT_BTN_XPATH = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="member_edit_change_name"]'
MEMBER_EDIT_NAME_POPUP_EDIT_NAME_AREA_XPATH = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//input[@id="member_edit_name_new"]'

MEMBER_EDIT_POPUP_XPATH = '//div[@aria-describedby="member_name_edit_dialog"]'
MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH = MEMBER_EDIT_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'

MEMBERS_TABLE_ID = 'members'
MANAGEMENT_REQUEST_TABLE_ID = 'management_requests_all'
MEMBERS_TABLE_ROWS_CSS = '#members tbody tr'
MANAGEMENT_REQUEST_DETAILS_BTN_ID = 'request_details'
APPROVE_REQUEST_BTN_XPATH = '//div[not(contains(@style,"display:none")) and contains(@data-name, "client_reg_request_edit_dialog")]//button[span= "Approve"]'
DECLINE_REQUEST_BTN_XPATH = '//div[not(contains(@style,"display:none")) and contains(@data-name, "client_reg_request_edit_dialog")]//button[span= "Decline"]'

NEW_CLIENT_REGISTRATION_REQUEST_POPUP_XPATH = '//div[@aria-describedby="member_used_server_register_dialog"]'
CLIENT_REGISTRATION_SUBSYSTEM_CODE_AREA_ID = 'used_server_subsystem_code'
USED_SERVERS_SEARCH_BTN_ID = 'used_server_server_search'
CLIENT_REGISTRATION_SUBMIT_BTN_ID = 'member_used_server_register_submit'
SECURITY_SERVERS_TABLE_ROWS_XPATH = '//div[@id ="used_server_search_all_wrapper"]//table//tbody'
SELECT_SECURITY_SERVER_BTN_ID = 'member_securityserver_search_select'

'''
MEMBER POPUP
'''
SUBSYSTEM_TAB = '//li[@aria-controls="member_subsystems_tab"]'
USED_SERVERS_TAB = '//li[@aria-controls="member_used_servers_tab"]'
GLOBAL_GROUP_TAB = '//li[@aria-controls="member_group_membership_tab"]'

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