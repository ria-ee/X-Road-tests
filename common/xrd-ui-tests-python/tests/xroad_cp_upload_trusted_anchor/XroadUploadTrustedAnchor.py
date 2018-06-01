from __future__ import absolute_import

import unittest

from main.maincontroller import MainController
from view_models import sidebar as sidebar_constants, global_configuration
from selenium.webdriver.common.by import By
import glob
from helpers import ssh_client
from helpers.list_utils import flatten
from helpers.ssh_server_actions import exec_as_xroad
from view_models.configuration_proxy import ANCHOR_INSTANCE_IDENTIFIER, ANCHOR_HASH, ANCHOR_GENERATED_AT


class XroadUploadTrustedAnchor(unittest.TestCase):
    """
    UC CP_13: Upload Trusted Anchor
    RIA URL: https://jira.ria.ee/browse/XT-421, https://jira.ria.ee/browse/XTKB-202
    Depends on finishing other test(s): None
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_upload_trusted_anchor(self):
        main = MainController(self)

        '''Set test name and number'''
        main.test_number = 'CP_13'
        main.test_name = self.__class__.__name__

        main.log('TEST: UC CP_13: Upload Trusted Anchor')

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        cp_ssh_host = main.config.get('cp.ssh_host')
        cp_ssh_user = main.config.get('cp.ssh_user')
        cp_ssh_pass = main.config.get('cp.ssh_pass')
        cp_proxy_dir = main.config.get('cp.proxy_dir')

        months = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'June', '07': 'July',
                  '08': 'Aug', '09': 'Sept', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

        identifier = main.config.get('cs.identifier')
        sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)

        try:
            '''Open webdriver'''
            main.reload_webdriver(main.url, main.username, main.password)

            main.log('''Open Global Configuration tab''')
            main.wait_jquery()
            main.wait_until_visible(type=By.CSS_SELECTOR, element=sidebar_constants.GLOBAL_CONFIGURATION_CSS).click()

            main.log('''Click on "DOWNLOAD" button''')
            main.wait_jquery()
            main.wait_until_visible(type=By.ID, element=global_configuration.ANCHOR_FILE_DOENLOAD_BTN_ID).click()

            main.log('''Get anchor generation time from central server''')
            anchor_utc = main.wait_until_visible(type=By.CLASS_NAME,
                                                 element=global_configuration.ANCHOR_GENERATED_UTC_CLASS)
            anchor_utc = anchor_utc.text
            main.log('''Anchor is generated: {0}'''.format(anchor_utc))

            main.log('''Get anchor hash from central server''')
            anchor_hash = main.wait_until_visible(type=By.CLASS_NAME,
                                                  element=global_configuration.ANCHOR_HASH_CLASS)
            anchor_hash = anchor_hash.text
            main.log('''Ancor hash is: {0}'''.format(anchor_hash))

            main.log('''Change anchor generation time format for file path''')
            anchor_utc_for_file_path = anchor_utc.replace(' ', '_').replace(':', '_')
            main.log('''Time format for file path is: {0}'''.format(anchor_utc_for_file_path))

            main.log('''Change anchor generation time format for verification''')
            anchor_utc_for_verification = anchor_utc.split('-')
            anchor_utc_for_verification[1] = months[anchor_utc_for_verification[1]]
            anchor_utc_for_verification = '-'.join(anchor_utc_for_verification)
            main.log('''Time format for verification is: {0}'''.format(anchor_utc_for_verification))

            downloaded_file_path = glob.glob(main.get_download_path(global_configuration.ANCHOR_FILE_NAME.
                                                                    format(identifier, anchor_utc_for_file_path)))[0]
            main.log('''Downloaded file path is : {0}'''.format(downloaded_file_path))

            upload_file_path = main.config.get('cp.anchor_path')
            main.log('''File path for upload is : {0}'''.format(upload_file_path))

            main.log('CP_13/1 CP administrator copies the anchor file to configuration '
                     'proxy instance settings directory.')

            sshclient.exec_command('sudo chmod -R 777 {0}'.format(cp_proxy_dir), sudo=True)

            sshclient = ssh_client.SSHClient(cp_ssh_host, cp_ssh_user, cp_ssh_pass)
            sftp = sshclient.get_client().open_sftp()
            sftp.put(downloaded_file_path, upload_file_path)
            sftp.close()

            main.log('Verify instance identifier')
            std_out = flatten(exec_as_xroad(sshclient, 'confproxy-view-conf -p cp-test | grep {0}'.format(identifier)))
            main.is_equal(ANCHOR_INSTANCE_IDENTIFIER.format(identifier), std_out[0])
            main.log(std_out[0])

            # main.log('Verify generation time')
            # std_out = flatten(exec_as_xroad(sshclient, 'confproxy-view-conf -p cp-test | grep \'{0}\''
            #                                 .format(anchor_utc_for_verification)))
            # main.is_equal(ANCHOR_GENERATED_AT.format(anchor_utc_for_verification), std_out[0])
            # main.log(std_out[0])

            main.log('Verify hash')
            std_out = flatten(exec_as_xroad(sshclient, 'confproxy-view-conf -p cp-test | grep {0}'.format(anchor_hash)))
            main.is_equal(ANCHOR_HASH.format(anchor_hash), std_out[0])
            main.log(std_out[0])

        except:
            main.log('XroadUploadTrustedAnchor: Failed to upload trusted anchor')
            main.save_exception_data()
            assert False
        finally:
            '''Test teardown'''
            main.tearDown()
