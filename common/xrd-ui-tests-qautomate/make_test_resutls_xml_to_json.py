import xml.etree.ElementTree as ET
from pprint import pprint
import urllib2
import json

import sys

print("Usage: make_test_resutls_xml_to_json.py project_id test_set_instance_id browser_name sw_version apitoken")

arguments = {}
r = 0
for arg in sys.argv:
    arguments[r] = arg
    r = r + 1

PROJECT_ID = str(arguments[1])
INSTANCE_ID = str(arguments[2])
BROWSER_NAME = str(arguments[3])
SW_VERSION = str(arguments[4])
API_TOKEN = str(arguments[5])
URL = "https://prod.practitest.com/api/automated_tests/upload_test_result.json"
AUTH = {'Authorization': "custom api_token=" + API_TOKEN, "Content-Type": "application/json"}

tree = ET.parse('test_reports/TEST-unittest.suite.TestSuite.xml')
root = tree.getroot()

for child in root:
    first_child = child.tag
    tc_id = ""
    if first_child == "testcase":
        tc_name_full = child.get('name')
        tc_id = tc_name_full.split("_")[-1]
        print("TC_NAME: " + tc_name_full + " and TC_ID: " + tc_id)
        failure = 0
        for next_child in child:
            duration = next_child.get("time")
            if next_child.get("failure") == None:
                print("Failure case")
                failure = 1
            else:
                failure = 0
        payload = {
            "project_id": PROJECT_ID ,
            "instance_display_id" : INSTANCE_ID + ":" + tc_id,
            "duration": '00:00:00',
            "instance_custom_fields":[{"name":"browser","value": BROWSER_NAME},{"name":"SW_version","value": SW_VERSION}],
            "exit_code": failure
            }

        pprint(payload)
        payload = json.dumps(payload)
        req = urllib2.Request(URL, payload, AUTH)
        try:
            resp = urllib2.urlopen(req)
            print(resp.code)
        except urllib2.URLError, e:
            print(e.code)
            print("Body:", e.read()) # this one returns the body string