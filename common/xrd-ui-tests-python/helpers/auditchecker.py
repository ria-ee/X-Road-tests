import ssh_client
import re
import json


class AuditChecker:
    '''
    X-Road log (audit.log) checker. Connects to security or central server over SSH and gets the last audit.log rows from
     it, then compares them to specified log entries and checks if they match. Used for checking if certain log entries
     have been added in some tests.
    '''

    # Default log file path
    logfile = '/var/log/xroad/audit.log'

    # Log line regular expression with named parameters
    line_regex = '(?P<timestamp>.*?)\s+(?P<server>.*?)\s+(?P<type>.*?)\s+\[(?P<component>.*?)\]\s+(?P<date>.*?)\s(?P<time>.*?)\s+-\s+(?P<json>.*)'

    # Initialize variables
    client = None
    error = None
    sudo = False

    # Output and checked lines that can be used by the test.
    missing_lines = []
    found_lines = []
    log_output = []

    def __init__(self, host, username, password, logfile=None, sudo=False):
        '''
        Sets up the class instance and default parameters. Opens connection to the server.
        :param host: str - hostname of the server
        :param username: str - SSH username
        :param password: str - SSH password
        :param logfile: str - logfile path in the server
        :param sudo: bool - use sudo for reading logfile. If set, user should be in sudoers list with NOPASSWD.
        '''

        # Open connection
        self.client = ssh_client.SSHClient(host, username, password)

        # If different logfile set, save it.
        if logfile is not None:
            self.logfile = logfile

        # Should we use sudo for tail command?
        self.sudo = sudo

    def get_regex(self):
        '''
        Returns the compiled regex object created from self.line_regex variable.
        :return: RegExp object
        '''
        return re.compile(self.line_regex)

    def get_line_count(self):
        '''
        Returns the current logfile line count using "wc -l" command. Can be used to limit the number of rows retrieved
        by get_log_lines.
        :return: int - number of lines in the file, or -1 if an error occurs.
        '''
        command = 'wc -l < {0}'.format(self.logfile)
        output, error = self.client.exec_command(command=command, sudo=self.sudo)
        if self.error or not output:
            return -1
        try:
            num = int(output[0])
            return num
        except:
            return -1

    def get_log_lines(self, lines=None, from_line=None):
        '''
        Gets a specified number of lines from the end of the logfile. Behaviour with both "lines" and "from_line"
        set is undefined, use only one of them.
        :param lines: int | None - if set, number of lines to return.
        :param from_line: int | None - if set, return rows from this line number
        :return: list[str] | None - lines from the end of the logfile as a list; None if an error occurs
        '''
        if lines is not None:
            params = '-n -{0}'.format(lines)
        if from_line is not None:
            params = '-n +{0}'.format(from_line)

        # Create shell command
        command = 'tail {1} {0}'.format(self.logfile, params)

        # Execute shell command
        output, error = self.client.exec_command(command=command, sudo=self.sudo)

        # Save error output
        self.error = error
        if self.error:
            # Got an error, return nothing.
            return None

        # Everything went well, return output.
        return output

    def reorder_lines(self, reverse_match):
        '''
        Reverse the internal lists if they have been saved as reversed {reverse_match=True when using check_log)
        :param reverse_match: bool - reverse the internal lists or not
        :return: None
        '''
        if reverse_match:
            self.log_output = self.log_output[::-1]
            self.missing_lines = self.missing_lines[::-1]
            self.found_lines = self.found_lines[::-1]

    def check_log(self, check, lines=None, from_line=None, reverse_match=True, skip_invalid_lines=True, strict=True):
        '''
        Checks if log contains an entry or entries.
        :param check: list[str]|str|list[dict]|dict - an entry or a list of entries to be checked for
        :param lines: int | None - if set, number of lines to get from the logfile
        :param from_line: int | None - if set, get logfile rows from this line number
        :param reverse_match: bool - True to check from the end to the beginning (default)
        :param skip_invalid_lines: bool - skip lines from the logfile if they cannot be parsed or are empty; otherwise
                                          the function will fail when encountering a line like that.
        :param strict: bool|None - if False, skip log lines until the next specified entry is found; True to fail right
                                   when first one does not match; None to be strict only with reverse_match=True
        :return: bool - True if all entries were found; False otherwise
        '''

        # We only check lists, so if the data is not a list, make it be one.
        if not isinstance(check, list):
            check = [check]

        rgx = self.get_regex()
        output = self.get_log_lines(lines=lines, from_line=from_line)

        if reverse_match:
            # If reverse matching is in effect, start from the last entry and ignore "additional" entries from the start.
            # Reverse the lists. We need true reversed lists, so we cannot use reversed() that gives an iterator.
            output = output[::-1]
            check = check[::-1]

        # If strict is not set, set it automatically.
        if strict is None:
            # When reverse matching, use strict.
            if reverse_match:
                strict = True
            else:
                strict = False

        # All elements are considered "not found" until found otherwise
        self.missing_lines = check
        self.found_lines = []
        self.log_output = output

        # If nothing is to be searched, check for nothing.
        if not check:
            # Reorder the lines if they were reversed
            self.reorder_lines(reverse_match)

            return True

        check_element = self.missing_lines[0]

        for line in output:
            try:
                row_data = [m.groupdict() for m in rgx.finditer(line)][0]
            except:
                # Failed to find regex match, invalid log entry; also exit if no more lines to analyze.
                if not skip_invalid_lines or not self.missing_lines:
                    # Reorder the lines if they were reversed
                    self.reorder_lines(reverse_match)
                    # End checking - no result
                    return False

                # We're allowed to skip lines, continue with the next one
                check_element = self.missing_lines[0]
                continue

            # Initialize variables.
            timestamp = None
            component = None
            server = None
            json_data = None
            log_time = None
            log_date = None
            log_type = None

            # Get variables for log entry.
            if 'timestamp' in row_data:
                timestamp = row_data['timestamp']
            if 'component' in row_data:
                component = row_data['component']
            if 'server' in row_data:
                server = row_data['server']
            if 'json' in row_data:
                json_data = row_data['json']
            if 'time' in row_data:
                log_time = row_data['time']
            if 'date' in row_data:
                log_date = row_data['date']
            if 'type' in row_data:
                log_type = row_data['type']

            if json_data is None:
                # No actual log data, continue.
                continue

            # Parse log data. If it is corrupt (non-json), the function will fail with an exception.
            data = json.loads(json_data)

            # Data is not a dict, log format error
            if not isinstance(data, dict):
                raise Exception('Log data is not a dictionary object.')

            # "Check for" value is a string, convert it to dict as value "event".
            if isinstance(check_element, basestring):
                # Allow "whatever" log entries for other actions that are logged but the message does not need to be checked.
                if check_element == '*':
                    check_element = data['event']

                check_element = {'event': check_element}

            # Check if all values in "check" exist in data
            if check_element.viewitems() <= data.viewitems():
                # All values of check_element exist in data, remove the line from unfound lines
                self.missing_lines.pop(0)
            elif strict:
                # check_element values do not exist or differ from data. If strict is used, we need everything in order.

                # Reorder the lines if they were reversed
                self.reorder_lines(reverse_match)

                # No match
                return False

            # If no other unfound elements left, exit loop
            if not self.missing_lines:
                break

            # Get the next element to be checked in the next cycle
            check_element = self.missing_lines[0]

        # Reorder the lines if they were reversed
        self.reorder_lines(reverse_match)

        # If at least one not found, return False
        if self.missing_lines:
            return False

        # Otherwise return True
        return True
