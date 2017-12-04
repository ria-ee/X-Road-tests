# coding=utf-8
import unittest
from main.maincontroller import MainController
import view_management
from helpers import xroad

"""
 TRUST_01: View Approved Certification Services
 RIA URL: https://jira.ria.ee/browse/XTKB-184
 Depends on finishing other test(s):
 Requires helper scenarios:
 X-Road version: 6.16.0
 """


class XroadTrustViewApprovedCertService(unittest.TestCase):
    def test_xroad_view_approved_cert(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC TRUST_01'
        main.log('TEST:  UC TRUST_01: View Approved Certification Services')

        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        ca_name = 'ca.asa'

        '''Configure the service'''
        test_view_approved_cert_servives = view_management.test_verify_approved_cert_services(case=main, ca_name=ca_name)

        try:
            '''Open webdriver'''
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            '''Run the test'''
            test_view_approved_cert_servives()
        except:
            main.log(
                'Xroad_trust_view_approved_cert_service: Failed to view Approved Certification Services')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
