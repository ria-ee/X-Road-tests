import re
import time

import requests
from selenium.webdriver.common.by import By

from helpers.ssh_server_actions import get_key_conf_keys_count, get_keyconf_update_timeout
from view_models import popups
from view_models.keys_and_certificates_table import DELETE_BTN_ID, KEY_TABLE_ROW_BY_LABEL_XPATH
from view_models.log_constants import DELETE_KEY, DELETE_KEY_FAIL
from view_models.messages import ERROR_MESSAGE_CSS, KEY_DELETE_FAILED_CONNECTION_REFUSED, \
    KEY_DELETE_FAILED_SERVICE_DISABLED_ERROR_MSG_REGEX
from view_models.popups import CONFIRM_POPUP_TEXT_AREA_ID, CONFIRM_POPUP_CANCEL_BTN_XPATH


def delete_key_from_configuration(self, key_label, sshclient, try_cancel=False, log_checker=None,
                                  unregister_request_fail=False, request_sending_fail=False, has_auth_certs=True):
    self.log('*** SS_35 Delete a Key from the System Configuration')
    self.log('Get authentication keys in system configuration')
    key_count = get_key_conf_keys_count(sshclient, "AUTHENTICATION")
    current_log_lines = None
    if log_checker:
        current_log_lines = log_checker.get_line_count()
    self.log('Clicking on "{}" key'.format(key_label))
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=KEY_TABLE_ROW_BY_LABEL_XPATH.format(key_label)).click()
    self.wait_jquery()
    self.log('SS_35 1. Clicking on "Delete" button')
    self.wait_until_visible(type=By.ID, element=DELETE_BTN_ID).click()
    self.wait_jquery()
    if has_auth_certs:
        self.log('SS_35 2. Checking if auth cert unregistering message is present and text as expected')
        warning = self.wait_until_visible(type=By.ID, element=CONFIRM_POPUP_TEXT_AREA_ID).text
        self.is_equal('Key \'{}\' has certificates that need to be unregistered before deletion. '
                      'Continue with unregistration and deletion of associated certifcates and the key from '
                      'server configuration?'.format(key_label), warning)
    if try_cancel:
        self.log('SS_35 3a. Canceling key deletion')
        self.wait_until_visible(type=By.XPATH, element=CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        self.log('Checking if key is still present in keys view')
        self.is_not_none(self.wait_until_visible(type=By.XPATH, element=KEY_TABLE_ROW_BY_LABEL_XPATH.format(key_label)))
        timeout = get_keyconf_update_timeout(sshclient)
        self.log('Waiting {} seconds for keyconf update'.format(timeout))
        time.sleep(timeout)
        self.log('Checking if same amount of keys still present in system configuration')
        key_count_after_canceling = get_key_conf_keys_count(sshclient, "AUTHENTICATION")
        self.is_equal(key_count, key_count_after_canceling, msg='{}:{}'.format(key_count, key_count_after_canceling))
    else:
        self.log('SS_35 3. Confirm key deletion')
        popups.confirm_dialog_click(self)
        self.wait_jquery()
        if request_sending_fail:
            self.log('SS_42 1-2a. The creating or sending of the deletion request failed')
            expected_error_msg = KEY_DELETE_FAILED_CONNECTION_REFUSED
            self.log('SS_35 4a. The process of unregistering certificates terminated with an error message:\n{}'.format(
                expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_equal(expected_error_msg, error_msg)
            timeout = get_keyconf_update_timeout(sshclient)
            self.log('Waiting {} seconds for keyconf update'.format(timeout))
            time.sleep(timeout)
            self.log('Checking if key count is same after deleting')
            key_count_after_canceling = get_key_conf_keys_count(sshclient, "AUTHENTICATION")
            self.is_equal(key_count, key_count_after_canceling)
            if current_log_lines:
                expected_log_msg = DELETE_KEY_FAIL
                self.log('SS_35 4a.2 System logs the event "{}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
        elif unregister_request_fail:
            self.log('SS_42 3a. Unregistering response was an error message')
            expected_error_msg = KEY_DELETE_FAILED_SERVICE_DISABLED_ERROR_MSG_REGEX
            self.log('SS_35 4a. The process of unregistering certificates terminated with an error message:\n{}'.format(
                expected_error_msg))
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=ERROR_MESSAGE_CSS).text
            self.is_true(re.match(expected_error_msg, error_msg), msg='Expected error message regex: {}\nGot: {}'.format(expected_error_msg, error_msg))
            if current_log_lines:
                expected_log_msg = DELETE_KEY_FAIL
                self.log('SS_35 4a.2 System logs the event "{}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
            timeout = get_keyconf_update_timeout(sshclient)
            self.log('Waiting {} seconds for keyconf update'.format(timeout))
            time.sleep(timeout)
            self.log('Checking if key count is same after deleting')
            key_count_after_canceling = get_key_conf_keys_count(sshclient, "AUTHENTICATION")
            self.is_equal(key_count, key_count_after_canceling)
        else:
            if current_log_lines:
                expected_log_msg = DELETE_KEY
                self.log('SS_35 7. System logs the event "{}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
            if has_auth_certs:
                self.log('SS_42 Authentication certificates unregistered')
                timeout = get_keyconf_update_timeout(sshclient)
                self.log('Waiting {} seconds for keyconf update'.format(timeout))
                time.sleep(timeout)
                self.log('SS_35 Checking if keys were deleted in system configuration')
                key_count_after = get_key_conf_keys_count(sshclient, "AUTHENTICATION")
                self.is_true(key_count_after < key_count)


def wait_until_proxy_up(address, self, timeout=1200):
    start_time = int(time.time())
    self.log('Waiting for xroad-proxy startup (timeout {} s)...'.format(timeout))
    while True:
        try:
            requests.get(address, verify=False)
        except TypeError:
            # If we get a TypeError, we have an older version of Requests/urllib3 that fails when checking the
            # certificate returns an error. Although a workaround, this is also an expected outcome.
            self.log('xroad-proxy started up')
            return
        except requests.HTTPError as e:
            if e.message and 'SSL' in e.strerror:
                self.log('xroad-proxy started up')
                return
            pass
        except Exception as e:
            if start_time != -1 and int(time.time()) - start_time > timeout:
                self.log('Timeout ({} seconds) while waiting for xroad-proxy startup'.format(timeout))
                self.log('Exception: {}'.format(e.message))
                return
            pass
        time.sleep(1) # Do not flood the server with requests
