import re

from helpers.list_utils import flatten
from helpers.ssh_server_actions import exec_as_xroad
from view_models.configuration_proxy import ACTIVE_KEY_CONFIG_LINE, SIGNING_KEY_CONFIG_LINE, ADDED_KEY_TO_CONF_INI, \
    NO_ACTIVE_KEY, KEY_ID_REGEX, CERT_FILE_REGEX


def generate_signing_key(self, sshclient, cp_identifier, conf_path, token_id, no_active_key=False):
    def generate_key():
        self.log(
            'CP_09 1. Adding new signing key to configuration proxy {0} and token {1}'.format(cp_identifier, token_id))
        std_out = exec_as_xroad(sshclient, 'confproxy-add-signing-key -p {0} -t {1}'.format(cp_identifier, token_id))
        output = flatten(std_out)

        self.log('CP_09 2. System generates a new configuration signing key on the referred token')
        key_id = get_regex_first_group_match_from_list(KEY_ID_REGEX, output)
        self.is_not_none(key_id, msg='Key id not found from stdout')
        key_file_name = '{}.p12'.format(key_id)
        self.log('Checking if key file "{}" exists'.format(key_file_name))
        std_out = sshclient.exec_command('sudo ls /etc/xroad/signer | grep {}'.format(key_file_name))
        self.is_equal(std_out[0][0], key_file_name)

        self.log('CP_09 2. System generates a corresponding self-signed certificate')
        cert_file_name = get_regex_first_group_match_from_list(CERT_FILE_REGEX, output)
        self.is_not_none(cert_file_name, msg='Cert filename not found from stdout')
        self.log('Checking if cert file "{} exists"'.format(cert_file_name))
        std_out = sshclient.exec_command('sudo ls {0} | grep {1}'.format(conf_path.replace('conf.ini', ''), cert_file_name))
        self.is_equal(std_out[0][0], cert_file_name)

        self.log('CP_09 3. System saves the generated key information and '
                 'the certificate to the proxy instance settings file')
        if no_active_key:
            expected_msg = NO_ACTIVE_KEY
            self.log('Checking success message "{}"'.format(expected_msg))
            self.is_true(any(expected_msg == a for a in output), msg='"{}" not found from stdout'.format(expected_msg))

            expected_line = ACTIVE_KEY_CONFIG_LINE.format(key_id)
            self.log('Checking if new key is set as active key in conf.ini')
            std_out = sshclient.exec_command(
                'sudo grep \'{0}\' {1}'.format(expected_line, conf_path))
            self.is_equal(expected_line, std_out[0][0])

        expected_msg = ADDED_KEY_TO_CONF_INI
        self.log('Checking success message "{}"'.format(expected_msg))
        self.is_true(any(expected_msg == a for a in output), msg='"{}" not found from stdout'.format(expected_msg))

        expected_line = SIGNING_KEY_CONFIG_LINE.format(key_id)
        self.log('Checking if "{}" is present in "conf.ini"'.format(expected_line))
        std_out = sshclient.exec_command('sudo grep \'{0}\' {1}'.format(expected_line, conf_path))
        self.is_true(re.match(expected_line, std_out[0][0]), msg='"{}" not found in conf.ini'.format(expected_line))

    return generate_key


def get_regex_first_group_match_from_list(regex, output):
    for line in output:
        if re.match(regex, line):
            return re.search(regex, line).group(1)
    return None
