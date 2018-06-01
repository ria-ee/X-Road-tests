from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_local_group import xroad_local_group
from helpers import xroad

class XroadDeleteLocalGroup(unittest.TestCase):
    """
    UC SERVICE_29 Delete a Local Group
    RIA URL: https://jira.ria.ee/browse/XT-286, https://jira.ria.ee/browse/XTKB-156
    Depends on finishing other test(s): None
    Requires helper scenarios:
    xroad_client_registration_in_ss_221\XroadSecurityServerClientRegistration.py
    xroad_configure_service_222\XroadConfigureService.py
    X-Road version: 6.16.0
    """
    def test_add_sub_to_member(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SERVICE_29'
        main.test_name = self.__class__.__name__

        main.log('TEST: SERVICE_29 Delete a Local Group')
        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
        client_name = main.config.get('ss2.client_name')
        subsystem_row = xroad.split_xroad_subsystem(main.config.get('ss2.client_id'))
        subsystem = subsystem_row['subsystem']
        try:
            '''Open webdriver'''
            main.reload_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_local_group.test_delete_local_group(client_name=client_name, subsystem=subsystem)
            test_func(main)
        except:
            main.log('XroadDeleteLocalGroup: Failed to delete a local group')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
