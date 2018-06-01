# coding=utf-8
from view_models import sidebar, members_table, cs_security_servers, popups
from selenium.webdriver.common.by import By
import time
import re


def test_select_members(case, ss1_server_name=None, ss1_class=None, ss1_code=None):
    '''
    :param self: self: MainController object
    :param ss1_server_name: ss1_server_name: str - security server name
    :param ss1_class: ss1_class: str - security server class
    :param ss1_code: ss1_code str - security server code
    :return:
    '''

    self = case
    def select_members():
        self.log('UC MEMBER_04: 1. CS administrator selects to view the list of X-Road members.')
        '''Click on "Members" button'''
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()
        self.wait_jquery()

        '''Get content of members table'''
        table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
        self.wait_jquery()

        self.log(
            'Get members table and click on row that contains client name: {0}, client class: {1}, client code: {2}'.format(
                ss1_server_name, ss1_class, ss1_code))

        self.log('UC MEMBER_04: 2. System displays the number of X-Road members and the following information for each member: the name of the X-Road member;the member class of the X-Road member;the member code of the X-Road member.')
        client_row = members_table.get_row_by_columns(table, [ss1_server_name, ss1_class, ss1_code])

        self.click(client_row)

        self.log('UC MEMBER_04: 2. The following user action options are displayed:add an X-Road member: add an X-Road member')

        self.log('Verify "ADD" button')
        cs_add_btn = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).is_enabled()
        self.is_true(cs_add_btn,
                     msg='Add button not enabled')

        self.log('UC MEMBER_04: 2. The following user action options are displayed:add an X-Road member: view the details of an X-Road member')

        self.log('Verify "Details" button')
        cs_details_btn = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).is_enabled()
        self.is_true(cs_details_btn,
                     msg='Details button not enabled')

        '''Open clients details'''
        self.log('Open client details')
        self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
        self.wait_jquery()

    return select_members


def test_members_details(case):
    '''
    UC MEMBER_05: View the Details of an X-Road Member

    :param self: MainController object
    :return:
    '''

    self = case

    def member_details():
        self.log('UC MEMBER_05: View the Details of an X-Road Member')
        self.log('UC MEMBER_05: 2. The following user action options are displayed:edit the name of the X-Road member')
        self.log('Verify "EDIT" button')
        cs_edit_btn = self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_NAME_EDIT_BTN_XPATH).is_enabled()
        self.is_true(cs_edit_btn,
                     msg='Edit button not enabled')
        self.log('UC MEMBER_05: 2. The following user action options are displayed:view the security servers owned by the X-Road member')

        '''Verify "Owned servers" tab'''
        self.log('Verify "Owned servers" tab')
        owned_servers = self.wait_until_visible(type=By.XPATH, element=members_table.OWNED_SERVERS_TAB).is_enabled()
        self.is_true(owned_servers,
                     msg='Owned servers tab not enabled')
        self.log('UC MEMBER_05: 2. The following user action options are displayed:view the global group membership of the X-Road member')

        '''Verify "Global group membership" tab'''
        self.log('Verify "Global group membership" tab')
        global_group_membership = self.wait_until_visible(type=By.XPATH,
                                                          element=members_table.GLOBAL_GROUP_TAB).is_enabled()
        self.is_true(global_group_membership,
                     msg='Global group membership tab not enabled')
        self.log('UC MEMBER_05: 2. The following user action options are displayed:view the subsystems of the X-Road member')

        '''Verify "Subsystems" tab'''
        self.log('Verify "Subsystems" tab')
        subsystem = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).is_enabled()
        self.is_true(subsystem,
                     msg='Subsystem tab not enabled')
        self.log('UC MEMBER_05: 2. The following user action options are displayed:view the security servers where the X-Road member or the member s subsystems are registered as security server clients')

        '''Verify "Used servers" tab'''
        self.log('Verify "Used servers" tab')
        used_servers = self.wait_until_visible(type=By.XPATH, element=members_table.USED_SERVERS_TAB).is_enabled()
        self.is_true(used_servers,
                     msg='Used_servers tab not enabled')
        self.log('UC MEMBER_05: 2. The following user action options are displayed:view the management requests associated with the X-Road member')

        '''Verify "Management requests" tab'''
        self.log('Verify "Management requests" tab')
        management_requests = self.wait_until_visible(type=By.XPATH,
                                                      element=members_table.MANAGEMENT_REQUESTS_TAB).is_enabled()
        self.is_true(management_requests,
                     msg='Used_servers tab not enabled')
        self.log('UC MEMBER_05: 2. The following user action options are displayed:delete the X-Road member')

        '''Verify "Delete" button'''
        self.log('Verify "Delete" button')
        delete_btn = self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).is_enabled()
        self.is_true(delete_btn,
                     msg='Delete button not enabled')

    return member_details


def test_list_security_servers(case, ss1_server_name=None):
    '''
    UC MEMBER_06: View the Security Servers Owned by an X-Road Member
    :param self: MainController object
    :param ss1_server_name: str - security server name
    :return:
    '''
    self = case

    def list_security_servers():
        self.log('UC MEMBER_06: 1. CS administrator selects to view the security servers owned by an X-Road member.')

        '''Click "Owned servers" tab'''
        self.log('Click "Owned servers" tab')
        self.wait_until_visible(type=By.XPATH, element=members_table.OWNED_SERVERS_TAB).click()
        self.wait_jquery()
        '''Get server name'''
        server_name = self.wait_until_visible(type=By.CSS_SELECTOR, element='.open_details').text

        '''Verify server name'''
        self.is_equal(server_name, ss1_server_name)
        self.log('UC MEMBER_06 2. Create an authentication certificate registration request for adding an owned security server for the X-Road member')

        '''Verify add button'''
        add_button = self.wait_until_visible(type=By.CSS_SELECTOR,
                                             element=cs_security_servers.ADD_OWNED_SERVER_BTN_CSS).is_enabled()
        self.is_true(add_button,
                     msg='Add button not enabled')

        '''Click on server name'''
        self.wait_until_visible(type=By.CSS_SELECTOR, element='.open_details').click()
        self.wait_jquery()

        self.log('UC MEMBER_06 2. View the details of a security server owned by the X-Road member')
        '''Verify "Security server details" tab'''
        security_server_details_tab = self.wait_until_visible(type=By.XPATH,
                                                              element=cs_security_servers.SECURITY_SERVER_DETAILS_TAB).is_enabled()
        self.is_true(security_server_details_tab,
                     msg='"Security sever details" tab not enabled')

        self.log('Verify "Clients" tab')
        '''Verify "Cleints" tab'''
        clients_tab = self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_CLIENT_TAB).is_enabled()
        self.is_true(clients_tab,
                     msg='"Clients" tab not enabled')

        self.log('Verify "Authentication certificate" tab')
        '''Verify "Authentication certificates" tab'''
        authentication_certificates_tab = self.wait_until_visible(type=By.XPATH,
                                                                  element=cs_security_servers.SECURITYSERVER_AUTH_CERT_TAB_XPATH).is_enabled()
        self.is_true(authentication_certificates_tab,
                     msg='"Authentication certificates" tab not enabled')

        self.log('Verify "Server management request" tab')
        '''Verify "Server management request" tab'''
        server_management_request_tab = self.wait_until_visible(type=By.XPATH,
                                                                element=cs_security_servers.SERVER_MANAGEMENT_REQUESTS_TAB).is_enabled()
        self.is_true(server_management_request_tab,
                     msg='"Server management request" tab not enabled')

        '''Click close button'''
        self.wait_until_visible(type=By.XPATH, element=popups.SECURITY_SERVER_EDIT_POPUP_CANCEL_XPATH).click()
        self.wait_jquery()


    return list_security_servers


def test_view_member_subystems(case, ss1_server_name=None, ss1_subsystem=None, ss1_class=None, ss1_code=None):

    self = case

    def view_member_subystems():
        self.log('UC MEMBER_07: 1. CS administrator selects to view the subsystems of an X-Road member.')
        self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()
        '''Verify Add new subsystem button'''
        self.log('UC MEMBER_07: 2. The following user action options are displayed:add a subsystem to the X-Road member.')
        add_button = self.wait_until_visible(type=By.XPATH, element=members_table.ADD_SUBSYSTEM_BTN_ID).is_enabled()
        self.is_true(add_button,
                     msg='"Add" button not enabled')

        '''Get member details table'''
        table = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TABLE_XPATH).text


        self.log('UC MEMBER_07: 2. System displays the list of subsystems of the member.')

        '''Verify code of the subsystem and code of the security server'''
        if ss1_server_name and ss1_subsystem not in table:
            raise self.failureException('No Subsystem Code or Used Servers found')

        '''Click "Add" on subsystem popup'''
        self.wait_until_visible(type=By.XPATH, element=members_table.ADD_SUBSYSTEM_BTN_ID).click()

        '''Enter test name to subsystem'''
        self.log('Insert "test" to "Subsystem Code" area')
        subsystem_input = self.wait_until_visible(type=By.ID, element=members_table.SUBSYSTEM_CODE_AREA_ID)
        self.input(subsystem_input, 'test')

        '''Click "OK" button'''
        self.log('Confirm adding subsystem, click on "OK" button')
        self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        '''Find test row'''
        subsys_row = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TR_BY_CODE_XPATH.format('test'))
        '''Click on test row'''
        self.click(subsys_row)

        self.log('UC MEMBER_07: 2. The following user action options are displayed:delete a subsystem that is not registered as a client to any security servers.')

        delete_button = self.wait_until_visible(type=By.XPATH, element=members_table.DELETE_SUBSYSTEM_BTN_ID).is_enabled()
        self.is_true(delete_button,
                     msg='"Delete" button not enabled')

        '''Click "Delete" button'''
        self.wait_until_visible(type=By.XPATH, element=members_table.DELETE_SUBSYSTEM_BTN_ID).click()

        '''Confirm deleteion'''
        popups.confirm_dialog_click(self)
        self.wait_jquery()
        '''Close popup'''
        popups.close_all_open_dialogs(self)

    return view_member_subystems




def test_view_security_servers(case, ss1_server_name=None, ss1_subsystem=None, ss1_class=None, ss1_code=None):
    self = case

    def view_security_servers():
        self.log('UC MEMBER_08: 1. CS administrator selects to view the security servers used by an X-Road member.')

        '''Click Used Servers tab'''
        self.wait_until_visible(type=By.XPATH, element=members_table.USED_SERVERS_TAB).click()
        self.wait_jquery()

        self.log('UC MEMBER_08: 2. Create a security server client registration request for registering a subsystem of the member as a client to a security server')

        '''Verify Add new clients registration button'''
        add_securityserver_client = self.wait_until_visible(type=By.XPATH,
                                                            element=members_table.REGISTER_SECURITYSERVER_CLIENT_ADD_BTN_ID).is_enabled()
        self.is_true(add_securityserver_client,
                     msg='"Add" button not enabled')

        '''Get table of used servers'''
        used_servers = self.wait_until_visible(type=By.XPATH, element=members_table.USED_SERVERS_TABLE_XPATH).text
        self.wait_jquery()


        self.log('UC MEMBER_08: 2. The system displays the list of security servers that have the members subsystems registered as security server clients.')
        self.log('UC MEMBER_08: 2. View the details of the security server that has a subsystem of the member registered as a security server client.')

        '''Verify server code details view is enabled'''
        server_code = self.wait_until_visible(type=By.XPATH, element="//a[@class='open_details']").is_enabled()
        self.is_true(server_code,
                     msg='View the details of the security server that has a subsystem of the member registered as a security server client not enabled')
        self.log('UC MEMBER_08: 2. View the details of the owner of the security server that has the a subsystem of the member registered as a security server client.')

        '''Verify server owner details view is enabled'''
        server_owner = self.wait_until_visible(type=By.XPATH, element="(//a[@class='open_details'])[2]").is_enabled()
        self.is_true(server_owner,
                     msg='View the details of the owner of the security server that has the a subsystem of the member registered as a security server client not enabled')

        '''Verify code of the subsystem and code of the security server'''
        if ss1_server_name and ss1_subsystem not in used_servers:
            raise self.failureException('No Server Code or Client Subsystem Code or Server Owner found')

        '''Click on used servers table'''
        self.wait_until_visible(type=By.XPATH, element=members_table.USED_SERVERS_TABLE_XPATH).click()
        self.log('UC MEMBER_08: 2. Create a security server client deletion request to delete the registration of a members subsystem as a client of a security server')
        delete_button = self.wait_until_visible(type=By.XPATH,
                                                element=members_table.DELETE_REGISTER_SECURITYSERVER_CLIENT_BTN_ID).is_enabled()
        self.is_true(delete_button,
                     msg='"Delete" button not enabled')
        '''Close popup'''
        popups.close_all_open_dialogs(self)

    return view_security_servers


def test_view_member_management_requests(case):
    self = case
    def view_member_management_requests():
        self.log('UC MEMBER_09: 1. CS administrator selects to view management requests associated with the X-Road member.')

        '''Click Management Requests tab'''
        self.wait_until_visible(type=By.XPATH,
                                element=members_table.MANAGEMENT_REQUESTS_TAB).click()
        self.wait_jquery()

        '''Get member details table'''
        table = self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_MANAGEMENT_TABLE_XPATH)

        '''Verify that first Request ID is clickable'''
        request_id = self.wait_until_visible(type=By.XPATH, element="//a[@class='open_details']").is_enabled()
        self.is_true(request_id,
                     msg='"View of request detatails is not enabled')


        '''Get latest request details'''
        request_id = table.find_elements_by_tag_name('td')[0].text
        request_type = table.find_elements_by_tag_name('td')[1].text
        created = table.find_elements_by_tag_name('td')[2].text
        status = table.find_elements_by_tag_name('td')[3].text

        self.log('UC MEMBER_09: 2. System displays the identifier of the request')

        '''Request id verification'''
        request_id_match = re.match(popups.MEMBER_DETAILS_MANAGEMENT_REGQUEST_ID_REGEX, request_id)

        self.log('Request id verification')
        self.is_true(request_id_match,
                     msg='Request id is in wrong format')

        self.log('UC MEMBER_09: 2. System displays the type of the request')

        '''Request type verification'''
        request_type_match = re.match(popups.MEMBER_DETAILS_MANAGEMENT_REQUEST_TYPE, request_type)

        self.log('Request type verification')
        self.is_true(request_type_match,
                     msg='Request type is in wrong format')
        self.log('UC MEMBER_09: 2. System displays the date and time of when the request was saved in the system configuration')

        '''Request date verification'''
        request_created_match = re.match(popups.MEMBER_DETAILS_MANAGEMENT_REGQUEST_CREATED_REGEX, created)

        self.log('Request date verification')

        self.is_true(request_created_match,
                     msg='Date is in wrong format')

        self.log('UC MEMBER_09: 2. System displays the status of the request')
        if (len(status) == 0 or re.match(popups.MEMBER_DETAILS_MANAGEMENT_REQUEST_STATUS, status)):
            pass
        else:
            raise Exception('Status in wrong format')

    return view_member_management_requests
