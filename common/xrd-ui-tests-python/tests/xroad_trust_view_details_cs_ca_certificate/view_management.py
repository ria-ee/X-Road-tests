# coding=utf-8
from selenium.webdriver.common.by import By
from view_models import certification_services, sidebar, ss_system_parameters
import re
import time


def test_ca_cs_details_view_cert(case, ca_host=None):
    '''
    :param case: MainController object
    :return:
    '''
    self = case

    def view_cert():
        '''Open "Certification services"'''
        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        view_cert_data(self,ca_host=ca_host)

    return view_cert


def view_cert_data(self,ca_host=None):
    '''Get approved CA row'''
    service_row = self.wait_until_visible(type=By.XPATH, element=certification_services.LAST_ADDED_CERT_XPATH)

    '''Double click on approved CA row'''
    self.double_click(service_row)

    self.log('UC TRUST_03: 1.CS administrator selects to view a certificate')

    '''Click on "VIEW CERTIFICATE" button'''
    self.by_id(certification_services.CA_DETAILS_VIEW_CERT).click()
    self.wait_jquery()
    time.sleep(2)

    self.log('UC TRUST_03: 2.System displays the following information: the contents of the certificate.')

    '''Get certificate data'''
    cert_dump = self.by_id(certification_services.CA_DETAILS_VIEW_CERT_DUMP).text

    text = ['Serial Number:', 'Signature Algorithm: sha256WithRSAEncryption', 'X509v3 Subject Key Identifier:', 'X509v3 Authority Key Identifier:']
    if not (re.search('Issuer: C = [A-Z]+, O = [A-Z]+, CN = {0}'.format(ca_host), cert_dump) and re.search('Subject: C = [A-Z]+, O = [A-Z]+, CN = {0}'.format(ca_host), cert_dump) and all(x in cert_dump for x in text )):
        raise Exception('Problems with Certificate details content')

    '''Get SHA-1'''
    sha1 = self.by_id(certification_services.CA_DETAILS_VIEW_CERT_SHA1).text

    self.log('UC TRUST_03: 2.System displays the following information: the SHA-1 hash value of the certificate.')

    '''Verify SHA-1'''
    sha1_match = re.match(ss_system_parameters.SHA1_REGEX, sha1)
    self.is_true(sha1_match,
                 msg='SHA-1 in wrong format')
