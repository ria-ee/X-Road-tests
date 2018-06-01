import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_ss_client_certification_213 import client_certification


class XroadCertifyClient(unittest.TestCase):
    """
    SS_28 Generate a Key
    SS_29 Generate a Certificate Signing Request for a Key
    SS_30 Import a Certificate from Local File System
    RIA URL: https://jira.ria.ee/browse/XT-341, https://jira.ria.ee/browse/XTKB-85
    RIA URL: https://jira.ria.ee/browse/XT-342, https://jira.ria.ee/browse/XTKB-86
    RIA URL: https://jira.ria.ee/browse/XT-343
    Depends on finishing other test(s): MEMBER_47
    Requires helper scenarios: client_certification
    X-Road version: 6.16.0
    """

    def test_certify_client(self):
        main = MainController(self)
        main.test_number = 'UC SS_28/29/30'
        main.test_name = self.__class__.__name__

        ss1_host = main.config.get('ss1.host')
        ss1_user = main.config.get('ss1.user')
        ss1_pass = main.config.get('ss1.pass')
        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')
        ss2_ssh_host = main.config.get('ss2.ssh_host')
        ss2_ssh_user = main.config.get('ss2.ssh_user')
        ss2_ssh_pass = main.config.get('ss2.ssh_pass')

        ss1_client = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        ss1_client_2 = xroad.split_xroad_id(main.config.get('ss1.client2_id'))
        ss2_client = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        try:
            main.reload_webdriver(ss1_host, ss1_user, ss1_pass)
            client_certification.test_generate_csr_and_import_cert(client_code=ss1_client_2['code'],
                                                                   client_class=ss1_client_2['class'])(main)

            main.reload_webdriver(ss1_host, ss1_user, ss1_pass)
            client_certification.test_generate_csr_and_import_cert(client_code=ss1_client['code'],
                                                                   client_class=ss1_client['class'])(main)

            main.reload_webdriver(ss2_host, ss2_user, ss2_pass)
            client_certification.test_generate_csr_and_import_cert(ss2_ssh_host=ss2_ssh_host,
                                                                   ss2_ssh_user=ss2_ssh_user,
                                                                   ss2_ssh_pass=ss2_ssh_pass,
                                                                   client_code=ss2_client['code'],
                                                                   client_class=ss2_client['class'])(main)
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
