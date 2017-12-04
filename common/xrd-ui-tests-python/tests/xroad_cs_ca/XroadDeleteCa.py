import unittest
from main.maincontroller import MainController
import ca_management


class XroadDeleteCa(unittest.TestCase):
    """
    TRUST_14 Delete an Approved Certification Service
    RIA URL: https://jira.ria.ee/browse/XT-440, https://jira.ria.ee/browse/XTKB-69
    Depends on finishing other test(s): XroadAddCa
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_xroad_delete_ca(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC TRUST_14'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ca_name = main.config.get('ca.host')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        test_delete_ca = ca_management.test_delete_ca(case=main, ca_name=ca_name, cs_ssh_host=cs_ssh_host,
                                                      cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass,
                                                      cancel_deletion=True)

        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

            # Run the test
            test_delete_ca()
        except:
            main.log('XroadDeleteCa: Failed to delete CA')
            main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
