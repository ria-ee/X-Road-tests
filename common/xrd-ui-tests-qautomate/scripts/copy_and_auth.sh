echo Start cert copy
echo $1
sudo cp -f $1auth_csr*.$2 scripts/temp_auth.$2
sudo rm -f $1auth_csr*.$2
echo End cert copy
echo Start cert sign-auth
echo $2
sudo cat scripts/temp_auth.$2 | $3 > scripts/auth-cert_automation.$2
echo End cert sign-auth
