# coding=utf-8
import unittest
from main.maincontroller import MainController
import view_management

"""
 UC TRUST_04: View the Settings of a Certification Service
 RIA URL: https://jira.ria.ee/browse/XTKB-191
 Depends on finishing other test(s):
 Requires helper scenarios:
 X-Road version: 6.16.0
 """


class XroadTrustViewDetailsCsSettings(unittest.TestCase):
    def test_xroad_view_view_cs(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC TRUST_04'
        main.log('TEST:  UC TRUST_04: View the Settings of a Certification Service')

        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        profile_class = main.config.get('ca.profile_class')

        '''Configure the service'''
        test_view_details_cs_ca_cert = view_management.test_ca_cs_details_view_cert(case=main, profile_class=profile_class)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            '''Run the test'''
            test_view_details_cs_ca_cert()
        except:
            main.log(
                'Xroad_trust_view_details_cs_settings: Failed to view the Settings of a Certification Service')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
