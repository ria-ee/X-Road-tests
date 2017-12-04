# coding=utf-8
from selenium.webdriver.common.by import By
from view_models import certification_services, sidebar
import re


def test_verify_approved_cert_services(case, ca_name=None):
    '''

    :param case: MainController object
    :param ca_name: string name of the approved certification service
    :return:
    '''
    self = case

    def view_approved_cert_services():
        '''Open "Certification services"'''

        self.log(' UC TRUST_01: 1.CS administrator selects to view the list of approved certification services.')

        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        view_cert_services(self, ca_name)

    return view_approved_cert_services


def view_cert_services(self, ca_name):
    self.log(
        ' UC TRUST_01: 2.System displays the list of approved certification services: Value of the subject common name, The validity period of the service CA certificate.')

    get_row = self.wait_until_visible(type=By.XPATH, element=certification_services.LAST_ADDED_CERT_XPATH).text
    '''Click on approved CN row'''
    self.wait_until_visible(type=By.XPATH, element=certification_services.LAST_ADDED_CERT_XPATH).click()
    '''Split row'''
    cs_row = get_row.split()
    '''Get Approved Certification name'''
    name = cs_row[0]
    '''Get valid from date'''
    valid_from_date = cs_row[1]
    '''Get valid from time'''
    valid_from_time = cs_row[2]
    '''Get valid to date'''
    valid_to_date = cs_row[3]
    '''Get valid to time'''
    valid_to_time = cs_row[4]

    self.log(' UC TRUST_01: 2.Verify the value of the subject common name (CN) element from the certification service.')

    '''Verify the value of the subject common name (CN) element from the certification service'''
    self.is_equal(name, ca_name,
                  msg='The value of the subject common name (CN) element from the certification service is wrong')

    self.log(' UC TRUST_01: 2. Verify the validity period of the service CA certificate.')

    '''"Valid from" date verification'''
    valid_from_date_match = re.match(certification_services.DATE_REGEX, valid_from_date)

    self.is_true(valid_from_date_match,
                 msg='Date is in wrong format')

    '''"Valid from" time verification'''

    valid_from_time_match = re.match(certification_services.TIME_REGEX, valid_from_time)

    self.is_true(valid_from_time_match,
                 msg='Time is in wrong format')

    self.log(' UC TRUST_01: 2. Verify the validity period of the service CA certificate.')

    '''"Valid to" date verification'''
    valid_to_date_match = re.match(certification_services.DATE_REGEX, valid_to_date)

    self.is_true(valid_to_date_match,
                 msg='Date is in wrong format')

    '''"Valid to" time verification'''

    valid_to_time_match = re.match(certification_services.TIME_REGEX, valid_to_time)

    self.is_true(valid_to_time_match,
                 msg='Time is in wrong format')

    self.log(' UC TRUST_01: 2. The following user action options are displayed: Add an approved certification service.')

    add_btn = self.by_id(certification_services.ADD_BTN_ID).is_enabled()
    self.is_true(add_btn,
                 msg='"ADD" button not found')

    self.log(
        ' UC TRUST_01: 2. The following user action options are displayed: View the details of an approved certification service.')

    details_btn = self.by_id(certification_services.DETAILS_BTN_ID).is_enabled()
    self.is_true(details_btn,
                 msg='"Edit" button not found')

    self.log(
        ' UC TRUST_01: 2. The following user action options are displayed: Delete an approved certification service.')

    delete_btn = self.by_id(certification_services.DELETE_BTN_ID).is_enabled()
    self.is_true(delete_btn,
                 msg='"Delete" button not found')
