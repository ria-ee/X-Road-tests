from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs


class XroadCentralService(unittest.TestCase):
    """
    UC SERVICE_11 (UC SERVICE 41/3) Parse User Input (Add a Central Service)
    RIA URL: https://jira.ria.ee/browse/XT-298, https://jira.ria.ee/browse/XTKB-57
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.9.4
    """
    def test_parse_central_service_inputs(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SERVICE_11'
        main.test_name = self.__class__.__name__

        main.log('TEST: SERVICE 41/3 PARSE ADDED CENTRAL SERVICES INPUTS')

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_parse_user_inputs.test_central_service_inputs()
            test_func(main)
        except:
            main.log('XroadCentralService: Failed to to parse user inputs')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
