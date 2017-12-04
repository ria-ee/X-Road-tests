import traceback

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from helpers import auditchecker
from tests.xroad_add_to_acl_218.add_to_acl import select_subjects_to_acl
from view_models import popups as popups, clients_table_vm as clients_table_vm, log_constants
from view_models.clients_table_vm import select_subjects_from_table, SERVICE_CLIENT_NAME_XPATH, \
    SERVICE_CLIENT_IDENTIFIER_XPATH
from view_models.log_constants import ADD_ACCESS_RIGHTS_TO_SUBJECT, REMOVE_ACCESS_RIGHTS_FROM_SUBJECT
from view_models.popups import CLIENT_DETAILS_POPUP_ACL_SUBJECTS_OPEN_CLIENTS_SERVICES_ID, \
    CLIENT_DETAILS_POPUP_ACL_SUBJECTS_ADD_BTN_ID

test_name = 'ADD_TO_ACL_CLIENT'


def select_rows(self, rows_to_select, table):
    """
    Selects rows_to_select given rows or all rows if variable is 0
    :param self: MainController class object
    :param rows_to_select: List of rows or 0 (List(integer) | 0)
    :param table: WebElement Table
    :return: selected rows (distinct text from row) (List(String))
    """
    if rows_to_select == 0:
        selected_rows = popups.select_rows_from_services_table(table=table,
                                                               rows_to_select=0)
        self.log('Clicking on "add all to ACL" button')
        self.wait_until_visible(type=By.ID,
                                element=popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ADD_ALL_TO_ACL_BTN_ID).click()
    else:
        self.log('Selecting rows')
        selected_rows = popups.select_rows_from_services_table(table=table,
                                                               rows_to_select=rows_to_select)
        self.log('Clicking on "add selected to ACL" button')
        self.by_id(popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ADD_SELECTED_TO_ACL_BTN_ID).click()
    return selected_rows


def rows_are_unselectable(table, rows):
    """
    If every element in rows are unselectable in table, returns TRUE. If some element is selectable, returns FALSE
    :param table: Table to check the condition(WebElement)
    :param rows: List of rows, unselectable row td text (List(String))
    :return: True if rows are unselectable otherwise false (Boolean)
    """
    try:
        for row in rows:
            table.find_element(By.XPATH,
                               '//tr[contains(@class, "unselectable" )]//*[text() = "' + row + '"]')
    except NoSuchElementException:
        return False
    return True


def test_empty_client(ss_ssh_host=None, ss_ssh_user=None, ss_ssh_pass=None, rows_to_select=None, remove_data=True,
                      client_name=None, view_service_clients=False):
    def test_case(self):
        # Add access to new client
        self.log('*** SERVICE_03 Add a Service Client to a Security Server Client / empty client')

        # UC SERVICE_04 1. Select to add access rights for a service client
        self.log('SERVICE_03 1. Select to add a service client for a security server client')
        if ss_ssh_host is not None:
            log_checker = auditchecker.AuditChecker(host=ss_ssh_host, username=ss_ssh_user,
                                                    password=ss_ssh_pass)
            current_log_lines = log_checker.get_line_count()
        try:
            self.log('Choose client')
            clients_table_vm.open_acl_subjects_popup(self, client_name)
            popups.open_client_search_list_from_acl_subjects_popup(self)

            # UC SERVICE_03 2. Select the subject and the services
            self.log('SERVICE_03 2. Select the subject and the services')
            selected_id = select_subjects_to_acl(self, [5])

            # Add access to new client
            self.wait_until_visible(type=By.ID, element=popups.ACL_SUBJECTS_SEARCH_POPUP_NEXT_BTN_ID).click()

            self.log('Waiting for services table')
            table = self.wait_until_visible(type=By.ID,
                                            element=popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ALL_SERVICES_TABLE_ID)

            selected_rows = select_rows(self=self, rows_to_select=rows_to_select, table=table)

            # UC SERVICE_03 3. System saves the access right records
            self.log('SERVICE_03 3. System saves the access right records')

            self.wait_jquery()
            if ss_ssh_host is not None:
                expected_log_msg = ADD_ACCESS_RIGHTS_TO_SUBJECT
                # UC SERVICE_03 4. System logs the event
                self.log('SERVICE_03 4. System logs the event "{0}"'.format(expected_log_msg))
                logs_found = log_checker.check_log(expected_log_msg, from_line=current_log_lines + 1)
                self.is_true(logs_found)

            # UC SERVICE_03. Check if correct rows are displayed
            self.log('Getting opened services for client')
            open_rows = popups.open_services_table_rows(self)
            self.log('Testing if rows are correct')
            self.is_equal(selected_rows, open_rows, test_name,
                          'SERVICE_03 check if correct rows are displayed - failed',
                          'SERVICE_03 check if correct rows are displayed')
        except Exception:
            self.log('SERVICE_03 ERROR: {0}'.format(traceback.format_exc()))

        if view_service_clients:
            self.log('Close access rights popup')
            popups.close_all_open_dialogs(self, limit=1)
            self.wait_jquery()
            self.log('SERVICE_01 1. Viewing service clients of a security server client')
            self.log('SERVICE_01 2. System displays the name of the X-Road member')
            self.is_equal(client_name, self.wait_until_visible(type=By.XPATH, element=SERVICE_CLIENT_NAME_XPATH).text)
            self.log('SERVICE_01 2. System displays the X-Road identifier')
            self.is_equal(selected_id[0],
                          self.wait_until_visible(type=By.XPATH, element=SERVICE_CLIENT_IDENTIFIER_XPATH).text)
            self.log('SERVICE_01 2. "Add a client" button is visible')
            self.is_not_none(self.by_id(CLIENT_DETAILS_POPUP_ACL_SUBJECTS_ADD_BTN_ID))
            self.log('SERVICE_01 2. "Access rights" button is visible')
            self.is_not_none(self.by_id(CLIENT_DETAILS_POPUP_ACL_SUBJECTS_OPEN_CLIENTS_SERVICES_ID))
        if remove_data:
            if ss_ssh_host is not None:
                remove_added_data(self, log_checker, client_name, selected_id=selected_id)
            else:
                remove_added_data(self, client_name=client_name, selected_id=selected_id)

    return test_case


def test_existing_client(ss_ssh_host=None, ss_ssh_user=None, ss_ssh_pass=None, rows_to_select=None, remove_data=True,
                         client_name=None):
    def test_case(self):
        selected_id = None
        try:
            # Add access to new client
            self.log('*** SERVICE_03 Add a Service Client to a Security Server Client / existing client')

            # UC SERVICE_04 1. Select to add access rights for a service client
            self.log('SERVICE_03 1. Select to add a service client for a security server client')

            if ss_ssh_host is not None:
                log_checker = auditchecker.AuditChecker(host=ss_ssh_host, username=ss_ssh_user,
                                                        password=ss_ssh_pass)
                current_log_lines = log_checker.get_line_count()
            # From previously added in test_main, we need a client which already have a service

            clients_table_vm.open_acl_subjects_popup(self, client_name)
            popups.open_client_search_list_from_acl_subjects_popup(self)

            # UC SERVICE_03 2. Select the subject and the services
            self.log('SERVICE_03 2. Select the subject and the services')
            selected_id = select_subjects_to_acl(self, [5])

            # Add access to new client
            self.log('Adding access to new client')
            self.wait_until_visible(type=By.ID, element=popups.ACL_SUBJECTS_SEARCH_POPUP_NEXT_BTN_ID).click()
            self.wait_jquery()

            table = self.wait_until_visible(type=By.ID,
                                            element=popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ALL_SERVICES_TABLE_ID)

            select_rows(self=self, rows_to_select=rows_to_select[0], table=table)

            # UC SERVICE_03 3. System saves the access right records
            self.log('SERVICE_03 3. System saves the access right records')

            self.log('Logging out to clear out')
            # Logout, login. no need for logout functionality testing at this point so we can logout from url
            self.driver.get(self.url + 'login/logout')
            self.login(self.username, self.password)

            # Test existing client
            self.log('Test existing client')

            # Open clients
            clients_table_vm.open_acl_subjects_popup(self, client_name)

            # Wait for jquery table loading and until table is visible
            self.wait_jquery()
            clients_with_services_table = self.wait_until_visible(type=By.ID,
                                                                  element=popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_TABLE_ID)

            all_clients_table = popups.open_client_search_list_from_acl_subjects_popup(self)
            # Checking if you can not add already added client
            self.log('Selecting already selected client to add services')
            self.is_true(rows_are_unselectable(all_clients_table, selected_id), test_name,
                         'SERVICE_03 CHECK IF CORRECT ROWS ARE UNSELECTABLE',
                         'SERVICE_03 CHECK IF CORRECT ROWS ARE UNSELECTABLE FAILED')
            # Closing clients dialog
            self.wait_until_visible(type=By.XPATH, element=popups.ACL_SUBJECTS_SEARCH_POPUP_CLOSE_BTN_XPATH).click()

            self.log('SERVICE_03 1. Selecting previously added client')
            # Select previously added client
            select_subjects_from_table(self, subjects_table=clients_with_services_table, subjects=selected_id)

            # UC SERVICE_03 2. Select the subject and services.
            self.log('SERVICE_03 2. Select the subject and services.')

            self.log('Opening access rights of the selected client')
            # Open client access rights
            self.by_id(popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_OPEN_CLIENTS_SERVICES_ID).click()
            self.log('Reading already opened services')
            # load already open services into list
            already_opened_services = popups.open_services_table_rows(self)

            # Add services
            self.log('Add services')

            self.log('Clicking on "Add services" button')
            # Click on add services BTN
            self.wait_until_visible(type=By.ID,
                                    element=popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ADD_SERVICES_BTN_ID).click()

            self.wait_jquery()
            clients_with_services_table = self.wait_until_visible(type=By.ID,
                                                                  element=popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ALL_SERVICES_TABLE_ID)

            self.is_true(rows_are_unselectable(table=clients_with_services_table, rows=already_opened_services),
                         test_name,
                         'SERVICE_03 check if correct rows are unselectable - failed',
                         'SERVICE_03 check if correct rows are unselectable')

            # UC SERVICE_03 Select services
            self.log('SERVICE_03 Select services')

            self.log('Selecting services which should be not already assigned')

            if rows_to_select[1] == [0]:
                selected_services = select_rows(self=self, table=clients_with_services_table, rows_to_select=0)
            else:
                selected_services = select_rows(self=self, table=clients_with_services_table,
                                                rows_to_select=rows_to_select[1])

            # UC SERVICE_03 3. System saves the access right records
            self.log('SERVICE_03 3. System saves the access right records')

            if ss_ssh_host is not None:
                self.wait_jquery()
                logs_found = log_checker.check_log(log_constants.ADD_ACCESS_RIGHTS_TO_SUBJECT,
                                                   from_line=current_log_lines + 1)
                self.is_true(logs_found,
                             msg='SERVICE_03 4. Some log entries were missing. Expected: "{0}", found: "{1}"'.format(
                                 log_constants.ADD_ACCESS_RIGHTS_TO_SUBJECT,
                                 log_checker.found_lines))

            self.log('SERVICE_03 3. Reading all opened services of the client')
            # Load all opened services to list
            all_opened_services = popups.open_services_table_rows(self)

            # Remove services that were there before
            recently_added_services = list(set(all_opened_services) - set(already_opened_services))

            # UC SERVICE_03 verify added access
            self.log('SERVICE_03 verify added access')

            self.is_equal(set(selected_services), set(recently_added_services),
                          test_name,
                          'SERVICE_03 verify added access - failed',
                          'SERVICE_03 verify added access')
        except Exception:
            self.log('SERVICE_03 ERROR: {0}'.format(traceback.format_exc()))

        if remove_data:
            remove_added_data(self, client_name=client_name, selected_id=selected_id)

    return test_case


def remove_added_data(self, log_checker=None, client_name=None, selected_id=None):
    """
    SERVICE_05(1-4) removes added data specific to these tests
    :param log_checker: Auditchecker instance for log checking
    :param self: MainController class object
    """
    self.log('*** SERVICE_05 Remove Access Rights from a Service Client')
    # Logout, login. no need for logout functionality testing at this point so we can logout from url
    self.driver.get(self.url + 'login/logout')
    self.login(self.username, self.password)

    # UC SERVICE_05 1. Select to remove service access rights from a service client
    self.log('SERVICE_05 1. Select to remove service access rights from a service client')

    # Open clients
    clients_table_vm.open_acl_subjects_popup(self, client_name)

    self.wait_jquery()
    clients_with_services_table = self.wait_until_visible(type=By.ID,
                                                          element=popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_TABLE_ID)

    if log_checker is not None:
        current_log_lines = log_checker.get_line_count()
    # Select previously added client
    self.log('Selecting previously added client')
    select_subjects_from_table(self, subjects_table=clients_with_services_table, subjects=selected_id)
    # Open client access rights
    self.log('Opening access rights of the selected client')
    self.by_id(popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_OPEN_CLIENTS_SERVICES_ID).click()
    # Wait for services table to be visible possible ajax call
    self.wait_jquery()

    # UC SERVICE_05 2, 3. Select the services and remove access to them.
    self.log('SERVICE_05 2, 3. Select the services and remove access to them.')
    self.by_id(popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_REMOVE_ALL_SERVICES_BTN_ID).click()
    popups.confirm_dialog_click(self)
    self.wait_jquery()

    if log_checker is not None:
        expected_log_msg = REMOVE_ACCESS_RIGHTS_FROM_SUBJECT
        self.log('SERVICE_05 4. System logs the event "{0}"'.format(expected_log_msg))
        logs_found = log_checker.check_log(expected_log_msg,
                                           from_line=current_log_lines + 1)
        self.is_true(logs_found)

    self.driver.get(self.url + 'login/logout')
