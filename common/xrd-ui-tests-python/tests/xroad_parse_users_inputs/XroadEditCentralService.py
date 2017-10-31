from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs


class XroadEditCentralService(unittest.TestCase):
    """
    UC SERVICE_11 (UC SERVICE 42/3) Parse User Input (Edit the Implementing Service of a Central Service)
    RIA URL: https://jira.ria.ee/browse/XT-299, https://jira.ria.ee/browse/XTKB-58
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.9.4
    """
    def test_parse_edited_central_service_inputs(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SERVICE_11'
        main.test_name = self.__class__.__name__

        main.log('TEST: SERVICE 42/3 PARSE EDITED CENTRAL SERVICES INPUTS')

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_parse_user_inputs.test_edited_central_service_inputs()
            test_func(main)
        except:
            main.log('XroadEditCentralService: Failed to to parse user inputs')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
