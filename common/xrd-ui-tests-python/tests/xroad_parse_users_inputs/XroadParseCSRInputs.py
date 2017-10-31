from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs


class XroadParseCSRInputs(unittest.TestCase):
    """
    UC SS 41 (UC SS 29/5) Parse User Input (CSR)
    RIA URL: https://jira.ria.ee/browse/XT-342, https://jira.ria.ee/browse/XTKB-63
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.9.4
    """
    def test_parse_csr_inputs(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SS_41'
        main.test_name = self.__class__.__name__

        main.log('TEST: SS 29/5 PARSE CSR SELECTIONS')
        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_parse_user_inputs.test_csr_inputs()
            test_func(main)
        except:
            main.log('XroadParseCSRInputs: Failed to to parse user inputs')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
