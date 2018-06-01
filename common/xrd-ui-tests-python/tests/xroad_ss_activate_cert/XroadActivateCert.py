import unittest

from main.maincontroller import MainController
from tests.xroad_ss_activate_cert.activate_cert import activate_cert


class XroadActivateCert(unittest.TestCase):
    """
    SS_32 Activate a Certificate
    RIA URL: https://jira.ria.ee/browse/XTKB-71
    RIA URL: https://jira.ria.ee/browse/XTKB-90
    RIA URL: https://jira.ria.ee/browse/XTKB-106
    Depends on finishing other test(s): MEMBER_12
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_activate_cert(self):
        main = MainController(self)
        main.test_number = 'UC SS_32'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        test_activate_cert = activate_cert(main, ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass, registered=False)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_activate_cert()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()