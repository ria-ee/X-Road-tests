SECURITY_SERVER_TABLE_ID = 'securityservers'
SECURITY_SERVER_CLIENT_DETAILS_BTN_ID = 'securityserver_edit'
SECURITY_SERVER_DELETE_BTN_ID = 'securityserver_delete'
SECURITY_SERVER_MANAGEMENT_PROVIDER_NAME_ID = 'service_provider_name'
SECURITY_SERVER_MANAGEMENT_PROVIDER_EDIT_BTN_ID= 'service_provider_edit'
SECURITY_SERVER_MANAGEMENT_PROVIDER_ID = 'service_provider_id'
MANAGEMENT_REG_REQUEST_SERVER_NAME_ID = 'used_server_name'
MANAGEMENT_REG_REQUEST_SERVER_CLASS_ID = 'used_server_class'
MANAGEMENT_REG_REQUEST_SERVER_CODE_ID = 'used_server_code'
MANAGEMENT_REG_REQUEST_SUBSYSTEM_CODE_ID = 'used_server_subsystem_code'
MANAGEMENT_SERVICE_SECURITY_SERVER_ID = 'service_provider_security_servers'
MANAGEMENT_SERVICE_WSDL_ID = 'wsdl_address'
MANAGEMENT_SERVICE_ADDRESS_ID = 'services_address'
MANAGEMENT_SERVICE_OWNERS_GROUP_CODE_XPATH = '//td[text()="Security Server Owners Group Code"]/following::td'
SERVER_CLIENT_TAB = '//li[@aria-controls="server_clients_tab"]'
SECURITY_SERVER_DETAILS_TAB = '//li[@aria-controls="server_details_tab"]'
SERVER_MANAGEMENT_REQUESTS_TAB = '//li[@aria-controls="server_management_requests_tab"]'
SERVER_MANAGEMENT_OWNED_SERVERS_TAB = '//li[@aria-controls="member_owned_servers_tab"]'
ADD_CLIENT_TO_SECURITYSERVER_BTN_ID = 'securityserver_client_add'
ADD_OWNED_SERVER_BTN_CSS = "#member_owned_servers_tab_actions #add_owned_server"
OWNED_SERVERS_SERVER_CODE_INPUT_ID = "owned_server_add_servercode"
OWNED_SERVERS_UPLOAD_CERT_BTN_ID = "owned_server_cert_upload_button"
OWNED_SERVERS_UPLOAD_OWNER_NAME_ID = "owned_server_owner_name"
OWNED_SERVERS_UPLOAD_OWNER_CLASS_ID = "owned_server_owner_class"
OWNED_SERVERS_UPLOAD_OWNER_CODE_ID = "owned_server_owner_code"
ADD_OWNED_SERVER_SUBMIT_BUTTON_ID = "add_owned_server_submit"
SECURITYSERVER_AUTH_CERT_ROW_CSS = '#securityserver_auth_certs tbody tr'
SECURITYSERVER_AUTH_CERT_TAB_XPATH = '//*[@href="#server_auth_certs_tab"]'
SECURITYSERVER_AUTH_CERT_DELETE_BTN_ID = 'securityserver_authcert_delete'
SECURITY_SERVER_TABLE_CSS = '#securityservers_wrapper tbody'
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
SECURITYSERVER_CLIENT_REGISTER_CANCEL_BTN_CSS = '*[data-name="cancel"]'
SECURITYSERVER_CLIENT_NAME_ID = 'securityserver_client_name'
SECURITYSERVER_CLIENT_CLASS_ID = 'securityserver_client_class'
SECURITYSERVER_CLIENT_CODE_ID = 'securityserver_client_code'
SECURITYSERVER_CLIENT_SERVER_OWNER_NAME_ID = 'securityserver_client_owner_name'
SECURITYSERVER_CLIENT_SERVER_OWNER_CLASS_ID = 'securityserver_client_owner_class'
SECURITYSERVER_CLIENT_SERVER_OWNER_CODE_ID = 'securityserver_client_owner_code'
SECURITYSERVER_CLIENT_SERVER_CODE_ID = 'securityserver_client_server_code'

# MANAGEMENT REQUESTS
SECURITYSERVER_MANAGEMENT_REQUESTS_TABLE_ID = 'securityserver_management_requests'
REVOKE_REGISTRATION_REQUEST = '.reg_request_revoke'
REVOKE_CLIENT_MANAGEMENT_REQUEST_BTN_XPATH = '//div[@aria-describedby="client_reg_request_edit_dialog"]//button[contains(@class, "reg_request_revoke")]'
REVOKE_CERT_MANAGEMENT_REQUEST_BTN_XPATH = '//div[@aria-describedby="auth_cert_reg_request_edit_dialog"]//button[contains(@class, "reg_request_revoke")]'
MANAGEMENT_REQUESTS_CLIENT_DELETION_XPATH = '//table[@id="management_requests_all"]//td[contains(text(), \"Client deletion\")]'
MANAGEMENT_REQUESTS_CERT_DELETION_XPATH = '//table[@id="management_requests_all"]//td[contains(text(), \"Certificate deletion\")]'
MANAGEMENT_REQUESTS_APPROVED_XPATH = '//table[@id="management_requests_all"]//td[contains(text(), \"APPROVED\")]'
CLIENT_DELETION_REQUEST_DETAILS_DIALOG_ID = "client_deletion_request_edit_dialog"
CERT_DELETION_REQUEST_DETAILS_DIALOG_ID = "auth_cert_deletion_request_edit_dialog"
CLIENT_DELETION_REQUEST_DETAILS_DIALOG_COMMENTS_INPUT_CLASS = "management_request_comments"
CLIENT_DELETION_REQUEST_COMMENTS_INPUT_XPATH = '//div[@aria-describedby="client_deletion_request_edit_dialog"]//p[contains(@class, "management_request_comments")]'
AUTH_CERT_DELETION_REQUEST_COMMENTS_INPUT_XPATH = '//div[@aria-describedby="auth_cert_deletion_request_edit_dialog"]//p[contains(@class, "management_request_comments")]'
CLIENT_REGISTRATION_REQUEST_POPUP_COMMENT_XPATH = '//div[@aria-describedby="client_reg_request_edit_dialog"]//p[contains(@class, "management_request_comments")]'
REVOKE_CERT_DELETE_REQUEST_COMMENT = '\'{}\' revocation'
REVOKE_CLIENT_DELETE_REQUEST_COMMENT = 'Request ID {} revocation'

# DELETION REQUEST
DELETION_REQUEST_OWNER_NAME_ID = 'delete_auth_cert_owner_name'
DELETION_REQUEST_OWNER_CLASS_ID = 'delete_auth_cert_owner_class'
DELETION_REQUEST_OWNER_CODE_ID = 'delete_auth_cert_owner_code'
DELETION_REQUEST_SERVER_CODE_ID = 'delete_auth_cert_servercode'
DELETION_REQUEST_SUBMIT_BTN_XPATH = '//div[@aria-describedby="auth_cert_delete_dialog"]//span[text()="Submit"]'
DELETION_REQUEST_CANCEL_BTN_XPATH = '//div[@aria-describedby="auth_cert_delete_dialog"]//span[text()="Cancel"]'
