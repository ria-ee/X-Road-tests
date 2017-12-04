import re
import time

from selenium.webdriver.common.by import By

from helpers import xroad
from tests.xroad_cs_ca.ca_management import edit_ca_settings
from view_models.certification_services import INTERMEDIATE_CA_TAB_XPATH, INTERMEDIATE_CA_ADD_BTN_ID, \
    SUBMIT_CA_CERT_BTN_ID, IMPORT_CA_CERT_BTN_ID, INTERMEDIATE_CA_OCSP_TAB_XPATH, INTERMEDIATE_CA_OCSP_ADD_BTN_ID, \
    IMPORT_OCSP_CERT_BTN_ID, OCSP_RESPONDER_URL_AREA_ID, SUBMIT_OCSP_CERT_AND_URL_BTN_ID, INTERMEDIATE_CA_BY_NAME_XPATH, \
    INTERMEDIATE_CA_DELETE_BTN_ID, INTERMEDIATE_CA_TR_BY_NAME_XPATH, DATE_REGEX, INTERMEDIATE_CA_EDIT_BTN_ID, \
    INTERMEDIATE_CA_SUBJECT_DN_ID, CA_DISTINGUISHED_NAME, INTERMEDIATE_CA_ISSUER_DN_ID, INTERMEDIATE_CA_VALID_FROM_ID, \
    INTERMEDIATE_CA_VALID_TO_ID
from view_models.log_constants import ADD_INTERMEDIATE_CA, ADD_INTERMEDIATE_CA_OCSP, DELETE_INTERMEDIATE_CA, \
    ADD_INTERMEDIATE_CA_FAILED
from view_models.messages import NOTICE_MESSAGE_CSS, ERROR_MESSAGE_CSS, WRONG_FORMAT_INTERMEDIATE_CA_CERTIFICATE, \
    INTERMEDIATE_CA_ADDED_SUCCESSFULLY
from view_models.sidebar import CERTIFICATION_SERVICES_CSS


def test_add_intermediate_ca(self, ca_name, cert, ocsp_url=None, ocsp_cert=None, check_error=False, log_checker=None):
    def add_intermediate_ca():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.log('Open certification services view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=CERTIFICATION_SERVICES_CSS).click()
        self.wait_jquery()
        self.log('Open CA editing')
        edit_ca_settings(self, ca_name)
        self.log('Open "Intermediate CA" tab')
        self.wait_until_visible(type=By.XPATH, element=INTERMEDIATE_CA_TAB_XPATH).click()
        self.wait_jquery()
        self.log('TRUST_12 1. Clicking "Add" button')
        self.wait_until_visible(type=By.ID, element=INTERMEDIATE_CA_ADD_BTN_ID).click()
        self.log('TRUST_12 2. Uploading intermediate CA file from local file system')
        upload_input = self.wait_until_visible(type=By.ID, element=IMPORT_CA_CERT_BTN_ID)
        xroad.fill_upload_input(self, upload_input, cert)
        self.wait_jquery()
        self.log('TRUST_12 2. Clicking "OK" button')
        self.wait_until_visible(type=By.ID, element=SUBMIT_CA_CERT_BTN_ID).click()
        if check_error:
            expected_error_msg = WRONG_FORMAT_INTERMEDIATE_CA_CERTIFICATE
            self.log('TRUST_12 3a.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            if current_log_lines is not None:
                expected_log_msg = ADD_INTERMEDIATE_CA_FAILED
                self.log('TRUST_12 3a.2 System logs the event "{}"'.format(expected_log_msg))
                time.sleep(1.5)
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
            return
        notice_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=NOTICE_MESSAGE_CSS).text
        expected_notice_msg = INTERMEDIATE_CA_ADDED_SUCCESSFULLY
        self.log('TRUST_12 4. System displays the message "{}"'.format(expected_notice_msg))
        self.is_equal(expected_notice_msg, notice_msg)
        if current_log_lines is not None:
            expected_log_msg = ADD_INTERMEDIATE_CA
            self.log('TRUST_12 5. System logs the event "{}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
            current_log_lines = log_checker.get_line_count()
        self.log('Open intermediate CA OCSP tab')
        self.wait_until_visible(type=By.XPATH, element=INTERMEDIATE_CA_OCSP_TAB_XPATH).click()
        self.wait_jquery()
        self.log('Click on "ADD" button')
        self.wait_until_visible(type=By.ID, element=INTERMEDIATE_CA_OCSP_ADD_BTN_ID).click()
        self.log('Upload OCSP cert')
        ocsp_upload_btn = self.wait_until_visible(type=By.ID, element=IMPORT_OCSP_CERT_BTN_ID)
        xroad.fill_upload_input(self, ocsp_upload_btn, ocsp_cert)
        self.log('Enter {} to ocsp url'.format(ocsp_url))
        ocsp_url_input = self.wait_until_visible(type=By.ID, element=OCSP_RESPONDER_URL_AREA_ID)
        self.input(ocsp_url_input, ocsp_url)
        self.log('Click "OK"')
        self.wait_until_visible(type=By.ID, element=SUBMIT_OCSP_CERT_AND_URL_BTN_ID).click()
        self.wait_jquery()
        if current_log_lines is not None:
            expected_log_msg = ADD_INTERMEDIATE_CA_OCSP
            self.log('TRUST_12 6. System logs the event "{}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

    return add_intermediate_ca


def test_delete_intermediate_ca(self, ca_name, log_checker=None):
    def delete_intermediate_ca():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.log('Open certification services view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=CERTIFICATION_SERVICES_CSS).click()
        self.wait_jquery()
        self.log('Open CA settings')
        edit_ca_settings(self, ca_name)
        self.log('Open Intermediate CA tab')
        self.wait_until_visible(type=By.XPATH, element=INTERMEDIATE_CA_TAB_XPATH).click()
        self.wait_jquery()
        self.log('Clicking on Intermediate CA "{}"'.format(ca_name))
        self.wait_until_visible(type=By.XPATH, element=INTERMEDIATE_CA_BY_NAME_XPATH.format(ca_name)).click()
        self.log('TRUST_13 1. Clicking on "Delete" button')
        self.wait_until_visible(type=By.ID, element=INTERMEDIATE_CA_DELETE_BTN_ID).click()
        self.wait_jquery()
        try:
            self.by_xpath(INTERMEDIATE_CA_BY_NAME_XPATH.format(ca_name)).click()
            self.log('Deleting CA failed, CA table row exists after deletion')
            assert False
        except:
            self.log('TRUST_13 2. System deletes the intermediate CA information from the system configuration')
            pass
        if current_log_lines is not None:
            expected_log_msg = DELETE_INTERMEDIATE_CA
            self.log('TRUST_13 3. System logs the event "{}"'.format(expected_log_msg))
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)

    return delete_intermediate_ca


def test_view_intermediate_ca(self, ca_name):
    def view_intermediate_ca():
        self.log('Open certification services view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=CERTIFICATION_SERVICES_CSS).click()
        self.wait_jquery()
        self.log('Open CA settings')
        edit_ca_settings(self, ca_name)
        self.log('SERVICE_06 1. Open Intermediate CA tab')
        self.wait_until_visible(type=By.XPATH, element=INTERMEDIATE_CA_TAB_XPATH).click()
        self.wait_jquery()
        self.log('SERVICE_06 2. System displays the list of intermediate CAs')
        self.log('Get intermediate CA {} row'.format(ca_name))
        intermediate_ca_tr = self.wait_until_visible(type=By.XPATH,
                                                     element=INTERMEDIATE_CA_TR_BY_NAME_XPATH.format(ca_name))
        self.log('Get row columns')
        tds = intermediate_ca_tr.find_elements_by_tag_name('td')
        self.log('SERVICE_06 2. The value of the subject common name element from the inermediate CA certificate '
                 'is displayed as the name of the intermediate CA')
        self.is_equal(ca_name, tds[0].text)
        self.log('SERVICE_06 2. The valid from time is displayed in format YYYY-MM-DD HH:MM:SS')
        self.is_true(re.match(DATE_REGEX, tds[1].text))
        self.log('SERVICE_06 2. The valid to time is displayed in format YYYY-MM-DD HH:MM:SS')
        self.is_true(re.match(DATE_REGEX, tds[2].text))

    return view_intermediate_ca


def test_view_intermediate_ca_details(self, ca_name):
    def view_intermediate_ca_details():
        self.log('Open certification services view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=CERTIFICATION_SERVICES_CSS).click()
        self.wait_jquery()
        self.log('Open CA settings')
        edit_ca_settings(self, ca_name)
        self.log('Open Intermediate CA tab')
        self.wait_until_visible(type=By.XPATH, element=INTERMEDIATE_CA_TAB_XPATH).click()
        self.wait_jquery()
        self.log('System displays the list of intermediate CAs')
        self.log('Get intermediate CA {} row'.format(ca_name))
        self.wait_until_visible(type=By.XPATH, element=INTERMEDIATE_CA_BY_NAME_XPATH.format(ca_name)).click()
        self.log('SERVICE_07 1. Open intermediate CA details')
        self.wait_until_visible(type=By.ID, element=INTERMEDIATE_CA_EDIT_BTN_ID).click()
        self.wait_jquery()
        self.log('SERVICE_07 2. System displays the subject distinguished name {}'.format(CA_DISTINGUISHED_NAME))
        self.is_equal(CA_DISTINGUISHED_NAME,
                      self.wait_until_visible(type=By.ID, element=INTERMEDIATE_CA_SUBJECT_DN_ID).text)
        self.log('SERVICE_07 2. System displays the issuer distinguished name {}'.format(CA_DISTINGUISHED_NAME))
        self.is_equal(CA_DISTINGUISHED_NAME, self.by_id(INTERMEDIATE_CA_ISSUER_DN_ID).text)
        self.log('SERVICE_07 2. System displays the valid from time in format YYYY-MM-DD HH:MM:SS')
        self.is_true(re.match(DATE_REGEX, self.by_id(INTERMEDIATE_CA_VALID_FROM_ID).text))
        self.log('SERVICE_07 2. System displays the valid to time in format YYYY-MM-DD HH:MM:SS')
        self.is_true(re.match(DATE_REGEX, self.by_id(INTERMEDIATE_CA_VALID_TO_ID).text))

    return view_intermediate_ca_details
