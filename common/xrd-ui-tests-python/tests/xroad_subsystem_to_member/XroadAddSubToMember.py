from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_subsystem_to_member import xroad_add_subsystem_to_member


class XroadAddSubToMember(unittest.TestCase):
    """
    UC MEMBER_56 Add a Subsystem to an X-Road Member
    RIA URL: https://jira.ria.ee/browse/XTKB-146
    Depends on finishing other test(s): None
    Requires helper scenarios: MEMBER_10
    X-Road version: 6.16.0
    """
    def test_add_sub_to_member(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC MEMBER_56'
        main.test_name = self.__class__.__name__

        main.log('TEST: MEMBER_56 Add a Subsystem to an X-Road Member')
        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_add_subsystem_to_member.test_add_subsystem()
            test_func(main)
        except:
            main.log('XroadAddSubToMember: Failed to add subsystem')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
