from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_tokens_keys_certs import tokens_keys_certs


class XroadViewTokenDetails(unittest.TestCase):
    def test_view_token_details_SS_20(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_20'
        main.test_name = self.__class__.__name__

        main.log('TEST: UC SS_20. View the Details of a Token (XTKB-111)')
        main.url = main.config.get('ss1.host')
        main.username = main.config.get('ss1.user')
        main.password = main.config.get('ss1.pass')
        main.reset_webdriver(main.url, main.username, main.password)

        test_func = tokens_keys_certs.test_view_token_details()
        test_func(main)

        main.tearDown()
