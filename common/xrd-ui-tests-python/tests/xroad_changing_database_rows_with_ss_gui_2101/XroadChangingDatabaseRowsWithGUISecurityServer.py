from __future__ import absolute_import

import unittest

from tests.xroad_changing_database_rows_with_ss_gui_2101 import changing_database_rows_with_ss_gui
from main.maincontroller import MainController


class XroadChangingDatabaseRowsWithGUISecurityServer(unittest.TestCase):
    """
    Change Security Server database entries via graphical user interface.
    SS_01 1-4 Log In to the Graphical User Interface
    SS_02 1-2 Log Out of the Graphical User Interface
    MEMBER_47 1, 2, 4-6 Add a Client
    MEMBER_49 1-3 Change a Security Server Client's Internal Server Connection Type
    MEMBER_53 1-3, 4a, 7 Delete a Security Server Client
    RIA URL: https://jira.ria.ee/browse/XT-314
    RIA URL: https://jira.ria.ee/browse/XT-315
    RIA URL: https://jira.ria.ee/browse/XT-399
    RIA URL: https://jira.ria.ee/browse/XT-401
    RIA URL: https://jira.ria.ee/browse/XT-405
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_changing_database_rows_with_ss_gui_2_10_1(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'MEMBER_47 / MEMBER_49 / MEMBER_53'
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

        test_func = changing_database_rows_with_ss_gui.test_test(
            ssh_host=main.config.get('ss1.ssh_host'),
            ssh_username=main.config.get('ss1.ssh_user'),
            ssh_password=main.config.get('ss1.ssh_pass'),
            users=users, client_id=client_id)
        test_func(main)
        main.tearDown()
