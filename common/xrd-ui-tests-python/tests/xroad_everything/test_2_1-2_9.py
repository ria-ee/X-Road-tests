from __future__ import absolute_import

import unittest


class Test(unittest.TestCase):
    print('Testing 2.1-2.9 tests')

    # Add clients to central server (2.2.1), undo later
    def test_01_xroad_security_server_client_registration(self):
        from tests.xroad_client_registration_in_ss_221.test_main import XroadSecurityServerClientRegistration
        print('\n test_01_xroad_security_server_client_registration STARTED \n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadSecurityServerClientRegistration)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_01_xroad_security_server_client_registration FINISHED')
        del XroadSecurityServerClientRegistration

    # Configure test service (2.2.2), undo later
    def test_02_xroad_configure_service(self):
        from tests.xroad_configure_service_222.test_main import XroadConfigureService
        print('\n test_02_xroad_configure_service STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadConfigureService)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_02_xroad_configure_service FINISHED')
        del XroadConfigureService

    # Refresh WSDL (2.2.5), no undo necessary (according to specification, end state is the same as start state)
    def test_03_xroad_refresh_wsdl(self):
        from tests.xroad_refresh_wsdl_225.test_main import XroadRefreshWsdl
        print('\n test_03_xroad_refresh_wsdl STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadRefreshWsdl)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_03_xroad_refresh_wsdl FINISHED')
        del XroadRefreshWsdl

    # Deactivate and reactivate WSDL (2.2.6), no undo necessary (specification: end state is the same as start state)
    def test_04_xroad_deactivate_wsdl(self):
        from tests.xroad_deactivate_wsdl_226.test_main import XroadDeactivateWsdl
        print('\n test_04_xroad_deactivate_wsdl STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeactivateWsdl)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_04_xroad_deactivate_wsdl FINISHED')
        del XroadDeactivateWsdl

    # Using TLS locally (2.2.7), undo right away
    def test_05_xroad_Local_tls(self):
        from tests.xroad_tls_227.test_main import XroadLocalTls
        print('\n test_05_xroad_Local_tls STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadLocalTls)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_05_xroad_Local_tls FINISHED')
        del XroadLocalTls

    def test_06_xroad_delete_local_tls(self):
        from tests.xroad_tls_227.test_main import XroadDeleteLocalTls
        print('\n test_06_xroad_delete_local_tls STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeleteLocalTls)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_06_xroad_delete_local_tls FINISHED')
        del XroadDeleteLocalTls

    # Add central service (2.2.8), undo later
    def test_07_xroad_add_central_service(self):
        from tests.xroad_add_central_service_228.test_main import XroadAddCentralService
        print('\n test_07_xroad_add_central_service STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadAddCentralService)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_07_xroad_add_central_service FINISHED')
        del XroadAddCentralService

    # Test adding access to XRoad member (2.2.9), no undo necessary (specification: end state is the same as start state)
    def test_08_xroad_member_access(self):
        from tests.xroad_member_access_229.test_main import XroadMemberAccess
        print('\n test_08_xroad_member_access STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadMemberAccess)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_08_xroad_member_access FINISHED')
        del XroadMemberAccess

    # Delete central service (undo 2.2.8)
    def test_09_xroad_delete_central_service(self):
        from tests.xroad_add_central_service_228.test_main import XroadDeleteCentralService
        print('\n test_09_xroad_delete_central_service STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeleteCentralService)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_09_xroad_delete_central_service FINISHED')
        del XroadDeleteCentralService

    # Delete test service (undo 2.2.2)
    def test_10_xroad_delete_service(self):
        from tests.xroad_configure_service_222.test_main import XroadDeleteService
        print('\n test_10_xroad_delete_service STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeleteService)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_10_xroad_delete_service FINISHED')
        del XroadDeleteService

    # Delete client (undo 2.2.1)
    def test_11_xroad_security_server_client_deletion(self):
        from tests.xroad_client_registration_in_ss_221.client_registration_in_ss_deletion import \
            XroadSecurityServerClientDeletion
        print('\n test_11_xroad_security_server_client_deletion STARTED\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadSecurityServerClientDeletion)
        ret = unittest.TextTestRunner(verbosity=0).run(suite)
        if len(ret.failures) > 0:
            assert False
        elif len(ret.errors) > 0:
            assert False
        print('\n test_11_xroad_security_server_client_deletion FINISHED')
        del XroadSecurityServerClientDeletion
