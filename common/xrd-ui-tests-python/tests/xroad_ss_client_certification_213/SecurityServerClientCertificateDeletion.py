from __future__ import absolute_import

import unittest

from helpers import xroad, auditchecker
from tests.xroad_ss_client_certification_213 import client_certification_2_1_3
from main.maincontroller import MainController


class SecurityServerClientCertificateDeletion(unittest.TestCase):
    def test_security_server_certificate_deletion(self):
        # Instatiate MainController
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.1.3-del'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('ss2.host')
        main.username = main.config.get('ss2.user')
        main.password = main.config.get('ss2.pass')
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')
        client_id = main.config.get('ss2.client2_id')

        client = xroad.split_xroad_id(client_id)
        member_name = client['code']
        member_class = client['class']

        main.log('Deleting certificate')

        try:
            # Create webdriver and go to main URL
            main.reset_webdriver(main.url, main.username, main.password)
            # Delete the key
            log_checker = auditchecker.AuditChecker(ss2_ssh_host, ss2_ssh_user, ss2_ssh_pass)
            client_certification_2_1_3.delete_added_key(main, member_name, member_class, cancel_deletion=True,
                                                        log_checker=log_checker)
        except AssertionError:
            raise
        except:
            main.log('Failed to delete certificate.')
            assert False
        finally:
            main.tearDown()