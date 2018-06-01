import unittest

from helpers import auditchecker, xroad
from main.maincontroller import MainController
from tests.xroad_cs_edit_management_service.edit_management_service import edit_management_service


class XroadEditManagementService(unittest.TestCase):
    """
    MEMBER_33 Change the Management Services' Provider
    RIA URL: https://jira.ria.ee/browse/XT-385, https://jira.ria.ee/browse/XTKB-135
    Depends on finishing other test(s): MEMBER_57
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_edit_management_service(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_33'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        new_provider = xroad.split_xroad_subsystem(main.config.get('ss1.client_id'))
        new_provider['name'] = main.config.get('ss1.client_name')
        old_provider = xroad.split_xroad_subsystem(main.config.get('ss1.management_id'))
        old_provider['name'] = main.config.get('ss1.management_name')

        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)

        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            edit_management_service(main, new_provider, log_checker=log_checker)()
        except:
            main.save_exception_data()
            raise
        finally:
            main.log('Restore old management service')
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            edit_management_service(main, old_provider, log_checker=log_checker)()
            main.tearDown()
