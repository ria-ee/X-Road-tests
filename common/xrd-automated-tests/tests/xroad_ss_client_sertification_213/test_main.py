from __future__ import absolute_import

import unittest

import xroad
from tests.xroad_ss_client_sertification_213 import client_certification_2_1_3
from main.maincontroller import MainController


class SecurityServerClientRegistration(unittest.TestCase):
    def test_security_server_client_registration_2_1_3(self):
        MainController.close_webdriver = True
        MainController.tear_down = True
        MainController.log_in = True
        main = MainController(self)
        main.url = 'https://xtee9.ci.kit:4000/' #main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
        main.reset_webdriver(main.url, main.username, main.password)

        main.log('TEST: CERTIFYING SECURITY SERVER CLIENTS')
        # ss1_client = xroad.split_xroad_id('SUBSYSTEM : XTEE-CI-XM : GOV : 00000001 : MockSystemGatling')
        test_func = client_certification_2_1_3.test('00000001', 'GOV')
        test_func(main)
        main.tearDown()
