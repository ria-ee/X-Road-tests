from __future__ import absolute_import

import unittest

from tests.xroad_changing_database_rows_with_cs_gui_291 import changing_database_rows_with_cs_gui
from main.maincontroller import MainController


class XroadChangingDatabaseRowsWithGUICentralServer(unittest.TestCase):
    """
    Change Central Server database entries via graphical user interface.
    CS_01 1-4 Log In to the Graphical User Interface
    CS_02 1-2 Log Out of the Graphical User Interface
    MEMBER_10 1-2, 4-5 Add an X-Road Member
    MEMBER_11 1-3, 4 Edit the Name of an X-Road Member
    MEMBER_26 1-7 Delete an X-Road Member
    RIA URL: https://jira.ria.ee/browse/XT-302
    RIA URL: https://jira.ria.ee/browse/XT-303
    RIA URL: https://jira.ria.ee/browse/XT-362
    RIA URL: https://jira.ria.ee/browse/XT-363
    RIA URL: https://jira.ria.ee/browse/XT-378
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_changing_database_rows_with_cs_gui_2_9_1(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'MEMBER_10 / MEMBER_11 / MEMBER_26'
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

        test_func = changing_database_rows_with_cs_gui.test_test(
            ssh_host=main.config.get('cs.ssh_host'),
            ssh_username=main.config.get('cs.ssh_user'),
            ssh_password=main.config.get('cs.ssh_pass'),
            users=users, client_id=client_id, client_name=client_name, client_name2=client_name2)
        test_func(main)
        main.tearDown()
