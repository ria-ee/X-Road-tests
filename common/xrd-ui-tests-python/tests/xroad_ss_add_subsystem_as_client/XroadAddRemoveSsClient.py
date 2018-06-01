import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_ss_add_subsystem_as_client import add_subsystem
from tests.xroad_ss_add_subsystem_as_client.add_subsystem import add_client_to_ss, add_client_to_ss_by_hand


class XroadAddRemoveSsClient(unittest.TestCase):
    """
    Adds and removes Security Server client to prepare environment for WSDL tests.
    Depends on finishing other test(s): MEMBER_10
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_add_remove_client(self):
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
                                                        check_errors=False, delete_added=True,
                                                        check_status=False)

        try:
            # Open webdriver
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)

            # Run the test
            test_add_client()
        except:
            main.log('XroadAddRemoveSsClient: Failed to add client')
            main.save_exception_data()
            raise
        finally:
            # Test teardown
            main.tearDown()
