# coding=utf-8
from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_add_to_acl_from_client_219 import add_to_acl_client_2_1_9 as test_add_to_acl_client


class AddToAclFromClient(unittest.TestCase):
    main = None

    # TEST PLAN 2.1.9 add access from client view

    def test_add_1_client(self):
        main = self.get_main_object()

        main.log('TEST: ADD TO ACL FROM CLIENT VIEW')
        main.log('ADD 1 SERVICE TO CLIENT')
        test_add_to_acl_client.test_empty_client([1], remove_data=True)(main)

    def test_add_list_of_services(self):
        main = self.get_main_object()

        main.log('TEST: ADD TO ACL FROM CLIENT VIEW')
        main.log('ADD LIST OF SERVICES TO CLIENT')
        test_add_to_acl_client.test_empty_client([1, 3], remove_data=True)(main)

    def test_add_all_service(self):
        main = self.get_main_object()

        main.log('TEST: ADD TO ACL FROM CLIENT VIEW')
        main.log('ADD ALL SERVICES TO CLIENT')
        test_add_to_acl_client.test_empty_client(0, remove_data=True)(main)

    def test_add_1_client_to_existing(self):
        main = self.get_main_object()

        main.log('TEST: ADD TO ACL FROM CLIENT VIEW')
        main.log('ADD 1 SERVICE TO CLIENT WHERE ALREADY EXISTS')
        test_add_to_acl_client.test_existing_client(rows_to_select=[[1], [3]], remove_data=True)(main)

    def test_add_list_of_services_to_existing(self):
        main = self.get_main_object()

        main.log('TEST: ADD TO ACL FROM CLIENT VIEW')
        main.log('ADD LIST OF SERVICES TO CLIENT WHERE ALREADY EXISTS')
        test_add_to_acl_client.test_existing_client(rows_to_select=[[1], [2, 3]], remove_data=True)(main)

    def test_add_all_service_to_existing(self):
        main = self.get_main_object()
        main.log('TEST: ADD TO ACL FROM CLIENT VIEW')
        main.log('ADD ALL SERVICES TO CLIENT WHERE ALREADY EXISTS')
        test_add_to_acl_client.test_existing_client(rows_to_select=[[1], [0]], remove_data=True)(main)

    def get_main_object(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.1.9'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('ss1.host')
        username = main.config.get('ss1.user')
        password = main.config.get('ss1.pass')

        main.reset_webdriver(main.url, username=username, password=password)
        return main
