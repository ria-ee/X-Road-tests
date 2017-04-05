from selenium.common.exceptions import TimeoutException, NoSuchElementException
from view_models import popups

ERROR_MESSAGE_CSS = '.messages .error'
ERROR_MESSAGE_CLOSE_CSS = '.messages .error i'
WARNING_MESSAGE_CSS = '#warning'
NOTICE_MESSAGE_CSS = '.messages .notice'

# {0} is replaced with WSDL file URL
WSDL_ERROR_INVALID_URL = 'Failed to add WSDL: Malformed URL. WSDL URL must point to a WSDL file.'
WSDL_ERROR_INCORRECT_WSDL = 'Failed to add WSDL: Incorrect file structure. WSDL URL must point to a WSDL file.'
WSDL_ERROR_ADDRESS_EXISTS = 'Failed to add WSDL: WSDL address already exists.'  # Service 'mockSwaRef.v1' already exists in WSDL http://xtee2.asa:8080/www/mock.wsdl
WSDL_ERROR_DUPLICATE_SERVICE = 'Failed to add WSDL: Duplicate service.'
WSDL_ERROR_VALIDATION_FAILED = 'Failed to add WSDL: WSDL ({0}) validation failed'

WSDL_EDIT_ERROR_VALIDATION_FAILED = 'Failed to edit WSDL: WSDL ({0}) validation failed'

WSDL_REFRESH_ERROR_VALIDATION_FAILED = 'Failed to refresh WSDL(s): WSDL ({0}) validation failed'
WSDL_REFRESH_WARNING_ADDING_SERVICES = 'Adding services:'
WSDL_REFRESH_WARNING_DELETING_SERVICES = 'Deleting services:'

# SERVICE_EDIT_INVALID_URL = 'Invalid URL format, must begin with \'http\' or \'https\''
SERVICE_EDIT_INVALID_URL = '\'{0}\' is an invalid URL, examples of valid URL-s: \'http://www.example.com\', \'https://www.example.com\''
SERVICE_EDIT_INVALID_TIMEOUT = 'Timeout value must be a positive integer.'
SERVICE_EDIT_INFINITE_TIMEOUT_WARNING = 'A timeout value of zero is interpreted as an infinite timeout.'

CERTIFICATE_NOT_SIGNING_KEY = 'Failed to import certificate: Authentication certificate cannot be imported to signing keys'
NO_KEY_FOR_CERTIFICATE = 'Failed to import certificate: Could not find key corresponding to the certificate'
NO_CLIENT_FOR_CERTIFICATE = 'Failed to import certificate: Certificate issued to an unknown member'
WRONG_FORMAT_CERTIFICATE = 'Failed to import certificate: Incorrect file format. Only PEM and DER files allowed.'
CERTIFICATE_ALREADY_EXISTS = 'Failed to import certificate: Certificate already exists under key'
CA_NOT_VALID_AS_SERVICE = 'Failed to import certificate: Cannot read member identifier from signing certificate: InternalError: Certificate is not issued by approved certification service provider.'


def get_error_message(self):
    '''
    Returns the first visible error message string (an element with class 'error' inside an element with class
     'messages'). If no such element if found, None is returned.
    One error message should be displayed at once but if there are many, it returns the first visible one found.
    :param self: MainController class object
    :return: string | None
    '''
    # Check if an error message was shown.
    try:
        messages = self.by_css(ERROR_MESSAGE_CSS, multiple=True)
        # We're here, so the element exists. Loop over the found element(s) to find the first one that is visible.
        for message in messages:
            # Return message text if it is displayed
            if message.is_displayed():
                return message.text
        # We didn't find any visible elements in the loop, so no error.
        return None
    # Element not found. This means that there is no error message.
    except NoSuchElementException:
        return None


def close_error_messages(self):
    '''
    Closes all visible error messages (an element with class 'error' inside an element with class 'messages').
    :param self: MainController class object
    :return: None
    '''
    # Check if an error message was shown.
    try:
        messages = self.by_css(ERROR_MESSAGE_CLOSE_CSS, multiple=True)
        # We're here, so the element exists. Loop over the found element(s) to find the first one that is visible.
        for message in messages:
            # Click message text if it is displayed
            if message.is_displayed():
                message.click()
        return None
    # Element not found. This means that there is no error message.
    except NoSuchElementException:
        return None


def get_warning_message(self):
    '''
    Returns the warning message string (an element with id 'warning').
    If no such element if found, None is returned.
    :param self: MainController class object
    :return: string | None
    '''
    # Check if an error message was shown.
    try:
        message = self.by_css(WARNING_MESSAGE_CSS)
        # We're here, so the element exists. If it is visible, return the message text.
        if message.is_displayed():
            return message.text
        else:
            # The element was not visible, so no warnings.
            return None
    # Element not found. This means that there is no error message.
    except NoSuchElementException:
        return None


def get_notice_message(self):
    '''
    Returns the first visible notice message string (an element with class 'notice' inside an element with class
     'messages'). If no such element if found, None is returned.
    One error message should be displayed at once but if there are many, it returns the first visible one found.
    :param self: MainController class object
    :return: string | None
    '''
    # Check if an error message was shown.
    try:
        messages = self.by_css(NOTICE_MESSAGE_CSS, multiple=True)
        # We're here, so the element exists. Loop over the found element(s) to find the first one that is visible.
        for message in messages:
            # Return message text if it is displayed
            if message.is_displayed():
                return message.text
        # We didn't find any visible elements in the loop, so no error.
        return None
    # Element not found. This means that there is no error message.
    except NoSuchElementException:
        return None


def get_console_output(self):
    '''
    Returns the console output text if anything is shown.
    If no such element if found visible, None is returned.
    :param self: MainController class object
    :return: string | None
    '''
    # Check if an error message was shown.
    # Check if an error message was shown.
    try:
        message = self.by_css(popups.CONSOLE_OUTPUT_DIALOG_TEXT_CSS)
        # We're here, so the element exists. If it is visible, return the message text.
        if message.is_displayed():
            return message.text
        else:
            # The element was not visible, so no warnings.
            return None
    # Element not found. This means that there is no error message.
    except NoSuchElementException:
        return None
