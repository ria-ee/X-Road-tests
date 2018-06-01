from tests.xroad_global_groups_tests.global_groups_tests import check_logs_for, LOGIN, LOGOUT


def check_login(self, ssh_client, cs_user, cs_pass):
    '''
    Login function that also checks if it succeeded. If specified, first logs the user out from existing session.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param logout_user: dict|None - user data for user that should be logged out; None if logout is not necessary
    :param login_user: dict|None - user data for user logging in; None if login not necessary
    :return: None
    '''
    # Login and logout checks (all users)

    self.log('CS_01 1-4. Checking login')

    # Log in the new user
    self.login(cs_user, cs_pass)

    # Check logs
    bool_value, data, date_time = check_logs_for(ssh_client=ssh_client, event=LOGIN, user=cs_user)
    self.is_true(bool_value,
                 'CS_01 4. Log check for logging in - check failed',
                 'CS_01 4. Log check for logging in')


def check_logout(self, ssh_client, cs_user):
    self.log('CS_02 1-2. Checking logout')
    self.logout()

    # Check logs
    bool_value, data, date_time = check_logs_for(ssh_client, LOGOUT, cs_user)
    self.is_true(bool_value,
                 'CS_02 3. Log check for logging out - check failed', 'CS_02 3. Log check for logging out',
                 )
