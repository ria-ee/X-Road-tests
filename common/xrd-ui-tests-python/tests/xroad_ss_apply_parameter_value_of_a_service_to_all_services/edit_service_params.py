from selenium.webdriver.common.by import By

from view_models import clients_table_vm, popups
from view_models.clients_table_vm import get_service_by_index, get_service_url_by_index, get_service_timeout_by_index
from view_models.log_constants import EDIT_SERVICE_PARAMS
from view_models.popups import EDIT_WSDL_BUTTON_ID, \
    EDIT_SERVICE_POPUP_TIMEOUT_ID, EDIT_SERVICE_POPUP_OK_BTN_XPATH, EDIT_SERVICE_POPUP_URL_ID, \
    EDIT_SERVICE_POPUP_TIMEOUT_APPLY_ALL_CHECKBOX_ID, \
    EDIT_SERVICE_POPUP_URL_APPLY_ALL_CHECKBOX_ID, EDIT_SERVICE_POPUP_TLS_APPLY_ALL_CHECKBOX_ID


def test_edit_tls_to_all(self, client, client_name, wsdl_url, log_checker=None):
    def edit_service_parameters():
        try:
            current_log_lines = None
            if log_checker is not None:
                current_log_lines = log_checker.get_line_count()
            self.log('Open client services tab')
            clients_table_vm.open_client_popup_services(self, client=client, client_name=client_name)
            self.log('Expanding WSDL services')
            wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_url)
            wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_index)
            wsdl_row.find_element_by_css_selector(popups.CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS).click()
            self.log('Get first service url')
            service_0_row = get_service_by_index(self, 0)
            service_0_url = service_0_row.find_elements_by_tag_name('td')[3].text
            self.log('Get second service url')
            service_1_row = get_service_by_index(self, 1)
            service_1_url = service_1_row.find_elements_by_tag_name('td')[3].text
            self.log('Checking if second service url does not start with https')
            self.is_false(service_1_url.startswith('https'))
            self.log('Click on first row')
            service_0_row.click()
            self.log('Open service edit dialogue')
            self.wait_until_visible(type=By.ID, element=EDIT_WSDL_BUTTON_ID).click()
            self.log('Replacing url protocol with https')
            https_url = service_0_url.replace('http:', 'https:')
            url_input = self.wait_until_visible(type=By.ID, element=EDIT_SERVICE_POPUP_URL_ID)
            self.log('Changing service url to https one')
            self.input(url_input, https_url)
            self.log('SERVICE_22 1. Checking apply TLS parameter to all the services in the WSDL')
            self.wait_until_visible(type=By.ID, element=EDIT_SERVICE_POPUP_TLS_APPLY_ALL_CHECKBOX_ID).click()
            self.log('Clicking "OK"')
            self.by_xpath(EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
            self.wait_jquery()
            if current_log_lines is not None:
                expected_log_msg = EDIT_SERVICE_PARAMS
                self.log('SERVICE_22 3. System logs the event {}'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)
            self.log('SERVICE_22 2. System saves the parameter value for every service described in the same WSDL')
            service_0_row = get_service_by_index(self, 0)
            self.is_not_none(service_0_row.find_element_by_class_name('fa-lock'))
            service_1_row = get_service_by_index(self, 1)
            self.log('SERVICE_22 TLS verification option is changed only for the services '
                     'where the protocol part of the service address is "https"')
            self.log('Checking if second service(http) did not get affected by TLS change')
            try:
                service_1_row.find_element_by_class_name('fa-lock')
                self.log('Second service(http) should not have TLS option checked')
                assert False
            except:
                pass

        finally:
            self.log('Restore first service url')
            self.log('Clicking on first service row')
            service_0_row.click()
            self.log('Open edit dialogue')
            self.wait_until_visible(type=By.ID, element=EDIT_WSDL_BUTTON_ID).click()
            self.log('Restore url value')
            url_input = self.wait_until_visible(type=By.ID, element=EDIT_SERVICE_POPUP_URL_ID)
            self.input(url_input, service_0_url)
            self.log('Click "OK"')
            self.by_xpath(EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
            self.wait_jquery()

    return edit_service_parameters


def test_edit_url_to_all(self, client, client_name, wsdl_url):
    def edit_url_to_all():
        try:
            self.log('Open client services tab')
            clients_table_vm.open_client_popup_services(self, client=client, client_name=client_name)
            self.log('Expanding WSDL services')
            wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_url)
            wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_index)
            wsdl_row.find_element_by_css_selector(popups.CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS).click()

            self.log('Get first service row')
            service_0_row = get_service_by_index(self, 0)
            self.log('Get second service url')
            service_1_url = get_service_url_by_index(self, 1)
            self.log('Click on first service')
            service_0_row.click()
            self.log('Open service edit dialogue')
            self.wait_until_visible(type=By.ID, element=EDIT_WSDL_BUTTON_ID).click()
            self.log('SERVICE_22 1. Checking apply url to all the services in the WSDL')
            self.wait_until_visible(type=By.ID, element=EDIT_SERVICE_POPUP_URL_APPLY_ALL_CHECKBOX_ID).click()
            self.log('Clicking "OK"')
            self.by_xpath(EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
            self.wait_jquery()
            self.log('SERVICE_22 2. System saves the parameter value for every service described in the same WSDL')
            self.log('Checking if second url is same as first')
            self.is_equal(get_service_url_by_index(self, 0), get_service_url_by_index(self, 1))
        finally:
            self.log('Restore second service url')
            self.log('Click on second service')
            get_service_by_index(self, 1).click()
            self.log('Open edit dialogue')
            self.wait_until_visible(type=By.ID, element=EDIT_WSDL_BUTTON_ID).click()
            self.log('Restore url value')
            url_input = self.wait_until_visible(type=By.ID, element=EDIT_SERVICE_POPUP_URL_ID)
            self.input(url_input, service_1_url)
            self.log('Click "OK"')
            self.by_xpath(EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
            self.wait_jquery()

    return edit_url_to_all


def test_edit_timeout_to_all(self, client, client_name, wsdl_url):
    def edit_timeout_to_all():
        self.log('Open client services tab')
        clients_table_vm.open_client_popup_services(self, client=client, client_name=client_name)
        self.log('Expanding wsdl services')
        wsdl_index = clients_table_vm.find_wsdl_by_name(self, wsdl_url)
        wsdl_row = clients_table_vm.client_services_popup_get_wsdl(self, wsdl_index=wsdl_index)
        wsdl_row.find_element_by_css_selector(popups.CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS).click()

        self.log('Click on first service row')
        get_service_by_index(self, 0).click()
        self.log('Open edit dialogue')
        self.wait_until_visible(type=By.ID, element=EDIT_WSDL_BUTTON_ID).click()
        self.log('SERVICE_22 1. Checking apply timeout parameter to all the services in the WSDL')
        self.wait_until_visible(type=By.ID, element=EDIT_SERVICE_POPUP_TIMEOUT_APPLY_ALL_CHECKBOX_ID).click()
        new_value = '59'
        self.log('Setting new timeout value')
        timeout_input = self.wait_until_visible(type=By.ID, element=EDIT_SERVICE_POPUP_TIMEOUT_ID)
        self.input(timeout_input, new_value)
        self.log('Click "OK"')
        self.by_xpath(EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
        self.log('SERVICE_22 2. System saves the parameter value for every service in the same WSDL')
        self.is_equal(get_service_timeout_by_index(self, 0), get_service_timeout_by_index(self, 1))

    return edit_timeout_to_all
