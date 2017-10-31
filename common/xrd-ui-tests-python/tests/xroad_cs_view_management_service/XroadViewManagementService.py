from selenium.webdriver.common.by import By

from view_models.cs_security_servers import SECURITY_SERVER_MANAGEMENT_PROVIDER_ID, \
    SECURITY_SERVER_MANAGEMENT_PROVIDER_NAME_ID, MANAGEMENT_SERVICE_SECURITY_SERVER_ID, MANAGEMENT_SERVICE_WSDL_ID, \
    MANAGEMENT_SERVICE_ADDRESS_ID, MANAGEMENT_SERVICE_OWNERS_GROUP_CODE_XPATH
from view_models.sidebar import SYSTEM_SETTINGS_BTN_CSS


def view_management_service(self, service_provider, server_name, server_id, wsdl_url, service_address_uri,
                            owners_group_code):
    def view_management_service_conf():
        self.log('MEMBER_32 1. Opening management service configuration')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=SYSTEM_SETTINGS_BTN_CSS).click()
        self.wait_jquery()
        self.log('MEMBER_32 2. System displays:')
        self.log('the X-Road identifier of the management services provider')
        service_provider_value = self.wait_until_visible(type=By.ID,
                                                         element=SECURITY_SERVER_MANAGEMENT_PROVIDER_ID).get_attribute('value')
        self.log('the name of the management services provider')
        server_name_value = self.wait_until_visible(type=By.ID,
                                                    element=SECURITY_SERVER_MANAGEMENT_PROVIDER_NAME_ID).text
        self.log('the X-Road identifiers of the security servers where the management service provider is '
                 'registered as a security server client')
        server_id_value = self.wait_until_visible(type=By.ID, element=MANAGEMENT_SERVICE_SECURITY_SERVER_ID).text
        self.log('the URL of the WSDL file describing the management services')
        wsdl_url_value = self.wait_until_visible(type=By.ID, element=MANAGEMENT_SERVICE_WSDL_ID).text
        self.log('the address of the management services')
        service_address_url_value = self.wait_until_visible(type=By.ID, element=MANAGEMENT_SERVICE_ADDRESS_ID).text
        self.log('the code of the global group that needs to have access rights to management services')
        owners_group_code_value = self.wait_until_visible(type=By.XPATH,
                                                          element=MANAGEMENT_SERVICE_OWNERS_GROUP_CODE_XPATH).text

        self.log('Checking service provider values')
        self.is_equal(service_provider, service_provider_value)
        self.is_equal(server_name, server_name_value)
        self.is_equal(server_id, server_id_value)
        self.is_equal(wsdl_url, wsdl_url_value)
        self.is_true(service_address_url_value.startswith(service_address_uri))
        self.is_equal(owners_group_code, owners_group_code_value)

    return view_management_service_conf
