# Qautomate installation guide

Harmonized Test Environment QAutomate install guide

1. Download and unzip Linux64-bit installer file
    - Temporary link:
        - https://s3-eu-west-1.amazonaws.com/qautomate-1.8/latest/QAutomate-1.8.0-linux-64bit-official-development-release.zip

2. Install following SW packages from unzipped folder
    
- Ubuntu 14.04 `$ ./install_full_environment1404.sh`
- Ubuntu 16.04 `$ ./install_full_environment1604.sh`
 
Note! If problems installing Python or other modules, run "$ sudo apt-get update". Run install script again.

Check with environmental variables by running ```env```

1. Environmental variable PYTHONPATH:"/home/user/.local/lib/python2.7/site-packages/qautomate" 
2. Environment variable PATH:"/home/user/.local/lib/python2.7/site-packages/qautomate/webframework/resources"

Finalize installation with log off computer if needed.

Uninstall QAutomate run in terminal from unzipped folder
    ```$ ./installer_lin.py remove```


