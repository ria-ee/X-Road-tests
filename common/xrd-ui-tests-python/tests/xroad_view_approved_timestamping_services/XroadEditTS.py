# coding=utf-8
import unittest
from main.maincontroller import MainController
import ts_management


class XroadEditTS(unittest.TestCase):
    """
    UC TRUST_17: Edit the URL of a Timestamping Server
    RIA URL: https://jira.ria.ee/browse/XTKB-79
    Depends on finishing other test(s):
    Requires helper scenarios:
    X-Road version: 6.16
    """
    def test_xroad_edit_ts(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'UC TRUST_17'
        main.log('TEST: UC TRUST_17: Edit the URL of a Timestamping Server')

        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        ts_name = main.config.get('tsa.host')
        ts_url = main.config.get('tsa.tsa_host')

        test_name = self._testMethodName

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        # Configure the service
        test_edit_ts = ts_management.test_edit_ts(case=main, cs_ssh_host=cs_ssh_host,
                                                  cs_ssh_user=cs_ssh_user, cs_ssh_pass=cs_ssh_pass, ts_url=ts_url,
                                                  ts_name=ts_name,
                                                  test_name=test_name)
        try:
            # Open webdriver
            main.reload_webdriver(url=cs_host, username=cs_user, password=cs_pass)

            # Run the test
            test_edit_ts()
        except:
            main.log('XroadEditTs: Failed to edit TS')
            main.save_exception_data()
            assert False
        finally:
            # Test teardown
            main.tearDown()
