import fileinput
import os
import time

from selenium.webdriver.common.by import By

from helpers.xroad import fill_upload_input
from view_models.global_configuration import ANCHOR_FILE_DOENLOAD_BTN_ID, TRUSTED_ANCHORS_TAB_CSS
from view_models.log_constants import ADD_TRUSTED_ANCHOR_FAIL, ADD_TRUSTED_ANCHOR
from view_models.messages import ERROR_MESSAGE_CSS, UPLOAD_ANCHOR_SAME_INSTANCE_ERROR, \
    UPLOAD_ANCHOR_INTERNAL_CONF_ERROR, UPLOAD_ANCHOR_UNKNOWN_ERROR, UPLOAD_ANCHOR_INVALID_FILE_ERROR, \
    UPLOAD_ANCHOR_URL_UNREACHABLE_ERROR, UPLOAD_ANCHOR_EXPIRED_ERROR, UPLOAD_ANCHOR_SIGNATURE_ERROR
from view_models.popups import FILE_UPLOAD_BROWSE_BUTTON_ID, FILE_UPLOAD_SUBMIT_BUTTON_ID
from view_models.sidebar import GLOBAL_CONFIGURATION_CSS
from view_models.trusted_anchor import ANCHOR_VALIDATOR_SCRIPT, ANCHOR_FILE_PREFIX, ANCHOR_GENERATED_AT_CSS, \
    UPLOAD_ANCHOR_BTN_ID, SAVE_ANCHOR_BTN_ID, TRUSTED_ANCHOR_BY_IDENTIFIER_XPATH


def download_external_conf(self):
    self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_CONFIGURATION_CSS).click()
    self.wait_until_visible(type=By.ID, element=ANCHOR_FILE_DOENLOAD_BTN_ID).click()
    time.sleep(3)


def test_upload_anchor(self, log_checker=None, same_instance=False, download_error=False, expired=False,
                       invalid_signature=False, internal=False, other_error=False, invalid_file=False,
                       generated_at_check=False, new_identifier=None):
    def upload_anchor():
        current_log_lines = None
        if log_checker:
            current_log_lines = log_checker.get_line_count()
        self.log('Open global configuration view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_CONFIGURATION_CSS).click()
        self.log('Open "Trusted anchors" tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=TRUSTED_ANCHORS_TAB_CSS).click()
        self.wait_jquery()
        if generated_at_check:
            self.log('Getting current anchor "Generated at"')
            generated_at_before = get_generated_at(self)
        self.log('FED_02 1. Clicking on "Upload anchor" button')
        self.wait_until_visible(type=By.ID, element=UPLOAD_ANCHOR_BTN_ID).click()
        upload_btn = self.wait_until_visible(type=By.ID, element=FILE_UPLOAD_BROWSE_BUTTON_ID)
        self.log('FED_02 2. Filling upload input with anchor')
        fill_upload_input(self, upload_btn, get_anchor_path(self))
        self.log('Clicking on "OK" button')
        self.wait_until_visible(type=By.ID, element=FILE_UPLOAD_SUBMIT_BUTTON_ID).click()
        if invalid_file:
            self.log('FED_02 3a Verification of the download configuration failed for unknown reason')
            expected_error_msg = UPLOAD_ANCHOR_INVALID_FILE_ERROR
            self.log('FED_02 3a.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            return
        elif same_instance:
            self.log('FED_02 4a The anchor points to a configuration source of the local X-Road Instance')
            expected_error_msg = UPLOAD_ANCHOR_SAME_INSTANCE_ERROR
            self.log('FED_02 4a.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            return
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=SAVE_ANCHOR_BTN_ID).click()
        if download_error:
            self.log('FED_02 7a Downloading of the configuration fails')
            expected_error_msg = UPLOAD_ANCHOR_URL_UNREACHABLE_ERROR
            self.log('FED_02 7a.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            if current_log_lines:
                expected_log_msg = ADD_TRUSTED_ANCHOR_FAIL
                self.log('FED_02 7a.2 System logs the event "{}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
        elif expired:
            self.log('FED_02 7b The Downloaded configuration is expired')
            expected_error_msg = UPLOAD_ANCHOR_EXPIRED_ERROR
            self.log('FED_02 7b.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            if current_log_lines:
                expected_log_msg = ADD_TRUSTED_ANCHOR_FAIL
                self.log('FED_02 7b.2 System logs the event "{}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
        elif invalid_signature:
            self.log('FED_02 7c Verification of the signature value of the downloaded configuration failed')
            expected_error_msg = UPLOAD_ANCHOR_SIGNATURE_ERROR
            self.log('FED_02 7c.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            if current_log_lines:
                expected_log_msg = ADD_TRUSTED_ANCHOR_FAIL
                self.log('FED_02 7c.2 System logs the event "{}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
        elif internal:
            self.log('FED_02 7d The download configuration is internal not external')
            expected_error_msg = UPLOAD_ANCHOR_INTERNAL_CONF_ERROR
            self.log('FED_02 7d.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            if current_log_lines:
                expected_log_msg = ADD_TRUSTED_ANCHOR_FAIL
                self.log('FED_02 7d.2 System logs the event "{}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
        elif other_error:
            self.log('FED_02 7e Verification of the download configuration failed for unknown reason')
            expected_error_msg = UPLOAD_ANCHOR_UNKNOWN_ERROR
            self.log('FED_02 7e.1 System displays the error message "{}"'.format(expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            if current_log_lines:
                expected_log_msg = ADD_TRUSTED_ANCHOR_FAIL
                self.log('FED_02 7e.2 System logs the event "{}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
        else:
            self.wait_jquery()
            if new_identifier:
                self.is_not_none(self.wait_until_visible(type=By.XPATH,
                                                         element=TRUSTED_ANCHOR_BY_IDENTIFIER_XPATH.format(
                                                             new_identifier)))
            elif generated_at_check:
                self.log('Getting new anchor "Generated at"')
                generated_at_after = get_generated_at(self)
                self.log(
                    'FED_02 8. System verifies that an anchor with the same instance identifier as the uploaded one'
                    'exists in the system configuration and replaces the existing anchor with the uploaded one')
                self.not_equal(generated_at_before, generated_at_after)
            if current_log_lines:
                expected_log_msg = ADD_TRUSTED_ANCHOR
                self.log('FED_02 9. System logs the event {}'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)

    return upload_anchor


def get_generated_at(self):
    return filter(lambda x: x.size['height'] > 0, self.by_css(ANCHOR_GENERATED_AT_CSS, multiple=True))[0].text


def get_anchor_path(self):
    anchor_file_name = filter(lambda x: ANCHOR_FILE_PREFIX in x, os.listdir(self.download_dir))[0]
    anchor_path = self.get_download_path(anchor_file_name)
    return os.path.abspath(anchor_path)


def set_validator_script_to(sshclient, status):
    sshclient.exec_command('sh -c "printf \'{0}\' > {1}"'.format('#!/bin/bash\n\nexit {0}'.format(status),
                                                                 ANCHOR_VALIDATOR_SCRIPT),
                           sudo=True)


def replace_in_file(self, word, replacement):
    anchor_path = get_anchor_path(self)
    anchor_file = fileinput.input(anchor_path, inplace=True)
    for line in anchor_file:
        print line.replace(word, replacement),
    anchor_file.close()
