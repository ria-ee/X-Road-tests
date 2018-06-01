import time

from selenium.webdriver.common.by import By

from view_models import members_table
from view_models.cs_security_servers import SECURITY_SERVER_MANAGEMENT_PROVIDER_EDIT_BTN_ID, MEMBERS_TABLE_ID, \
    SELECT_MEMBER_BTN_XPATH, SECURITY_SERVER_MANAGEMENT_PROVIDER_ID
from view_models.log_constants import EDIT_MANAGEMENT_SERVICE_PROVIDER
from view_models.sidebar import SYSTEM_SETTINGS_BTN_CSS


def edit_management_service(self, new_provider, log_checker=None):
    def management_service_edit():
        current_log_lines = None
        if log_checker is not None:
            current_log_lines = log_checker.get_line_count()
        self.log('Open system settings tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=SYSTEM_SETTINGS_BTN_CSS).click()
        self.wait_jquery()
        self.log('Get current provider field data')
        old_provider = self.wait_until_visible(type=By.ID,
                                               element=SECURITY_SERVER_MANAGEMENT_PROVIDER_ID).get_attribute('value')
        self.log('MEMBER_33 1. Edit management service provider button is clicked')
        self.wait_until_visible(type=By.ID, element=SECURITY_SERVER_MANAGEMENT_PROVIDER_EDIT_BTN_ID).click()
        self.log('MEMBER_33 2. Selecting member from the list of X-Road members subsystems')
        table = self.wait_until_visible(type=By.ID, element=MEMBERS_TABLE_ID)
        self.wait_jquery()
        members_table.get_row_by_columns(table,
                                         [new_provider['name'],
                                          new_provider['code'],
                                          new_provider['class'],
                                          new_provider['subsystem'],
                                          new_provider['instance'],
                                          new_provider['type']]).click()

        self.log('MEMBER_33 3. Select button is pressed')
        self.wait_until_visible(type=By.XPATH, element=SELECT_MEMBER_BTN_XPATH).click()
        self.wait_jquery()
        if current_log_lines is not None:
            expected_log_msg = EDIT_MANAGEMENT_SERVICE_PROVIDER
            self.log('MEMBER_33 4. System logs the event {0}'.format(expected_log_msg))
            time.sleep(1.5)
            logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
            self.is_true(logs_found)
        self.log('Checking if provider field changed after editing')
        provider_after_edit = self.wait_until_visible(type=By.ID,
                                                      element=SECURITY_SERVER_MANAGEMENT_PROVIDER_ID).get_attribute('value')
        self.not_equal(old_provider, provider_after_edit)

    return management_service_edit
