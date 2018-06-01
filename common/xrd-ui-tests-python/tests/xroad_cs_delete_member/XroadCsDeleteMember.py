import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_changing_database_rows_with_cs_gui_291.changing_database_rows_with_cs_gui import USERNAME
from tests.xroad_cs_delete_member import deleting_in_cs
from tests.xroad_cs_delete_member.deleting_in_cs import remove_member


class XroadCsDeleteMember(unittest.TestCase):
    """
    MEMBER_26 Delete an X-Road Member
    RIA URL: https://jira.ria.ee/browse/XTKB-215
    RIA URL: https://jira.ria.ee/browse/XT-378
    RIA URL: https://jira.ria.ee/browse/XTKB-41
    Depends on finishing other test(s): MEMBER_14
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_a_delete_member(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_26.a'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        ss1_client_2_name = main.config.get('ss1.client2_name')
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        ss_1_client_2 = {'name': ss1_client_2_name, 'class': ss1_client_2['class'], 'code': ss1_client_2['code'],
                         'subsystem_code': ss1_client_2['subsystem']}

        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            remove_member(main, ss_1_client_2, try_cancel=True, log_checker=log_checker)
        except:
            main.save_exception_data()
            assert False
        finally:
            main.tearDown()

    def test_b_xroad_cs_delete_member_with_subsystem(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_26.b'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        cs_host = main.config.get('cs.host')
        cs_username = main.config.get('cs.user')
        cs_password = main.config.get('cs.pass')

        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        ss2_client_name = main.config.get('ss2.client_name')
        cs_identifier = main.config.get('cs.identifier')
        ss_2_client = {'name': ss2_client_name, 'class': ss2_client['class'], 'code': ss2_client['code'],
                       'subsystem_code': ss2_client['subsystem'], 'identifier': cs_identifier}
        try:
            main.reload_webdriver(cs_host, cs_username, cs_password)
            remove_member(main, ss_2_client, member_has_subsystem_as_client=True)
        except:
            main.save_exception_data()
            assert False
        finally:
            main.tearDown()

    def test_c_xroad_cs_delete_member_with_global_group(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_26.c'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        client_id = main.config.get('ss1.client2_id')
        client_name = main.config.get('ss1.client2_name')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name

        cs_host = main.config.get('cs.host')
        cs_username = main.config.get('cs.user')
        cs_password = main.config.get('cs.pass')
        user = {USERNAME: cs_username}
        test_group_name = main.config.get('cs.global_group')
        add_member_and_add_to_group = deleting_in_cs.test_deleting_member_with_global_group(
            client,
            user,
            test_group_name)

        try:
            main.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
            add_member_and_add_to_group(main)
            main.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
            remove_member(main, client, group=test_group_name)
        except:
            main.save_exception_data()
            assert False
        finally:
            main.tearDown()
