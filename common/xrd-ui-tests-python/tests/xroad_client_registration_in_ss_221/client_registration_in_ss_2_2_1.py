import time
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from helpers import ssh_server_actions, auditchecker, ssh_client
from tests.xroad_ss_client_certification_213 import client_certification_2_1_3
from view_models import members_table, clients_table_vm, sidebar, popups, \
    keys_and_certificates_table as keyscertificates_constants, cs_security_servers, log_constants, messages, \
    groups_table
from view_models.keys_and_certificates_table import APPROVED
from view_models.log_constants import DELETE_SUBSYSTEM, REVOKE_AUTH_REGISTRATION_REQUEST, DELETE_CLIENT
from view_models.members_table import MANAGEMENT_REQUEST_TABLE_ID

SYSTEM_TYPE = 'SUBSYSTEM'

test_name = '2.2.1 CLIENT REGISTRATION IN SECURITY SERVER'


def test_remove(cs_host, cs_username, cs_password,
                sec_1_host, sec_1_username, sec_1_password,
                sec_2_host, sec_2_username, sec_2_password,
                ss1_ssh_host=None, ss1_ssh_username=None, ss1_ssh_password=None,
                ss2_ssh_host=None, ss2_ssh_username=None, ss2_ssh_password=None,
                cs_new_member=None, ss1_client=None, ss1_client_2=None, ss2_client=None, ss2_client_2=None,
                cs_member_name=None, ss1_client_name=None, ss1_client_2_name=None, ss2_client_name=None,
                ss2_client_2_name=None,
                ca_ssh_host=None, ca_ssh_username=None, ca_ssh_password=None,
                cs_ssh_host=None, cs_ssh_username=None, cs_ssh_password=None, global_group=None):
    """
    Removes the data that was created when running the main test.
    :param global_group: str - global group name
    :param cs_ssh_password: str - central server ssh password
    :param cs_ssh_username: str - central server ssh username
    :param cs_ssh_host: str - central server ssh host
    :param ss1_client_2_name: str - security server 1 client 2 name
    :param ss1_client_2: dict - security server 1 client 2 data
    :param ss2_ssh_host: str - security server 2 ssh hostname
    :param ss2_ssh_username: str - security server 2 ssh username
    :param ss2_ssh_password: str - security server 2 ssh password
    :param ss1_ssh_password: str - security server 1 ssh password
    :param ss1_ssh_username: str - security server 1 ssh username
    :param ss1_ssh_host: str - security server 1 hostname
    :param cs_host: str - central server hostname
    :param cs_username: str - central server UI username
    :param cs_password: str - central server UI password
    :param sec_1_host: str - security server 1 hostname
    :param sec_1_username: str - security server 1 UI username
    :param sec_1_password: str - security server 1 UI password
    :param sec_2_host: str - security server 2 hostname
    :param sec_2_username: str - security server 2 UI username
    :param sec_2_password: str - security server 2 UI password
    :param cs_new_member: dict - central server new member data
    :param ss1_client: dict - security server 1 new client data
    :param ss2_client: dict - security server 2 new client data
    :param ss2_client_2: dict - security server 2 second client data
    :param cs_member_name: str - central server member name
    :param ss1_client_name: str - security server 1 client name
    :param ss2_client_name: str - security server 2 client name
    :param ss2_client_2_name: str - security server 2 second client name
    :param ca_ssh_host: str - CA ssh host
    :param ca_ssh_username: str - CA ssh username
    :param ca_ssh_password: str - CA ssh password
    :return: None
    """

    def test_case(self):
        '''
        Main function for removing the data.
        :param self: MainController object
        :return: None
        '''
        # TEST PLAN 2.2.1 removing the data that was created during 2.2.1
        self.log('2.2.1-del Remove data we created during the test.')

        cs_member = {'name': cs_member_name, 'class': cs_new_member['class'], 'code': cs_new_member['code']}

        ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                       'subsystem_code': ss1_client['subsystem']}

        ss_1_client_2 = {'name': ss1_client_2_name, 'class': ss1_client_2['class'], 'code': ss1_client_2['code'],
                         'subsystem_code': ss1_client_2['subsystem']}

        ss_2_client = {'name': ss2_client_name, 'class': ss2_client['class'], 'code': ss2_client['code'],
                       'subsystem_code': ss2_client['subsystem']}

        ss_2_client_2 = {'name': ss2_client_2_name, 'class': ss2_client_2['class'], 'code': ss2_client_2['code'],
                         'subsystem_code': ss2_client_2['subsystem']}
        try:
            # Remove the members and subsystems
            remove_data(self, cs_host, cs_username, cs_password, sec_1_host, sec_1_username, sec_1_password,
                        ss1_ssh_host, ss1_ssh_username, ss1_ssh_password,
                        sec_2_host, sec_2_username, sec_2_password,
                        ss2_ssh_host, ss2_ssh_username, ss2_ssh_password,
                        cs_member, ss_1_client, ss_1_client_2, ss_2_client,
                        ss_2_client_2, ca_ssh_host=ca_ssh_host, ca_ssh_username=ca_ssh_username,
                        ca_ssh_password=ca_ssh_password, cs_ssh_host=cs_ssh_host, cs_ssh_username=cs_ssh_username,
                        cs_ssh_password=cs_ssh_password, global_group=global_group)
        except:
            # Something went wrong
            self.log('Failed to remove client.')
            traceback.print_exc()
            assert False, '2.2.1 failed to remove client'

    return test_case


def test_test(case, cs_host, cs_username, cs_password,
              sec_1_host, sec_1_username, sec_1_password,
              sec_2_host, sec_2_username, sec_2_password,
              cs_new_member=None, ss1_client=None, ss1_client_2=None, ss2_client=None, ss2_client_2=None,
              cs_member_name=None, ss1_client_name=None, ss1_client_2_name=None, ss2_client_name=None,
              ss2_client_2_name=None, ss1_ssh_host=None, ss1_ssh_user=None, ss1_ssh_pass=None,
              remove_added_data=True, ss2_ssh_host=None, ss2_ssh_user=None, ss2_ssh_pass=None, ss1_host=None,
              ss1_server_name=None, ss2_server_name=None, ca_ssh_host=None, ca_ssh_username=None, ca_ssh_password=None,
              global_group=None, cs_ssh_host=None, cs_ssh_user=None, cs_ssh_pass=None):
    """

    :param ss2_ssh_user: str - security server 2 ssh user
    :param ss2_ssh_host: str - security server 2 ssh host
    :param ss1_host: str - security server 1 host
    :param ss2_ssh_pass: str - security server 2 ssh pass
    :param ss1_ssh_pass: str - security server 1 ssh pass
    :param ss1_ssh_host: str - security server 1 ssh host
    :param ssl_ssh_user: str - security server 1 ssh user
    :param ss1_client_2_name: str - security server 1 client 2 name
    :param ss1_client_2: dict - security server 1 client 2 data
    :param case: MainController object
    :param cs_host: str - central server hostname
    :param cs_username: str - central server UI username
    :param cs_password: str - central server UI password
    :param sec_1_host: str - security server 1 hostname
    :param sec_1_username: str - security server 1 UI username
    :param sec_1_password: str - security server 1 UI password
    :param sec_2_host: str - security server 2 hostname
    :param sec_2_username: str - security server 2 UI username
    :param sec_2_password: str - security server 2 UI password
    :param cs_new_member: dict - central server new member data
    :param ss1_client: dict - security server 1 new client data
    :param ss2_client: dict - security server 2 new client data
    :param ss2_client_2: dict - security server 2 second client data
    :param cs_member_name: str - central server member name
    :param ss1_client_name: str - security server 1 client name
    :param ss2_client_name: str - security server 2 client name
    :param ss2_client_2_name: str - security server 2 second client name
    :param remove_added_data: bool - True to remove the data after testing; False otherwise
    :param ca_ssh_host: str - CA ssh host
    :param ca_ssh_username: str - CA ssh username
    :param ca_ssh_password: str - CA ssh password
    :return: None
    """
    self = case
    sync_retry = 30
    sync_timeout = 120
    wait_input = 2  # delay in seconds before starting to look for input fields before entering text to them
    registered_status = 'registered'

    def test_case():
        """
        Executes the test.
        :return: None
        """
        # TEST PLAN 2.2.1 registering clients to security servers
        self.log('*** 2.2.1 / XT-465')

        # Create member objects using supplied parameters
        cs_member = {'name': cs_member_name, 'class': cs_new_member['class'], 'code': cs_new_member['code']}

        ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                       'subsystem_code': ss1_client['subsystem']}

        ss_1_client_2 = {'name': ss1_client_2_name, 'class': ss1_client_2['class'], 'code': ss1_client_2['code'],
                         'subsystem_code': ss1_client_2['subsystem']}

        ss_2_client = {'name': ss2_client_name, 'class': ss2_client['class'], 'code': ss2_client['code'],
                       'subsystem_code': ss2_client['subsystem']}

        ss_2_client_2 = {'name': ss2_client_2_name, 'class': ss2_client_2['class'], 'code': ss2_client_2['code'],
                         'subsystem_code': ss2_client_2['subsystem']}

        delete_client = remove_added_data

        # Initialize errors and exceptions to be False
        error = False
        self.exception = False
        try:
            # TEST PLAN 2.2.1-1 add member to Central Server
            self.log('2.2.1-1 add member to Central Server')

            # Log in to Central Server
            login(self, cs_host, cs_username, cs_password)

            # Add members to Central Server
            add_member_to_cs(self, cs_member)
            popups.close_all_open_dialogs(self)
            add_member_to_cs(self, ss_1_client_2)

            # TEST PLAN 2.2.1-2 add the new member''s subsystem as a client to Security Server 1
            self.log('2.2.1-2 add the new member''s subsystem as a client to Security Server 1')
            # Log in to Security Server 1
            login(self, sec_1_host, sec_1_username, sec_1_password)

            self.log('Wait {0} seconds for the change'.format(sync_timeout))
            time.sleep(sync_timeout)
            '''Add client to Security Server 1'''
            add_client_to_ss(self, ss_1_client_2, retry_interval=sync_retry, retry_timeout=sync_timeout,
                             wait_input=wait_input, step='2.2.1-2: ')
            self.driver.get(sec_1_host)
            '''Certifiy added client'''
            client_certification_2_1_3.test_generate_csr_and_import_cert(client_code=ss_1_client_2['code'],
                                                                         client_class=ss_1_client_2['class'])(self)
            login_with_logout(self, cs_host, cs_username, cs_password)
            '''Add subsystem to member'''
            add_sub_as_client_to_member(self, self.config.get('ss1.server_name'), ss_1_client_2, wait_input=wait_input)
            '''Approve requests'''
            approve_requests(self, cancel_confirmation=True, use_case='MEMBER_37')

            login(self, sec_1_host, sec_1_username, sec_1_password)
            # Add client to Security Server 1
            add_client_to_ss(self, ss_1_client, retry_interval=sync_retry, retry_timeout=sync_timeout,
                             wait_input=wait_input, step='2.2.1-2: ')

            # TEST PLAN 2.2.1-3 certify the new member in Security Server 1
            self.log('2.2.1-3 certify the new member in Security Server 1')
            self.driver.get(sec_1_host)
            # Create signing certificate using helper scenario 2.1.3
            client_certification_2_1_3.test_generate_csr_and_import_cert(client_code=ss_1_client['code'],
                                                                         client_class=ss_1_client['class'])(self)

            # TEST PLAN 2.2.1-4 add a registration request for the newly added subsystem in Central Server
            self.log('2.2.1-4 add a registration request for the newly added subsystem in Central Server')
            # Log in to Central Server
            login_with_logout(self, cs_host, cs_username, cs_password)

            # Add subsystem to member
            add_sub_as_client_to_member(self, self.config.get('ss1.server_name'), ss_1_client, wait_input=wait_input,
                                        step='2.2.1-4: ')

            # TEST PLAN 2.2.1-5 approve the registration requests
            self.log('2.2.1-5 approve the registration requests')
            # Approve registration requests
            approve_requests(self, '2.2.1-5 ', cancel_confirmation=True)
            self.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)

            self.log('MEMBER_39 Revoke a Registration Request')
            '''Make copy of ss1client to make another client, which gets revoked'''
            revoke_client = ss_1_client.copy()
            '''Replace subsystem information'''
            revoke_client['subsystem'] = 'revoke'
            revoke_client['subsystem_code'] = 'revoke'
            self.log('Add new client to member, which will be revoked')
            add_sub_as_client_to_member(self, self.config.get('ss1.server_name'), revoke_client, wait_input=wait_input,
                                        check_request=False)
            revoke_requests(self, try_cancel=True,
                            log_checker=auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass))
            popups.close_all_open_dialogs(self)
            '''Remove added client'''
            remove_client_subsystem(self, revoke_client)

            # TEST PLAN 2.2.1-6 add a new subsystem as a client to Security Server 2
            self.log('2.2.1-6 add a new subsystem as a client to Security Server 2')

            # Log in to Security Server 2
            login(self, sec_2_host, sec_2_username, sec_2_password)

            '''Add client to Security Server 2'''
            add_client_to_ss_by_hand(self, ss_2_client, ssh_host=ss2_ssh_host,
                                     ssh_user=ss2_ssh_user, ssh_pass=ss2_ssh_pass)

            '''Create client with different code for testing errors'''
            fail_client = ss_2_client.copy()
            fail_client['code'] = 'asd123'

            '''MEMBER_48 4a. sending of the registration request failed'''
            add_client_to_ss_by_hand(self, fail_client, check_send_errors=True, ssh_host=ss2_ssh_host,
                                     ssh_user=ss2_ssh_user, ssh_pass=ss2_ssh_pass, ss_host=ss1_host)

            # TEST PLAN 2.2.1-7 certify the new member in Security Server 2
            self.log('2.2.1-7 certify the new member in Security Server 2')

            login_with_logout(self, sec_2_host, sec_2_username, sec_2_password)
            # Create signing certificate for the client using helper scenario 2.1.3
            client_certification_2_1_3.test_generate_csr_and_import_cert(client_code=ss_2_client['code'],
                                                                         client_class=ss_2_client['class'])(self)

            # TEST PLAN 2.2.1-8 add a registration request for the newly added subsystem (SS2) in Central Server
            self.log('2.2.1-8 add a registration request for the newly added subsystem (SS2) in Central Server')

            # Log in to Central Server
            login_with_logout(self, cs_host, cs_username, cs_password)

            # Add subsystem to member
            add_subsystem_to_server_client(self, self.config.get('ss2.server_name'), ss_2_client, wait_input=wait_input)

            self.log('Wait {0} for sync'.format(sync_retry))
            time.sleep(sync_retry)

            # TEST PLAN 2.2.1-9 approve the registration requests
            self.log('2.2.1-9 approve the registration requests')

            # Approve registration requests
            approve_requests(self, '2.2.1-9: ')

            # TEST PLAN 2.2.1-10 add a second subsystem as a client to Security Server 2
            self.log('2.2.1-10 add a second subsystem as a client to Security Server 2')

            # Log in to Security Server 2
            login_with_logout(self, sec_2_host, sec_2_username, sec_2_password)

            # Add a client to Security Server 2
            add_client_to_ss(self, ss_2_client_2, wait_input=wait_input, step='2.2.1-10: ')

            # TEST PLAN 2.2.1-11 add a registration request for the second subsystem (SS2) in Central Server
            self.log('2.2.1-11 add a registration request for the second subsystem (SS2) in Central Server')

            # Log in to Central Server
            login_with_logout(self, cs_host, cs_username, cs_password)

            # Add subsystem to the client
            add_sub_as_client_to_member(self, self.config.get('ss2.server_name'), ss_2_client_2, wait_input=wait_input,
                                        step='2.2.1-11: ')

            self.log('Wait {0} for sync'.format(sync_retry))
            time.sleep(sync_retry)

            # TEST PLAN 2.2.1-12 approve the registration requests
            self.log('2.2.1-12 approve the registration requests')

            # Approve registration requests
            approve_requests(self, '2.2.1-12: ')

            if self.exception:
                error = True
                raise RuntimeError(
                    '2.2.1 Test failed. Please check that all previously added clients have been deleted.')

            # TEST PLAN 2.2.1-check verify that everything succeeded
            # Some checks have already been done right after adding the clients and if they failed, the test
            # has already failed and gone to the except-block before getting to this point.
            self.log('2.2.1-check verify that everything succeeded')

            # TEST PLAN 2.2.1-check verify that the members and subsystems are visible in Central Server
            self.log('2.2.1-check verify that the members and subsystems are visible in Central Server')
            # Log in to Central Server
            login_with_logout(self, cs_host, cs_username, cs_password)

            # Check for expected result
            check_expected_result_cs(self, ss_1_client, ss_2_client, ss_2_client_2)

            # TEST PLAN 2.2.1-check verify that the clients are visible in Security Server 1
            self.log('2.2.1-check verify that the clients are visible in Security Server 1')
            # log in to Security Server 1
            login_with_logout(self, sec_1_host, sec_1_username, sec_1_password)

            # Check if client has been registered
            check_expected_result_ss(self, ss_1_client, retry_interval=sync_retry, retry_timeout=sync_timeout)

            # TEST PLAN 2.2.1-check verify that the clients are visible in Security Server 2
            self.log('2.2.1-check verify that the clients are visible in Security Server 2')

            # Log in to Security Server 2
            login_with_logout(self, sec_2_host, sec_2_username, sec_2_password)

            # Check if client has been registered
            check_expected_result_ss(self, ss_2_client, registered_status=registered_status, retry_interval=sync_retry,
                                     retry_timeout=sync_timeout)

            # Check if client 2 has been registered
            check_expected_result_ss(self, ss_2_client_2, registered_status=registered_status,
                                     retry_interval=sync_retry, retry_timeout=sync_timeout)

        except Exception:
            # We got an exception, so the test failed. Save screenshot and traceback to a file.
            delete_client = True
            self.save_exception_data()
            traceback.print_exc()
            error = True
        finally:
            # Delete the client
            if delete_client:
                self.log('2.2.1-del Deleting client')
                # Remove all data we created
                try:
                    remove_data(self, cs_host=cs_host, cs_username=cs_username, cs_password=cs_password,
                                sec_1_host=sec_1_host,
                                sec_1_username=sec_1_username, sec_1_password=sec_1_password,
                                sec_1_ssh_host=ss1_ssh_host, sec_1_ssh_username=ss1_ssh_user,
                                sec_1_ssh_password=ss1_ssh_pass,
                                sec_2_ssh_host=ss2_ssh_host, sec_2_ssh_username=ss2_ssh_user,
                                sec_2_ssh_password=ss2_ssh_pass,
                                sec_2_host=sec_2_host, sec_2_username=sec_2_username, sec_2_password=sec_2_password,
                                cs_member=cs_member, ss_1_client=ss_1_client, ss_2_client=ss_2_client,
                                ss_2_client_2=ss_2_client_2, ca_ssh_host=ca_ssh_host, ca_ssh_username=ca_ssh_username,
                                ca_ssh_password=ca_ssh_password, cs_ssh_host=cs_ssh_host, cs_ssh_username=cs_ssh_user,
                                cs_ssh_password=cs_ssh_pass, ss_1_client_2=ss_1_client_2, global_group=global_group)
                except:
                    self.log('2.2.1 Client deletion FAILED')
            # If we got an error previously, raise an exception
            if error:
                assert False, '2.2.1 failed'

    return test_case


def add_member_to_cs(self, member):
    '''
    Adds a member to Central Server.
    :param self: MainController object
    :param member: dict - member data
    :return: None
    '''
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
    '''
    Adds a client to security server.
    :param self: MainController object
    :param client: dict - client data
    :param retry_interval: int - retry interval in seconds (if changes have not yet propagated)
    :param retry_timeout: int - retry timeout in seconds
    :param wait_input: int - time in seconds to wait before entering text in input fields
    :param step: str - prefix to be added to logs
    :return: None
    '''
    self.log(step + 'Click on "ADD CLIENT" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

    self.log(step + 'Click on "SELECT CLIENT FROM GLOBAL LIST" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.SELECT_CLIENT_FROM_GLOBAL_LIST_BTN_ID).click()
    self.wait_jquery()

    # Allow listing of global clients
    c_box = self.wait_until_visible(type=By.ID, element=clients_table_vm.SHOW_ONLY_LOCAL_CLIENTS_CHECKBOX_ID)
    if c_box.is_selected():
        c_box.click()
    start_time = time.time()
    while True:
        # Loop until timeout or success
        try:
            # If retry_interval set, sleep for a while
            if retry_interval > 0:
                self.log(step + 'Waiting {0} before searching'.format(retry_interval))
                time.sleep(retry_interval)

            # Try to find our client from global list
            self.log(step + 'Searching global list for clients')

            self.wait_until_visible(type=By.XPATH, element=clients_table_vm.GLOBAL_CLIENT_LIST_SEARCH_BTN_XPATH).click()
            self.wait_jquery()

            table = self.wait_until_visible(type=By.ID, element=clients_table_vm.GLOBAL_CLIENTS_TABLE_ID)
            self.wait_jquery()

            self.log(step + 'Searching for client row')

            # Try to get the row associated with the client. If not found, we'll get an exception.
            member_row = members_table.get_row_by_columns(table, [client['name'], client['class'], client['code']])

            self.wait_jquery()
            member_row.click()
            # If we got here, client was found
            self.log(step + 'Found client row')
            break
        except:
            # Check if timeout
            if time.time() > start_time + retry_timeout:
                # Got a timeout, raise exception
                if retry_timeout > 0:
                    self.log(step + 'Timeout while waiting')
                raise
            # No timeout, continue loop
            self.log(step + 'Client row not found')

    # Click "OK"
    self.wait_jquery()

    self.log(step + 'confirm popup')
    self.wait_until_visible(type=By.XPATH, element=clients_table_vm.SELECT_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # Enter data to form
    subsystem_input = self.wait_until_visible(type=By.XPATH,
                                              element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_XPATH)
    self.wait_jquery()

    self.input(subsystem_input, client['subsystem_code'], click=False)

    # Try to add client
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    # Confirm the popup that should have opened
    warning = self.wait_until_visible(type=By.ID, element=popups.CONFIRM_POPUP_TEXT_AREA_ID).text
    self.wait_jquery()

    self.log('MEMBER_48 2a.1 When adding client with not existing subsystem, a warning is shown')
    self.is_true(warning in get_expected_warning_messages(client), test_name,
                 step + 'WARNING NOT CORRECT: {0}'.format(
                     warning),
                 step + 'EXPECTED WARNING MESSAGE: "{0}" GOT: "{1}"'.format(
                     get_expected_warning_messages(client),
                     warning))

    self.log('MEMBER_48 2a.2 Warning popup is confirmed')
    popups.confirm_dialog_click(self)

    # Check status
    self.log(step + 'ADDING CLIENT TO SECURITY SERVER STATUS TEST')
    status_title = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
    try:
        self.is_equal(status_title, 'registration in progress', test_name,
                      step + 'TITLE NOT CORRECT: {0}'.format(status_title),
                      step + 'EXPECTED STATUS TITLE: {0}'.format('registration in progress')
                      )
    except:
        time.sleep(5)
        pass


def add_client_to_ss_by_hand(self, client, check_send_errors=False, ss_host=None, ssh_host=None,
                             ssh_user=None, ssh_pass=None):
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
    client_class = client['class']
    self.log('MEMBER_47 2. Set the class to {0}'.format(client_class))
    select = Select(self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    select.select_by_visible_text(client_class)

    client_code = client['code']
    self.log('MEMBER_47 2. Set the member code to {0}'.format(client_code))
    input_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, client_code)

    client_subsystem_code = client['subsystem_code']
    self.log('MEMBER_47 2. Set the subsystem code to {0}'.format(client_subsystem_code))
    subsystem_input = self.wait_until_visible(type=By.XPATH,
                                              element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_XPATH)
    self.input(subsystem_input, client_subsystem_code)

    self.wait_jquery()
    if ssh_host is not None:
        log_checker = auditchecker.AuditChecker(ssh_host, ssh_user, ssh_pass)
        current_log_lines = log_checker.get_line_count()

    '''Try to save the client'''
    self.log('Click "OK"')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()
    self.wait_jquery()

    if check_send_errors:
        self.log('MEMBER_48 4a. sending of the registration request failed')
        hosts_replacement = 'asd.asd'
        try:
            self.ssh_client = ssh_client.SSHClient(ssh_host, ssh_user, ssh_pass)
            self.ssh_client.exec_command('sed -i -e "s/{0}/{1}/g" {2}'.format(ss_host, hosts_replacement,
                                                                              '/etc/hosts'), sudo=True)
            '''Continue warning popup when visible'''
            self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
            self.wait_jquery()
            popups.confirm_dialog_click(self)

            self.log('MEMBER_48 4a.1 System displays the error message: '
                     '"Failed to send registration request: X", where X is description of the error')
            '''Wait until error message is visible'''
            error_msg = self.wait_until_visible(type=By.CSS_SELECTOR, element=messages.ERROR_MESSAGE_CSS).text
            '''Check if error message is as expected'''
            self.is_true(error_msg.startswith(messages.REGISTRATION_REQUEST_SENDING_FAILED))

            self.log('MEMBER_48 4a.2 System logs the event "Register client failed" to the audit log')
            '''Check if "Register client failed" is in audit log'''
            logs_found = log_checker.check_log(log_constants.REGISTER_CLIENT_FAILED,
                                               from_line=current_log_lines + 1)
            self.is_true(logs_found, msg='"Register client failed" event not found in log"')
        except:
            self.log('Failure when checking client registration errors')
            assert False
        finally:
            '''Restoring hosts file'''
            self.ssh_client.exec_command(
                'sed -i -e "s/{0}/{1}/g" {2}'.format(hosts_replacement, ss_host, '/etc/hosts'),
                sudo=True)
            '''Removing added client'''
            remove_client(self=self, client=client)
            return

    warning = self.wait_until_visible(type=By.ID, element=popups.CONFIRM_POPUP_TEXT_AREA_ID).text
    self.is_true(warning in get_expected_warning_messages(client))

    '''Confirm adding the client.'''
    self.log('2.2.1-6: Confirm message')
    popups.confirm_dialog_click(self)
    self.wait_jquery()

    '''Try to find the client in client list and check the status'''
    self.log('2.2.1-6: ADDING CLIENT TO SECURITY SERVER STATUS TEST')
    status_title = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
    self.log('Status title: {0}'.format(status_title))
    if status_title.lower() == clients_table_vm.CLIENT_STATUS_SAVED:
        # Something is wrong, status should be "registration in progress". Set the exception to be raised
        # later but go on with the current test.
        self.log('2.2.1-6 WARNING: status should be "registration in progress" but is "saved"')
        self.log('2.2.1-6 WARNING: CONTINUING TEST WITH STATUS "saved"')
        status_title = 'registration in progress'
        self.exception = True

    self.is_equal(status_title, 'registration in progress', test_name,
                  '2.2.1-6: TITLE NOT CORRECT: {0}'.format(status_title),
                  '2.2.1-6: EXPECTED MESSAGE: {0}'.format('registration in progress')
                  )

    if log_checker is not None:
        '''MEMBER_48 7. System logs the event "Register client" to the audit log'''
        self.log('MEMBER_48 7. System logs the event "Register client" to the audit log')
        time.sleep(1.5)
        logs_found = log_checker.check_log(log_constants.REGISTER_CLIENT,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found, msg='"Register client" event not found in log"')


def add_sub_as_client_to_member(self, system_code, client, wait_input=2, step='', check_request=True):
    """
    Adds a subsystem to member and as a client.
    :param self: MainController object
    :param system_code: str - subsystem code
    :param client: dict - client data
    :param wait_input: int - seconds to wait before inputs
    :param step: str - prefix to be added to logs
    :return:
    """

    # Open management requests
    self.log(step + 'CHECKING REGISTRATIONS STATUS TEST')
    self.log(step + 'Open management requests table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()
    self.wait_jquery()

    # Get the requests table and wait until it finishes loading
    requests_table = self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_TABLE_ID)
    self.wait_jquery()

    row = requests_table.find_element_by_tag_name('tbody').find_element_by_tag_name('tr')

    # Open the members table
    self.log(step + 'Open members table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()

    self.wait_jquery()

    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()

    # Open client details
    self.log(step + 'Open client details')
    members_table.get_row_by_columns(table, [client['name'], client['class'], client['code']]).click()
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()

    # Open servers tab
    self.log(step + 'Open user servers tab')
    self.wait_until_visible(type=By.XPATH, element=members_table.USED_SERVERS_TAB).click()
    self.wait_jquery()

    # Start adding the client, fill fields
    self.log(step + 'Add new client')
    self.wait_until_visible(type=By.XPATH, element=members_table.REGISTER_SECURITYSERVER_CLIENT_ADD_BTN_ID).click()
    self.log(step + 'Enter ' + client['subsystem_code'] + ' to "subsystem code" area')

    subsystem_input = self.wait_until_visible(type=By.ID,
                                              element=members_table.CLIENT_REGISTRATION_SUBSYSTEM_CODE_AREA_ID)
    self.input(subsystem_input, client['subsystem_code'])
    self.wait_jquery()

    self.wait_until_visible(type=By.ID, element=members_table.USED_SERVERS_SEARCH_BTN_ID).click()
    self.wait_jquery()

    # Try to find the subsystem in list
    rows = self.wait_until_visible(type=By.XPATH,
                                   element=members_table.SECURITY_SERVERS_TABLE_ROWS_XPATH).find_elements_by_tag_name(
        'tr')
    for row in rows:
        if str(row.find_elements_by_tag_name('td')[3].text) == system_code:
            row.click()
            break

    self.wait_until_visible(type=By.ID, element=members_table.SELECT_SECURITY_SERVER_BTN_ID).click()
    self.wait_jquery()

    self.wait_until_visible(type=By.ID, element=members_table.CLIENT_REGISTRATION_SUBMIT_BTN_ID).click()
    self.wait_jquery()

    # Reload main page
    self.driver.get(self.url)

    # Open management requests again
    self.log(step + 'Open management requests table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()

    # Get the table and wait for it to load
    requests_table = self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_TABLE_ID)
    self.wait_jquery()

    # Check if last requests have been submitted for approval
    if check_request:
        rows = requests_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0:1]
        for row in rows:
            self.is_true(keyscertificates_constants.SUBMITTED_FOR_APPROVAL_STATE in row.text, test_name,
                         step + 'CHECKING FOR "{0}" FROM THE LATEST REQUEST ROW FAILED"'.format(
                             keyscertificates_constants.SUBMITTED_FOR_APPROVAL_STATE),
                         step + 'Look "{0}" from the latest requests row: {0}'.format(
                             keyscertificates_constants.SUBMITTED_FOR_APPROVAL_STATE in row.text))


def add_subsystem_to_server_client(self, server_code, client, wait_input=3):
    """
    Adds a subsystem to server client.
    :param self: MainController object
    :param server_code: str - server code
    :param client: dict - client data
    :param wait_input: int - seconds to wait before entering text to inputs
    :return: None
    """

    # Open clients list for server
    open_servers_clients(self, server_code)

    # Start adding new client
    self.log('2.2.1-8: Add new client')
    self.wait_until_visible(type=By.ID, element=cs_security_servers.ADD_CLIENT_TO_SECURITYSERVER_BTN_ID).click()
    self.wait_jquery()

    # Search for the client
    self.log('2.2.1-8: Click on search client')
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SEARCH_BTN_ID).click()
    self.wait_jquery()
    time.sleep(wait_input)

    # Get the table and look for the client
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

    # Enter data
    self.log('2.2.1-8: Enter ' + client['subsystem_code'] + ' to subsystem code area')
    subsystem_input = self.wait_until_visible(type=By.ID, element=cs_security_servers.SUBSYSTEM_CODE_AREA_ID)

    # Clear the input and set value
    subsystem_input.click()
    subsystem_input.clear()
    subsystem_input.send_keys(client['subsystem_code'])
    self.wait_jquery()

    # Submit the form
    self.wait_until_visible(type=By.ID,
                            element=cs_security_servers.SECURITYSERVER_CLIENT_REGISTER_SUBMIT_BTN_ID).click()
    self.wait_jquery()


def approve_requests(self, use_case='', step='', cancel_confirmation=False):
    """
    Approve the management requests.
    :param self: MainController object
    :param step: str - prefix for logging
    :return: None
    """

    '''Open main page'''
    self.log(step + 'Open central server')
    self.driver.get(self.url)
    self.wait_jquery()

    '''Go to management requests'''
    self.log(step + 'Open management requests table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()
    self.wait_jquery()
    self.wait_until_visible(type=By.ID, element=MANAGEMENT_REQUEST_TABLE_ID)

    '''Find all requests that are submitted for approval'''
    try:
        td = self.by_xpath(
            members_table.get_requests_row_by_td_text(keyscertificates_constants.SUBMITTED_FOR_APPROVAL_STATE))
    except:
        td = None

    try:
        while td is not None:
            request_id = td.find_elements_by_tag_name('td')[0].text
            td.click()
            self.log(step + 'Open management request details')
            self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
            self.wait_jquery()

            self.log(use_case + '1. Approve request button is pressed')
            self.wait_until_visible(type=By.XPATH, element=members_table.APPROVE_REQUEST_BTN_XPATH).click()
            self.wait_jquery()
            self.log(use_case + '2. System prompts for confirmation')
            if cancel_confirmation:
                self.log(use_case + '3a. Approval process is canceled')
                self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
                self.wait_jquery()

                '''As the state shouldn't change after canceling, then we can approve the request'''
                self.log(step + 'Press approve button again')
                self.wait_until_visible(type=By.XPATH, element=members_table.APPROVE_REQUEST_BTN_XPATH).click()
                self.wait_jquery()
            self.log(step + '3. Confirm request approval')
            popups.confirm_dialog_click(self)
            td = self.by_xpath(members_table.get_requests_row_by_td_text(APPROVED))
            last_approved_request_id = td.find_elements_by_tag_name('td')[0].text
            self.log(step + '6. System sets the state of the request to "{0}"'.format(APPROVED))
            self.is_equal(request_id, last_approved_request_id)
            '''Find the next request waiting to be approved'''
            try:
                td = self.by_xpath(
                    members_table.get_requests_row_by_td_text(keyscertificates_constants.SUBMITTED_FOR_APPROVAL_STATE))
            except:
                td = None
    except:
        traceback.print_exc()


def check_expected_result_cs(self, ss_1_client, ss_2_client, ss_2_client_2, check_limit=6):
    """
    Checks for expected results (new clients) in central server.
    :param self: MainController object
    :param ss_1_client: dict - client data for security server 1
    :param ss_2_client: dict - client data for security server 2
    :param ss_2_client_2: dict - second client data for security server 2
    :param check_limit: int - check no more than this number of items (helps to speed up checks)
    :return: None
    """
    self.log('2.2.1-13: TEST CENTRAL SERVER RESULTS')
    self.log('2.2.1-13: Check from members table')

    # Find the client from members table and click on it
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()

    client_row = members_table.get_row_by_columns(table, [ss_1_client['name'], ss_1_client['class'],
                                                          ss_1_client['code']])
    client_row.click()

    # Open the client details and subsystem tab
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()

    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()
    self.wait_jquery()

    table = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TABLE_XPATH)
    self.wait_jquery()

    # Check if security server 1 client subsystem exists
    self.is_not_none(
        members_table.get_row_by_columns(table, [ss_1_client['subsystem_code'], self.config.get('ss1.server_name')]),
        test_name,
        '2.2.1-13.1: CHECKING IF CLIENT 1 EXISTS FAILED',
        '2.2.1-13.1: CHECKING IF CLIENT 1 EXISTS')

    table = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TABLE_XPATH)
    self.wait_jquery()

    # Check if security server 2 client subsystem exists
    self.is_not_none(
        members_table.get_row_by_columns(table, [ss_2_client['subsystem_code'], self.config.get('ss2.server_name')]),
        test_name,
        '2.2.1-13.1: CHECKING IF CLIENT 2 EXISTS FAILED',
        '2.2.1-13.1: CHECKING IF CLIENT 2 EXISTS')

    self.log('2.2.1-13: Check from members table: TEST SUCCESSFUL')

    # Go to clients
    self.reset_page()
    self.log('2.2.1-13: Check security servers > clients table for ss1')
    open_servers_clients(self, self.config.get('ss1.server_name'))
    clients_table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENTS_TABLE_ID)
    self.wait_jquery()

    # Check if clients exists
    self.is_not_none(members_table.get_row_by_columns(clients_table,
                                                      [ss_1_client['name'], ss_1_client['class'],
                                                       ss_1_client['code'],
                                                       ss_1_client['subsystem_code']]), test_name,
                     '2.2.1-13.2: CHECKING IF TS1 HAS SUB 1 FAILED',
                     '2.2.1-13.2: CHECKING IF TS1 HAS SUB 1')

    self.log('2.2.1-13.2: Check security servers > clients table for TS1: TEST SUCCESSFUL')

    self.log('2.2.1-13.3: Check security servers > clients table for TS2')

    open_servers_clients(self, self.config.get('ss2.server_name'))
    clients_table = self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENTS_TABLE_ID)
    self.wait_jquery()

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

    # Check if requests are approved.
    counter = 0
    for row in rows:
        if row.text is not u'':
            if row.find_elements_by_tag_name('td')[8].text == 'APPROVED':
                counter += 1
                row.click()
                self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
                self.wait_jquery()

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
    '''
    Checks if security server has client listed.
    :param self: MainController object
    :param client: dict - client data
    :param retry_interval: int - retry interval in seconds (data syncing may be delayed)
    :param retry_timeout: int - retry timeout in seconds
    :param registered_status: str - status that the client should have
    :return: None
    '''
    self.log('2.2.1-13: TEST SECURITY SERVER RESULTS')
    self.log('2.2.1-13: Check from members table')

    # Loop until success or timeout
    start_time = time.time()
    while True:
        try:
            if retry_interval > 0:
                self.log('2.2.1-13: Waiting {0} before checking'.format(retry_interval))
                time.sleep(retry_interval)

            self.driver.get(self.url)
            self.wait_jquery()

            # Check the client status
            status = added_client_row(self, client).find_element_by_class_name('status').get_attribute('title')
            self.log('2.2.1-13: Check if ' + ':'.join(
                [client['code'], client['subsystem_code']]) + ' is {0}: {1} ({2})'.format(registered_status,
                                                                                          status == registered_status,
                                                                                          status))
            assert status == registered_status
            # We got here - success
            break
        except:
            # Exception, check if we still have time.
            if time.time() > start_time + retry_timeout:
                # Timeout - failed
                if retry_timeout > 0:
                    self.log('2.2.1-13: Timeout while waiting')
                assert False
                raise

    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()

    # Check imports
    client_certification_2_1_3.check_import(self, client['class'], client['code'])


def added_client_row(self, client):
    '''
    Finds a client row from table.
    :param self: MainController object
    :param client: dict - client data
    :return: WebDriverElement - row associated with the client
    '''
    self.added_client_id = ' : '.join(
        [SYSTEM_TYPE, ssh_server_actions.get_server_name(self), client['class'], client['code'],
         client['subsystem_code']])
    self.log('Finding added client: '.format(self.added_client_id))
    table_rows = self.by_css(clients_table_vm.CLIENT_ROW_CSS, multiple=True)
    client_row_index = clients_table_vm.find_row_by_client(table_rows, client_id=self.added_client_id)
    if client_row_index is not None:
        return table_rows[client_row_index]
    return None


def get_expected_warning_messages(client):
    '''
    Returns a list of warning messages that may be shown for operations with a client.
    :param client: dict - client data
    :return: list[str] - list of warning messages associated with the client
    '''
    return ['Do you want to send a client registration request for the added client?\n' \
            'New subsystem \'' + client['subsystem_code'] + '\' will be submitted for registration for member \'' + \
            ' '.join([client['name'], client['class'] + ':', client['code']]) + '\'.',
            'Do you want to send a client registration request for the added client?']


def login(self, host, username, password):
    '''
    Helper function for logging in.
    :param self: MainController object
    :param host: str - hostname of the server
    :param username: str - UI username
    :param password: str - UI password
    :return: None
    '''
    self.reset_webdriver(host, username=username, password=password)
    self.wait_jquery()


def login_with_logout(self, host, username, password):
    '''
    Login but with logging out first.
    :param self: MainController object
    :param host: str - hostname of the server
    :param username: str - UI username
    :param password: str - UI password
    :return: None
    '''
    self.logout(host)
    # Log in
    login(self, host, username, password)


def open_servers_clients(self, code):
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
            if row.find_element_by_tag_name('td').text == code:
                row.click()

    # Open details
    self.log('Click on Details button')
    self.wait_until_visible(type=By.ID, element=cs_security_servers.SECURITY_SERVER_CLIENT_DETAILS_BTN_ID).click()
    self.wait_jquery()

    # Open clients tab
    self.log('Click on clients tab')
    self.wait_until_visible(type=By.XPATH, element=cs_security_servers.SERVER_CLIENT_TAB).click()
    self.wait_jquery()


def request_has_client(self, client):
    '''
    Checks if the request is associated with a client.
    :param self: MainController object
    :param client: dict - client data
    :return: bool - True if request is associated with the specified client
    '''
    return (self.by_xpath(members_table.CLIENT_REQUEST_NAME_AREA_XPATH).text == client['name']) & (self.by_xpath(
        members_table.CLIENT_REQUEST_CLASS_AREA_XPATH).text == client['class']) & (self.by_xpath(
        members_table.CLIENT_REQUEST_CODE_AREA_XPATH).text == client['code']) & (self.by_xpath(
        members_table.CLIENT_REQUEST_SUB_CODE_AREA_XPATH).text == client['subsystem_code'])


def remove_data(self, cs_host, cs_username, cs_password, sec_1_host, sec_1_username, sec_1_password,
                sec_1_ssh_host, sec_1_ssh_username, sec_1_ssh_password,
                sec_2_host, sec_2_username, sec_2_password,
                sec_2_ssh_host, sec_2_ssh_username, sec_2_ssh_password,
                cs_member, ss_1_client, ss_1_client_2, ss_2_client, ss_2_client_2,
                ca_ssh_host=None, ca_ssh_username=None, ca_ssh_password=None,
                cs_ssh_host=None, cs_ssh_username=None, cs_ssh_password=None,
                global_group=None):
    '''
    Removes the data that was created during tests.
    :param global_group: str - global group name
    :param cs_ssh_password: str - central server ssh password
    :param cs_ssh_username: str - central server ssh username
    :param cs_ssh_host: str -central server ssh host
    :param ss_1_client_2: dict- security server 1 second client data
    :param sec_2_ssh_password: str - security server 2 ssh password
    :param sec_2_ssh_username: str - security server 2 ssh username
    :param sec_2_ssh_host: str - security server 2 ssh host
    :param sec_1_ssh_password: str - security server 1 ssh password
    :param sec_1_ssh_username: str - security server 1 ssh username
    :param sec_1_ssh_host: str -security server 1 ssh host
    :param self: MainController object
    :param cs_host: str - central server hostname
    :param cs_username: str - central server UI username
    :param cs_password: str - central server UI password
    :param sec_1_host: str - security server 1 hostname
    :param sec_1_username: str - security server 1 UI username
    :param sec_1_password: str - security server 1 UI password
    :param sec_2_host: str - security server 2 hostname
    :param sec_2_username: str - security server 2 UI username
    :param sec_2_password: str - security server 2 UI password
    :param cs_member: dict - central server member data
    :param ss_1_client: dict - security server 1 new client data
    :param ss_2_client: dict - security server 2 new client data
    :param ss_2_client_2: dict - security server 2 second client data
    :param ca_ssh_host: str|None - CA ssh host, used for revoking certificates in CA
    :param ca_ssh_username: str|None - CA ssh username, used for revoking certificates in CA
    :param ca_ssh_password: str|None - CA ssh password, used for revoking certificates in CA
    :return: None
    '''
    self.log('2.2.1-del Removing test data')
    self.logout(cs_host)

    '''Delete client from ss1'''
    log_checker_ss1 = auditchecker.AuditChecker(host=sec_1_ssh_host, username=sec_1_ssh_username,
                                                password=sec_1_ssh_password)
    current_log_lines = log_checker_ss1.get_line_count()
    self.reload_webdriver(sec_1_host, sec_1_password, sec_1_password)
    safe(self, remove_client_with_cert_and_cancelling, ss_1_client,
         'Client removal with cert and deletion cancelling failed')
    expected_log_msg = DELETE_CLIENT
    self.log('MEMBER_53 8. System logs the event "{0}"'.format(expected_log_msg))
    logs_found = log_checker_ss1.check_log(expected_log_msg, from_line=current_log_lines + 1, strict=False)
    self.is_true(logs_found)

    '''Delete subsystem with global group from member'''
    self.reload_webdriver(cs_host, cs_username, cs_password)
    group = global_group
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    group_member_count = self.wait_until_visible(type=By.XPATH,
                                                 element=groups_table.GLOBAL_GROUP_TR_BY_TD_TEXT_XPATH.format(
                                                     group)).find_elements_by_tag_name('td')[2].text
    log_checker = auditchecker.AuditChecker(host=cs_ssh_host,
                                            username=cs_ssh_username,
                                            password=cs_ssh_password)
    current_log_lines = log_checker.get_line_count()
    expected_log_msg = DELETE_SUBSYSTEM
    self.reload_webdriver(cs_host, cs_username, cs_password)
    safe(self, remove_client_subsystem_with_canceling, ss_1_client,
         'Removing client {0} with subsystem'.format(ss_1_client))
    self.log('MEMBER_14 6. System logs the event {0}'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    self.is_true(logs_found)
    popups.close_all_open_dialogs(self)
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.GLOBAL_GROUPS_CSS).click()
    self.log('MEMBER_14 4. Subsystem, which was deleted is removed from global group')
    group_member_count_after = self.wait_until_visible(type=By.XPATH,
                                                       element=groups_table.GLOBAL_GROUP_TR_BY_TD_TEXT_XPATH.format(
                                                           group)).find_elements_by_tag_name('td')[2].text
    self.is_true(group_member_count > group_member_count_after)

    self.log('Removing members from central server')
    safe(self, remove_member, cs_member, 'Removing member {0} failed'.format(cs_member))
    safe(self, remove_member, ss_1_client_2, 'Removing member {0} failed'.format(ss_1_client_2))

    '''Reload the CS homepage'''
    self.reset_webdriver(cs_host, cs_username, cs_password)
    '''Revoke waiting management requests'''
    try:
        self.log('2.2.1-del revoking management requests')
        revoke_requests(self)
    except:
        self.log('2.2.1-del revoking requests failed')
        traceback.print_exc()

    '''Remove client 2 from ss1'''
    '''Go to security server 1'''
    self.log('2.2.1-del removing certificate from security server 1')
    login(self, sec_1_host, sec_1_username, sec_1_password)
    '''Try to remove client with canceling deletion and confirming certificate removal popup from ss1'''
    self.driver.get(self.url)
    safe(self, remove_client_keep_cert, ss_1_client_2, 'Removing client from security server 1 failed')
    '''Remove client 2 certificate from ss1'''
    safe(self, remove_certificate, ss_1_client_2, 'Removing certificate from security server 1 failed')

    # Connect to CA over SSH
    try:
        ca_ssh_client = ssh_client.SSHClient(host=ca_ssh_host, username=ca_ssh_username, password=ca_ssh_password)
    except:
        ca_ssh_client = None

    '''Revoke the certificates in CA'''
    self.log('Revoking security server 1 added client certificates in CA')
    self.log('Open "Keys and Certificates tab"')
    try:
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
        self.wait_jquery()

        # Wait for the generated key row to appear
        self.wait_until_visible(type=By.XPATH,
                                element=keyscertificates_constants.get_generated_key_row_xpath(ss_1_client['code'],
                                                                                               ss_1_client['class']))
        certs_to_revoke = get_certificates_to_revoke(self, ss_1_client)
        if ssh_client is not None:
            self.log('Revoking certificates in CA')
            client_certification_2_1_3.revoke_certs(ca_ssh_client, certs_to_revoke)
    except:
        self.log('Failed to revoke security server 1 added client certificates')
        traceback.print_exc()

    self.log('Check if log contains delete client event')

    '''Remove client1 key from ss1'''
    try:
        remove_key_and_revoke_certificates(self, ss_1_client, ca_ssh_client)
    except:
        self.log('2.2.1-del Removing certificate from security server 1 failed')
        traceback.print_exc()

    self.log('2.2.1-del removing client from security server 1')

    '''Logchecker for security server 2'''
    log_checker = auditchecker.AuditChecker(host=sec_2_ssh_host, username=sec_2_ssh_username,
                                            password=sec_2_ssh_password)
    current_log_lines = log_checker.get_line_count()
    '''Go to security server 2'''
    self.log('2.2.1-del removing certificate from security server 2')
    login(self, sec_2_host, sec_2_username, sec_2_password)
    '''Try to remove certificate'''
    try:
        remove_key_and_revoke_certificates(self, ss_2_client, ca_ssh_client)
    except:
        self.log('2.2.1-del Removing certificate from security server 2 failed')
        traceback.print_exc()

    if ca_ssh_client is not None:
        ca_ssh_client.close()

    self.driver.get(self.url)
    '''Try to remove client from security server 2'''
    safe(self, remove_client, ss_2_client, 'Removing client {0} failed'.format(ss_2_client))
    '''Check if log contains Delete client event'''
    log_errors = []
    expected_log_msg = DELETE_CLIENT
    self.log('MEMBER_53 8. System logs the event {0}'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    if not logs_found:
        log_error = 'SS2 client 1 delete: some log entries were missing. Expected: "{0}", found: "{1}"'.format(
            log_constants.DELETE_CLIENT,
            log_checker.found_lines)
        self.log(log_error)
        log_errors.append(log_error)
    current_log_lines = log_checker.get_line_count()

    self.driver.get(self.url)
    '''Try to remove second client from security server 2'''
    safe(self, remove_client, ss_2_client_2, 'Removing client {0} failed'.format(ss_2_client_2))
    expected_log_msg = DELETE_CLIENT
    self.log('MEMBER_53 8. System logs the event {0}'.format(expected_log_msg))
    logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
    if not logs_found:
        log_error = 'SS2 client 2 delete: some log entries were missing. Expected: "{0}", found: "{1}"'.format(
            log_constants.DELETE_CLIENT,
            log_checker.found_lines)
        self.log(log_error)
        log_errors.append(log_error)
    login(self, cs_host, cs_username, cs_password)
    safe(self, remove_client_subsystem, ss_2_client_2,
         '2.2.1-del Removing security server 1 client subsystem failed')
    if log_errors:
        self.is_true(False, msg='2.2.1-del Log error count {0}, errors: {1}'.format(len(log_errors), log_errors))


def remove_member(self, member):
    '''
    Removes a member.
    :param self: MainController object
    :param member: dict - member data
    :return: None
    '''

    # Get the members table
    self.log('Wait for members table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()
    self.wait_jquery()
    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()

    # Get the member row
    self.log('Get row by row values')
    row = members_table.get_row_by_columns(table, [member['name'], member['class'], member['code']])
    if row is None:
        # Nothing found - error
        assert False, '2.2.1-del: member not found'

    # Click on the member
    row.click()

    # Open details
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()

    # Click delete button
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.wait_jquery()

    # Confirm the deletion
    self.log('Confirm deleting member')
    popups.confirm_dialog_click(self)


def remove_client_with_cert_and_cancelling(self, client):
    """
    Wrapper function for remove_client(), removes client with certificate and cancels deletion before confirming
    :param self: Maincontroller object
    :param client: dict - client data
    :return:
    """
    remove_client(self, client, delete_cert=True, cancel_deletion=True)


def remove_client_keep_cert(self, client):
    """
    Wrapper function for remove_client(), removes client without certificate
    :param self: Maincontroller object
    :param client: dict - client data
    :return:
    """
    remove_client(self, client, cancel_deletion=True, deny_cert_deletion=True)


def remove_client(self, client, delete_cert=False, cancel_deletion=False, deny_cert_deletion=False):
    """
    Removes a client.
    :param cancel_deletion: bool - cancel delete confirmation popup before confirming
    :param delete_cert: bool - confirm certificate deletion
    :param self: MainController object
    :param client: dict - client data
    :return: None
    """

    '''Open security servers tab'''
    self.log('Open "Security servers tab"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.CLIENTS_BTN_CSS).click()
    self.wait_jquery()

    '''Edit client details'''
    self.log('Opening client details')
    added_client_row(self, client).find_element_by_css_selector(clients_table_vm.DETAILS_TAB_CSS).click()
    self.wait_jquery()

    '''Unregister the client'''
    self.log('Unregister Client')
    try:
        self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
        self.wait_jquery()
        '''Confirm unregistering'''
        popups.confirm_dialog_click(self)
        try:
            self.log('MEMBER_53 1. Client deletion process is started')
            self.wait_jquery()
            self.log('MEMBER_53 2. System prompts for confirmation')
            if cancel_deletion:
                self.log('MEMBER_53 3.a Client deletion is canceled')
                self.by_xpath(popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
                self.by_id(popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
                self.wait_jquery()
            self.log('MEMBER_53 3. Client deletion is confirmed')
            popups.confirm_dialog_click(self)
            self.wait_jquery()
            '''Certificate deletion'''
            if delete_cert:
                self.log('MEMBER_53 4. System verifies that the signature certificates associated with the client '
                         'have no other users and asks for confirmation to delete the client\'s signature certificates')
                self.wait_until_visible(type=By.XPATH, element=popups.YESNO_POPUP_XPATH)
                self.log('MEMBER_53 5. Certificate deletion is confirmed')
                self.by_xpath(popups.YESNO_POPUP_YES_BTN_XPATH).click()
                self.log('Open "Keys and Certificates tab"')
                self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
                self.wait_jquery()
                '''Get the other next tr from client key'''
                expected_next_tr = self.by_xpath(keyscertificates_constants.get_generated_key_row_cert_xpath(
                    client['code'],
                    client['class']))
                '''Check if tr has not cert-active class,
                which means that the key has no cert and deletion was successful'''
                self.is_true('cert-active' not in expected_next_tr.get_attribute('class').split(' '))
            elif deny_cert_deletion:
                self.log('MEMBER_53 5a. Deny certificate deletion')
                self.wait_until_visible(type=By.XPATH, element=popups.YESNO_POPUP_XPATH)
                self.by_xpath(popups.YESNO_POPUP_NO_BTN_XPATH).click()
        except:
            '''Didn't get another dialog. This is not a problem.'''
            pass
    except:
        '''Unregister failed, client can probably be deleted'''
        self.log('Not unregistering')
        try:
            '''Try to delete the client'''
            self.log('Deleting client')
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
            self.wait_jquery()
            '''Confirm deletion'''
            popups.confirm_dialog_click(self)
            if delete_cert:
                '''Wait certificate deletion confirmation popup'''
                self.wait_until_visible(type=By.XPATH, element=popups.YESNO_POPUP_XPATH)
                '''Confirm certificate deletion'''
                self.by_xpath(popups.YESNO_POPUP_YES_BTN_XPATH).click()
                self.log('Open "Keys and Certificates tab"')
                self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
                self.wait_jquery()

                expected_next_tr = self.by_xpath(type=By.XPATH,
                                                 element=keyscertificates_constants.get_generated_key_row_cert_xpath(
                                                     client['code'],
                                                     client['class']))
                self.is_true(expected_next_tr.get_attribute('class').contains('key'))
        except:
            pass

    self.log('CLIENT DELETED')
    self.is_none(added_client_row(self, client))


def remove_client_subsystem_with_canceling(self, client):
    remove_client_subsystem(self, client, try_cancel=True)


def remove_client_subsystem(self, client, try_cancel=False):
    '''
    MEMBER_14 Delete a X-Road Member's Subsystem
    :param self: MainController object
    :param client: dict - client data
    :return: None
    '''

    # Open the members table
    self.log('Open members table')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MEMBERS_CSS).click()
    self.wait_jquery()

    table = self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_TABLE_ID)
    self.wait_jquery()

    # Open client details
    self.log('Open client details')
    members_table.get_row_by_columns(table, [client['name'], client['class'], client['code']]).click()
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.wait_jquery()

    # Open subsystems tab
    self.log('Open subsystems tab')
    self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TAB).click()
    self.wait_jquery()

    self.wait_jquery()

    subsys_row = self.wait_until_visible(type=By.XPATH, element=members_table.SUBSYSTEM_TR_BY_CODE_XPATH.format(
        client['subsystem_code']))
    subsys_row.click()

    # Click "Delete"
    self.log('MEMBER_14 1. Subsystem delete button is clicked')
    self.wait_until_visible(type=By.XPATH, element=members_table.DELETE_SUBSYSTEM_BTN_ID).click()
    self.log('MEMBER_14 2. System prompts for confirmation')
    if try_cancel:
        self.log('MEMBER_14 3a. Subsystem deletion is canceled')
        self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_until_visible(type=By.XPATH, element=members_table.DELETE_SUBSYSTEM_BTN_ID).click()

    self.log('MEMBER_14 3. Subsystem deletion is confirmed')
    popups.confirm_dialog_click(self)
    self.wait_jquery()


def remove_certificate(self, client):
    '''
    Removes a certificate from a client.
    :param self: MainController object
    :param client: dict - client data
    :return: None
    '''
    self.log('REMOVE CERTIFICATE')
    self.log('Open "Keys and Certificates tab"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()

    '''Click the key row'''
    self.log('Click on generated key row')
    self.wait_until_visible(type=By.XPATH,
                            element=keyscertificates_constants.get_generated_key_row_xpath(client['code'],
                                                                                           client[
                                                                                               'class'])).click()
    self.wait_jquery()

    '''Click "Delete"'''
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()
    self.wait_jquery()

    '''Confirm the removal'''
    popups.confirm_dialog_click(self)

    '''Check if table doesn't contain deleted key'''
    try:
        self.by_xpath(keyscertificates_constants.get_generated_key_row_xpath(client['code'], client['class']))
        assert False
    except:
        pass


def get_certificates_to_revoke(self, client):
    '''
    Gets a list of the client's certificates that need to be revoked.
    :param self: MainController object
    :param client: dict - client data
    :return: [str] - list of certificate filenames to revoke
    '''
    # Initialize the list of certificates to revoke. Because we are deleting the key, we need to revoke all certificates
    # under it.
    certs_to_revoke = []

    # Try to get the certificates under the generated keys
    key_num = 1
    newcerts_base = './newcerts'
    while True:
        try:
            key_friendly_name_xpath = keyscertificates_constants.get_generated_key_row_active_cert_friendly_name_xpath(
                client['code'], client['class'], key_num)
            key_name_element = self.by_xpath(key_friendly_name_xpath)
            element_text = key_name_element.text.strip()
            # Split the element by space and get the last part of it as this is the key id as a decimal
            cert_id = int(element_text.rsplit(' ', 1)[-1])
            cert_hex = '{0:02x}'.format(cert_id).upper()
            # Key filenames are of even length (zero-padded) so we'll generate one like that
            if len(cert_hex) % 2 == 1:
                cert_filename = '{0}/0{1}.pem'.format(newcerts_base, cert_hex)
            else:
                cert_filename = '{0}/{1}.pem'.format(newcerts_base, cert_hex)
            certs_to_revoke.append(cert_filename)
        except:
            # Exit loop if element not found (= no certificates listed)
            break
        key_num += 1

    return certs_to_revoke


def remove_key_and_revoke_certificates(self, client, ssh_client=None):
    '''
    Removes a certificate from a client and revokes the associated certificate in the CA.
    :param self: MainController object
    :param client: dict - client data
    :param ssh_client: SSHClient object connected to CA | None to disable
    :return: None
    '''
    self.log('REMOVE AND REVOKE CERTIFICATE')
    self.log('Open "Keys and Certificates tab"')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.KEYSANDCERTIFICATES_BTN_CSS).click()
    self.wait_jquery()

    # Wait for the generated key row to appear
    generated_key_row = self.wait_until_visible(type=By.XPATH,
                                                element=keyscertificates_constants.get_generated_key_row_xpath(
                                                    client['code'],
                                                    client['class']))
    certs_to_revoke = get_certificates_to_revoke(self, client)

    print 'certs to revoke', certs_to_revoke

    # Click the key row
    self.log('Click on generated key row')
    generated_key_row.click()
    self.wait_jquery()

    # Click "Delete"
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()
    self.wait_jquery()

    # Confirm the removal
    popups.confirm_dialog_click(self)

    # Check if table doesn't contain deleted key
    try:
        self.by_xpath(keyscertificates_constants.get_generated_key_row_xpath(client['code'], client['class']))
        assert False
    except:
        pass

    if ssh_client is not None:
        self.log('Revoking certificates in CA')
        client_certification_2_1_3.revoke_certs(ssh_client, certs_to_revoke)


def revoke_requests(self, try_cancel=False, auth=False, log_checker=None):
    '''
    Revoke management requests that are in waiting state.
    :param try_cancel:  bool|False - cancels revoke before confirming
    :param auth: bool|False - request type auth
    :param log_checker: obj|None - auditchecker instance
    :param self: MainController object
    :return: None
    '''
    current_log_lines = None
    if log_checker is not None:
        current_log_lines = log_checker.get_line_count()
    '''Client/cert successful revoke message'''
    success_message = messages.AUTH_REQUEST_REVOKE_SUCCESSFUL_NOTICE if auth \
        else messages.REQUEST_REVOKE_SUCCESSFUL_NOTICE
    '''Client/cert delete request selector'''
    deletion_request_selector = cs_security_servers.MANAGEMENT_REQUESTS_CERT_DELETION_XPATH if auth \
        else cs_security_servers.MANAGEMENT_REQUESTS_CLIENT_DELETION_XPATH
    '''Client/cert details dialog selector'''
    details_dialog_selector = cs_security_servers.CERT_DELETION_REQUEST_DETAILS_DIALOG_ID if auth \
        else cs_security_servers.CLIENT_DELETION_REQUEST_DETAILS_DIALOG_ID
    '''Client/cert details dialog comment selector'''
    delete_request_comment = cs_security_servers.REVOKE_CERT_DELETE_REQUEST_COMMENT if auth \
        else cs_security_servers.REVOKE_CLIENT_DELETE_REQUEST_COMMENT
    '''Client/cert registration request selector'''
    reg_request_selector = cs_security_servers.REVOKE_CERT_MANAGEMENT_REQUEST_BTN_XPATH if auth \
        else cs_security_servers.REVOKE_CLIENT_MANAGEMENT_REQUEST_BTN_XPATH
    self.log('MEMBER_39 Revoke a Registration Request')
    self.log('Open management requests tab')
    self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar.MANAGEMENT_REQUESTS_CSS).click()
    self.wait_jquery()

    self.log('Find request with waiting status')
    td = self.wait_until_visible(type=By.XPATH, element=members_table.get_requests_row_by_td_text(
        keyscertificates_constants.WAITING_STATE))
    '''Waiting request id'''
    request_id = td.find_elements_by_tag_name('td')[0].text
    self.log('Click on waiting request')
    td.click()
    self.log('Open request details')
    self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
    self.wait_jquery()

    self.log('MEMBER_39 1. Click on revoke button')
    self.wait_until_visible(type=By.XPATH,
                            element=reg_request_selector).click()
    self.wait_jquery()

    self.log('MEMBER_39 2. System prompts for confirmation')
    if try_cancel:
        self.log('MEMBER_39 3a request revoking is canceled')
        self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
        self.wait_jquery()
        self.log('Click on revoke button again')
        self.wait_until_visible(type=By.XPATH,
                                element=reg_request_selector).click()
        self.wait_jquery()

    self.log('MEMBER_39 3. Confirm request revocation')
    popups.confirm_dialog_click(self)
    self.wait_jquery()
    expected_success_msg = success_message.format(request_id)
    self.log('MEMBER_39 6. System displays the message "{0}"'.format(expected_success_msg))
    notice_msg = messages.get_notice_message(self)
    self.is_equal(expected_success_msg, notice_msg)
    self.log('MEMBER_39 5. System sets the state of registration request to revoked')
    first_revoked_request_id = self.by_xpath(members_table.get_requests_row_by_td_text(
        keyscertificates_constants.REVOKED_STATE)).find_element_by_tag_name('td').text
    self.is_equal(request_id, first_revoked_request_id)
    self.log('MEMBER_39 5. System creates a deletion request with revoked request id')
    self.by_xpath(deletion_request_selector).click()
    self.wait_until_visible(type=By.ID, element=members_table.MANAGEMENT_REQUEST_DETAILS_BTN_ID).click()
    '''Request details dialog element'''
    client_deletion_details_dialog = self.wait_until_visible(type=By.ID, element=details_dialog_selector)
    '''Request details comment field text'''
    comment = client_deletion_details_dialog.find_element_by_class_name(
        cs_security_servers.CLIENT_DELETION_REQUEST_DETAILS_DIALOG_COMMENTS_INPUT_CLASS).text
    self.is_equal(comment, delete_request_comment.format(request_id))
    if current_log_lines is not None:
        expected_log_msg = REVOKE_AUTH_REGISTRATION_REQUEST
        logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
        self.is_true(logs_found)


def safe(self, func, member, message):
    """
    A try-except wrapper that allows executing functions without crashing. Used for removing data that
     might not be there.
    :param self: MainController object
    :param func: function to execute
    :param member: member to use as a parameter to function
    :param message: str - message to display in case of an error
    :return: bool - True if no error; False otherwise
    """
    try:
        func(self, member)
        return True
    except Exception, e:
        if self.debug:
            self.log('Got an exception in safe(): {0}'.format(message))
        traceback.print_exc()
        # raise AssertionError
