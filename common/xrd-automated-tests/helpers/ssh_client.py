import paramiko  # https://github.com/paramiko/paramiko


class SSHClient:
    '''
    Simple SSH Client class using Paramiko library.
    Connects to an SSH server and allows to execute commands and use stdin, stdout, stderr.
    '''
    stdin = None
    stdout = None
    stderr = None
    debug = False
    client = None

    def __init__(self, host, username, password):
        """
            Connects to host.
            If sudo is needed in connection, user to connect as should also be in sudoers
        :param host: string (only domain and extension eg. "xtee.asa")
        :param username: string
        :param password: string
        """
        self.open(host, username, password)

    def get_client(self):
        '''
        Returns the internal paramiko.SSHClient instance.
        :return: paramiko.SSHClient
        '''
        return self.client

    def exit_status(self):
        '''
        Get the latest command's exit status code.
        :return: int - status code
        '''
        return self.status

    def write(self, str, flush=False):
        '''
        Using stdin, send text to server and, if specified, flush the buffer.
        :param str: str - text to send
        :param flush: bool - flush the buffer after sending
        :return: bool - True if stdin exists, False otherwise
        '''
        if self.stdin:
            if str:
                self.stdin.write(str)
            if flush:
                self.stdin.flush()
            return True
        return False

    def write_flush(self, str, linefeed=True):
        '''
        Using stdin, send text or line to server and flush it.
        :param str:
        :param linefeed: bool - add a newline character to the string if True
        :return: bool - True if stdin exists, False otherwise
        '''
        # Send the text without flushing
        self.write(str)
        if linefeed:
            # Send a linefeed and flush.
            return self.write('\n', flush=True)
        else:
            # No linefeed required, just flush.
            return self.write(None, flush=True)

    def writeline(self, line):
        '''
        Using stdin, send a line (adding a linefeed character to specified text) to server and flush it.
        :param line: str - text to send, without the linefeed
        :return: bool - True if stdin exists, False otherwise
        '''
        return self.write_flush(line, linefeed=True)

    def readline(self):
        '''
        Reads a line from stdout, excluding newline characters.
        :return: str|None - data from stdout, or None if stdout does not exist
        '''
        if self.stdout:
            # Read the line and strip it from newlines.
            return self.stdout.readline().strip('\n')
        return None

    def exec_command(self, command, sudo=False, timeout=None):
        """
            Executes the command.
            To enable sudo, param must be true, default False
            Returns console ouput as string array(each line one element) removes '\n' from lines.
        :param command: string - command to send
        :param sudo: bool - True to send sudo before command
        :return: string array
        """
        if sudo:
            command = 'echo "' + self.server_password + '" | sudo -S ' + command
        if self.debug:
            print 'Execute', command
        # Execute command, read output (stdout, stderr)
        # print 'execute command'
        stdin, stdout, stderr = self.client.exec_command(command)

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

        out_clean = []
        out_error = []
        if timeout is None:
            # Get the exit status and save it internally
            self.status = stdout.channel.recv_exit_status()

            if self.debug:
                print 'return stdout'

            for line in stdout:
                line = line.strip('\n')  # Remove newline character
                if line:
                    out_clean.append(line)
            for ln in stderr:
                out_error.append(ln)

            if self.debug:
                print out_clean
                print out_error
        else:
            # Set channel timeout
            stdout.channel.settimeout(timeout)

        # Return output and error buffer
        return out_clean, out_error

    def open(self, host, username, password):
        '''
            Connects to host.
            If sudo is needed in connection, user to connect as should also be in sudoers
        :param host: string (only domain and extension eg. "xtee.asa")
        :param username: string
        :param password: string
        '''
        if self.client is None:
            self.server_password = password
            # add allowed key (currently disabled because we add all keys automatically)
            # key = paramiko.RSAKey(data=base64.b64decode(b'AAA...'))
            self.client = paramiko.SSHClient()
            # Set host key policy (add unknown keys automatically for testing)
            self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
            # Connect to server
            self.client.connect(host, username=username, password=password)
            # Set default exit status
            self.status = -1

    def close(self):
        '''
        Close the connection.
        :return: None
        '''
        if self.client is not None:
            self.client.close()
            self.client = None
            self.status = -1
