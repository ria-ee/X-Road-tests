from helpers.list_utils import flatten
from helpers.ssh_server_actions import exec_as_xroad
from view_models.configuration_proxy import ACTIVE_KEY_CONFIG_LINE, ALL_SIGNING_KEYS_REGEX


def activate_signing_key(self, sshclient, conf_path, cp_identifier):
    self.log('Getting all signing keys from conf.ini')
    keys = get_all_signing_keys(sshclient, conf_path)
    self.log('Getting active key id from confproxy')
    active_key = get_active_key(sshclient, cp_identifier)
    self.log('Getting inactive key id from signing keys')
    inactive_key = get_first_inactive_key(active_key, keys)
    self.log('\nActive key: {0}\nInactive key: {1}'.format(active_key, inactive_key))
    self.log('CP_10 1. Editing the active key identifier in {}\'s conf.ini'.format(cp_identifier))
    set_active_key(sshclient, active_key, inactive_key, conf_path)
    self.log('CP_10 2. System starts using the activated key')
    self.log('Checking if active key is equal to {}'.format(inactive_key))
    new_active_key = get_active_key(sshclient, cp_identifier)
    self.is_equal(inactive_key, new_active_key)


def get_all_signing_keys(sshclient, conf_path):
    return [key_row.split(' = ')[1] for key_row in flatten(sshclient.exec_command(
        'grep \'{0}\' {1}'.format(ALL_SIGNING_KEYS_REGEX, conf_path)))]


def set_active_key(sshclient, active_key, inactive_key, conf_path):
    sshclient.exec_command(
        'sed -i -e "s/{0}/{1}/g" {2}'.format(ACTIVE_KEY_CONFIG_LINE.format(active_key),
                                             ACTIVE_KEY_CONFIG_LINE.format(inactive_key),
                                             conf_path),
        sudo=True)


def get_active_key(sshclient, cp_identifier):
    return exec_as_xroad(sshclient,
                         'confproxy-view-conf -p {} | grep -A1 \'active-signing-key-id:\' |'
                         ' tail -1 | cut -d " " -f 1'.format(
                             cp_identifier))[0][0].strip()


def get_first_inactive_key(active_key, keys):
    return filter(lambda x: x != active_key, keys)[0]
