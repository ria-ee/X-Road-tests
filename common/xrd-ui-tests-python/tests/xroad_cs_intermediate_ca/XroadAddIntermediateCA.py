import unittest

from helpers import auditchecker
from main.maincontroller import MainController
from tests.xroad_cs_intermediate_ca import cs_intermediate_ca
from tests.xroad_cs_ocsp_responder import ocsp_responder


class XroadAddIntermediateCA(unittest.TestCase):
    """
    TRUST_12 Add an Intermediate CA to a Certification Service
    RIA URL: https://jira.ria.ee/browse/XTKB-186
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_xroad_intermediate_ca_adding(self):
        main = MainController(self)

        main.test_number = 'UC TRUST_12'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        ca_name = main.config.get('ca.name')

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')
        ca_certificate_filename = 'ca.cert.pem'
        ocsp_cert_filename = 'ocsp.cert.pem'

        ocsp_responder.ca_get_certificates(main, ca_ssh_host, ca_ssh_user, ca_ssh_pass, filenames=[ocsp_cert_filename])
        ocsp_responder.ca_get_certificates(main, ca_ssh_host, ca_ssh_user, ca_ssh_pass, [ca_certificate_filename])

        ca_certificate = main.get_download_path(ca_certificate_filename)
        ocsp_certificate = main.get_download_path(ocsp_cert_filename)
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        ocsp_url = main.config.get('ca.ocs_host')

        add_intermediate_ca = cs_intermediate_ca.test_add_intermediate_ca(main,
                                                                          ocsp_url=ocsp_url,
                                                                          ca_name=ca_name,
                                                                          ocsp_cert=ocsp_certificate,
                                                                          cert=ca_certificate,
                                                                          log_checker=log_checker)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_intermediate_ca()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_xroad_intermediate_ca_invalid_file_error(self):
        main = MainController(self)
        main.test_number = 'UC TRUST_12'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        ca_name = main.config.get('ca.name')

        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        error_cert_path = main.get_temp_path('INFO')


        add_intermediate_ca = cs_intermediate_ca.test_add_intermediate_ca(main,
                                                                          check_error=True,
                                                                          ca_name=ca_name,
                                                                          cert=error_cert_path,
                                                                          log_checker=log_checker)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            add_intermediate_ca()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
