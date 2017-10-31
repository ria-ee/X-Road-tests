from __future__ import absolute_import

import unittest

from tests.xroad_changing_database_rows_with_cs_gui_291 import changing_database_rows_with_cs_gui_2_9_1
from main.maincontroller import MainController


class XroadChangingDatabaseRowsWithGUICentralServer(unittest.TestCase):
    def test_changing_database_rows_with_cs_gui_2_9_1(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.9.1'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.reset_webdriver(main.url)

        groups = main.config.get('xroad.registration_officer_group')
        users = {'user1': {'username': main.config.get('xroad.user1'), 'password': main.config.get('xroad.user1'),
                           'group': groups},
                 'user2': {'username': main.config.get('xroad.user2'), 'password': main.config.get('xroad.user2'),
                           'group': groups},
                 'user3': {'username': main.config.get('xroad.user3'), 'password': main.config.get('xroad.user3'),
                           'group': groups},
                 'databaseuser': {'username': main.config.get('xroad.centerui_db_user'),
                                  'password': main.config.get('xroad.centerui_db_pass'),
                                  'db_name': main.config.get('xroad.centerui_db_name')}
                 }

        client_id = main.config.get('ss1.client2_id')
        client_name = main.config.get('ss1.client2_name')
        client_name2 = main.config.get('ss1.client2_name3')

        main.log('TEST: CHANGING DATABASE ROWS WITH USER INTERFACE IN CENTRAL SERVER')
        test_func = changing_database_rows_with_cs_gui_2_9_1.test_test(
            ssh_host=main.config.get('cs.ssh_host'),
            ssh_username=main.config.get('cs.ssh_user'),
            ssh_password=main.config.get('cs.ssh_pass'),
            users=users, client_id=client_id, client_name=client_name, client_name2=client_name2)
        test_func(main)
        main.tearDown()
