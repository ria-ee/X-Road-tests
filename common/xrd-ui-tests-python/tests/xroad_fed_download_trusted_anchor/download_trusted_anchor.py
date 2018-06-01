import time
from selenium.webdriver.common.by import By

from tests.xroad_fed_upload_trusted_anchor.upload_trusted_anchor import get_anchor_path
from view_models.global_configuration import TRUSTED_ANCHORS_TAB_CSS
from view_models.sidebar import GLOBAL_CONFIGURATION_CSS
from view_models.trusted_anchor import DOWNLOAD_BTN_XPATH


def test_download_trusted_anchor(self):
    def download_trusted_anchor():
        self.log('Open global configuration view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=GLOBAL_CONFIGURATION_CSS).click()
        self.log('Open "Trusted anchors" tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=TRUSTED_ANCHORS_TAB_CSS).click()
        self.wait_jquery()
        self.log('FED_06 1. "Download a trusted anchor" button is clicked')
        filter(lambda x: x.size['height'] > 0, self.by_xpath(DOWNLOAD_BTN_XPATH, multiple=True))[0].click()
        self.log('FED_06 2. Downloading the file starts')
        self.wait_jquery()
        time.sleep(3)
        self.log('FED_06 3. Downloaded file is saved in the local file system')
        self.is_not_none(get_anchor_path(self))

    return download_trusted_anchor
