from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs


class XroadEditCsMemberInputs(unittest.TestCase):
    """
    UC MEMBER_54 (UC MEMBER 11/3) Parse User Input (Edit the Name of an X-Road Member)
    RIA URL: https://jira.ria.ee/browse/XT-363, https://jira.ria.ee/browse/XTKB-52
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.9.4
    """
    def test_parse_edit_cs_member_inputs(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'MEMBER_54'
        main.test_name = self.__class__.__name__

        main.log('TEST: MEMBER 11/3 PARSE EDITED MEMBER INPUTS')

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_parse_user_inputs.test_edit_cs_member_inputs()
            test_func(main)
        except:
            main.log('XroadCsMemberInputs: Failed to to parse user inputs')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
