import time
import unittest

from helpers import xroad, auditchecker
from main.maincontroller import MainController
from tests.xroad_ss_client_certification_213 import client_certification_2_1_3
from tests.xroad_ss_client_certification_213.client_certification_2_1_3 import delete_added_key


class XroadSecurityServerCertImportGlobalConfExpired(unittest.TestCase):
    """
    SS_30 3a Certificate import fails when global config has expired
    RIA URL: https://jira.ria.ee/browse/XTKB-15
    RIA URL: https://jira.ria.ee/browse/XTKB-102
    Depends on finishing other test(s): client_registration
    Requires helper scenarios:
    X-Road version: 6.16
    """

    def test_securityServerGlobalConfExpired(self):
        main = MainController(self)
        ss_host = main.config.get('ss2.host')
        ss_username = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')
        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client2_id'))
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')
        log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)

        expire_global_conf = client_certification_2_1_3.expire_global_conf(main,
                                                                           ss2_ssh_host,
                                                                           ss2_ssh_user,
                                                                           ss2_ssh_pass)
        test_import_cert_global_conf_expired = client_certification_2_1_3.test_import_cert_global_conf_expired(main,
                                                                                                               ss_host,
                                                                                                               ss_username,
                                                                                                               ss_pass,
                                                                                                               ss2_client,
                                                                                                               log_checker)

        start_xroad_conf_client = client_certification_2_1_3.start_xroad_conf_client(main,
                                                                                     ss2_ssh_host,
                                                                                     ss2_ssh_user,
                                                                                     ss2_ssh_pass)
        try:
            expire_global_conf()
            main.log('SS_30 3a certificate import fails when global config has expired')
            test_import_cert_global_conf_expired()
        except:
            assert False
        finally:
            start_xroad_conf_client()
            delete_added_key(main, client_code=ss2_client['code'], client_class=ss2_client['class'],
                             cancel_deletion=False)
            main.tearDown()
            main.log('Wait 1 minute so the configuration is up to date before running other tests')
            time.sleep(60)
