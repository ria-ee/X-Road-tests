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
    server_password = None
    sudo_password = None
    connect_key = None
    key_password = None

    def __init__(self, host, username, password=None, key_file=None, key_password=None):
        '''
        Connects to host.
        If sudo is needed in connection, user to connect as should also be in sudoers file.
        Password field can also set the private key file and key password by using the following syntax:
            "/home/user/private.key" - sets the key but not the password (file must not be password-protected)
            "/home/user/private.key::testpass" - tries to unlock the key file with password "testpass"
        Note that the extraction of key filename and key password from the password field only works when key_file
        has not been set.
        :param host: string - hostname to connect
        :param username: string - username to send to server
        :param password: None|string - user password; required for user-pass authentication or when using sudo with password
        :param key_file: None|string - private key file for SSH connections
        :param key_password: None|string - if private key file is password-protected, key file password
        '''
        if password is not None and key_file is None:
            # If password starts with "key:", treat it like key_file was set. If key_file was set, do not override it.
            if password.startswith('key:'):
                # Get the key filename without leading and trailing spaces and without "key:"
                key_file = password[4:].strip()

                # If key file parameter has a password, the syntax is filename::password; look for an ending like that
                if '::' in key_file:
                    temp = key_file.split('::', 1)
                    key_file = temp[0]
                    key_password = temp[1]

                # If sudo requires a password, it can be set on username field in format username:password
                if ':' in username:
                    temp = username.split(':', 1)
                    username = temp[0]
                    password = temp[1]
                else:
                    password = None

        self.open(host, username, password, key_file, key_password)

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
        Returns console output as string array(each line one element) removes '\n' from lines.
        :param command: string - command to send
        :param sudo: bool - True to send sudo before command
        :return: string array
        """
        if sudo:
            # command = 'echo "' + self.server_password + '" | sudo -S ' + command
            if self.sudo_password is None or self.sudo_password == '':
                command = 'sudo {0}'.format(command)
            else:
                command = 'echo "{0}" | sudo -S {1}'.format(self.sudo_password, command)
        if self.debug:
            print('Execute: {0}'.format(command))

        # Execute command, read output (stdout, stderr)
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
                print('Return stdout')

            for line in stdout:
                line = line.strip('\n')  # Remove newline character
                if line:
                    out_clean.append(line)
            for ln in stderr:
                out_error.append(ln)

            if self.debug:
                print('{0}\n{1}'.format(out_clean, out_error))
        else:
            # Set channel timeout
            stdout.channel.settimeout(timeout)

        # Return output and error buffer
        return out_clean, out_error

    def open(self, host, username, password=None, key_file=None, key_password=None):
        '''
        Connects to host.
        If sudo is needed in connection, user to connect as should also be in sudoers file.
        :param host: string - hostname to connect to
        :param username: string - username to send to server
        :param password: None|string - user password; required for user-pass authentication or when using sudo with password
        :param key_file: None|string - private key file for SSH connections
        :param key_password: None|string - if private key file is password-protected, key file password
        '''
        if self.client is None:
            if key_file is None:
                self.connect_key = None
                self.server_password = password
            else:
                self.connect_key = paramiko.RSAKey.from_private_key_file(key_file, password=key_password)
                self.server_password = None
            # Always set password for sudo
            self.sudo_password = password
            # add allowed key (currently disabled because we add all keys automatically)
            # key = paramiko.RSAKey(data=base64.b64decode(b'AAA...'))
            self.client = paramiko.SSHClient()
            # Set host key policy (add unknown keys automatically for testing)
            self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
            # Connect to server
            self.client.connect(host, username=username, password=self.server_password, pkey=self.connect_key)
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
