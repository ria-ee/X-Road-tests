from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_tokens_keys_certs import tokens_keys_certs


class XroadViewKeyDetails(unittest.TestCase):
    def test_view_key_details_SS_21(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_21'
        main.test_name = self.__class__.__name__

        main.log('TEST: UC SS_21. View the Details of a Key (XTKB-112)')
        main.url = main.config.get('ss1.host')
        main.username = main.config.get('ss1.user')
        main.password = main.config.get('ss1.pass')
        main.reset_webdriver(main.url, main.username, main.password)

        test_func = tokens_keys_certs.test_view_key_details()
        try:
            test_func(main)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
