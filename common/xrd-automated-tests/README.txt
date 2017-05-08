Add needed servers to hosts file if necessary


<h1>Jenkins setup: #</h1>

sudo apt-get update

sudo apt-get install nginx

* check for nginx status (has to be running)

service nginx status
* install open-jdk 7

sudo apt-get install openjdk-7-jdk


<h2>install jenkins</h2>
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





<h2>install firefox</h2>
wget https://downloads.sourceforge.net/project/ubuntuzilla/mozilla/apt/pool/main/f/firefox-mozilla-build/firefox-mozilla-build_47.0.2-0ubuntu1_amd64.deb?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fubuntuzilla%2Ffiles%2Fmozilla%2Fapt%2Fpool%2Fmain%2Ff%2Ffirefox-mozilla-build%2F&ts=1487075893&use_mirror=netix
* install firefox

sudo dpkg -i firefox-mozilla-build_47.0.1-0ubuntu1_amd64.deb\?r\=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fubuntuzilla%2Ffiles%2Fmozilla%2Fapt%2Fpool%2Fmain%2Ff%2Ffirefox-mozilla-build%2F

* install xvfb for firefox

sudo apt-get install xvfb

Xvfb :10 -screen 0 1024x768x16 &

<h2>install pip</h2>
sudo apt-get remove python-pip

sudo apt-get install build-essential libssl-dev libffi-dev python-dev

sudo wget https://bootstrap.pypa.io/get-pip.py

sudo python get-pip.py

sudo apt-get install python-pip



<h2>install Geckodriver</h2>
wget https://github.com/mozilla/geckodriver/releases/download/v0.13.0/geckodriver-v0.13.0-linux64.tar.gz

tar -xvzf geckodriver*

chmod +x geckodriver

cp geckodriver /usr/local/bin/

<h3>add geckodriver to system path</h3>
export PATH=$PATH:/usr/local/bin/geckodriver

<h2>install dependencies:</h2>

sudo apt-get install build-essential libssl-dev libffi-dev python-dev

<h3>install python libraries</h3>
sudo apt-get update

1. pip install requests

sudo pip install selenium==2.53.6

sudo pip install cffi

    * if fails
    
    sudo pip2.7 install cffi
    
2. pip install cryptography

    * if fails
    
    sudo pip2.7 install cryptography
    
3. pip install paramiko

    * if fails
    
    sudo pip2.7 install paramiko
    
4. sudo pip install nose2

* look at the package "six" version, must be greater than 1.6


<h2>get tests into the machine</h2>

* jenkins user needs full access the directory: 
sudo chmod -R 777 {directory}
* ca ssh host needs read access to ca_server/home/ca/CA/certs/*


<h1>RUNNING TESTS</h1>

* repo_root_dir is an example of the tests root directory. Configure it according to your system.

project_location=$(pwd)

repo_root_dir=/home/username/x-road-tests

test_dir=xroad_everything

test_name=test_main

* kills firefox browsers and clears profile(a lot of data)

set +e

killall 'firefox'

rm -rf /tmp/tmp*

rm -rf /tmp/rust_mozprofile*

cd $repo_root_dir/tests/$test_dir

export DISPLAY=:10

export PYTHONUNBUFFERED=true

export PYTHONPATH=$repo_root_dir

nose2 --plugin nose2.plugins.junitxml  --junit-xml $test_name

cp $repo_root_dir/tests/$test_dir/nose2-junit.xml  $project_location

# NB! If a test fails, it tries to delete all the data it has created but if there is a connection
# or an environment problem, there is a chance that this may fail. Therefore you should always check
# the test environment (X-Road servers) manually and verify that no test data has been left there.

![Logo](https://github.com/ria-ee/X-Road/blob/develop/doc/Manuals/img/eu_regional_development_fund_horizontal_div_15.png "EU logo")