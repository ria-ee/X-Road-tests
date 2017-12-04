# coding=utf-8

from selenium.webdriver.common.by import By
from helpers import auditchecker
from view_models import sidebar, messages, cs_security_servers, members_table, popups, log_constants, clients_table_vm, popups
import time
from selenium.webdriver.support.select import Select



def test_add_subsystem_to_member(case, ss1_code=None, subsystem_text=None):
    self = case
    def add_subsystem_to_member():
        """
        Add a subsystem to an X-Road Member
        :param self: MainController object
        :param member_name: str - member name
        :param subsystem_text: str - subsystem
        :return: None
        """
        self.wait_jquery()
        '''Open member details'''
        self.log('Click member name - ' + ss1_code + ' - in members table')
        self.wait_until_visible(type=By.XPATH, element=members_table.get_member_data_from_table(1, ss1_code)).click()
        self.log('Click on "DETAILS" button')
        self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
        '''Open subsystem tab'''
        self.log('Click on "Subsystem" tab')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()

        '''MEMBER_56/1 CS administrator selects to add a subsystem to an X-Road member.'''
        self.log('MEMBER_56/1 CS administrator selects to add a subsystem to an X-Road member, '
                 'by clicking on "ADD buton"')
        self.wait_jquery()
        self.wait_until_visible(type=By.XPATH, element=members_table.ADD_SUBSYSTEM_BTN_ID).click()

        '''MEMBER_56/2 CS administrator inserts the code of the subsystem..'''
        self.log('MEMBER_56/2 CS administrator inserts the code of the subsystem, '
                 'by inserting (string length = {0}) - {1} - to the "Subsystem code" text field'
                 .format(len(subsystem_text), subsystem_text))
        self.wait_jquery()
        subsystem_text_field = self.wait_until_visible(type=By.ID, element=members_table.SUBSYSTEM_CODE_AREA_ID)
        self.input(subsystem_text_field, subsystem_text)
        self.wait_jquery()
        '''Click "OK" button'''
        self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()
    return add_subsystem_to_member

def test_add_subsystem_to_server_client(case, ss1_code=None, wait_input=3, random_code=None):
    self = case
    def add_subsystem_to_server_client():
        """
        Adds a subsystem to server client.
        :param self: MainController object
        :param server_code: str - server code
        :param client: dict - client data
        :param wait_input: int - seconds to wait before entering text to inputs
        :return: None
        """

        # Open clients list for server
        open_servers_clients(self, ss1_code)

        # UC MEMBER_56 1. Select to add a subsystem to an X-Road member
        self.log('MEMBER_56 1. Select to add a subsystem to an X-Road member')
        self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_CLIENT_TO_SECURITYSERVER_BTN_ID).click()
        self.wait_jquery()

        # Search for the member
        self.log('Search for the member')
        self.wait_until_visible(type=By.ID, element=cs_security_servers.SEARCH_BTN_ID).click()
        self.wait_jquery()
        time.sleep(wait_input)

        # Get the table and look for the client
        table = self.wait_until_visible(type=By.XPATH, element=cs_security_servers.MEMBERS_SEARCH_TABLE_XPATH)
        rows = table.find_elements_by_tag_name('tr')
        self.log('Finding member from table')
        for row in rows:
            tds = row.find_elements_by_tag_name('td')
            if tds[0].text is not u'':
                if (tds[0].text == 'TS1') & (tds[1].text == 'TS1OWNER') & (tds[2].text == 'GOV') & (
                            tds[3].text == random_code):
                    row.click()
                    break

        self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SELECT_MEMBER_BTN_XPATH).click()


        self.wait_jquery()
        # time.sleep(wait_input)

        # Enter data
        subsystem_input = self.wait_until_visible(type=By.ID, element=cs_security_servers.SUBSYSTEM_CODE_AREA_ID)

        # Clear the input and set value
        subsystem_input.click()
        # subsystem_input.clear()
        self.wait_jquery()

        # Submit the form
        self.wait_until_visible(type=By.ID,
                                element=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID).click()
        self.wait_jquery()
        time.sleep(5)
    return add_subsystem_to_server_client

def open_servers_clients(self, ss1_code=None):
    '''
    Open security servers and their clients in UI.
    :param self: MainController object
    :param code: str - server name
    :return:
    '''
    self.log('Open Security servers')
    self.reset_page()
    self.wait_jquery()
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
    self.wait_jquery()

    # Get the table
    table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
    self.wait_jquery()

    # Find the client and click on it
    self.log('Click on client row')
    rows = table.find_elements_by_tag_name('tr')
    for row in rows:
        if row.text is not u'':
            if row.find_element_by_tag_name('td').text == ss1_code:
                row.click()

    # Open details
    self.log('Click on Details button')
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENT_DETAILS_BTN_ID).click()
    self.wait_jquery()

    # Open clients tab
    self.log('Click on clients tab')
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_CLIENT_TAB).click()
    self.wait_jquery()

def test_add_client_to_ss_by_hand(case, client_class=None, client_code=None, client_subsystem=None, client_id_code=None, client_id_sub=None, random_code=None):
    self = case
    def add_client_to_ss_by_hand():
        """
        Adds a client to security server without searching for it in lists.
        :param self: MainController object
        :param client: dict - client data
        :return: None
        """

        '''MEMBER_47 1. Start adding the client'''
        self.log('MEMBER_47 1. Start adding the client')
        self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

        '''MEMBER_47 2. Set the class, code, subsystem'''
        '''Add member class'''
        select = Select(self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID))
        select.select_by_visible_text(client_class)

        '''Add member code'''
        input_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
        self.input(input_code, client_code)

        '''Add subsystem code'''
        subsystem_input = self.wait_until_visible(type=By.XPATH,
                                                  element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_XPATH)
        '''Add random input'''
        self.input(subsystem_input, random_code)


        '''Try to save the client'''
        self.log('Click "OK"')
        self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
        self.wait_jquery()

        '''Popup confirm'''
        popups.confirm_dialog_click(self)

    return add_client_to_ss_by_hand

def test_ss_client_deletion(case, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None, ss1_code=None,
                                    client_instance=None, client_class=None, client_code=None,
                                    client_subsystem=None, random_code=None):
    '''
    :param self: MainController object
    :param cs_ssh_host: Central Server SSH host
    :param cs_ssh_user: CS SSH username, needed if cs_ssh_host is set
    :param cs_ssh_pass: CS SSH password, needed if cs_ssh_host is set
    :param ss1_code: security server owner code
    :param client_name: client name
    :param client_instance: client instance
    :param client_class: client class
    :param client_code: client code
    :param client_subsystem: client subsystem code
    :param random_code: random generated code for test
    :return:
    '''

    self = case
    def ss_client_deletion():

        self.log('Open Security servers')
        self.reset_page()
        self.wait_jquery()
        '''Open Security Servers'''
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
        self.wait_jquery()

        '''Get the table'''
        table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
        self.wait_jquery()

        self.log('Click on client row')
        '''Find the client and click on it'''
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            if row.text is not u'':
                if row.find_element_by_tag_name('td').text == ss1_code:
                    '''Double click on row'''
                    self.double_click(row)
                    self.wait_jquery()

        self.log('Click on clients tab')
        '''Click on clients tab'''
        self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_CLIENT_TAB).click()
        self.wait_jquery()
        '''Get the clients table'''
        clients_table = self.wait_until_visible(type=By.ID,
                                                element=cs_security_servers.SECURITY_SERVER_CLIENTS_TABLE_ID)

        '''Click on member what to delete'''
        member_to_delete = members_table.get_row_by_columns(clients_table,
                                                            [client_subsystem, client_class, client_code, random_code])
        member_to_delete.click()

        self.log(
            'MEMBER_16 1. CS administrator selects to create a security server client deletion request for a subsystem of an X-Road member.')

        self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENTS_DELETE_BTN_ID).click()
        self.wait_jquery()
        self.log('MEMBER_16 2. System displays a prefilled security server client deletion request.')

        '''Verify client name'''
        popup_client_name = self.wait_until_visible(type=By.ID,
                                                    element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_REQUEST_NAME).text
        self.is_equal(popup_client_name, client_subsystem,
                      msg='Client information: client name is wrong')

        '''Verify class name'''
        popup_class_name = self.wait_until_visible(type=By.ID,
                                                   element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_REQUEST_CLASS).text

        self.is_equal(popup_class_name, client_class,
                      msg='Client information: client class is wrong')

        '''Verify code name'''
        popup_code = self.wait_until_visible(type=By.ID,
                                             element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_REQUEST_CODE).text

        self.is_equal(popup_code, client_code,
                      msg='Client information: client code is wrong')

        '''Verify subsystem code'''
        popup_subsystem_code = self.wait_until_visible(type=By.ID,
                                                       element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_REQUEST_SUB_CODE).text

        self.is_equal(popup_subsystem_code, random_code,
                      msg='Client information: client subsystem code is wrong')

        '''Verify owner name'''
        popup_owner_name = self.wait_until_visible(type=By.ID,
                                                   element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_REQUEST_OWNER_NAME).text

        self.is_equal(popup_owner_name, client_subsystem,
                      msg='Client information: owner name is wrong')

        '''Verify owner class'''
        popup_owner_class = self.wait_until_visible(type=By.ID,
                                                    element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_REQUEST_OWNER_CLASS).text

        self.is_equal(popup_owner_class, client_class,
                      msg='Client information: owner class is wrong')

        '''Verify owner code'''
        popup_owner_code = self.wait_until_visible(type=By.ID,
                                                   element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_REQUEST_OWNER_CODE).text

        self.is_equal(popup_owner_code, client_code,
                      msg='Client information: owner code is wrong')

        '''Verify server code'''
        popup_server_code = self.wait_until_visible(type=By.ID,
                                                    element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_REQUEST_SERVER_CODE).text

        self.is_equal(popup_server_code, client_subsystem,
                      msg='Client information: server code is wrong')

        self.log('MEMBER_16 3a. CS administrator selects to terminate the use case.')

        self.wait_until_visible(type=By.XPATH,
                                element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_CANCEL).click()

        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        current_log_lines = log_checker.get_line_count()

        self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENTS_DELETE_BTN_ID).click()
        self.wait_jquery()
        self.log('MEMBER_16 3. CS administrator submits the request.')
        self.wait_until_visible(type=By.XPATH,
                                element=popups.CS_SECURITY_SERVER_CLIENT_DELETION_SUBMIT).click()

        '''Server part of log message'''
        server = clients_table_vm.server_cs(client_instance, client_class, client_code, client_subsystem)
        '''Subsystem part of log message'''
        subsystem = clients_table_vm.subsystem_cs(client_instance, client_class, client_code, random_code)
        '''Get the message after deletion'''
        message = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.NOTICE_MESSAGE_CSS).text
        '''Verify message'''
        success_message = messages.SECURITY_SERVER_CLIENT_DELETION_REQUEST.format(subsystem, server)
        self.log('MEMBER_16 5. System displays the message:{}'.format(success_message))
        self.is_equal(success_message, message)

        self.log('MEMBER_16 6. System logs the event {0} to audit log'.format(log_constants.SS_CLIENT_DELETION_REQUEST))
        logs_found = log_checker.check_log(log_constants.SS_CLIENT_DELETION_REQUEST, from_line=current_log_lines + 1)
        self.is_true(logs_found)
    return ss_client_deletion

def delete_member(self, ss1_code=None, random_code=None):
    self.wait_jquery()
    '''Open member details'''
    self.log('Click member name - ' + ss1_code + ' - in members table')
    self.wait_until_visible(type=By.XPATH, element=members_table.get_member_data_from_table(1, ss1_code)).click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    '''Open subsystem tab'''
    self.log('Click on "Subsystem" tab')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()


    subsys_row = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TR_BY_CODE_XPATH.format(random_code))
    subsys_row.click()

    # Click "Delete"
    self.log('MEMBER_14 1. Subsystem delete button is clicked')
    self.wait_until_visible(type=By.XPATH, element=members_table.DELETE_SUBSYSTEM_BTN_ID).click()
    self.log('MEMBER_14 2. System prompts for confirmation')

    self.log('MEMBER_14 3. Subsystem deletion is confirmed')
    popups.confirm_dialog_click(self)


def ss_delete_client(self, client_instance=None, client_class=None, client_code=None, random_code=None):
    '''Get id text'''
    subsystem = clients_table_vm.subsystem_ss(client_instance, client_class, client_code, random_code)
    '''Find id row'''
    client_row = clients_table_vm.get_client_row_element(self, client_id=subsystem)
    '''Double click on row'''
    self.double_click(client_row)

    self.log('MEMBER_52 1. Unregister Client')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
    self.wait_jquery()
    self.log('MEMBER_52 2. System prompts for confirmation')
    self.log('MEMBER_52 3a. Confirmation dialog is canceled')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
    self.log('MEMBER_52 1. Unregister Client button is pressed again')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
    self.wait_jquery()
    self.log('MEMBER_52 3. Confirmation dialog is confirmed')
    popups.confirm_dialog_click(self)
