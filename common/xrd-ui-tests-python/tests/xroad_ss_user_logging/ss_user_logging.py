from tests.xroad_global_groups_tests.global_groups_tests import check_logs_for, LOGIN, LOGOUT


def check_login(self, cs_user, cs_pass, log_checker=None):
    '''
    Login function that also checks if it succeeded. If specified, first logs the user out from existing session.
    :param self: MainController object
    :param ssh_client: SSHClient object
    :param logout_user: dict|None - user data for user that should be logged out; None if logout is not necessary
    :param login_user: dict|None - user data for user logging in; None if login not necessary
    :return: None
    '''
    # Login and logout checks (all users)
    current_log_lines = None
    if log_checker:
        current_log_lines = log_checker.get_line_count()
    self.log('CS_01 1-4. Checking login')

    # Log in the new user
    self.login(cs_user, cs_pass)

    if current_log_lines:
        logs_found = log_checker.check_log(LOGIN, from_line=current_log_lines + 1)
        self.is_true(logs_found)


def check_logout(self, log_checker=None):
    current_log_lines = None
    if log_checker:
        current_log_lines = log_checker.get_line_count()
    self.log('CS_01 1-4. Checking login')
    self.logout()
    if current_log_lines:
        logs_found = log_checker.check_log(LOGOUT, from_line=current_log_lines + 1)
        self.is_true(logs_found)
