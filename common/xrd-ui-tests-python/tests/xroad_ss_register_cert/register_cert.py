import time
from selenium.webdriver.common.by import By

from view_models.keys_and_certificates_table import CERT_BY_KEY_LABEL, DELETE_BTN_ID
from view_models.popups import confirm_dialog_click
from view_models.sidebar import KEYSANDCERTIFICATES_BTN_CSS


def delete_auth_cert(self, auth_key_label):
    self.log('SS_39 Delete certificate')
    self.log('Opening keys and certificates view')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()
    self.log('Clicking on authentication certificate {0}'.format(auth_key_label))
    self.wait_until_visible(type=By.XPATH, element=CERT_BY_KEY_LABEL.format(auth_key_label)).click()
    self.log('Waiting until "Delete" button is clickable')
    delete_btn = self.by_id(DELETE_BTN_ID)
    timeout = 120
    while not delete_btn.is_enabled() or timeout == 0:
        time.sleep(30)
        timeout -= 30
        self.reset_page()
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=CERT_BY_KEY_LABEL.format(auth_key_label)).click()
        delete_btn = self.by_id(DELETE_BTN_ID)
    delete_btn.click()
    self.log('Confirming deletion popup')
    confirm_dialog_click(self)
    self.wait_jquery()
