from __future__ import absolute_import

import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_client_registration_in_ss_221 import client_registration_in_ss_2_2_1


class XroadSecurityServerClientDeletion(unittest.TestCase):
    """
    MEMBER_14 Delete an X-Road Member's Subsystem
    MEMBER_53 Delete a Security Server Client
    RIA URL: https://jira.ria.ee/browse/XTKB-34
    RIA URL: https://jira.ria.ee/browse/XTKB-124
    RIA URL: https://jira.ria.ee/browse/XTKB-131
    Depends on finishing other test(s): client registration, global group
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_client_deletion(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.2.1'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        main.reset_webdriver(url=main.url, username=main.username, password=main.password, close_previous=False,
                             init_new_webdriver=False)

        ss1_ssh_host = main.config.get('ss1.ssh_host')
        ss1_ssh_username = main.config.get('ss1.ssh_user')
        ss1_ssh_password = main.config.get('ss1.ssh_pass')

        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_username = main.config.get('ss2.ssh_user')
        ss2_ssh_password = main.config.get('ss2.ssh_pass')

        main.management_services = xroad.split_xroad_subsystem(main.config.get('ss1.management_id'))
        cs_member = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        ss2_client_2 = xroad.split_xroad_id(main.config.get('ss2.client2_id'))

        cs_member_name = main.config.get('ss1.client_name')
        ss1_client_name = main.config.get('ss1.client_name')
        ss1_client_2_name = main.config.get('ss1.client2_name')
        ss2_client_name = main.config.get('ss2.client_name')
        ss2_client_2_name = main.config.get('ss2.client2_name')

        main.log('Removing added data from 2.2.1')
        test_func = client_registration_in_ss_2_2_1.test_remove(main.config.get('cs.host'),
                                                                main.config.get('cs.user'),
                                                                main.config.get('cs.pass'),
                                                                main.config.get('ss1.host'),
                                                                main.config.get('ss1.user'),
                                                                main.config.get('ss1.pass'),
                                                                main.config.get('ss2.host'),
                                                                main.config.get('ss2.user'),
                                                                main.config.get('ss2.pass'),
                                                                cs_new_member=cs_member, cs_member_name=cs_member_name,
                                                                ss1_client=ss1_client, ss1_client_name=ss1_client_name,
                                                                ss1_client_2=ss1_client_2,
                                                                ss1_client_2_name=ss1_client_2_name,
                                                                ss1_ssh_host=ss1_ssh_host,
                                                                ss1_ssh_username=ss1_ssh_username,
                                                                ss1_ssh_password=ss1_ssh_password,
                                                                ss2_ssh_host=ss2_ssh_host,
                                                                ss2_ssh_username=ss2_ssh_username,
                                                                ss2_ssh_password=ss2_ssh_password,
                                                                ss2_client=ss2_client, ss2_client_name=ss2_client_name,
                                                                ss2_client_2=ss2_client_2,
                                                                ss2_client_2_name=ss2_client_2_name,
                                                                ca_ssh_host=main.config.get('ca.ssh_host'),
                                                                ca_ssh_username=main.config.get('ca.ssh_user'),
                                                                ca_ssh_password=main.config.get('ca.ssh_pass'),
                                                                cs_ssh_host=main.config.get('cs.ssh_host'),
                                                                cs_ssh_username=main.config.get('cs.ssh_user'),
                                                                cs_ssh_password=main.config.get('cs.ssh_pass'),
                                                                global_group=main.config.get('cs.global_group')
                                                                )
        test_func(main)
        main.tearDown()
