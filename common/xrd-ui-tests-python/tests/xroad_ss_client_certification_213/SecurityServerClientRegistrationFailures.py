from __future__ import absolute_import

import unittest

from tests.xroad_ss_client_certification_213 import client_certification_2_1_3
from main.maincontroller import MainController
from helpers import xroad


class SecurityServerClientRegistrationFailures(unittest.TestCase):
    def test_registration_failures_213(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.1.3'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
        client_name = main.config.get('ss2.client2_name')
        client_id = main.config.get('ss2.client2_id')
        ca_name = main.config.get('ca.host')
        client = xroad.split_xroad_id(client_id)
        member_code = client['code']
        member_class = client['class']
        member_instance = client['instance']

        main.reset_webdriver(main.url, main.username, main.password)
        main.log('TEST: CERTIFYING SECURITY SERVER CLIENTS FAILURES')
        fail_test_func = client_certification_2_1_3.failing_tests(client_name, member_class, member_code, member_instance, ca_name=ca_name)

        fail_test_func(main)
        main.tearDown()
