from __future__ import absolute_import

import unittest

from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss_2_2_1
from main.maincontroller import MainController
from helpers import xroad


class XroadSecurityServerClientRegistration(unittest.TestCase):
    def test_client_registration(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.1'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        remove_added_data = False

        main.management_services = xroad.split_xroad_subsystem(main.config.get('ss1.management_id'))
        cs_member = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        ss2_client_2 = xroad.split_xroad_id(main.config.get('ss2.client2_id'))

        cs_member_name = main.config.get('ss1.client_name')
        ss1_client_name = main.config.get('ss1.client_name')
        ss2_client_name = main.config.get('ss2.client_name')
        ss2_client_2_name = main.config.get('ss2.client2_name')

        main.log('TEST: REGISTERING SECURITY SERVER CLIENT')
        test_func = client_registration_in_ss_2_2_1.test_test(main, main.config.get('cs.host'),
                                                              main.config.get('cs.user'),
                                                              main.config.get('cs.pass'),
                                                              main.config.get('ss1.host'), main.config.get('ss1.user'),
                                                              main.config.get('ss1.pass'),
                                                              main.config.get('ss2.host'), main.config.get('ss2.user'),
                                                              main.config.get('ss2.pass'),
                                                              cs_new_member=cs_member, cs_member_name=cs_member_name,
                                                              ss1_client=ss1_client, ss1_client_name=ss1_client_name,
                                                              ss2_client=ss2_client, ss2_client_name=ss2_client_name,
                                                              ss2_client_2=ss2_client_2,
                                                              ss2_client_2_name=ss2_client_2_name,
                                                              remove_added_data=remove_added_data)
        test_func()
        main.tearDown()
