import unittest
from main.maincontroller import MainController
import ocsp_responder


class XroadDeleteOcspResponder(unittest.TestCase):
    '''
    UC TRUST_11 Delete an OCSP Responder of a CA
    '''

    def test_xroad_delete_ocsp_responder(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'UC TRUST_11'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ca_name = main.config.get('ca.host')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        ocsp_url = main.config.get('ca.ocs_host')

        # Configure the service
        test_delete_ocsp_responder = ocsp_responder.test_delete_ocsp_responder(case=main, ca_name=ca_name,
                                                                               ocsp_url=ocsp_url,
                                                                               cs_ssh_host=cs_ssh_host,
                                                                               cs_ssh_user=cs_ssh_user,
                                                                               cs_ssh_pass=cs_ssh_pass)

        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

            # Test deleting OCSP responder
            test_delete_ocsp_responder()
        except:
            main.log('XroadDeleteOcspResponder: Failed to delete OCSP responder')
            main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
