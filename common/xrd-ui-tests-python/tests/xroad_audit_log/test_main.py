# coding=utf-8
import unittest

import tests.xroad_audit_log.audit_log as audit_log
from main.maincontroller import MainController
import json
import sys


class XroadAuditLog(unittest.TestCase):
    def test_xroad_audit_log(self):
        '''
        audit.log checking test. Checks if audit.log of a specified server contains specified (in configuration or
        command-line parameters) entries. Test succeeds if all of the entries are found; fails otherwise.
        :return: None
        '''
        main = MainController(self)

        # Set test name and number
        main.test_number = 'LOGCHECK'
        main.test_name = self.__class__.__name__

        # Get parameters from the configuration file.

        # We can supply a "server" name to this test. This means that it uses this name as a category name and
        # fetches ssh_host, ssh_user and ssh_pass of this category. For example, you can set audit.server=ss1 and
        # the values that are used are ss1.ssh_host, ss1.ssh_user, and ss1.ssh_pass respectively.
        audit_server = main.config.get('audit.server')
        if audit_server is not None:
            # audit.server was supplied so we're reading data from the sections
            xroad_server = main.config.get('{0}.ssh_host'.format(audit_server))
            ssh_username = main.config.get('{0}.ssh_user'.format(audit_server))
            ssh_password = main.config.get('{0}.ssh_pass'.format(audit_server))
        else:
            # If audit.server was not supplied, we read each parameter separately
            xroad_server = main.config.get('audit.ssh_host')
            ssh_username = main.config.get('audit.ssh_user')
            ssh_password = main.config.get('audit.ssh_pass')

        # Get logfile
        logfile = main.config.get('audit.logfile')

        # Get data to be checked
        check_json = main.config.get('audit.check-logs')

        # Read data from this line
        from_line = main.config.get_int('audit.from-line', 0)

        # Because the supplied parameter may also be a string, use try-except
        try:
            check_entries = json.loads(check_json)
        except (ValueError, TypeError):
            check_entries = [check_json]
            sys.exc_clear()

        # Configure the service
        test_audit_log = audit_log.test_audit_log(case=main, xroad_server=xroad_server, ssh_username=ssh_username,
                                                  ssh_password=ssh_password, logfile=logfile)

        try:
            # Run audit.log checking
            test_audit_log(check_lines=check_entries, from_line=from_line)
        except:
            main.log('XroadAuditLog: audit.log check failed for: {0}'.format(check_json))
            main.save_exception_data()
            raise
        finally:
            # Test teardown
            main.tearDown()
