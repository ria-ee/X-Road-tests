import unittest

from helpers import ssh_client
from main.maincontroller import MainController
from tests.xroad_cs_user_logging.cs_user_logging import check_logout, check_login


class XroadCsUserLogging(unittest.TestCase):
    """
    CS_01 Log In to the Graphical User Interface
    CS_02 Log Out of the Graphical User Interface
    RIA URL: https://jira.ria.ee/browse/XT-302
    RIA URL: https://jira.ria.ee/browse/XT-303
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_cs_user_logging(self):
        main = MainController(self)
        main.test_number = 'UC CS_01/CS_02'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        sshclient = ssh_client.SSHClient(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            check_logout(main, sshclient, cs_user)
            check_login(main, sshclient, cs_user, cs_pass)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

