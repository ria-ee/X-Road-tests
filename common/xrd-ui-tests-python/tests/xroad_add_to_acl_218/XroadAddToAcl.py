# coding=utf-8
import unittest

import add_to_acl
from main.maincontroller import MainController
from helpers import xroad, auditchecker


class XroadAddToAcl(unittest.TestCase):
    """
    SERVICE_17 Add Access Rights to a Service
    SERVICE_18 Remove Access Rights from a Service
    RIA URL: https://jira.ria.ee/browse/XT-274, https://jira.ria.ee/browse/XTKB-172
    RIA URL: https://jira.ria.ee/browse/XT-275, https://jira.ria.ee/browse/XTKB-173
    Depends on finishing other test(s): XroadConfigureService
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_add_to_acl(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = 'SERVICE_17 / SERVICE_18'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        ss_ssh_host = main.config.get('ss2.ssh_host')
        ss_ssh_user = main.config.get('ss2.ssh_user')
        ss_ssh_pass = main.config.get('ss2.ssh_pass')

        log_checker = auditchecker.AuditChecker(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        subject_list = [xroad.get_xroad_subsystem(requester)]

        service_name = main.config.get('services.test_service')

        test_add_subjects = add_to_acl.test_add_subjects(main, client=client, wsdl_url=wsdl_url,
                                                         service_name=service_name, service_subjects=subject_list,
                                                         remove_data=True,
                                                         allow_remove_all=False, log_checker=log_checker)

        test_add_all_subjects = add_to_acl.test_add_all_subjects(main, client=client,
                                                                 wsdl_url=wsdl_url, service_name=service_name,
                                                                 remove_data=True,
                                                                 allow_remove_all=True, log_checker=log_checker)

        try:
            # Test add one user to ACL
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_add_subjects()

            # Test add all to ACL
            main.reload_webdriver(url=ss_host, username=ss_user, password=ss_pass)
            test_add_all_subjects()
        except:
            main.log('2.1.8 failed')
            raise
        finally:
            # Test teardown
            main.tearDown()