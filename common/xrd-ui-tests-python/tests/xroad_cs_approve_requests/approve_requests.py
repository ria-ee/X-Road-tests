from selenium.webdriver.common.by import By

from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import added_client_row
from view_models import members_table


def check_client_registration_status(self, client, registered_status='registered'):
    status = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
    self.log('Check if ' + ':'.join(
        [client['code'], client['subsystem_code']]) + ' is {0}: {1} ({2})'.format(registered_status,
                                                                                  status == registered_status,
                                                                                  status))


def check_client_in_cs(self, clients):
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    client = clients[0]
    client_row = members_table.get_row_by_columns(table, [client['name'], client['class'],
                                                          client['code']])
    self.click(client_row)

    # Open the client details and subsystem tab
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()

    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()
    self.wait_jquery()

    table = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TABLE_XPATH)
    self.wait_jquery()

    for client in clients:
        self.is_not_none(
            members_table.get_row_by_columns(table, [client['subsystem_code'], client['server_name']]),
            '',
            'MEMBER_10 5. CHECKING IF {} EXISTS FAILED'.format(client['subsystem_code']),
            'MEMBER_10 5. CHECKING IF {} EXISTS'.format(client['subsystem_code']))

