# coding=utf-8
from selenium.webdriver.common.by import By
from view_models import popups, clients_table_vm, groups_table
from time import gmtime, strftime
import time


def test_verify_local_group_client(case, ss_client_id=None, ss_client_name=None):
    '''

    :param case: MainController object
    :param ss_client_id: string client id information
    :param ss_client_name: string client name information
    :return:
    '''

    self = case

    def local_group_ss_client():
        create_local_group(self, ss_client_id=ss_client_id)
        verify_details(self, ss_client_id=ss_client_id, ss_client_name=ss_client_name)
        delete_local_group(self)

    return local_group_ss_client


def verify_details(self, ss_client_id=None, ss_client_name=None):
    '''

    :param self: MainController object
    :param ss_client_id: string client id information
    :param ss_client_name: string client name information
    :return:
    '''

    '''Click on the local groups row'''
    self.by_xpath(groups_table.LOCAL_GROUP_ROW_BY_TD_TEXT_XPATH.format(clients_table_vm.TEST_DATA)).click()
    self.wait_jquery()

    '''Click on group details'''
    self.log('SERVICE_24: 1.SS administrator selects to view the details of a local group.')

    self.wait_until_visible(type=By.ID, element=groups_table.GROUP_DETAILS_BTN_ID).click()

    self.log('Click on "ADD MEMBERS" button')
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID).click()

    self.log('Click on "SEARCH" button')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DETAILS_BUTTON_SEARCH_XPATH).click()

    self.log('Get founded members and members subsystem codes')
    founded_subsystems = self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_FOUNDED_SUBSYSTEMS_XPATH,
                                                 multiple=True)
    '''Make full client id'''
    client_id = 'SUBSYSTEM : ' + ss_client_id


    '''Click on specific client id'''
    for client in founded_subsystems:
        if client.text == client_id:
            client.click()
            break

    self.log('... and clicking on "ADD SELECTED TO GROUP" button')
    self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_ADD_SELECTED_TO_GROUP_BTN_ID).click()

    '''Click on member'''
    self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_ADD_GROUP_MEMBERS_XPATH).click()

    member = self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_ADD_GROUP_MEMBERS_XPATH).text
    id = self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_ADD_GROUP_MEMBERS_ID_XPATH).text
    member_date = self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_ADD_GROUP_MEMBERS_DATE_XPATH).text

    self.log('SERVICE_24: 2. The name of the group member')
    self.is_equal(member, ss_client_name,
                  msg='Wrong member name')

    self.log('SERVICE_24: 2. The X-Road identifier of the group member')
    self.is_equal(id, client_id,
                  msg='Wrong member id')

    date = strftime("%Y-%m-%d", gmtime())
    self.log('SERVICE_24: 2. The date of when the member was added to the local group')
    self.is_equal(member_date, date,
                  msg='Wrong local group added date')


    self.log('SERVICE_24: 2. Add group members to the local group')

    add_members_btn = self.wait_until_visible(type=By.ID,
                                              element=popups.LOCAL_GROUP_DETAILS_BUTTON_ADD_MEMBERS_ID).is_enabled()
    self.log('"ADD GROUP" button verification"')
    self.is_true(add_members_btn,
                 msg='"ADD MEMBERS" button not found')
    self.log('SERVICE_24: 2. Remove group members from the local group')
    remove_selected_members_btn = self.wait_until_visible(type=By.ID,
                                                          element=popups.LOCAL_GROUP_DETAILS_BUTTON_REMOVE_SELECTED_MEMBERS).is_enabled()
    self.log('"REMOVE SELECTED MEMBERS" button verification"')
    self.is_true(remove_selected_members_btn,
                 msg='"REMOVE SELECTED MEMBERS" button not found')
    remove_all_selected_members_btn = self.wait_until_visible(type=By.ID,
                                                              element=popups.LOCAL_GROUP_REMOVE_ALL_MEMBERS_BTN_ID).is_enabled()
    self.log('"REMOVE ALL MEMBERS" button verification"')
    self.is_true(remove_all_selected_members_btn,
                 msg='"REMOVE ALL MEMBERS" button not found')


    self.log('SERVICE_24: 2. Edit the description of the local group')

    edit_description_btn = self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_EDIT_DESCRIPTION_BTN_XPATH).is_enabled()
    self.log('"EDIT" button verification"')
    self.is_true(edit_description_btn,
                 msg='"EDIT" button not found')


    self.log('SERVICE_24: 2. Delete the local group')
    delete_group = self.wait_until_visible(type=By.ID, element=popups.LOCAL_GROUP_DELETE_GROUP_BTN_ID).is_enabled()
    self.log('"DELETE GROUP" button verification"')
    self.is_true(delete_group,
                 msg='"DELETE GROUP" button not found')




def create_local_group(self, ss_client_id):
    '''

    :param self: MainController object
    :param ss_client_id: string client id information
    :return:
    '''
    self.log('Open clients details, by double clicking on client id')

    ss_client_id_row = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.get_client_id(ss_client_id))
    self.double_click(ss_client_id_row)
    self.log('SERVICE_23 1.SS administrator selects to view the local groups of a security server client.')

    self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUPS_TAB).click()

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

    self.wait_jquery()


def delete_local_group(self):
    """
    Delete local group
    :param self: MainController object
    :return: None
    """

    self.log('Delete local group by clicking on "DELETE GROUP" button')
    self.wait_until_visible(type=By.XPATH, element=popups.LOCAL_GROUP_DELETE_GROUP_BTN_XPATH).click()
    self.log('... and clicking on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()
