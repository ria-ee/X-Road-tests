import re

from selenium.webdriver.common.by import By

from tests.xroad_fed_upload_trusted_anchor.upload_trusted_anchor import get_generated_at
from view_models.global_configuration import TRUSTED_ANCHORS_TAB_CSS
from view_models.sidebar import GLOBAL_CONFIGURATION_CSS
from view_models.trusted_anchor import TRUSTED_ANCHOR_BY_IDENTIFIER_XPATH, INSTANCE_IDENTIFIER, UPLOAD_ANCHOR_BTN_ID, \
    DOWNLOAD_BTN_XPATH, DELETE_BTN_XPATH, ANCHOR_HASH, ANCHOR_HASH_REGEX, GENERATED_AT_REGEX


def test_view_trusted_anchors(self):
    def view_trusted_anchors():
        self.log('Open global configuration view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_CONFIGURATION_CSS).click()
        self.log('FED_01 1. Open "Trusted anchors" tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=TRUSTED_ANCHORS_TAB_CSS).click()
        self.wait_jquery()
        self.log('FED_01 2. System displays trusted anchors')
        self.log('FED_02 2. The instance identifier of the X-Road instance the trusted anchor '
                 'originates from is visible')
        self.wait_until_visible(type=By.XPATH, element=TRUSTED_ANCHOR_BY_IDENTIFIER_XPATH.format(INSTANCE_IDENTIFIER))
        self.log('FED_02 2. The SHA-224 hash value of the trusted anchor file is visible')
        hash = filter(lambda x: x.size['height'] > 0, self.by_css(ANCHOR_HASH, multiple=True))[0].text
        self.is_true(re.match(ANCHOR_HASH_REGEX, hash))
        self.log('FED_02 2. The generation date and time (UTC) of the trusted anchor file is visible')
        generated_at = get_generated_at(self)
        self.is_true(re.match(GENERATED_AT_REGEX, generated_at))
        self.log('FED_02 The following user action options are displayed')
        self.log('FED_02 "Upload a trusted anchor" button is visible')
        self.is_not_none(self.by_id(UPLOAD_ANCHOR_BTN_ID))
        self.log('FED_02 "Download a trusted anchor" button is visible')
        self.is_true(len(filter(lambda x: x.size['height'] > 0, self.by_xpath(DOWNLOAD_BTN_XPATH, multiple=True))) > 0)
        self.log('FED_02 "Delete a trusted anchor" button is visible')
        self.is_true(len(filter(lambda x: x.size['height'] > 0, self.by_xpath(DELETE_BTN_XPATH, multiple=True))) > 0)

    return view_trusted_anchors
