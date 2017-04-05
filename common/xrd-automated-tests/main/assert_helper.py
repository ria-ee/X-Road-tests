class AssertHelper:
    def __init__(self, case):
        self.case = case

    def is_true(self, con1, test_name=None, msg='Failed', log_message=None):
        log(test_name, msg, log_message, con1 == True)
        self.case.assertTrue(con1, msg)

    def is_false(self, con1, test_name=None, msg='Failed', log_message=None):
        log(test_name, msg, log_message, con1 == False)
        self.case.assertFalse(con1, msg)

    def is_equal(self, con1, con2, test_name=None, msg='Failed', log_message=None):
        log(test_name, msg, log_message, con1 == con2)
        self.case.assertEqual(con1, con2, msg)

    def not_equal(self, con1, con2, test_name=None, msg='Failed', log_message=None):
        log(test_name, msg, log_message, con1 != con2)
        self.case.assertNotEqual(con1, con2, msg)

    def is_none(self, con1, test_name=None, msg='Failed', log_message=None):
        log(test_name, msg, log_message, con1 is None)
        self.case.assertIsNone(con1, msg)

    def is_not_none(self, con1, test_name=None, msg='Failed', log_message=None):
        log(test_name, msg, log_message, con1 is not None)
        self.case.assertIsNotNone(con1, msg)


def log(test_name, err_message, log_message, condition):
    if test_name is not None:
        print test_name
    if log_message:
        if condition:
            print log_message, 'SUCCESSFUL'
        else:
            print err_message
