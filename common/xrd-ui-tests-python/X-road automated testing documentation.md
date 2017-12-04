# X-road automated testing documentation

**Authors** : Sten Luhtoja, Märt Tibar, Arto Vaas


![Logo](https://raw.githubusercontent.com/ria-ee/X-Road/develop/doc/Manuals/img/eu_regional_development_fund_horizontal_div_15.png "EU logo")
# Tabel of  Contents

- [Introduction](#introduction)
- [1.Used Technologies](#1used-technologies)
  * [1.1 Programming languages](#11-programming-languages)
  * [1.2 Automation tools](#12-automation-tools)
  * [1.3 Build management](#13-build-management)
    + [1.3.1 Used Ubuntu Packages](#131-used-ubuntu-packages)
    + [1.3.2 Used Libraries, frameworks and APIs:](#132-used-libraries--frameworks-and-apis-)
    + [1.3.3 Used Plugins](#133-used-plugins)
  * [1.4 Recording and publishing test results](#14-recording-and-publishing-test-results)
- [2 Framework description](#2-framework-description)
  * [2.1 Framework structure](#21-framework-structure)
  * [2.2 List of framework packages (directories)](#22-list-of-framework-packages--directories-)
  * [2.3 Helpers Package](#23-helpers-package)
  * [2.4 ConfReader class (confreader.py)](#24-confreader-class--confreaderpy-)
    + [2.4.1 INI file (ini\_path)](#241-ini-file--ini--path-)
    + [2.4.2 Text file (config\_file)](#242-text-file--config--file-)
    + [2.4.3 JSON file](#243-json-file)
  * [2.5 MockRunner class (mockrunner.py)](#25-mockrunner-class--mockrunnerpy-)
    + [2.5.1 Starting the service](#251-starting-the-service)
    + [2.5.2 Stopping the service](#252-stopping-the-service)
  * [2.6 SoapTestClient class (soaptestclient.py)](#26-soaptestclient-class--soaptestclientpy-)
  * [2.7 SSHClient class (ssh\_client.py)](#27-sshclient-class--ssh--clientpy-)
  * [2.8 AuditChecker class (auditchecker.py)](#28-auditchecker-class--auditchecker-py-)
  * [2.9 Main Package](#29-main-package)
  * [2.10 Mock Directory](#210-mock-directory)
  * [2.11 Temp Directory](#211-temp-directory)
  * [2.12 Tests package](#212-tests-package)
  * [2.13 Test dependencies and requirements](#213-test-dependencies-and-requirements)
  * [2.14 Mock Service](#214-mock-service)
  * [2.15 WSDL files](#215-wsdl-files)
- [3 Executing tests in Jenkins CI](#3-executing-tests-in-jenkins-ci)
  * [3.1 Project configuration](#31-project-configuration)
  * [3.2 Starting the project](#32-starting-the-project)
  * [3.3 Test results](#33-test-results)
- [4 Performance testing](#4-performance-testing)
  * [4.1 Programming languages](#41-programming-languages)
  * [4.2 Automation tools](#42-automation-tools)
  * [4.3 Build management](#43-build-management)
    + [4.3.1 Used Packages](#431-used-packages)
    + [4.3.2 Used Plugins](#432-used-plugins)
  * [4.4 Mock](#44-mock)
  * [4.5 Installing performance test](#45-installing-performance-test)
  * [4.6 Command line parameters](#46-command-line-parameters)
  * [4.7 Request validation](#47-request-validation)
  * [4.8 Setting up Jenkins to run performance test](#48-setting-up-jenkins-to-run-performance-test)
    + [General](#general)
    + [Source Code Managment.](#source-code-managment)
    + [Build](#build)
    + [Post-build Actions](#post-build-actions)
  * [4.9 Running performance test](#49-running-performance-test)
    + [Preconditions to run test](#preconditions-to-run-test)

# Introduction

This document holds the information and instructions for the X-ROAD automated tests. The document introduces the project architecture and describes packages and more important classes and methods.

Firstly, the document introduces technologies which were used in the creation of the project. It also describes the plugins, packages and libraries needed for executing the project was agreed upon.

Secondly, the architecture of the project is described. Specifically, packages, classes and methods are described in detail.

Finally Jenkins project configuration is brought out and how to execute the test. In similar manner it is possible to run other tests too.



# 1.Used Technologies
## 1.1 Programming languages

Automatic tests are created using Python (version 2.7)

## 1.2 Automation tools

Firefox browser version 47.0.2 and Selenium WebDriver 2.53.6 were used when tests were created.
It is also possible to use Firefox browser version 52.0 and Selenium WebDriver version 3.0.2 when executing tests.

## 1.3 Build management

Used libraries and other needed software are meant to be installed according to the manual or according to the documentation of the library.

### 1.3.1 Used Ubuntu Packages

* Nginx
* Jenkins
* Openjdk-7-jdk
* Firefox
* Geckodriver
* xvfb

### 1.3.2 Used Libraries, frameworks and APIs:

* update
* requests
* selenium
* sudo pip install cffi
* cryptography
* paramiko
* nose2

### 1.3.3 Used Plugins

* ShiningPanda Plugin
* Junit Plugin

## 1.4 Recording and publishing test results

Test results are saved in the filesystem until the next test run, it will then be overwritten. Tests history is visible in Jenkins environment, it is possible to see logs and test results.

Python library Nose2 will save the result in XML format, Jenkins plugin Junit plugin converts it to a html format.


# 2 Framework description

The main class in the test framework is **main.MainController**. This communicates with the browser, handles exceptions and provides configuration parameters to the tests using a **helpers.ConfReader** instance.


## 2.1 Framework structure

The framework consists of Python packages that contain classes, view models and helper files. Helper files contain functions used by different classes.

The framework also requires a mock service to be running and accessible from security servers. This is not part of the testing framework but as it is a required service, it is also described in this chapter.

The framework also requires an HTTP server that serves WSDL files (service descriptions) to the security server. This is not part of the testing framework but as it is a required service, the WSDL files are also described in this chapter.

## 2.2 List of framework packages (directories)

| temp | Temporary data created from tests |
| tests | Tests. |
| view\_models | Page or object related functions and constants. |
The list of packages and directories in the framework is shown in the following table.

_Table 1. List of framework packages._

| **Package** | **Description** |
| --- | --- |
| helpers | Other classes and helper functions. |
| main | Main framework controller classes. |
| mock | Certificates and queries for mocking services |

## 2.3 Helpers Package

This package holds different helper classes and methods for easier access to resources.

_Table 2. List of files in helpers package_

| **Filename** | **Description** | **Methods** | **Description** | **Parameters**|
| --- | --- | --- | --- | --- |
| auditchecker.py | AuditChecker class, connects to security or central server over SSH and gets the last audit.log rows from it, then compares them to specified log entries and checks if they match. Used for checking if certain log entries have been added in some tests|def __init__(self, host, username, password, logfile=None, sudo=False)|Sets up the class instance and default parameters. Opens connection to the server.|self: MainController object|
|	|	|	|	|host: str - hostname of the server|
|	|	|	|	|username: str - SSH username|
|	|	|	|	|password: str - SSH password|
|	|	|	|	|logfile: str - logfile path in the server|
|	|	|	|	|sudo: bool - use sudo for reading logfile. If set, user should be in sudoers list with NOPASSWD.|
|	|	|	|	|return: None|
|	|	|def get_regex(self):|Returns the compiled regex object created from self.line_regex variable.|self: MainController object|
|	|	|def get_line_count(self):|Returns the current logfile line count using "wc -l" command. Can be used to limit the number of rows retrieved|self: MainController object|
|	|	|def get_log_lines(self, lines=None, from_line=None):|Gets a specified number of lines from the end of the logfile. Behaviour with both "lines" and "from_line" set is undefined, use only one of them.|self: MainController object|
|	|	|	|	|int / None - if set, number of lines to return.|
|	|	|	|	|int / None - if set, return rows from this line number|
|	|	|	|	|return: list[str] | None - lines from the end of the logfile as a list; None if an error occurs|
|	|	|def reorder_lines(self, reverse_match):|Reverse the internal lists if they have been saved as reversed {reverse_match=True when using check_log)|self: MainController object|
|	|	|	|	|reverse_match: bool - reverse the internal lists or not|
|	|	|	|	|return: None|
|	|	|def check_log(self, check, lines=None, from_line=None, reverse_match=True, skip_invalid_lines=True, strict=True):|Checks if log contains an entry or entries.|self: MainController object|
|	|	|	|	|check: list[str]|str|list[dict]|dict - an entry or a list of entries to be checked for|
|	|	|	|	|lines: int / None - if set, number of lines to get from the logfile|
|	|	|	|	|from_line: int / None - if set, get logfile rows from this line number|
|	|	|	|	|reverse_match: bool - True to check from the end to the beginning (default)|
|	|	|	|	|skip_invalid_lines: bool - skip lines from the logfile if they cannot be parsed or are empty; otherwise the function will fail when encountering a line like that.
|	|	|	|	|strict: bool / None - if False, skip log lines until the next specified entry is found; True to fail right when first one does not match; None to be strict only with reverse_match=True
|	|	|	|	|return: bool - True if all entries were found; False otherwise|
| confreader.py | ConfReader class, Reads different configuration files, stores the data into a key-value list and allows getting the values from there.|def parse_config_value(val):|Parses string values read from different sources to None, bool, int, float or string.|val: str - value to parse|
|	|	|	|	|return: str - parsed value|
|	|	|def clear_config(self):|Clears the internal dictionary|self: MainController object|
|	|	|	|	|return: None|
|	|	|def set_config(self, conf):|Appends/overwrites the internal configuration. Will not delete values that do not exist in dict conf|self: MainController object|
|	|	|	|	|conf: dict - dictionary with keys and values|
|	|	|	|	|return: None|
|	|	|def set(self, key, value):|Sets a single key and value|self: MainController object|
|	|	|	|	|key: str - key|
|	|	|	|	|return: None|
|	|	|def read_command_line_arguments(self):|Reads command-line arguments and updates configuration.|self: MainController object|
|	|	|	|	|return: None|
|	|	|def read_ini(self, ini_file):|Reads an ini file.|self: MainController object|
|	|	|	|	|ini_file: str - path of the file to be parsed|
|	|	|	|	|return: None|
|	|	|def read_key_value_pairs(self, file):|Read file with key=value pairs|self: MainController object|
|	|	|	|	|file: path of configuration file|
|	|	|	|	|return: None|
|	|	|def read_json(self, file):|Reads JSON file.|self: MainController object|
|	|	|	|	|file: path to JSON file|
|	|	|	|	|return: None|
|	|	|def get(self, key, default=None):|Get a value using a key, or default if not found.|self: MainController object|
|	|	|	|	|key: str - key to look for|
|	|	|	|	|default: default value if key is not found. None by default.|
|	|	|	|	|return: value or default value|
|	|	|def get_string(self, key, default=''):|Gets a string by key, or default is value is not a string.|self: MainController object|
|	|	|	|	|key: str - key|
|	|	|	|	|default: str - default value|
|	|	|	|	|return: str or default value|
|	|	|def get_int(self, key, default=0):|Gets an integer by key, or default is value is not an integer.|self: MainController object|
|	|	|	|	|key: str - key|
|	|	|	|	|default: int - default value|
|	|	|	|	|return: int or default value|
|	|	|def get_float(self, key, default=0.0):|Gets a float by key, or default is value is not a float.|self: MainController object|
|	|	|	|	|key: str - key|
|	|	|	|	|default: float - default value|
|	|	|	|	|return: float or default value|
|	|	|def get_bool(self, key, default=False):|Gets a boolean by key, or default is value is not a boolean.|self: MainController object|
|	|	|	|	|key: str - key|
|	|	|	|	|default: bool - default value|
|	|	|	|	|return: bool or default value|
|	|	|def __init__(self, default=None, init_command_line=True, ini_path=None, config_path=None, json_path=None):|Initialize the class.|self: MainController object|
|	|	|	|	|default: dict / None - default configuration to load automatically|
|	|	|	|	|init_command_line: bool - initialize with command-line arguments automatically|
|	|	|	|	|ini_path: str / None - path to configuration INI file to be loaded automatically or None if not used|
|	|	|	|	|config_path: str / None - path to configuration key=value pairs file to be loaded automatically or None if not used|
|	|	|	|	|json_path: str / None - path to configuration JSON to be loaded automatically or None if not used|
|	|	|	|	|return: None|
| login.py | Holds login, logout and login-checking methods.|def login(self, username, password, login_with_enter=False):|Try to log in to a server (central or security) with the specified username and password.|self: MainController object|
|	|	|	|	|username: str - Username to log in with|
|	|	|	|	|password: str - Password to log in with|
|	|	|	|	|login_with_enter: bool - send "Enter" key instead of clicking the login button|
|	|	|	|	|return: bool - True if login succeeded or already logged in; False otherwise|
|	|	|def check_login(self, username, wait=False):|Check if user is already logged in (field visible and username matches)|self: MainController object|
|	|	|	|	|username: str - check for login username|
|	|	|	|	|return: bool - True if logged in and username matches; False otherwise|
|	|	|def logout(self, url=None):|Log out by going to logout URL.|self: MainController object|
|	|	|	|	|url: host where logout is needed, string|
|	|	|	|	|return: None|
| mockrunner.py | MockRunner class, Class that tries to control the mock service script (SoapUI MockRunner) over an SSH connection. Uses ssh_helper.SSHClient component.|def __init__(self, host, username, password, command, ready_regex='.*\[SoapUIMockServiceRunner\] Started.*', ready_timeout=60, stop_keycode=3):|Initialize the class and open the SSH connection.|self: MainController object|
|	|	|def start(self):|Tries to start the mock service.|self: MainController object|
|	|	|	|	|return: None|
|	|	|def restart(self):|Restart mock service.|self: MainController object|
|	|	|	|	|return: bool - if the service was started|
|	|	|def stop(self):|Stop the mock service.|self: MainController object|
|	|	|	|	|return: None|
|	|	|def get_error(self):|Returns the last error.|self: MainController object|
|	|	|	|	|return: str|None - last error message|
| soaptestclient.py | SoapTestClient class, Test client to send SOAP queries to the test services. Uses XML ElementTree for parsing XML and UUID to generate unique IDs for requests.|def __init__(self, url=None, body=None, client_certificate=None, server_certificate=None, query_timeout=None, retry_interval=None, fail_timeout=None, headers=None, xroad_namespace=None, xroad_identifiers_namespace=None, faults_successful=None, faults_unsuccessful=None, verify_service=None, params=None, log=None):|Initializes the class and sets default values for all necessary parameters (if specified).|self: MainController object|
|	|	|	|	|url: str - service URL|
|	|	|	|	|body: str - request body|
|	|	|	|	|client_certificate: (client_certificate, client_key) - paths of the client certificate and key files|
|	|	|	|	|server_certificate: str - path of the server certificate for verification of the service|
|	|	|	|	|query_timeout: int - single query timeout in seconds|
|	|	|	|	|retry_interval: int - retry interval to check the same condition multiple times|
|	|	|	|	|fail_timeout: int - retry time limit|
|	|	|	|	|headers: [str] - override default HTTP headers|
|	|	|	|	|xroad_namespace: str - override default XRoad namespace|
|	|	|	|	|xroad_identifiers_namespace: str - override default XRoad namespace|
|	|	|	|	|faults_successful: [str] - fault codes for a successful query (other codes are considered a success)|
|	|	|	|	|faults_unsuccessful: [str] - fault codes for an unsuccessful query (other codes are considered a success)|
|	|	|	|	|erify_service: dict{} - verify specified service parameters; if one doesn't match, query fails|
|	|	|	|	|params: dict{}/None - default parameters for query|
|	|	|	|	|log: logging function|
|	|	|	|	|return: None|
|	|	|def log(self, str):|Default logging function.|self: MainController object|
|	|	|	|	|str: str - text to be logged|
|	|	|	|	|return: None|
|	|	|def query(self, url=None, body=None, params=None, timeout=None):|Log out by going to logout URL.|Sends a query to the service. All parameters are optional and if not set, they're replaced with default ones that were supplied to the init method.|self: MainController object|
|	|	|	|	|url: str/None - URL of the service|
|	|	|	|	|body: str/None - request body (XML)|
|	|	|	|	|params: dict/None - parameters to be replaced in the body;|
|	|	|	|	|timeout: int - query timeout in seconds|
|	|	|	|	|return: bool - True if the query succeeded and no Fault element was found in the result; False otherwise|
|	|	|def check_query_success(self, url=None, body=None, params=None, query_timeout=None, faults=None):|Sends the query and checks if the result was a success or not. Uses the same parameters as the query() method, but can be additionally supplied with a list of faults that are considered errors. If the faults list is specified, the function returns True even if there was a fault but it wasn't in the list; otherwise False. Wildcards can be used in the end of the fault strings and will only check for a match in the beginning of the fault code.|self: MainController object|
|	|	|	|	|url: str/None - URL of the service|
|	|	|	|	|body: str/None - request body (XML)|
|	|	|	|	|params: dict/None - parameters to be replaced in the body|
|	|	|	|	|query_timeout: int - query timeout in seconds|
|	|	|	|	|faults: str|[str]|None/bool - string or list of strings of the codes to be considered real faults, None or True for all, False for none|
|	|	|	|	|return: bool - True if the query succeeded and didn't get a (specified) fault; False otherwise|
|	|	|def check_query_loop(self, url=None, body=None, params=None, query_timeout=None, faults=None, fail_timeout=None, retry_interval=None, verify_service=None, check_success=True):|Checks for query result like check_query_success but in a loop. Depending on check_success=True (check if the query succeeds) or check_success=False (check if the query fails) it tries the query again after retry_interval seconds until the condition is met or a timeout (specified by fail_timeout seconds) occurs. If the condition is met and, if specified, verify_service conditions match the result service, returns True; otherwise False is returned.|self: MainController object|
|	|	|	|	|url: str/None - URL of the service|
|	|	|	|	|body: str/None - request body (XML)|
|	|	|	|	|params: dict/None - parameters to be replaced in the body;|
|	|	|	|	|query_timeout: int - query timeout in seconds|
|	|	|	|	|faults: str/[str]|None|bool - string or list of strings of the codes to be considered real faults, None or True for all, False for none|
|	|	|	|	|fail_timeout: int - checking failed if this number of seconds pass|
|	|	|	|	|retry_interval: int - number of seconds until first try or retry (after failing)|
|	|	|	|	|verify_service: dict - parameters to check in the result|
|	|	|	|	|check_success: bool - True to wait until the query succeeds; False to wait until it fails|
|	|	|	|	|return: bool - True if success condition is met and verify_service matches result service; False otherwise|
|	|	|def check_success(self, url=None, body=None, params=None, query_timeout=None, faults=None, fail_timeout=None, retry_interval=None, verify_service=None):|Re-checks a query until no (specified) faults are returned and service data verified (if verify_service dictionary is set) every retry_interval seconds until timeout occurs. If no specified faults are returned by the service and it passes verification, returns True; otherwise returns False.|self: MainController object|
|	|	|	|	|url: str/None - URL of the service|
|	|	|	|	|body: str/None - request body (XML)|
|	|	|	|	|params: dict/None - parameters to be replaced in the body|
|	|	|	|	|query_timeout: int - query timeout in seconds|
|	|	|	|	|faults: str/[str]|None|bool - string or list of strings of the codes to be considered real faults, None or True for all, False for none|
|	|	|	|	|fail_timeout: int - checking failed if this number of seconds pass|
|	|	|	|	|retry_interval: int - number of seconds until first try or retry (after failing)|
|	|	|	|	|erify_service: dict - parameters to check in the result|
|	|	|	|	|return: bool - True if success condition is met and verify_service matches result service; False otherwise|
|	|	|def check_fail(self, url=None, body=None, params=None, query_timeout=None, faults=None, fail_timeout=None, retry_interval=None, verify_service=None):|Re-checks a query until a (specified) fault is returned and service data verified (if verify_service dictionary is set) every retry_interval seconds until timeout occurs. If specified fault is returned by the service and it passes verification, returns True; otherwise returns False.|self: MainController object|
|	|	|	|	|url: str|None - URL of the service|
|	|	|	|	|body: str|None - request body (XML)|
|	|	|	|	|params: dict|None - parameters to be replaced in the body|
|	|	|	|	|query_timeout: int - query timeout in seconds|
|	|	|	|	|faults: str|[str]|None|bool - string or list of strings of the codes to be considered real faults, None or True for all, False for none|
|	|	|	|	|fail_timeout: int - checking failed if this number of seconds pass|
|	|	|	|	|retry_interval: int - number of seconds until first try or retry (after failing)|
|	|	|	|	|verify_service: dict - parameters to check in the result|
|	|	|	|	|return: bool - True if success condition is met and verify_service matches result service; False otherwise|
|	|	|def get_service(self):|Returns service parameters from last result XML or None on error.|self: MainController object|
|	|	|	|	|return: dict{instance, class, code, subsystem, service, service_version} - service data dictionary|
|	|	|def verify_service(self, service=None):|Verifies that the parameters set match the ones returned in the last XML result. If parameter service is a match or a subset of the last service data, returns True; otherwise False|self: MainController object|
|	|	|	|	|service: dict - service parameters to verify|
|	|	|	|	|return: bool - True if service is a subset of last XML service data; False otherwise|
| ssh\_client.py | SSHClient class, Simple SSH Client class using Paramiko library. Connects to an SSH server and allows to execute commands and use stdin, stdout, stderr.|def __init__(self, host, username, password):|Connects to host. If sudo is needed in connection, user to connect as should also be in sudoers| self: MainController object|
|	|	|	|	|host: string (only hostname)|
|	|	|	|	|username: string|
|	|	|	|	|password: string\|None|
|	|	|	|	|key\_file: string\|None|
|	|	|	|	|key\_password: string\|None|
|	|	|	|	|return: None|
|	|	|def get_client(self):|Returns the internal paramiko.SSHClient instance.|self: MainController object|
|	|	|	|	|return: paramiko.SSHClient|
|	|	|def exit_status(self):|Get the latest command's exit status code.|self: MainController object|
|	|	|	|	|return: int - status code|
|	|	|def write(self, str, flush=False):|Using stdin, send text to server and, if specified, flush the buffer.|self: MainController object|
|	|	|	|	|str: str - text to send|
|	|	|	|	|flush: bool - flush the buffer after sending|
|	|	|	|	|return: bool - True if stdin exists, False otherwise|
|	|	|def write_flush(self, str, linefeed=True):|Using stdin, send text or line to server and flush it.|self: MainController object|
|	|	|	|	|str: str - text to send|
|	|	|	|	|linefeed: bool - add a newline character to the string if True|
|	|	|	|	|return: bool - True if stdin exists, False otherwise|
|	|	|def writeline(self, line):|Using stdin, send a line (adding a linefeed character to specified text) to server and flush it.|self: MainController object|
|	|	|	|	|line: str - text to send, without the linefeed|
|	|	|	|	|return: bool - True if stdin exists, False otherwise|
|	|	|def readline(self):|Reads a line from stdout, excluding newline characters.|self: MainController object|
|	|	|	|	|str/None - data from stdout, or None if stdout does not exist|
|	|	|def exec_command(self, command, sudo=False, timeout=None):|Executes the command. To enable sudo, param must be true, default False. Returns console ouput as string array(each line one element) removes '\n' from lines.|self: MainController object|
|	|	|	|	|ommand: string - command to send|
|	|	|	|	|sudo: bool - True to send sudo before command|
|	|	|	|	|return: string array|
|	|	|def open(self, host, username, password):|Connects to host. If sudo is needed in connection, user to connect as should also be in sudoers|self: MainController object|
|	|	|	|	|host: string (only hostname)|
|	|	|	|	|username: string|
|	|	|	|	|password: string\|None|
|	|	|	|	|key\_file: string\|None|
|	|	|	|	|key\_password: string\|None|
|	|	|	|	|return: None|
|	|	|def close(self):|Close the connection.|self: MainController object|
|	|	|	|	|return: None|
| ssh\_server\_actions.py | Helper functions for checking XRoad logs and other server specific methods.|def get_server_time(ssh_host, ssh_username, ssh_password):|Creates connection to ss_host with ssh_username and ssh_password and retrieves server date|ssh_host: string (only hostname)|
|	|	|	|	|ssh_password: string|
|	|	|	|	|ssh_username: string|
|	|	|	|	|return: datettime object of current server systen time|
|	|	|def get_key_conf_keys_count(sshclient, key_type):|Gets count of keys of specified type in system configuration|sshclient: obj - sshclient instance|
|	|	|	|	|key_type: str - key type|
|	|	|	|	|return: None|
|	|	|def get_key_conf_token_count(sshclient):|Gets count of device objects in system configuration|sshclient: obj - sshclient instance|
|	|	|	|	|return: None|
|	|	|def get_key_conf_csr_count(sshclient):|Gets count of csr objects in system configuration|sshclient: sshclient instance|
|	|	|	|	|return: None|
| ssh\_user\_actions.py | Helper functions for manipulating Linux users. |def add_user(client, username, password, group=None):|Creates new user to connected server. Server connections comes from client param|client: ssh_helper object|
|	|	|	|	|username: string (username to create)|
|	|	|	|	|password: string (password to assign to user)|
|	|	|	|	|group: string (group to add user, empty don't want to add to group)|
|	|	|	|	|return: None|
|	|	|def delete_user(client, username):|Deletes user from connected server. Server connection comes from client param|client: ssh_helper object|
|	|	|	|	|username: string (username to delete)|
|	|	|	|	|return: None|
| webdriver\_init.py | Helper functions for creating browser instances.|def get_webdriver(type=webdriver.Firefox, download_dir='', log_dir='', marionette=False):|Gets the webdriver object depending on the type set.|type: RemoteWebDriver - type of the WebDriver, allowed: Firefox, Chrome, Ie|
|	|	|	|	|download_dir: str - path of the download directory|
|	|	|	|	|log_dir: str - path of the logfile|
|	|	|	|	|marionette: bool - used only for Firefox; True for Selenium 3; False for Selenium 2|
|	|	|	|	|return: WebDriver object|
|	|	|def get_ie(download_dir='', log_dir=''):|Stub for getting Internet Explorer WebDriver.|download_dir: str - path of the download directory|
|	|	|	|	|log_dir: str - path of the logfile|
|	|	|	|	|return: WebDriver object|
|	|	|def get_chrome(download_dir='', log_dir=''):|Stub for getting Chrome WebDriver|download_dir: str - path of the download directory|
|	|	|	|	|log_dir: str - path of the logfile|
|	|	|	|	|return: WebDriver object|
|	|	|def get_firefox(download_dir='', log_dir='', marionette=False):|Returns a Firefox WebDriver that accepts untrusted certificates, will no ask to resume from crashes, does not use cache, uses specified download directory and logfile, downloads files automatically.|download_dir: str - path of the download directory|
|	|	|	|	|log_dir: str - path of the logfile|
|	|	|	|	|marionette: bool - False to use Selenium 2, True for Selenium 3|
|	|	|	|	|return: WebDriver object|
| xroad.py | Helper functions for XRoad datatypes.|def split_xroad_id(xroad_id, type=None):|Creates a dictionary {type, instance, class, code, subsystem} from an XRoad ID string.|def split_xroad_id(xroad_id, type=None):|Creates a dictionary {type, instance, class, code, subsystem} from an XRoad ID string.|xroad_id: str - XRoad ID string|
|	|	|	|	|type: str - member type|
|	|	|	|	|return: dict{type, instance, class, code, subsystem}|
|	|	|def get_service_name(service):|Returns service part of string service.version|service: service full name|
|	|	|	|	|return: str - service name|
|	|	|def get_service_version(service):|Returns version part of string service.version; empty string if not specified.|service: service full name|
|	|	|	|	|return: str - service version or empty string|
|	|	|def get_xroad_id(xroad_data):|Returns the XRoad ID string using an xroad data dict. Type (member/subsystem) is automatically detected from 'subsystem' value - if it exists, return a subsystem; if not, return a member.|xroad_data: dict - XRoad data from get_xroad_id()|
|	|	|	|	|return: str - XRoad ID string|
|	|	|def get_xroad_member(xroad_data, xroad_type='MEMBER'):|Returns an XRoad ID member string using an xroad data dict.|xroad_data: dict - XRoad data from get_xroad_id()|
|	|	|	|	|xroad_type: str - subsystem type string, default=MEMBER|
|	|	|	|	|return: str - XRoad ID string|
|	|	|def get_xroad_subsystem(xroad_data, xroad_type='SUBSYSTEM'):|Returns an XRoad ID subsystem string using an xroad data dict.|xroad_data: dict - XRoad data from get_xroad_id()|
|	|	|	|	|xroad_type: str - subsystem type string, default=SUBSYSTEM|
|	|	|	|	|return: str - XRoad ID string|
|	|	|def fill_upload_input(self, upload_button_element, local_path):|Fills upload element input[type="file"] without using the file open dialog.|self: MainController object|
|	|	|	|	|upload_button_element: WebElement - "Upload" or "Browse" button (label[class="upload"])|
|	|	|	|	|local_path: str - file path on local computer|
|	|	|	|	|return: None|
|	|	|def get_xroad_path(client, client_type=None):|Returns an X-Road path.|client: dict - client data|
|	|	|	|	|return: client_type: str/None - if set, used as client type; otherwise the type is extracted from client parameter|
|	|	|	|	|return: str - X-Road path|

## 2.4 ConfReader class (confreader.py)

ConfReader is a class for storing and reading parameters from different sources. It supports reading parameters from command-line arguments, INI files, JSON files and text files containing one key=value pair on each line (ignoring empty lines).

**Configuration parsing**

INI files, config files and command-line arguments are all parsed to detect types (Boolean, None, string, integer, float) automatically. Values are initially loaded as strings and type detection is necessary for some methods that need integers or floats as input. The values are automatically checked for text &quot;True&quot;, &quot;False&quot;, &quot;None&quot;, and numeric values. Because keeping a numeric value as string may sometimes be necessary, type detection can be avoided by wrapping the value inside single quotes (&#39;), example: age=&#39;14&#39;.

**Configuration examples setting the following values:**

| additional\_info=None (NoneType) --person.name=&quot;John Doe&quot; (string) --person.age=24 (integer) --person.tv\_show=&quot;24&quot; (string) --person.married=True (Boolean) |
| --- |

**Command-line arguments**

Each argument needs to be prefixed with two dashes (--). Long values should be wrapped inside double quotes (&quot;), values without spaces do not need to be wrapped.

Example assumes script filename of _test.py_

| python test.py --additional\_info=None --person.name=&quot;John Doe&quot; --person.age=24 --person.tv\_show=&quot;&#39;24&#39;&quot; --person.married=True |
| --- |

### 2.4.1 INI file (ini\_path)

INI files ignore empty lines and comment lines starting with a semicolon (;). ConfReader parameter names are constructed from section and key names, concatenated with a dot (.). Section [MAIN] (capital letters) is a special section that will not be used as a prefix.

Sections can be used for grouping parameters, but everything can be written under MAIN.

If command-line arguments are parsed (_init\_command\_line=True_ when initializing the class), INI file can be specified with argument **--ini=/path/to/file.ini**.

| ; Grouped parameters[MAIN]additional\_info=None[person]name=John Doeage=24tv\_show=&#39;24&#39;married=True | ; Everything grouped under MAIN [MAIN]additional\_info=Noneperson.name=John Doeperson.age=24person.tv\_show=&#39;24&#39;person.married=True |
| --- | --- |

### 2.4.2 Text file (config\_file)

Each line consists of key=value pair. Empty lines are ignored. Lines without an equals sign (=) are ignored and can be used as comments.

If command-line arguments are parsed (_init\_command\_line=True_ when initializing the class), configuration file can be specified with argument **--config=/path/to/file**.

| This is an example config file additional\_info=Noneperson.name=John Doeperson.age=24person.tv\_show=&#39;24&#39;person.married=True |
| --- |

### 2.4.3 JSON file

The advantage of using JSON (JavaScript Object Notation) is that values are converted to dictionaries without parsing them.

| {&quot;additional\_info&quot;: &quot;None&quot;, &quot;person.name&quot;: &quot;John Doe&quot;, &quot;person.age&quot;: 24, &quot;person.tv\_show&quot;: &quot;24&quot;, &quot;person.married&quot;: true} |
| --- |

If command-line arguments are parsed (_init\_command\_line=True_ when initializing the class), JSON file can be specified with argument **--json=/path/to/file**.

_Table 3. ConfReader class methods_

| Method name | Method description |
| --- | --- |
| clear\_config() | Clear all parameters. |
| set\_config(conf) | Update parameters with dictionary _conf_, overwriting the existing values but not clearing everything. |
| set(key, value) | Set parameter _key_ value to _value_ |
| get(key) | Get parameter _key_ value. |
| get\_string(key, default=&#39;&#39;) | Get parameter _key_ value. If _key_ does not exist, return default value. |
| get\_int(key, default=0) | Get parameter _key_ integer value. If _key_ does not exist or is not an integer, return default value. |
| get\_floatkey, default=0.0) | Get parameter _key_ float value. If _key_ does not exist or is not a float, return default value. |
| get\_bool(key, default=False) | Get parameter _key_ Boolean value. If _key_ does not exist or is not a Boolean, return default value. |
| read\_command\_line\_arguments() | Reads parameters from command-line arguments. |
| read\_ini(ini\_file) | Reads parameters from an INI file. |
| read\_key\_value\_pairs(file) | Reads parameters from a configuration text file (key=value pairs). |
| read\_json(file) | Reads parameters from a JSON file. |

## 2.5 MockRunner class (mockrunner.py)

MockRunner is a simple class that controls the mock service script (SoapUI MockRunner) over an SSH connection.

Uses ssh\_helper.SSHClient component. Connects to SSH server, sends a one-liner command and then waits until a specified regex matches output or a timeout occurs. To stop the service, sends a single keycode (Ctrl-C by default).

### 2.5.1 Starting the service

When MockRunner tries to start the service, it goes through the following steps.

1. Connect to service server over SSH
2. Send username and password
3. Execute _command_
4. Check standard output (stdout) on the server and look for _ready\_regex_ match.
5. If match is found, service has been started. If timeout occurs first, service start failed.
6. Control is given back to the calling program.

If any of these steps fail, the service will not be started, start command returns False and MockRunner.error variable will contain an error message.

### 2.5.2 Stopping the service

Stopping the service is done by sending _stop\_keycode_ to standard input (stdin) over the SSH link. No other checks are made.

_Table 4. MockRunner class methods_

| **Method name** | **Method description** |
| --- | --- |
| start() | Start the service. Returns True if service start was detected, False otherwise. |
| stop() | Stop the service by sending _stop\_keycode_ key. |
| restart() | Restart the service by executing stop() and start() in sequence. |
| get\_error() | Returns last start() error or None if no error. |



## 2.6 SoapTestClient class (soaptestclient.py)

SoapTestClient is the test client class for sending SOAP requests to XRoad security servers. The component is used for testing if the services respond, succeed, return an error, and if the return data matches the expected data.

SoapTestClient uses the Python Requests library to send SOAP queries over HTTP(S) and parses response XML to extract XRoad service parameters.

_Table 5. SoapTestClient class methods_

| **Method name** | **Method description** |
| --- | --- |
| query(url=None, body=None, params=None, timeout=None) | Sends a query to the service.  _url_ and _body_ are required parameters. All parameters are optional when calling the method. If not set, they are replaced with default ones that were supplied to the init method. |
| check\_query\_success(url=None, body=None, params=None, query\_timeout=None, faults=None) | Checks if a query succeeds. Sends a query to the service using query() with the same parameters and check if a the response contains a Fault element and if the fault code matches a supplied list of faults. All parameters are optional when calling the method. If not set, they are replaced with default ones that were supplied to the init method. |
| check\_query\_loop(url=None, body=None, params=None, query\_timeout=None, faults=None, fail\_timeout=None, retry\_interval=None, verify\_service=None, check\_success=True) | Checks if a query succeeds or fails (depending on _check\_success_ value) before _query\_timeout_ occurs. Sends a query to the service using check\_query\_success() every _retry\_interval_ seconds until it returns the same value as _check\_success_. If _verify\_service_ is supplied, it then checks if it is a subset of response service parameters. Returns _True_ if all conditions are _True_ before _fail\_timeout_ seconds pass, _False_ otherwise. All parameters are optional when calling the method. If not set, they are replaced with default ones that were supplied to the init method. |
| check\_success(url=None, body=None, params=None, query\_timeout=None, faults=None, fail\_timeout=None, retry\_interval=None, verify\_service=None) | Checks if the query succeeds before _query\_timeout_ occurs. Sends a query to the service using check\_query\_loop() using _check\_success=True_ every _retry\_interval_ seconds until it returns _True_. If a timeout of _query\_timeout_ seconds occurs returns _False_. All parameters are optional when calling the method. If not set, they are replaced with default ones that were supplied to the init method. |
| check\_fail(url=None, body=None, params=None, query\_timeout=None, faults=None, fail\_timeout=None, retry\_interval=None, verify\_service=None) | Checks if a query fails before _query\_timeout_ occurs. Sends a query to the service using check\_query\_loop() using _check\_success=False_ every _retry\_interval_ seconds until it returns _True_. If a timeout of _query\_timeout_ seconds occurs returns _False_. All parameters are optional when calling the method. If not set, they are replaced with default ones that were supplied to the init method. |
| get\_service() | Internal method to extract service parameters as a dictionary from latest query response XML. |
| verify\_service(service) | Method to check if _service_ is a subset of last service parameters returned by _get\_service()_ |
| log(str) | Internal default debug logging method. Prints a string to standard output. |

## 2.7 SSHClient class (ssh\_client.py)

SSHClient is a simple SSH Client class using the Paramiko library. It connects to an SSH server and allows to execute commands, use standard input, output and receive errors (stdin, stdout, stderr). Connection is made during class initialization and remains open until _close()_ method is called.

_Table 6. SSHClient class methods_

| **Method name** | **Description** |
| --- | --- |
| get\_client() | Returns the Paramiko internal SSHClient instance. |
| exit\_status() | Returns the last command&#39;s exit status code. |
| write(str, flush=False) | Writes to remote standard input (stdin). If _flush=True_, flushes the buffer after writing. |
| write\_flush(str) | Writes to remote standard input (stdin) and flushes the buffer. |
| writeline(line) | Writes a line to remote server, automatically adds a linefeed character. |
| readline() | Reads a line from remote standard output (stdout) and returns it without linefeed characters. |
| exec\_command(command, sudo=False, timeout=None) | Executes a command on the remote server. If _sudo=True_, tries to execute the command with _sudo_ prefix (root rights, user must have _sudo_ access). If _timeout_ in seconds is supplied, sets the Paramiko internal channel timeout. |
| open(host, username, password) | Connects to host over SSH using specified credentials. |
| close() | Closes the connection. |

## 2.8 AuditChecker class (auditchecker.py)

AuditChcker is an X-Road log (audit.log) checker. It connects to security or central server over SSH and gets the last audit.log rows from
it, then compares them to specified log entries and checks if they match. Used for checking if certain log entries have been added in some tests.

_Table 7. AuditChecker class methods_

| **Method name** | **Description** |
| --- | --- |
| get\_regex() | Returns the compiled regular expression object created from internal regex string. |
| get\_line\_count() | Returns the current logfile line count using "wc -l" command. |
| get\_log\_lines(lines=None, from_line=None) | Gets a specified number of lines from the end of the logfile. If from_line is specified, gets all lines from this to the end of the file. |
| reorder\_lines(reverse_match) | Reverses the internal lists if reverse_match=True, used internally. |
| check_log(check, lines=None, from_line=None, reverse_match=True, skip_invalid_lines=True, strict=True) | Checks if log contains an entry or entries. |

## 2.9 Main Package

Main package contains two classes: MainController and AssertHelper.

**AssertHelper** is a base class for MainController adding assertion methods that can be used during tests.

**MainController** class is the test framework main controller. It handles and interacts with the web browser, provides helper functions for finding elements, logging in and out of XRoad, basic logging and main configuration parameters.
By default, MainController loads its configuration from _config.ini_ file located in the Main Package directory. If parameter _config.load\_custom\_config_ is set to _True_ (default), it also tries to load additional configuration parameters
from _config.kvp_ (key-value pairs), _config.ini_ (INI file), and _config.json_ (JSON) files in the current working directory (usually test directory).

_Table 8. MainController class methods_

| Method name | Method description |
| --- | --- |
| setUp() | Setup method for starting a test. Starts a browser (WebDriver) and Mock Service if they are configured to start automatically. |
| tearDown() | Test teardown method, used for closing the test environment after successful or failed tests. Stops mock service if it was started, and closes the browser window. If an exception has been raised during the test, and screenshots and traceback saving has been enabled, takes a screenshot and saves a traceback to a file. |
| save\_exception\_data(exctype=None, excvalue=None, exctrace=None) | Saves the exception screenshot and traceback if set in configuration. |
| remove\_files(file\_list, remove\_directories=True) | Removes files and, if _remove\_directories=True_, directories given in _file\_list_ as a list of strings. Single filename may also be supplied as a string for _file\_list_ parameter. Returns _True_ if everything was successfully deleted, _False_ otherwise. |
| empty\_directory(path) | Empties a directory without deleting the directory itself. |
| get\_path(path=&#39;&#39;) | Gets the current base path (one level up from maincontroller.py location). If _path_ parameter is supplied, then: if it is an absolute path, returns _path_, if a relative path, concatenates it with the base path. |
| get\_temp\_path(path=&#39;&#39;) | Returns the configured temporary path. Otherwise works like _get\_path()_ |
| get\_download\_path(path=&#39;&#39;) | Returns the configured download path. Otherwise works like _get\_path()_ |
| get\_cert\_path(path=&#39;&#39;) | Returns the configured mock certificate path. Otherwise works like _get\_path()_ |
| get\_query\_path(path=&#39;&#39;) | Returns the configured test query path. Otherwise works like _get\_path()_ |
| get\_xml\_query(filename) | Returns XML query data from a specified file using _get\_query\_path()_ to compute the full path. |
| reset\_webdriver(url, username=None, password=None, close\_previous=None, init\_new\_webdriver=True) | Resets the browser (WebDriver) to a specified URL. If the browser window is not open or _init\_new\_webdriver=True_, starts a new browser instance. If _close\_previous=True_ and a browser window was open, closes it. Is _username_ is not _None_, tries to log in to XRoad GUI with _username_ and _password_. |
| reload\_webdriver(url, username=None, password=None) | Sets the browser to a new URL. |
| reset\_page() | Reloads the current browser page. |
| start\_mock\_service() | If starting the Mock Service is not disabled in the configuration, tries to start it. Creates a new _MockRunner_ instance if it does not exist. |
| save\_screenshot(filename) | Takes a screenshot of the current browser window and saves it to configured temporary directory. |
| save\_text\_data(filename, data) | Saves text data to a file in the configured temporary directory. |
| logout() | Logs out from XRoad GUI. |
| login(username, password) | Tries to log in to XRoad GUI with the specified credentials. |
| log(message) | Prints the current timestamp and message to standard output. |
| **Web element methods** |   |
| by\_id(element) | Gets an element from the current page in the browser using the _id_ attribute. |
| by\_xpath(element, multiple=False) | Gets an element from the current page in the browser using an XPath locator string. If _multiple=True_, returns multiple elements. |
| by\_css(element, multiple=False) | Gets an element from the current page in the browser using a CSS selector string. If _multiple=True_, returns multiple elements. |
| wait(condition, timeout=120) | Waits until the browser reports the specified condition to be true, or a timeout of _timeout_ seconds occurs. |
| wait\_until\_visible(element, type=None, timeout=10, multiple=False) | Waits until specified element (or specified elements, depending on _multiple_ value) is visible or a timeout of _timeout_ seconds occurs. If _type_ is specified, _element_ can be a locator string. |
| js(script, \*args) | Executes a JavaScript with optional arguments in the browser and returns the result. |
| async\_js(script, \*args) | Executes a JavaScript asynchronously (non-blocking) in the browser. |
| wait\_jquery(timeout=120) | Waits until jQuery object is not active or a timeout of _timeout_ seconds occurs . Used when checking if jQuery-based AJAX queries have finished. |
| get\_classes(element) | Returns a list of CSS classes associated with the specified _element_. |
| input(element, text, click=True, clear=True) | Types _text_ into an HTML input/textarea element. If _click=True_, first clicks on the element. If _clear=True_, clears the field before typing. |
| **Methods inherited from AssertHelper** |   |
| is\_true(con1, test\_name=None, msg=&#39;Failed&#39;, log\_message=None) | If con1 is not True, raises an _AssertionException_ with message _msg_. Logs the assertion with _test\_name_ and _log\_message_ (if specified). |
| is\_false(con1, test\_name=None, msg=&#39;Failed&#39;, log\_message=None) | If con1 is not False, raises an _AssertionException_ with message _msg_. Logs the assertion with _test\_name_ and _log\_message_ (if specified). |
| is\_equal(con1, con2, test\_name=None, msg=&#39;Failed&#39;, log\_message=None) | If con1 and con2 are not equal, raises an _AssertionException_ with message _msg_. Logs the assertion with _test\_name_ and _log\_message_ (if specified). |
| not\_equal(con1, con2, test\_name=None, msg=&#39;Failed&#39;, log\_message=None) | If con1 and con2 are equal, raises an _AssertionException_ with message _msg_. Logs the assertion with _test\_name_ and _log\_message_ (if specified). |
| is\_none(con1, test\_name=None, msg=&#39;Failed&#39;, log\_message=None) | If con1 is not _None_, raises an _AssertionException_ with message _msg_. Logs the assertion with _test\_name_ and _log\_message_ (if specified). |
| is\_not\_none(con1, test\_name=None, msg=&#39;Failed&#39;, log\_message=None) | If con1 is _None_, raises an _AssertionException_ with message _msg_. Logs the assertion with _test\_name_ and _log\_message_ (if specified). |

## 2.10 Mock Directory

Mock directory (mock) contains the certificates and XML query bodies that are used by SoapTestClient mock client. It contains two subdirectories.

The &quot;cert&quot; subdirectory contains the certificate (mock.crt) and private key (mock.key) of the mock client, and the certificate of the Mock Service (mockservice.crt, used for verifying the server&#39;s certificate).

The &quot;queries&quot; subdirectory contains query templates that are parsed by SoapTestClient and sent by the server when testing access lists and services themselves. The list of query templates is shown in the following table.


_Table 9. Mock directory files_

| Filename | Description |
| --- | --- |
| service.xml | SOAP query template for sending queries to security server services. |
| centralservice.xml | SOAP query template for sending queries to central services. |

The following dynamic variables are allowed in the templates, these are replaced with different values for the specific query.

_Table 10. Query template parameters_

| Parameter | Description |
| --- | --- |
| {uuid} | random generated UUID to make the queries unique. |
| {xroadProtocolVersion} | X-Road protocol version (configuration parameter _services.xroad_protocol_) |
| {xroadIssue} | X-Road issue identifier (configuration parameter _services.xroad_issue_) |
| {xroadUserId} | X-Road user ID (configuration parameter _services.xroad_userid_) |
| {serviceMemberInstance} | service provider X-Road instance (query-specific) |
| {serviceMemberClass} | service provider X-Road class (query-specific) |
| {serviceMemberCode} | service provider X-Road code (query-specific) |
| {serviceSubsystemCode} | service provider X-Road subsystem code (query-specific) |
| {serviceCode} | service name (query-specific); for central server queries this is the central service name |
| {serviceProviderCode} | service provider name (query-specific), used only for central server queries |
| {serviceVersion} | service version (query-specific) |
| {memberInstance} | requester X-Road instance (query-specific) |
| {memberClass} | requester X-Road class (query-specific) |
| {memberCode} | requester X-Road code (query-specific) |
| {subsystemCode} | requester X-Road subsystem code (query-specific) |

The following dynamic variables are allowed in the templates, these are replaced with different values for the specific query.

## 2.11 Temp Directory

This directory holds temporary data and test failures(text files and screenshots) created by tests.

There is also a sub-directory &quot;download&quot; where downloaded files are stored, eg. certificates and signing requests.

## 2.12 Tests package

This package contains all the tests. Tests have their own packages.The test structure contains mostly three major files: \_\_init\_\_.py, test\_main.py and the test itself(usually in format test\_\*.py)



_Table 11. Test example architecture_

| \_\_init\_\_.py | Must be file for python package. Makes the test visible to others |
| --- | --- |
| test\_main.py | Extends unittest.TestCase class, calls the test with needed data. |
| test\_\*.py | Test itself, takes care of methods and calls needed for the test.. |


## 2.13 Test dependencies and requirements

_Table 12. Test dependencies and requirements_

| Test class | Depends on finishing other test(s) | Requires helper scenarios |
| --- | --- | --- |
| XroadSecurityServerClientRegistration | None |   |
| XroadAddToAcl | None |   |
| XroadAddToAclFromClient | None |   |
| XroadSecurityServerClientRegistration | None | client_registration_in_ss |
| XroadConfigureService | XroadSecurityServerClientRegistration | add_to_acl |
| XroadRefreshWsdl | XroadConfigureService |   |
| XroadDeactivateWsdl | XroadConfigureService |   |
| XroadLocalTls | XroadConfigureService |   |
| XroadAddCentralService | XroadConfigureService | add_to_acl |
| XroadMemberAccess | XroadConfigureService | add_to_acl |
| XroadChangingDatabaseRowsWithGUICentralServer | None |   |
| XroadChangingDatabaseRowsWithGUISecurityServer | None |   |
| XroadCsLogging | None |   |
| XroadSsLogging | None | client_registration_in_ss, add_to_acl |

## 2.14 Mock Service

The UI testing  service (located under _mock/service-soapui_ directory) serves SOAP requests from users proxied by the security servers. It is a small service that is based on the main xrd-mock-soapui mock service but implements a lesser set of functionality and contains different services (_xroadGetRandom_ and _bodyMassIndex_). It is used for testing service parameters and access lists.

The UI testing mock service has been made in SoapUI and requires SoapUI to run. The mock service is not directly a part of the framework as it can be configured to be running all the time in a different server or the framework may be configured to use other (or non-SoapUI) services that may already be running.

It differs from the _xrd-mock-soapui_ service by defining different services and lesser functionality. As it is only used for verification of the main aspects of X-Road services, it is better and more easily maintainable to use a smaller service that only contains the necessary functionality than to merge it with others.

The UI testing mock service location is set in the WSDL files (under _&lt;wsdl:service&gt;_ subelement _&lt;soap:address&gt;_ attribute _location_) and framework configuration parameters _services.test\_service\_url_, _services.test\_service\_2\_url_, _services.test\_service\_url\_ssl_ (HTTPS), _services.test\_service\_2\_url\_ssl_ (HTTPS). The service must listen on two ports, one using regular HTTP protocol and the other using HTTPS.

| Examples of the part of a WSDL file that points to two services that should already be running on localhost port 8086 under different URLs.     &lt;wsdl:service name=&quot;xroadGetRandom&quot;&gt;        &lt;wsdl:port name=&quot;xroadGetRandomPortSoap11&quot;                binding=&quot;tns:xroadGetRandomPortSoap11&quot;&gt;            &lt;soap:address location=&quot;http://localhost:8086/xroadGetRandom&quot; /&gt;        &lt;/wsdl:port&gt;    &lt;/wsdl:service&gt;     &lt;wsdl:service name=&quot;bodyMassIndex&quot;&gt;        &lt;wsdl:port name=&quot;bodyMassIndexPortSoap11&quot;                binding=&quot;tns:bodyMassIndexPortSoap11&quot;&gt;            &lt;soap:address location=&quot;http://localhost:8086/bodyMassIndex&quot; /&gt;        &lt;/wsdl:port&gt;    &lt;/wsdl:service&gt; |
| --- |

The Mock Service itself is defined in a single XML file (SoapUI project) but as it has to support certificates, it also requires a SoapUI settings file (for supporting SSL), a key store and a certificate file. The list of files required to run the service is in the following table.

_Table 13. Mock service directory files_

| Filename | Description |
| --- | --- |
| soapui-settings.xml | SoapUI settings file (XML). Defines SSL port for services to be 18086, keystore file as &quot;mockservice.keystore&quot; and keystore password as &quot;password&quot;. These values can be edited in SoapUI or directly in XML under elements _&lt;con:setting&gt;_ with attributes &quot;id&quot; starting with &quot;SSLSettings&quot;. |
| testservice-soapui-project.xml | Mock service SoapUI project (XML). Defines two services: _xroadGetRandom_ and _bodyMassIndex_, both are run from port 8086 (if SoapUI settings define an SSL port, they are run from the SSL port at the same time as well). Can be edited from SoapUI. |
| mockservice.keystore | Keystore for the mock service. Default keystore password used is &quot;password&quot;. |

## 2.15 WSDL files

The WSDL files are used for providing information about services to the security servers. They describe the service (name and version) and the URL from which the security server can access it. Multiple services can be described in one WSDL.

The test automation scenarios require different WSDL files to test different outcomes - a working WSDL, a WSDL that removes a previously defined service, a WSDL that gives a parser error and a WSDL that gives a parser warning.

The WSDL files have to be served from an HTTP server that is accessible from security servers and accessible over SSH from the test framework (to edit the files remotely). WSDL files base URL is defined in the main configuration with key _wsdl.remote\_path_ and other WSDL parameters are also under _wsdl_ section.

List of WSDL files defined in the default configuration is in the following table.



_Table 14. WSDL files in default configuration_

| Filename | Description |
| --- | --- |
| testservice.wsdl | The WSDL that is added to the security servers. As the tests require the same file to be overwritten with others (working, erroneous, warning, removed service), it contains different data at different times. |
| testservice\_original.wsdl | This is the base WSDL file that is working correctly and defines two services: _bodyMassIndex.v1_ and _xroadGetRandom.v1_ |
| testservice\_xroadGetRandom\_only.wsdl | Derived from &quot;testservice\_original.wsdl&quot; but defines only one service: _xroadGetRandom.v1_ |
| error.wsdl | A file that results in a WSDL parser error. |
| warning.wsdl | A file that results in a WSDL parser warning. |

# 3 Executing tests in Jenkins CI
## 3.1 Project configuration

1. Choose a freestyle project type
2. Choose project name
3. Add Build step &quot;Custom Python Builder&quot;
  * Home = Python 2.7 location (/usr/bin/python2.7)
  * Nature = Shell
  * Command:

project_location=$(pwd)
repo_root_dir=/var/lib/jenkins/workspace/repository/common/xrd-automated-tests
test_dir=xroad_everything
test_name=test_main


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

4. Add post build action
  * Publish Junit test result report
  * Add the file name which was previously copied.


## 3.2 Starting the project

Open project or from the projects list open project dropdown and click &quot;Build now&quot;. It is also possible to add build triggers.

## 3.3 Test results

When the test is done, you can see test result in Jenkins. Choose the test which result is wanted. Click on &quot;Latest Test Result&quot;.

The Junit report contains three sections: Result bar, All Failed Tests, and All Tests.


Result bar, show the percentage of failed, skipped and passed test on a line:

 Red - failed tests

 Yelllow - skipped tests

 Blue - passed tests

All Failed Tests table: shows the list of all failed tests.

All Tests table: shows the list of all tests, if test contains multiple tests, one can see them when clicking on the test link.


# 4 Performance testing
## 4.1 Programming languages

Performance tests are created using Scala programming language. They are located at [xrd-gatling-tests](../xrd-gatling-tests) directory.

## 4.2 Automation tools

Performance test is developed to work with Gatling 2.2.3 version.

## 4.3 Build management

Used libraries and other needed software are meant to be installed according to the manual or according to the documentation of the library.

### 4.3.1 Used Packages

* Jenkins
* Gatling

### 4.3.2 Used Plugins

* Junit Plugin

## 4.4 Mock

Mock sends out the messages with the size what Gatling script says. Sends them against the xtee9.ci.kit where is the WSDL registered.

Mock service will be started at the Jenkins job. Mock service runs cd /opt/riajenk/xrd-soapui-mock

../SoapUI-5.3.0/bin/mockservicerunner.sh

## 4.5 Installing performance test

Performance test file &quot;xroad.scala&quot; should be placed in the gatling/user-files/simulations folder.

Before running the tests, the performance test service [gatling.wsdl](../xrd-gatling-tests/gatling.wsdl) should be configured in the X-Road environment.

## 4.6 Command line parameters

Table will show command line parameters how you can modify the performance test. Variable should be used on the command line as -Dvariable=value.

| **Parameter** | **Default value** | **Value information** |
| --- | --- | --- |
| xRoadURL | http://127.0.0.1:8080/ | X-road security server |
| rpsTargets | 1,5,10,15,20,25,30,35,40,45,50 | Target request per second (req/s) |
| warmUpHoldPeriod | 30 | Warm-up lenght (sek) |
| mainHoldPeriod | 600 | Period of holding threads (sek) |
| userBumpInterval | 3 | Ramp-up period(sek) |
| weight2kB | 30.0 | The proportion of messages 2kB (%) |
| weight10kB | 60.0 | The proportion of messages 10kB (%) |
| weight100kB | 9.0 | The proportion of messages 100kB (%) |
| weight2MB | 0.9 | The proportion of messages 2MB(%) |
| weight10MB | 0.1 | The proportion of messages 10MB (%) |


**Message based parameters:**

| **Parameter** | **Default value** | **Value information** |
| --- | --- | --- |
| msgXRoadInstance | ee-dev | id:xRoadInstance (MEMBER, SERVICE) |
| msgMemberClass | COM | id:memberClass (MEMBER, SERVICE) |
| msgMemberCode | 11045744 | id:memberCode (MEMBER, SERVICE) |
| msgSubsystemCode | MOCK | id:subsystemCode (SERVICE) |
| msgServiceCode | getMock | id:serviceCode (SERVICE) |
| msgServiceVersion | v1 | id:serviceVersion (SERVICE) |
| msgUserId | EE1234567890 | xrd:userId |
| msgIssue | 12345 | xrd:issue |


Gatling performance test is not sending out messages in different size, it will send &quot;desiredResponseSize&quot; parameter, what indicates to mock service on which size should the response be. If users change the percentage of the sizes it is important to control that all size percentages summ will be 100.

## 4.7 Request validation
reqiests are validated against:
* HTTP response is 200
* Response ID code (<xrd:id>) is same as in request
* <SOAP-ENV:Fault> element is not presented
* Mock timestamp is in numbers and in <mockTimeStamp> element


## 4.8 Setting up Jenkins to run performance test

Create new project for performance test - Freestyle project
### General
* Chek remove old builds.
* Write in Strategy feeld: Log Rotation.
### Source Code Managment.
* Chek Git.
* Write in Reposotory URL feeld your repository adress.
* If credentials are neede press add button and and them.
* Branch Specifier (blank for 'any') wirte dovn the branch on our case: */master
* Repository browser: Auto
### Build
* Add build stem->Execute shell
* Use the parameters and else info you need to add:
#!/bin/bash

// Creating directory for reports
mkdir -p /var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/results/report
// Creating directory for reports history
mkdir -p /var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/results/history

// Removing old results
rm -rf /var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/results/report/*

JAVA_OPTS=`echo "
// add memory to gatling
  -Xms1024m
  -Xmx1024m
// Simulation Class
  -Dgatling.core.simulationClass=ria.XRoad
// Gatling don't ask for test run description
  -Dgatling.core.mute=true
// Lober Bound value
  -Dgatling.charting.indicators.lowerBound=500
// Higher Bound value
  -Dgatling.charting.indicators.higherBound=1000
// Maximum dots on the graph
  -Dgatling.charting.maxPlotPerSeries=3600
// turn of GA
  -Dgatling.http.enableGA=false
// Turn off Keep Alive
  -Dgatling.http.ahc.keepAlive=false
// Timeout when establishing a connection
  -Dgatling.http.ahc.connectTimeout=5000
// Timeout when a used connection stays idle
  -Dgatling.http.ahc.readTimeout=15000
// Request Timeout value
  -Dgatling.http.ahc.requestTimeout=15000
// Change the default simulation folder to bild simulation folder
  -Dgatling.core.directory.simulations=/var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts
// Change the default results directory to build directory folder
  -Dgatling.core.directory.results=/var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/results
// Change the default binaries directory to build binaries folder
  -Dgatling.core.directory.binaries=/var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/binaries
// Change the name of the results folder
  -Dgatling.core.outputDirectoryBaseName=reports
  
// these paramters are explained in chapter 4.6
  -DxRoadURL=http://xtee9.ci.kit
  
  -DwarmUpHoldPeriod=3
  -DmainHoldPeriod=15
  -DuserBumpInterval=3
  
  -DrpsTargets=1,5
  
  -Dweight2kB=30.0
  -Dweight10kB=60.0
  -Dweight100kB=9.0
  -Dweight2MB=0.9
  -Dweight10MB=0.1
  
  -DmsgXRoadInstance=XTEE-CI-XM
  -DmsgMemberClass=GOV
  -DmsgMemberCode=00000001
  -DmsgSubsystemCode=MockSystemGatling
  -DmsgServiceCode=mock
  -DmsgServiceVersion=v1
  -DmsgUserId=EE12345678901
  -DmsgIssue=12345

" | xargs` \
/var/lib/jenkins/gatling-charts-highcharts-bundle-2.2.3/bin/gatling.sh


// Copying new results to report directory
cp -R /var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/results/reports-* /var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/results/report/
// Moving results to history to save history
mv /var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/results/reports-* /var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/results/history/

All parameters can be changed on that script, by adding or removing them.


Parameter information:
* xtee2.ci.kit is a mock server
* xtee9.ci.kit is a security server

### Post-build Actions
add Publish HTML reports stepp

HTML directory to archive : User needs to add  directory location where the report inex.exe and other files are (example: /var/lib/jenkins/workspace/XRoad-load-test/common/xrd-automated-tests/gatling_scripts/results/report)
Index page[s] : user should add html file names from report folders, they would like to see in result view tabs.(example: index.html )

## 4.9 Running performance test

### Preconditions to run test
* Service provider subsystem should have the service configured (gatling.wsdl added under the services).
* Service mock.v1 should have acces rights granted to the subsystem that is sending the queries.
* Service mock.v1 should be enabled.
* Mock service should be running 
	* Example command: cd /opt/riajenk/xrd-testing-service; ../SoapUI-5.3.0/bin/mockservicerunner.sh -s soapui-settings-gatling.xml gatling-mock.xml

If all the preconditions are fullfilled then you can start the jenkins buld and wait for the results.

Results are shown in the Jenkins Job behind the "report" link.



