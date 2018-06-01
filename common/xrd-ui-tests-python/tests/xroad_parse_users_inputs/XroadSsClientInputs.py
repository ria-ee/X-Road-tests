from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs


class XroadSsClientInputs(unittest.TestCase):
    """
    UC MEMBER_54 (UC MEMBER 47/3) Parse User Input (SS client)
    RIA URL: https://jira.ria.ee/browse/XT-399, https://jira.ria.ee/browse/XTKB-48
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.16.0
    """
    def test_parse_ss_client_inputs(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'MEMBER_54'
        main.test_name = self.__class__.__name__

        main.log('TEST: MEMBER 47/3 PARSE USER SS CLIENT INPUTS')
        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_parse_user_inputs.test_ss_client_inputs()
            test_func(main)
        except:
            main.log('XroadSsClientInputs: Failed to to parse user inputs')
            main.save_exception_data()
            raise
        finally:
            '''Test teardown'''
            main.tearDown()