from selenium.webdriver.common.by import By

from view_models.central_services import SERVICES_TABLE_ROW_CSS
from view_models.sidebar import CENTRAL_SERVICES_CSS


def test_view_central_service(self):
    def view_central_service():
        self.log('SERVICE_40 1. Opening central services view')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=CENTRAL_SERVICES_CSS).click()
        self.wait_jquery()
        self.log('SERVICE_40 2. System displays the list of central services')
        central_services = self.wait_until_visible(type=By.CSS_SELECTOR, element=SERVICES_TABLE_ROW_CSS, multiple=True)
        for central_service in central_services:
            central_service.click()

            tds = central_service.find_elements_by_tag_name('td')
            service_code = tds[0].text
            self.log('SERVICE_40 2. System displays the code of the central service: {}'.format(service_code))
            self.is_true(len(service_code))
            self.log('SERVICE_40 2. System displays the X-Road identifier of the implementing service')
            for td in tds[1:]:
                self.is_true(len(td.text) > 0)
    return view_central_service
