from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs
from helpers import xroad


class XroadEditAddressServiceInputs(unittest.TestCase):
    """
    UC SERVICE_11 (UC SERVICE_19/3) Parse User Input (Address of a Service)
    RIA URL: https://jira.ria.ee/browse/XT-276, https://jira.ria.ee/browse/XTKB-55
    Depends on finishing other test(s): None
    Requires helper scenarios: None
    X-Road version: 6.16.0
    """
    def test_parse_edit_address_service(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SERVICE_11'
        main.test_name = self.__class__.__name__

        main.log('TEST: SERVICE 19/3 PARSE EDITED ADDRESS OF A SERVICE INPUTS')
        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        try:
            '''Open webdriver'''
            main.reset_webdriver(main.url, main.username, main.password)
            '''Run the test'''
            test_func = xroad_parse_user_inputs.test_edit_address_service()
            test_func(main)
        except:
            main.log('XroadEditAddressServiceInputs: Failed to to parse user inputs')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()

