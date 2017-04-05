SECURITY_SERVER_TABLE_ID = 'securityservers'
SECURITY_SERVER_CLIENT_DETAILS_BTN_ID = 'securityserver_edit'
SERVER_CLIENT_TAB = '//li[@aria-controls="server_clients_tab"]'
SERVER_MANAGEMENT_REQUESTS_TAB = '//li[@aria-controls="server_management_requests_tab"]'
ADD_CLIENT_TO_SECURITYSERVER_BTN_ID = 'securityserver_client_add'

SECURITY_SERVER_CLIENTS_TABLE_ID = 'securityserver_clients'

# NEW CLIENT REGISTRATION REQUEST POPUP
SEARCH_MEMBER_POPUP_XPATH = '//div[@aria-describedby="member_search_dialog"]'
SEARCH_BTN_ID = 'securityserver_client_client_search'
SUBSYSTEM_CODE_AREA_ID = 'securityserver_client_subsystem_code'
MEMBERS_TABLE_ID = 'member_search'
SELECT_MEMBER_BTN_XPATH = '//div[not(contains(@style,"display:none")) and contains(@class, "ui-dialog")]//button[@id="member_search_select"]'
MEMBERS_SEARCH_TABLE_XPATH = '//div[@id = "member_search_wrapper"]//tbody'

# NEW CLIENT REGISTRATION REQUEST
NEW_CLIENT_REGISTRATION_REQUEST_POPUP_XPATH = '//div[@aria-describedby="securityserver_client_register_dialog"]'
SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID = 'securityserver_client_register_submit'

# MANAGEMENT REQUESTS
SECURITYSERVER_MANAGEMENT_REQUESTS_TABLE_ID = 'securityserver_management_requests'
REVOKE_REGISTRATION_REQUEST = '.reg_request_revoke'
REVOKE_MANAGEMENT_REQUEST_BTN_XPATH = '//div[@aria-describedby="client_reg_request_edit_dialog"]//button[contains(@class, "reg_request_revoke")]'
