# -*- coding: utf-8 -*-
from variables import strings, errors
from webframework import TESTDATA
import subprocess
import os
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.config import get_config_value
from webframework.extension.util.file_utils import get_file_content
from time import sleep

class Common_lib_ssh(CommonUtils):
    """
    Common library for ssh or lxd connection handeling

    Changelog:
    * 19.10.2017
        | Ssh methods added for file manipulation
    * 11.07.2017
        | Documentation updated
    """

    def __init__(self):
        """
        Initilization method for moving test data to class

        *Updated: 11.07.2017*

        """
        CommonUtils.__init__(self)
        self.log_file_output = ""
        self.run_folder = ""

    def find_exception_from_logs_and_save(self, start_time, stop_time, name_prefix="", copy_location=""):
        """
        Find exceptions from logs and save them
        """

        self.run_folder = get_config_value("reporting_folder_run")
        self.report_folder = get_config_value("reporting_folder")
        error_log_file = open(self.report_folder + os.sep + "error_logs.txt", "w")
        error_log_file.write("\nLOG START TIME: " + start_time + "\n")
        has_error = False
        for log_file in strings.ss_all_logs:
            log_file_name = log_file.split("/")[-1]
            try:
                log_content = get_file_content(os.path.join(self.run_folder, log_file_name))
            except:
                continue

            for line in log_content:
                if "] ERROR" in line.upper():
                    has_error = True
                    print(log_file_name + ": " + line)
                    error_log_file.write(log_file_name + ": " + line)
                elif ".EXCEPTION" in line.upper():
                    has_error = True
                    error_log_file.write(log_file_name + ": " + line)
                elif "HTTPERROR" in line.upper():
                    has_error = True
                    error_log_file.write(log_file_name + ": " + line)

        error_log_file.write("\nLOG STOP TIME: " + stop_time)
        error_log_file.close()
        if has_error:
            self.warning("Error log has errors")
        for log_file in strings.ss_all_logs:
            log_file_name = log_file.split("/")[-1]
            copy_location = copy_location.split("error_logs.txt")[0]
            print(copy_location)
            try:
                if not os.path.exists(copy_location):
                    os.makedirs(copy_location)
                command = "sudo cp " + self.run_folder + os.sep + log_file_name + " " + copy_location + name_prefix + "_" + log_file_name

                self.run_bash_command(command, True)
            except AssertionError:
                self.warning("Could not copy file " + log_file_name)

        return has_error

    # server="jenkins@test-cs2.i.palveluvayla.com" or xroad-lxd-cs
    def empty_server_log_files(self, server):
        """
        **Test steps:**
                * **Step 2:** :func:`~pagemodel.run_bash_command(formated_command.Run_bash_command(formated_command.format`, *formated_command.format(server*, *'service rsyslog rotate'*, *""*
        """
        shell_command = 'sudo truncate -c -s 0'
        if strings.server_environment_type() == strings.lxd_type_environment:
            server = server.split(".lxd")[0]
            formated_command ="lxc exec {} -- bash -c '{} {} || true'"
        elif strings.server_environment_type() == strings.ssh_type_environment:
            formated_command = "ssh {} {} {} || true"
        else:
            raise Exception(errors.enviroment_type_not_valid)
        for log_file in strings.ss_all_logs:
            command = formated_command.format(server, shell_command, log_file)
            self.run_bash_command(command, False)
        self.run_bash_command(formated_command.format(server, 'service rsyslog rotate', ""), False)

    def collect_server_log_files(self, server="xroad-lxd-cs"):
        """
        """
        self.run_folder = get_config_value("reporting_folder_run")
        if strings.server_environment_type() == strings.lxd_type_environment:
            server = server.split(".lxd")[0]
            formated_command = "lxc file pull {}{} " + self.run_folder + "/{} || true"
        elif strings.server_environment_type() == strings.ssh_type_environment:
            print(self.run_folder)
            formated_command = "ssh {} sudo cat {} > " + self.run_folder + "/{} || true"
        else:
            raise Exception(errors.enviroment_type_not_valid)
        for log_file in strings.ss_all_logs:
            command = formated_command.format(server, log_file, log_file.split("/")[-1])
            self.run_bash_command(command, True)

    def delete_files_from_directory(self, section="cs_url", path=u'/var/lib/xroad/backup'):
        """
        :param section:  Test data section name
        """
        server = TESTDATA[section][u'server_address']
        if strings.server_environment_type() == strings.lxd_type_environment:
            server = server.split(".lxd")[0]
            command = "lxc exec {} -- sudo rm -rf {}".format(server, path)
        elif strings.server_environment_type() == strings.ssh_type_environment:
            command = "ssh {} sudo rm -rf {}".format(server, path)
        else:
            raise Exception(errors.enviroment_type_not_valid)

        self.run_bash_command(command, True)

    def generate_empty_file(self, section, path):
        """
        :param section:  Test data section name
        """
        server = TESTDATA[section][u'server_address']
        if strings.server_environment_type() == strings.lxd_type_environment:
            server = server.split(".lxd")[0]
            command = "lxc exec {} -- sudo touch {}".format(server, path)
        elif strings.server_environment_type() == strings.ssh_type_environment:
            command = "ssh {} sudo touch {}".format(server, path)
        else:
            raise Exception(errors.enviroment_type_not_valid)

        self.run_bash_command(command, True)

    def change_file_permission(self, section, path, permission):
        """
        :param section:  Test data section name
        """
        server = TESTDATA[section][u'server_address']
        if strings.server_environment_type() == strings.lxd_type_environment:
            server = server.split(".lxd")[0]
            command = "lxc exec {} -- sudo chmod {} {}".format(server, permission, path)
        elif strings.server_environment_type() == strings.ssh_type_environment:
            command = "ssh {} sudo chmod {} {}".format(server, permission, path)
        else:
            raise Exception(errors.enviroment_type_not_valid)

        self.run_bash_command(command, True)

    def move_file(self, section, move_from, move_to):
        """
        :param section:  Test data section name
        """
        server = TESTDATA[section][u'server_address']
        if strings.server_environment_type() == strings.lxd_type_environment:
            server = server.split(".lxd")[0]
            command = "lxc exec {} -- sudo mv {} {}".format(server, move_from, move_to)
        elif strings.server_environment_type() == strings.ssh_type_environment:
            command = "ssh {} sudo touch {} {}".format(server, move_from, move_to)
        else:
            raise Exception(errors.enviroment_type_not_valid)

        self.run_bash_command(command, True)

    def run_bash_command(self, command, to_print=True):
        """
        Runs bash command

        """
        if to_print:
            print(command)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, com_errors = p.communicate()
        if com_errors:
            self.fail(com_errors)
        return output

    def read_server_file(self, server="xroad-lxd-cs", log_file_name="/var/log/xroad/audit.log"):
        """
        Read file from given path in server

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.log_file_output = self.Log_file_output = self.run_bash_command`, *command*
        """
        if strings.server_environment_type() == strings.lxd_type_environment:
            server = server.split(".lxd")[0]
            command ="lxc exec {} -- tail -n 30 {}". format(server, log_file_name)
        elif strings.server_environment_type() == strings.ssh_type_environment:
            command = "ssh {} exec -- sudo tail -n 30 {}".format(server, log_file_name)
        else:
            raise Exception(errors.enviroment_type_not_valid)
        self.log_file_output = self.run_bash_command(command)
        return self.log_file_output

    def parse_log_file_tail(self, log_output="", row_count=5):
        """
        Parse log file to show x number of rows
        """
        last_rows = [row for row in log_output.strip().split("\n") if row.strip()][-int(row_count):]
        return "\n".join(last_rows)

    def verify_audit_log(self, section=u'ss1_url', event="Log in user"):
        """
        Verify audit log file in server.

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.fail(errors.Fail(errors.audit_log_is_empty)`, *errors.audit_log_is_empty*
                * **Step 2:** :func:`~pagemodel.fail(errors.Fail(errors.string_is_not_dict + "\n" + self`, *errors.string_is_not_dict + "\n" + self.parse_log_file_tail(log_output*
                * **Step 3:** :func:`~pagemodel.fail(errors.Fail(errors.log_event_fail`, *errors.log_event_fail(event*
                * **Step 4:** :func:`~pagemodel.fail(errors.Fail(errors.log_user_fail`, *errors.log_user_fail(user*
        """

        # Sleep waiting log
        sleep(1)

        server_log_address = TESTDATA[section][u'server_address']
        user = TESTDATA[section][u'j_username']
        log_output = self.read_server_file(server_log_address, strings.audit_log)

        # Prints full log string
        newest_log_string = self.parse_log_file_tail(log_output, row_count=1)
        print(newest_log_string)
        newest_log = newest_log_string[newest_log_string.find("{"):]
        print(newest_log)
        if not newest_log:
            self.fail(errors.audit_log_is_empty)
        newest_log = eval(newest_log, {"null":None})
        print("Log event:", newest_log["event"])
        print("Log user:", newest_log["user"])
        if not isinstance(newest_log, dict):
            self.fail(errors.string_is_not_dict + "\n" + self.parse_log_file_tail(log_output))
        if not event == newest_log["event"]:
            self.fail(errors.log_event_fail(event) + "\n" + self.parse_log_file_tail(log_output))
        if not user == newest_log["user"]:
            self.fail(errors.log_user_fail(user) + "\n" + self.parse_log_file_tail(log_output))


    def get_all_logs_from_server(self, section):
        """
        :param section:  Test data section name
        """
        server_log_address = TESTDATA[section][u'server_address']
        try:
            print("GETTING ALL LOGS")
            log_output = self.collect_server_log_files(server_log_address)
        except Exception as e:
            print("Could not read all log file" + str(e))

    def empty_all_logs_from_server(self, section):
        """
        :param section:  Test data section name
        """
        server_log_address = TESTDATA[section][u'server_address']
        try:
            log_output = self.empty_server_log_files(server_log_address)
        except Exception as e:
            print("Could not read all log file" + str(e))