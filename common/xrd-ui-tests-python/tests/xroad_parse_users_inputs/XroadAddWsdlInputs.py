from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs


class XroadAddWsdlInputs(unittest.TestCase):
    """
    UC SERVICE_11 (UC SERVICE 08/3) Parse User Input (Add a WSDL to a Security Server Client)
    RIA URL: https://jira.ria.ee/browse/XT-265, https://jira.ria.ee/browse/XTKB-94
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.16.0
    """
    def test_parse_added_wsdl_inputs(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SS_41'
        main.test_name = self.__class__.__name__

        main.log('TEST: SERVICE 08/3 PARSE ADDED TIMEOUT WSDL URL INPUTS')
        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')

        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_parse_user_inputs.test_added_wsdl_inputs()
            test_func(main)
        except:
            main.log('XroadAddWsdlInputs: Failed to to parse user inputs')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
