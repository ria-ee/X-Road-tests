import time
import unittest

from helpers import ssh_client
from main.maincontroller import MainController
from tests.xroad_cs_ca.ca_management import configure_ca
from tests.xroad_ss_client_certification_213.client_certification import generate_csr_input_parsing, changeCAToFi


class XroadGenerateCSRInputParsing(unittest.TestCase):
    """
    SS_29 5a Generate a Certificate Signing Request input parsing
    RIA URL: https://jira.ria.ee/browse/XTKB-222
    Depends on finishing other test(s): MEMBER_01
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_generate_csr_input_parsing(self):
        main = MainController(self)

        main.test_number = 'UC SS_29.5a'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')
        sshclient = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ca_name = main.config.get('ca.name')
        profile_class = main.config.get('ca.profile_class')

        test_generate_csr_input_parsing = generate_csr_input_parsing(main)
        ca_driver = None

        try:
            if not main.config.get_bool('config.harmonized_environment', False):
                ca_driver = changeCAToFi(main, cs_host, cs_user, cs_pass, ca_name, sshclient)
            main.reset_webdriver(ss_host, ss_user, ss_pass, close_previous=False)
            test_generate_csr_input_parsing()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
            if ca_driver:
                main.driver = ca_driver
                if not main.config.get_bool('config.harmonized_environment', False):
                    configure_ca(main, auth_only_certs=None,
                                 certificate_classpath=profile_class)
                sshclient.exec_command('service xroad-confclient restart', sudo=True)
                sshclient.close()
                time.sleep(120)
                main.tearDown()
