import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_cs_revoke_requests.revoke_requests import revoke_requests


class XroadRevokeRequests(unittest.TestCase):
    """
    MEMBER_39 Revoke a Registration Request
    RIA URL: https://jira.ria.ee/browse/XT-391
    RIA URL: https://jira.ria.ee/browse/XTKB-45
    RIA URL: https://jira.ria.ee/browse/XTKB-91
    Depends on finishing other test(s): XroadAddClientToMemberExtensions
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_xroad_revoke_requests(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_39'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        main.log('MEMBER_39 Revoke a Registration Request')
        main.log('Add new client to member, which will be revoked')
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            revoke_requests(main, try_cancel=True, log_checker=log_checker)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
