from helpers.list_utils import flatten
from helpers.ssh_server_actions import exec_as_xroad
from view_models.configuration_proxy import VALIDITY_CONFIG_LINE, VALIDITY_STDOUT_LINE, VALIDITY_DEFAULT_TIMEOUT, \
    KEY_CERT_MISSING_STDOUT


def test_edit_settings_file(self, sshclient, cp_identifier, cp_conf):
    def edit_settings_file():
        new_key_id = 'UniqueKeyId'
        new_timeout = '601'
        self.log('CP_10 Adding new signing key line to conf.ini')
        sshclient.exec_command('sh -c "echo \'signing-key-id-1 = {0}\' >> {1}"'.format(new_key_id, cp_conf))
        self.log('Checking if change is reflected in configuration proxy view')
        std_out = flatten(
            exec_as_xroad(sshclient, 'confproxy-view-conf -p {0} | grep {1}'.format(cp_identifier, new_key_id)))
        expected = KEY_CERT_MISSING_STDOUT.format(new_key_id)
        self.log('Checking if line "{}" is present'.format(expected))
        self.is_equal(expected, std_out[0].strip())

        self.log('CP_10 Deleting conf.ini last line(previously added key)')
        sshclient.exec_command('sed -i \'$ d\' {}'.format(cp_conf))
        self.log('Checking if change is reflected in configuration proxy view')
        std_out = flatten(
            exec_as_xroad(sshclient, 'confproxy-view-conf -p {0} | grep {1}'.format(cp_identifier, new_key_id)))
        self.log('Checking if "{}" not present'.format(new_key_id))
        self.is_false(any(new_key_id in a for a in std_out))

        self.log('CP_10 changing validity timeout to {}'.format(new_timeout))
        sshclient.exec_command(
            'sed -i -e "s/{0}/{1}/g" {2}'.format(VALIDITY_CONFIG_LINE.format(VALIDITY_DEFAULT_TIMEOUT),
                                                 VALIDITY_CONFIG_LINE.format(new_timeout),
                                                 cp_conf))

        self.log('Checking if change is reflected in configuration proxy view')
        expected_line = VALIDITY_STDOUT_LINE.format(new_timeout)
        self.log('Checking if line "{}" is present'.format(expected_line))
        std_out = flatten(exec_as_xroad(sshclient, 'confproxy-view-conf -p {0} | grep \'{1}\''.format(cp_identifier,
                                                                                                      expected_line)))
        self.is_equal(expected_line, std_out[0].strip())

    return edit_settings_file
