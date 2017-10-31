from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_logging_in_cs_2111 import logging_in_cs_2_11_1


class XroadLoggingInCentralServer(unittest.TestCase):
    """
    MEMBER_10 1-2, 4-7, 4a
    MEMBER_11 1-2, 4-5
    RIA URL: https://jira.ria.ee/browse/XTKB-38
    RIA URL: https://jira.ria.ee/browse/XTKB-39
    Depends on finishing other test(s): client_registration
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_loggin_in_central_server_2_11_1(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.11.1'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')
        if main.driver is None:
            main.reset_webdriver(main.url, username=main.username, password=main.password, init_new_webdriver=False)

        group = main.config.get('cs.global_group')
        server_id = main.config.get('ss1.server_name')
        client_id = main.config.get('ss1.client2_id')
        client_name = main.config.get('ss1.client2_name')
        client_name2 = main.config.get('ss1.client2_name2')
        existing_client_id = main.config.get('ss1.management_id')
        existing_client_name = main.config.get('ss1.server_name')

        server_groups = '{0},{1},{2}'.format(main.config.get('xroad.registration_officer_group'),
                                             main.config.get('xroad.system_administrator_group'),
                                             main.config.get('xroad.security_officer_group'))

        users = {'user1': {'username': main.config.get('xroad.user1'), 'password': main.config.get('xroad.user1'),
                           'group': server_groups},
                 'user2': {'username': main.config.get('xroad.user2'), 'password': main.config.get('xroad.user2'),
                           'group': server_groups},
                 'user3': {'username': main.config.get('xroad.user3'), 'password': main.config.get('xroad.user3'),
                           'group': server_groups}
                 }

        main.log('TEST: LOGGING TEST IN CENTRAL SERVER')
        test_func = logging_in_cs_2_11_1.test_test(main.config.get('cs.ssh_host'),
                                                   main.config.get('cs.ssh_user'),
                                                   main.config.get('cs.ssh_pass'),
                                                   group=group, server_id=server_id, client_id=client_id,
                                                   client_name=client_name, client_name2=client_name2, users=users,
                                                   existing_client_id=existing_client_id,
                                                   existing_client_name=existing_client_name)
        test_func(main)
        main.tearDown()


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(XroadLoggingInCentralServer)
    unittest.TextTestRunner().run(suite)
