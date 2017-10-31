import unittest
from main.maincontroller import MainController
import ocsp_responder


class XroadAddOcspResponder(unittest.TestCase):
    '''
    UC TRUST_10 Add/Edit OCSP Responder of a CA
    '''

    def test_xroad_add_ocsp_responder(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC TRUST_10'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ca_name = main.config.get('ca.host')
        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        ocsp_url = main.config.get('ca.ocs_host')
        ocsp_cert_filename = 'ocsp.cert.pem'

        # Get OCSP certificate from CA
        main.log('Getting CA certificates from {0}'.format(ca_ssh_host))
        ocsp_responder.ca_get_certificates(main, ca_ssh_host, ca_ssh_user, ca_ssh_pass, filenames=[ocsp_cert_filename])

        # Get local certificate path
        certificate_filename = main.get_download_path(ocsp_cert_filename)
        invalid_certificate_filename = main.get_temp_path('INFO')

        # Configure the service
        test_edit_ocsp_responder = ocsp_responder.test_edit_ocsp_responder(case=main, ca_name=ca_name,
                                                                           ocsp_url=ocsp_url, cs_ssh_host=cs_ssh_host,
                                                                           cs_ssh_user=cs_ssh_user,
                                                                           cs_ssh_pass=cs_ssh_pass,
                                                                           certificate_filename=certificate_filename,
                                                                           invalid_certificate_filename=invalid_certificate_filename)
        test_add_ocsp_responder = ocsp_responder.test_add_ocsp_responder(case=main, ca_name=ca_name, ocsp_url=ocsp_url,
                                                                         cs_ssh_host=cs_ssh_host,
                                                                         cs_ssh_user=cs_ssh_user,
                                                                         cs_ssh_pass=cs_ssh_pass,
                                                                         certificate_filename=certificate_filename,
                                                                         invalid_certificate_filename=invalid_certificate_filename)
        test_delete_ocsp_responder = ocsp_responder.test_delete_ocsp_responder(case=main, ca_name=ca_name,
                                                                               ocsp_url=ocsp_url,
                                                                               cs_ssh_host=cs_ssh_host,
                                                                               cs_ssh_user=cs_ssh_user,
                                                                               cs_ssh_pass=cs_ssh_pass)

        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

            # Test adding OCSP responder
            test_add_ocsp_responder()

            # Test editing the added OCSP responder
            test_edit_ocsp_responder()
        except:
            main.log('XroadAddOcspResponder: Failed to add OCSP responder')
            main.save_exception_data()
            try:
                # Delete service
                main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
                test_delete_ocsp_responder()
            except:
                main.log('XroadAddOcspResponder: Failed to delete added data.')
                main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
