# coding=utf-8
from selenium.webdriver.common.by import By
from view_models import certification_services, sidebar, ss_system_parameters
import re
import time


def test_ca_cs_details_view_cert(case, profile_class=None):
    '''

    :param case: MainController object
    :param profile_class: string The fully qualified name of the Java class
    :return:
    '''
    self = case

    def view_cert():
        '''Open "Certification services"'''
        self.wait_until_visible(self.by_css(sidebar.CERTIFICATION_SERVICES_CSS)).click()
        self.wait_jquery()

        view_cert_data(self, profile_class=profile_class)

    return view_cert


def view_cert_data(self, profile_class=None):
    '''Get approved CA row'''
    service_row = self.wait_until_visible(type=By.XPATH, element=certification_services.LAST_ADDED_CERT_XPATH)

    '''Double click on approved CA row'''
    self.double_click(service_row)

    '''Click on "Edit button"'''
    self.by_id(certification_services.DETAILS_BTN_ID).click()

    self.log('UC TRUST_04 1.CS administrator selects to view the settings of a certification service.')

    self.wait_until_visible(type=By.XPATH, element=certification_services.CA_SETTINGS_TAB_XPATH).click()
    self.wait_jquery()

    self.log(
        'UC TRUST_04: 2.System displays the following settings. Usage restrictions for the certificates issued by the certification service.')

    auth_checkbox = self.wait_until_visible(certification_services.EDIT_CA_AUTH_ONLY_CHECKBOX_XPATH,
                                            By.XPATH).is_enabled()
    self.is_true(auth_checkbox, msg='Authentication chechkbox not found')

    '''Click on authentication checkbox'''
    self.wait_until_visible(certification_services.EDIT_CA_AUTH_ONLY_CHECKBOX_XPATH, By.XPATH).click()

    self.log(
        'UC TRUST_04: 2.System displays the following settings. The fully qualified name of the Java class that describes the certificate profile for certificates issued by the certification service.')

    '''Get profile info'''
    profile_info_area = self.wait_until_visible(type=By.XPATH,
                                                element=certification_services.EDIT_CERTIFICATE_PROFILE_INFO_AREA_XPATH)
    profile_info = profile_info_area.get_attribute("value")
    '''Verify profile info'''

    self.is_equal(profile_info, profile_class,
                  msg='The name of the Java class that describes the certificate profile is wrong')

    self.log(
        'UC TRUST_04: 2. The following user action options are displayed:edit the settings of the certification service')

    '''Verify "Save" button'''
    save_button_id = self.wait_until_visible(type=By.ID,
                                             element=certification_services.SAVE_CA_SETTINGS_BTN_ID).is_enabled()
    self.is_true(save_button_id, msg='"Save" button not found')
