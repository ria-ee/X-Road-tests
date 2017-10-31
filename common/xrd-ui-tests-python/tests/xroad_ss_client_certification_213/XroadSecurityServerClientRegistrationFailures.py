from __future__ import absolute_import

import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_ss_client_certification_213 import client_certification_2_1_3


class XroadSecurityServerClientRegistrationFailures(unittest.TestCase):
    """
    SS_30 extensions(4a, 6a, 7a, 8a, 9a, 9b, 10a, 11a)
    RIA URL: https://jira.ria.ee/browse/XTKB-102
    RIA URL: https://jira.ria.ee/browse/XTKB-115
    Depends on finishing other test(s): client_registration
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_registration_failures_213(self):
        main = MainController(self)

        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
        client_name = main.config.get('ss2.client2_name')
        client_id = main.config.get('ss2.client2_id')
        ca_name = main.config.get('ca.host')
        client = xroad.split_xroad_id(client_id)
        member_code = client['code']
        member_class = client['class']
        member_instance = client['instance']
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        main.reset_webdriver(main.url, main.username, main.password)
        fail_test_func = client_certification_2_1_3.failing_tests(client_name, member_class, member_code,
                                                                  member_instance, ca_name=ca_name,
                                                                  ss2_ssh_host=ss2_ssh_host, ss2_ssh_user=ss2_ssh_user,
                                                                  ss2_ssh_pass=ss2_ssh_pass)

        fail_test_func(main)
        main.tearDown()
