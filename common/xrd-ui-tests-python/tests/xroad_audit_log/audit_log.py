# coding=utf-8

from helpers import auditchecker


def test_audit_log(case, xroad_server, ssh_username,
                   ssh_password, logfile='/var/log/xroad/audit.log'):
    '''
    Checks for log entries using the AuditChecker class over SSH connection. Asserts if all supplied log entries exist
    in the audit.log or not. Raises an AssertionError if at least one entry is missing.
    :param case: MainController object
    :param xroad_server: X-Road server hostname/IP-address
    :param ssh_username: SSH username
    :param ssh_password: SSH password
    :param logfile: str - X-Road audit.log file path
    :param last_lines_only: bool - Check only last lines, even there are more returned lines. If False,
                                   just checks all returned log lines.
    :return:
    '''

    self = case

    def check_audit_log(check_lines, lines=None, from_line=None, sudo=False):
        '''
        Main test function for audit.log checking.
        :param check_lines: list[dict]|list[str]|dict|str - List of or log entries to check for.
        :param lines: int|None - If specified, read this number of lines from the end of the logfile
        :param from_line: int|None - If specified, start checking from this line in the logfile
        :param sudo: bool - Use sudo when issuing commands
        :return: bool - True if all entries exist
        '''
        self.log('Checking {0}:{1}'.format(xroad_server, logfile))
        self.log('Log entries to be checked: {0}'.format(check_lines))

        # Create an AuditChecker instance.
        checker = auditchecker.AuditChecker(host=xroad_server, username=ssh_username, password=ssh_password,
                                            logfile=logfile, sudo=sudo)

        # Check for entries.
        check_result = checker.check_log(check_lines, lines=lines, from_line=from_line)

        # Assert if everything was found or not; if not, raise an exception.
        self.is_true(check_result, msg='Some required log entries not found: {0}'.format(checker.missing_lines))

        # Also return the result
        return check_result

    return check_audit_log
