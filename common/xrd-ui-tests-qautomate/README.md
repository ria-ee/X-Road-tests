# xrd-ui-tests-qautomate

This folder contains X-Road ui test made with qautomate framework.

## Folder structure

* pagemodel > pagemodels used in test cases
* common_lib > components and common libs used in test cases
* config > configuration files for qautomate project
* data > xml test data
* documentation > sphinx documentation source
* measurements > Performance test measurements
* profile > test running profiles
* scripts > scripts used during tests or development
* tests > test cases
* variabels > files containing python variables for tests

## Sphinx documentation

Generated sphinx documentation: [Documentation](https://s3-eu-west-1.amazonaws.com/xroad-tests-qautomate/index.html)

## Qautomate installation

Qautomate installation is covered in separate document: [installation.md](installation.md).


## Qautorunner

* Move to project folder
* Run command "qautorunner.py -c $TESTPROFILE -p $TESTXML -b ff -s -v ogg"


## Jenkins integration

- Create Freestyle project
- Checkout project from git
- Under "Build" -> Execute shell
    `export PYTHONPATH=/home/jenkins/.local/lib/python2.7/site-packages/qautomate/
    export PATH=$PATH:/home/jenkins/.local/lib/python2.7/site-packages/qautomate/webframework/resources/
    export DISPLAY=:0
    ls -la
    cd $GIT_WORKING_DIR
    qautorunner.py -c $TESTPROFILE -p $TESTXML -b ff -s -v ogg`


