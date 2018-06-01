import unittest

from helpers import auditchecker, xroad
from main.maincontroller import MainController
from tests.xroad_cs_register_management_service.register_management_service import register_management_service
from tests.xroad_cs_edit_management_service.edit_management_service import edit_management_service


class XroadRegisterManagementService(unittest.TestCase):
    def test_register_management_service(self):
        """
        MEMBER_57 Register the Management Service Provider as a Security Server Client
        RIA URL: https://jira.ria.ee/browse/XTKB-134
        Depends on finishing other test(s): MEMBER_25
        Requires helper scenarios:
        X-Road version: 6.16.0
        :return:
        """
        main = MainController(self)
        main.test_number = 'UC MEMBER_57'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        server_name = main.config.get('ss1.server_name')
        register_management = register_management_service(main, server_name, try_cancel=True,
                                                          log_checker=auditchecker.AuditChecker(cs_ssh_host,
                                                                                                cs_ssh_user,
                                                                                                cs_ssh_pass))

        new_provider = xroad.split_xroad_subsystem(main.config.get('ss2.client_id'))
        new_provider['name'] = main.config.get('ss2.client_name')
        old_provider = xroad.split_xroad_subsystem(main.config.get('ss1.management_id'))
        old_provider['name'] = main.config.get('ss1.management_name')

        try:
            # Set new management service
            main.log('Set new management service')
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            edit_management_service(main, new_provider)()

            # Register new management service
            main.log('Register new management service')
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            register_management()
        except:
            main.save_exception_data()
        finally:
            try:
                main.log('Restoring old management service')
                main.reload_webdriver(cs_host, cs_user, cs_pass)
                edit_management_service(main, old_provider)()
            except:
                main.log('XroadRegisterManagementService: Failed to restore old management service')
            finally:
                main.tearDown()
