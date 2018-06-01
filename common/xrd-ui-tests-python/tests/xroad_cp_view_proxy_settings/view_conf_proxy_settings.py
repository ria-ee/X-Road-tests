from helpers.list_utils import flatten
from helpers.ssh_server_actions import exec_as_xroad
from tests.xroad_cp_activate_configuration_source_signing_key.activate_configuration_source_signing_key import \
    get_all_signing_keys
from view_models.configuration_proxy import CP_CONF_HEADING, get_cp_view_anchor_fields, \
    get_cp_view_configuration_url_field, get_cp_view_signing_keys, VALIDITY_STDOUT_LINE, VALIDITY_DEFAULT_TIMEOUT, \
    CP_ANCHOR_NOT_FOUND_ERROR_MSG, CP_NO_VALIDITY_INTERVAL_ERROR_MSG, CP_NO_ACTIVE_SIGNING_KEY_ERROR_MSGS
import time, re

def test_view_all_cp_settings(self, sshclient, cp_identifier, empty_cp_identifier, cp_conf_location,
                              empty_cp_anchor_location, cs_identifier, cp_conf_url, empty_cp_conf_url):
    def view_all_cp_settings():
        self.log('CP_01 1. Trying to view all proxy instance settings.')
        std_out = flatten(exec_as_xroad(sshclient, 'confproxy-view-conf -a'))
        self.log('Finding "{}" proxy part from output'.format(cp_identifier))

        # Get and format the CP configuration start heading for main and empty cp
        cp_heading = CP_CONF_HEADING.format(cp_identifier)
        empty_cp_heading = CP_CONF_HEADING.format(empty_cp_identifier)
        # Generate generic regex for all CP headings
        cp_regex = re.compile(CP_CONF_HEADING.format('.*'))

        # Init start and end line variables
        empty_cp_start = None
        empty_cp_end = None
        cp_start = None
        cp_end = None

        for i in range(0, len(std_out)):
            line = std_out[i]

            # If CP config (main and empty) section start found and end not found, a new config ends previous section
            if cp_start is not None and cp_end is None and cp_regex.match(line):
                cp_end = i - 1
            elif empty_cp_start is not None and empty_cp_end is None and cp_regex.match(line):
                empty_cp_end = i

            # If a CP config start section found, save the line
            if cp_heading in line:
                cp_start = i
            elif empty_cp_heading in line:
                empty_cp_start = i

        # If no end line found, section may end at output end
        if empty_cp_end is None:
            empty_cp_end = len(std_out) - 1
        if cp_end is None:
            cp_end = len(std_out) - 1

        # Save the configs
        cp_conf = std_out[cp_start:cp_end]
        empty_cp_conf = std_out[empty_cp_start:empty_cp_end]
        self.log('Getting "{}" proxy signing keys from configuration file'.format(cp_identifier))
        keys = set(get_all_signing_keys(sshclient, cp_conf_location))
        self.log(
            'CP_01 2. System displays the following information of the "{}" proxy instance: '.format(cp_identifier))
        check_cp_view_lines(self, cp_conf, cs_identifier, cp_conf_url, keys)
        self.log('CP_01 2a. System show errors for the missing parts of the settings')
        check_empty_cp_view_lines(self, empty_cp_conf, empty_cp_anchor_location, empty_cp_conf_url)

    return view_all_cp_settings


def check_empty_cp_view_lines(self, conf_lines, cp_anchor_location, conf_url):
    expected_msg = CP_ANCHOR_NOT_FOUND_ERROR_MSG.format(cp_anchor_location)
    self.log('Checking for trusted anchor missing error "{}"'.format(expected_msg))
    self.is_true(any(expected_msg in a for a in conf_lines), msg='Expected error not found')

    expected_msg = CP_NO_VALIDITY_INTERVAL_ERROR_MSG
    self.log('Checking for not configured validity interval error "{}"'.format(expected_msg))
    self.is_true(any(expected_msg in a for a in conf_lines), msg='Expected error not found')

    expected_msgs = CP_NO_ACTIVE_SIGNING_KEY_ERROR_MSGS
    self.log('Checking for not configured active signing key error "{}"'.format(' '.join(expected_msgs)))
    self.is_true(all(any(msg in a for a in conf_lines) for msg in expected_msgs), msg='Expected error not found')

    expected_msgs = get_cp_view_configuration_url_field(conf_url)
    self.log('Checking if configuration URL "{}" present'.format(conf_url))
    self.is_true(all(any(msg in a for a in conf_lines) for msg in expected_msgs), msg='Configuration URL not found')


def check_cp_view_lines(self, conf_lines, cs_identifier, conf_url, keys):
    time.sleep(3)
    expected_msgs = get_cp_view_anchor_fields(cs_identifier)
    self.log('Checking if trusted anchor fields "{}" are visible'.format(', '.join(expected_msgs)))
    self.is_true(all(any(expected_msg in a for a in conf_lines) for expected_msg in expected_msgs),
                 msg='Expected fields not found')

    expected_msgs = get_cp_view_configuration_url_field(conf_url)
    self.log('Checking if configuration url "{}" is visible'.format(conf_url))
    self.is_true(all(any(expected_msg in a for a in conf_lines) for expected_msg in expected_msgs),
                 msg='Configuration url not visible')

    expected_msgs = get_cp_view_signing_keys()
    self.log('Checking if signing keys and certificates part is visible')
    self.is_true(all(any(expected_msg in a for a in conf_lines) for expected_msg in expected_msgs),
                 msg='Signing keys and certificates part is not visible')

    expected_msg = VALIDITY_STDOUT_LINE.format(VALIDITY_DEFAULT_TIMEOUT)
    self.log('Checking if validity interval field is visible')
    self.is_true(any(expected_msg in a for a in conf_lines), msg='Validity interval row is not visible')

    self.is_true(all(
        any('{0} (Certificate: /etc/xroad/confproxy/cp-test/cert_{0}.pem'.format(key) in a for a in conf_lines) for key
        in keys), msg='Keys and certificates are not visible')

    active_heading_index = conf_lines.index('active-signing-key-id:')
    signing_key_heading_index = conf_lines.index('signing-key-id-*:')
    self.log('Checking if active signing key row is visible')
    active_signing_key = conf_lines[(active_heading_index + signing_key_heading_index) / 2]
    self.is_not_none(active_signing_key, msg='Active signing key row not visible')
