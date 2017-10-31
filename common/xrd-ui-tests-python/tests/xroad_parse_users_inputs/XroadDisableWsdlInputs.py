from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs


class XroadDisableWsdlInputs(unittest.TestCase):
    """
    UC SERVICE_11 (UC SERVICE 13/4) Parse User Input (WSDL URL)
    RIA URL: https://jira.ria.ee/browse/XT-270, https://jira.ria.ee/browse/XTKB-54
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.9.4
    """
    def test_parse_user_input_SS_41(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SERVICE_11'
        main.test_name = self.__class__.__name__

        main.log('TEST: SERVICE 13/4 PARSE DISABLE WSDL INPUTS')
        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')

        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_parse_user_inputs.test_disable_wsdl_inputs()
            test_func(main)
        except:
            main.log('XroadDisableWsdlInputs: Failed to to parse user inputs')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()

