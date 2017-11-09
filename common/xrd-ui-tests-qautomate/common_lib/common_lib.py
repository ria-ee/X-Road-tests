# -*- coding: utf-8 -*-
from webframework import TESTDATA
import subprocess
import os
import glob
from urlparse import urlparse
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep

# Library file allows define common methods, which can be
# added to test cases or page models
from pagemodel.common_elements import Common_elements

class Common_lib(CommonUtils):
    """
    Common library that contains useful methods for testing

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_elements = Common_elements()

    def read_liityntapalvelin_konfiguraatio_parameters(self, parameters=None):
        """

        :param parameters:  Test data section dictionary
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.add_dynamic_content_to_parameters(parameters, "data_folder", WORKSPACE + os.Add_dynamic_content_to_parameters(parameters, "data_folder", workspace + os.sep + GIT_WORKING_DIR + os`, *parameters*, *"data_folder"*, *WORKSPACE + os.sep + GIT_WORKING_DIR + os.sep + "data" + os.sep*, *u'paths'*
        """

        # Read asennus file if exists
        try:
            content = ""
            print(os.getcwd() + "\n")
            conf_file_path = os.getcwd() + os.sep + "liityntapalvelin_asennus_konfiguraatio.txt"
            print(conf_file_path)
            with open(conf_file_path) as f:
                content = f.readlines()
            table_content = content[0].split(",")
            SERVER_FULL_URL = table_content[0]
            MEMBER_NAME = table_content[1]
            MEMBER_CLASS = table_content[2]
            MEMBER_CODE = table_content[3]
            MEMBER_NAME_SUB = table_content[4]
            CENTRAL_SERVER_FULL_URL = table_content[5]
            TSP_URL = table_content[6]
            SYNC_TIMEOUT = table_content[7]
            LOGIN_CS_USERNAME = table_content[8]
            LOGIN_CS_PASSWORD = table_content[9]
            LOGIN_SS_USERNAME = table_content[10]
            LOGIN_SS_PASSWORD = table_content[11]
            XROAD_ID = table_content[12]
            CS_PIN_CODE = table_content[13]
            SS_PIN_CODE = table_content[14]
            APPROVED_CA = table_content[15]
            SIGN_CERT_SERVER = table_content[16]
            SIGN_CERT_SSH_KEY = table_content[17]
            SIGNED_KEY_FORMAT = table_content[18]
            WORKSPACE = table_content[19]
            GIT_WORKING_DIR = table_content[20]

            # CERTIFICATES FOLDER PEM
            self.add_dynamic_content_to_parameters(parameters, "data_folder", WORKSPACE + os.sep + GIT_WORKING_DIR + os.sep + "data" + os.sep, u'paths')

            # GENERAL SETTINGS
            if SIGN_CERT_SSH_KEY == "" or SIGN_CERT_SSH_KEY == "empty":
                auth_key = ""
            else:
                auth_key = "-i " + SIGN_CERT_SSH_KEY
            self.add_dynamic_content_to_parameters(parameters, "sign_cert_format", SIGNED_KEY_FORMAT, u'paths')
            if not "lxc" in SIGN_CERT_SERVER:
                self.add_dynamic_content_to_parameters(parameters, "sign_cert_server_connect_parameters", "ssh " + SIGN_CERT_SERVER + " " + auth_key, u'paths')
            else:
                self.add_dynamic_content_to_parameters(parameters, "sign_cert_server_connect_parameters", SIGN_CERT_SERVER, u'paths')

            # Server conf
            self.add_dynamic_content_to_parameters(parameters, "member_name", MEMBER_NAME, u'member1_configuration')
            self.add_dynamic_content_to_parameters(parameters, "member_class", MEMBER_CLASS, u'member1_configuration')
            self.add_dynamic_content_to_parameters(parameters, "member_code", MEMBER_CODE, u'member1_configuration')
            self.add_dynamic_content_to_parameters(parameters, "tsp_url", TSP_URL, u'ss1_url')
            self.add_dynamic_content_to_parameters(parameters, "tsp_url", TSP_URL, u'cs_url')

            self.add_dynamic_content_to_parameters(parameters, "member_id", "SUBSYSTEM : " + XROAD_ID + " : " + MEMBER_CLASS + " : " + MEMBER_CODE + " : " +  MEMBER_NAME_SUB, u'member1_configuration')
            self.add_dynamic_content_to_parameters(parameters, "member_name", MEMBER_NAME, u'member1_configuration')
            self.add_dynamic_content_to_parameters(parameters, "member_class", MEMBER_CLASS, u'member1_configuration')
            self.add_dynamic_content_to_parameters(parameters, "member_code", MEMBER_CODE, u'member1_configuration')
            self.add_dynamic_content_to_parameters(parameters, "subsystem_code", MEMBER_NAME_SUB,
                                                   u'member1_configuration')
            self.add_dynamic_content_to_parameters(parameters, "sync_timeout", SYNC_TIMEOUT, u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "sync_timeout", SYNC_TIMEOUT, u'ss1_url')
            self.add_dynamic_content_to_parameters(parameters, "pin", CS_PIN_CODE, u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "pin", SS_PIN_CODE, u'ss1_url')
            self.add_dynamic_content_to_parameters(parameters, "instance_identifier", XROAD_ID, u'member1_configuration')

            # Servers
            self.add_dynamic_content_to_parameters(parameters, "url", SERVER_FULL_URL + "/login", u'ss1_url')
            self.add_dynamic_content_to_parameters(parameters, "url", CENTRAL_SERVER_FULL_URL + "/login", u'cs_url')

            # Get logs servers
            server_tmp = SERVER_FULL_URL.replace(':4000', "")
            server_url = server_tmp.replace('https://',"")
            server_tmp = CENTRAL_SERVER_FULL_URL.replace(':4000', "")
            central_server_url = server_tmp.replace('https://',"")
            server_url_short = server_url.split(".")[0]
            self.add_dynamic_content_to_parameters(parameters, "server1", server_url, u'log_server')
            self.add_dynamic_content_to_parameters(parameters, "server2", central_server_url, u'log_server')
            self.add_dynamic_content_to_parameters(parameters, "security_server_code", server_url_short,
                                                   u'member1_configuration')

            # Keys
            self.add_dynamic_content_to_parameters(parameters, "approved_ca", APPROVED_CA, u'server_environment')
            self.add_dynamic_content_to_parameters(parameters, "server_address", server_url, u'member1_configuration')
            # Subsystem

            # Login cs
            self.add_dynamic_content_to_parameters(parameters, "j_username", LOGIN_CS_USERNAME, u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "j_password", LOGIN_CS_PASSWORD, u'cs_url')
            # Login ss
            self.add_dynamic_content_to_parameters(parameters, "j_username", LOGIN_SS_USERNAME, u'ss1_url')
            self.add_dynamic_content_to_parameters(parameters, "j_password", LOGIN_SS_PASSWORD, u'ss1_url')
        except:
            print("Could not read dynamic conf file, Using default settings xml file")
            pass

    def read_keskuspalvelin_konfiguraatio_parameters(self, parameters=None):
        """

        :param parameters:  Test data section dictionary
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.add_dynamic_content_to_parameters(parameters, "data_folder", WORKSPACE + os.Add_dynamic_content_to_parameters(parameters, "data_folder", workspace + os.sep + GIT_WORKING_DIR + os`, *parameters*, *"data_folder"*, *WORKSPACE + os.sep + GIT_WORKING_DIR + os.sep + "data" + os.sep*, *u'paths'*
        """
        try:
            content = ""
            print(os.getcwd() + "\n")
            conf_file_path = os.getcwd() + os.sep + "keskuspalvelin_asennus_konfiguraatio.txt"
            print(conf_file_path)
            with open(conf_file_path) as f:
                content = f.readlines()
            table_content = content[0].split(",")
            CS_SERVER_FULL_URL = table_content[0]
            SS_MGM_CS_SERVER_FULL_URL = table_content[1]
            CS_MEMBER_NAME = table_content[2]
            CS_MEMBER_CLASS = table_content[3]
            CS_MEMBER_CODE = table_content[4]
            MEMBER_NAME_SUB = table_content[5]
            TSP_URL = table_content[6]
            SYNC_TIMEOUT = table_content[7]
            LOGIN_CS_USERNAME = table_content[8]
            LOGIN_CS_PASSWORD = table_content[9]
            LOGIN_SS_MGM_CS_USERNAME = table_content[10]
            LOGIN_SS_MGM_CS_PASSWORD = table_content[11]
            XROAD_ID = table_content[12]
            CS_PIN_CODE = table_content[13]
            SS_PIN_CODE = table_content[14]
            CS_MEMBER_CLASS_DESC = table_content[15]
            OCSP_RESPONDER_URL = table_content[16]
            APPROVED_CA = table_content[17]
            SIGN_CERT_SERVER = table_content[18]
            SIGN_CERT_SSH_KEY = table_content[19]
            SIGNED_KEY_FORMAT = table_content[20]
            WORKSPACE= table_content[21]
            GIT_WORKING_DIR = table_content[22]

            # CERTIFICATES FOLDER PEM
            self.add_dynamic_content_to_parameters(parameters, "data_folder", WORKSPACE + os.sep + GIT_WORKING_DIR + os.sep + "data" + os.sep, u'paths')

            # GENERAL SETTINGS
            if SIGN_CERT_SSH_KEY == "" or SIGN_CERT_SSH_KEY == "empty":
                auth_key = ""
            else:
                auth_key = "-i " + SIGN_CERT_SSH_KEY
            self.add_dynamic_content_to_parameters(parameters, "sign_cert_format", SIGNED_KEY_FORMAT, u'paths')
            if not "lxc" in SIGN_CERT_SERVER:
                self.add_dynamic_content_to_parameters(parameters, "sign_cert_server_connect_parameters", "ssh " + SIGN_CERT_SERVER + " " + auth_key, u'paths')
            else:
                self.add_dynamic_content_to_parameters(parameters, "sign_cert_server_connect_parameters", SIGN_CERT_SERVER, u'paths')

            # Server conf
            self.add_dynamic_content_to_parameters(parameters, "member_name", CS_MEMBER_NAME, u'member_mgm_configuration')
            self.add_dynamic_content_to_parameters(parameters, "member_class", CS_MEMBER_CLASS, u'member_mgm_configuration')
            self.add_dynamic_content_to_parameters(parameters, "member_code", CS_MEMBER_CODE, u'member_mgm_configuration')
            self.add_dynamic_content_to_parameters(parameters, "member_class_description", CS_MEMBER_CLASS_DESC, u'member_mgm_configuration')

            self.add_dynamic_content_to_parameters(parameters, "member_id", "SUBSYSTEM : " + XROAD_ID + " : " + CS_MEMBER_CLASS + " : " + CS_MEMBER_CODE + " : " +  MEMBER_NAME_SUB, u'member_mgm_configuration')
            self.add_dynamic_content_to_parameters(parameters, "sync_timeout", SYNC_TIMEOUT, u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "pin", CS_PIN_CODE, u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "pin", SS_PIN_CODE, u'ss_mgm_url')
            self.add_dynamic_content_to_parameters(parameters, "instance_identifier", XROAD_ID, u'member_mgm_configuration')
            self.add_dynamic_content_to_parameters(parameters, "instance_identifier", XROAD_ID, u'cs_url')

            self.add_dynamic_content_to_parameters(parameters, "subsystem_code", MEMBER_NAME_SUB, u'member_mgm_configuration')

            # Get logs servers
            server_tmp = CS_SERVER_FULL_URL.replace(':4000', "")
            central_server_url = server_tmp.replace('https://',"")
            server_tmp = SS_MGM_CS_SERVER_FULL_URL.replace(':4000', "")
            ss_mgm_server_url = server_tmp.replace('https://', "")
            ss_mgm_server_url_short = ss_mgm_server_url.split(".")[0]

            self.add_dynamic_content_to_parameters(parameters, "server1", central_server_url, u'log_server')
            self.add_dynamic_content_to_parameters(parameters, "server2", ss_mgm_server_url, u'log_server')
            self.add_dynamic_content_to_parameters(parameters, "security_server_code", ss_mgm_server_url_short,
                                                   u'member_mgm_configuration')

            # Servers
            self.add_dynamic_content_to_parameters(parameters, "tsp_url", TSP_URL, u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "ocsp_responder_url", OCSP_RESPONDER_URL, u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "url", CS_SERVER_FULL_URL + "/login", u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "url", SS_MGM_CS_SERVER_FULL_URL + "/login",
                                                   u'ss_mgm_url')
            self.add_dynamic_content_to_parameters(parameters, "server_address", central_server_url, u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "server_address", ss_mgm_server_url,
                                                   u'member_mgm_configuration')

            # Keys Sign
            self.add_dynamic_content_to_parameters(parameters, "approved_ca", APPROVED_CA, u'server_environment')

            # Subsystem
            self.add_dynamic_content_to_parameters(parameters, "subsystem_code", MEMBER_NAME_SUB, u'member_mgm_configuration')
            # Login cs
            self.add_dynamic_content_to_parameters(parameters, "j_username", LOGIN_CS_USERNAME, u'cs_url')
            self.add_dynamic_content_to_parameters(parameters, "j_password", LOGIN_CS_PASSWORD, u'cs_url')
            # Login ss mgm cs
            self.add_dynamic_content_to_parameters(parameters, "j_username", LOGIN_SS_MGM_CS_USERNAME, u'ss_mgm_url')
            self.add_dynamic_content_to_parameters(parameters, "j_password", LOGIN_SS_MGM_CS_PASSWORD, u'ss_mgm_url')
        except Exception as e:
            print(str(e))
            print("Could not read dynamic conf file, Using default settings xml file")
            pass

    def sync_global_conf(self, parameters=None):
        """
        :param parameters:  Test data section dictionary
        """
        print("Waiting global conf sync time: " + str(parameters))
        sleep(float(parameters))

    def send_soap_api_request_hello(self, parameters=None):
        """
        :param parameters:  Test data section dictionary
        """
        print("Sending Soap request")
        print("Request: " + "http://" + parameters[u'address'] + ", " + parameters[u'request'] + ", " + parameters[u'response'])
        sleep(3)
        self.verify_soap_api_value("http://" + parameters[u'address'] , parameters[u'request'] , parameters[u'response'] )

    def log_out(self):
        """
        **Test steps:**
                * **Step 2:** :func:`~common_lib.common_elements.Common_elements.click_user_info`
                * **Step 3:** :func:`~common_lib.common_elements.Common_elements.click_log_out`
        """
        print("waiting logout")
        sleep(2)
        self.wait_until_jquery_ajax_loaded()
        self.common_elements.click_user_info()
        sleep(2)
        try:
            self.common_elements.click_log_out()
        except:
            current_url = urlparse(self.get_current_url())
            current_url = current_url.scheme + "://" + current_url.netloc + "/login/logout"
            print(current_url)
            self.go_to(current_url)
            self.warning("Logged out using browser url")
        sleep(2)

    def verify_cert_request(self, parameters):
        """
        :param parameters:  Test data section dictionary
        """
        # Wait while for downloading der file
        sleep(10)
        try:
            newest_der = max(glob.iglob(parameters[u'downloads_folder'] + '*.der'), key=os.path.getctime)
            print(newest_der)
        except:
            print("Certificate download failed")
            print(subprocess.check_output("ls " + parameters[u'downloads_folder'], shell=True))
            raise Exception("Certificate download failed")

        try:
            cert_string = subprocess.check_output("openssl req -in " +  newest_der + " -text -noout -inform DER", shell=True)
            begin_index = str(cert_string).find("Subject:")
            end_index = str(cert_string).find("Subject Public Key")
            print(str(cert_string)[begin_index:end_index])
            #os.system("sudo rm " + newest_p10)
            return True
        except Exception as e:
            print("Certificate file cannot be read")
            print(e)
            return False

    def remove_anchor_and_certs_from_downloads(self, parameters):
        """

        :param parameters:  Test data section dictionary
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.delete_files_with_extension(parameters[u'downloads_folder'], ".Delete_files_with_extension(parameters[u'downloads_folder'], ".p10")`, *parameters[u'downloads_folder']*, *".p10"*
                * **Step 2:** :func:`~pagemodel.delete_files_with_extension(parameters[u'downloads_folder'], ".Delete_files_with_extension(parameters[u'downloads_folder'], ".der")`, *parameters[u'downloads_folder']*, *".der"*
                * **Step 3:** :func:`~pagemodel.delete_files_with_extension(parameters[u'downloads_folder'], ".Delete_files_with_extension(parameters[u'downloads_folder'], ".pem")`, *parameters[u'downloads_folder']*, *".pem"*
                * **Step 4:** :func:`~pagemodel.delete_files_with_extension(parameters[u'downloads_folder'], ".Delete_files_with_extension(parameters[u'downloads_folder'], ".xml")`, *parameters[u'downloads_folder']*, *".xml"*
        """
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".p10")
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".der")
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".pem")
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".xml")

    def remove_cert_from_downloads(self, parameters):
        """

        :param parameters:  Test data section dictionary
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.delete_files_with_extension(parameters[u'downloads_folder'], ".Delete_files_with_extension(parameters[u'downloads_folder'], ".der")`, *parameters[u'downloads_folder']*, *".der"*
        """
        self.delete_files_with_extension(parameters[u'downloads_folder'], ".der")

    def delete_files_with_extension(self, folder, extension):
        """
        """
        files = glob.iglob(folder + '*' + extension)
        for _file in files:
            print _file
            try:
                os.system("sudo rm " + _file)
            except:
                print("Could not delete", _file, "file from Downloads")

    def read_cert_number_request(self, cert_type):
        """
        """
        try:
            cert_number = subprocess.check_output("openssl x509 -in " +  "scripts/" + cert_type + "-cert_automation.der" + " -serial -noout", shell=True)
            print(cert_number)
            cert_number = cert_number.split('=')
            number_decimal = int("0x" + str(cert_number[1].lower()), 16)
            print(number_decimal)
            return str(number_decimal)
        except Exception as e:
            print("Certificate file cannot be read")
            print(e)
            return ""

    def copy_and_sign_cert_request(self, parameters):
        """
        :param parameters:  Test data section dictionary
        """
        print("copy and sign start")
        print(os.getcwd() + "\n")
        call_string = "./scripts/copy_and_sign.sh " + parameters[u'downloads_folder'] + " " + parameters[u'sign_cert_format'] + " '" + parameters[u'sign_cert_server_connect_parameters'] + " sign-sign'"
        print(call_string)
        subprocess.call(call_string,shell=True)

    def copy_and_auth_cert_request(self, parameters):
        """
        :param parameters:  Test data section dictionary
        """
        print("copy and auth start")
        print(os.getcwd() + "\n")
        call_string = "./scripts/copy_and_auth.sh " + parameters[u'downloads_folder'] + " " + parameters[u'sign_cert_format'] + " '" + parameters[u'sign_cert_server_connect_parameters'] + " sign-auth'"
        print(call_string)
        subprocess.call(call_string,shell=True)

    def revoke_cert(self, parameters):
        """
        :param parameters:  Test data section dictionary
        """
        print("revoke start")
        print("./scripts/revoke.sh " + parameters[u'sign_cert_format'] + " " + parameters[u'sign_cert_server_connect_parameters'])
        subprocess.call("./scripts/revoke.sh " + parameters[u'sign_cert_format'] + " '" + parameters[u'sign_cert_server_connect_parameters'] + "'",shell=True)
        os.system("sudo mv " + "scripts/sign-cert_automation.der old.der" )

    def revoke_cert_auth(self, parameters):
        """
        :param parameters:  Test data section dictionary
        """
        print("revoke auth start")
        subprocess.call("./scripts/revoke_auth.sh " + parameters[u'sign_cert_format'] + " '" + parameters[u'sign_cert_server_connect_parameters'] + "'",shell=True)
        os.system("sudo mv " + "scripts/auth-cert_automation.der old.der" )

    def get_ui_error_message(self):
        """
        """
        if self.is_visible((By.CLASS_NAME, u'alerts'), 2):
            msg = self.get_text((By.CLASS_NAME, u'alerts'))
            print("ALERT IS PRESENT: " + msg)
        if self.is_visible((By.CLASS_NAME, u'message'), 1):
            msg = self.get_text((By.CLASS_NAME, u'message'))
            print("MESSAGE: " + msg)

    def get_version_information(self):
        """
        """
        try:
            system_call_string = 'output=$(curl -s -k -d "j_username=ui&j_password=kapabTY" -c cookies https://test-ss1.i.palveluvayla.com:4000/j_security_check && curl -s -k -b cookies https://test-ss1.i.palveluvayla.com:4000/about | grep "Security Server version");echo $output | head -n1 | cut -d " " -f4'
            print(os.system(system_call_string))
        except:
            print("error getting version")

    def get_log_utc_time(self):
        """
        """
        from datetime import datetime
        log_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
        print(log_time)
        return log_time

    def type_file_name_pyautogui(self, type_string):
        """
        """
        sleep(3)
        import pyautogui
        try:
            output = subprocess.check_output('lsb_release -r', shell=True)
            print(output)
        except Exception as e:
            print(e)
        pyautogui.press('end')
        for i in range(0,30):
            pyautogui.press('backspace', interval=0.01)

        if "16" in output:
            splitted_path = type_string.split("/")
            for i in range(0,len(splitted_path)):
                if not splitted_path[i] == "" and i > 0:
                    pyautogui.hotkey('shift','7')
                    pyautogui.typewrite(splitted_path[i])
            sleep(1)
            pyautogui.press('enter')
        else:
            pyautogui.typewrite(type_string, interval=0.05)
        sleep(0.5)
        pyautogui.press('enter')

    def get_logs_report(self, start_time, stop_time, get_log_server="", get_log_type="", get_logs_folder=""):
        """
        """
        print("Get server logs for report")
        print(start_time)
        print(stop_time)
        folder_out = os.getcwd()
        if get_logs_folder == "" :
            get_logs_folder = "/home/jenkins/fetch-elasticsearch-logs/"
        if get_log_type == "":
            get_log_type = "jettylog"
        if get_log_server ==  "":
            get_log_server = "test-cs2.i.palveluvayla.com"
        get_logs_cmd = "get-logs.sh"
        command_input = get_logs_folder + get_logs_cmd + ' ' + get_log_type + ' ' +get_log_server + ' ' + start_time + ' ' + stop_time + ' > ' + get_logs_folder + 'server_' + get_log_type
        print(command_input)
        try:
            output = subprocess.check_output(command_input, shell=True)
            print(output)
        except Exception as e:
            print(e)
        print("Parsing log simplified format")
        import json
        try:
            data = json.loads(open(get_logs_folder + 'server_jettylog').read())
            fname = get_logs_folder + 'server_log.txt'
            if not os.path.isfile(fname):
                f=open(fname, 'w')
                f.close()
            log_msg_len = len(data["hits"]["hits"])
            f=open(fname, 'a')
            f.write("SERVER_LOG_TYPE: " + get_log_type + " SERVER_LOG_HOST: " + get_log_server + "\n")

            for i in range(0,log_msg_len-1):
                timestamp = data["hits"]["hits"][i]["_source"]["@timestamp"]
                severity = data["hits"]["hits"][i]["_source"]["severity"]
                host = data["hits"]["hits"][i]["_source"]["host"]
                msg = data["hits"]["hits"][i]["_source"]["message"]
                msg = msg.encode('ascii', 'ignore')
                if msg[-1].isspace():
                    msg_edited = msg[:-1]
                else:
                    msg_edited = msg
                log_msg =  timestamp + " " + severity + " " + host + " " + '"' + msg_edited + '"' + "\n"
                f.write(log_msg)
            f.close()
        except Exception as e:
            print(e)
