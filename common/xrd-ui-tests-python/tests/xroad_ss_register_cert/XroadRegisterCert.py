import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_ss_client_certification_213 import client_certification
from tests.xroad_ss_register_cert.register_cert import delete_auth_cert


class XroadRegisterCert(unittest.TestCase):
    """
    MEMBER_01 Register a Security Server
    SS_34 Register an Authentication Certificate
    RIA URL: https://jira.ria.ee/browse/XTKB-71
    RIA URL: https://jira.ria.ee/browse/XTKB-110
    Depends on finishing other test(s): MEMBER_26 4a
    Requires helper scenarios: SS_29, SS_30, SS_39
    X-Road version: 6.16.0
    """
    def test_register_cert_cert_errors(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'MEMBER_01/SS_34'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')

        cs_ssh_host = main.config.get('cs.ssh_host')

        ca_name = main.config.get('ca.name')
        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        member_id = main.config.get('ss2.client2_id')
        member_name = main.config.get('ss2.client2_name')
        member = xroad.split_xroad_subsystem(member_id)
        member['name'] = member_name

        cert_path = 'temp.pem'
        auth_key_label = main.config.get('certs.ss_auth_key_label')
        dns = None
        organization = None
        if main.config.get_bool('config.harmonized_environment', False):
            dns = ss_ssh_host
            organization = main.config.get('ss2.organization')

        test_register_cert = client_certification.register_cert(main, ss_ssh_host, ss_ssh_user, ss_ssh_pass,
                                                                cs_host=cs_ssh_host, client=member,
                                                                ca_ssh_host=ca_ssh_host, ca_ssh_user=ca_ssh_user,
                                                                ca_ssh_pass=ca_ssh_pass, ca_name=ca_name,
                                                                check_inputs=True, cert_path=cert_path,
                                                                dns=dns, organization=organization)

        try:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            delete_auth_cert(main, auth_key_label)
            test_register_cert()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
