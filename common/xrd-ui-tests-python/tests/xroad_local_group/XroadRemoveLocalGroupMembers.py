from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_local_group import xroad_local_group


class XroadRemoveLocalGroupMembers(unittest.TestCase):
    """
    UC SERVICE_27 Remove Members from a Local Group
    RIA URL: https://jira.ria.ee/browse/XT-284, https://jira.ria.ee/browse/XTKB-154
    Depends on finishing other test(s): None
    Requires helper scenarios:
    xroad_client_registration_in_ss_221\XroadSecurityServerClientRegistration.py
    xroad_configure_service_222\XroadConfigureService.py
    X-Road version: 6.16.0
    """
    def test_add_sub_to_member(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SERVICE_27'
        main.test_name = self.__class__.__name__

        main.log('TEST: SERVICE_27 Remove Members from a Local Group')
        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')

        try:
            '''Open webdriver'''
            main.reload_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_local_group.test_remove_member_from_local_group()
            test_func(main)
        except:
            main.log('XroadRemoveLocalGroupMembers: Failed to remove member from a local group')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
