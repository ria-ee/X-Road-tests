import re

from selenium.webdriver.common.by import By

from view_models.members_table import MANAGEMENT_REQUEST_TABLE_ID, get_requests_row_by_td_text, \
    CERTIFICATE_REGISTRATION, CLIENT_REGISTRATION, CERTIFICATE_DELETION, CLIENT_DELETION, \
    MANAGEMENT_REQUEST_DETAILS_BTN_ID, REQUEST_SOURCES
from view_models.sidebar import MANAGEMENT_REQUESTS_CSS


def check_column_data(self, ths, request_type, registration=True):
    request_row = self.by_xpath(get_requests_row_by_td_text(request_type))
    tds = request_row.find_elements_by_tag_name('td')
    self.log('Click on request row')
    request_row.click()
    date_regex = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    column_count = 8
    self.log('Check if details button exists')
    self.is_not_none(self.by_id(MANAGEMENT_REQUEST_DETAILS_BTN_ID))
    if registration:
        """Only registration requests have status in last column"""
        column_count = 9
    for i in range(0, column_count):
        column_header = ths[i].text
        column_data = tds[i].text
        self.log('{0} request: Checking column: {1}'.format(request_type, column_header))
        if column_header == 'Created':
            self.is_true(re.match(date_regex, column_data))
        elif column_header == 'Source':
            self.is_true(column_data in REQUEST_SOURCES)
        else:
            assert len(column_data) > 0


def test_view_management_request(self):
    def view_requests():
        self.log('MEMBER_34 1. Management requests table is opened')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=MANAGEMENT_REQUESTS_CSS).click()
        self.wait_until_visible(type=By.ID, element=MANAGEMENT_REQUEST_TABLE_ID)
        self.wait_jquery()
        self.log('MEMBER_34 2. System displays the list of management requests')
        table_headers = self.driver.find_elements_by_tag_name('th')
        check_column_data(self, table_headers, CERTIFICATE_REGISTRATION)
        check_column_data(self, table_headers, CLIENT_REGISTRATION)
        check_column_data(self, table_headers, CERTIFICATE_DELETION, registration=False)
        check_column_data(self, table_headers, CLIENT_DELETION, registration=False)

    return view_requests
