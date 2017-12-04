# coding=utf-8
import unittest
from main.maincontroller import MainController
import del_management
from helpers import xroad
from tests.xroad_client_registration_in_ss_221.client_registration_in_ss import approve_requests
from view_models import cs_security_servers

"""
 UC MEMBER_16: Create a Security Server Client Deletion Request
 RIA URL: https://jira.ria.ee/browse/XTKB-195
 Depends on finishing other test(s):
 Requires helper scenarios:
 X-Road version: 6.16.0
 """


class XroadMemberSsClientDeletionRequest(unittest.TestCase):
    def test_xroad_member_request(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_16'
        main.log('TEST:  UC MEMBER_16: Create a Security Server Client Deletion Request')

        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_username = main.config.get('cs.user')
        cs_password = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        ss1_code = main.config.get('ss1.server_name')
        client_server_id = xroad.split_xroad_id(main.config.get('ss1.server_id'))
        client_subsystem = client_server_id['subsystem']
        client_instance = client_server_id['instance']
        client_code = client_server_id['code']
        client_class = client_server_id['class']
        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')
        random_code = cs_security_servers.randomword(6)

        member_add_subsystem = del_management.test_add_subsystem_to_member(case=main, ss1_code=ss1_code,
                                                                           subsystem_text=random_code)

        server_client_add_subsystem = del_management.test_add_subsystem_to_server_client(case=main, ss1_code=ss1_code,
                                                                                         random_code=random_code)

        add_client_to_ss = del_management.test_add_client_to_ss_by_hand(case=main, client_class=client_class,
                                                                        client_code=client_code,
                                                                        random_code=random_code)

        delete_client = del_management.test_ss_client_deletion(case=main, cs_ssh_host=cs_ssh_host,
                                                               cs_ssh_user=cs_ssh_user,
                                                               cs_ssh_pass=cs_ssh_pass, ss1_code=ss1_code,
                                                               client_subsystem=client_subsystem,
                                                               client_instance=client_instance, client_code=client_code,
                                                               client_class=client_class,
                                                               random_code=random_code)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)

            '''Add subsystem to member'''
            member_add_subsystem()

            '''Add subsystem to server client'''
            server_client_add_subsystem()
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            '''Add client to ss'''
            add_client_to_ss()

            '''Open webdriver'''
            main.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
            '''Approve requests'''
            approve_requests(main)
            '''Security Server Client Deletion Request '''
            delete_client()


        except:
            main.log('XroadMemberSsClientDeletionRequest: Failed to Create a Security Server Client Deletion Request')
            main.save_exception_data()
            assert False

        finally:
            '''Open webdriver'''
            main.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
            del_management.delete_member(main, ss1_code=ss1_code, random_code=random_code)

            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            del_management.ss_delete_client(main, client_instance=client_instance,
                                            client_code=client_code,
                                            client_class=client_class,
                                            random_code=random_code)

            '''Test teardown'''
            main.tearDown()
