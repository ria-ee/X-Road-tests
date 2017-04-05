from helpers import ssh_client
import re
import time


class MockRunner:
    '''
    Class that tries to control the mock service script (SoapUI MockRunner) over an SSH connection. Uses
    ssh_helper.SSHClient component.

    Connects to SSH server, sends a one-liner command and then waits until a specified regex matches output or a timeout
    occurs. To stop the service, sends a single keycode (Ctrl-C by default).
    '''
    running = False  # Internal variable - service running or not
    error = None  # Last error
    command = None  # Mock start command
    debug = False

    def __init__(self, host, username, password, command,
                 ready_regex='.*\[SoapUIMockServiceRunner\] Started.*', ready_timeout=60, stop_keycode=3):
        '''
        Initialize the class and open the SSH connection.
        :param host: str - hostname of the server
        :param username: str - username
        :param password: str - password
        :param command: str - mock service start command, one-liner (semicolons can be used for command sequence)
        :param ready_regex: str - regex to wait for until concluding that the service is up and running
        :param ready_timeout: int - service start timeout in seconds; if this passes, starting failed
        :param stop_keycode: int - keycode to send to kill the service; can be Ctrl-C (3) or Enter (13) for SoapUI
        '''
        self.ssh = ssh_client.SSHClient(host=host, username=username, password=password)
        self.command = command
        self.ready_regex = re.compile(ready_regex)
        self.ready_timeout = ready_timeout
        self.stop_keycode = stop_keycode

    def start(self):
        '''
        Tries to start the mock service.
        :return: bool - if the service was started
        '''

        # No errors by default
        self.error = None

        # If the service is already running, set an error and fail start (return False)
        if self.running:
            self.error = 'Already running'
            return False

        # Set running to be true to block other start requests
        self.running = True

        # Execute command over SSH, line reading timeout is 1 second
        self.ssh.exec_command(self.command, timeout=1)

        # Get the current time to check for timeout
        start_time = time.time()
        while True:
            # Read lines from SSH
            try:
                line = self.ssh.readline()
                if line:
                    if self.debug:
                        # Print line for logging
                        print line

                    # If the line matches the specified regex, mock is running, break the loop.
                    if self.ready_regex.match(line):
                        break
                else:
                    # Go to the exception
                    raise RuntimeError
            except:
                # If time limit passed, set an error and return False
                if time.time() > start_time + self.ready_timeout:
                    self.error = 'Mock start timeout'
                    return False

        return True

    def restart(self):
        '''
        Restart mock service.
        :return:
        '''
        # If already running, stop it.
        if self.running:
            self.stop()

        # Start again.
        self.start()

    def stop(self):
        '''
        Stop the mock service.
        :return:
        '''
        if self.running:
            if self.debug:
                print "Mock stopping"
            # Send a stop character and flush it.
            try:
                self.ssh.write(chr(self.stop_keycode), flush=True)
            except:
                pass

            # Not running and no error.
            self.running = False
            self.error = None

    def get_error(self):
        '''
        Returns the last error.
        :return: str|None - last error message
        '''
        return self.error
