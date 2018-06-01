# coding=utf-8
from selenium.webdriver.common.by import By
from view_models import popups, clients_table_vm, groups_table
from time import gmtime, strftime
from helpers import xroad


def test_verify_local_group_client(case):
    '''

    :param case: MainController object
    :return:
    '''
    self = case

    def local_group_ss_client():
        try:
            create_local_group(self)
            verify_local_group_security_server_client(self)
        except:
            raise
        finally:
            # Always delete the group
            delete_local_group(self)

    return local_group_ss_client


def verify_local_group_security_server_client(self):
    '''

    :param self: MainController object
    :return: None
    '''
    add_group = self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).is_enabled()

    self.log('"ADD GROUP" button verification"')
    self.is_true(add_group,
                 msg='"Add group" button not found')


    details_btn = self.by_xpath(groups_table.LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(clients_table_vm.TEST_DATA[::-1])).is_enabled()
    self.log('"Details" button verification"')
    self.is_true(details_btn,
                 msg='"Details" button not found')

    self.log('SERVICE_23 2.System displays the list of local groups. For each local group, the following information is displayed')

    local_group_row = self.by_xpath(groups_table.LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(clients_table_vm.TEST_DATA)).text
    local_group_row_splitted = local_group_row.split()
    code = local_group_row_splitted[0]
    self.log('Verify the code of the local group')
    '''Verify the code of the local group'''
    self.is_equal(code, clients_table_vm.TEST_DATA[::-1],
                  msg='Wrong local group code')

    description = local_group_row_splitted[1]
    self.log('Verify the description of the local group')
    self.is_equal(description, clients_table_vm.TEST_DATA,
                  msg='Wrong local group description')
    self.log('Verify the number of members in the local group')
    member_count = local_group_row_splitted[2]
    self.is_equal(member_count, '0',
                  msg='Wrong member count')

    updated_date = local_group_row_splitted[3]
    date = strftime("%Y-%m-%d", gmtime())
    self.log('Verify the date when the local group was last updated.')
    self.is_equal(updated_date, date,
                  msg='Wrong local group update date')

def open_client_groups(self):
    client_name = self.config.get('ss2.client2_name')
    subsystem_row = xroad.split_xroad_subsystem(self.config.get('ss2.client2_id'))
    subsystem = subsystem_row['subsystem']

    self.log('Open clients details by clicking on client {0} subsystem {1}'.format(client_name, subsystem))
    self.wait_jquery()

    '''Click on client row'''
    client_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                             get_client_id_by_member_code_subsystem_code(client_name,subsystem))

    '''Click on "Details" button'''
    client_row.find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS).click()
    self.wait_jquery()

    self.log('SERVICE_23 1.SS administrator selects to view the local groups of a security server client.')

    self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUPS_TAB).click()
    self.wait_jquery()


def create_local_group(self):
    open_client_groups(self)

    self.log('Click on "ADD GROUP" button')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_GROUP_ADD_BTN_ID).click()

    self.log('Insert "Code" for the new local group')
    new_group_code = self.wait_until_visible(type=By.ID, element=popups.GROUP_ADD_POPUP_CODE_AREA_ID)
    self.input(new_group_code, clients_table_vm.TEST_DATA[::-1])

    self.log('Insert "Description" for the new local group')
    new_group_description = self.wait_until_visible(type=By.ID, element=popups.GROUP_ADD_POPUP_CODE_DESCRIPTION_ID)
    self.input(new_group_description, clients_table_vm.TEST_DATA)

    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.GROUP_ADD_POPUP_OK_BTN_XPATH).click()


def delete_local_group(self):
    """
    Delete local group
    :param self: MainController object
    :return: None
    """

    # Close all popups
    popups.close_all_open_dialogs(self)
    self.wait_jquery()

    open_client_groups(self)

    self.log('Open group details')
    self.by_xpath(groups_table.LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(clients_table_vm.TEST_DATA[::-1])).click()
    self.wait_jquery()

    self.log('Click on "Details" button')
    self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.log('Delete local group by clicking on "DELETE GROUP" button')
    self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DELETE_GROUP_BTN_XPATH).click()
    self.wait_jquery()
    self.log('... and clicking on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
