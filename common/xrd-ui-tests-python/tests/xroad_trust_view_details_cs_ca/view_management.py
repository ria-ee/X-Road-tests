# coding=utf-8
from selenium.webdriver.common.by import By
from view_models import certification_services, sidebar
import re


def test_view_details_cert_services(case, distinguished_name=None):
    '''

    :param case: MainController object
    :return:
    '''
    self = case

    def view_details():
        '''Open "Certification services"'''

        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        view_cert_services_details(self, distinguished_name=distinguished_name)

    return view_details


def view_cert_services_details(self, distinguished_name=None):
    self.log('UC TRUST_02: 1.CS administrator selects to view the details of an approved certification service.')

    '''Get approved CA row'''
    service_row = self.wait_until_visible(type=By.XPATH, element=certification_services.LAST_ADDED_CERT_XPATH)

    '''Double click on approved CA row'''
    self.double_click(service_row)
    '''Click on "Edit" button'''
    self.by_id(certification_services.DETAILS_BTN_ID).click()
    '''Get distinguished issuer name'''
    distinguished_issuer = self.by_id(certification_services.CA_DETAILS_ISSUER_DISTINGUISHED).text

    '''Get distinguished subject name'''
    distinguished_subject = self.by_id(certification_services.CA_DETAILS_SUBJECT_DISTINGUISHED).text
    '''Get CA valid from time'''
    ca_valid_from = self.by_id(certification_services.CA_DETAILS_VALID_FROM).text
    '''Get CA valid to time'''
    ca_valid_to = self.by_id(certification_services.CA_DETAILS_VALID_TO).text
    self.log(
        ' UC TRUST_02: 2.System displays the following information: the distinguished name (DN) of the subject of the certification service CA certificate.')


    self.is_equal(distinguished_issuer, distinguished_name,
                  msg='The value of the subject common name (CN) element from the certification service is wrong')

    self.log(
        ' UC TRUST_02: 2.System displays the following information: the distinguished name (DN) of the issuer of the certification service CA certificate.')

    self.is_equal(distinguished_subject, distinguished_name,
                  msg='The value of the subject common name (CN) element from the certification service is wrong')

    self.log(
        ' UC TRUST_02: 2.System displays the following information: the validity period of the certification service CA certificate.')

    '''"Valid from" verification'''
    valid_from_date_match = re.match(certification_services.DATE_TIME_REGEX, ca_valid_from)

    self.is_true(valid_from_date_match,
                 msg='"Valid from" is in wrong forma')

    self.log(
        ' UC TRUST_02: 2.System displays the following information: the validity period of the certification service CA certificate.')

    '''"Valid to" verification'''
    valid_to_date_match = re.match(certification_services.DATE_TIME_REGEX, ca_valid_to)

    self.is_true(valid_to_date_match,
                 msg='"Valid to" is in wrong format')

    self.log(
        ' UC TRUST_02: 2.The following user action options are displayed: view the settings of the certification service CA.')

    ca_settings_tab = self.wait_until_visible(type=By.XPATH,
                                              element=certification_services.CA_SETTINGS_TAB_XPATH).is_enabled()

    self.is_true(ca_settings_tab,
                 msg='"CA Settings" tab not found')

    self.log(
        ' UC TRUST_02: 2.The following user action options are displayed: view the OCSP responders configured for the certification service CA.')

    ocsp_respond_tab = self.by_xpath(certification_services.OCSP_RESPONSE_TAB).is_enabled()
    self.is_true(ocsp_respond_tab,
                 msg='"OCSP Responders" tab not found')

    self.log(
        ' UC TRUST_02: 2.The following user action options are displayed: view the intermediate CAs configured for the certification service.')
    intermediate_ca_tab = self.by_xpath(certification_services.INTERMEDIATE_CA_TAB).is_enabled()
    self.is_true(intermediate_ca_tab,
                 msg='"Intermediate CAs" tab not found')
