from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_tokens_keys_certs import tokens_keys_certs


class XroadKeyDetails(unittest.TestCase):
    """
    UC  SS 21  View the Details of a Key
    RIA URL: https://jira.ria.ee/browse/XT-334, https://jira.ria.ee/browse/XTKB-112
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.16.0
    """
    def test_view_key_details_SS_21(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SS_21'
        main.test_name = self.__class__.__name__

        main.log('TEST: UC SS_21. View the Details of a Key')
        main.url = main.config.get('ss1.host')
        main.username = main.config.get('ss1.user')
        main.password = main.config.get('ss1.pass')

        try:
            '''Open webdriver'''
            main.reload_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = tokens_keys_certs.test_view_key_details()
            test_func(main)
        except:
            main.log('XroadKeyDetails: Failed to view details of a key')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
