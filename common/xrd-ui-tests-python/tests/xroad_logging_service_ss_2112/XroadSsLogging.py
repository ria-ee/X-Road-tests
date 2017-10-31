from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_logging_service_ss_2112 import logging_service_ss_2_11_2
from view_models.log_constants import *


class XroadLoggingInSecurityServer(unittest.TestCase):
    """
    SERVICE_25 1-6, 3a, 4a Add a local group of a security server
    SERVICE_20 3 Set the option to verify TLS certificate of a servcie
    RIA URL: https://jira.ria.ee/browse/XTKB-36
    RIA URL: https://jira.ria.ee/browse/XTKB-77
    RIA URL: https://jira.ria.ee/browse/XTKB-157
    Depends on finishing other test(s): client deletion
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_loggin_in_security_server_2_11_2(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.11.2'
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
        test_func = logging_service_ss_2_11_2.test_test(ssh_host=main.config.get('ss1.ssh_host'),
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
