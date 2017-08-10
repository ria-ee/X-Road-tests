from __future__ import absolute_import

import unittest

from tests.xroad_parse_users_input_SS_41 import parse_user_input_SS_41
from main.maincontroller import MainController


class UserInputParse(unittest.TestCase):
    def test_parse_user_input_SS_41(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SS_41'
        main.test_name = self.__class__.__name__

        main.log('TEST: PARSE USER INPUT')
        main.url = main.config.get('ss1.host')
        main.username = main.config.get('ss1.user')
        main.password = main.config.get('ss1.pass')
        main.reset_webdriver(main.url, main.username, main.password)

        test_func = parse_user_input_SS_41.test_01()
        test_func(main)

        test_func = parse_user_input_SS_41.test_02()
        test_func(main)

        test_func = parse_user_input_SS_41.test_03()
        test_func(main)

        test_func = parse_user_input_SS_41.test_04()
        test_func(main)

        test_func = parse_user_input_SS_41.test_05()
        test_func(main)

        test_func = parse_user_input_SS_41.test_06()
        test_func(main)

        main.tearDown()

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')
        main.reset_webdriver(main.url, main.username, main.password)

        test_func = parse_user_input_SS_41.test_07()
        test_func(main)

        test_func = parse_user_input_SS_41.test_08()
        test_func(main)

        test_func = parse_user_input_SS_41.test_09()
        test_func(main)

        test_func = parse_user_input_SS_41.test_10()
        test_func(main)

        test_func = parse_user_input_SS_41.test_11()
        test_func(main)

        main.tearDown()
