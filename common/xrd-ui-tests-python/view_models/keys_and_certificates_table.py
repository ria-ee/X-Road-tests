KEY_LABEL_TEXT = "test_certificate_keys"

KEY_CONFIG_FILE = '/etc/xroad/signer/keyconf.xml'

OCSP_RESPONSE_CLASS_NAME = 'cert-ocsp-response'
OCSP_DISABLED_RESPONSE = 'disabled'
OCSP_DISABLED_CERT_ROW = '//td[contains(@class, {0}) and text()="{1}"]'.format(OCSP_RESPONSE_CLASS_NAME, OCSP_DISABLED_RESPONSE)
OCSP_CERT_FRIENDLY_NAME = 'cert-friendly-name'
OCSP_DISABLED_CERT_ROW2 = '//td[contains(@class, {0}) and text()="{1}"]/..'.format(OCSP_RESPONSE_CLASS_NAME, OCSP_DISABLED_RESPONSE)


def get_cert_row(text):
    return '//td[contains(@class, {0}) and text()="{1}"]'.format(OCSP_CERT_FRIENDLY_NAME, text)


KEY_LABEL_TEXT_AND_RESULTS = [[256 * 'S', True, "Parameter '{0}' input exceeds 255 characters", 'label', False],
                              ['   ' + KEY_LABEL_TEXT + '   ', False, None, None, True],
                              ['z', False, None, None, False],
                              [255 * 'S', False, None, None, False],
                              ['', False, None, None, False],
                              [KEY_LABEL_TEXT, False, None, None, False]]

KEY_USAGE_TYPE_SIGN = 'sign'
DETAILS_BTN_ID = 'details'
CERT_ACTIVE_CSS = '.cert-active'
GENERATEKEY_BTN_ID = 'generate_key'
GENERATECSR_BTN_ID = 'generate_csr'
ACTIVATE_BTN_ID = 'activate'
DISABLE_BTN_ID = 'disable'
REGISTER_BTN_ID = 'register'
UNREGISTER_BTN_ID = 'unregister'
DELETE_BTN_ID = 'delete'
IMPORT_BTN_ID = 'import_cert'
FILEPATH_IMPORT_BTN_ID = 'file_upload_button'
FILE_IMPORT_OK_BTN_ID = 'file_upload_submit'
FILEPATH_INPUT_AREA_CSS = '.selected_file'
FILEPATH_FORM_INPUT_ID = 'file_upload'
UNSAVED_KEY_CSS = '.key.unsaved'
APPROVED = 'APPROVED'
SUBMITTED_FOR_APPROVAL_STATE = 'SUBMITTED FOR APPROVAL'
WAITING_STATE = 'WAITING'
REVOKED_STATE = 'REVOKED'
DECLINED_STATE = 'DECLINED'

KEYS_AND_CERTIFICATES_TABLE_ID = 'keys'
KEYS_AND_CERTIFICATES_TABLE_ROWS_CSS = '.keys tbody tr'
GLOBAL_ERROR_CERTIFICATE_ROW_XPATH = '//td[text()="global error"]'
SAVED_CERTIFICATE_ROW_XPATH = '//td[text()="saved"]'
REG_IN_PROGRESS_CERTIFICATE_ROW_XPATH = '//td[text()="registration in progress"]'
DEL_IN_PROGRESS_CERTIFICATE_ROW_XPATH = '//td[text()="deletion in progress"]'

REGISTER_DIALOG_ADDRESS_INPUT_ID = 'address'

GENERATED_KEYS_TABLE_ROW_CSS = '.key'
CERT_REQUESTS_TABLE_ROW_CSS = ".cert-request"
KEY_TABLE_ROW_BY_LABEL_XPATH = '//table[contains(@id, "keys")]//tr[contains(@class, "key")]//td[contains(text(), \"{0}\")]'
KEY_TABLE_CERT_ROW_BY_LABEL_XPATH = KEY_TABLE_ROW_BY_LABEL_XPATH + '/../following::tr[contains(@class, "cert-active")]'
GENERATED_KEY_TABLE_ROW_XPATH = '//table[contains(@id, "keys")]//tr[contains(@class, "key")]//td[contains(text(), \"' + KEY_LABEL_TEXT + '\")]'
SOFTTOKEN_TABLE_ROW_XPATH = '//table[contains(@id, "keys")]//tr[contains(@class, "token")]/td[div="Token: softToken-0"]'
SOFTTOKEN_TABLE_XPATH = '//table[contains(@id, "keys")]//tr[contains(@class, "token")]/td'
TOKEN_NAMES_CLASS = "token-name"
CERT_BY_KEY_LABEL = '//tr[contains(., "{0}")]/following::tr[2]'
TOKEN_DETAILS_ERROR_PARAMETER = 'friendly_name'
TOKEN_DETAILS_MISSING_PARAMETER = 'Missing parameter: friendly_name'
SOFTTOKEN_FRIENDLY_NAME = 'softToken-0'
SOFTTOKEN_TABLE_ROW_XPATH2 = "//div[@class='left token-name']"
SOFTTOKEN_KEY_ROW = "//tr[@class='key token-available token-inactive key-unavailable']"
SOFTTOKEN_FRIENDLY_NAME_WHITESPACES = '           test               '
SOFTTOKEN_LOGOUT = '//button[@class="deactivate_token"]'
SOFTTOKEN_LOGIN = '//button[@class="activate_token"]'
SOFTTOKEN_PIN_WHITESPACES = '  1234  '
SOFTTOKEN_LOGOUT_TEXT = 'LOGOUT'
SOFTTOKEN_PIN = '1234'
SOFTTOKEN_PIN_ERROR_PARAMETER = 'pin'





IMPORT_CERTIFICATE_POPUP_XPATH = '//div[@aria-describedby="file_upload_dialog"]'

GENERATE_CSR_SIGNING_REQUEST_POPUP_XPATH = '//div[@data-name="generate_csr_dialog"]'
GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID = 'csr_format'
GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID = 'approved_ca'
GENERATE_CSR_SIGNING_REQUEST_CLIENT_DROPDOWN_ID = 'member_id'
GENERATE_CSR_SIGNING_REQUEST_USAGE_DROPDOWN_ID = 'key_usage'
GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH = GENERATE_CSR_SIGNING_REQUEST_POPUP_XPATH + '//button[@data-name="ok"]'
GENERATE_CSR_SIGNING_REQUEST_POPUP_CANCEL_BTN_XPATH = GENERATE_CSR_SIGNING_REQUEST_POPUP_XPATH + '//button[@data-name="cancel"]'

SUBJECT_DISTINGUISHED_NAME_POPUP_XPATH = '//div[@data-name="subject_dn_dialog"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_SERIAL_NUMBER_XPATH = '//input[@name="serialNumber"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_C_XPATH = '//input[@name="C"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_O_XPATH = '//input[@name="O"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_CN_XPATH = '//input[@name="CN"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH = SUBJECT_DISTINGUISHED_NAME_POPUP_XPATH + '//button[@data-name="ok"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_CANCEL_BTN_XPATH = SUBJECT_DISTINGUISHED_NAME_POPUP_XPATH + '//button[@data-name="cancel"]'
SIGNING_KEY_LABEL = 'signingkey'
AUTH_KEY_LABEL = 'authkey'


def get_generated_row_row_by_td_text(text):
    return '//table[contains(@id, "keys")]//tr[contains(@class, "cert-active")]//td[contains(text(), \"' + text + '\")]'


def get_generated_key_row_xpath(client_code, client_class):
    return '//table[contains(@id, "keys")]//tr[contains(@class, "key")]//td[contains(text(), \"' + \
           KEY_LABEL_TEXT + '_' + client_code + '_' + client_class + '\")]'

def get_generated_key_row_key_usage_xpath(client_code, client_class):
    return '//table[contains(@id, "keys")]//tr[contains(@class, "key")]//td[contains(text(), \"' + \
           KEY_LABEL_TEXT + '_' + client_code + '_' + client_class + '\")]//span[contains(@class, "key-usage")]'

def get_generated_key_row_cert_xpath(client_code, client_class):
    return '//table[contains(@id, "keys")]//tr[contains(@class, "key")]//td[contains(text(), \"' + \
           KEY_LABEL_TEXT + '_' + client_code + '_' + client_class + '\")]/../following::tr[2]'

def get_generated_key_row_csr_xpath(client_code, client_class):
    return '//table[contains(@id, "keys")]//tr[contains(@class, "key")]//td[contains(text(), \"' + \
           KEY_LABEL_TEXT + '_' + client_code + '_' + client_class + '\")]/../following::tr[contains(@class, "cert-request")]'

def get_generated_key_row_active_cert_friendly_name_xpath(client_code, client_class, key_num = 1):
    return '(//table[contains(@id, "keys")]//tr[contains(@class, "key")]//td[contains(text(), \"' + \
           KEY_LABEL_TEXT + '_' + client_code + '_' + client_class + '\")]/..' + \
           '/following::tr[{0}])[contains(@class, "cert-active")]//td[contains(@class, "friendly-name")]'.format(key_num+1)

def get_text(text):
    return ".//*[text()[contains(.,'" + text + "')]]"


def get_csr_data(id, nr):
    return "//select[@id='" + id + "']//option[" + str(nr) + "]"
