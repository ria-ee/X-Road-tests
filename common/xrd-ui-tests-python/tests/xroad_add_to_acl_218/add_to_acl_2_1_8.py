# coding=utf-8
from selenium.webdriver.common.by import By
from helpers import xroad

from view_models import popups, clients_table_vm


def select_existing_acl_subjects(self, subjects, select_duplicate=False):
    '''
    Waits until ACL subject list is visible, loaded and then selects (clicks on) subjects from this table.
    :param self: MainController class object
    :param subjects: List of strings - X-Road IDs
    :param select_duplicate: Boolean to allow selecting duplicate rows from the table (if there are duplicate IDs)
    :return: List of selected subject IDs
    '''
    self.log('Subject list table: {0}'.format(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_TABLE_ID))
    # Find the search results table element and wait until it is visible.
    subject_list_table = self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_TABLE_ID, type=By.ID)

    # The table should be visible now. Select the subjects and return them.
    return clients_table_vm.select_subjects_from_table(self, subject_list_table, subjects, select_duplicate)


def select_subjects_to_acl(self, service_subjects, select_duplicate=True):
    '''
    Finds the ACL subject list and selects (clicks on) subjects from it.

    :param self: MainController class object
    :param service_subjects: List of strings - X-Road IDs
    :param select_duplicate: Boolean to allow selecting duplicate rows from the table (if there are duplicate IDs)
    :return: List of selected subject IDs
    '''
    # Find the search results table element
    subject_search_results_table = self.by_id(popups.ACL_SUBJECTS_SEARCH_POPUP_RESULTS_TABLE_ID)

    # Select the subjects and return them
    return clients_table_vm.select_subjects_from_table(self, subject_search_results_table, service_subjects,
                                                       select_duplicate=select_duplicate)


def add_subjects_to_acl(self, service_subjects, select_duplicate=True):
    '''
    Adds subjects to ACL list by calling the functions to select them and then clicking the "Add selected to ACL" button.
    :param self: MainController class object
    :param service_subjects: List of strings - X-Road IDs
    :param select_duplicate: Boolean to allow selecting duplicate rows from the table (if there are duplicate IDs)
    :return: List of selected subject IDs
    '''

    # Select subjects from ACL list.
    selected_ids = select_subjects_to_acl(self, service_subjects, select_duplicate)

    # Find the button element and click it
    add_selected_to_acl_button = self.by_id(popups.ACL_SUBJECTS_SEARCH_POPUP_ADD_SELECTED_TO_ACL_BUTTON_ID)
    add_selected_to_acl_button.click()

    # Return selected IDs
    return selected_ids


def remove_subjects_from_acl(self, service_subjects, select_duplicate=False):
    '''
    Removes subjects from ACL.
    :param self: MainController class object
    :param service_subjects: List of strings - X-Road IDs
    :param select_duplicate: Boolean to allow selecting duplicate rows from the table (if there are duplicate IDs)
    :return: None
    '''

    # Wait until first ACL row is visible (this means that the data has been parsed and loaded into a table)
    self.log(
        'Waiting until visible: {0}'.format(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_FIRST_SUBJECT_ROW_CSS))
    self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_FIRST_SUBJECT_ROW_CSS,
                            type=By.CSS_SELECTOR)

    self.log('Removing subjects: {0}'.format(', '.join(service_subjects)))
    if service_subjects:
        # If subject list is not empty, select the subjects in it (click on them)
        select_existing_acl_subjects(self, service_subjects, select_duplicate=select_duplicate)

        # Find the "Remove selected" button and click it.
        remove_selected_button = self.by_id(popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_REMOVE_SELECTED_BTN_ID)
        remove_selected_button.click()

        # A confirmation dialog should open, confirm what you're asked.
        popups.confirm_dialog_click(self)
    else:
        # Subject list empty, do not remove anything.
        self.log('Nothing to be removed')


def remove_all_subjects_from_acl(self):
    '''
    Removes ALL subjects from ACL by clicking the "Remove all" button.
    :param self: MainController class object
    :return: None
    '''

    # Wait until first ACL row is visible (this means that the data has been parsed and loaded into a table)
    self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_FIRST_SUBJECT_ROW_CSS,
                            type=By.CSS_SELECTOR, timeout=20)

    # Find the "Remove all" button and click it
    remove_all_button = self.by_id(popups.CLIENT_DETAILS_POPUP_ACL_SUBJECTS_REMOVE_ALL_BTN_ID)
    remove_all_button.click()

    # A confirmation dialog should open, confirm what you're asked.
    popups.confirm_dialog_click(self)


def add_all_subjects_to_acl(self, return_list=True):
    '''
    Adds all subjects in the list to the ACL.
    :param self: MainController class object
    :param return_list: Boolean - do we need to return a list of subjects that should have been added.
    :return: List of subjects or if return_list is False, an empty list.
    '''
    added_subjects = []

    # We return the actual list only if we are instructed to (by default actually but can still be disabled).
    # This is because, with long lists, it is quite slow to loop over every element and check its ID.
    if return_list:
        # Find all selectable elements that have class xroad-id
        selectable_xroad_elements = self.by_css(popups.XROAD_ID_SELECTABLE_ROW_CSS, multiple=True)

        # Loop over the found elements and save their IDs for returning.
        self.log('Looping over results list and collecting ids. May be slow, elements: {0}'.format(
            len(selectable_xroad_elements)))
        for element in selectable_xroad_elements:
            added_subjects.append(element.text)

        self.log('Loop finished')

    # Find the "Add all to ACL" button and click it
    add_all_to_acl_button = self.by_id(popups.ACL_SUBJECTS_SEARCH_POPUP_ADD_ALL_TO_ACL_BUTTON_ID)
    add_all_to_acl_button.click()

    # A dialog box should open. Wait until the button "Confirm" is visible, then click it.
    popups.confirm_dialog_click(self)

    # Return the list of added subjects or an empty list
    return added_subjects


def get_current_acl_subjects(self):
    '''
    Get the current ACL subject IDs as a list.
    :param self: MainController class object
    :return: List of subject XRoad IDs
    '''

    # Find all ACL subjects' XRoad IDs
    subject_list = self.by_css(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_XROAD_ID_ELEMENTS_CSS, multiple=True)

    # Initialize list containing current subject ids
    subject_ids = []

    # Loop over the elements and add them to our "current" list
    for subject in subject_list:
        subject_ids.append(subject.text)

    # Return the list.
    return subject_ids


def verify_added_subjects(self, current_subjects, added_subjects, strict_check_duplicates=True):
    '''
    TEST PLAN 2.1.8.4.
    Verifies if all subjects were added to the ACL list. Needs the initial subject list and a list of added subjects
    as parameters and checks if these combined make up the new ACL list. Contains assertions for the test.
    :param self: MainController class object
    :param current_subjects: List of current ACL subjects' XRoad IDs
    :param added_subjects: List of XRoad IDs of the subjects that were added to ACL
    :param strict_check_duplicates: Boolean. If False, we consider the lists to be equal even if one of them has duplicates
            and the other doesn't.
    :return: (Boolean, int) - (True if all subjects were added; False otherwise, number of subjects that were added)
    '''

    self.log('Verifying added subject list')

    # Get the updated subject list that should also contain the subjects we just added.
    updated_subject_list = get_current_acl_subjects(self)

    # Get the difference between updated and old subject list - should be equal to subjects that should have been added.
    new_subjects_in_list = list(set(updated_subject_list) - set(current_subjects))

    # True if subjects to be added (added_subjects) match the updated list (new_subjects_in_list)
    if strict_check_duplicates:
        all_subjects_added = (sorted(added_subjects) == sorted(new_subjects_in_list))
    else:
        # We used list(set(list_variable)) because we check if the unique values match. The testing database contained
        # a few elements with duplicate XRoad IDs but we cannot check which is which so we fall back to unique values.
        # In real life system, no duplicates should be allowed.
        all_subjects_added = (sorted(list(set(added_subjects))) == sorted(list(set(new_subjects_in_list))))

    return all_subjects_added, len(new_subjects_in_list)


def search_all_subjects(self):
    '''
    TEST PLAN 2.1.8.2.
    In client ACL list view, click "Add subjects" and do an empty search.

    :param self:  MainController class object
    :return: None
    '''
    # We need to find the "Add subjects" button.
    add_subjects_button = self.by_id(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_ADD_SUBJECTS_BTN_CSS)

    # Click on the button to open the search window for subjects.
    add_subjects_button.click()

    # Find the search button in "Add Subjects" popup
    search_subjects_button = self.by_css(popups.ACL_SUBJECTS_SEARCH_POPUP_SEARCH_BTN_CSS)
    # We'll wait until the button is visible.
    self.wait_until_visible(search_subjects_button)
    # Click on the button to do an empty search and list all of the possible subjects.
    search_subjects_button.click()
    self.log('Clicking: Search')

    # Wait until the search button is visible
    self.wait_until_visible(search_subjects_button)
    self.log('Search subjects button visible')

    self.wait_until_visible(element=popups.ACL_SUBJECTS_SEARCH_POPUP_SEARCH_SUBJECTS_SELECTABLE_TABLE,
                            type=By.CSS_SELECTOR)
    self.log('Subjects table visible.')


def restore_original_subject_list(case, current_subjects, added_subjects, allow_remove_all=False,
                                  remove_duplicates=False):
    '''
    Restores the original subject list by computing the difference between the initial list and a list of added subjects,
    and then removing the items that weren't originally there.
    :param self: MainController class object
    :param current_subjects: List of current ACL subjects' XRoad IDs
    :param added_subjects: List of XRoad IDs of the subjects that were added to ACL
    :param allow_remove_all: Boolean. Allow using the "Remove all" button (works only if the original list was empty)
    :param remove_duplicates: Boolean. Allow removal of duplicate elements if there are any. Otherwise duplicates will remain.
    :return: None
    '''

    self = case

    # Restore the original ACL subjects list

    # If we are allowed to use "Remove all" and the initial list is empty, use "Remove all"
    if allow_remove_all and not current_subjects:
        self.log('Removing all subjects at once.')
        remove_all_subjects_from_acl(self)
    # If not, select each item and then click "Remove selected"
    else:
        self.log('Selecting each subject individually:')
        remove_subjects_from_acl(self, added_subjects, select_duplicate=remove_duplicates)

    # Wait until ajax query that removes the subjects finishes
    self.wait_jquery()

    # Get the post-restore subject list (for double-checking if restore was successful).
    restored_subject_list = get_current_acl_subjects(self)

    # True if original ACL list matches restored ACL list (restore successful)
    original_list_restored = (sorted(current_subjects) == sorted(restored_subject_list))
    if not original_list_restored:
        missing = list(set(current_subjects) - set(restored_subject_list))
        search_all_subjects(self)
        add_subjects_to_acl(self, service_subjects=missing)
        self.wait_jquery()
        restored_subject_list = get_current_acl_subjects(self)
        original_list_restored = (sorted(current_subjects) == sorted(restored_subject_list))

    # Test assertion for if the original list was successfully restored or not.
    self.is_true(original_list_restored, msg='Original subject list was not restored')

    self.log('Loop finished')


def test_add_subjects(case, client=None, client_name=None, client_id=None, wsdl_index=None, wsdl_url=None,
                      service_index=None,
                      service_name=None, service_subjects=[],
                      remove_data=True,
                      allow_remove_all=True,
                      remove_current=False):
    '''
    Test function. Adds specified subjects to a specified client's ACL.
    :param client_name: string | None - name of the client whose ACL we modify (this or client_id must be set)
    :param client_id: string | None - XRoad ID of the client whose ACL we modify (this or client_name must be set)
    :param wsdl_index: int - index (zero-based) for WSDL we select from the list
    :param service_index: int - index (zero-based) for WSDL we select from the list
    :param service_subjects: List of strings with the XRoad IDs of the subjects to be added to the ACL
    :param remove_data: Boolean - remove data after test or not.
    :param allow_remove_all: Boolean - allow using "Remove all" button when removing data and if original ACL was empty.
    :return:
    '''

    self = case
    client_id = xroad.get_xroad_subsystem(client)

    def add_to_acl():
        """
        :param self: MainController class object
        :return: None
        ''"""

        # TEST PLAN 2.1.8
        self.log('*** 2.1.8 / XT-462 / helper. Add access from service view.')

        # Select duplicate elements (if database, for some reason, contains duplicate IDs). Not actually configurable
        # but can be moved to parameters if necessary.
        select_duplicate = True

        #
        # TEST PLAN 2.1.8-1 Security server clients view: choose a client and open their Services tab.
        #
        self.log('2.1.8-1 Security server clients view: choose a client and open their Services tab.')

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_name=client_name, client_id=client_id)

        # Find the table that lists all WSDL files and services
        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        # Wait until that table is visible (opened in a popup)
        self.wait_until_visible(services_table)

        # Find the WSDL, expand it and select service
        clients_table_vm.client_services_popup_open_wsdl_acl(self, services_table=services_table,
                                                             service_index=service_index, service_name=service_name,
                                                             wsdl_index=wsdl_index, wsdl_url=wsdl_url)

        # A popup has been opened that lists current services. This may load for a few seconds with big lists.

        # We'll wait until the "Add subjects" button is visible (popup is open and list has been fully loaded)
        self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_ADD_SUBJECTS_BTN_CSS, type=By.ID,
                                timeout=20)

        # As we need to check that only the subjects that we add later make it to this list, we get the current list of
        # subjects for later comparison.
        current_subjects = get_current_acl_subjects(self)
        self.log('Current ACL subjects: {0}'.format(', '.join(current_subjects)))

        if remove_current:
            remove_all_subjects_from_acl(self)

        #
        # TEST PLAN 2.1.8-2. Do an empty search to show all subjects that are registered in the system.
        #
        self.log('2.1.8-2 Do an empty search to show all subjects that are registered in the system.')
        search_all_subjects(self)

        #
        # TEST PLAN 2.1.8-3. Select subjects from search results and click "Add Selected to ACL" button to add them.
        #

        self.log(
            '2.1.8-3. Select subjects from search results and click "Add Selected to ACL" button to add them.')
        self.added_subjects = add_subjects_to_acl(self, service_subjects, select_duplicate=select_duplicate)

        # Wait until ajax query that adds the subjects finishes.
        self.wait_jquery()

        # TEST PLAN 2.1.8-4. Check if ACL list has been updated and only the subjects we selected have been added.
        self.log('2.1.8-4. Check if ACL list has been updated and only the subjects we selected have been added.')
        all_subjects_added, added_subjects_count = verify_added_subjects(self, current_subjects, self.added_subjects,
                                                                         strict_check_duplicates=True)

        #
        # TEST PLAN general: UNDO THE CHANGES WE MADE
        #

        # Restore the original subject list if remove_data is True
        if remove_data:
            restore_original_subject_list(self, current_subjects, self.added_subjects, allow_remove_all,
                                          remove_duplicates=select_duplicate)
        else:
            self.log('2.1.8 Not restoring original ACL subject list')

        # Close all open dialogs (pre-logout, not essential)
        popups.close_all_open_dialogs(self)

        # Assertion if all selected subjects were added and found in the new subject list.
        self.is_true(all_subjects_added,
                      msg='2.1.8 Some subjects were not added, tried to add {0}, succeeded {1}'.format(
                          len(self.added_subjects), added_subjects_count))
        return current_subjects

    return add_to_acl


def test_add_all_subjects(case, client=None, client_name=None, client_id=None, wsdl_index=None, wsdl_url=None,
                          service_index=None,
                          service_name=None, remove_data=True,
                          allow_remove_all=True):
    '''
    MainController test function. Very similar to test_add_subjects but adds ALL subjects to a specified subject's ACL.
    :param client_name: string | None - name of the client whose ACL we modify (this or client_id must be set)
    :param client_id: string | None - XRoad ID of the client whose ACL we modify (this or client_name must be set)
    :param wsdl_index: int - index (zero-based) for WSDL we select from the list
    :param service_index: int - index (zero-based) for WSDL we select from the list
    :param remove_data: Boolean - remove data after test or not.
    :param allow_remove_all: Boolean - allow using "Remove all" button when removing data and if original ACL was empty.
    :return:
    '''

    self = case
    client_id = xroad.get_xroad_subsystem(client)

    def add_all_to_acl():
        """
        :param self: MainController class object
        :return: None
        ''"""

        self.log('2.1.8 add all to ACL')

        # Select duplicate elements (if database, for some reason, contains duplicate IDs). Not actually configurable
        # but can be moved to parameters if necessary.
        select_duplicate = True

        #
        # TEST PLAN 2.1.8-1 Security server clients view: choose a client and open their Services tab.
        #

        # Open client popup using shortcut button to open it directly at Services tab.
        clients_table_vm.open_client_popup_services(self, client_id=client_id)

        # Find the table that lists all WSDL files and services
        services_table = self.by_id(popups.CLIENT_DETAILS_POPUP_SERVICES_TABLE_ID)
        # Wait until that table is visible (opened in a popup)
        self.wait_until_visible(services_table)

        # Find the WSDL, expand it and select service
        clients_table_vm.client_services_popup_open_wsdl_acl(self, services_table=services_table,
                                                             service_index=service_index, service_name=service_name,
                                                             wsdl_index=wsdl_index, wsdl_url=wsdl_url)

        # A popup has been opened that lists current services. This may load for a few seconds with big lists.

        # We'll wait until the "Add subjects" button is visible (popup is open and list has been fully loaded)
        self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_EXISTING_ACL_SUBJECTS_ADD_SUBJECTS_BTN_CSS, type=By.ID,
                                timeout=20)

        # As we need to check that only the subjects that we add later make it to this list, we get the current list of
        # subjects for later comparison.
        current_subjects = get_current_acl_subjects(self)
        self.log('Current ACL subjects: {0}'.format(', '.join(current_subjects)))

        #
        # TEST PLAN 2.1.8-2 Do an empty search to show all subjects that are registered in the system.
        #
        search_all_subjects(self)

        #
        # TEST PLAN 2.1.8-3. Click "Add All to ACL" button to add all listed subjects to ACL.
        #

        self.added_subjects = add_all_subjects_to_acl(self)

        # Wait until ajax query that adds the subjects finishes
        self.wait_jquery()

        #
        # TEST PLAN 2.1.8-4. Check if ACL list has been updated and only the subjects we selected have been added.
        #
        all_subjects_added, added_subjects_count = verify_added_subjects(self, current_subjects, self.added_subjects,
                                                                         strict_check_duplicates=True)

        #
        # TEST PLAN general: UNDO THE CHANGES WE MADE
        #

        # Restore the original subject list
        if remove_data:
            self.log('Added subject count: {0}'.format(len(self.added_subjects)))
            restore_original_subject_list(self, current_subjects, self.added_subjects, allow_remove_all,
                                          remove_duplicates=select_duplicate)
        else:
            self.log('Not restoring original ACL subject list')

        # Close all open dialogs (pre-logout, not essential)
        popups.close_all_open_dialogs(self)

        # Assertion if all selected subjects were added and found in the new subject list.
        self.is_true(all_subjects_added, msg='Some subjects were not added, tried to add {0}, succeeded {1}'.format(
            len(self.added_subjects), added_subjects_count))

    return add_all_to_acl