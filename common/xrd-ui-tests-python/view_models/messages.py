from selenium.common.exceptions import NoSuchElementException

from view_models import popups

CLIENT_ALREADY_EXISTS_ERROR = 'Client already exists'
DELETE_AUTH_CERT_REQ_ADDED = 'Request of deleting authentication certificate from security server \'{0}\' added successfully'
ERROR_MESSAGE_CSS = '.messages .error'
ERROR_MESSAGE_CLOSE_CSS = '.messages .error i'
WARNING_MESSAGE_CSS = '#warning'
NOTICE_MESSAGE_CSS = '.messages .notice'
SERVICE_DISABLED_MESSAGE = 'Out of order'
DESCRIPTION_CHANGED_SUCCESSFULLY = 'Description changed successfully'

# {0} is replaced with WSDL file URL
WSDL_ERROR_INVALID_URL = 'Failed to add WSDL: Malformed URL. WSDL URL must point to a WSDL file.'
WSDL_ERROR_INCORRECT_WSDL = 'Failed to add WSDL: Incorrect file structure. WSDL URL must point to a WSDL file.'
WSDL_ERROR_ADDRESS_EXISTS = 'Failed to add WSDL: WSDL address already exists.'  # Service 'mockSwaRef.v1' already exists in WSDL http://www.example/mock.wsdl
WSDL_ERROR_DUPLICATE_SERVICE = 'Failed to add WSDL: Duplicate service.'
WSDL_ERROR_VALIDATION_FAILED = 'Failed to add WSDL: WSDL ({0}) validation failed'

WSDL_EDIT_ERROR_VALIDATION_FAILED = 'Failed to edit WSDL: WSDL ({0}) validation failed'
WSDL_EDIT_ERROR_FILE_DOES_NOT_EXIST = 'Failed to edit WSDL: Downloading WSDL failed. WSDL URL must point to a WSDL file.'
WSDL_EDIT_ERROR_WSDL_EXISTS = 'Failed to edit WSDL: WSDL address already exists.'
WSDL_EDIT_INCORRECT_STRUCTURE = 'Failed to edit WSDL: Incorrect file structure. WSDL URL must point to a WSDL file.'


WSDL_ADD_ERROR_VALIDATOR_COMMAND_NOT_FOUND = 'Failed to add WSDL: Running WSDL validator failed. Command not found.'
WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_FOUND = 'Failed to refresh WSDL(s): Running WSDL validator failed. Command not found.'
WSDL_REFRESH_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE = 'Failed to refresh WSDL(s): Running WSDL validator failed. Command not executable.'
WSDL_ERROR_VALIDATOR_COMMAND_NOT_EXECUTABLE = 'Failed to add WSDL: Running WSDL validator failed. Command not executable.'

WSDL_REFRESH_ERROR_SERVICE_EXISTS = 'Failed to refresh WSDL(s): New service \'{0}\' at {1} also exists at {2}'
WSDL_REFRESH_ERROR_VALIDATION_FAILED = 'Failed to refresh WSDL(s): WSDL ({0}) validation failed'
WSDL_REFRESH_WARNING_ADDING_SERVICES = 'Adding services:'
WSDL_REFRESH_WARNING_DELETING_SERVICES = 'Deleting services:'

# INVALID_URL = 'Invalid URL format, must begin with \'http\' or \'https\'' # Specification variant
INVALID_URL = '\'{0}\' is an invalid URL, examples of valid URL-s: \'http://www.example.com\', \'https://www.example.com\''  # Real variant
INPUT_DATA_TOO_LONG = "Parameter '{0}' input exceeds 255 characters"
MISSING_PARAMETER = "Missing parameter: {0}"
INVALID_CERTIFICATE_PROFILE = "Certificate profile with name '{0}' does not exist."
MEMBER_DELETED_FROM_GLOBAL_GROUP = 'Member \'{0}\' successfully deleted from global group \'{1}\''
MEMBER_ADDED_TO_GLOBAL_GROUP = 'Member \'{0}\' successfully added to global group \'{1}\''
ADD_MEMBER_TO_GLOBAL_GROUP = "Add member to global group"
SERVICE_EDIT_INVALID_URL = INVALID_URL
SERVICE_EDIT_INVALID_TIMEOUT = 'Timeout value must be a positive integer.'
SERVICE_EDIT_INFINITE_TIMEOUT_WARNING = 'A timeout value of zero is interpreted as an infinite timeout.'

AUTH_CERT_IMPORT_FILE_FORMAT_ERROR = 'Failed to import authentication certificate: Incorrect file format. Only PEM and DER files allowed.'
AUTH_CERT_IMPORT_FILE_CANNOT_BE_USED = 'Failed to import authentication certificate: This certificate cannot be used for authentication.'
INVALID_URL = SERVICE_EDIT_INVALID_URL

TSL_CERTIFICATE_ALREADY_EXISTS = "Certificate already exists"
TSL_CERTIFICATE_INCORRECT_FILE_FORMAT = "Incorrect file format. Only PEM and DER files allowed."
CERTIFICATE_IMPORT_SUCCESSFUL = 'Certificate imported successfully'
CA_ADD_SUCCESSFUL = 'Certification service added successfully'

UNKNOWN_ORGANIZATION_ERROR = 'Failed to import certificate: Certificate issued to an unknown member'
IMPORT_CERT_KEY_NOT_FOUND_ERROR = 'Failed to import certificate: key not found'
AUTHCERT_DELETION_DISABLED = 'Services/authCertDeletion is disabled: Out of order'
CERTIFICATE_NOT_VALID = 'Failed to import certificate: Certificate is not valid'
CERTIFICATE_NOT_SIGNING_KEY = 'Failed to import certificate: Authentication certificate cannot be imported to signing keys'
NO_KEY_FOR_CERTIFICATE = 'Failed to import certificate: Could not find key corresponding to the certificate'
NO_CLIENT_FOR_CERTIFICATE = 'Failed to import certificate: Certificate issued to an unknown member'
SIGN_CERT_INSTEAD_AUTH_CERT = "Failed to import certificate: Cannot read member identifier from signing certificate: IncorrectCertificate: Certificate subject name does not contain organization"
WRONG_FORMAT_CERTIFICATE = 'Failed to import certificate: Incorrect file format. Only PEM and DER files allowed.'
WRONG_FORMAT_OCSP_CERTIFICATE = 'Failed to upload OCSP responder certificate: Incorrect file format. Only PEM and DER files allowed.'
CERTIFICATE_ALREADY_EXISTS = 'Failed to import certificate: Certificate already exists under key'
CA_NOT_VALID_AS_SERVICE = 'Failed to import certificate: Cannot read member identifier from signing certificate: InternalError: Certificate is not issued by approved certification service provider.'
INTERMEDIATE_CA_ADDED_SUCCESSFULLY = 'Intermediate CA added successfully'
WRONG_FORMAT_INTERMEDIATE_CA_CERTIFICATE = 'Failed to upload intermediate CA certificate: Incorrect file format. Only PEM and DER files allowed.'
WRONG_FORMAT_CA_CERTIFICATE = 'Failed to upload service CA certificate: Incorrect file format. Only PEM and DER files allowed.'
WRONG_FORMAT_TS_CERTIFICATE = 'Failed to upload approved TSA certificate: Incorrect file format. Only PEM and DER files allowed.'
GROUP_ALREADY_EXISTS_ERROR = 'A group with code \'{0}\' already exists'

GLOBAL_GROUP_ALREADY_TAKEN = "Failed to add global group: '{0}' has already been taken"
REQUEST_SENT_NOTICE = 'Request sent'

MEMBER_ALREADY_EXISTS_ERROR = 'Failed to add member: Member with class \'{0}\' and code \'{1}\' already exists'
CERTIFICATE_ADDING_NEW_SERVER_REQUEST_ADDED_NOTICE = 'Request of adding authentication certificate to new security server \'SERVER:{0}\' added successfully'
CERTIFICATE_ADDING_EXISTING_SERVER_REQUEST_ADDED_NOTICE = 'Request of adding authentication certificate to existing security server \'SERVER:{0}\' added successfully'
SUBSYSTEM_DELETION_COMMENT = '\'SUBSYSTEM:{0}/{1}/{2}/{3}\' deletion'
CERTIFICATE_IMPORT_EXPIRED_GLOBAL_CONF_ERROR = 'Failed to import certificate: Global configuration is expired'
REQUEST_REVOKE_SUCCESSFUL_NOTICE = 'Successfully revoked client registration request with id \'{0}\''
AUTH_REQUEST_REVOKE_SUCCESSFUL_NOTICE = 'Successfully revoked authentication request with id \'{0}\''
GLOBAL_CONF_EXPIRED_MESSAGE = 'Global configuration is expired'
UNREGISTER_CERT_FAIL_NO_VALID_CERT = 'Failed to unregister certificate: Security server has no valid authentication certificate'

# Client registration request confirmation message, {0}=subsystem, {1}=client name, {2}=client class, {3}=client code
CLIENT_REGISTRATION_SUBSYSTEM_CONFIRMATION = 'Do you want to send a client registration request for the added client?\n' \
                                             'New subsystem \'{0}\' will be submitted for registration for member \'{1} {2}: {3}\'.'
CLIENT_REGISTRATION_CONFIRMATION = 'Do you want to send a client registration request for the added client?'

# For CLIENT_REGISTRATION_* {0} is replaced with the client X-Road identifier, {1} is replaced with the X-Road server identifier
CLIENT_REGISTRATION_SUCCESS = "Request of adding client '{0}' to security server '{1}' added successfully"
CLIENT_REGISTRATION_ALREADY_REGISTERED = "Failed to add new server client request: '{0}' has already been registered as a client to security server '{1}'"
CLIENT_REGISTRATION_ALREADY_REQUESTED = "Failed to add new server client request: A request for registering '{0}', as a client to security server '{1}' has already been submitted"
CLIENT_REGISTRATION_FAIL_REGEX = "^Failed to send registration request\: .*"

KEY_GENERATION_TIMEOUT_ERROR = 'Connection to Signer (port 5558) timed out'
SERVER_UNREACHABLE_ERROR = 'Server unreachable. Make sure if server is up and running.'
ADD_CENTRAL_SERVICE_EXISTS_ERROR = 'Failed to save central service: \'{0}\' has already been taken'
ADD_CENTRAL_SERVICE_PROVIDER_NOT_FOUND_ERROR = 'Failed to save central service: Provider with ID \'SUBSYSTEM:{0}/{1}/{2}/{3}\' not found'
EDIT_CENTRAL_SERVICE_PROVIDER_NOT_FOUND_ERROR = 'Failed to update central service: Provider with ID \'SUBSYSTEM:{0}/{1}/{2}/{3}\' not found'

UNREGISTER_CLIENT_SEND_REQUEST_FAIL = 'Failed to send deletion request: Service {0} is disabled: Out of order'
GENERATE_CERTIFICATE_NOT_FOUND_ERROR = 'Failed to generate new key: /bin/sh: 1: {0}: not found'
GENERATE_CERTIFICATE_NOT_FOUND_ERROR_REGEX = 'Failed to generate new key: .*: {0}: not found'
REGISTRATION_REQUEST_SENDING_FAILED = 'Failed to send registration request: Service .* is disabled: Out of order'
CERTIFICATE_DELETION_REQUEST_SENDING_FAILED = 'Failed to send certificate deletion request. Continue with certificate deletion anyway?'
UNREGISTER_CERT_REQUEST_SENDING_FAILED = 'Failed to unregister certificate: Could not connect to any target host'
SS_CONFIGURATION_BACKUP_ERROR = "Failed to back up configuration: Error making configuration backup, script exited with status code '1'"
SS_SUCCESSFUL_DELETE = 'Selected backup deleted successfully'
INPUT_EXCEEDS_255_CHARS = 'Parameter \'{0}\' input exceeds 255 characters'
INVALID_HOST_ADDRESS = 'Invalid host address'
FAILED_TO_REGISTER_CONNECTION_REFUSED_ERROR = 'Failed to register certificate: ConnectException: Connection refused (Connection refused)'

UPLOAD_CONTAIN_INVALID_CHARACTERS = 'Failed to upload new backup file: Filename \'{0}\' contains invalid characters. Valid characters include: (A-Z), (a-z), (0-9), (_), (.), (-).'
UPLOAD_WRONG_EXTENSION = 'Failed to upload new backup file: Uploaded file name \'{0}\' has an invalid extension, the only valid one is \'tar\''

DELETE_ANCHOR_SUCCESS_MSG = 'Configuration anchor of instance \'{}\' deleted successfully.'
UPLOAD_ANCHOR_SIGNATURE_ERROR = 'Failed to save uploaded trusted anchor: ' \
                                 'Signature of configuration cannot be verified'
UPLOAD_ANCHOR_EXPIRED_ERROR = 'Failed to save uploaded trusted anchor: ' \
                                 'Configuration from source is out of date'
UPLOAD_ANCHOR_URL_UNREACHABLE_ERROR = 'Failed to save uploaded trusted anchor: ' \
                                 'Configuration source cannot be reached, check source URL in uploaded anchor file'
UPLOAD_ANCHOR_INVALID_FILE_ERROR = 'Failed to upload trusted anchor: ' \
                                 'Incorrect file structure.'
UPLOAD_ANCHOR_UNKNOWN_ERROR = 'Failed to save uploaded trusted anchor: ' \
                                 'Configuration from source failed verification'
UPLOAD_ANCHOR_INTERNAL_CONF_ERROR = 'Failed to save uploaded trusted anchor: ' \
                                 'Anchor points to an internal configuration source. ' \
                                 'Only external configuration source anchors are supported as trusted anchors'
UPLOAD_ANCHOR_SAME_INSTANCE_ERROR = 'Failed to upload trusted anchor: Anchors originating from this instance are not supported as trusted anchors.'
CERT_ALREADY_SUBMITTED_ERROR_BEGINNING = 'Failed to add authentication certificate adding request: Certificate is already submitted for registration with request'
UPLOAD_WRONG_FORMAT = 'Failed to upload new backup file: Content of uploaded file must be in tar format'
UPLOAD_EXISTS = 'Backup file with name \'{0}\' already exists, do you want to overwrite it?'
TOKEN_DETAILS_MISSING_PARAMETER = 'Missing parameter: friendly_name'
TOKEN_PIN_INCORRECT = 'PIN incorrect'
HARDTOKEN_PIN_INCORRECT = 'Login failed: CKR_PIN_INCORRECT'
HARDTOKEN_PIN_INCORRECT_2TRY = 'Login failed: CKR_PIN_INCORRECT, tries left: 1'
HARDTOKEN_PIN_INCORRECT_3TRY = 'Login failed: CKR_PIN_INCORRECT. PIN locked.'
HARDTOKEN_PIN_INCORRECT_PIN_LOCKED = 'PIN locked'
HARDTOKEN_PIN_INCORRECT_FORMAT = 'PIN format incorrect'
HARDTOKEN_LOGIN_FAILED = 'Login failed: CKR_USER_PIN_NOT_INITIALIZED'
HARDTOKEN_LOGOUT_FAILED = 'CKR_DEVICE_ERROR'
HARDTOKEN_KEY_DELETE_FAILED = "Failed to delete key: Failed to delete private key \'{0}\' on token 'utimaco-UTIMACO CS000000-CryptoServer PKCS11 Token': iaik.pkcs.pkcs11.wrapper.PKCS11Exception: CKR_DEVICE_ERROR"

KEY_DELETE_FAILED_CONNECTION_REFUSED = 'Failed to delete key: ConnectException: Connection refused (Connection refused)'

KEY_DELETE_FAILED_SERVICE_DISABLED_ERROR_MSG_REGEX = 'Failed to delete key: Service .+authCertDeletion is disabled: Out of order'
KEY_DELETE_SENDING_FAILED = 'Failed to delete key: Could not connect to any target host .*'
MANAGEMENT_SERVICE_REGISTERED = 'Management service provider \'.*\' registered as security server \'.*\' client'
MANAGEMENT_SERVICE_ADDED_COMMENT = 'Management service provider registration'
DECLINED_REQUEST_NOTICE = 'Successfully declined request with id \'{0}\''

SECURITY_SERVER_CODE_ALREADY_REGISTRED = 'Failed to add new owned server request: Server with owner class \'{0}\', owner code \'{1}\' and server code \'{2}\' already exists.'
AUTH_CERT_ALREADY_REGISTRED = "Failed to add new owned server request: Certificate is already registered, request id \'"
RESTORE_CONFIGURATION_FAILED = 'Failed to restore configuration: Restoring configuration from file \'{0}\' failed.'
BACKUP_CONFIGURATION_RESTORED_SUCCESSFUL = "Configuration restored successfully from file \'{0}\'."

CP_CONF_DOWNLOAD_REQUEST_ERROR_1 = 'Failed to download configuration from any configuration location:'
CP_CONF_DOWNLOAD_REQUEST_ERROR_2 = 'Error when downloading conf'
CP_CONF_DOWNLOAD_REQUEST_ERROR_3 = 'HttpError: {0}'
CP_DOWNLOAD_UPDATE_CONFIGURATION_ERROR = 'ERROR e.r.x.c.c.g.ConfigurationClient - Failed to download configuration from any configuration location:'
CP_DOWNLOAD_UPDATE_CONFIGURATION_LOCATION_ERROR = 'location: http://{0}/internalconf?version=2; error: HttpError: {0}'
CP_DOWNLOAD_SUCCESSFULL = 'Downloading configuration from http://{0}/internalconf?version=2'
SECURITY_SERVER_CLIENT_DELETION_REQUEST = 'Request of deleting client \'SUBSYSTEM:{0}/{1}/{2}/{3}\' from security server \'SERVER:{4}/{5}/{6}/{7}\' added successfully'


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


def get_auth_cert_del_req_added_message(client):
    return DELETE_AUTH_CERT_REQ_ADDED.format(
        'SERVER:{0}/{1}/{2}/{3}'.format(client['instance'], client['class'], client['code'], client['server_name']))


def get_cert_adding_existing_server_req_added_notice(client):
    return CERTIFICATE_ADDING_EXISTING_SERVER_REQUEST_ADDED_NOTICE.format(
        '{0}/{1}/{2}/{3}'.format(client['instance'], client['class'], client['code'], client['server_name']))
