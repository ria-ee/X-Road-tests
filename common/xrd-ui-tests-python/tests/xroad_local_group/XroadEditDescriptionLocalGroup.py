from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_local_group import xroad_local_group


class XroadEditDescriptionLocalGroup(unittest.TestCase):
    """
    UC SERVICE_28 Edit the Description of a Local Group
    RIA URL: https://jira.ria.ee/browse/XT-285, https://jira.ria.ee/browse/XTKB-155
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.16.0
    """
    def test_add_sub_to_member(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SERVICE_28'
        main.test_name = self.__class__.__name__

        main.log('TEST: UC SERVICE_28 Edit the Description of a Local Group')
        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
    #
    # try:
        '''Open webdriver'''
        main.reload_webdriver(main.url, main.username, main.password)
        '''Run the test'''
        test_func = xroad_local_group.test_edit_local_group_description()
        test_func(main)
    # except:
    #     main.log('XroadEditDescriptionLocalGroup: Failed to edit the description of a local group')
    #     main.save_exception_data()
    #     assert False
    # finally:
    #     '''Test teardown'''
    #     main.tearDown()
