# coding=utf-8
import unittest

from helpers import xroad, auditchecker, ssh_client
from main.maincontroller import MainController
from tests.xroad_configure_service_222 import wsdl_validator_errors, configure_service
from tests.xroad_configure_service_222.wsdl_validator_errors import set_wsdl_validator_invalid_command, \
    remove_wsdl_validator_from_conf, set_wsdl_validator_not_executable
from tests.xroad_refresh_wsdl_225.refresh_wsdl import webserver_set_wsdl


class XroadWsdlValidatorErrors(unittest.TestCase):
    """
    SERVICE_08 6a, 6d, 6e adding WSDL Validator config errors test
    SERVICE_14 3a, 3d, 3e refreshing WSDL Validator config errors test
    Reloading application in this test may take up to ~10 minutes,
    so the whole test worst case running time is around 40 minutes
    RIA URL: https://jira.ria.ee/browse/XTKB-22
    RIA URL: https://jira.ria.ee/browse/XTKB-26
    Depends on finishing other test(s): XroadSecurityServerClientRegistration
    Requires helper scenarios: add wsdl, refresh wsdl
    X-Road version: 6.16.0
    """

    def test_xroad_wsdl_validator_errors(self):
        main = MainController(self)

        main.test_number = 'SERVICE_08/14'
        main.test_name = self.__class__.__name__

        ssh_host = main.config.get('ss1.ssh_host')
        ssh_user = main.config.get('ss1.ssh_user')
        ssh_pass = main.config.get('ss1.ssh_pass')

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        client_id = xroad.split_xroad_id(main.config.get('ss1.client_id'))
        client_name = main.config.get('ss1.client_name')

        '''Not executable file path'''
        not_exec_file_path = '/etc/xroad/conf.d/notExecutableParser'
        wsdl_local_path = main.config.get('wsdl.local_path')
        wsdl_remote_path = main.config.get('wsdl.remote_path')
        wsdl_warning = main.config.get('wsdl.service_wsdl_warning_filename')
        wsdl_filename = main.config.get('wsdl.service_wsdl')
        wsdl_url = wsdl_remote_path.format(wsdl_filename)
        wsdl_error = main.config.get('wsdl.service_wsdl_error_filename')
        wsdl_warning_url = wsdl_remote_path.format(wsdl_warning)
        log_checker = auditchecker.AuditChecker(ssh_host, ssh_user, ssh_pass)

        test_adding_wsdl_validator_not_set = wsdl_validator_errors.test_adding_wsdl_validator_not_set(self=main,
                                                                                                      wsdl_url=wsdl_url,
                                                                                                      ss_host=ss_host,
                                                                                                      ss_user=ss_user,
                                                                                                      ss_pass=ss_pass,
                                                                                                      client_id=client_id,
                                                                                                      client_name=client_name,
                                                                                                      ssh_host=ssh_host,
                                                                                                      ssh_username=ssh_user,
                                                                                                      ssh_password=ssh_pass)
        test_refreshing_wsdl_validator_not_set = wsdl_validator_errors.test_refreshing_wsdl_validator_not_set(self=main,
                                                                                                              wsdl_url=wsdl_url,
                                                                                                              ss_host=ss_host,
                                                                                                              ss_user=ss_user,
                                                                                                              ss_pass=ss_pass,
                                                                                                              client_id=client_id,
                                                                                                              client_name=client_name)
        test_adding_wsdl_validator_invalid_command = wsdl_validator_errors.test_adding_wsdl_validator_invalid_command(
            self=main,
            wsdl_warning_url=wsdl_warning_url,
            ss_host=ss_host,
            ss_user=ss_user,
            ss_pass=ss_pass,
            client_id=client_id,
            client_name=client_name,
            log_checker=log_checker
            )
        test_refreshing_wsdl_validator_invalid_command = wsdl_validator_errors.test_refreshing_wsdl_validator_invalid_command(
            self=main,
            wsdl_url=wsdl_url,
            ss_host=ss_host,
            ss_user=ss_user,
            ss_pass=ss_pass,
            client_id=client_id,
            client_name=client_name,
            log_checker=log_checker
            )
        test_adding_wsdl_validator_not_executable = wsdl_validator_errors.test_adding_wsdl_validator_not_executable(
            self=main,
            wsdl_warning_url=wsdl_warning_url,
            ss_host=ss_host,
            ss_user=ss_user,
            ss_pass=ss_pass,
            client_id=client_id,
            client_name=client_name,
            log_checker=log_checker)
        test_refreshing_wsdl_validator_not_executable = wsdl_validator_errors.test_refreshing_wsdl_validator_not_executable(
            self=main,
            wsdl_url=wsdl_url,
            ss_host=ss_host,
            ss_user=ss_user,
            ss_pass=ss_pass,
            client_id=client_id,
            client_name=client_name,
            log_checker=log_checker)
        delete_service = configure_service.test_delete_service(main, client_name=client_name,
                                                               client_id=client_id,
                                                               wsdl_url=wsdl_url,
                                                               try_cancel=False)
        try:
            main.log('Copy wsdl with warning file to testservice wsdl')
            main.ssh_client = ssh_client.SSHClient(ssh_host, ssh_user, ssh_pass)
            webserver_set_wsdl(main, wsdl_source_filename=wsdl_local_path.format(wsdl_warning),
                               wsdl_target_filename=wsdl_local_path.format(wsdl_filename))
            remove_wsdl_validator_from_conf(main, ssh_host, ssh_user, ssh_pass, ss_host)

            main.log('SERVICE_08 6a. Adding wsdl when wsdl validator is not set')
            test_adding_wsdl_validator_not_set()

            main.log('Copy wsdl with error file to testservice wsdl')
            webserver_set_wsdl(main, wsdl_source_filename=wsdl_local_path.format(wsdl_error),
                               wsdl_target_filename=wsdl_local_path.format(wsdl_filename))

            main.log('SERVICE_14 3a. Refreshing wsdl, the location of the WSDL validator is not set.')
            test_refreshing_wsdl_validator_not_set()

            set_wsdl_validator_invalid_command(main, ssh_host, ssh_user, ssh_pass, ss_host)
            main.log('SERVICE_08 6d. The address of the WSDL validator program is incorrect and '
                     'system was not able to run the validation program.')

            test_adding_wsdl_validator_invalid_command()
            main.log('SERVICE_14 3d. The address of the WSDL validator program is incorrect and '
                     'system was not able to run the validation program.')
            test_refreshing_wsdl_validator_invalid_command()

            set_wsdl_validator_not_executable(main, ssh_host, ssh_user, ssh_pass, ss_host,
                                              not_exec_file_path)

            main.log('SERVICE_08 6e. The address of the WSDL validator refers to non-executable file and '
                     'system wsd not able to run the validation program')
            test_adding_wsdl_validator_not_executable()

            main.log('SERVICE_14 3e. The address of the WSDL validator refers to non-executable file and '
                     'system was not able to run the validation program.')
            test_refreshing_wsdl_validator_not_executable()
        except:
            main.log('Failed to test WSDL validator errors')
        finally:
            main.log('Reload page')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            main.log('Delete added service')
            try:
                delete_service()
            except:
                main.log('Failed to delete service')
            main.log('Restore local.ini')
            wsdl_validator_errors.restore_wsdl_validator(case=main, ssh_host=ssh_host, ssh_username=ssh_user,
                                                         ssh_password=ssh_pass, not_exec_file_path=not_exec_file_path)
            main.log('Wait until server responds before continuing with tests')
            wsdl_validator_errors.wait_until_server_up(ss_host)
            main.tearDown()
