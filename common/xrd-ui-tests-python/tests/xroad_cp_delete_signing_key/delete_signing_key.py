from helpers.list_utils import flatten
from helpers.ssh_server_actions import exec_as_xroad
from tests.xroad_cp_activate_configuration_source_signing_key.activate_configuration_source_signing_key import \
    get_active_key
from view_models.configuration_proxy import ACTIVE_CERT_DELETE_MSG, get_cp_key_deletion_success_messages, \
    KEY_ID_NOT_FOUND_MSG


def test_delete_signing_key(self, sshclient, cp_identifier, key_id, conf_path, active=False, not_exists=False):
    def delete_signing_key():
        self.log('CP_11 1. Trying to delete key with id "{}"'.format(key_id))
        std_out = flatten(
            exec_as_xroad(sshclient, 'confproxy-del-signing-key -p {0} -k {1}'.format(cp_identifier, key_id)))
        if active:
            self.log('CP_11 1a Trying to delete active key')
            expected_msg = ACTIVE_CERT_DELETE_MSG
            self.log('CP_11 1a.1 System notifies with error message "{}"'.format(expected_msg))
            self.is_true(any(expected_msg in a for a in std_out), msg='"{}" not found in stdout'.format(expected_msg))
            self.log('Checking if {} is still active key'.format(key_id))
            self.is_equal(key_id, get_active_key(sshclient, cp_identifier))
            self.log('Checking if key and cert still present in token')
            self.is_true(key_and_cert_present_in_token(sshclient, key_id))
        elif not_exists:
            self.log('CP_11 1b Trying to delete not existing key')
            expected_msg = KEY_ID_NOT_FOUND_MSG.format(key_id)
            self.log('CP_11 1b.1 System notifies with error message "{}"'.format(expected_msg))
            self.is_true(any(expected_msg in a for a in std_out), msg='{} not found in stdout'.format(expected_msg))
        else:
            expected_msgs = get_cp_key_deletion_success_messages(key_id)
            self.log('Checking if messages {} present in std_out'.format(expected_msgs))
            self.is_true(all(any(a in x for x in std_out) for a in expected_msgs))
            self.log('CP_11 2. Checking if key and cert were deleted from token')
            self.is_false(key_and_cert_present_in_token(sshclient, key_id))
            self.log('CP_11 2. Checking if key id is deleted from \'conf.ini\'')
            std_out = sshclient.exec_command(
                'grep \'{0}\' {1}'.format(key_id, conf_path, cp_identifier))
            self.is_false(any(key_id in a for a in std_out))

    return delete_signing_key


def key_and_cert_present_in_token(sshclient, key_id):
    std_out = flatten(exec_as_xroad(sshclient, 'signer-console lc | grep {}'.format(key_id)))
    return any(key_id in a for a in std_out)
