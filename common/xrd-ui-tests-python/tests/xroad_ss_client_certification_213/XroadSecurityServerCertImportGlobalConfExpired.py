import time
import unittest

from helpers import xroad, auditchecker, ssh_client
from main.maincontroller import MainController
from tests.xroad_ss_client_certification_213 import client_certification
from tests.xroad_ss_client_certification_213.client_certification import delete_added_key


class XroadSecurityServerCertImportGlobalConfExpired(unittest.TestCase):
    """
    SS_30 3a Certificate import fails when global config has expired
    RIA URL: https://jira.ria.ee/browse/XT-343, https://jira.ria.ee/browse/XTKB-15, https://jira.ria.ee/browse/XTKB-102
    Depends on finishing other test(s): XroadSecurityServerClientRegistration
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_securityServerGlobalConfExpired(self):
        main = MainController(self)
        main.test_number = 'UC SS_30.3a'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_username = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')
        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client2_id'))
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')
        log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)

        sshclient = ssh_client.SSHClient(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
        expire_global_conf = client_certification.expire_global_conf(main, sshclient)

        test_import_cert_global_conf_expired = client_certification.test_import_cert_global_conf_expired(main,
                                                                                                         ss_host,
                                                                                                         ss_username,
                                                                                                         ss_pass,
                                                                                                         ss2_client,
                                                                                                         log_checker)

        start_xroad_conf_client = client_certification.start_xroad_conf_client(main, sshclient)
        try:
            main.reload_webdriver(ss_host, ss_username, ss_pass)
            expire_global_conf()
            main.log('SS_30 3a certificate import fails when global config has expired')
            test_import_cert_global_conf_expired()
        except:
            main.save_exception_data()
            raise
        finally:
            try:
                start_xroad_conf_client()
            except:
                main.log('Failed to start confclient')
            try:
                delete_added_key(main, ss2_client, cancel_deletion=False)
            except:
                main.log('Failed to delete added key')
            main.tearDown()
            main.log('Wait 1 minute so the configuration is up to date before running other tests')
            time.sleep(60)
