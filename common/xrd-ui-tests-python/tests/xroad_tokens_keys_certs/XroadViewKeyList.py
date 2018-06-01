from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_tokens_keys_certs import tokens_keys_certs


class XroadViewKeyList(unittest.TestCase):
    def test_view_list_tokens_keys_certs_SS_19(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_19'
        main.test_name = self.__class__.__name__

        main.log('TEST: UC SS_19. View the List of Tokens, Keys and Certificates (XTKB-99)')
        main.url = main.config.get('ss1.host')
        main.username = main.config.get('ss1.user')
        main.password = main.config.get('ss1.pass')
        main.reset_webdriver(main.url, main.username, main.password)
        host = main.config.get('ca.host')

        test_func = tokens_keys_certs.test_view_list_of_tokens_keys_certs(host)
        try:
            test_func(main)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
