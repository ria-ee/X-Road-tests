# coding=utf-8
from __future__ import absolute_import

import time
import unittest


class TestAll(unittest.TestCase):
    print 'Testing all tests'

    # Add clients to central server (2.2.1), undo later
    def test_01_xroad_security_server_client_registration(self):
        from tests.xroad_client_registration_in_ss_221.test_main import XroadSecurityServerClientRegistration
        print '\n test_01_xroad_security_server_client_registration STARTED \n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadSecurityServerClientRegistration)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_01_xroad_security_server_client_registration FINISHED'
        del XroadSecurityServerClientRegistration
        return

    # Configure test service (2.2.2), undo later
    def test_02_xroad_configure_service(self):
        from tests.xroad_configure_service_222.test_main import XroadConfigureService
        print '\n test_02_xroad_configure_service STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadConfigureService)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_02_xroad_configure_service FINISHED'
        del XroadConfigureService
        return

    # Refresh WSDL (2.2.5), no undo necessary (according to specification, end state is the same as start state)
    def test_03_xroad_refresh_wsdl(self):
        from tests.xroad_refresh_wsdl_225.test_main import XroadRefreshWsdl
        print '\n test_03_xroad_refresh_wsdl STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadRefreshWsdl)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_03_xroad_refresh_wsdl FINISHED'
        del XroadRefreshWsdl

        return

    # Deactivate and reactivate WSDL (2.2.6), no undo necessary (specification: end state is the same as start state)
    def test_04_xroad_deactivate_wsdl(self):
        from tests.xroad_deactivate_wsdl_226.test_main import XroadDeactivateWsdl
        print '\n test_04_xroad_deactivate_wsdl STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeactivateWsdl)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_04_xroad_deactivate_wsdl FINISHED'
        del XroadDeactivateWsdl
        return

    # Using TLS locally (2.2.7), undo right away
    def test_05_xroad_Local_tls(self):
        from tests.xroad_tls_227.test_main import XroadLocalTls
        print '\n test_05_xroad_Local_tls STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadLocalTls)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_05_xroad_Local_tls FINISHED'
        del XroadLocalTls
        return

    def test_06_xroad_delete_local_tls(self):
        from tests.xroad_tls_227.test_main import XroadDeleteLocalTls
        print '\n test_06_xroad_delete_local_tls STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeleteLocalTls)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_06_xroad_delete_local_tls FINISHED'
        del XroadDeleteLocalTls
        return

    # Add central service (2.2.8), undo later
    def test_07_xroad_add_central_service(self):
        from tests.xroad_add_central_service_228.test_main import XroadAddCentralService
        print '\n test_07_xroad_add_central_service STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadAddCentralService)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_07_xroad_add_central_service FINISHED'
        del XroadAddCentralService
        return

    # Test adding access to XRoad member (2.2.9), no undo necessary (specification: end state is the same as start state)
    def test_08_xroad_member_access(self):
        from tests.xroad_member_access_229.test_main import XroadMemberAccess
        print '\n test_08_xroad_member_access STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadMemberAccess)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_08_xroad_member_access FINISHED'
        del XroadMemberAccess
        return

    # Delete central service (undo 2.2.8)
    def test_09_xroad_delete_central_service(self):
        from tests.xroad_add_central_service_228.test_main import XroadDeleteCentralService
        print '\n test_09_xroad_delete_central_service STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeleteCentralService)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_09_xroad_delete_central_service FINISHED'
        del XroadDeleteCentralService
        return

    # Delete test service (undo 2.2.2)
    def test_10_xroad_delete_service(self):
        from tests.xroad_configure_service_222.test_main import XroadDeleteService
        print '\n test_10_xroad_delete_service STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadDeleteService)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_10_xroad_delete_service FINISHED'
        del XroadDeleteService
        return

    # Delete client (undo 2.2.1)
    def test_11_xroad_security_server_client_deletion(self):
        from tests.xroad_client_registration_in_ss_221.client_registration_in_ss_deletion import \
            XroadSecurityServerClientDeletion
        print '\n test_11_xroad_security_server_client_deletion STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadSecurityServerClientDeletion)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print 'Waiting 120 seconds for changes'
        time.sleep(120)
        print '\n test_11_xroad_security_server_client_deletion FINISHED'
        del XroadSecurityServerClientDeletion
        return

    # Test 2.9.1 Testing database in central
    def test_12_xroad_changing_database_rows_with_gui_in_central_server(self):
        from tests.xroad_changing_database_rows_with_cs_gui_291.test_main import \
            XroadChangingDatabaseRowsWithGUICentralServer
        print '\n test_l2_xroad_changing_database_rows_with_gui_in_central_server STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadChangingDatabaseRowsWithGUICentralServer)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_l2_xroad_changing_database_rows_with_gui_in_central_server FINISHED'
        del XroadChangingDatabaseRowsWithGUICentralServer
        return

    # Test 2.10.1 Testing database in security server
    def test_13_xroad_changing_database_rows_with_gui_in_security_server(self):
        from tests.xroad_changing_database_rows_with_ss_gui_2101.test_main import \
            XroadChangingDatabaseRowsWithGUISecurityServer
        print '\n test_13_xroad_changing_database_rows_with_gui_in_security_server STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadChangingDatabaseRowsWithGUISecurityServer)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_13_xroad_changing_database_rows_with_gui_in_security_server FINISHED'
        del XroadChangingDatabaseRowsWithGUISecurityServer
        return

    # Test 2.11.1 Testing logging in central server
    def test_14_xroad_logging_in_central_server(self):
        from tests.xroad_logging_in_cs_2111.test_main import XroadLoggingInCentralServer
        print '\n test_14_xroad_logging_in_central_server STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadLoggingInCentralServer)
        unittest.TextTestRunner(verbosity=0).run(suite)
        print '\n test_14_xroad_logging_in_central_server FINISHED'
        del XroadLoggingInCentralServer

        return

    # Test 2.11.2
    def test_15_XroadLoggingInSecurityServer(self):
        from tests.xroad_logging_service_ss_2112.test_main import XroadLoggingInSecurityServer
        print '\n test_15_XroadLoggingInSecurityServer STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(XroadLoggingInSecurityServer)
        unittest.TextTestRunner(verbosity=0).run(suite)
        del XroadLoggingInSecurityServer
        print '\n test_15_XroadLoggingInSecurityServer FINISHED'

    # Test 2.1.3 Failures
    def test_16_security_server_client_registration_failures(self):
        from tests.xroad_ss_client_sertification_213.SecurityServerClientRegistrationFailures import \
            SecurityServerClientRegistrationFailures
        print '\n test_16_security_server_client_registration_failures STARTED\n'
        suite = unittest.TestLoader().loadTestsFromTestCase(SecurityServerClientRegistrationFailures)
        unittest.TextTestRunner(verbosity=0).run(suite)
        del SecurityServerClientRegistrationFailures
        print '\n test_16_security_server_client_registration_failures FINISHED'
