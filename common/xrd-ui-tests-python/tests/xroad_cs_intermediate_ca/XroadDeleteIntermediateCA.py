import unittest

from helpers import auditchecker
from main.maincontroller import MainController
from tests.xroad_cs_intermediate_ca import cs_intermediate_ca


class XroadDeleteIntermediateCA(unittest.TestCase):
    """
    TRUST_13 Delete an Intermediate CA
    RIA URL: https://jira.ria.ee/browse/XTKB-187
    Depends on finishing other test(s): TRUST_12
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_xroad_intermediate_ca_deleting(self):
        main = MainController(self)

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        ca_name = main.config.get('ca.ssh_host')

        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)

        test_delete_intermediate_ca = cs_intermediate_ca.test_delete_intermediate_ca(main,
                                                                                     ca_name=ca_name,
                                                                                     log_checker=log_checker)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            test_delete_intermediate_ca()

        finally:
            main.tearDown()
