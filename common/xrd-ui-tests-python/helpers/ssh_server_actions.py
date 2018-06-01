import json
import re

import time

import datetime

import ssh_client
from view_models import keys_and_certificates_table

def exec_commands(self, sshclient, commands, timeout=1):
    channel = sshclient.invoke_shell()
    time.sleep(1)
    channel.recv(9999)
    output = None
    for command in commands:
        self.log('Sending "{}" to stdin'.format(command))
        channel.send(command + "\n")
        while not channel.recv_ready():  # Wait for the server to read and respond
            time.sleep(0.1)
        time.sleep(timeout)
        output = channel.recv(9999) # read in
        time.sleep(0.1)
    channel.close()
    return output

def exec_as_xroad(sshclient, command):
    stdout, stderr = sshclient.exec_command('sudo -Hu {0} {1}'.format('xroad', command), sudo=True)
    return stdout, stderr

def refresh_ocsp(sshclient):
    sshclient.exec_command(command='rm /var/cache/xroad/*ocsp', sudo=True)
    sshclient.exec_command(command='service xroad-signer restart', sudo=True)
    sshclient.exec_command(command='service xroad-proxy restart', sudo=True)


def get_server_time(ssh_host, ssh_username, ssh_password):
    """
        Creates connection to ss_host with ssh_username and ssh_password and retrieves server date
    :param ssh_host: string (only hostname)
    :param ssh_password: string
    :param ssh_username: string
    :return: return datettime object of current server systen time
    """
    client = ssh_client.SSHClient(ssh_host, username=ssh_username, password=ssh_password)
    output, out_error = client.exec_command('date "+%y-%m-%d %H:%M:%S.%6N"')
    time = datetime.datetime.strptime(output[0], '%y-%m-%d %H:%M:%S.%f')
    client.close()
    return time


def get_history_for_user(client, database_user, database, user, limit):
    return client.exec_command(
        'psql -A -t -F"," -U {0} -d {1} -c "select table_name, operation, timestamp from history where user_name like \'{2}\' group by table_name, operation, timestamp order by timestamp desc limit {3}"'.format(
            database_user, database, user, limit))


def get_log_lines(client, file_name, lines):
    log_regex = re.compile(
        r'^(([0-9]{4}-[0-9]{2}-[0-9]{2})T(([0-9]{2}:[0-9]{2}:[0-9]{2})(\+[0-9]{2}:[0-9]{2}))) ([^ ]+) ([^ ]+) +(\[([^\]]+)\]) (([0-9]{4}-[0-9]{2}-[0-9]{2}) (([0-9]{2}:[0-9]{2}:[0-9]{2})(\+[0-9]{4}))) ([^ ]+) (.*)$')
    # Execute command, read output (stdout, stderr)
    out_clean, out_error = client.exec_command('tail -{0} {1}'.format(lines, file_name), sudo=True)

    # Loop over stdout lines
    for line in out_clean:
        row = line.strip('\n')  # Remove newline character
        result = log_regex.match(row)  # Match
        if result:
            # Load json data
            data = json.loads(result.group(16))

            # Create result object
            return {
                'timestamp': result.group(1),  # rfc3339 (syslog)
                'date': result.group(2),  # date only (syslog)
                'time_tz': result.group(3),  # time with timezone (syslog)
                'time': result.group(4),  # time only (syslog)
                'timezone': result.group(5),  # timezone only (syslog)
                'hostname': result.group(6),  # system hostname
                'type': result.group(7),  # message type (example: INFO)
                'msg_service': result.group(9),  # service (example: X-Road Proxy UI)
                'msg_timestamp': result.group(10),  # message timestamp
                'msg_date': result.group(11),  # message date
                'msg_time_tz': result.group(12),  # message time with timezone
                'msg_time': result.group(13),  # message time only
                'msg_timezone': result.group(14),  # message timezone only
                'data': data  # data from message json
            }


def get_key_conf_keys_count(sshclient, key_type):
    """
    Gets count of keys of specified type in system configuration
    :param sshclient: obj - sshclient instance
    :param key_type: str - key type
    :return:
    """
    return sshclient.exec_command(command='grep "key usage=\\\"{0}\\\"" {1} | wc -l'.format(key_type,
                                                                                            keys_and_certificates_table.KEY_CONFIG_FILE),
                                  sudo=True)[0][0]


def get_key_conf_token_count(sshclient):
    """
    Gets count of device objects in system configuration
    :param sshclient: obj - sshclient instance
    :return:
    """
    return \
        sshclient.exec_command(command='grep "<device>" {0} | wc -l'.format(keys_and_certificates_table.KEY_CONFIG_FILE),
                               sudo=True)[0][0]


def get_key_conf_csr_count(sshclient):
    """
    Gets count of csr objects in system configuration
    :param sshclient: sshclient instance
    :return:
    """
    return sshclient.exec_command(
        command='grep "<certRequest.*>" {0} | wc -l'.format(keys_and_certificates_table.KEY_CONFIG_FILE), sudo=True)[0][
        0]
def get_server_name(self):
    return self.by_id('server-info').get_attribute('data-instance')


def get_client(ssh_host, ssh_username, ssh_password):
    return ssh_client.SSHClient(ssh_host, username=ssh_username, password=ssh_password)


def cp(ssh_client_instance, src, destination, sudo=False):
    cp_command = 'cp -p {0} {1}'.format(src, destination)
    return ssh_client_instance.exec_command(cp_command, sudo)


def mv(ssh_client_instance, src, destination, sudo=False):
    mv_command = 'mv {0} {1}'.format(src, destination)
    return ssh_client_instance.exec_command(mv_command, sudo)

def get_keyconf_update_timeout(sshclient):
    server_time = int(sshclient.exec_command('date +"%s"')[0][0])
    file_modified = int(sshclient.exec_command('date +"%s" -r {}'.format('/etc/xroad/signer/keyconf.xml'), sudo=True)[0][0])
    ago = server_time - file_modified
    return 65 - ago

def get_certificate_filename(cert_hex):
    """
    Returns the filename of the certificate (relative to CA program location)
    :param cert_hex: str - uppercase hex string representation of the cert identifier
    :return: str - filename of the certificate
    """
    newcerts_base = './newcerts'
    if len(cert_hex) % 2 == 1:
        cert_filename = '{0}/0{1}.pem'.format(newcerts_base, cert_hex)
    else:
        cert_filename = '{0}/{1}.pem'.format(newcerts_base, cert_hex)

    return cert_filename


def get_certificate_id_from_text(text):
    """
    Returns the certificate identifier number from full text in the table row.
    :param text: str - key friendly name
    :return: str - certificate identifier as hex string
    """
    element_text = text.strip()

    # Split the element by space and get the last part of it as this is the key id as a decimal
    cert_id = int(element_text.rsplit(' ', 1)[-1])
    cert_hex = '{0:02x}'.format(cert_id).upper()
    return cert_hex


def get_valid_certificates(self, client):
    """
    Gets a list of the client's certificates that may be revoked.
    :param self: MainController object
    :param client: dict - client data
    :return: [str] - list of certificate filenames to revoke
    """
    # Initialize the list of certificates to revoke. Because we are deleting the key, we need to revoke all certificates
    # under it.
    certs_to_revoke = []

    # Try to get the certificates under the generated keys
    key_num = 1
    while True:
        try:
            key_friendly_name_xpath = keys_and_certificates_table.get_generated_key_row_active_cert_friendly_name_xpath(
                client['code'], client['class'], key_num)
            key_name_element = self.by_xpath(key_friendly_name_xpath)
            """
            element_text = key_name_element.text.strip()
            # Split the element by space and get the last part of it as this is the key id as a decimal
            cert_id = int(element_text.rsplit(' ', 1)[-1])
            cert_hex = '{0:02x}'.format(cert_id).upper()
            """
            cert_hex = get_certificate_id_from_text(key_name_element.text)
            # Key filenames are of even length (zero-padded) so we'll generate one like that
            cert_filename = get_certificate_filename(cert_hex)
            certs_to_revoke.append(cert_filename)
        except:
            # Exit loop if element not found (= no certificates listed)
            break
        key_num += 1

    return certs_to_revoke


