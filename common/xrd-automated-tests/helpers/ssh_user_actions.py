def add_user(client, username, password, group=None):
    """
        Creates new user to connected server.
        Server connections comes from client param
    :param client: ssh_helper object
    :param username: string (username to create)
    :param password: string (password to assign to user)
    :param group: string (group to add user, empty don't want to add to group)
    """
    # command = 'useradd -p $(echo "' + password + '" | openssl passwd -1 -stdin) ' + username
    command = 'useradd -p $(echo "{0}" | openssl passwd -1 -stdin) {1}'.format(password, username)
    print command
    for line in client.exec_command(command=command, sudo=True):
        print line
    if group:
        # command = 'usermod -a -G ' + group + ' ' + username
        command = 'usermod -a -G {0} {1}'.format(group, username)
        print command
        for line in client.exec_command(command=command, sudo=True):
            print line


def delete_user(client, username):
    """
        Deletes user from connected server
        Server connection comes from client param
    :param client: ssh_helper object
    :param username: string (username to delete)
    """
    # command = 'deluser ' + username
    command = 'deluser {0}'.format(username)
    print command
    for line in client.exec_command(command=command, sudo=True):
        print line
