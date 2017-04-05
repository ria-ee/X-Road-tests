# coding=utf-8
import unittest

import add_central_service_2_2_8
from tests.xroad_add_to_acl_218 import add_to_acl_2_1_8
from tests.xroad_configure_service_222 import configure_service_2_2_2
from main.maincontroller import MainController
from helpers import xroad


class XroadAddCentralService(unittest.TestCase):
    def test_add_central_service_2_2_8(self):
        MainController.close_webdriver = True
        MainController.driver_autostart = False
        main = MainController(self)
        # main.start_mock_service()

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')

        requester = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        provider = xroad.split_xroad_id(main.config.get('services.central_service_provider_id'))
        provider_2 = xroad.split_xroad_id(main.config.get('services.central_service_provider_2_id'))

        service_name = main.config.get('services.test_service')
        central_service_name = main.config.get('services.central_service')

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        wait_sync_retry_delay = main.config.get('services.request_sync_delay')
        sync_max_seconds = main.config.get('services.request_sync_timeout')

        requester_id = xroad.get_xroad_subsystem(requester)

        # Configure the service
        add_central_service = add_central_service_2_2_8.test_add_central_service(main, provider=provider,
                                                                                 central_service_name=central_service_name,
                                                                                 sync_max_seconds=sync_max_seconds,
                                                                                 wait_sync_retry_delay=wait_sync_retry_delay)

        # Configure a new service
        configure_service = configure_service_2_2_2.test_configure_service(main, client=provider_2,
                                                                           service_name=service_name,
                                                                           check_add_errors=False,
                                                                           check_edit_errors=False,
                                                                           check_parameter_errors=False)

        # Add the subject to ACL
        configure_service_acl = add_to_acl_2_1_8.test_add_subjects(main, client=provider_2, wsdl_url=wsdl_url,
                                                                   service_name=service_name,
                                                                   service_subjects=[requester_id],
                                                                   remove_data=False, allow_remove_all=False)
        # Enable the service
        enable_service = configure_service_2_2_2.test_enable_service(main, client=provider_2, wsdl_url=wsdl_url)

        delete_service = configure_service_2_2_2.test_delete_service(main, client=provider_2, wsdl_url=wsdl_url)

        # Configure the service
        edit_central_service = add_central_service_2_2_8.test_edit_central_service(main,
                                                                                   provider=provider_2,
                                                                                   central_service_name=central_service_name,
                                                                                   sync_max_seconds=sync_max_seconds,
                                                                                   wait_sync_retry_delay=wait_sync_retry_delay)

        delete_central_service = add_central_service_2_2_8.test_delete_central_service(main,
                                                                                       central_service_name=central_service_name,
                                                                                       sync_max_seconds=sync_max_seconds,
                                                                                       wait_sync_retry_delay=wait_sync_retry_delay)


        try:
            main.log('XroadAddCentralService: Add central service')
            # Set Central Server UI
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            add_central_service()

            main.log('XroadAddCentralService: Configure service parameters')
            # Set Security Server 2 and configure service parameters
            main.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)
            configure_service()

            main.log('XroadAddCentralService: Configure service ACL')
            # Go to SS2 main page (no need to login again) and configure ACL
            main.reload_webdriver(url=ss2_host)
            configure_service_acl()

            main.log('XroadAddCentralService: Enable service')
            # Go to SS2 main page (no need to login again) and enable service
            main.reload_webdriver(url=ss2_host)
            enable_service()

            main.log('XroadAddCentralService: Edit central service')
            # Go to CS main page (login again if necessary) and edit the central service
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            edit_central_service()

        except:
            main.log('XroadAddCentralService: Error, undoing changes')
            try:
                # Go to CS main page (login again if necessary) and edit the central service
                main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

                try:
                    # Delete central service
                    delete_central_service()
                except:
                    main.log('XroadAddCentralService: Error deleting central service')
                    raise
                finally:
                    try:
                        # Go to SS2 main page (re-login if necessary) and delete the newly created service
                        main.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)
                        delete_service()
                    except:
                        main.log('XroadAddCentralService: Error deleting security server service')
                        raise
            except:
                raise
        finally:
            # Test teardown
            main.tearDown()


class XroadDeleteCentralService(unittest.TestCase):
    def test_add_central_service_2_2_8(self):
        MainController.close_webdriver = True
        MainController.driver_autostart = False
        main = MainController(self)
        main.start_mock_service()

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ss2_host = main.config.get('ss2.host')
        ss2_user = main.config.get('ss2.user')
        ss2_pass = main.config.get('ss2.pass')

        provider_2 = xroad.split_xroad_id(main.config.get('services.central_service_provider_2_id'))

        central_service_name = main.config.get('services.central_service')

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        wait_sync_retry_delay = main.config.get('services.request_sync_delay')
        sync_max_seconds = main.config.get('services.request_sync_timeout')

        delete_service = configure_service_2_2_2.test_delete_service(main, client=provider_2, wsdl_url=wsdl_url)

        delete_central_service = add_central_service_2_2_8.test_delete_central_service(main,
                                                                                       central_service_name=central_service_name,
                                                                                       sync_max_seconds=sync_max_seconds,
                                                                                       wait_sync_retry_delay=wait_sync_retry_delay)

        main.tear_down = True

        try:
            try:
                # Go to CS main page (login again if necessary) and edit the central service
                main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

                # Delete central service
                delete_central_service()
            except:
                main.log('XroadDeleteCentralService: Failed to delete central service')
                raise
            finally:
                try:
                    # Go to SS2 main page (re-login if necessary) and delete the newly created service
                    main.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)
                    delete_service()
                except:
                    main.log('XroadDeleteCentralService: failed to delete security server service')
                    raise
        finally:
            # Test teardown
            main.tearDown()
