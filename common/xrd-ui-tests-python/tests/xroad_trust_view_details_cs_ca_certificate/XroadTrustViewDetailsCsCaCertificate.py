# coding=utf-8
import unittest
from main.maincontroller import MainController
import view_management

"""
 UC TRUST_03: View Certificate Details
 RIA URL: https://jira.ria.ee/browse/XTKB-188
 Depends on finishing other test(s):
 Requires helper scenarios:
 X-Road version: 6.16.0
 """


class XroadTrustViewDetailsCsCaCertificate(unittest.TestCase):
    def test_xroad_view_cs_ca_cert(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC TRUST_03'
        main.log('TEST:  UC TRUST_03: View Certificate Details')

        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        ca_name = main.config.get('ca.name')
        '''Configure the service'''
        test_view_details_cs_ca_cert = view_management.test_ca_cs_details_view_cert(case=main, ca_name=ca_name)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            '''Run the test'''
            test_view_details_cs_ca_cert()
        except:
            main.log(
                'Xroad_trust_view_details_cs_ca_certificate: Failed to view Certificate Details')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
