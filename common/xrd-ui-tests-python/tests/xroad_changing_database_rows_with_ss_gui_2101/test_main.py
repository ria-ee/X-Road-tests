from __future__ import absolute_import

import unittest

from tests.xroad_changing_database_rows_with_ss_gui_2101 import changing_database_rows_with_ss_gui_2_10_1
from main.maincontroller import MainController


class XroadChangingDatabaseRowsWithGUISecurityServer(unittest.TestCase):
    def test_changing_database_rows_with_ss_gui_2_10_1(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.10.1'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('ss1.host')
        if main.driver is None:
            main.reset_webdriver(main.url, init_new_webdriver=False)

        users = {'user1': {'username': main.config.get('xroad.user1'), 'password': main.config.get('xroad.user1'),
                           'group': main.config.get('xroad.registration_officer_group')},
                 'user2': {'username': main.config.get('xroad.user2'), 'password': main.config.get('xroad.user2'),
                           'group': main.config.get('xroad.registration_officer_group')},
                 'user3': {'username': main.config.get('xroad.user3'), 'password': main.config.get('xroad.user3'),
                           'group': main.config.get('xroad.registration_officer_group')},
                 'databaseuser': {'username': main.config.get('xroad.serverconf_db_user'),
                                  'password': main.config.get('xroad.serverconf_db_password'),
                                  'db_name': main.config.get('xroad.serverconf_db_name')}
                 }
        client_id = main.config.get('ss1.client3_id')

        main.log('TEST: CHANGING DATABASE ROWS WITH USER INTERFACE IN SECURITY SERVER')
        test_func = changing_database_rows_with_ss_gui_2_10_1.test_test(
            ssh_host=main.config.get('ss1.ssh_host'),
            ssh_username=main.config.get('ss1.ssh_user'),
            ssh_password=main.config.get('ss1.ssh_pass'),
            users=users, client_id=client_id)
        test_func(main)
        main.tearDown()
