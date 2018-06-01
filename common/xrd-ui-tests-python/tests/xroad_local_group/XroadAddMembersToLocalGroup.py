from __future__ import absolute_import

import unittest
from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_local_group import xroad_local_group


class XroadAddMembersToLocalGroup(unittest.TestCase):
    """
    UC SERVICE_26 Add Members to a Local Group
    RIA URL: https://jira.ria.ee/browse/XT-283, https://jira.ria.ee/browse/XTKB-153
    Depends on finishing other test(s): None
    Requires helper scenarios:
    xroad_client_registration_in_ss_221\XroadSecurityServerClientRegistration.py
    xroad_configure_service_222\XroadConfigureService.py
    X-Road version: 6.16.0
    """
    def test_add_sub_to_member(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SERVICE_26'
        main.test_name = self.__class__.__name__

        main.log('TEST: SERVICE_26 Add Members to a Local Group')
        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')
        client_name = main.config.get('ss2.client_name')
        subsystem_row = xroad.split_xroad_subsystem(main.config.get('ss2.client_id'))
        subsystem = subsystem_row['subsystem']

        try:
            '''Open webdriver'''
            main.reload_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_local_group.test_add_member_to_local_group(client_name=client_name, subsystem=subsystem)
            test_func(main)
        except:
            main.log('XroadAddMembersToLocalGroup: Failed to add member to a local group')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
