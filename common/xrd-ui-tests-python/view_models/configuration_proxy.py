VALIDITY_CONFIG_LINE = 'validity-interval-seconds = {}'
VALIDITY_STDOUT_LINE = 'Validity interval: {} s.'
VALIDITY_DEFAULT_TIMEOUT = '600'
KEY_CERT_MISSING_STDOUT = '{} (CERTIFICATE FILE MISSING!)'
ADDED_KEY_TO_CONF_INI = 'Added key to conf.ini'
NO_ACTIVE_KEY = 'No active key configured, setting new key as active in conf.ini'
ACTIVE_SIGNING_KEY_PARAM_NAME = 'active-signing-key-id'
ACTIVE_KEY_CONFIG_LINE = ACTIVE_SIGNING_KEY_PARAM_NAME + ' = {}'
SIGNING_KEY_CONFIG_LINE = '^signing-key-id-.* = {}$'
CP_CREATION_CP_EXISTS_MESSAGE = 'Configuration for instance \'{}\' already exists, aborting.'
PIN_INCORRECT_ERROR_MSG = 'PIN incorrect'
ALL_SIGNING_KEYS_REGEX = 'signing-key-id-*.* = .*$'
KEY_ID_REGEX = 'Generated key with ID (.*)'
CERT_FILE_REGEX = 'Saved self-signed certificate to (.*)'
ACTIVE_CERT_DELETE_MSG = 'Not allowed to delete an active signing key!'
KEY_ID_NOT_FOUND_MSG = 'The key ID \'{}\' could not be found in \'conf.ini\'.'
CP_CONF_DOES_NOT_EXIST_MSG = 'Configuration for proxy instance \'{}\' does not exist.'
CP_CONF_HEADING = 'Configuration for proxy \'{}\''
DATE_TIME_REGEX = '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z'
ANCHOR_INSTANCE_IDENTIFIER = 'Instance identifier: {0}'
ANCHOR_HASH = 'Hash:                {0}'
ANCHOR_GENERATED_AT = 'Generated at:        {0}'
IDENTIFIERS = ['PRIVATE-PARAMETERS', 'SHARED-PARAMETERS']
CP_ANCHOR_NOT_FOUND_ERROR_MSG = '\'anchor.xml\' could not be loaded: IOError: {} (No such file or directory)'
CP_NO_VALIDITY_INTERVAL_ERROR_MSG = 'Validity interval: NOT CONFIGURED (add \'validity-interval-seconds\' to \'conf.ini\')'
CP_NO_ACTIVE_SIGNING_KEY_ERROR_MSGS = ['active-signing-key-id:',
                                       'NOT CONFIGURED (add \'active-signing-key-id\' to \'conf.ini\'']
NO_SIGNING_KEYS_CONFIGURED_ERROR_MSG = 'No signing keys configured!'
CP_ANCHOR_TIME_REGEX = '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z'
GENERATED_ANCHOR_XML_TO_MSG = 'Generated anchor xml to \'{}\''
CP_SHARED_PARAMETERS = 'Saving content to file /tmp/test_download/KS1/shared-params.xml'
CP_PRIVATE_PARAMETERS = 'Saving content to file /tmp/test_download/KS1/private-params.xml'


def get_cp_no_conf_file_errors(cp_identifier):
    return ['Could not load configuration for \'{}'.format(cp_identifier), '\'conf.ini\' does not exist.']


def get_cp_could_not_load_source_anchor_errors(cp_instance):
    return ['Could not load source anchor:',
            'IOError: /etc/xroad/confproxy/{}/anchor.xml (No such file or directory)'.format(cp_instance)]


def get_cp_view_configuration_url_field(conf_url):
    return ['Configuration URL', conf_url]


def get_cp_view_anchor_fields(cs_identifier):
    return ['anchor.xml', 'Instance identifier: {}'.format(cs_identifier), 'Generated at:', 'Hash:']


def get_cp_view_signing_keys():
    return ['Signing keys and certificates', 'active-signing-key-id', 'signing-key-id-*']


def get_cp_key_deletion_success_messages(key_id):
    return ['Deleted key from signer',
            'Deleted key from \'conf.ini\'.',
            'Deleted self-signed certificate \'cert_{}.pem\''.format(key_id)]


def get_cp_creation_success_messages(identifier):
    return ['Generating configuration directory for instance \'{}\' ...'.format(identifier),
            'Populating \'conf.ini\' with default values ...',
            'Done.']
