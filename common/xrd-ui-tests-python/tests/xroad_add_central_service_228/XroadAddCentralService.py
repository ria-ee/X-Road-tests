# coding=utf-8
import unittest

import add_central_service
from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_add_to_acl_218 import add_to_acl
from tests.xroad_configure_service_222 import configure_service


class XroadAddCentralService(unittest.TestCase):
    """
    SERVICE_41 1-2, 3-7, 4a, 5a Add a Central Service
    SERVICE_42 1-2, 4-6, 3a, 4a Edit the Implementing Service of a Central Service
    SERVICE_43 Delete a Central Service
    RIA URL: https://jira.ria.ee/browse/XT-298, https://jira.ria.ee/browse/XTKB-29, https://jira.ria.ee/browse/XTKB-76
    RIA URL: https://jira.ria.ee/browse/XT-299, https://jira.ria.ee/browse/XTKB-30
    RIA URL: https://jira.ria.ee/browse/XT-300, https://jira.ria.ee/browse/XTKB-35
    Depends on finishing other test(s): XroadSecurityServerClientRegistration, XroadConfigureService
    Requires helper scenarios: xroad_configure_service_222, xroad_add_to_acl_218
    X-Road version: 6.16.0
    """

    def test_add_central_service_2_2_8(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SERVICE_41 / SERVICE_42'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

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
        service_url = main.config.get('services.test_service_url')

        requester_id = xroad.get_xroad_subsystem(requester)

        # Configure the service
        add_central_service = add_central_service.test_add_central_service(main, provider=provider,
                                                                           requester=requester,
                                                                           central_service_name=central_service_name,
                                                                           sync_max_seconds=sync_max_seconds,
                                                                           wait_sync_retry_delay=wait_sync_retry_delay,
                                                                           try_same_code_twice=True,
                                                                           try_not_existing_member=True,
                                                                           cs_ssh_host=cs_ssh_host,
                                                                           cs_ssh_user=cs_ssh_user,
                                                                           cs_ssh_pass=cs_ssh_pass)

        # Configure a new service
        configure_service = configure_service.test_configure_service(main, client=provider_2,
                                                                     service_name=service_name,
                                                                     check_add_errors=False,
                                                                     check_edit_errors=False,
                                                                     service_url=service_url,
                                                                     check_parameter_errors=False)

        # Add subject to ACL
        configure_service_acl = add_to_acl.test_add_subjects(main, client=provider_2, wsdl_url=wsdl_url,
                                                             service_name=service_name,
                                                             service_subjects=[requester_id],
                                                             remove_data=False, allow_remove_all=False)
        # Enable new service
        enable_service = configure_service.test_enable_service(main, client=provider_2, wsdl_url=wsdl_url)

        # Delete new service (undo the changes we made)
        delete_service = configure_service.test_delete_service(main, client=provider_2, wsdl_url=wsdl_url)

        # Configure central service
        edit_central_service = add_central_service.test_edit_central_service(main,
                                                                             provider=provider_2,
                                                                             requester=requester,
                                                                             central_service_name=central_service_name,
                                                                             sync_max_seconds=sync_max_seconds,
                                                                             wait_sync_retry_delay=wait_sync_retry_delay,
                                                                             cs_ssh_host=cs_ssh_host,
                                                                             cs_ssh_user=cs_ssh_user,
                                                                             cs_ssh_pass=cs_ssh_pass,
                                                                             try_not_existing_provider=True)

        # Delete central service (undo changes we made)
        delete_central_service = add_central_service.test_delete_central_service(main,
                                                                                 cs_ssh_host=cs_ssh_host,
                                                                                 cs_ssh_user=cs_ssh_user,
                                                                                 cs_ssh_pass=cs_ssh_pass,
                                                                                 central_service_name=central_service_name,
                                                                                 provider=provider_2,
                                                                                 requester=requester,
                                                                                 sync_max_seconds=sync_max_seconds,
                                                                                 wait_sync_retry_delay=wait_sync_retry_delay)

        try:
            # Add central service
            main.log('XroadAddCentralService: Add central service')
            # Set Central Server UI
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            add_central_service()

            # Configure new provider for central service
            main.log('XroadAddCentralService: Configure service parameters (using xroad_configure_service_222)')
            # Set Security Server 2 and configure service parameters
            main.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)
            configure_service()

            # Configure new provider for central service (set access using ACL)
            main.log('XroadAddCentralService: Configure service ACL (using xroad_add_to_acl_218)')
            # Go to SS2 main page (no need to login again) and configure ACL
            main.reload_webdriver(url=ss2_host)
            configure_service_acl()

            # Eenable the new provider service
            main.log('XroadAddCentralService: Enable service (using xroad_configure_service_222)')
            # Go to SS2 main page (no need to login again) and enable service
            main.reload_webdriver(url=ss2_host)
            enable_service()

            # Edit and test the central service with the new provider
            main.log('XroadAddCentralService: Edit central service')
            # Go to CS main page (login again if necessary) and edit the central service
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            edit_central_service()

        except Exception:
            main.log('XroadAddCentralService: Error, undoing changes')
            main.save_exception_data()
            try:
                # Go to CS main page (login again if necessary) and edit the central service
                main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

                try:
                    # Delete central service
                    delete_central_service()
                except:
                    main.log('XroadAddCentralService: Error deleting central service')
                    main.save_exception_data()
                    raise
                finally:
                    try:
                        # Go to SS2 main page (re-login if necessary) and delete the newly created service
                        main.reload_webdriver(url=ss2_host, username=ss2_user, password=ss2_pass)
                        delete_service()
                    except:
                        main.log('XroadAddCentralService: Error deleting security server service')
                        main.save_exception_data()
                        assert False
            except:
                assert False
            assert False
        finally:
            # Test teardown
            main.tearDown(save_exception=False)
