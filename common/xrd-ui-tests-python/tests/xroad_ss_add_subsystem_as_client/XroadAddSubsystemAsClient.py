import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_ss_add_subsystem_as_client import add_subsystem
from tests.xroad_ss_add_subsystem_as_client.add_subsystem import add_client_to_ss, add_client_to_ss_by_hand


class XroadAddSubsystemAsClient(unittest.TestCase):
    """
    MEMBER_47 Add a Client to the Security Server
    RIA URL:https://jira.ria.ee/browse/XT-399
    Depends on finishing other test(s): MEMBER_10
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_a_add_subsystem_as_client(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_47.a'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')
        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')
        ss1_client_2_name = main.config.get('ss1.client2_name')
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        sync_retry = 30
        sync_timeout = 120
        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_name = main.config.get('ss1.client_name')
        ss_1_client = {'name': ss1_client_name, 'class': ss1_client['class'], 'code': ss1_client['code'],
                       'subsystem_code': ss1_client['subsystem']}
        ss_1_client_2 = {'name': ss1_client_2_name, 'class': ss1_client_2['class'], 'code': ss1_client_2['code'],
                         'subsystem_code': ss1_client_2['subsystem']}

        ss2_client_2 = xroad.split_xroad_id(main.config.get('ss2.client2_id'))
        ss2_client_2_name = main.config.get('ss2.client2_name')
        ss_2_client_2 = {'name': ss2_client_2_name, 'class': ss2_client_2['class'], 'code': ss2_client_2['code'],
                         'subsystem_code': ss2_client_2['subsystem']}

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            add_client_to_ss(main, ss_1_client_2, retry_interval=sync_retry, retry_timeout=sync_timeout,
                             step='MEMBER_47(1): ')

            main.reload_webdriver(ss_host, ss_user, ss_pass)
            add_client_to_ss(main, ss_1_client, retry_interval=sync_retry, retry_timeout=sync_timeout,
                             step='MEMBER_47(2): ')

            main.reload_webdriver(ss2_host, ss2_user, ss2_pass)
            add_client_to_ss(main, ss_2_client_2, step='MEMBER_47(3): ')
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_b_add_subsystem_as_client_by_hand(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_47.b'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')
        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')
        log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        management_wsdl_url = main.config.get('wsdl.management_service_wsdl_url')
        management_client = xroad.split_xroad_id(main.config.get('ss1.management_id'))
        management_client_id = xroad.get_xroad_subsystem(management_client)
        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        ss2_client_name = main.config.get('ss2.client_name')
        ss_2_client = {'name': ss2_client_name, 'class': ss2_client['class'], 'code': ss2_client['code'],
                       'subsystem_code': ss2_client['subsystem']}
        fail_client = ss_2_client.copy()
        fail_client['code'] = 'asd123'
        try:
            main.reload_webdriver(ss2_host, ss2_user, ss2_pass)
            add_client_to_ss_by_hand(main, ss_2_client, log_checker=log_checker, cancel_registration=True)

            main.reload_webdriver(ss2_host, ss2_user, ss2_pass)
            add_client_to_ss_by_hand(main, fail_client, check_send_errors=True, log_checker=log_checker,
                                     sec_1_host=ss_host, sec_1_user=ss_user, sec_1_pass=ss_pass,
                                     management_client_id=management_client_id, management_wsdl_url=management_wsdl_url)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_c_add_client_input_errors(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_47.c'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client_id = main.config.get('ss2.client_id')
        client_name = main.config.get('ss2.client_name')

        existing_client = xroad.split_xroad_subsystem(main.config.get('ss2.client2_id'))
        existing_client['name'] = main.config.get('ss2.client2_name')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')
        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        # Configure the service
        test_add_client = add_subsystem.test_add_client(case=main,
                                                        client_name=client_name,
                                                        client_id=client_id, duplicate_client=existing_client,
                                                        log_checker=log_checker,
                                                        check_errors=True
                                                        )

        try:
            # Open webdriver
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            # Run the test
            test_add_client()
        except:
            main.log('XroadAddClient: Failed to add client')
            main.save_exception_data()
            raise
        finally:
            # Test teardown
            main.tearDown()
'''
    def test_d_add_remove_client(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC MEMBER_47'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        client_id = main.config.get('ss2.client_id')
        client_name = main.config.get('ss2.client_name')

        # Configure the service
        test_add_client = add_subsystem.test_add_client(case=main,
                                                        client_name=client_name,
                                                        client_id=client_id,
                                                        check_errors=False, delete_added=True
                                                        )

        try:
            # Open webdriver
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            # Run the test
            test_add_client()
        except:
            main.log('XroadAddClient: Failed to add client')
            main.save_exception_data()
            raise
        finally:
            # Test teardown
            main.tearDown()
'''