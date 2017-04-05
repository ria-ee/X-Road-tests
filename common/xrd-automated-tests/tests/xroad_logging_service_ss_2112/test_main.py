from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_logging_service_ss_2112 import logging_service_ss_2_11_2
from view_models.log_constants import *


class XroadLoggingInSecurityServer(unittest.TestCase):
    def test_loggin_in_security_server_2_11_2(self):
        MainController.close_webdriver = True
        MainController.tear_down = True
        MainController.log_in = False

        main = MainController(self)
        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')
        if main.driver is None:
            main.reset_webdriver(main.url, username=main.username, password=main.password, init_new_webdriver=False)

        # member = {'name': 'Client Two', 'class': 'GOV', 'code': 'CLIENT2'}
        # client = {'code': 'CLIENT2', 'class': 'GOV', 'subsystem_code': 'sub', 'type': 'SUBSYSTEM'}

        # users = {'user1': {'username': 'user1', 'password': 'user1',
        #                    'group': 'xroad-registration-officer,xroad-service-administrator'},
        #          'user2': {'username': 'user2', 'password': 'user2',
        #                    'group': 'xroad-registration-officer,xroad-service-administrator'},
        #          'user3': {'username': 'user3', 'password': 'user3',
        #                    'group': 'xroad-registration-officer,xroad-service-administrator'}
        #          }

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
