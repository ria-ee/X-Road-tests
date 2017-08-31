CERTIFICATION_SERVICES_TABLE_ID = 'cas'

DELETE_BTN_ID = 'ca_delete'
ADD_BTN_ID = 'ca_add'
DETAILS_BTN_ID = 'ca_details'

IMPORT_CA_CERT_BTN_ID = 'ca_cert_button'
ADD_CA_AUTH_ONLY_CHECKBOX_XPATH = '//div[@id="ca_settings_dialog"]//input[@name="authentication_only"]'
EDIT_CA_AUTH_ONLY_CHECKBOX_XPATH = '//div[@id="ca_settings_tab"]//input[@name="authentication_only"]'
CA_SETTINGS_TAB_XPATH = '//li[@aria-controls="ca_settings_tab"]'

SUBMIT_CA_CERT_BTN_ID = 'ca_cert_submit'

CERTIFICATE_PROFILE_INFO_AREA_CSS = '.cert_profile_info'
ADD_CERTIFICATE_PROFILE_INFO_AREA_XPATH = '//div[@id="ca_settings_dialog"]//input[@name="cert_profile_info"]'
EDIT_CERTIFICATE_PROFILE_INFO_AREA_XPATH = '//div[@id="ca_settings_tab"]//input[@name="cert_profile_info"]'
SUBMIT_CA_SETTINGS_BTN_ID = 'ca_settings_submit'
SAVE_CA_SETTINGS_BTN_ID = 'ca_settings_save'

OCSP_RESPONSE_TAB = '//li[@aria-controls="ocsp_responders_tab"]'
OCSP_RESPONDER_ADD_BTN_ID = 'ocsp_responder_add'
OCSP_RESPONDER_EDIT_BTN_ID = 'ocsp_responder_edit'
OCSP_RESPONDER_DELETE_BTN_ID = 'ocsp_responder_delete'

IMPORT_OCSP_CERT_BTN_ID = 'ocsp_responder_cert_button'
OCSP_RESPONDER_URL_AREA_ID = 'ocsp_responder_url'

SUBMIT_OCSP_CERT_AND_URL_BTN_ID = 'ocsp_responder_url_and_cert_submit'

OCSP_SETTINGS_POPUP = '//div[@aria-describedby="ocsp_responder_url_and_cert_dialog"]'
OCSP_SETTINGS_POPUP_OK_BTN_XPATH = OCSP_SETTINGS_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'
OCSP_SETTINGS_POPUP_CANCEL_BTN_XPATH = OCSP_SETTINGS_POPUP + '//div[@class="ui-dialog-buttonset"]//button[span="Cancel"]'


def get_ca_by_td_text(text):
    return '//table[contains(@id, "cas")]//tr//td[contains(text(), \"' + text + '\")]'


def get_ocsp_by_td_text(text):
    return '//table[contains(@id, "ocsp_responders")]//tr//td[contains(text(), \"' + text + '\")]'


def get_ocsp_responders(self):
    responders = self.by_xpath(
        '(//table[contains(@id, "ocsp_responders")]//tr//td[1])[not(contains(@class,"dataTables_empty"))]',
        multiple=True)
    result = []
    for responder in responders:
        result.append(responder.text)

    return result