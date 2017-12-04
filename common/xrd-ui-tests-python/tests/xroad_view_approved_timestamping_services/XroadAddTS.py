# coding=utf-8
import unittest
from main.maincontroller import MainController
import ts_management
from tests.xroad_cs_ocsp_responder import ocsp_responder


class XroadAddTS(unittest.TestCase):

    """
    UC TRUST_16: Add an Approved Timestamping Service
    RIA URL: https://jira.ria.ee/browse/XTKB-75
    Depends on finishing other test(s): Delete test must run before (xroad_view_approved_timestamping_services\XroadDeleteTS.py)
    Requires helper scenarios:
    X-Road version: 6.16.0
    """



    def test_xroad_add_ts(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC TRUST_16'
        main.log('TEST: UC TRUST_16: Add an Approved Timestamping Service')

        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        ts_name = main.config.get('tsa.host')
        ts_url = main.config.get('tsa.tsa_host')
        ts_certificate_filename = 'tsa.cert.pem'

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        test_name = self._testMethodName
        ocsp_responder.ca_get_certificates(main, ca_ssh_host, ca_ssh_user, ca_ssh_pass, [ts_certificate_filename])

        ts_certificate = main.get_download_path(ts_certificate_filename)
        invalid_ts_certificate = main.get_download_path('INFO')

        # Configure the service
        test_add_ts = ts_management.test_add_ts(case=main, ts_url=ts_url, ts_certificate=ts_certificate,
                                                invalid_ts_certificate=invalid_ts_certificate, cs_ssh_host=cs_ssh_host,
                                                cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass, ts_name=ts_name,
                                                test_name=test_name)

        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)
            # Run the test
            test_add_ts()
        except:
            main.log('XroadAddTs: Failed to add TS')
            main.save_exception_data()
            try:
                # Delete service
                main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

            except:
                main.log('XroadAddTs: Failed to delete added data.')
                main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
