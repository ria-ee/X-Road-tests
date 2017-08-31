# Introduction

This file contains the instructions for setting up the environment and adding Jenkins jobs that execute the tests.

# Installation instructions

If you are using local domain names, make sure that they are working in Jenkins environment (add the domains to hosts file if necessary).

# Jenkins setup:

sudo apt-get update


* check for nginx status (has to be running)

service nginx status
* install open-jdk 8

sudo apt-get install openjdk-8-jdk


## install jenkins
wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -

sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

sudo apt-get update

sudo apt-get install jenkins

* get initial admin password for jenkins

sudo cat /var/lib/jenkins/secrets/initialAdminPassword

* install Junit Plugin

find and install JUnit Plugin in jenkins

* install ShiningPanda Plugin

find and install ShiningPanda Plugin in jenkins

* install HTML Publisher Plugin



## install firefox
wget 
https://sourceforge.net/projects/ubuntuzilla/files/mozilla/apt/pool/main/f/firefox-mozilla-build/firefox-mozilla-build_48.0.2-0ubuntu1_amd64.deb/download?use_mirror=netix&r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fubuntuzilla%2Ffiles%2Fmozilla%2Fapt%2Fpool%2Fmain%2Ff%2Ffirefox-mozilla-build%2F&use_mirror=netix

-O firefox-mozilla-build_47.0.2-0ubuntu1_amd64.deb

* install firefox

sudo dpkg -i firefox-mozilla-build_47.0.1-0ubuntu1_amd64.deb\?r\=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fubuntuzilla%2Ffiles%2Fmozilla%2Fapt%2Fpool%2Fmain%2Ff%2Ffirefox-mozilla-build%2F

* install xvfb for firefox

sudo apt-get install firefox xvfb

Xvfb :10 -screen 0 1024x768x16 &

## install pip
sudo apt-get remove python-pip

sudo apt-get install build-essential libssl-dev libffi-dev python-dev

sudo wget https://bootstrap.pypa.io/get-pip.py

sudo python get-pip.py

sudo apt-get install python-pip



## install Geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.13.0/geckodriver-v0.13.0-linux64.tar.gz

tar -xvzf geckodriver*

chmod +x geckodriver

sudo cp geckodriver /usr/local/bin/

### install python libraries
sudo apt-get update

1. pip install requests

sudo pip install selenium==2.53.6

sudo pip install cffi

    * if fails
    
    sudo pip2.7 install cffi
    
2. pip install cryptography

sudo pip install cryptography

    * if fails
    
    sudo pip2.7 install cryptography
    
3. pip install paramiko

sudo pip install paramiko

    * if fails
    
    sudo pip2.7 install paramiko
    
4. pip install nose2

sudo pip install nose2

* look at the package "six" version, must be greater than 1.6
pip show six
	* if version is older than 1.6
	sudo pip install six --upgrade

## get tests into the machine

* jenkins user needs full access to the test skripts directory: 
sudo chmod -R 777 {test scripts directory}
* ca ssh host needs read access to ca_server/home/ca/CA/certs/*

# Setting up Configuration

## Central Server (KS1)
	* Members
		* GOV : TS1OWNER
			* Subsystem: Management Services
		* GOV : TS2OWNER
	* Global Groups
		* security-server-owners
			* Member: GOV : TS1OWNER
			* Member: GOV : TS2OWNER

## Security Server 1 (TS1) clients
	* GOV : TS1OWNER (owner)
	* GOV : TS1OWNER : Management Services
		* Services: Management Services
			* Access: security-server-owners

## Security Server 2 (TS2) clients
	* GOV : TS2OWNER (owner)

# Set up WSDL service

WSDL files are served by HTTP server software, and accessed remotely by X-Road servers. Test scripts need access to the server over SSH connection.
To set up the WSDL server, install an HTTP server (for example, nginx or Apache) or use an existing installation.
To install nginx: sudo apt-get install nginx
To install Apache: sudo apt-get install apache2

* Upload WSDL files (all files under _mock/service_wsdl/_, _gatling_scripts/gatling.wsdl_) to a publicly accessible HTTP server directory (depending on the server software). 
* SSH user should have write access to the uploaded _testservice.wsdl_ and read access to others.
* Save the directory path in the configuration file to _local\_path_ setting under section _wsdl_. Set the corresponding URL to _remote\_path_ under section _wsdl_.
* Note that both paths should end with _{0}_ that is replaced automatically with the correct filename depending on the test. Example: _remote\_path_=http://web.example/www/{0}_

# Mock server

Mock server uses SoapUI to run the mock services. SoapUI requires Java Runtime Environment (JRE).
To install JRE, run the command: sudo apt-get install jre
Download SoapUI Open Source Linux Tarball from https://www.soapui.org/ and move it to your destination directory.
Extract the tarball (assuming version 5.3.0): tar xzf SoapUI-5.3.0-linux-bin.tar.gz
Set the path you extracted the SoapUI archive in the configuration under _mockrunner_ section _service\_command_ parameter (replace _/home/testuser_ with your own path).
Copy the mock service data (all files except README under _mock/service-soapui/_ directory) to the same directory
where you extracted SoapUI.

###Note that you can disable autostarting the mock service with every test in the configuration file (by setting _enabled=False_ under _mockrunner_ section) and keep it running all the time.

# RUNNING TESTS

* repo_root_dir is an example of the tests root directory. Configure it according to your system.

project_location=$(pwd)

repo_root_dir=/var/lib/jenkins/workspace/repository/common/xrd-automated-tests

test_dir=xroad_everything

test_name=test_main

* Executes Xvfb, kills firefox browsers and clears profile(a lot of data)

set +e

Xvfb :10 -screen 0 1024x768x16 &

killall 'firefox'

rm -rf /tmp/tmp*

rm -rf /tmp/rust_mozprofile*

cd $repo_root_dir/tests/$test_dir

export DISPLAY=:10

export PYTHONUNBUFFERED=true

export PYTHONPATH=$repo_root_dir

nose2 --plugin nose2.plugins.junitxml  --junit-xml $test_name

cp $repo_root_dir/tests/$test_dir/nose2-junit.xml  $project_location

#### NB! If a test fails, it tries to delete all the data it has created but if there is a connection
#### or an environment problem, there is a chance that this may fail. Therefore you should always check
#### the test environment (X-Road servers) manually and verify that no test data has been left there.

# Performance tests
Performance test setup and running information can be found from [X-road automated testing documentation](X-road%20automated%20testing%20documentation.md)

![Logo](https://github.com/ria-ee/X-Road/blob/develop/doc/Manuals/img/eu_regional_development_fund_horizontal_div_15.png "EU logo")