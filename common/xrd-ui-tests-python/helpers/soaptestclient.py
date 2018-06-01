import requests
import time
import re
import uuid
from xml.etree import ElementTree
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages import urllib3
from urlparse import urlparse

# If the access rights are ok but the service endpoint has a problem, it may return:
# - Server.ServerProxy.ServiceFailed.InvalidContentType
# - Server.ServerProxy.ServiceFailed.NetworkError
# If access is denied, fault code is:
# - Server.ServerProxy.AccessDenied
# If service is not found:
# - Server.ServerProxy.UnknownService
# Service is found but disabled:
# - Server.ServerProxy.ServiceDisabled
# Requested service owner (member) not found:
# - Server.ClientProxy.UnknownMember
# Internal error (erroneous request or misconfiguration)
# - Server.ClientProxy.InternalError
# Header error:
# - Client.InconsistentHeaders
# SOAP error:
# - Client.InvalidSoap
# Invalid protocolVersion in request XML
# - Client.InvalidProtocolVersion

# As our test client creates insecure HTTPS requests intentionally, disable the warnings for them
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SoapTestClient:
    '''
    Test client to send SOAP queries to the test services. Uses XML ElementTree for parsing XML and UUID to generate
    unique IDs for requests.
    '''
    url = None
    client_certificate = None  # Send this certificate to server when using SSL
    server_certificate = None  # For verification when using SSL
    headers = {'Content-Type': 'text/xml; charset=UTF-8'}  # Default HTTP headers
    body = None
    query_uuid = None
    fault = None
    fault_code = None
    fault_message = None
    xml = None
    verify_service_data = None
    verify_hostname = True
    params = None
    query_timeout = 90.0  # Query timeout in seconds
    retry_interval = 0  # Seconds to retry in a loop after getting errors (if check_* function is called). 0 for no retries.
    fail_timeout = 120  # Stop loop and throw error when at least this amount of time has passed.

    set_default_params = True  # Set UUID for request body
    debug = False # Enable debug mode

    xroad_namespace = 'http://x-road.eu/xsd/xroad.xsd'
    xroad_identifiers_namespace = 'http://x-road.eu/xsd/identifiers'

    # XML XPaths for strings to search for.
    fault_xpath = './/SOAP-ENV:Body/SOAP-ENV:Fault'  # Fault element in result XML
    fault_code_xpath = './faultcode'  # Fault code element under Fault
    fault_string_xpath = './faultstring'  # Fault string element under Fault
    fault_detail_xpath = './detail/faultDetail'  # Fault detailed description element under Fault

    # XRoad service XPaths
    xroad_service_xpath = './/xroad:service'  # Service element in result XML
    xroad_service_code_xpath = './id:serviceCode'  # Service code under Service
    xroad_service_version_xpath = './id:serviceVersion'  # Service version under Service
    xroad_service_instance_xpath = './id:xRoadInstance'  # XRoad instance identifier under Service
    xroad_service_member_class_xpath = './id:memberClass'  # XRoad member class under Service
    xroad_service_member_code_xpath = './id:memberCode'  # XRoad member code under Service
    xroad_service_member_subsystem_xpath = './id:subsystemCode'  # XRoad subsystem code under Service

    # Faults to check for, not set by default
    faults_successful = None
    faults_unsuccessful = None

    class CustomHTTPAdapter(HTTPAdapter):
        '''
        Custom HTTP Adapter class for requests that allows ignoring the certificate hostname check (useful for
        local setups where the hostname in URL might not match the one in the certificate).
        '''
        assert_hostname = None

        def __init__(self, assert_hostname=False, *args, **kwargs):
            '''
            Initialize the class and set the specified assertion option.
            :param assert_hostname: str|bool False - string with the hostname to verify, False to skip
                                                     certificate hostname verification
            '''
            self.assert_hostname = assert_hostname
            super(SoapTestClient.CustomHTTPAdapter, self).__init__(*args, **kwargs)

        def init_poolmanager(self, connections, maxsize, block=False):
            '''
            Initializes the PoolManager object with custom hostname assertion settings (specified during initialization).
            :param connections: int - PoolManager initialization parameter (num_pools). Number of connection pools to
                                      cache before discarding the least recently used pool.
            :param maxsize: int - PoolManager initialization parameter. Number of connections that can be reused.
            :param block: bool - PoolManager initialization parameter. If True, and maxsize number of connections has
                                 been reached, the call will block.
            :return: None
            '''
            self.poolmanager = PoolManager(num_pools=connections,
                                           maxsize=maxsize,
                                           block=block,
                                           assert_hostname=self.assert_hostname)

    def __init__(self, url=None, body=None, client_certificate=None, server_certificate=None, query_timeout=None,
                 retry_interval=None, fail_timeout=None, headers=None, xroad_namespace=None,
                 xroad_identifiers_namespace=None, faults_successful=None, faults_unsuccessful=None,
                 verify_service=None, verify_hostname=True, params=None, log=None):
        '''
        Initializes the class and sets default values for all necessary parameters (if specified).

        All parameters are optional and will be used as default values if they are not overriden when calling a query.
        :param url: str - service URL
        :param body: str - request body
        :param client_certificate: (client_certificate, client_key) - paths of the client certificate and key files
        :param server_certificate: str - path of the server certificate for verification of the service
        :param query_timeout: int - single query timeout in seconds
        :param retry_interval: int - retry interval to check the same condition multiple times
        :param fail_timeout: int - retry time limit
        :param headers: [str] - override default HTTP headers
        :param xroad_namespace: str - override default XRoad namespace
        :param xroad_identifiers_namespace: str - override default XRoad namespace
        :param faults_successful: [str] - fault codes for a successful query (other codes are considered a success)
        :param faults_unsuccessful: [str] - fault codes for an unsuccessful query (other codes are considered a success)
        :param verify_service: dict{} - verify specified service parameters; if one doesn't match, query fails
        :param verify_hostname: bool|str - if server_certificate is not None, True to verify that the hostname matches
                                           the one in the URL, False to ignore checking, or string with the hostname to
                                           verify
        :param params: dict{}|None - default parameters for query
        :param log: logging function
        '''

        # Internal variables are set only if the parameters are not None.

        if url is not None:
            self.url = url
        if body is not None:
            self.body = body
        if client_certificate is not None:
            self.client_certificate = client_certificate
        if server_certificate is not None:
            self.server_certificate = server_certificate
        if query_timeout is not None:
            self.query_timeout = query_timeout
        if retry_interval is not None:
            self.retry_interval = retry_interval
        if fail_timeout is not None:
            self.fail_timeout = fail_timeout
        if headers is not None:
            self.headers = headers
        if xroad_namespace is not None:
            self.xroad_namespace = xroad_namespace
        if xroad_identifiers_namespace is not None:
            self.xroad_identifiers_namespace = xroad_identifiers_namespace
        if faults_successful is not None:
            self.faults_successful = faults_successful
        if faults_unsuccessful is not None:
            self.faults_unsuccessful = faults_unsuccessful
        if verify_service is not None:
            self.verify_service_data = verify_service
        if verify_hostname is not None:
            self.verify_hostname = verify_hostname
        if params is not None:
            self.params = params
        if log is not None:
            self.log = log

    def log(self, str):
        '''
        Default logging function.
        :param str: str - text to be logged
        :return: None
        '''
        print(str)

    def query(self, url=None, body=None, params=None, timeout=None):
        '''
        Sends a query to the service. All parameters are optional and if not set, they're replaced with default
        ones that were supplied to the init method.
        :param url: str|None - URL of the service
        :param body: str|None - request body (XML)
        :param params: dict|None - parameters to be replaced in the body; example: body="Hello, {name}",
                                    params={'name': 'John'} will result in body="Hello, John"
        :param timeout: int - query timeout in seconds
        :return: bool - True if the query succeeded and no Fault element was found in the result; False otherwise
        '''

        # Set parameters or use defaults if not set.
        if url is None:
            url = self.url
        if timeout is None:
            timeout = self.query_timeout
        if body is None:
            body = self.body
        if params is None:
            params = self.params

        # Set last result, fault, fault code and message and query uuid to be None.
        self.result = None
        self.fault = None
        self.fault_code = None
        self.fault_message = None
        self.query_uuid = None
        self.xml = None

        # Do we need to replace parameters at all?
        if self.set_default_params:
            # If no params are set, use at least an uuid to make the request unique
            if params is None:
                self.query_uuid = uuid.uuid4()
                params = {'uuid': self.query_uuid}
            # If uuid is not set, set it
            elif 'uuid' not in params:
                self.query_uuid = uuid.uuid4()
                params['uuid'] = self.query_uuid

            # Replace all {parameters} in body
            body = body.format(**params)

        # Send the query as POST request
        self.log('Sending query to {0}'.format(url))

        if self.debug:
            self.log(body)

        # Create new session that allows us to specify a custom HTTPAdapter
        session = requests.Session()

        # Use our CustomHTTPAdapter for HTTPS queries, use verify_hostname parameter that was set during initialization
        verify_hostname = self.verify_hostname
        if verify_hostname == True:
            # If set to True, extract the hostname from the URL
            verify_hostname = urlparse(url).hostname

        session.mount('https://', self.CustomHTTPAdapter(verify_hostname))

        # Run POST query
        r = session.post(url=url, data=body, headers=self.headers, timeout=timeout,
                          cert=self.client_certificate, verify=self.server_certificate)

        # Set last XML to be query result
        self.xml = r.text

        if self.debug:
            self.log(r.text)

        # Get the object model from XML
        root = ElementTree.fromstring(self.xml)

        # Get the namespace of the element and save it to ns variable as SOAP-ENV
        rm = re.match('\{(.*)\}', root.tag)
        namespace = rm.group(1) if rm else ''

        ns = {'SOAP-ENV': namespace}

        # Try to find Fault element - if exists, we got an error
        fault = root.find(self.fault_xpath, ns)
        if fault is not None:
            # Return XML string and fault data
            self.fault = {'code': fault.find(self.fault_code_xpath).text,
                          'message': fault.find(self.fault_string_xpath).text,
                          'detail': fault.find(self.fault_detail_xpath).text}
            self.fault_message = self.fault['message']
            self.fault_code = self.fault['code']
            # Return False because we got a fault
            return False

        # Return True because the request succeeded
        return True

    def check_query_success(self, url=None, body=None, params=None, query_timeout=None, faults=None):
        '''
        Sends the query and checks if the result was a success or not. Uses the same parameters as the query() method,
        but can be additionally supplied with a list of faults that are considered errors. If the faults list is
        specified, the function returns True even if there was a fault but it wasn't in the list; otherwise False.
        Wildcards can be used in the end of the fault strings and will only check for a match in the beginning
        of the fault code.
        Example faults:
            ['Server.ServerProxy.ServiceFailed.InvalidContentType'] matches only the full fault code
            ['Server.ServerProxy.*'] matches all Server.ServerProxy faults but if a Server.ClientProxy fault is shown,
                                     it still returns True (query was a success)
            ['Server.ServerProxy.*','Server.ClientProxy.*'] matches all Server.ServerProxy and Server.ClientProxy faults
        :param url: str|None - URL of the service
        :param body: str|None - request body (XML)
        :param params: dict|None - parameters to be replaced in the body; example: body="Hello, {name}",
                                    params={'name': 'John'} will result in body="Hello, John"
        :param query_timeout: int - query timeout in seconds
        :param faults: str|[str]|None|bool - string or list of strings of the codes to be considered real faults,
                                                None or True for all, False for none
        :return: bool - True if the query succeeded and didn't get a (specified) fault; False otherwise
        '''
        # If faults is a string, convert it to list with one item - the same string
        if isinstance(faults, basestring):
            faults = [faults]

        # If no faults specified, check for any.
        if faults is None:
            faults = True

        # Send the query and get the result
        result = self.query(url=url, body=body, params=params, timeout=query_timeout)

        # Log query result
        if self.log:
            self.log('- SOAP query result: fault={0}, code={1}, error={2}'.format(self.fault is not None,
                                                                                  self.fault_code, self.fault))

        if result:
            # We got no fault, so request was successful
            return True

        # We're here, so a fault occured. Let's compare it with out fault list because, depending on the query,
        # all faults may not be considered bad.
        fault_code = self.fault_code

        # If faults is True, we match all errors (strict mode). Because we're here, we had a fault.
        if faults == True:
            # Query did not succeed
            return False

        # Loop over faults list and compare them
        for f in faults:
            # Check if the string ends with a wildcard *
            if f[-1:] == '*':
                # We got a wildcard, check if the code starts with the specified fault
                if fault_code.startswith(f[:-1]):
                    # Match - query did not succeed
                    return False
            else:
                # No wildcards, check equality
                if fault_code == f:
                    # Match - query failed
                    return False

        # Fault was found but not in our fault list so we'll consider this a success.
        return True

    def check_query_loop(self, url=None, body=None, params=None, query_timeout=None, faults=None, fail_timeout=None,
                         retry_interval=None, verify_service=None, check_success=True):
        '''
        Checks for query result like check_query_success but in a loop. Depending on check_success=True (check if the
        query succeeds) or check_success=False (check if the query fails) it tries the query again after retry_interval
        seconds until the condition is met or a timeout (specified by fail_timeout seconds) occurs. If the condition
        is met and, if specified, verify_service conditions match the result service, returns True; otherwise False is
        returned.
        :param url: str|None - URL of the service
        :param body: str|None - request body (XML)
        :param params: dict|None - parameters to be replaced in the body; example: body="Hello, {name}",
                                    params={'name': 'John'} will result in body="Hello, John"
        :param query_timeout: int - query timeout in seconds
        :param faults: str|[str]|None|bool - string or list of strings of the codes to be considered real faults,
                                                None or True for all, False for none
        :param fail_timeout: int - checking failed if this number of seconds pass
        :param retry_interval: int - number of seconds until first try or retry (after failing)
        :param verify_service: dict - parameters to check in the result
        :param check_success: bool - True to wait until the query succeeds; False to wait until it fails
        :return: bool - True if success condition is met and verify_service matches result service; False otherwise
        '''

        # Save the time the check started.
        start_time = time.time()

        # Read default values if parameters are not set.
        if fail_timeout is None:
            fail_timeout = self.fail_timeout
        if retry_interval is None:
            retry_interval = self.retry_interval
        if verify_service is None:
            verify_service = self.verify_service_data

        # Block invalid timeout values.
        if fail_timeout <= 0:
            fail_timeout = 0
        if retry_interval < 0:
            retry_interval = fail_timeout

        # Loop until break statement
        while True:
            if self.log:
                if retry_interval > 0:
                    self.log('Waiting {0} seconds before query'.format(retry_interval))
            time.sleep(retry_interval)

            # Get the result of the query
            result = self.check_query_success(url=url, body=body, params=params, query_timeout=query_timeout,
                                              faults=faults)

            # If we're checking for faults instead, inverse result value
            if not check_success:
                result = not result

            # Now, we have result=True if we got what we wanted, False otherwise. Let's see if we need to verify the
            # service too or not.
            if verify_service is not None:
                result = self.verify_service(verify_service) and result

            # If we got what we wanted, return True
            if result:
                return True

            # If we're here, we still don't have a result we wanted. Let's see if we have enough time to try again.
            if retry_interval == 0 or time.time() > start_time + fail_timeout:
                # Time limit exceeded, we failed, so return False
                return False

    def check_success(self, url=None, body=None, params=None, query_timeout=None, faults=None, fail_timeout=None,
                      retry_interval=None, verify_service=None):
        '''
        Re-checks a query until no (specified) faults are returned and service data verified (if verify_service
         dictionary is set) every retry_interval seconds until timeout occurs. If no specified faults are returned
         by the service and it passes verification, returns True; otherwise returns False.
        :param url: str|None - URL of the service
        :param body: str|None - request body (XML)
        :param params: dict|None - parameters to be replaced in the body; example: body="Hello, {name}",
                                    params={'name': 'John'} will result in body="Hello, John"
        :param query_timeout: int - query timeout in seconds
        :param faults: str|[str]|None|bool - string or list of strings of the codes to be considered real faults,
                                                None or True for all, False for none
        :param fail_timeout: int - checking failed if this number of seconds pass
        :param retry_interval: int - number of seconds until first try or retry (after failing)
        :param verify_service: dict - parameters to check in the result
        :return: bool - True if success condition is met and verify_service matches result service; False otherwise
        '''

        # Default faults are the faults set as "success" faults
        if faults is None:
            faults = self.faults_unsuccessful
        return self.check_query_loop(url=url, body=body, params=params, query_timeout=query_timeout, faults=faults,
                                     fail_timeout=fail_timeout, retry_interval=retry_interval,
                                     verify_service=verify_service,
                                     check_success=True)

    def check_fail(self, url=None, body=None, params=None, query_timeout=None, faults=None, fail_timeout=None,
                   retry_interval=None, verify_service=None):
        '''
        Re-checks a query until a (specified) fault is returned and service data verified (if verify_service
         dictionary is set) every retry_interval seconds until timeout occurs. If specified fault is returned
         by the service and it passes verification, returns True; otherwise returns False.
        :param url: str|None - URL of the service
        :param body: str|None - request body (XML)
        :param params: dict|None - parameters to be replaced in the body; example: body="Hello, {name}",
                                    params={'name': 'John'} will result in body="Hello, John"
        :param query_timeout: int - query timeout in seconds
        :param faults: str|[str]|None|bool - string or list of strings of the codes to be considered real faults,
                                                None or True for all, False for none
        :param fail_timeout: int - checking failed if this number of seconds pass
        :param retry_interval: int - number of seconds until first try or retry (after failing)
        :param verify_service: dict - parameters to check in the result
        :return: bool - True if success condition is met and verify_service matches result service; False otherwise
        '''

        # Default faults are the faults set as "fail" faults
        if faults is None:
            faults = self.faults_unsuccessful
        return self.check_query_loop(url=url, body=body, params=params, query_timeout=query_timeout, faults=faults,
                                     fail_timeout=fail_timeout, retry_interval=retry_interval,
                                     verify_service=verify_service,
                                     check_success=False)

    def get_service(self):
        '''
        Returns service parameters from last result XML or None on error.
        :return: dict{instance, class, code, subsystem, service, service_version} - service data dictionary
        '''

        # If no XML is set, return None
        if self.xml is None:
            return None

        # Get the root element from XML
        root = ElementTree.fromstring(self.xml)

        # Get the namespace of the element and save it to ns variable as SOAP-ENV
        rm = re.match('\{(.*)\}', root.tag)

        # Set the namespace
        namespace = rm.group(1) if rm else ''
        ns = {'SOAP-ENV': namespace, 'xroad': self.xroad_namespace, 'id': self.xroad_identifiers_namespace}

        '''
          Example service tag:
          <xrd:service id:objectType="SERVICE">
             <id:xRoadInstance>KS1</id:xRoadInstance>
             <id:memberClass>GOV</id:memberClass>
             <id:memberCode>TS2OWNER</id:memberCode>
             <id:subsystemCode>sub2</id:subsystemCode>
             <id:serviceCode>xroadGetRandom</id:serviceCode>
             <id:serviceVersion>v1</id:serviceVersion>
          </xrd:service>
        '''

        # Try to find service element - if exists, we got a result
        xroad = root.find(self.xroad_service_xpath, ns)

        if xroad is not None:
            # Return XML string and fault data. Elements are found using set XPaths.
            service_name = xroad.find(self.xroad_service_code_xpath, ns).text
            service_version = xroad.find(self.xroad_service_version_xpath, ns).text
            return {'instance': xroad.find(self.xroad_service_instance_xpath, ns).text,
                    'class': xroad.find(self.xroad_service_member_class_xpath, ns).text,
                    'code': xroad.find(self.xroad_service_member_code_xpath, ns).text,
                    'subsystem': xroad.find(self.xroad_service_member_subsystem_xpath, ns).text,
                    'service': '{0}.{1}'.format(service_name, service_version), 'service_name': service_name,
                    'service_version': service_version}
        return None

    def verify_service(self, service=None):
        '''
        Verifies that the parameters set match the ones returned in the last XML result.
        If parameter service is a match or a subset of the last service data, returns True; otherwise False
        :param service: dict - service parameters to verify
        :return: bool - True if service is a subset of last XML service data; False otherwise
        '''
        if service is None:
            service = self.verify_service_data

        # If nothing to verify, return None
        if service is None:
            return None

        # Get service data from latest response
        responder_service = self.get_service()

        # If no data, not a match.
        if responder_service is None:
            return False

        # Return: if service data items are a subset of latest response service data items
        return set(service.items()).issubset(responder_service.items())
