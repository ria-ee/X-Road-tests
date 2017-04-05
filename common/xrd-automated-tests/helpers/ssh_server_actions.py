import datetime
import json
import re
import ssh_client


def get_server_time(ssh_host, ssh_username, ssh_password):
    """
        Creates connection to ss_host with ssh_username and ssh_password and retrieves server date
    :param ssh_host: string (domain and extension eg. "xtee.asa")
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
    # return client.exec_command(
    #     'psql -A -t -F"," -U ' + database_user + ' -d ' + database +
    #     ' -c "select table_name, operation, timestamp from history where user_name like \'' + user +
    #     '\' group by table_name, operation, timestamp order by timestamp desc limit ' + str(
    #         limit) + '"')
    return client.exec_command(
        'psql -A -t -F"," -U {0} -d {1} -c "select table_name, operation, timestamp from history where user_name like \'{2}\' group by table_name, operation, timestamp order by timestamp desc limit {3}"'.format(
            database_user, database, user, limit))


def get_log_lines(client, file_name, lines):
    log_regex = re.compile(
        r'^(([0-9]{4}-[0-9]{2}-[0-9]{2})T(([0-9]{2}:[0-9]{2}:[0-9]{2})(\+[0-9]{2}:[0-9]{2}))) ([^ ]+) ([^ ]+) +(\[([^\]]+)\]) (([0-9]{4}-[0-9]{2}-[0-9]{2}) (([0-9]{2}:[0-9]{2}:[0-9]{2})(\+[0-9]{4}))) ([^ ]+) (.*)$')
    # Execute command, read output (stdout, stderr)
    # out_clean, out_error = client.exec_command('tail -' + str(lines) + ' ' + file_name, sudo=True)
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


def get_server_name(self):
    return self.by_id('server-info').get_attribute('data-instance')


def get_client(ssh_host, ssh_username, ssh_password):
    return ssh_client.SSHClient(ssh_host, username=ssh_username, password=ssh_password)
