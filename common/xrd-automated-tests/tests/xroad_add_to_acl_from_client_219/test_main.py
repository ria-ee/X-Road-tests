# coding=utf-8
from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_add_to_acl_from_client_219 import add_to_acl_client_2_1_9 as test_add_to_acl_client


class AddToAclFromClient(unittest.TestCase):
    main = None

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
        main.url = main.config.get('ss1.host')
        main.username = main.config.get('ss1.user')
        main.password = main.config.get('ss1.pass')
        main.close_webdriver = True
        main.tear_down = True
        main.log_in = True
        main.driver.get(main.url)
        main.login(main.username, main.password)
        return main
