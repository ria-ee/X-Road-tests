ADD_GROUP_BTN_ID = 'group_add'

NEW_GROUP_POPUP_XPATH = '//div[@aria-describedby="group_add_dialog"]'
NEW_GROUP_POPUP_OK_BTN_XPATH = NEW_GROUP_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
NEW_GROUP_POPUP_CANCEL_BTN_XPATH = NEW_GROUP_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'

GROUP_CODE_AREA_ID = 'group_add_code'
GROUP_DESCRIPTION_AREA_ID = 'group_add_description'

GROUP_TABLE_ID = 'global_groups'

GROUP_DETAILS_BTN_ID = 'group_details'

DELETE_GROUP_BTN_ID = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="group_details_delete_group"]'

GROUP_DATA = [['', '', True, "Missing parameter: {0}", 'code', False],
              ['', 'GROUPTEST', True, "Missing parameter: {0}", 'code', False],
              ['GROUPTEST', '', True, "Missing parameter: {0}", 'description', False],
              [256 * 'A', 'TESTGROUP', True, "Parameter '{0}' input exceeds 255 characters", 'code', False],
              ['GROUPTEST', 256 * 'T', True, "Parameter '{0}' input exceeds 255 characters", 'description', False],
              ['GROUPTEST', 'TESTGROUP', False, None, None, False],
              ['   GROUPTEST   ', '   TESTGROUP   ', False, None, None, True],
              [255 * 'A', 255 * 'T', False, None, None, False]
              ]


LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH = '//table[@id="groups"]//tr[td//text()[contains(., "{0}")]]'
LOCAL_GROUP_ROW_CSS = '#groups tbody tr'
GROUP_MEMBERS_ADD_SEARCH_INPUT_XPATH = '//div[@data-name="group_members_add_dialog"]//input[@name="group_members_search_all"]'
GROUP_MEMBERS_ADD_SEARCH_BUTTON_XPATH = '//div[@data-name="group_members_add_dialog"]//button[@class="search"]'
MEMBER_ROW_BY_TWO_COLUMNS_XPATH = '//tr[contains(.,"{0}") and contains(., "{1}")]'
GROUP_MEMBERS_ADD_BUTTON_ID = 'add_selected_members_to_group'
GLOBAL_GROUP_ROW_BY_TD_TEXT_XPATH = '//table[@id="global_groups"]//td[contains(., {0})]'
GLOBAL_GROUP_TR_BY_TD_TEXT_XPATH = GLOBAL_GROUP_ROW_BY_TD_TEXT_XPATH + '/..'
GLOBAL_GROUP_ADD_MEMBERS_BTN_ID = 'group_details_add_members'

def get_clobal_group_code_description_by_text(text):
    return "//table[@id='global_groups']//td[text()='{0}']".format(text)

def get_global_group_member_count_by_code(code):
    return "//table[@id='global_groups']//td[text()='{0}']/following::td[2]".format(code)
