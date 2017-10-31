import sidebar as sidebar_vm
import popups
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from helpers import xroad
import messages

MEMBER_SUBSYSTEM_CODE_AND_RESULTS = [['', '', True, 'Missing parameter: {0}', 'add_member_code', False],
                                     ['', 'SUB_TEST', True, 'Missing parameter: {0}', 'add_member_code', False],
                                     ['SUB_TEST', '', True, 'Missing parameter: {0}', 'add_subsystem_code', False],
                                     [256 * 'A', 'SUB_TEST', True, "Parameter '{0}' input exceeds 255 characters", 'add_member_code', False],
                                     ['SUB_TEST', 256 * 'A', True, "Parameter '{0}' input exceeds 255 characters", 'add_subsystem_code', False],
                                     [256 * 'A', 256 * 'A', True, "Parameter '{0}' input exceeds 255 characters", 'add_member_code', False],
                                     ['SUB_TEST', 'TEST_SUB', False, None, None, False],
                                     ['Z', 'Y', False, None, None, False],
                                     ['   SUB_TEST   ', '   TEST_SUB   ', False, None, None, True]
                                     ]

ONE_SS_CLIENT = ['CL_TEST', 'TEST_CL']

WSDL_DATA = [['   {0}   ', False, None, None, True],
             ['{0}', False, None, None, False],
             ['', True, 'Missing parameter: {0}', 'new_url', None],
             ['http://{1}/#256#.wsdl', True, "Parameter '{0}' input exceeds 255 characters", 'new_url', None],
             ['http://{1}/#255#.wsdl', True, "Failed to edit WSDL: Downloading WSDL failed. WSDL URL must point to a WSDL file.", None, None],
             ]

WSDL_DATA_ADDING = [['   {0}   ', False, None, None, True],
                    ['', True, 'Missing parameter: {0}', 'wsdl_add_url', None],
                    ['http://{1}/#256#.wsdl', True, "Parameter '{0}' input exceeds 255 characters",
                     'wsdl_add_url', None],
                    ['http://{1}/#255#.wsdl', True,
                     "Failed to add WSDL: Downloading WSDL failed. WSDL URL must point to a WSDL file.", None, None],
                    ]

WSDL_DISABLE_NOTICES = [[256 * 'A', True, "Parameter '{0}' input exceeds 255 characters", 'wsdl_disabled_notice'],
                        [255 * 'A', False, None, None],
                        ['A', False, None, None],
                        ['Out of order', False, None, None],
                        ['', False, None, None],
                        ['   Out of order   ', False, None, None]
                        ]

SERVICE_URLS_DATA = [['', True, 'Missing parameter: {0}', 'params_url', False],
                     ['{0}#256#/managementservice/', True, "Parameter '{0}' input exceeds 255 characters", 'params_url', False],
                     ['{0}#255#/managementservice/', False, None, None, False],
                     ['{0}managementservice/', False, None, None, False],
                     ['    {0}managementservice/    ', False, None, None, True]
                     ]

SERVICE_TIMEOUTS_DATA = [[0, '', True, 'Missing parameter: {0}', 'params_timeout', False],
                         [256, '12', True, "Parameter '{0}' input exceeds 255 characters", 'params_timeout', False],
                         [0, '    12   ', False, None, None, True],
                         ]

ADD_CLIENT_BTN_ID = 'client_add'

CLIENT_TABLE_ID = 'clients'
DETAILS_TAB_CSS = 'li[data-tab="#details_tab"]'
ACL_SUBJECTS_TAB_CSS = 'li[data-tab="#acl_subjects_tab"]'
SERVICES_TAB_CSS = 'li[data-tab="#services_tab"]'
SERVICES_TAB_XPATH = '//div[@aria-describedby = "client_details_dialog"]//a[text()=" Services"]'
INTERNAL_CERTS_TAB_CSS = 'li[data-tab="#internal_certs_tab"]'
LOCAL_GROUPS_TAB_CSS = 'li[data-tab="#local_groups_tab"]'

INTERNAL_CERTS_TAB_TITLE_CSS = 'a[href="#internal_certs_tab"]'

CLIENT_ROW_CSS = '#clients tbody tr'
SELECT_CLIENT_FROM_GLOBAL_LIST_BTN_ID = 'client_select'
GLOBAL_CLIENT_LIST_SEARCH_BTN_XPATH = '//div[@aria-describedby = "client_select_dialog"]//button[contains(@class, "search")]'
SHOW_ONLY_LOCAL_CLIENTS_CHECKBOX_ID = 'search_filter'
GLOBAL_CLIENTS_TABLE_ID = 'clients_global_wrapper'
SELECT_CLIENT_POPUP_XPATH = '//div[@aria-describedby = "client_select_dialog"]'
SELECT_CLIENT_POPUP_OK_BTN_XPATH = SELECT_CLIENT_POPUP_XPATH + '//div[@class="ui-dialog-buttonset"]//button[span="OK"]'

CLIENT_STATUS_SAVED = 'saved'
CLIENT_STATUS_REGISTRATION = 'registration in progress'


def open_acl_subjects_popup(self, client_name):
    print('Open clients view')
    # Wait for the element and click
    self.wait_until_visible(self.by_css(sidebar_vm.CLIENTS_BTN_CSS)).click()
    print('Open Service clients dialog')
    self.wait_jquery()
    self.wait_until_visible(type=By.CSS_SELECTOR, element=CLIENT_ROW_CSS)
    table_rows = self.by_css(CLIENT_ROW_CSS, multiple=True)
    client_row_index = find_row_by_client(table_rows, client_name=client_name)
    table_rows[client_row_index].find_element_by_css_selector(ACL_SUBJECTS_TAB_CSS).click()


def find_row_by_client(table_rows, client=None, client_name=None, client_id=None):
    """
    Finds a client index (zero-based) in list of table rows by comparing the values in the table with the string
    supplied as a parameter.

    :param table_rows: WebElement - already found table rows
    :param client_name: string - client name
    :return: int | None - client row index (zero-based) or None if client was not found
    """

    if client is not None:
        client_id = xroad.get_xroad_id(client)
    if client_name is not None:
        cell_index = 1  # Second cell contains the client name
        compare_text = client_name
    elif client_id is not None:
        cell_index = 2  # Third cell contains the client ID
        compare_text = client_id
    else:
        # We don't know what we're looking for, return nothing
        return None

    for i, row in enumerate(table_rows):
        row_client_data = row.find_elements_by_tag_name('td')[cell_index]
        if row_client_data.text == compare_text:
            # We found our client! Return the row ID.
            return i

    print('Client not found: {0}'.format(compare_text))
    # Client not found, return none
    return None


def find_wsdl_by_name(self, wsdl_name):
    """
    Finds a WSDL index (zero based) from the table of WSDLs by comparing the values in the table with the
    string supplied.

    :param services_table: WebElement - services table that contains the rows
    :param wsdl_name: string - WSDL address with port
    :return: int | None - WSDL row index (zero-based) or None if client was not found
    """

    services_table_rows = self.by_css(popups.CLIENT_DETAILS_POPUP_WSDL_CSS, multiple=True)

    for i, row in enumerate(services_table_rows):
        # Get the second table cell
        row_wsdl_name = row.find_elements_by_tag_name("td")[1]

        # See if its content matches the WSDL address
        if re.match(popups.CLIENT_DETAILS_POPUP_WSDL_REGEX.format(re.escape(wsdl_name)), row_wsdl_name.text):
            # Match - return index
            return i

    # WSDL not found
    return None


def select_subjects_from_table(self, subjects_table, subjects, select_duplicate=False):
    '''
    Selects (clicks on) specified subjects in the table.
    :param self: MainController class object
    :param subjects_table: WebElement - the table we have already found somewhere else
    :param subjects: string | List of XRoad IDs (string) | List of 1-based indexes of the subjects to be selected
    :param select_duplicate: Boolean. Allow selection of duplicate elements if True. If False, don't select duplicates.
    :return:
    '''

    # If service_subjects is not a list, make it one
    if not isinstance(subjects, list):
        subjects = [subjects]

    # Initialize list of selected xroad ids
    selected_ids = []

    print('Looping over subjects list')

    # Loop over the subjects list and try to find them in the table
    for subject in subjects:
        # If the subject is an integer, it is a 1-based index of the element to be selected.
        if isinstance(subject, int):
            # Find the nth element by XPATH
            xroad_id = subjects_table.find_element_by_xpath(
                popups.XROAD_ID_BY_INDEX_XPATH.format(str(subject)))
        # Subject is a string, find the element by text
        else:
            # Find the element by string
            xroad_id = subjects_table.find_element_by_xpath(
                popups.XROAD_ID_BY_NAME_XPATH.format(subject))

        # Wait until the element is visible (scrolling may take some time)
        self.wait_until_visible(xroad_id)

        # Get the element text
        xroad_id_text = xroad_id.text

        # Get the current table row classes as a list
        current_row = xroad_id.find_element_by_xpath('../..')
        current_row_classes = self.get_classes(current_row)

        # If the element is unselectable, raise an exception
        if 'unselectable' in current_row_classes:
            raise RuntimeError(xroad_id_text + ' is unselectable')

        # Check if the element is already selected
        if xroad_id_text in selected_ids:
            if select_duplicate:
                # Duplicates allowed
                print('{0} already found in selected subjects list but selecting anyway'.format(xroad_id_text))
            else:
                # Duplicates not allowed, skip
                print('{0} already found in selected subjects list, ignoring'.format(xroad_id_text))
                continue

        # Add the ID to a list for later checking
        selected_ids.append(xroad_id_text)

        # Click the element
        xroad_id.click()

    return selected_ids


def get_client_row_element(self, client=None, client_name=None, client_id=None):
    # There might be a query still running, wait until it ends.
    self.wait_jquery()

    # Find all client rows in client table
    table_rows = self.wait_until_visible(CLIENT_ROW_CSS, type=By.CSS_SELECTOR, multiple=True)

    client_row_index = find_row_by_client(table_rows, client=client, client_name=client_name, client_id=client_id)
    if client_row_index is None:
        raise RuntimeError('Client not found, client_name={0}, client_id={1}'.format(client_name, client_id))

    client_row = table_rows[client_row_index]

    return client_row


def open_client_popup_services(self, client=None, client_name=None, client_id=None):
    return open_client_popup_tab(self, client=client, client_name=client_name, client_id=client_id, selector=SERVICES_TAB_CSS,
                                 type=By.CSS_SELECTOR)


def open_client_popup_internal_servers(self, client=None, client_name=None, client_id=None):
    return open_client_popup_tab(self, client=client, client_name=client_name, client_id=client_id, selector=INTERNAL_CERTS_TAB_CSS,
                                 type=By.CSS_SELECTOR)


def open_client_popup_tab(self, client=None, client_name=None, client_id=None, selector=None, type=By.CSS_SELECTOR):
    client_row = get_client_row_element(self, client=client, client_name=client_name, client_id=client_id)
    shortcut_button = client_row.find_element(type, selector)
    ''':type: selenium.webdriver.remote.webelement.WebElement'''

    # Click the button to open the tab directly under the client.
    shortcut_button.click()

    # Wait until everything has been loaded.
    self.wait_jquery()

    return True


def get_service_parameters(self, service_row):
    '''
    Returns a dictionary {code, name, version, acl_count, title, url, timeout, refresh} where
    service_code is the service code displayed
    acl_count is the number of clients in the ACL (displayed in brackets after the service code)
    title is the title of the service
    url is the URL of the service
    timeout is the current timeout of the service
    refresh is the date when the service was last refreshed
    :param self: MainController class object
    :param service_row: WebElement - table row with the service
    :return: dict{code: str, name: str, version: str, acl_count: int, title: str, url: str,
                timeout: int, refresh: str} | None
    '''
    try:
        # Get all cells of the row. Our values start from the second cell
        cells = service_row.find_elements_by_tag_name('td')

        service_code_cell = cells[1].text
        service_matches = re.search(popups.CLIENT_DETAILS_POPUP_SERVICE_CODE_REGEX, service_code_cell)

        service_code = service_matches.group(1)
        service_name = service_matches.group(2)
        service_version = service_matches.group(3)
        service_acl_count = int(service_matches.group(4))

        service_title = cells[2].text
        service_url = cells[3].text
        try:
            service_timeout = int(cells[4].text)
        except:
            service_timeout = None
        service_refresh = cells[5].text

        return {'code': service_code, 'name': service_name, 'version': service_version, 'acl_count': service_acl_count,
                'title': service_title, 'url': service_url, 'timeout': service_timeout, 'refresh': service_refresh}
    except:
        return None


def client_services_popup_select_wsdl(self, wsdl_index=None, wsdl_url=None):
    # Wait until everything has been downloaded
    self.wait_jquery()

    if wsdl_url is not None:
        wsdl_index = find_wsdl_by_name(self, wsdl_url)

    if wsdl_index is None:
        raise RuntimeError('WSDL index not found for {0}'.format(wsdl_url))

    self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_WSDL_CSS, type=By.CSS_SELECTOR, multiple=True)

    # We take the Nth element from the WSDL list, N=wsdl_index
    wsdl_row = client_services_popup_get_wsdl(self, wsdl_index)
    """:type: selenium.webdriver.remote.webelement.WebElement"""

    # Click the element to select it.
    wsdl_row.click()

    # Return the element, other code might need it
    return wsdl_row


def client_services_popup_get_services_rows(self, wsdl_index=None, wsdl_url=None):
    # Wait until WSDL definitions are visible and everything has been downloaded
    wsdl_list = self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_WSDL_CSS, type=By.CSS_SELECTOR, multiple=True)
    self.wait_jquery()

    if wsdl_url is not None:
        wsdl_index = find_wsdl_by_name(self, wsdl_url)

    if wsdl_index is None:
        raise RuntimeError('WSDL index not found for {0}'.format(wsdl_url))

    # We take the Nth element from the WSDL list, N=wsdl_index
    wsdl_element = client_services_popup_get_wsdl(self, wsdl_index)
    """:type: selenium.webdriver.remote.webelement.WebElement"""

    try:
        # If the WSDL element is not expanded, do it now by finding the plus sign and clicking it.
        open_services_element = wsdl_element.find_element_by_css_selector(
            popups.CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS)
        open_services_element.click()
    except Exception:
        # Ignore errors - the element is already expanded.
        pass

    service_rows = []

    try:
        # Loop over the table rows until:
        # a) get to the next WSDL row (= services list that we were scanning has ended)
        # b) get an exception - no next sibling found so we've reached the end of the table; or some other undefined
        #    state has been found so don't continue
        next_row = wsdl_element
        while True:
            # Find the following sibling (next element in HTML)
            next_row = next_row.find_element_by_xpath('./following-sibling::*')
            next_row_classes = self.get_classes(next_row)

            # Check if we're still looking at services. If not, go to exception handler that exits.
            if not 'service' in next_row_classes:
                # Services list has ended, exit loop
                break

            service_rows.append(next_row)

    except NoSuchElementException:
        # Nothing found, return what we've got
        return service_rows

    return service_rows


def client_services_popup_find_service(self, wsdl_index=None, wsdl_url=None, service_index=None, service_name=None):
    # Wait until WSDL definitions are visible
    self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_WSDL_CSS, type=By.CSS_SELECTOR, multiple=True)

    self.wait_jquery()

    if wsdl_url is not None:
        wsdl_index = find_wsdl_by_name(self, wsdl_url)

    if wsdl_index is None:
        raise RuntimeError('WSDL index not found for {0}'.format(wsdl_url))

    # We take the Nth element from the WSDL list, N=wsdl_index
    wsdl_element = client_services_popup_get_wsdl(self, wsdl_index)
    """:type: selenium.webdriver.remote.webelement.WebElement"""

    try:
        # If the WSDL element is not expanded, do it now by finding the plus sign and clicking it.
        open_services_element = wsdl_element.find_element_by_css_selector(
            popups.CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS)
        open_services_element.click()
    except Exception:
        # Ignore errors - the element is already expanded.
        pass

    if service_index is None:
        try:
            # Loop over the table rows until:
            # a) we find the service we were looking for
            # b) get to the next WSDL row (= services list that we were scanning has ended)
            # c) get an exception - no next sibling found so we've reached the end of the table; or some other undefined
            #    state has been found so don't continue
            next_row = wsdl_element
            while True:
                # Find the following sibling (next element in HTML)
                next_row = next_row.find_element_by_xpath('./following-sibling::*')
                next_row_classes = self.get_classes(next_row)

                # Check if we're still looking at services. If not, go to exception handler that exits.
                if not 'service' in next_row_classes:
                    raise RuntimeError('Services list has ended.')

                # Get the service name (second td element)
                service_name_text = next_row.find_elements_by_tag_name('td')[1].text
                if service_name_text.startswith('{0} '.format(service_name)) or service_name_text.startswith(
                        '{0}.'.format(service_name)):
                    service_row = next_row
                    break

        except (RuntimeError, NoSuchElementException):
            self.log('Service "{0}" not found.'.format(service_name))
            return None
    else:
        service_all_rows = self.by_css(popups.CLIENT_DETAILS_POPUP_SERVICE_ROWS_CSS, multiple=True)
        service_row_index = wsdl_index + 1 + service_index
        service_row = service_all_rows[service_row_index]

    return service_row


def client_services_popup_open_wsdl_acl(self, services_table, service_index=None, wsdl_index=None, service_name=None,
                                        wsdl_url=None):
    # Find all WSDL definitions (these define the services under them)
    wsdl_list = self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_WSDL_CSS, type=By.CSS_SELECTOR, multiple=True)

    if wsdl_index is None:
        wsdl_index = find_wsdl_by_name(self, wsdl_url)

    # We take the Nth element from the WSDL list, N=wsdl_index
    wsdl_element = client_services_popup_get_wsdl(self, wsdl_index)
    """:type: selenium.webdriver.remote.webelement.WebElement"""

    # Try to find the closed WSDL element and open it.
    try:
        open_services_element = wsdl_element.find_element_by_css_selector(
            popups.CLIENT_DETAILS_POPUP_WSDL_CLOSED_SERVICE_CSS)
        open_services_element.click()
    except NoSuchElementException:
        # We got an exception. Let's assume that the WSDL is already open. If it is not, we'll get another exception
        # when trying to find/click the service row.
        pass

    service_row = client_services_popup_find_service(self, wsdl_index=wsdl_index,
                                                     service_name=service_name)
    service_row.click()

    # Find the "Access Rights" button and click it to open the ACL popup window.
    access_rights_button = self.by_id(popups.CLIENT_DETAILS_POPUP_ACCESS_RIGHTS_BTN_ID)
    access_rights_button.click()


def client_services_popup_get_wsdl(self, wsdl_index):
    '''
    Get WSDL row element from services list by index.
    :param self: MainController class object
    :param wsdl_index: int - zero-based row index
    :return: selenium.webdriver.remote.webelement.WebElement
    '''
    # Find all WSDL definitions (these define the services under them)
    wsdl_list = self.wait_until_visible(popups.CLIENT_DETAILS_POPUP_WSDL_CSS, type=By.CSS_SELECTOR, multiple=True)

    # We take the Nth element from the WSDL list, N=wsdl_index
    wsdl_row = wsdl_list[wsdl_index]

    return wsdl_row


def client_servers_popup_set_connection(self, type):
    self.log('MEMBER_49 2. Selecting internal server connection type "{0}"'.format(type))
    connection_type_select = Select(self.by_id(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_CONNECTION_TYPE_ID))
    connection_type_select.select_by_value(type)

    self.log('MEMBER_49 3. Save button is pressed, system saves the connection type')
    connection_type_save_button = self.by_id(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_CONNECTION_TYPE_SAVE_BTN_ID)
    connection_type_save_button.click()

    self.log('Check if success message is shown')
    self.wait_jquery()
    notice = messages.get_notice_message(self)
    return (notice is not None)


def client_servers_popup_delete_tls_certs(self, cancel_deletion=False):
    """
    :param self:
    :param cancel_deletion: bool|False - if canceling before confirming
    :return:
    """
    delete_button = self.by_id(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_DELETE_CERTIFICATE_BTN_ID)
    deleted_certs = 0
    while True:
        certificate = self.by_css(popups.CLIENT_DETAILS_POPUP_INTERNAL_SERVERS_TLS_CERTS_CSS)
        # Nothing found
        if certificate is None:
            break
        # Table is empty, exit
        if 'dataTables_empty' in self.get_classes(certificate):
            break

        self.log('MEMBER_51 1. TLS certificate is selected')
        certificate.click()
        self.log('MEMBER_51 1. Delete button is pressed')
        delete_button.click()

        self.log('MEMBER_51 2. System prompts for confirmation')
        if cancel_deletion:
            self.log('MEMBER_51 3.a Deletion confirmation is canceled')
            self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_CANCEL_BTN_XPATH).click()
            self.log('Click delete button again')
            delete_button.click()

        self.log('MEMBER_51 3. Deletion is confirmed')
        popups.confirm_dialog_click(self)
        self.wait_jquery()

        deleted_certs += 1

    return deleted_certs


def get_client_id_by_member_code_subsystem_code(self, member_code, subsystem_code):
    client_id = self.config.get('ss2.client_id')
    client_id = client_id.split(' : ')
    instance = client_id[0]
    client_class = client_id[1]
    return '//span[text()= "SUBSYSTEM : ' + instance + ' : ' + client_class + ' : ' + member_code + ' : ' + \
           subsystem_code + '"]'


def get_client_subsystem_xpath(self, client):
    return '//span[text()= "SUBSYSTEM : ' + client['instance'] + ' : ' + client['class'] + ' : ' + client[
        'code'] + ' : ' + \
           client['subsystem'] + '"]'


def find_service_url_by_text(self, text):
    return self.wait_until_visible(type=By.XPATH, element='//table[@id="services"]//td[text()="' + text + '"]')


def find_service_timeout_by_text(self, url, timeout):
    return self.wait_until_visible(type=By.XPATH,
                                   element='//table[@id="services"]//td[text()="' + url + '"]/../td[text()="' + timeout + '"]')
