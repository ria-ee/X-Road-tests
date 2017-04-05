from __future__ import absolute_import

import unittest

from tests.xroad_ss_client_sertification_213 import client_certification_2_1_3
from main.maincontroller import MainController


class SecurityServerClientRegistrationFailures(unittest.TestCase):
    def test_registration_failures_213(self):
        main = MainController(self)
        main.url = main.config.get('ss1.host')
        main.username = main.config.get('ss1.user')
        main.password = main.config.get('ss1.pass')
        main.reset_webdriver(main.url, main.username, main.password)
        main.log('TEST: CERTIFYING SECURITY SERVER CLIENTS FAILURES')
        fail_test_func = client_certification_2_1_3.failing_tests()

        fail_test_func(main)
        main.tearDown()
