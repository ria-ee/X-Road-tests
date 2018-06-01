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

sshpass -p $pass ssh $user@$host <<EOF

    sudo apt-get install -y xroad-confproxy
    sudo service xroad-signer restart
    sudo sh -c "echo '[configuration-proxy]\naddress=xroad-lxd-web.lxd\nconfiguration-path=/etc/xroad/confproxy/\ngenerated-conf-path=/var/lib/xroad/public\nsignature-digest-algorithm-id=SHA-512\nhash-algorithm-uri=http://www.w3.org/2001/04/xmlenc#sha512\ndownload-script=/usr/share/xroad/scripts/download_instance_configuration.sh' >> $local_ini_file"
EOF


