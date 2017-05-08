class AssertHelper:
    '''
    Helps with and logs assertions, used as a base class for MainController.
    '''
    def __init__(self, case):
        self.case = case

    def is_true(self, con1, test_name=None, msg='Failed', log_message=None):
        '''
        Checks if variable is True.
        :param con1: bool - variable to check
        :param test_name: str|None - test name for logging or None to ignore
        :param msg: str - error message to log and display if assertion fails
        :param log_message: str - message to log
        :return: None
        '''
        log(test_name, msg, log_message, con1 == True)
        self.case.assertTrue(con1, msg)

    def is_false(self, con1, test_name=None, msg='Failed', log_message=None):
        '''
        Checks if variable is False.
        :param con1: bool - variable to check
        :param test_name: str|None - test name for logging or None to ignore
        :param msg: str - error message to log and display if assertion fails
        :param log_message: str - message to log
        :return: None
        '''
        log(test_name, msg, log_message, con1 == False)
        self.case.assertFalse(con1, msg)

    def is_equal(self, con1, con2, test_name=None, msg='Failed', log_message=None):
        '''
        Checks if variables are equal.
        :param con1: variable to compare
        :param con2: variable to compare
        :param test_name: str|None - test name for logging or None to ignore
        :param msg: str - error message to log and display if assertion fails
        :param log_message: str - message to log
        :return: None
        '''
        log(test_name, msg, log_message, con1 == con2)
        self.case.assertEqual(con1, con2, msg)

    def not_equal(self, con1, con2, test_name=None, msg='Failed', log_message=None):
        '''
        Checks if variables are not equal.
        :param con1: variable to compare
        :param con2: variable to compare
        :param test_name: str|None - test name for logging or None to ignore
        :param msg: str - error message to log and display if assertion fails
        :param log_message: str - message to log
        :return: None
        '''
        log(test_name, msg, log_message, con1 != con2)
        self.case.assertNotEqual(con1, con2, msg)

    def is_none(self, con1, test_name=None, msg='Failed', log_message=None):
        '''
        Checks if variable is None.
        :param con1: variable to check
        :param test_name: str|None - test name for logging or None to ignore
        :param msg: str - error message to log and display if assertion fails
        :param log_message: str - message to log
        :return: None
        '''
        log(test_name, msg, log_message, con1 is None)
        self.case.assertIsNone(con1, msg)

    def is_not_none(self, con1, test_name=None, msg='Failed', log_message=None):
        '''
        Checks if variable is not None.
        :param con1: variable to check
        :param test_name: str|None - test name for logging or None to ignore
        :param msg: str - error message to log and display if assertion fails
        :param log_message: str - message to log
        :return: None
        '''
        log(test_name, msg, log_message, con1 is not None)
        self.case.assertIsNotNone(con1, msg)


def log(test_name, err_message, log_message, condition):
    """
    Used for simple debug logging by AssertHelper class.
    :param test_name: str|None - test name to display
    :param err_message: str - error message to display if condition is not True
    :param log_message: str - message to display always
    :param condition: bool - True if no error; False otherwise
    :return: None
    """
    if test_name is not None:
        print test_name
    if log_message:
        if condition:
            print log_message, 'SUCCESSFUL'
        else:
            print err_message
