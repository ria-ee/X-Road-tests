# coding=utf-8
import unittest
from main.maincontroller import MainController
import view_management

"""
 UC TRUST_02: View the Details of a Certification Service CA
 RIA URL: https://jira.ria.ee/browse/XTKB-185
 Depends on finishing other test(s):
 Requires helper scenarios:
 X-Road version: 6.16.0
 """


class XroadTrustViewDetailsCsCa(unittest.TestCase):
    def test_xroad_view_details(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC TRUST_02'
        main.log('TEST:  UC TRUST_02: View the Details of a Certification Service CA')

        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        '''Configure the service'''
        test_view_details_cs_ca = view_management.test_view_details_cert_services(case=main)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            '''Run the test'''
            test_view_details_cs_ca()
        except:
            main.log(
                'Xroad_trust_view_details_cs_ca: Failed to view the Details of a Certification Service CA')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
