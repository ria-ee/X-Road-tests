# coding=utf-8
import unittest

import add_to_acl_2_1_8
from main.maincontroller import MainController
from helpers import xroad


class XroadAddToAcl(unittest.TestCase):
    def test_add_to_acl(self):
        main = MainController(self)

        # Set test name and number
        main.test_number = '2.1.8'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss2.host')
        ss_user = main.config.get('ss2.user')
        ss_pass = main.config.get('ss2.pass')

        client = xroad.split_xroad_id(main.config.get('ss2.client_id'))
        requester = xroad.split_xroad_id(main.config.get('ss2.client_id'))

        wsdl_url = main.config.get('wsdl.remote_path').format(main.config.get('wsdl.service_wsdl'))

        subject_list = [xroad.get_xroad_subsystem(requester)]

        service_name = main.config.get('services.test_service')

        # TEST PLAN 2.1.8 (2.1.8-3 subitem 1 - "Add Selected to ACL")
        # Add some subjects (subject_list) to ACL
        test_add_subjects = add_to_acl_2_1_8.test_add_subjects(main, client=client, wsdl_url=wsdl_url,
                                                               service_name=service_name, service_subjects=subject_list,
                                                               remove_data=True,
                                                               allow_remove_all=False)

        # TEST PLAN 2.1.8 (2.1.8-3 subitem 2 - "Add All to ACL")
        # Add all subjects to ACL
        test_add_all_subjects = add_to_acl_2_1_8.test_add_all_subjects(main, client=client,
                                                                       wsdl_url=wsdl_url, service_name=service_name,
                                                                       remove_data=True,
                                                                       allow_remove_all=True)

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