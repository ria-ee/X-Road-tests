import unittest

from helpers import auditchecker
from main.maincontroller import MainController
from tests.xroad_global_groups_tests import global_groups_tests


class XroadEditGlobalGroupDescription(unittest.TestCase):
    """
    SERVICE_35 Edit the Description of a Global Group
    RIA URL: https://jira.ria.ee/browse/XTKB-181
    Depends on finishing other test(s): global group adding
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_edit_global_group_description(self):
        main = MainController(self)

        main.test_number = 'UC SERVICE_35'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        group = main.config.get('cs.global_group')
        new_group_description = ' {} '.format('A'*255)
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)

        test_edit_global_group_details = global_groups_tests.test_edit_global_group_description(main, group,
                                                                                                log_checker=log_checker)

        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_edit_global_group_details(new_group_description, check_inputs=True)
        except:
            main.save_exception_data()
            raise
        finally:
            main.log('Restoring global group description')
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_edit_global_group_details(group)
            main.tearDown()
