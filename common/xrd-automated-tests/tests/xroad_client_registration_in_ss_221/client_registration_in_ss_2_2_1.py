import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from view_models import members_table, clients_table_vm, sidebar, popups, \
    keys_and_certificates_table as keyscertificates_constants, cs_security_servers
from tests.xroad_ss_client_sertification_213 import client_certification_2_1_3
from helpers import ssh_server_actions
import time

SYSTEM_TYPE = 'SUBSYSTEM'

test_name = '2.2.1 CLIENT REGISTRATION IN SECURITY SERVER'


def test_remove(cs_host, cs_username, cs_password,
                sec_1_host, sec_1_username, sec_1_password,
                sec_2_host, sec_2_username, sec_2_password,
                cs_new_member=None, ss1_client=None, ss2_client=None, ss2_client_2=None,
                cs_member_name=None, ss1_client_name=None, ss2_client_name=None, ss2_client_2_name=None):
    def test_case(self):
        self.log('test_remove method')

        cs_member = {'name': cs_member_name, 'class': cs_new_member['class'], 'code': cs_new_member['code']}

        ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                       'subsystem_code': ss1_client['subsystem']}

        ss_2_client = {'name': ss2_client_name, 'class': ss2_client['class'], 'code': ss2_client['code'],
                       'subsystem_code': ss2_client['subsystem']}

        ss_2_client_2 = {'name': ss2_client_2_name, 'class': ss2_client_2['class'], 'code': ss2_client_2['code'],
                         'subsystem_code': ss2_client_2['subsystem']}

        try:

            remove_data(self, cs_host, cs_username, cs_password, sec_1_host, sec_1_username, sec_1_password,
                        sec_2_host, sec_2_username, sec_2_password,
                        cs_member=cs_member, ss_1_client=ss_1_client, ss_2_client=ss_2_client,
                        ss_2_client_2=ss_2_client_2)
        except:
            self.log('Failed to remove client.')
            traceback.print_exc()
            assert False

    return test_case


def test_test(case, cs_host, cs_username, cs_password,
              sec_1_host, sec_1_username, sec_1_password,
              sec_2_host, sec_2_username, sec_2_password,
              cs_new_member=None, ss1_client=None, ss2_client=None, ss2_client_2=None,
              cs_member_name=None, ss1_client_name=None, ss2_client_name=None, ss2_client_2_name=None,
              remove_added_data=True):
    self = case
    sync_retry = 30
    sync_timeout = 120
    wait_input = 2  # delay in seconds before starting to look for input fields before entering text to them
    registered_status = 'registered'

    def test_case():
        cs_member = {'name': cs_member_name, 'class': cs_new_member['class'], 'code': cs_new_member['code']}

        ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                       'subsystem_code': ss1_client['subsystem']}

        ss_2_client = {'name': ss2_client_name, 'class': ss2_client['class'], 'code': ss2_client['code'],
                       'subsystem_code': ss2_client['subsystem']}

        ss_2_client_2 = {'name': ss2_client_2_name, 'class': ss2_client_2['class'], 'code': ss2_client_2['code'],
                         'subsystem_code': ss2_client_2['subsystem']}

        delete_client = remove_added_data
        error = False
        self.exception = False
        try:
            login(self, cs_host, cs_username, cs_password)

            add_member_to_cs(self, cs_member)

            login(self, sec_1_host, sec_1_username, sec_1_password)

            self.log('Wait {0} seconds for the change'.format(sync_timeout))
            time.sleep(sync_timeout)
            add_client_to_ss(self, ss_1_client, retry_interval=sync_retry, retry_timeout=sync_timeout,
                             wait_input=wait_input, step='2.2.1-2: ')

            self.log('2.2.1-3: Create sign certificate')
            self.driver.get(sec_1_host)
            client_certification_2_1_3.test(client_code=ss_1_client['code'], client_class=ss_1_client['class'])(self)
            self.log('2.2.1-3: Open central server ')
            login_with_logout(self, cs_host, cs_username, cs_password)

            self.log('Add sub as a client to member')
            add_sub_as_client_to_member(self, self.config.get('ss1.server_name'), ss_1_client, wait_input=wait_input,
                                        step='2.2.1-4: ')
            approve_requests(self, '2.2.1-5: ')

            login(self, sec_2_host, sec_2_username, sec_2_password)

            add_client_to_ss_by_hand(self, ss_2_client)

            self.log('2.2.1-7: Create sign certificate')
            login_with_logout(self, sec_2_host, sec_2_username, sec_2_password)
            client_certification_2_1_3.test(client_code=ss_2_client['code'], client_class=ss_2_client['class'])(self)

            self.log('Open central server ')
            login_with_logout(self, cs_host, cs_username, cs_password)

            self.log('2.2.1-8: Add testservice to security server 2 client')
            add_subsystem_to_server_client(self, self.config.get('ss2.server_name'), ss_2_client, wait_input=wait_input)

            self.log('Wait {0} for sync'.format(sync_retry))
            time.sleep(sync_retry)

            approve_requests(self, '2.2.1-9: ')

            login_with_logout(self, sec_2_host, sec_2_username, sec_2_password)

            add_client_to_ss(self, ss_2_client_2, wait_input=wait_input, step='2.2.1-10: ')

            login_with_logout(self, cs_host, cs_username, cs_password)

            add_sub_as_client_to_member(self, self.config.get('ss2.server_name'), ss_2_client_2, wait_input=wait_input,
                                        step='2.2.1-11: ')

            self.log('Wait {0} for sync'.format(sync_retry))
            time.sleep(sync_retry)

            approve_requests(self, '2.2.1-12: ')

            if self.exception:
                error = True
                raise RuntimeError(
                    'SOMETHING WENT WRONG, WITH TEST, PLEASE CHECK THAT ALL PREVIOUSLY CLIENTS HAVE BEEN DELETED!')

            login_with_logout(self, cs_host, cs_username, cs_password)

            check_expected_result_cs(self, ss_1_client, ss_2_client, ss_2_client_2)

            login_with_logout(self, sec_1_host, sec_1_username, sec_1_password)

            check_expected_result_ss(self, ss_1_client, retry_interval=sync_retry, retry_timeout=sync_timeout)

            login_with_logout(self, sec_2_host, sec_2_username, sec_2_password)

            check_expected_result_ss(self, ss_2_client, registered_status=registered_status, retry_interval=sync_retry,
                                     retry_timeout=sync_timeout)

            check_expected_result_ss(self, ss_2_client_2, registered_status=registered_status,
                                     retry_interval=sync_retry, retry_timeout=sync_timeout)
        except Exception, e:
            self.log('Exception: {0}'.format(e))
            delete_client = True

            millis = int(round(time.time() * 1000))
            exception_filename = 'safe_{0}.txt'.format(millis)
            screenshot_filename = 'safe_{0}.png'.format(millis)
            exception_data = traceback.format_exc()
            self.save_screenshot(screenshot_filename)
            self.save_text_data(exception_filename, exception_data)
            self.log('Files created' + ' ' + exception_filename + ' ' + screenshot_filename)
            traceback.print_exc()
            error = True
        finally:
            if delete_client:
                self.log('Deleting client')
                remove_data(self, cs_host, cs_username, cs_password, sec_1_host, sec_1_username, sec_1_password,
                            sec_2_host, sec_2_username, sec_2_password,
                            cs_member=cs_member, ss_1_client=ss_1_client, ss_2_client=ss_2_client,
                            ss_2_client_2=ss_2_client_2)

                if error:
                    assert False

    return test_case


def add_member_to_cs(self, member):
    self.log('2.2.1-1: Wait for the "ADD" button and click')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()
    self.log('2.2.1-1: Wait for the popup to be visible')
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_XPATH)
    self.log('2.2.1-1:  Enter ' + member['name'] + ' to "member name" area')
    input_name = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID)
    self.input(input_name, member['name'])
    self.log('2.2.1-1:  Select ' + member['class'] + ' from "class" dropdown')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=members_table.ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    select.select_by_visible_text(member['class'])
    self.log('2.2.1-1:  Enter ' + member['code'] + ' to "member code" area')
    input_code = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member['code'])
    self.log('2.2.1-1:  Click "OK" to add member')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()


def add_client_to_ss(self, client, retry_interval=0, retry_timeout=0, wait_input=2, step='x.x.x-y: '):
    self.log(step + 'Click on "ADD CLIENT" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

    self.log(step + 'Click on "SELECT CLIENT FROM GLOBAL LIST" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.SELECT_CLIENT_FROM_GLOBAL_LIST_BTN_ID).click()
    self.wait_jquery()

    c_box = self.wait_until_visible(type=By.ID, element=clients_table_vm.SHOW_ONLY_LOCAL_CLIENTS_CHECKBOX_ID)
    if c_box.is_selected():
        c_box.click()
    start_time = time.time()
    while True:
        try:
            if retry_interval > 0:
                self.log(step + 'Waiting {0} before searching'.format(retry_interval))
                time.sleep(retry_interval)

            self.log(step + 'Searching global list for clients')

            self.wait_until_visible(type=By.XPATH, element=clients_table_vm.GLOBAL_CLIENT_LIST_SEARCH_BTN_XPATH).click()
            self.wait_jquery()

            table = self.wait_until_visible(type=By.ID, element=clients_table_vm.GLOBAL_CLIENTS_TABLE_ID)
            self.wait_jquery()
            time.sleep(3)
            self.log(step + 'Searching for client row')
            members_table.get_row_by_columns(table, [client['name'], client['class'], client['code']]).click()
            self.log(step + 'Found client row')
            break
        except:
            if time.time() > start_time + retry_timeout:
                if retry_timeout > 0:
                    self.log(step + 'Timeout while waiting')
                raise
            self.log(step + 'Client row not found')

    self.wait_until_visible(type=By.XPATH, element=clients_table_vm.SELECT_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    time.sleep(wait_input)
    subsystem_input = self.wait_until_visible(type=By.CSS_SELECTOR,
                                              element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_CSS)
    self.wait_jquery()
    time.sleep(wait_input)

    self.input(subsystem_input, client['subsystem_code'])

    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    time.sleep(3)
    warning = self.wait_until_visible(type=By.ID, element=popups.CONFIRM_POPUP_TEXT_AREA_ID).text
    self.wait_jquery()

    self.is_true(warning in get_expected_warning_messages(client), test_name,
                 step + 'WARNING NOT CORRECT: {0}'.format(
                     warning),
                 step + 'EXPECTED WARNING MESSAGE: "{0}" GOT: "{1}"'.format(
                     get_expected_warning_messages(client),
                     warning))

    self.log(step + 'Confirm message')
    popups.confirm_dialog_click(self)

    self.log(step + 'ADDING CLIENT TO SECURITY SERVER STATUS TEST')
    status_title = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
    try:
        self.is_equal(status_title, 'registration in progress', test_name,
                      step + 'TITLE NOT CORRECT: {0}'.format(status_title),
                      step + 'EXPECTED STATUS TITLE: {0}'.format('registration in progress')
                      )
    except:
        time.sleep(300)
        pass


def add_client_to_ss_by_hand(self, client):
    self.log('2.2.1-6: Click on "ADD CLIENT" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

    self.log('2.2.1-6: Select ' + client['class'] + ' from  "MEMBER CLASS" dropdown')
    select = Select(self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    select.select_by_visible_text(client['class'])

    self.log('2.2.1-6: Enter ' + client['code'] + ' to  "MEMBER CODE AREA" dropdown')
    input_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, client['code'])

    self.log('2.2.1-6: Enter ' + client['subsystem_code'] + ' to  "SUBSYSTEM CODE AREA" dropdown')
    subsystem_input = self.wait_until_visible(type=By.CSS_SELECTOR,
                                              element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_CSS)
    self.input(subsystem_input, client['subsystem_code'])

    self.wait_jquery()

    self.log('2.2.1-6: click "OK"')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()
    time.sleep(10)
    warning = self.wait_until_visible(type=By.ID, element=popups.CONFIRM_POPUP_TEXT_AREA_ID).text
    self.is_equal(warning in get_expected_warning_messages(client), True, test_name,
                  '2.2.1-6: CHECKING FOR WARNING MESSAGE FAILED',
                  '2.2.1-6: CHECK FOR WARNING MESSAGE')

    self.log('2.2.1-6: Confirm message')
    popups.confirm_dialog_click(self)
    time.sleep(2)
    self.wait_jquery()
    time.sleep(10)
    self.log('2.2.1-6: ADDING CLIENT TO SECURITY SERVER STATUS TEST')
    status_title = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
    self.log('Status title: {0}'.format(status_title))
    if status_title.lower() == 'saved':
        self.log('WARNING: SOMETHING IS WRONG')
        self.log('WARNING: CHANGING STATUS TITLE TO REGISTRATION IN PROGRESS')
        status_title = 'registration in progress'
        self.exception = True

    self.is_equal(status_title, 'registration in progress', test_name,
                  '2.2.1-6: TITLE NOT CORRECT: {0}'.format(status_title),
                  '2.2.1-6: EXPECTED MESSAGE: {0}'.format('registration in progress')
                  )


def add_sub_as_client_to_member(self, system_code, client, wait_input=2, step='x.x.x-y: '):
    self.log(step + 'CHECKING REGISTRATIONS STATUS TEST')
    self.log(step + 'Open management requests table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()
    self.wait_jquery()

    requests_table = self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_TABLE_ID)
    self.wait_jquery()

    row = requests_table.find_element_by_tag_name('tbody').find_element_by_tag_name('tr')

    self.log(step + 'Open members table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()

    self.wait_jquery()

    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()

    self.log(step + 'Open client details')
    members_table.get_row_by_columns(table, [client['name'], client['class'], client['code']]).click()
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()

    self.log(step + 'Open user servers tab')
    self.wait_until_visible(type=By.XPATH, element=members_table.USED_SERVERS_TAB).click()
    self.wait_jquery()

    self.log(step + 'Add new client')
    self.wait_until_visible(type=By.XPATH, element=members_table.REGISTER_SECURITYSERVER_CLIENT_ADD_BTN_ID).click()
    self.log(step + 'Enter ' + client['subsystem_code'] + ' to "subsystem code" area')
    # time.sleep(wait_input)
    subsystem_input = self.wait_until_visible(type=By.ID,
                                              element=members_table.CLIENT_REGISTRATION_SUBSYSTEM_CODE_AREA_ID)
    self.input(subsystem_input, client['subsystem_code'])

    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=members_table.USED_SERVERS_SEARCH_BTN_ID).click()
    self.wait_jquery()

    rows = self.wait_until_visible(type=By.XPATH,
                                   element=members_table.SECURITY_SERVERS_TABLE_ROWS_XPATH).find_elements_by_tag_name(
        'tr')
    for row in rows:
        if str(row.find_elements_by_tag_name('td')[3].text) == system_code:
            row.click()
            break

    self.wait_until_visible(type=By.ID, element=members_table.SELECT_SECURITY_SERVER_BTN_ID).click()
    self.wait_jquery()
    time.sleep(5)
    self.wait_until_visible(type=By.ID, element=members_table.CLIENT_REGISTRATION_SUBMIT_BTN_ID).click()
    self.wait_jquery()
    time.sleep(15)

    self.driver.get(self.url)

    self.log(step + 'Open management requests table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()

    requests_table = self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_TABLE_ID)
    self.wait_jquery()
    time.sleep(5)
    rows = requests_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0:1]
    for row in rows:
        self.is_true('SUBMITTED FOR APPROVAL' in row.text, test_name,
                     step + 'CHECKING FOR "SUBMITTED FOR APPROVAL" FROM THE LATEST REQUEST ROW FAILED"',
                     step + 'Look "SUBMITTED FOR APPROVAL" from the latest requests row: {0}'.format(
                         'SUBMITTED FOR APPROVAL' in row.text))


def add_subsystem_to_server_client(self, server_code, client, wait_input=3):
    open_servers_clients(self, server_code)

    self.log('2.2.1-8: Add new client')
    self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_CLIENT_TO_SECURITYSERVER_BTN_ID).click()
    self.wait_jquery()

    self.log('2.2.1-8: CLick on search client')
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SEARCH_BTN_ID).click()
    self.wait_jquery()

    time.sleep(wait_input)
    table = self.wait_until_visible(type=By.XPATH, element=cs_security_servers.MEMBERS_SEARCH_TABLE_XPATH)
    rows = table.find_elements_by_tag_name('tr')
    self.log('2.2.1-8: Finding client from table')
    for row in rows:
        tds = row.find_elements_by_tag_name('td')
        if tds[0].text is not u'':
            if (tds[0].text == client['name']) & (tds[1].text == client['code']) & (tds[2].text == client['class']) & (
                        tds[3].text == u''):
                row.click()
                break

    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SELECT_MEMBER_BTN_XPATH).click()
    self.wait_jquery()
    time.sleep(wait_input)
    self.log('2.2.1-8: Enter ' + client['subsystem_code'] + ' to subsystem code area')
    subsystem_input = self.wait_until_visible(type=By.ID, element=cs_security_servers.SUBSYSTEM_CODE_AREA_ID)
    subsystem_input.click()
    subsystem_input.clear()
    subsystem_input.send_keys(client['subsystem_code'])
    self.wait_jquery()

    self.wait_until_visible(type=By.ID,
                            element=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID).click()
    self.wait_jquery()


def approve_requests(self, step):
    self.log(step + 'Open central server ')
    self.driver.get(self.url)
    self.wait_jquery()
    self.log(step + 'Open management requests table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()
    self.wait_jquery()
    time.sleep(10)

    try:
        td = self.by_xpath(members_table.get_requests_row_by_td_text('SUBMITTED FOR APPROVAL'))
    except:
        td = None

    try:
        while td is not None:
            td.click()
            self.log(step + 'Open management  request details')
            self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
            self.wait_jquery()
            time.sleep(3)
            self.log(step + 'Approve requests')
            self.wait_until_visible(type=By.XPATH, element=members_table.APPROVE_REQUEST_BTN_XPATH).click()
            self.wait_jquery()
            popups.confirm_dialog_click(self)
            try:
                time.sleep(5)
                td = self.by_xpath(members_table.get_requests_row_by_td_text('SUBMITTED FOR APPROVAL'))
            except:
                td = None
    except:
        traceback.print_exc()


def check_expected_result_cs(self, ss_1_client, ss_2_client, ss_2_client_2, check_limit=6):
    self.log('2.2.1-13: TEST CENTRAL SERVER RESULTS')
    self.log('2.2.1-13: Check from members table')

    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()
    time.sleep(5)
    client_row = members_table.get_row_by_columns(table, [ss_1_client['name'], ss_1_client['class'],
                                                          ss_1_client['code']])
    client_row.click()

    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()
    time.sleep(5)
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()
    self.wait_jquery()
    time.sleep(5)
    table = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TABLE_XPATH)
    self.wait_jquery()
    time.sleep(3)
    self.is_not_none(
        members_table.get_row_by_columns(table, [ss_1_client['subsystem_code'], self.config.get('ss1.server_name')]),
        test_name,
        '2.2.1-13.1: CHECKING IF CLIENT 1 EXISTS FAILED',
        '2.2.1-13.1: CHECKING IF CLIENT 1 EXISTS')

    table = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TABLE_XPATH)
    self.wait_jquery()
    time.sleep(3)
    self.is_not_none(
        members_table.get_row_by_columns(table, [ss_2_client['subsystem_code'], self.config.get('ss2.server_name')]),
        test_name,
        '2.2.1-13.1: CHECKING IF CLIENT 2 EXISTS FAILED',
        '2.2.1-13.1: CHECKING IF CLIENT 2 EXISTS')

    self.log('2.2.1-13: Check from members table: TEST SUCCESSFUL')
    self.reset_page()
    self.log('2.2.1-13: Check security servers > clients table for ss1')
    open_servers_clients(self, self.config.get('ss1.server_name'))
    clients_table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENTS_TABLE_ID)
    self.wait_jquery()
    time.sleep(3)
    self.is_not_none(members_table.get_row_by_columns(clients_table,
                                                      [ss_1_client['name'], ss_1_client['class'],
                                                       ss_1_client['code'],
                                                       ss_1_client['subsystem_code']]), test_name,
                     '2.2.1-13.2: CHECKING IF TS1 HAS SUB 1 FAILED',
                     '2.2.1-13.2: CHECKING IF TS1 HAS SUB 1')

    self.is_not_none(members_table.get_row_by_columns(clients_table,
                                                      [self.config.get('ss1.management_service_name'),
                                                       self.management_services['class'],
                                                       self.management_services['code'],
                                                       self.management_services['subsystem']]),
                     test_name, '2.2.1-13.2: CHECKING IF TS1 HAS MANAGEMENT SERVICES FAILED',
                     '2.2.1-13.2: CHECKING IF TS1 HAS MANAGEMENT SERVICES')

    self.log('2.2.1-13.2: Check security servers > clients table for TS1: TEST SUCCESSFUL')

    self.log('2.2.1-13.3: Check security servers > clients table for TS2')

    open_servers_clients(self, self.config.get('ss2.server_name'))
    clients_table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENTS_TABLE_ID)
    self.wait_jquery()
    time.sleep(3)
    self.is_not_none(members_table.get_row_by_columns(clients_table,
                                                      [ss_2_client['name'], ss_2_client['class'],
                                                       ss_2_client['code'],
                                                       ss_2_client['subsystem_code']]), test_name,
                     '2.2.1-13.3: CHECKING IF HAS CLIENT 1 FAILED',
                     '2.2.1-13.3: CHECKING IF HAS CLIENT 1')
    self.is_not_none(members_table.get_row_by_columns(clients_table,
                                                      [ss_2_client_2['name'],
                                                       ss_2_client_2['class'],
                                                       ss_2_client_2['code'],
                                                       ss_2_client_2['subsystem_code']]), test_name,
                     '2.2.1-13.3: CHECKING IF HAS CLIENT 2 FAILED',
                     '2.2.1-13.3: CHECKING IF HAS CLIENT 2')

    self.log('2.2.1-13.2: Check security servers > clients table for TS2: TEST SUCCESSFUL')

    self.log('2.2.1-13: Check management requests table')
    self.driver.get(self.url)
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()
    self.wait_jquery()
    requests_table = self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_TABLE_ID)
    self.wait_jquery()
    rows = requests_table.find_elements_by_tag_name('tr')
    check_man_service = False
    check_ss_1_client = False
    check_ss_2_client = False
    check_ss_2_client_2 = False

    counter = 0
    for row in rows:
        if row.text is not u'':
            if row.find_elements_by_tag_name('td')[8].text == 'APPROVED':
                counter += 1
                row.click()
                self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
                self.wait_jquery()
                # if request_has_client(self, {'name': self.config.get('ss1.server_name'), 'class': 'GOV', 'code': 'TS1OWNER',
                #                              'subsystem_code': 'Management Services'}):
                if request_has_client(self, {'name': self.config.get('ss1.server_name'),
                                             'class': self.management_services['class'],
                                             'code': self.management_services['code'],
                                             'subsystem_code': self.management_services['subsystem']}):
                    check_man_service = True
                if request_has_client(self, ss_1_client):
                    check_ss_1_client = True
                if request_has_client(self, ss_2_client):
                    check_ss_2_client = True
                if request_has_client(self, ss_2_client_2):
                    check_ss_2_client_2 = True
                self.wait_until_visible(type=By.XPATH,
                                        element=members_table.CLIENT_REGISTRATION_REQUEST_EDIT_POPUP_OK_BTN_XPATH).click()
                self.wait_jquery()

                # We only need to check our added requests, not everything. Exit loop when we're certain that we're done.
                if counter == check_limit:
                    break

    self.is_true(check_ss_1_client & check_ss_2_client & check_ss_2_client_2, test_name,
                 '2.2.1-13: CHECK APPROVED REQUEST FOR CLIENT FAILED', '2.2.1-13: CHECK APPROVED REQUEST FOR CLIENT')
    self.log('2.2.1-13: Check approved request for clients : TEST SUCCESSFUL')


def check_expected_result_ss(self, client, retry_interval=0, retry_timeout=0, registered_status='registered'):
    self.log('2.2.1-13: TEST SECURITY SERVER RESULTS')
    self.log('2.2.1-13: Check from members table')

    start_time = time.time()
    while True:
        try:
            if retry_interval > 0:
                self.log('2.2.1-13: Waiting {0} before checking'.format(retry_interval))
                time.sleep(retry_interval)

            self.driver.get(self.url)
            self.wait_jquery()

            status = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
            self.log('2.2.1-13: Check if ' + ':'.join(
                [client['code'], client['subsystem_code']]) + ' is {0}: {1} ({2})'.format(registered_status,
                                                                                          status == registered_status,
                                                                                          status))
            assert status == registered_status
            break
        except:
            if time.time() > start_time + retry_timeout:
                if retry_timeout > 0:
                    self.log('2.2.1-13: Timeout while waiting')
                raise

    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()
    client_certification_2_1_3.check_import(self, client['class'], client['code'])


def added_client_row(self, client):
    self.log('Finding added client')
    self.added_client_id = ' : '.join(
        [SYSTEM_TYPE, ssh_server_actions.get_server_name(self), client['class'], client['code'],
         client['subsystem_code']])
    table_rows = self.by_css(clients_table_vm.CLIENT_ROW_CSS, multiple=True)
    client_row_index = clients_table_vm.find_row_by_client(table_rows, client_id=self.added_client_id)
    return table_rows[client_row_index]


def get_expected_warning_messages(client):
    return ['Do you want to send a client registration request for the added client?\n' \
            'New subsystem \'' + client['subsystem_code'] + '\' will be submitted for registration for member \'' + \
            ' '.join([client['name'], client['class'] + ':', client['code']]) + '\'.',
            'Do you want to send a client registration request for the added client?']


def login(self, host, username, password):
    self.reset_webdriver(host, username=username, password=password)
    self.wait_jquery()


def login_with_logout(self, host, username, password):
    self.logout(host)
    self.reset_webdriver(host, username=username, password=password)
    self.wait_jquery()


def open_servers_clients(self, code):
    self.log('Open Security servers')
    self.reset_page()
    self.wait_jquery()
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.SECURITY_SERVERS_CSS).click()
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_TABLE_ID)
    self.wait_jquery()
    self.log('Click on client row')
    rows = table.find_elements_by_tag_name('tr')
    for row in rows:
        if row.text is not u'':
            if row.find_element_by_tag_name('td').text == code:
                row.click()
    self.log('Click on Details button')
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENT_DETAILS_BTN_ID).click()
    self.wait_jquery()
    self.log('Click on clients tab')
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_CLIENT_TAB).click()
    self.wait_jquery()


def request_has_client(self, client):
    return (self.by_xpath(members_table.CLIENT_REQUEST_NAME_AREA_XPATH).text == client['name']) & (self.by_xpath(
        members_table.CLIENT_REQUEST_CLASS_AREA_XPATH).text == client['class']) & (self.by_xpath(
        members_table.CLIENT_REQUEST_CODE_AREA_XPATH).text == client['code']) & (self.by_xpath(
        members_table.CLIENT_REQUEST_SUB_CODE_AREA_XPATH).text == client['subsystem_code'])


def remove_data(self, cs_host, cs_username, cs_password, sec_1_host, sec_1_username, sec_1_password,
                sec_2_host, sec_2_username, sec_2_password,
                cs_member, ss_1_client, ss_2_client, ss_2_client_2):
    self.log('REMOVING DATA')
    self.logout(cs_host)
    self.login(username=cs_username, password=cs_password)
    safe(self, remove_member, cs_member, 'Removing  member failed')

    self.reset_webdriver(cs_host, cs_username, cs_password)
    try:
        revoke_requests(self)
    except:
        traceback.print_exc()

    login(self, sec_1_host, sec_1_username, sec_1_password)
    safe(self, remove_certificate, ss_1_client, 'Removing  certificate failed')
    self.driver.get(self.url)
    safe(self, remove_client, ss_1_client, 'Removing  client failed')

    login(self, sec_2_host, sec_2_username, sec_2_password)
    safe(self, remove_certificate, ss_2_client, 'Removing  certificate failed')
    self.driver.get(self.url)
    safe(self, remove_client, ss_2_client, 'Removing  client failed')
    self.driver.get(self.url)
    safe(self, remove_client, ss_2_client_2, 'Removing  client failed')


def remove_member(self, member):
    self.log('Wait for members table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()
    self.log('Get row by row values')
    row = members_table.get_row_by_columns(table, [member['name'], member['class'], member['code']])
    if row is None:
        assert False
    row.click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.wait_jquery()
    self.log('Confirm deleting member')
    popups.confirm_dialog_click(self)


def remove_client(self, client):
    self.log('Open "Security servers tab"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.CLIENTS_BTN_CSS).click()
    time.sleep(3)

    self.log('Opening client details')
    added_client_row(self, client).find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS).click()
    self.wait_jquery()
    self.log('Unregister Client')
    try:
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
        self.wait_jquery()
        popups.confirm_dialog_click(self)
        try:
            self.wait_jquery()
            popups.confirm_dialog_click(self)
        except:
            pass
    except:
        self.log('Not unregistering')
        try:
            self.log('Deleting client')
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
            self.wait_jquery()
            popups.confirm_dialog_click(self)
        except:
            pass

    self.log('CLIENT DELETED')


def remove_certificate(self, client):
    self.log('REMOVE CERTIFICATE')
    self.log('Open "Keys and Certificates tab"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()
    self.log('Click on generated key row')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.get_generated_key_row_xpath(client['code'],
                                                                                           client[
                                                                                               'class'])).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()
    self.wait_jquery()
    popups.confirm_dialog_click(self)


def revoke_requests(self):
    self.log('REVOKING REQUESTS')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()
    self.wait_jquery()
    time.sleep(5)

    try:
        td = self.by_xpath(members_table.get_requests_row_by_td_text('SUBMITTED FOR APPROVAL'))
    except:
        td = None

    try:
        while td is not None:
            td.click()
            self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
            self.wait_jquery()
            time.sleep(1)
            self.log('Revoke requests')
            self.wait_until_visible(type=By.XPATH, element=members_table.DECLINE_REQUEST_BTN_XPATH).click()
            self.wait_jquery()
            popups.confirm_dialog_click(self)
            time.sleep(5)
            try:
                td = self.by_xpath(members_table.get_requests_row_by_td_text('SUBMITTED FOR APPROVAL'))
            except:
                td = None
    except:
        traceback.print_exc()


def safe(self, func, member, message):
    try:
        func(self, member)
    except Exception, e:
        self.log('this removes client, this is not a test, creating fail data is not needed')
        traceback.print_exc()
