from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_logging_in_cs_2111 import logging_in_cs


class XroadLoggingInCentralServer(unittest.TestCase):
    """
    Test logging in central server.
    CS_01 Log In to the Graphical User Interface
    CS_02 Log Out of the Graphical User Interface
    MEMBER_10 1-2, 4-7, 4a Add an X-Road Member
    MEMBER_11 Edit the Name of an X-Road Member
    MEMBER_15 1, 5-8, 10 Create a Security Server Client Registration Request
    MEMBER_39 1-5, 7 Revoke a Registration Request
    MEMBER_26 1-8 Delete an X-Road Member
    MEMBER_56 Add a Subsystem to an X-Road Member
    SERVICE_32 1-6, 4a Add a Global Group
    SERVICE_33 1-2, 3 (partial), 4 Add Members to a Global Group
    SERVICE_39 1-3 Delete a Global Group
    RIA URL: https://jira.ria.ee/browse/XT-302
    RIA URL: https://jira.ria.ee/browse/XT-303
    RIA URL: https://jira.ria.ee/browse/XT-362, https://jira.ria.ee/browse/XTKB-38
    RIA URL: https://jira.ria.ee/browse/XT-363, https://jira.ria.ee/browse/XTKB-39
    RIA URL: https://jira.ria.ee/browse/XT-367
    RIA URL: https://jira.ria.ee/browse/XT-391
    RIA URL: https://jira.ria.ee/browse/XT-378, https://jira.ria.ee/browse/XTKB-41
    RIA URL:
    RIA URL: https://jira.ria.ee/browse/XT-289
    RIA URL: https://jira.ria.ee/browse/XT-290
    RIA URL: https://jira.ria.ee/browse/XT-296
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_loggin_in_central_server_2_11_1(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'MEMBER_10/MEMBER_11/MEMBER_15/MEMBER_39/MEMBER_26'
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

        test_func = logging_in_cs.test_test(main.config.get('cs.ssh_host'),
                                            main.config.get('cs.ssh_user'),
                                            main.config.get('cs.ssh_pass'),
                                            group=group, server_id=server_id, client_id=client_id,
                                            client_name=client_name, client_name2=client_name2, users=users,
                                            existing_client_id=existing_client_id,
                                            existing_client_name=existing_client_name)
        try:
            test_func(main)
        except:
            main.save_exception_data()
        finally:
            main.tearDown()
