import unittest

from helpers import auditchecker
from main.maincontroller import MainController
from tests.xroad_ss_user_logging.ss_user_logging import check_login, check_logout


class XroadSSUserLogging(unittest.TestCase):
    """
    SS_01 Log In to the Graphical User Interface
    SS_02 Log Out of the Graphical User Interface
    RIA URL: https://jira.ria.ee/browse/XT-314
    RIA URL: https://jira.ria.ee/browse/XT-315
    """
    def test_ss_user_logging(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC SS_01/SS_02'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            check_logout(main, log_checker=log_checker)
            check_login(main, ss_user, ss_pass, log_checker=log_checker)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
