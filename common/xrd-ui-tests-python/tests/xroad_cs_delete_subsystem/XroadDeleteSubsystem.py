import unittest

from helpers import auditchecker, xroad
from main.maincontroller import MainController
from tests.xroad_cs_delete_subsystem.delete_subsystem import test_delete_subsystem


class XroadDeleteSubsystem(unittest.TestCase):
    """
    MEMBER_14 Delete an X-Road Member's Subsystem
    RIA URL: https://jira.ria.ee/browse/XT-366
    RIA URL: https://jira.ria.ee/browse/XTKB-131
    Depends on finishing other test(s): MEMBER_52, SERVICE_33
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_delete_subsystem_with_global_group(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_14'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        global_group = main.config.get('cs.global_group_1')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_name = main.config.get('ss1.client_name')
        ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                       'subsystem_code': ss1_client['subsystem']}
        test_delete_subsystem_global_group = test_delete_subsystem(main, ss_1_client, global_group, try_cancel=True,
                                                                   log_checker=log_checker)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_delete_subsystem_global_group()
        except:
            main.save_exception_data()
            assert False
        finally:
            main.tearDown()

    def test_delete_subsystem(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_14'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ss2_client_2 = xroad.split_xroad_id(main.config.get('ss2.client2_id'))
        ss2_client_2_name = main.config.get('ss2.client2_name')
        ss_2_client_2 = {'name': ss2_client_2_name, 'class': ss2_client_2['class'], 'code': ss2_client_2['code'],
                         'subsystem_code': ss2_client_2['subsystem']}
        delete_subsystem = test_delete_subsystem(main, ss_2_client_2)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            delete_subsystem()
        except:
            main.save_exception_data()
            assert False
        finally:
            main.tearDown()
