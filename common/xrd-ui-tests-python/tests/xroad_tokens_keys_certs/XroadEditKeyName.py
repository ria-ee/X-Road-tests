from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from tests.xroad_tokens_keys_certs import tokens_keys_certs


class XroadEditKeyName(unittest.TestCase):
    def test_edit_key_name_SS_23(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'SS_23'
        main.test_name = self.__class__.__name__

        main.log('TEST: EDIT KEY NAME (XTKB-114)')
        main.url = main.config.get('ss1.host')
        main.username = main.config.get('ss1.user')
        main.password = main.config.get('ss1.pass')
        ssh_host = main.config.get('ss1.ssh_host')
        ssh_user = main.config.get('ss1.ssh_user')
        ssh_pass = main.config.get('ss1.ssh_pass')

        main.reset_webdriver(main.url, main.username, main.password)

        test_func = tokens_keys_certs.test_change_key_name(ssh_host, ssh_user, ssh_pass)
        try:
            test_func(main)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
