import traceback

import sys
from selenium.common.exceptions import NoSuchElementException

from view_models import popups as popups, clients_table_vm as clients_table_vm
from selenium.webdriver.common.by import By
from tests.xroad_add_to_acl_218.add_to_acl_2_1_8 import select_subjects_to_acl
from view_models.clients_table_vm import select_subjects_from_table

test_name = 'ADD_TO_ACL_CLIENT'


def select_rows(self, rows_to_select, table):
    """
    Checks if rows to select is 0.
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
        # Select services from services table
        selected_rows = popups.select_rows_from_services_table(table=table,
                                                               rows_to_select=rows_to_select)
        self.log('Clicking on "add selected to ACL" button')
        # click on 'add selected to ACL' button
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


def test_empty_client(rows_to_select, remove_data=True):
    def test_case(self):
        # TEST PLAN 2.1.9.1 add access to new client
        self.log('*** 2.1.9 / XT-463')
        self.log('2.1.9.1 add access to new client')
        try:
            # TEST PLAN 2.1.9.1-1 choose client
            self.log('2.1.9.1-1 choose client')
            clients_table_vm.open_acl_subjects_popup(self)
            popups.open_client_search_list_from_acl_subjects_popup(self)

            # TEST PLAN 2.1.9.1-2 select client to add services
            self.log('2.1.9.1-2 Selecting client to add services')
            self.selected_id = select_subjects_to_acl(self, [5])

            # TEST PLAN 2.1.9.1-3 add access to new client
            self.log('2.1.9.1-3 adding access to new client')
            self.wait_until_visible(type=By.ID, element=popups.ACL_SUBJECTS_SEARCH_POPUP_NEXT_BTN_ID).click()

            self.log('Waiting for services table')
            table = self.wait_until_visible(type=By.ID,
                                            element=popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ALL_SERVICES_TABLE_ID)

            selected_rows = select_rows(self=self, rows_to_select=rows_to_select, table=table)

            # TEST PLAN 2.1.9.1-4 check if correct rows are displayed
            self.log('Getting opened services for client')
            open_rows = popups.open_services_table_rows(self)
            self.log('Testing if rows are correct')
            self.is_equal(selected_rows, open_rows, test_name, '2.1.9.1-4 check if correct rows are displayed - failed',
                          '2.1.9.1-4 check if correct rows are displayed')
        except Exception:
            self.log('2.1.9.1 ERROR: {0}'.format(traceback.format_exc()))

        if remove_data:
            remove_added_data(self)

    return test_case


def test_existing_client(rows_to_select, remove_data=True):
    def test_case(self):
        try:
            # TEST PLAN 2.1.9.2 add access to existing client
            self.log('*** 2.1.9 / XT-463')

            self.log('2.1.9.2 Adding a service to existing client')

            # From previously added in test_main, we need a client which already have a service
            self.add_1_service(rows_to_select=rows_to_select[0], remove_data=False)

            self.log('Logging out to clear out')
            # Logout, login. no need for logout functionality testing at this point so we can logout from url
            self.driver.get(self.url + 'login/logout')
            self.login()

            # TEST PLAN 2.1.9.2-1 choose existing client
            self.log('2.1.9.2-1 choose existing client')

            # Open clients
            clients_table_vm.open_acl_subjects_popup(self)

            # Wait for jquery table loading and until table is visible
            self.wait_jquery()
            clients_with_services_table = self.wait_until_visible(type=By.ID,
                                                                  element=popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_TABLE_ID)

            all_clients_table = popups.open_client_search_list_from_acl_subjects_popup(self)
            # Checking if you can not add already added client
            self.log('Selecting already selected client to add services')
            self.is_true(rows_are_unselectable(all_clients_table, self.selected_id), test_name,
                         'CHECK IF CORRECT ROWS ARE UNSELECTABLE',
                         'CHECK IF CORRECT ROWS ARE UNSELECTABLE FAILED')
            # Closing clients dialog
            self.wait_until_visible(type=By.XPATH, element=popups.ACL_SUBJECTS_SEARCH_POPUP_CLOSE_BTN_XPATH).click()

            self.log('Selecting previously added client')
            # Select previously added client
            select_subjects_from_table(self, subjects_table=clients_with_services_table, subjects=self.selected_id)

            # TEST PLAN 2.1.9.2-2 open access rights
            self.log('2.1.9.2-2 open access rights')

            self.log('Opening access rights of the selected client')
            # Open client access rights
            self.by_id(popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_OPEN_CLIENTS_SERVICES_ID).click()
            self.log('Reading already opened services')
            # load already open services into list
            already_opened_services = popups.open_services_table_rows(self)

            # TEST PLAN 2.1.9.2-3 add services
            self.log('2.1.9.2-3 add services')

            self.log('Clicking on "add services" button')
            # Click on add services BTN
            self.wait_until_visible(type=By.ID,
                                    element=popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ADD_SERVICES_BTN_ID).click()

            self.wait_jquery()
            clients_with_services_table = self.wait_until_visible(type=By.ID,
                                                                  element=popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ALL_SERVICES_TABLE_ID)

            self.is_true(rows_are_unselectable(table=clients_with_services_table, rows=already_opened_services),
                         test_name,
                         '2.1.9.2-3 check if correct rows are unselectable - failed',
                         '2.1.9.2-3 check if correct rows are unselectable')

            # TEST PLAN 2.1.9.2-4 select services
            self.log('2.1.9.2-4 select services')

            self.log('Selecting services which should be not already assigned')

            if rows_to_select[1] == [0]:
                selected_services = select_rows(self=self, table=clients_with_services_table, rows_to_select=0)
            else:
                selected_services = select_rows(self=self, table=clients_with_services_table,
                                                rows_to_select=rows_to_select[1])

            self.log('Clicking on "add selected to ACL" button')
            # Click on 'add selected to ACL' button
            self.by_id(popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_ADD_SELECTED_TO_ACL_BTN_ID).click()

            self.log('Reading all opened services of the client')
            # Load all opened services to list
            all_opened_services = popups.open_services_table_rows(self)

            # Remove services that were there before
            recently_added_services = list(set(all_opened_services) - set(already_opened_services))

            # TEST PLAN 2.1.9.2-5 verify added access
            self.log('2.1.9.2-5 verify added access')

            self.is_equal(selected_services, recently_added_services,
                          test_name,
                          '2.1.9.2-5 verify added access - failed',
                          '2.1.9.2-5 verify added access')
        except Exception:
            self.log('2.1.9.2 ERROR: {0}'.format(traceback.format_exc()))

        if remove_data:
            remove_added_data(self)

    return test_case


def remove_added_data(self):
    """
    removes added data specific to these tests
    :param self: MainController class object
    """
    self.log('2.1.9-del Removing data')
    # Logout, login. no need for logout functionality testing at this point so we can logout from url
    self.driver.get(self.url + 'login/logout')
    self.login()

    # Open clients
    clients_table_vm.open_acl_subjects_popup(self)

    self.wait_jquery()
    clients_with_services_table = self.wait_until_visible(type=By.ID,
                                                          element=popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_TABLE_ID)

    self.log('Selecting previously added client')
    # Select previously added client
    select_subjects_from_table(self, subjects_table=clients_with_services_table, subjects=self.selected_id)
    self.log('Opening access rights of the selected client')
    # Open client access rights
    self.by_id(popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_OPEN_CLIENTS_SERVICES_ID).click()
    # wait for services table to be visible possible ajax call
    self.wait_jquery()
    # remove all added services data
    self.by_id(popups.ACL_SUBJECT_OPEN_SERVICES_ADD_POPUP_REMOVE_ALL_SERVICES_BTN_ID).click()
    popups.confirm_dialog_click(self)

    self.driver.get(self.url + 'login/logout')
