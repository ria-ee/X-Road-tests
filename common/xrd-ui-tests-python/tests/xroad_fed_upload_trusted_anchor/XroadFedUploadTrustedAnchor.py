import datetime
import unittest

from helpers import ssh_client, auditchecker
from main.maincontroller import MainController
from tests.xroad_fed_upload_trusted_anchor.upload_trusted_anchor import download_external_conf, test_upload_anchor, \
    set_validator_script_to, replace_in_file
from view_models.trusted_anchor import CONFIGURATION_DOWNLOAD_FAIL_STATUS, CONFIGURATION_EXPIRED_STATUS, \
    SIGNATURE_VALUE_FAILED_STATUS, INTERNAL_CONF_ERROR_STATUS, OTHER_ERROR_STATUS, SUCCESS_STATUS, \
    ANCHOR_VALIDATOR_SCRIPT, INSTANCE_IDENTIFIER


class XroadFedUploadTrustedAnchor(unittest.TestCase):
    """
    FED_02 Upload a Trusted Anchor
    RIA URL: https://jira.ria.ee/browse/XTKB-227
    Depends on finishing other test(s): MEMBER_01
    Requires helper scenarios: GCONF_02
    X-Road version: 6.16.0
    """

    def test_a_upload_trusted_anchor_same_instance_error(self):
        main = MainController(self)
        main.test_number = 'UC FED_02.a'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')
        upload_anchor = test_upload_anchor(main, same_instance=True)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            download_external_conf(main)
            upload_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()

    def test_b_upload_trusted_anchor_download_error(self):
        main = MainController(self, empty_downloads=False)
        main.test_number = 'UC FED_02.b'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_identifier = main.config.get('cs.identifier')
        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        new_identifier = INSTANCE_IDENTIFIER
        sshclient = ssh_client.SSHClient(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        upload_anchor = test_upload_anchor(main, log_checker=log_checker, download_error=True)

        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            main.log('Backup anchor validator')
            sshclient.exec_command('cp -p {0} {0}.backup'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            set_validator_script_to(sshclient, CONFIGURATION_DOWNLOAD_FAIL_STATUS)
            replace_in_file(main, cs_identifier, new_identifier)
            upload_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.log('Restore anchor validator')
            sshclient.exec_command('cp -p {0}.backup {0}'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            main.tearDown()

    def test_c_upload_trusted_anchor_expired_error(self):
        main = MainController(self, empty_downloads=False)
        main.test_number = 'UC FED_02.c'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        sshclient = ssh_client.SSHClient(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        upload_anchor = test_upload_anchor(main, log_checker=log_checker, expired=True)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            main.log('Backup anchor validator')
            sshclient.exec_command('cp -p {0} {0}.backup'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            set_validator_script_to(sshclient, CONFIGURATION_EXPIRED_STATUS)
            upload_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.log('Restore anchor validator')
            sshclient.exec_command('cp -p {0}.backup {0}'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            main.tearDown()

    def test_d_upload_trusted_anchor_signature_error(self):
        main = MainController(self, empty_downloads=False)
        main.test_number = 'UC FED_02.d'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        sshclient = ssh_client.SSHClient(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        upload_anchor = test_upload_anchor(main, log_checker=log_checker, invalid_signature=True)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            main.log('Backup anchor validator')
            sshclient.exec_command('cp -p {0} {0}.backup'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            set_validator_script_to(sshclient, SIGNATURE_VALUE_FAILED_STATUS)
            upload_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.log('Restore anchor validator')
            sshclient.exec_command('cp -p {0}.backup {0}'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            main.tearDown()

    def test_e_upload_trusted_anchor_internal_configuration_error(self):
        main = MainController(self, empty_downloads=False)
        main.test_number = 'UC FED_02.e'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        sshclient = ssh_client.SSHClient(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        upload_anchor = test_upload_anchor(main, log_checker=log_checker, internal=True)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            main.log('Backup anchor validator')
            sshclient.exec_command('cp -p {0} {0}.backup'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            set_validator_script_to(sshclient, INTERNAL_CONF_ERROR_STATUS)
            upload_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.log('Restore anchor validator')
            sshclient.exec_command('cp -p {0}.backup {0}'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            main.tearDown()

    def test_f_upload_trusted_anchor_other_error(self):
        main = MainController(self, empty_downloads=False)
        main.test_number = 'UC FED_02.f'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        sshclient = ssh_client.SSHClient(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        upload_anchor = test_upload_anchor(main, log_checker=log_checker, other_error=True)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            main.log('Backup anchor validator')
            sshclient.exec_command('cp -p {0} {0}.backup'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            set_validator_script_to(sshclient, OTHER_ERROR_STATUS)
            upload_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.log('Restore anchor validator')
            sshclient.exec_command('cp -p {0}.backup {0}'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            main.tearDown()

    def test_g_upload_trusted_anchor(self):
        main = MainController(self, empty_downloads=False)
        main.test_number = 'UC FED_02.g'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        sshclient = ssh_client.SSHClient(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        new_identifier = INSTANCE_IDENTIFIER
        upload_anchor = test_upload_anchor(main, log_checker=log_checker, new_identifier=new_identifier)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            main.log('Backup anchor validator')
            sshclient.exec_command('cp -p {0} {0}.backup'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            set_validator_script_to(sshclient, SUCCESS_STATUS)
            upload_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.log('Restore anchor validator')
            sshclient.exec_command('cp -p {0}.backup {0}'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            main.tearDown()

    def test_h_update_trusted_anchor(self):
        main = MainController(self, empty_downloads=False)
        main.test_number = 'UC FED_02.h'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        sshclient = ssh_client.SSHClient(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        upload_anchor = test_upload_anchor(main, log_checker=log_checker, generated_at_check=True)
        try:
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            main.log('Backup anchor validator')
            sshclient.exec_command('cp -p {0} {0}.backup'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            set_validator_script_to(sshclient, SUCCESS_STATUS)
            currentyr = datetime.datetime.now().year
            nextyr = currentyr + 1
            replace_in_file(main, str(currentyr), str(nextyr))
            upload_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.log('Restore anchor validator')
            sshclient.exec_command('cp -p {0}.backup {0}'.format(ANCHOR_VALIDATOR_SCRIPT), sudo=True)
            main.tearDown()

    def test_i_upload_trusted_anchor_not_valid_file(self):
        main = MainController(self, empty_downloads=False)
        main.test_number = 'UC FED_02.i'
        main.test_name = self.__class__.__name__

        cs_host = main.config.get('cs.host')
        cs_user = main.config.get('cs.user')
        cs_pass = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')
        log_checker = auditchecker.AuditChecker(cs_ssh_host, cs_ssh_user, cs_ssh_pass)
        upload_anchor = test_upload_anchor(main, log_checker=log_checker, invalid_file=True)
        try:
            replace_in_file(main, 'source', 'asd')
            main.reload_webdriver(cs_host, cs_user, cs_pass)
            upload_anchor()
        except:
            main.save_exception_data()
            raise
        finally:
            main.tearDown()
