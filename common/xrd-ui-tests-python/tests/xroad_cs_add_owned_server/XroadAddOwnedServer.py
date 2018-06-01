import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_cs_add_member.add_cs_member import add_member_to_cs
from tests.xroad_cs_add_owned_server.add_owned_server import test_add_owned_server


class XroadAddOwnedServer(unittest.TestCase):
    """
    MEMBER_12 1-12, 7a Add an owned Security Server to an X-Road Member
    RIA URL: https://jira.ria.ee/browse/XTKB-71
    RIA URL: https://jira.ria.ee/browse/XTKB-90
    Depends on finishing other test(s): SS_34
    Requires helper scenarios: MEMBER_10
    X-Road version: 6.16.0
    """
    def test_a_add_owned_server_inputs(self):
        main = MainController(self, empty_downloads=False)

        main.test_number = 'MEMBER_12.a'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        member_id = main.config.get('ss2.client2_id')
        member_name = main.config.get('ss2.client2_name')
        member = xroad.split_xroad_subsystem(member_id)
        member['name'] = member_name
        cert_path = 'temp.pem'

        test_add_ss_to_cs_member_check_inputs = test_add_owned_server(main, cs_host, cs_user,
                                                                      cs_pass,
                                                                      cs_ssh_host, cs_ssh_user,
                                                                      cs_ssh_pass,
                                                                      member, cert_path=cert_path,
                                                                      check_inputs=True)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_member_to_cs(main, member)
            test_add_ss_to_cs_member_check_inputs()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_b_add_owned_server_cert_verification(self):
        main = MainController(self, empty_downloads=False)

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        member_id = main.config.get('ss2.client2_id')
        member_name = main.config.get('ss2.client2_name')
        member = xroad.split_xroad_subsystem(member_id)
        member['name'] = member_name
        cert_path = 'temp.pem'
        test_add_ss_to_cs_member_verify_cert = test_add_owned_server(main, cs_host, cs_user,
                                                                     cs_pass,
                                                                     cs_ssh_host, cs_ssh_user,
                                                                     cs_ssh_pass,
                                                                     member, cert_path=cert_path,
                                                                     verify_cert=True)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_add_ss_to_cs_member_verify_cert()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_c_add_owned_server(self):
        main = MainController(self, empty_downloads=False)

        main.test_number = 'MEMBER_12.b'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        member_id = main.config.get('ss2.client2_id')
        member_name = main.config.get('ss2.client2_name')
        member = xroad.split_xroad_subsystem(member_id)
        member['name'] = member_name
        cert_path = 'temp.pem'
        server_name = main.config.get('ss2.server_name')

        test_add_ss_to_cs_member = test_add_owned_server(main, cs_host, cs_user,
                                                         cs_pass,
                                                         cs_ssh_host, cs_ssh_user,
                                                         cs_ssh_pass,
                                                         member,
                                                         server_name=server_name,
                                                         cert_path=cert_path)

        try:
            test_add_ss_to_cs_member()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_d_add_existing_cert(self):
        main = MainController(self, empty_downloads=False)

        main.test_number = 'MEMBER_12.d'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        member_id = main.config.get('ss2.client2_id')
        member_name = main.config.get('ss2.client2_name')
        member = xroad.split_xroad_subsystem(member_id)
        member['name'] = member_name
        cert_path = 'temp.pem'
        server_name = main.config.get('ss2.server_name')

        test_add_ss_to_cs_member_check_server = test_add_owned_server(main, cs_host,
                                                                      cs_user,
                                                                      cs_pass,
                                                                      cs_ssh_host,
                                                                      cs_ssh_user,
                                                                      cs_ssh_pass,
                                                                      member,
                                                                      cert_path=cert_path,
                                                                      cert_used_already=True,
                                                                      server_name=server_name)
        try:
            test_add_ss_to_cs_member_check_server()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_e_add_existing_owned_server(self):
        main = MainController(self, empty_downloads=False)

        main.test_number = 'MEMBER_12.e'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        member_id = main.config.get('ss2.client2_id')
        member_name = main.config.get('ss2.client2_name')
        member = xroad.split_xroad_subsystem(member_id)
        member['name'] = member_name
        cert_path = 'temp.pem'
        server_name = main.config.get('ss2.server_name')

        test_add_ss_to_cs_member_check_server = test_add_owned_server(main, cs_host,
                                                                      cs_user,
                                                                      cs_pass,
                                                                      cs_ssh_host,
                                                                      cs_ssh_user,
                                                                      cs_ssh_pass,
                                                                      member,
                                                                      cert_path=cert_path,
                                                                      check_server=True,
                                                                      server_name=server_name)
        try:
            test_add_ss_to_cs_member_check_server()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()