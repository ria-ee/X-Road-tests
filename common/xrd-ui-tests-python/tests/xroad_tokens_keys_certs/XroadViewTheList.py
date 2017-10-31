from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_tokens_keys_certs import tokens_keys_certs


class XroadViewTheList(unittest.TestCase):
    """
    UC  SS 19  View the Details of a Key
    RIA URL: https://jira.ria.ee/browse/XT-332, https://jira.ria.ee/browse/XTKB-99
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.9.4
    """
    def test_view_list_tokens_keys_certs_SS_19(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_19'
        main.test_name = self.__class__.__name__

        main.log('TEST: UC SS_19. View the List of Tokens, Keys and Certificates')
        main.url = main.config.get('ss1.host')
        main.username = main.config.get('ss1.user')
        main.password = main.config.get('ss1.pass')
        host = main.config.get('ca.host')

        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = tokens_keys_certs.test_view_list_of_tokens_keys_certs(host)
            test_func(main)
        except:
            main.log('XroadViewTheList: Failed to view the list of tokens, keys and certificates')
            main.save_exception_data()
            assert False
        finally:
            main.tearDown()
