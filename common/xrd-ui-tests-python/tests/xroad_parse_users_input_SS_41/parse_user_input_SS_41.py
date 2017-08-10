import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import re

from view_models import sidebar as sidebar_constants, clients_table_vm, members_table,\
    keys_and_certificates_table as keyscertificates_constants, popups as popups, messages, \
    groups_table, central_services


def test_01():

    def test_case(self):
        """
        SS_28_4 System verifies entered key label
        :param self: MainController object
        :return: None
        """

        # TEST PLAN SS_28_4 System verifies entered key label
        self.log('*** SS_28_4 / XTKB-18')

        self.log('SS_28_4 System verifies entered key label')

        # Open the keys and certificates tab
        self.log('Open keys and certificates tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        time.sleep(5)

        # Loop through different key label names and expected results
        counter = 1
        for key_name in keyscertificates_constants.KEY_LABEL_TEXT_AND_RESULTS:
            input_text = key_name[0]
            error = key_name[1]
            error_message = key_name[2]
            error_message_label = key_name[3]
            whitespaces = key_name[4]

            self.log('Test-' + str(counter) + '. key label - "' + input_text + '"')

            # Generate key from softtoken
            add_key_label(self, input_text)

            # Verify key label
            parse_user_input(self, error, error_message, error_message_label)
            if error:
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_CANCEL_BTN_XPATH).click()
            else:
                self.log('Find entered key label name')
                key_label_name = self.wait_until_visible(type=By.XPATH,
                                                         element=keyscertificates_constants.
                                                         get_text(input_text.strip()))
                key_label_name = key_label_name.text
                if input_text == '':
                    # Verify that added key label can be empty
                    self.log('Find generated key label name')
                    self.wait_jquery()
                    key_name_hash = self.by_xpath(element='//tr[contains(@class, "unsaved")]')
                    key_name_hash = key_name_hash.text.encode('utf-8').split()
                    key_name_hash = key_name_hash[1]
                    self.log('Generated key label name - ' + key_name_hash)
                    # Verify that system generates key label name
                    reg_ex = r'^[A-Z0-9]*'
                    rex_ex_compare = re.findall(reg_ex, key_name_hash)

                    if len(key_name_hash) == 40 and key_name_hash == rex_ex_compare[0]:
                        generated_key_name = True
                    else:
                        generated_key_name = False
                    assert generated_key_name is True

                elif whitespaces:
                    find_text_with_whitespaces(self, input_text, key_label_name)
                else:
                    assert input_text in key_label_name
                # Delete the added key label
                delete_added_key_label(self)
            counter += 1

        self.wait_jquery()

    return test_case


def test_02():
    def test_case(self):
        """
        SS_29_5 System verifies entered CSR
        :param self: MainController object
        :return: None
        """

        # TEST PLAN SS_28_4 System verifies entered CSR
        self.log('*** SS_29_5 / XTKB-63')

        self.log('SS_29_5 System verifies entered CSR')

        # Open the keys and certificates tab
        self.log('Open keys and certificates tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.KEYSANDCERTIFICATES_BTN_CSS).click()
        time.sleep(5)

        # Generate key from softtoken
        add_key_label(self, keyscertificates_constants.KEY_LABEL_TEXT)

        self.log('Click on "GENERATE CSR" button')
        self.wait_jquery()
        self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATECSR_BTN_ID).click()

        # Verify user selections
        self.log('Verify Usage: selections')
        parse_user_selection(self, keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_USAGE_DROPDOWN_ID, 1)
        self.log('Verify Client: selections')
        parse_user_selection(self, keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CLIENT_DROPDOWN_ID, 1)
        self.log('Verify Certification Service: selections')
        parse_user_selection(self, keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_APPROVED_CA_DROPDOWN_ID, 2)
        self.log('Verify SCR Format: selections')
        parse_user_selection(self, keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_CSR_FORMAT_DROPDOWN_ID, 1)

        self.log('Click on "CANCEL" button')
        self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.GENERATE_CSR_SIGNING_REQUEST_POPUP_CANCEL_BTN_XPATH).click()

        # Delete the added key label
        delete_added_key_label(self)

    return test_case


def test_03():
    def test_case(self):
        """
        MEMBER_47 step 3 System verifies security server client input
        :param self: MainController object
        :return: None
        """
        # TEST PLAN MEMBER_47 step 3 System verifies clients member and subsystem code
        self.log('*** MEMBER_47_3 / XTKB-48')
        # Open security server clients tab
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        # Loop through clients members and subsystems codes and expected results
        counter = 1
        for add_client_data in clients_table_vm.MEMBER_SUBSYSTEM_CODE_AND_RESULTS:
            member_code = add_client_data[0]
            subsystem_code = add_client_data[1]
            error = add_client_data[2]
            error_message = add_client_data[3]
            error_message_label = add_client_data[4]
            whitespaces = add_client_data[5]

            self.log('Test-' + str(counter) + '. Member Code == "' + member_code +
                     '", Subsystem_code == "' + subsystem_code + '"')
            # Add client
            add_ss_client(self, member_code, subsystem_code)

            # Verify code, subsystem
            parse_user_input(self, error, error_message, error_message_label)
            if error:
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_CANCEL_BTN_XPATH).click()
            else:
                self.log('Click on "CONTINUE" button')
                self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
                self.log('Click on "CONFIRM" button')
                popups.confirm_dialog_click(self)

                self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
                client_id = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                                    get_client_id_by_member_code_subsystem_code(member_code.strip(),
                                                                                                subsystem_code.strip()))
                client_id_text = client_id.text
                self.log(client_id_text)
                if whitespaces:
                    find_text_with_whitespaces(self, member_code, client_id_text)
                    find_text_with_whitespaces(self, subsystem_code, client_id_text)
                else:
                    assert member_code and subsystem_code in client_id_text

                # Delete the added client
                delete_added_client(self, client_id)
            counter += 1

        self.wait_jquery()
    return test_case


def test_04():
    def test_case(self):
        """
        SERVICE_09 step 3 Verifies WSDL url
        :param self: MainController object
        :return: None
        """
        # TEST PLAN SERVICE 9 step 3 System verifies clients member and subsystem code
        self.log('*** SERVICE_09_3 / XTKB-53')
        # Open security server clients tab
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        member_code = clients_table_vm.ONE_SS_CLIENT[0]
        subsystem_code = clients_table_vm.ONE_SS_CLIENT[1]

        # Add client
        add_ss_client(self, member_code, subsystem_code)

        self.log('Click on "CONTINUE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

        self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
        client_id = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                            get_client_id_by_member_code_subsystem_code(member_code,
                                                                                        subsystem_code))
        counter = 1
        # Loop through wsdl url's
        for wsdl_data in clients_table_vm.WSDL_DATA:
            wsdl_url = wsdl_data[0]
            error = wsdl_data[1]
            error_message = wsdl_data[2]
            error_message_label = wsdl_data[3]
            whitespaces = wsdl_data[4]

            self.log('Test-' + str(counter) + '. WSDL URL == "' + wsdl_url + '"')

            self.log("Open client details")
            self.double_click(client_id)

            add_wsdl_url(self, wsdl_url)

            parse_user_input(self, error, error_message, error_message_label)

            self.wait_jquery()
            if error:
                self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_CANCEL_BTN_XPATH).click()
            else:
                # Verify that the added WSDL URL exists
                self.log('Find added WSDL URL row number - ' + wsdl_url)
                found_wsdl_url = self.wait_until_visible(type=By.CSS_SELECTOR,
                                                         element=popups.CLIENT_DETAILS_POPUP_WSDL_CSS)
                found_wsdl_url = found_wsdl_url.text
                if whitespaces:
                    find_text_with_whitespaces(self, wsdl_url, found_wsdl_url)
                else:
                    assert wsdl_url in found_wsdl_url
                    self.log('Found WSDL URL - ' + found_wsdl_url)

            self.log('Click on "CLOSE" button')
            self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        client_id = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                            get_client_id_by_member_code_subsystem_code(member_code, subsystem_code))
        self.log('Delete added client')
        delete_added_client(self, client_id)
        counter += 1

    return test_case


def test_05():
    def test_case(self):
        """
        SERVICE_09 step 3 Verifies WSDL url
        :param self: MainController object
        :return: None
        """
        # TEST PLAN SERVICE 9 step 3 System verifies clients member and subsystem code
        self.log('*** SERVICE_09_3 / XTKB-53')
        # Open security server clients tab
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        # Loop through clients members and subsystems codes and expected results
        member_code = clients_table_vm.ONE_SS_CLIENT[0]
        subsystem_code = clients_table_vm.ONE_SS_CLIENT[1]

        # Add client
        add_ss_client(self, member_code, subsystem_code)

        self.log('Click on "CONTINUE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

        self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
        client_id = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                            get_client_id_by_member_code_subsystem_code(member_code,
                                                                                        subsystem_code))
        # Add wsdl url
        self.log("Open client details")
        self.double_click(client_id)

        add_wsdl_url(self, clients_table_vm.WSDL_URL)

        self.log('Click on WSDL url row')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=popups.CLIENT_DETAILS_POPUP_WSDL_CSS).click()

        wsdl_disabled = True
        counter = 1
        for wsdl_disable_notice in clients_table_vm.WSDL_DISABLE_NOTICES:
            notice = wsdl_disable_notice[0]
            error = wsdl_disable_notice[1]
            error_message = wsdl_disable_notice[2]
            error_message_label = wsdl_disable_notice[3]

            self.log('Test-' + str(counter) + '. Notice == "' + notice + '"')

            if wsdl_disabled:
                self.log('Click on "ENABLE" button')
                self.wait_until_visible(type=By.ID,
                                        element=popups.CLIENT_DETAILS_POPUP_ENABLE_WSDL_BTN_ID).click()
            self.log('Click on "DISABLE" button')
            self.wait_until_visible(type=By.ID,
                                    element=popups.CLIENT_DETAILS_POPUP_DISABLE_WSDL_BTN_ID).click()
            self.log('Add notice - "' + notice + '"')
            notice_field = self.wait_until_visible(type=By.ID,
                                                   element=popups.DISABLE_WSDL_POPUP_NOTICE_ID)
            self.input(notice_field, notice)
            self.log('Click on "OK" button')
            self.wait_until_visible(type=By.XPATH,
                                    element=popups.DISABLE_WSDL_POPUP_OK_BTN_XPATH).click()
            parse_user_input(self, error, error_message, error_message_label)
            if error:
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.XPATH,
                                        element=popups.DISABLE_WSDL_POPUP_CANCEL_BTN_XPATH).click()
                wsdl_disabled = False
            else:
                wsdl_disabled = True
                # TODO: Kus saab 6igeid sisestusi kontrollida
        self.wait_jquery()
        self.log('Click on "CLOSE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        self.log('Delete added client')
        delete_added_client(self, client_id)
        counter += 1

    return test_case


def test_06():
    def test_case(self):
        """
        SERVICE_19 step 3 verifies address of a service
        :param self: MainController object
        :return: None
        """
        # TEST PLAN SERVICE 19 step 3 System verifies address of a service
        self.log('*** SERVICE_19_3 / XTKB-55')
        # Open security server clients tab
        self.log('Open security server clients tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CLIENTS_BTN_CSS).click()

        # Get parameters member_code and subsystem_code from clients_table_vm.py
        member_code = clients_table_vm.ONE_SS_CLIENT[0]
        subsystem_code = clients_table_vm.ONE_SS_CLIENT[1]

        # Add client of the security service
        add_ss_client(self, member_code, subsystem_code)

        # Confirm added client
        self.log('Click on "CONTINUE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.WARNING_POPUP_CONTINUE_XPATH).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

        # Get a client id as a parameter
        self.log('Find added Member Code == "' + member_code + ', Subsystem Code == ' + subsystem_code)
        client_id = self.wait_until_visible(type=By.XPATH, element=clients_table_vm.
                                            get_client_id_by_member_code_subsystem_code(member_code,
                                                                                        subsystem_code))
        # Add a wsdl url
        self.log("Open client details")
        self.double_click(client_id)

        add_wsdl_url(self, clients_table_vm.WSDL_URL)

        # Open WSDL URL services
        self.log('Open WSDL URL services, clicking on "+"')
        self.wait_until_visible(type=By.CLASS_NAME, element=popups.CLIENT_DETAILS_POPUP_WSDL_URL_DETAILS_CLASS).click()

        counter = 1

        # Loop through data from the clients_table_vm.py
        for service_url_data in clients_table_vm.SERVICE_URLS_DATA:
            # Set necessary parameters
            service_url = service_url_data[0]
            error = service_url_data[1]
            error_message = service_url_data[2]
            error_message_label = service_url_data[3]
            whitespaces = service_url_data[4]

            self.log('Test-' + str(counter) + '. Service url == "' + service_url + '"')

            # Activate a authCertDeletion service row
            self.log('Click on authCertDeletion service row')
            self.wait_until_visible(type=By.XPATH, element=popups.
                                    CLIENT_DETAILS_POPUP_WSDL_SERVICES_AUTHCERTDELETION_XPATH).click()
            # Add a service url
            self.log('Click on "EDIT" button')
            self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_EDIT_WSDL_BTN_ID).click()

            self.log('Enter service URL')
            entered_service_url = self.wait_until_visible(type=By.ID, element=popups.EDIT_SERVICE_POPUP_URL_ID)
            self.input(entered_service_url, service_url)

            self.log('Click on "OK" button')
            self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_OK_BTN_XPATH).click()

            # Check for the error messages
            parse_user_input(self, error, error_message, error_message_label)

            if error:
                # Close a pop-up window of the service details, if there is a error message
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.XPATH, element=popups.EDIT_SERVICE_POPUP_CANCEL_BTN_XPATH).click()
            else:
                # Verify that the added service url exists
                self.log('Find added service url text - ' + service_url.strip())
                get_srervice_url = clients_table_vm.find_service_url_by_text(self, service_url.strip())
                get_srervice_url = get_srervice_url.text
                self.log('Found service URL - ' + get_srervice_url)
                # Verify that there is not inputs with whitespaces
                if whitespaces:
                    find_text_with_whitespaces(self, service_url, get_srervice_url)
                else:
                    assert service_url in get_srervice_url
                    self.log('Found service URL - ' + get_srervice_url)

        # Close a pop-up window of the client details
        self.wait_jquery()
        self.log('Click on "CLOSE" button')
        self.wait_until_visible(type=By.XPATH, element=popups.CLIENT_DETAILS_POPUP_CLOSE_BTN_XPATH).click()

        # Delete added client
        delete_added_client(self, client_id)

        counter += 1

    return test_case


def test_07():
    def test_case(self):
        """
        MEMBER_10 step 4 and 6 System verifies added member in central server
        :param self: MainController object
        :return: None
        """
        # TEST PLAN MEMBER_10 step 4 and 6 System verifies clients member and subsystem code
        self.log('*** MEMBER_10_4, 6 / XTKB-48')

        # Loop through member names, classes, codes and expected results
        counter = 1
        for member in members_table.ADD_MEMBER_TEXTS_AND_RESULTS:
            member_name = member[0]
            member_class = member[1]
            member_code = member[2]
            error = member[3]
            error_message = member[4]
            error_message_label = member[5]
            whitespaces = member[6]
            self.log('Test-' + str(counter) + '. Member name == "' + member_name +
                     '", Member class == "' + member_class + '", Member code = "' + member_code + '"')

            add_cs_member(self, member_name, member_class, member_code)

            # Verify member name, member class, member code
            parse_user_input(self, error, error_message, error_message_label)

            if error:
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_CANCEL_BTN_XPATH).click()
            else:
                self.log('Get the confirmation message')
                self.wait_jquery()
                confirmation_message = messages.get_notice_message(self)
                self.log('Compare confirmation message to the expected confirmation message')
                assert confirmation_message in "Successfully added X-Road member with member class '" + member_class + \
                                               "' and member code '" + member_code.strip() + "'."

                # Close the member details pop up window
                self.log('Click on "CLOSE" button')
                self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH)\
                    .click()

                self.wait_jquery()
                # Verify that the added member name exists in the member table
                self.log('Find member name - ' + member_name + ' - in members table')
                get_member_name = self.by_xpath(element=members_table.
                                                get_member_data_from_table(1, member_name.strip()))
                get_member_name = get_member_name.text
                # Verify that the added member class exists in the member table
                self.log('Find member class - ' + member_class + ' - in members table')
                get_member_class = self.by_xpath(element=members_table.
                                                 get_member_data_from_table(2, member_class.strip()))
                get_member_class = get_member_class.text
                # Verify that the added member code exists in the member table
                self.log('Find member code - ' + member_code + ' - in members table')
                get_member_code = self.by_xpath(element=members_table.
                                                get_member_data_from_table(3, member_code.strip()))
                get_member_code = get_member_code.text

                if whitespaces:
                    find_text_with_whitespaces(self, member_name, get_member_name)
                    find_text_with_whitespaces(self, member_code, get_member_code)
                else:
                    assert member_name in get_member_name
                    assert member_class in get_member_class
                    assert member_code in get_member_code

                delete_added_member(self, member_name.strip())

            counter += 1

    return test_case


def test_08():
    def test_case(self):
        """
        MEMBER_11 step System verifies changed member name in the central server
        :param self: MainController object
        :return: None
        """
        # TEST PLAN MEMBER_11 step 3 System verifies changed member name in the central server
        self.log('*** MEMBER_11_3 / XTKB-52')

        # Add cs member
        add_cs_member(self, members_table.CS_MEMBER_NAME_CLASS_CODE[0],
                      members_table.CS_MEMBER_NAME_CLASS_CODE[1],
                      members_table.CS_MEMBER_NAME_CLASS_CODE[2])
        added_member_name = members_table.CS_MEMBER_NAME_CLASS_CODE[0]
        # Close the member details pop up window
        self.log('Click on "CLOSE" button')
        self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH) \
            .click()

        # Loop through member names and expected results
        counter = 1
        for member in members_table.CHANGE_MEMBER_TEXTS_AND_RESULTS:
            new_member_name = member[0]
            error = member[1]
            error_message = member[2]
            error_message_label = member[3]
            whitespaces = member[4]

            self.wait_jquery()
            self.log('Click member name - ' + added_member_name + ' - in members table')
            self.wait_until_visible(type=By.XPATH,
                                    element=members_table.get_member_data_from_table(1, added_member_name)).click()
            self.log('Click on "DETAILS" button')
            self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
            self.log('Click on "EDIT" button')
            self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_NAME_EDIT_BTN_XPATH).click()
            self.log('Change member name')
            edit_member_name = self.wait_until_visible(type=By.XPATH, element=members_table.
                                                       MEMBER_EDIT_NAME_POPUP_EDIT_NAME_AREA_XPATH)
            self.input(edit_member_name, new_member_name)

            self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_OK_BTN_XPATH)\
                .click()

            # Verify member name
            parse_user_input(self, error, error_message, error_message_label)

            if error:
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_NAME_POPUP_CANCEL_BTN_XPATH) \
                    .click()
                self.wait_jquery()
                self.log('Click on "Close" button')
                self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH)\
                    .click()

            else:
                added_member_name = new_member_name.strip()
                # Close the member details pop up window
                self.wait_jquery()
                self.log('Click on "CLOSE" button')
                self.wait_until_visible(type=By.XPATH,
                                        element=members_table.MEMBER_DETAILS_NAME_POPUP_CLOSE_BTN_XPATH).click()
                self.wait_jquery()
                # Verify that the added member name exists in the member table
                self.log('Find member name - ' + added_member_name + ' - in members table')
                get_member_name = self.by_xpath(element=members_table.get_member_data_from_table(1, added_member_name))
                get_member_name = get_member_name.text
                if whitespaces:
                    find_text_with_whitespaces(self, new_member_name, get_member_name)
                else:
                    assert new_member_name in get_member_name

        counter += 1
        # Delete added member
        delete_added_member(self, added_member_name)

    return test_case


def test_09():
    def test_case(self):
        """
        MEMBER_32 step 3 System verifies changed member name in the central server
        :param self: MainController object
        :return: None
        """
        # TEST PLAN MEMBER_32 step 3 System verifies changed member name in the central server
        self.log('*** MEMBER_32_3 / XTKB-56')

        # Open global groups
        self.log('Open Global Groups tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.GLOBAL_GROUPS_CSS).click()
        self.wait_jquery()

        # Loop through data from the groups_table.py
        counter = 1
        for group_data in groups_table.GROUP_DATA:
            # Set necessary parameters
            code = group_data[0]
            description = group_data[1]
            error = group_data[2]
            error_message = group_data[3]
            error_message_label = group_data[4]
            whitespaces = group_data[5]

            self.log('Test-' + str(counter) + '. Code == "' + code +
                     '", Description == "' + description + '"')

            # Start adding new group
            self.log('Click "ADD" to add new group')
            self.wait_until_visible(type=By.ID, element=groups_table.ADD_GROUP_BTN_ID).click()

            # Add new group
            self.log('2.11.1-8 add new group, fill in required fields')
            self.log('Send {0} to code area input'.format(code))
            group_code_input = self.wait_until_visible(type=By.ID, element=groups_table.GROUP_CODE_AREA_ID)
            self.input(group_code_input, code)
            self.log('Send {0} to code description input'.format(description))
            group_description_input = self.wait_until_visible(type=By.ID, element=groups_table.
                                                              GROUP_DESCRIPTION_AREA_ID)
            self.input(group_description_input, description)

            self.log('Click on "OK" to add new group')
            self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_OK_BTN_XPATH).click()
            self.wait_jquery()

            # Verify group code and description
            parse_user_input(self, error, error_message, error_message_label)

            if error:
                # Close a pop-up window , if there is a error message
                self.log('Click on "Cancel" button')
                self.wait_until_visible(type=By.XPATH, element=groups_table.NEW_GROUP_POPUP_CANCEL_BTN_XPATH).click()
                self.wait_jquery()
            else:
                # Verify that the added global group code exists
                self.log('Find added code text - ' + code.strip())
                global_croup_code = self.wait_until_visible(type=By.XPATH,
                                                            element=groups_table.
                                                            get_clobal_group_code_description_by_text(code.strip()))
                global_croup_code = global_croup_code.text
                # Verify that the added global group description exists
                self.log('Find added description text - ' + description.strip())
                global_croup_description = self.wait_until_visible(type=By.XPATH,
                                                                   element=groups_table.
                                                                   get_clobal_group_code_description_by_text(
                                                                       description.strip()))
                global_croup_description = global_croup_description.text
                self.log('Found global group code - ' + code)
                self.log('Found global group description - ' + description)

                if whitespaces:
                    find_text_with_whitespaces(self, code, global_croup_code)
                    find_text_with_whitespaces(self, description, global_croup_description)
                else:
                    assert code in global_croup_code
                    assert description in global_croup_description

                # Delete added global group
                self.log('Delete added global group')
                self.log('Click on added global group row')
                self.wait_until_visible(type=By.XPATH, element=groups_table.
                                        get_clobal_group_code_description_by_text(code.strip())).click()
                self.log('Click on "DETAILS" button')
                self.wait_until_visible(type=By.ID,
                                        element=groups_table.GROUP_DETAILS_BTN_ID).click()
                self.log('Click on "DELETE" button')
                self.wait_until_visible(type=By.XPATH,
                                        element=groups_table.DELETE_GROUP_BTN_ID).click()
                self.log('Click on "CONFIRM" button')
                popups.confirm_dialog_click(self)

            counter += 1

    return test_case


def test_10():
    def test_case(self):
        """
        SERVICE_42 step 3 System verifies added central services
        :param self: MainController object
        :return: None
        """
        # TEST PLAN MEMBER_42 step 3 System verifies added central services
        self.log('*** MEMBER_42_3 / XTKB-57')

        # Open central services
        self.log('Open Central Cervices tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CENTRAL_SERVICES_CSS).click()
        self.wait_jquery()

        # Loop through data from the groups_table.py
        counter = 1
        for group_data in central_services.NEW_CENTRAL_SERVICE_DATA:
            # Set parameters
            cs_code = group_data[0]
            code = group_data[1]
            version = group_data[2]
            provider_name = group_data[3]
            provider_code = group_data[4]
            provider_class = group_data[5]
            provider_subsystem = group_data[6]
            error = group_data[7]
            error_message = group_data[8]
            error_message_label = group_data[9]
            whitespaces = group_data[10]

            self.log('Test-' + str(counter) + '. Central Service Code == "' + cs_code +
                     '", Implementing Service Code == "' + code + '", Version == "' + version +
                     '", Provider name == "' + provider_name + '", Provider Code == "' + provider_code +
                     '", Provider Class == "' + provider_class + '", Provider subsystem == "' +
                     provider_subsystem + '"')

            # Start adding central service
            add_central_service(self, cs_code, code, version, provider_name, provider_code, provider_class,
                                provider_subsystem)

            # Verify central service data
            parse_user_input(self, error, error_message, error_message_label)

            if error:
                # Click on 'CANCEL' button
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_CANCEL_BUTTON_ID).click()
            else:
                # Verify that the added central service data exists
                self.log('Find added code text - ' + cs_code.strip())
                cs_code_in = self.wait_until_visible(type=By.XPATH,
                                                     element=central_services.get_central_service_text(cs_code.strip()))
                self.log('Find added code text - ' + code.strip())
                code_in = self.wait_until_visible(type=By.XPATH,
                                                  element=central_services.get_central_service_text(code.strip()))
                self.log('Find added code text - ' + version.strip())
                version_in = self.wait_until_visible(type=By.XPATH,
                                                     element=central_services.get_central_service_text(version.strip()))
                self.log('Find added code text - ' + provider_code.strip())
                provider_code_in = self.wait_until_visible(type=By.XPATH,
                                                           element=central_services.
                                                           get_central_service_text(provider_code.strip()))
                self.log('Find added code text - ' + provider_class.strip())
                self.wait_until_visible(type=By.XPATH,
                                        element=central_services.get_central_service_text(provider_class.strip()))
                self.log('Find added code text - ' + provider_subsystem.strip())
                provider_subsystem_in = self.wait_until_visible(type=By.XPATH,
                                                                element=central_services.
                                                                get_central_service_text(provider_subsystem.strip()))

                cs_code_text = cs_code_in.text
                code_text = code_in.text
                version_text = version_in.text
                provider_code_text = provider_code_in.text
                provider_subsystem_text = provider_subsystem_in.text

                if whitespaces:
                    find_text_with_whitespaces(self, cs_code, cs_code_text)
                    find_text_with_whitespaces(self, code, code_text)
                    find_text_with_whitespaces(self, version, version_text)
                    find_text_with_whitespaces(self, provider_code, provider_code_text)
                    find_text_with_whitespaces(self, provider_subsystem, provider_subsystem_text)
                else:
                    assert cs_code in cs_code_text
                    assert code in code_text
                    assert version in version_text
                    assert provider_code in provider_code_text
                    assert provider_subsystem in provider_subsystem_text

                # Delete added central service
                self.log('Delete added central service')
                self.log('Click on added central service row')
                cs_code_in.click()
                self.wait_jquery()
                self.log('Click on "DELETE" button')
                self.wait_until_visible(type=By.ID, element=central_services.SERVICE_DELETE_BUTTON_ID).click()
                self.log('Click on "CONFIRM" button')
                popups.confirm_dialog_click(self)

            counter += 1

    return test_case


def test_11():
    def test_case(self):
        """
        MEMBER_42 step 3 System verifies changed Implementing Service
        :param self: MainController object
        :return: None
        """
        # TEST PLAN MEMBER_32 step 3 System verifies changed Implementing Service
        self.log('*** MEMBER_42_3 / XTKB-58')

        # Open central services
        self.log('Open Central Cervices tab')
        self.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.CENTRAL_SERVICES_CSS).click()
        self.wait_jquery()

        # Start adding central service
        self.log('Add central service')
        add_central_service(self, central_services.CENTRAL_SERVICE[0], central_services.CENTRAL_SERVICE[1],
                            central_services.CENTRAL_SERVICE[2], central_services.CENTRAL_SERVICE[3],
                            central_services.CENTRAL_SERVICE[4], central_services.CENTRAL_SERVICE[5],
                            central_services.CENTRAL_SERVICE[6])

        cs_row = self.wait_until_visible(type=By.XPATH, element=central_services.
                                         get_central_service_text(central_services.CENTRAL_SERVICE[0].strip()))

        # Loop through data from the groups_table.py
        counter = 1
        for group_data in central_services.EDIT_CENTRAL_SERVICE_DATA:
            # Set parameters
            cs_code = group_data[0]
            code = group_data[1]
            version = group_data[2]
            provider_name = group_data[3]
            provider_code = group_data[4]
            provider_class = group_data[5]
            provider_subsystem = group_data[6]
            error = group_data[7]
            error_message = group_data[8]
            error_message_label = group_data[9]
            whitespaces = group_data[10]

            self.log('Test-' + str(counter) + '. Central Service Code == "' + cs_code +
                     '", Implementing Service Code == "' + code + '", Version == "' + version +
                     '", Provider name == "' + provider_name + '", Provider Code == "' + provider_code +
                     '", Provider Class == "' + provider_class + '", Provider subsystem == "' +
                     provider_subsystem + '"')

            self.log('Click on added central service row')
            cs_code_row = self.wait_until_visible(type=By.XPATH,
                                                  element=central_services.get_central_service_text('CS_CODE'))
            cs_code_row.click()

            # Start adding central service
            self.log('Click on "EDIT" button')
            self.wait_until_visible(type=By.ID, element=central_services.SERVICE_EDIT_BUTTON_ID).click()

            self.log('Click on "CLEAR" button')
            self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_CLEAR_BUTTON_ID).click()

            # Add code
            self.log('Add  code - ' + code)
            self.wait_jquery()
            code_input = self.wait_until_visible(type=By.ID,
                                                 element=popups.CENTRAL_SERVICE_POPUP_TARGET_CODE_ID)
            self.input(code_input, code)

            # Add version
            self.log('Add  code - ' + version)
            self.wait_jquery()
            version_input = self.wait_until_visible(type=By.ID,
                                                    element=popups.CENTRAL_SERVICE_POPUP_TARGET_VERSION_ID)
            self.input(version_input, version)

            # Add provider name
            self.log('Add  provider name - ' + provider_name)
            self.wait_jquery()
            provider_name_input = self.wait_until_visible(type=By.ID,
                                                          element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_ID)
            self.input(provider_name_input, provider_name)

            # Add provider code
            self.log('Add  provider code - ' + provider_code)
            self.wait_jquery()
            provider_code_input = self.wait_until_visible(type=By.ID,
                                                          element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CODE_ID)
            self.input(provider_code_input, provider_code)

            # Add provider class
            self.log('Select ' + provider_class + ' from "class" dropdown')
            select = Select(self.wait_until_visible(type=By.ID,
                                                    element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CLASS_ID))
            select.select_by_visible_text(provider_class)

            # Add provider subsystem
            self.log('Add  provider subsystem - ' + provider_subsystem)
            self.wait_jquery()
            provider_subsystem_input = self.wait_until_visible(type=By.ID,
                                                               element=popups.
                                                               CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_SUBSYSTEM_ID)
            self.input(provider_subsystem_input, provider_subsystem)

            # Click on 'OK' button
            self.log('Click on "OK" button')
            self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID).click()

            # Verify central service data
            parse_user_input(self, error, error_message, error_message_label)

            if error:
                # Click on 'CANCEL' button
                self.log('Click on "CANCEL" button')
                self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_CANCEL_BUTTON_ID).click()
            else:
                # Verify that the added central service data exists
                self.log('Find added code text - ' + cs_code.strip())
                cs_code_in = self.wait_until_visible(type=By.XPATH,
                                                     element=central_services.get_central_service_text(cs_code.strip()))
                self.log('Find added code text - ' + code.strip())
                code_in = self.wait_until_visible(type=By.XPATH,
                                                  element=central_services.get_central_service_text(code.strip()))
                self.log('Find added code text - ' + version.strip())
                version_in = self.wait_until_visible(type=By.XPATH,
                                                     element=central_services.get_central_service_text(version.strip()))
                self.log('Find added code text - ' + provider_code.strip())
                provider_code_in = self.wait_until_visible(type=By.XPATH,
                                                           element=central_services.
                                                           get_central_service_text(provider_code.strip()))
                self.log('Find added code text - ' + provider_class.strip())
                self.wait_until_visible(type=By.XPATH,
                                        element=central_services.get_central_service_text(provider_class.strip()))
                self.log('Find added code text - ' + provider_subsystem.strip())
                provider_subsystem_in = self.wait_until_visible(type=By.XPATH,
                                                                element=central_services.
                                                                get_central_service_text(provider_subsystem.strip()))

                code_text = code_in.text
                version_text = version_in.text
                provider_code_text = provider_code_in.text
                provider_subsystem_text = provider_subsystem_in.text

                if whitespaces:
                    find_text_with_whitespaces(self, code, code_text)
                    find_text_with_whitespaces(self, version, version_text)
                    find_text_with_whitespaces(self, provider_code, provider_code_text)
                    find_text_with_whitespaces(self, provider_subsystem, provider_subsystem_text)
                else:
                    assert code in code_text
                    assert version in version_text
                    assert provider_code in provider_code_text
                    assert provider_subsystem in provider_subsystem_text

            counter += 1

        # Delete added central service
        self.log('Delete added central service')
        self.log('Click on added central service row')
        cs_row = self.wait_until_visible(type=By.XPATH, element=central_services.
                                         get_central_service_text(central_services.CENTRAL_SERVICE[0].strip()))
        cs_row.click()
        self.wait_jquery()
        self.log('Click on "DELETE" button')
        self.wait_until_visible(type=By.ID, element=central_services.SERVICE_DELETE_BUTTON_ID).click()
        self.log('Click on "CONFIRM" button')
        popups.confirm_dialog_click(self)

    return test_case


def parse_user_selection(self, element, start_nr):
    """
    Verify user selections
    :param self: MainController object
    :param element: webelement
    :param start_nr: int
    :return:
    """

    self.log('Verify that there is no selected element with empty text, more than 256 characters and with whitespaces')
    element_exists = True
    while element_exists:
        try:
            self.wait_jquery()
            element_text = self.by_xpath(keyscertificates_constants.get_csr_data(element, start_nr))
            element_text = element_text.text
            element_without_whitespaces = element_text.strip()

            if element_text == '' or len(element_text) > 255 or len(element_text) != len(element_without_whitespaces):
                condition = False
            else:
                condition = True
            element_exists = True
            self.log('Selected text - ' + element_text)

        except:
            element_exists = False
            break

        assert condition is True
        self.log(condition)
        start_nr += 1


def parse_user_input(self, error, error_message, error_message_label):
    """
    Function Check for the error messages
    :param self: MainController object
    :param error: bool - Must there be a error message, True if there is and False if not
    :param error_message: str - Expected error message
    :param error_message_label: str - label for a expected error message
    :return:
    """
    if error:
        # Get a error message, compare it with expected error message and close error message
        self.log('Get the error message')
        self.wait_jquery()
        get_error_message = messages.get_error_message(self)
        self.log('Found error message - ' + get_error_message)
        self.log('Expected error message  - ' + error_message.format(error_message_label))

        self.log('Compare error message to the expected error message')
        assert get_error_message in error_message.format(error_message_label)

        self.log('Close the error message')
        messages.close_error_messages(self)
    else:
        # Verify that there is not error messages
        self.log('Verify that there is not error messages')
        get_error_message = messages.get_error_message(self)
        if get_error_message is None:
            error = False
        else:
            error = True
        assert error is False


def find_text_with_whitespaces(self, added_text, expected_text):
    """
    Verifies, that there is not inputs with whitespaces
    :param self: MainController object
    :param added_text: str - added text
    :param expected_text: str - expected text
    :return: None
    """
    try:
        # Compare added text with whitespaces and displayed text
        self.log('Compare added text with whitespaces and displayed text')
        self.log("'" + added_text + "' != '" + expected_text + "'")
        assert added_text in expected_text
        whitespace = True
    except:
        # Compare added text without whitespaces and displayed text
        self.log('Compare added text without whitespaces and displayed text')
        self.log("'" + added_text.strip() + "' == '" + expected_text + "'")
        assert added_text.strip() in expected_text
        whitespace = False
    assert whitespace is False


def add_key_label(self, key_label):
    """
    Add central key label
    :param self: MainController object
    :param key_label: str - key label
    :return:
    """
    # Generate key from softtoken
    self.wait_jquery()
    self.log('Click on softtoken row')
    self.wait_until_visible(type=By.XPATH, element=keyscertificates_constants.SOFTTOKEN_TABLE_ROW_XPATH).click()
    self.log('Click on "Generate key" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.GENERATEKEY_BTN_ID).click()

    # Enter key label
    self.log('Insert "' + key_label + '" to "LABEL" area')
    key_label_input = self.wait_until_visible(type=By.ID, element=popups.GENERATE_KEY_POPUP_KEY_LABEL_AREA_ID)
    self.input(key_label_input, key_label)

    # Save the key data
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.GENERATE_KEY_POPUP_OK_BTN_XPATH).click()


def add_cs_member(self, member_name, member_class, member_code):
    """
    Add central server member
    :param self: MainController object
    :param member_name: str - Member name
    :param member_class: str - Member class
    :param member_code: str - Member code
    :return:
    """
    # Add central server member
    self.wait_jquery()
    self.log('2.2.1-1: Wait for the "ADD" button and click')
    self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_BTN_ID).click()
    # Add member name
    self.log('2.2.1-1:  Enter ' + member_name + ' to "member name" area')
    input_name = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_NAME_AREA_ID)
    self.input(input_name, member_name)
    # Add member class
    self.log('2.2.1-1:  Select ' + member_class + ' from "class" dropdown')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=members_table.ADD_MEMBER_POPUP_MEMBER_CLASS_DROPDOWN_ID))
    select.select_by_visible_text(member_class)
    # Add member code
    self.log('2.2.1-1:  Enter ' + member_code + ' to "member code" area')
    input_code = self.wait_until_visible(type=By.ID, element=members_table.ADD_MEMBER_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member_code)
    # Click OK button to add member
    self.log('2.2.1-1:  Click "OK" to add member')
    self.wait_jquery()
    self.wait_until_visible(type=By.XPATH, element=members_table.ADD_MEMBER_POPUP_OK_BTN_XPATH).click()


def add_ss_client(self, member_code, subsystem_code):
    """
    Add security server client
    :param self: MainController object
    :param member_code: str
    :param subsystem_code: str
    :return:
    """
    # Add a client
    self.log('Click on "ADD CLIENT" button')
    self.wait_until_visible(type=By.ID, element=clients_table_vm.ADD_CLIENT_BTN_ID).click()

    # Add a member
    self.log('2.2.1-6: Enter ' + member_code + ' to  "MEMBER CODE AREA" dropdown')
    input_code = self.wait_until_visible(type=By.ID, element=popups.ADD_CLIENT_POPUP_MEMBER_CODE_AREA_ID)
    self.input(input_code, member_code)

    # Add a subsystem code
    self.log('2.2.1-6: Enter ' + subsystem_code + ' to  "SUBSYSTEM CODE AREA" dropdown')
    subsystem_input = self.wait_until_visible(type=By.XPATH,
                                              element=popups.ADD_CLIENT_POPUP_SUBSYSTEM_CODE_AREA_XPATH)
    self.input(subsystem_input, subsystem_code)

    # Save the client data
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_CLIENT_POPUP_OK_BTN_XPATH).click()


def add_wsdl_url(self, wsdl_url):
    """
    Add wsdl url to the client
    :param self: MainController object
    :param wsdl_url: str
    :return:
    """
    self.wait_jquery()
    self.log("Open 'Services' tab")
    self.wait_until_visible(type=By.XPATH, element=clients_table_vm.SERVICES_TAB_XPATH).click()
    self.log('Click on "Add WSDL" button')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_ADD_WSDL_BTN_ID).click()
    self.log('Enter WSDL URL - ' + wsdl_url)
    wsdl_url_element = self.wait_until_visible(type=By.ID, element=popups.ADD_WSDL_POPUP_URL_ID)
    self.input(wsdl_url_element, wsdl_url)
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.XPATH, element=popups.ADD_WSDL_POPUP_OK_BTN_XPATH).click()


def add_central_service(self, cs_code, code, version, provider_name, provider_code, provider_class, provider_subsystem):
    """
    Add central service
    :param self: MainController object
    :param cs_code: str
    :param code: str
    :param version: str
    :param provider_name: str
    :param provider_code: str
    :param provider_class: str
    :param provider_subsystem: str
    :return: None
    """

    # Start adding central service
    self.log('Click "ADD" to add new central service')
    self.wait_until_visible(type=By.ID, element=central_services.SERVICE_ADD_BUTTON_ID).click()

    # Add central service code
    self.log('Add central service code - ' + cs_code)
    self.wait_jquery()
    cs_code_input = self.wait_until_visible(type=By.ID,
                                            element=popups.CENTRAL_SERVICE_POPUP_CENTRAL_SERVICE_CODE_ID)
    self.input(cs_code_input, cs_code)

    # Add code
    self.log('Add  code - ' + code)
    self.wait_jquery()
    code_input = self.wait_until_visible(type=By.ID,
                                         element=popups.CENTRAL_SERVICE_POPUP_TARGET_CODE_ID)
    self.input(code_input, code)

    # Add version
    self.log('Add  code - ' + version)
    self.wait_jquery()
    version_input = self.wait_until_visible(type=By.ID,
                                            element=popups.CENTRAL_SERVICE_POPUP_TARGET_VERSION_ID)
    self.input(version_input, version)

    # Add provider name
    self.log('Add  provider name - ' + provider_name)
    self.wait_jquery()
    provider_name_input = self.wait_until_visible(type=By.ID,
                                                  element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_ID)
    self.input(provider_name_input, provider_name)

    # Add provider code
    self.log('Add  provider code - ' + provider_code)
    self.wait_jquery()
    provider_code_input = self.wait_until_visible(type=By.ID,
                                                  element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CODE_ID)
    self.input(provider_code_input, provider_code)

    # Add provider class
    self.log('Select ' + provider_class + ' from "class" dropdown')
    select = Select(self.wait_until_visible(type=By.ID,
                                            element=popups.CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_CLASS_ID))
    select.select_by_visible_text(provider_class)

    # Add provider subsystem
    self.log('Add  provider subsystem - ' + provider_subsystem)
    self.wait_jquery()
    provider_subsystem_input = self.wait_until_visible(type=By.ID,
                                                       element=popups.
                                                       CENTRAL_SERVICE_POPUP_TARGET_PROVIDER_SUBSYSTEM_ID)
    self.input(provider_subsystem_input, provider_subsystem)

    # Click on 'OK' button
    self.log('Click on "OK" button')
    self.wait_until_visible(type=By.ID, element=popups.CENTRAL_SERVICE_POPUP_OK_BUTTON_ID).click()


def delete_added_member(self, member_name):
    """
    Delete the member row from the list.
    :param self: MainController object
    :param member_name: str - member name
    :return: None
    """
    self.wait_jquery()
    self.log('Click member name - ' + member_name + ' - in members table')
    self.wait_until_visible(type=By.XPATH, element=members_table.get_member_data_from_table(1, member_name)).click()
    self.log('Click on "DETAILS" button')
    self.wait_until_visible(type=By.ID, element=members_table.MEMBERS_DETATILS_BTN_ID).click()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_EDIT_DELETE_BTN_XPATH).click()
    self.log('Click on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=members_table.MEMBER_DELETE_CONFIRM_BTN_ID).click()


def delete_added_client(self, client):
    """
    Delete the client row from the list.
    :param self: MainController object
    :param client: str - client id:
    :return: None
    """
    self.log("Open client details")
    self.double_click(client)
    # self.log('Click on "UNREGISTER" button')
    # self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_UNREGISTER_BUTTON_ID).click()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.ID, element=popups.CLIENT_DETAILS_POPUP_DELETE_BUTTON_ID).click()
    self.log('Click on "CONFIRM" button')
    popups.confirm_dialog_click(self)
    # self.log('Click on "CONFIRM" button')
    # popups.confirm_dialog_click(self)
    # TODO: Muudatus kui kliendid korda saavad


def delete_added_key_label(self):
    """
    Delete the key row from the list.
    :param self: MainController object
    :return: None
    """
    self.log('Delete added key')
    self.wait_jquery()
    self.log('Click on "DELETE" button')
    self.wait_until_visible(type=By.ID, element=keyscertificates_constants.DELETE_BTN_ID).click()
    self.log('Click on "CONFIRM" button')
    self.wait_until_visible(type=By.XPATH, element=popups.CONFIRM_POPUP_OK_BTN_XPATH).click()
    self.log('Added key is deleted')
