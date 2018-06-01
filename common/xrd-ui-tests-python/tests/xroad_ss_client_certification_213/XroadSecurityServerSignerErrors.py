import unittest

from main.maincontroller import MainController
from tests.xroad_ss_client_certification_213 import client_certification


class XroadSecurityServerSignerErrors(unittest.TestCase):
    """
    SS_28 5a Generate a key(fails)
    RIA URL: https://jira.ria.ee/browse/XT-341, https://jira.ria.ee/browse/XTKB-50
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_securityServerSignerTimedOut(self):
        main = MainController(self)
        # Set test name and number
        main.test_number = 'SS_28.5a'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_username = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        generate_key_timed_out = client_certification.test_generate_key_timed_out(main,
                                                                                  ss_host,
                                                                                  ss_username,
                                                                                  ss_pass,
                                                                                  ss2_ssh_host,
                                                                                  ss2_ssh_user,
                                                                                  ss2_ssh_pass)

        start_xroad_signer_service = client_certification.start_xroad_signer_service(main,
                                                                                     ss2_ssh_host,
                                                                                     ss2_ssh_user,
                                                                                     ss2_ssh_pass)
        try:
            generate_key_timed_out()
        except:
            main.save_exception_data()
            assert False
        finally:
            start_xroad_signer_service()
            main.tearDown()

    def test_securityServerCSRGenerationSignerTimedOut(self):
        """
            SS_29 6a Generate a csr(fails)
            RIA URL: https://jira.ria.ee/browse/XT-342, https://jira.ria.ee/browse/XTKB-51
            Depends on finishing other test(s):
            Requires helper scenarios:
            X-Road version: 6.16.0
            """
        main = MainController(self)
        # Set test name and number
        main.test_number = 'SS_29.6a'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_username = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        generate_csr_timed_out = client_certification.test_generate_csr_timed_out(main,
                                                                                  ss_host,
                                                                                  ss_username,
                                                                                  ss_pass,
                                                                                  ss2_ssh_host,
                                                                                  ss2_ssh_user,
                                                                                  ss2_ssh_pass)

        start_xroad_signer_service = client_certification.start_xroad_signer_service(main,
                                                                                     ss2_ssh_host,
                                                                                     ss2_ssh_user,
                                                                                     ss2_ssh_pass)
        try:
            generate_csr_timed_out()
        except:
            main.save_exception_data()
            raise
        finally:
            start_xroad_signer_service()
            client_certification.delete_added_key_after_service_up(main, ss_host)
            main.tearDown()
