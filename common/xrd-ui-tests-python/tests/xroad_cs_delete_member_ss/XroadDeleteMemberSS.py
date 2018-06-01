import time
import unittest

from selenium.webdriver.common.by import By

from helpers import xroad, ssh_client
from helpers.auditchecker import AuditChecker
from helpers.ssh_server_actions import refresh_ocsp
from main.maincontroller import MainController
from tests.xroad_configure_service_222.wsdl_validator_errors import wait_until_server_up
from tests.xroad_cs_delete_member.deleting_in_cs import test_add_security_server_to_member
from tests.xroad_cs_delete_member_ss.delete_member_ss import delete_member_ss
from tests.xroad_ss_client_certification_213.client_certification import register_cert, activate_disabled_cert
from view_models.keys_and_certificates_table import DELETE_BTN_ID, GLOBAL_ERROR_CERTIFICATE_ROW_XPATH
from view_models.popups import confirm_dialog_click
from view_models.sidebar import KEYSANDCERTIFICATES_BTN_CSS


class XroadDeleteMemberSS(unittest.TestCase):
    def test_delete_member_ss(self):
        """
        MEMBER_25 Delete a Security Server
        RIA URL: https://jira.ria.ee/browse/XT-377, https://jira.ria.ee/browse/XTKB-133
        Depends on finishing other test(s):
        Requires helper scenarios: client_certification
        X-Road version: 6.16.0
        :return:
        """
        main = MainController(self, empty_downloads=False)
        main.test_number = 'UC MEMBER_25'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        ss1_server_name = main.config.get('ss1.server_name')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        ca_ssh_host = main.config.get('ca.ssh_host')
        ca_ssh_user = main.config.get('ca.ssh_user')
        ca_ssh_pass = main.config.get('ca.ssh_pass')

        client_id = main.config.get('ss1.server_id')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = main.config.get('ss1.management_name')
        client['server_name'] = main.config.get('ss1.server_name')
        cert_path = 'temp.pem'
        ca_name = main.config.get('ca.name')

        delete_ss = delete_member_ss(main,
                                     server_name=ss1_server_name,
                                     log_checker=AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass),
                                     try_cancel=True)
        test_register_cert = register_cert(main, ss_ssh_host, ss_ssh_user, ss_ssh_pass,
                                           cs_host=cs_ssh_host, client=client,
                                           ca_ssh_host=ca_ssh_host, ca_ssh_user=ca_ssh_user,
                                           ca_ssh_pass=ca_ssh_pass,
                                           cert_path=cert_path, ca_name=ca_name, dns=ss_ssh_host,
                                           organization=client['name'])
        test_add_ss_to_cs_member = test_add_security_server_to_member(main, cs_host, cs_user,
                                                                      cs_pass,
                                                                      cs_ssh_host, cs_ssh_user,
                                                                      cs_ssh_pass,
                                                                      client, cert_path=cert_path
                                                                      )
        test_activate_cert = activate_disabled_cert(main, ss_ssh_host, ss_ssh_user, ss_ssh_pass,
                                                                      registered=True)
        ss_ssh_client = ssh_client.SSHClient(ss_ssh_host, ss_ssh_user, ss_ssh_pass)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            delete_ss()
        finally:
            try:
                main.log('Restoring security server')
                main.log('Waiting until servers synced')
                time.sleep(120)
                main.log('Refresh security server ocsp and cert statuses')
                refresh_ocsp(ss_ssh_client)
                main.log('Wait until server is up again')
                wait_until_server_up(ss_host)
                main.log('Open security server page')
                main.reload_webdriver(ss_host, ss_user, ss_pass)
                main.log('Open keys and certificates tab')
                main.wait_until_visible(type=By.CSS_SELECTOR, element=KEYSANDCERTIFICATES_BTN_CSS).click()
                main.log('Clicking on certificate with global error status')
                try:
                    main.click(element=main.wait_until_visible(type=By.XPATH, element=GLOBAL_ERROR_CERTIFICATE_ROW_XPATH))
                except:
                    main.driver.refresh()
                    main.click(element=main.wait_until_visible(type=By.XPATH, element=GLOBAL_ERROR_CERTIFICATE_ROW_XPATH))
                main.log('Deleting certificate with global error')
                main.by_id(DELETE_BTN_ID).click()
                main.log('Confirming certificate deletion')
                confirm_dialog_click(main)
                main.wait_jquery()
                test_register_cert()
                test_activate_cert()
                test_add_ss_to_cs_member()
            except:
                main.save_exception_data()
                raise
            finally:
                main.tearDown()
