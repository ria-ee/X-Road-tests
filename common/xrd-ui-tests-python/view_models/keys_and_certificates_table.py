KEY_LABEL_TEXT = "test_certificate_keys"

KEY_CONFIG_FILE = '/etc/xroad/signer/keyconf.xml'

KEY_LABEL_TEXT_AND_RESULTS = [[256 * 'S', True, "Parameter '{0}' input exceeds 255 characters", 'label', False],
                              ['   ' + KEY_LABEL_TEXT + '   ', False, None, None, True],
                              ['z', False, None, None, False],
                              [255 * 'S', False, None, None, False],
                              ['', False, None, None, False],
                              [KEY_LABEL_TEXT, False, None, None, False]]

DETAILS_BTN_ID = 'details'
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

KEYS_AND_CERTIFICATES_TABLE_ID = 'keys'

GENERATED_KEYS_TABLE_ROW_CSS = '.key'
CERT_REQUESTS_TABLE_ROW_CSS = ".cert-request"
GENERATED_KEY_TABLE_ROW_XPATH = '//table[contains(@id, "keys")]//tr[contains(@class, "key")]//td[contains(text(), \"' + KEY_LABEL_TEXT + '\")]'
SOFTTOKEN_TABLE_ROW_XPATH = '//table[contains(@id, "keys")]//tr[contains(@class, "token")]/td[div="Token: softToken-0"]'

IMPORT_CERTIFICATE_POPUP_XPATH = '//div[@aria-describedby="file_upload_dialog"]'

GENERATE_CSR_SIGNING_REQUEST_POPUP_XPATH = '//div[@data-name="generate_csr_dialog"]'
GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID = 'csr_format'
GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID = 'approved_ca'
GENERATE_CSR_SIGNING_REQUEST_CLIENT_DROPDOWN_ID = 'member_id'
GENERATE_CSR_SIGNING_REQUEST_USAGE_DROPDOWN_ID = 'key_usage'
GENERATE_CSR_SIGNING_REQUEST_POPUP_OK_BTN_XPATH = GENERATE_CSR_SIGNING_REQUEST_POPUP_XPATH + '//button[@data-name="ok"]'
GENERATE_CSR_SIGNING_REQUEST_POPUP_CANCEL_BTN_XPATH = GENERATE_CSR_SIGNING_REQUEST_POPUP_XPATH + '//button[@data-name="cancel"]'

SUBJECT_DISTINGUISHED_NAME_POPUP_XPATH = '//div[@data-name="subject_dn_dialog"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_C_XPATH = '//input[@name="C"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_O_XPATH = '//input[@name="O"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_CN_XPATH = '//input[@name="CN"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_OK_BTN_XPATH = SUBJECT_DISTINGUISHED_NAME_POPUP_XPATH + '//button[@data-name="ok"]'
SUBJECT_DISTINGUISHED_NAME_POPUP_CANCEL_BTN_XPATH = SUBJECT_DISTINGUISHED_NAME_POPUP_XPATH + '//button[@data-name="cancel"]'


def get_generated_row_row_by_td_text(text):
    return '//table[contains(@id, "keys")]//tr[contains(@class, "cert-active")]//td[contains(text(), \"' + text + '\")]'


def get_generated_key_row_xpath(client_code, client_class):
    return '//table[contains(@id, "keys")]//tr[contains(@class, "key")]//td[contains(text(), \"' + \
           KEY_LABEL_TEXT + '_' + client_code + '_' + client_class + '\")]'


def get_text(text):
    return ".//*[text()[contains(.,'" + text + "')]]"


def get_csr_data(id, nr):
    return "//select[@id='" + id + "']//option[" + str(nr) + "]"
