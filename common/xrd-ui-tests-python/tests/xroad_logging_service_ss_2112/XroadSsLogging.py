from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_logging_service_ss_2112 import logging_service_ss
from view_models.log_constants import *


class XroadLoggingInSecurityServer(unittest.TestCase):
    """
    SS_01 Log In to the Graphical User Interface
    SS_02 Log Out of the Graphical User Interface
    MEMBER_10 1, 2, 4, 5. Add an X-Road Member
    MEMBER_26 1-3 Delete an X-Road Member
    MEMBER_47 1, 2, 4-7, 5a Add a Client
    MEMBER_52 1-6 Unregister a Security Server Client
    MEMBER_53 1-7 Delete a Security Server Client
    SERVICE_08 1, 2, 4-7, 10, 5a Add a WSDL to a Security Server Client
    SERVICE_12 1, 2 Enable a WSDL
    SERVICE_19 1, 2, 4-6 Edit the Address of a Service
    SERVICE_20 Set the option to verify TLS certificate of a service
    SERVICE_21 1, 2, 4, 5 Edit the Timeout Value of a Service
    SERVICE_25 1-6, 3a, 4a Add a local group of a security server
    RIA URL: https://jira.ria.ee/browse/XT-314
    RIA URL: https://jira.ria.ee/browse/XT-315
    RIA URL: https://jira.ria.ee/browse/XT-362
    RIA URL: https://jira.ria.ee/browse/XT-378
    RIA URL: https://jira.ria.ee/browse/XT-399
    RIA URL: https://jira.ria.ee/browse/XT-404
    RIA URL: https://jira.ria.ee/browse/XT-405
    RIA URL: https://jira.ria.ee/browse/XT-265
    RIA URL: https://jira.ria.ee/browse/XT-269
    RIA URL: https://jira.ria.ee/browse/XT-276
    RIA URL: https://jira.ria.ee/browse/XT-277, https://jira.ria.ee/browse/XTKB-77
    RIA URL: https://jira.ria.ee/browse/XT-278
    RIA URL: https://jira.ria.ee/browse/XT-282, https://jira.ria.ee/browse/XTKB-36, https://jira.ria.ee/browse/XTKB-157
    Depends on finishing other test(s):
    Requires helper scenarios: add_to_acl
    X-Road version: 6.16.0
    """

    def test_logging_in_security_server(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'MEMBER_10 / MEMBER_47 / SERVICE_25 / SERVICE_08'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')
        if main.driver is None:
            main.reset_webdriver(main.url, username=main.username, password=main.password, init_new_webdriver=False)

        groups = '{0},{1}'.format(main.config.get('xroad.registration_officer_group'),
                                  main.config.get('xroad.service_administrator_group'))
        main.xroad_audit_log = LOG_FILE_LOCATION

        users = {'user1': {'username': main.config.get('xroad.user1'), 'password': main.config.get('xroad.user1'),
                           'group': groups},
                 'user2': {'username': main.config.get('xroad.user2'), 'password': main.config.get('xroad.user2'),
                           'group': groups},
                 'user3': {'username': main.config.get('xroad.user3'), 'password': main.config.get('xroad.user3'),
                           'group': groups}
                 }

        client_id = main.config.get('ss1.client2_id')
        client_name = main.config.get('ss1.client2_name')
        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        main.driver.get(main.url)
        main.login(main.username, main.password)
        main.log('TEST: LOGGING TEST IN SECURITY SERVER')
        test_func = logging_service_ss.test_test(ssh_host=main.config.get('ss1.ssh_host'),
                                                 ssh_username=main.config.get('ss1.ssh_user'),
                                                 ssh_password=main.config.get('ss1.ssh_pass'),
                                                 cs_host=main.config.get('cs.host'),
                                                 cs_username=main.config.get('cs.user'),
                                                 cs_password=main.config.get('cs.pass'),
                                                 sec_host=main.config.get('ss1.host'),
                                                 sec_username=main.config.get('ss1.user'),
                                                 sec_password=main.config.get('ss1.pass'),
                                                 users=users, client_id=client_id, client_name=client_name,
                                                 wsdl_url=wsdl_url)
        test_func(main)
        main.tearDown()
