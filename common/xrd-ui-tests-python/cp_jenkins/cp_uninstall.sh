#!/bin/sh
set -e
#cp credentials
xroad_config_file="/config.ini"
local_ini_file="/etc/xroad/conf.d/local.ini"
host=$(sed -nr "/^\["$1"\]/ { :l /^server_name[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" .$xroad_config_file)
user=$(sed -nr "/^\["$1"\]/ { :l /^ssh_user[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" .$xroad_config_file)
pass=$(sed -nr "/^\["$1"\]/ { :l /^ssh_pass[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" .$xroad_config_file)
cp_host="$host.lxd"

#install sshpass
sudo apt-get install sshpass


#Connecting and installing needed files

sshpass -p $pass ssh $user@$cp_host <<EOF

    sudo rm -rf /etc/xroad/ /var/lib/xroad/
    sudo apt-get purge -y xroad-confproxy xroad-common

EOF
