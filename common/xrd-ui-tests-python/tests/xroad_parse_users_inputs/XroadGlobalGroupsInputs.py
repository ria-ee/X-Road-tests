from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs


class XroadGlobalGroupsInputs(unittest.TestCase):
    """
    UC SERVICE_11 (UC SERVICE 32/3) Parse User Input (Add a Global Group)
    RIA URL: https://jira.ria.ee/browse/XT-289, https://jira.ria.ee/browse/XTKB-56
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.16.0
    """
    def test_parse_global_groups_inputs(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SERVICE_11'
        main.test_name = self.__class__.__name__

        main.log('TEST: SERVICE 32/3 PARSE ADDED GLOBAL GROUPS INPUTS')

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_parse_user_inputs.test_global_groups_inputs()
            test_func(main)
        except:
            main.log('XroadGlobalGroupsInputs: Failed to to parse user inputs')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
