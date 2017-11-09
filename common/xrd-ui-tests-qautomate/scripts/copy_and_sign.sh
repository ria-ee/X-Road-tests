echo Start cert copy
echo $1
echo $1sign_csr*.$2 scripts/temp.$2
sudo cp -v -f $1sign_csr*.$2 scripts/temp.$2
sudo rm -f $1sign_csr*.$2
echo End cert copy
echo Start cert sign-sign
echo $3
sudo cat scripts/temp.der | $3 > scripts/sign-cert_automation.der
echo End cert sign-sign
