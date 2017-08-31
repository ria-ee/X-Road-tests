from __future__ import absolute_import

import unittest


class Test(unittest.TestCase):
    print('DELETE DATA')

    # Deactivate and reactivate WSDL (2.2.6), no undo necessary (specification: end state is the same as start state)
    def test_01_xroad_deactivate_wsdl(self):
        from tests.xroad_deactivate_wsdl_226.test_main import XroadDeactivateWsdl
        print('\n test_04_xroad_deactivate_wsdl STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeactivateWsdl)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print('\n test_04_xroad_deactivate_wsdl FINISHED')
        del XroadDeactivateWsdl

    def test_02_xroad_delete_local_tls(self):
        from tests.xroad_tls_227.test_main import XroadDeleteLocalTls
        print('\n test_06_xroad_delete_local_tls STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeleteLocalTls)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print('\n test_06_xroad_delete_local_tls FINISHED')
        del XroadDeleteLocalTls

    # Delete central service (undo 2.2.8)
    def test_03_xroad_delete_central_service(self):
        from tests.xroad_add_central_service_228.test_main import XroadDeleteCentralService
        print('\n test_09_xroad_delete_central_service STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeleteCentralService)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print('\n test_09_xroad_delete_central_service FINISHED')
        del XroadDeleteCentralService

    # Delete test service (undo 2.2.2)
    def test_04_xroad_delete_service(self):
        from tests.xroad_configure_service_222.test_main import XroadDeleteService
        print('\n test_10_xroad_delete_service STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeleteService)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print('\n test_10_xroad_delete_service FINISHED')
        del XroadDeleteService

    # Delete client (undo 2.2.1)
    def test_05_xroad_security_server_client_deletion(self):
        from tests.xroad_client_registration_in_ss_221.client_registration_in_ss_deletion import \
            XroadSecurityServerClientDeletion
        print('\n test_11_xroad_security_server_client_deletion STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadSecurityServerClientDeletion)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print('\n test_11_xroad_security_server_client_deletion FINISHED')
        del XroadSecurityServerClientDeletion
