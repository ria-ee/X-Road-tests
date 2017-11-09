# -*- coding: utf-8 -*-
import os
from variables import strings
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_all_parameters
from time import sleep
from common_lib import Common_lib
from pagemodel.cs_backup_restore_dlg_restore_confirm import Cs_backup_restore_dlg_restore_confirm
from pagemodel.cs_backup_restore_dlg_delete_confirm import Cs_backup_restore_dlg_delete_confirm
from pagemodel.cs_backup_restore import Cs_backup_restore
from pagemodel.cs_backup_restore_dlg_back_up_config import Cs_backup_restore_dlg_back_up_config
from pagemodel.cs_backup_restore_dlg_upload_backup import Cs_backup_restore_dlg_upload_backup
from common_lib_ssh import Common_lib_ssh
from component_common import Component_common
from pagemodel.cs_backup_restore_dlg_up_back_conf_exist import Cs_backup_restore_dlg_up_back_conf_exist

class Component_cs_backup(CommonUtils):
    """
    Components common to central server backup view

    Changelog:
    * 19.10.2017
        | Backup generation case methods updated and new ones added
    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    cs_backup_restore_dlg_restore_confirm = Cs_backup_restore_dlg_restore_confirm()
    cs_backup_restore_dlg_delete_confirm = Cs_backup_restore_dlg_delete_confirm()
    cs_backup_restore = Cs_backup_restore()
    cs_backup_restore_dlg_back_up_config = Cs_backup_restore_dlg_back_up_config()
    cs_backup_restore_dlg_upload_backup = Cs_backup_restore_dlg_upload_backup()
    common_lib_ssh = Common_lib_ssh()
    component_common = Component_common()
    cs_backup_restore_dlg_up_back_conf_exist = Cs_backup_restore_dlg_up_back_conf_exist()

    def generate_backup(self):
        """
        Generate backup in central server

        **Test steps:**
            * **Step 1: generate backup file**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_button_id_backup`
            * **Step 2: verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.backup_created*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *strings.generate_backup_audit_log*
            * **Step 3: close backup dialog**
                * :func:`~pagemodel.cs_backup_restore_dlg_back_up_config.Cs_backup_restore_dlg_back_up_config.click_button_ok`
        """
        # Step generate backup file
        self.cs_backup_restore.click_button_id_backup()

        # Step Verify message and logs
        self.component_common.verify_notice_message(strings.backup_created)
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.generate_backup_audit_log)

        # Step Close backup dialog
        self.cs_backup_restore_dlg_back_up_config.click_button_ok()

    def generate_invalid_backup(self):
        """
        Generate invalid backup in central server

        **Test steps:**
            * **Step 1: generate backup file**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.change_file_permission`, *u'cs_url'*, *strings.devices_file*, *u'4'*
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_button_id_backup`
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.change_file_permission`, *u'cs_url'*, *strings.devices_file*, *u'771'*
            * **Step 2: verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.backup_created_error.format(u'1'*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *strings.failed_generate_backup_audit_log*
            * **Step 3: close backup dialog**
                * :func:`~pagemodel.cs_backup_restore_dlg_back_up_config.Cs_backup_restore_dlg_back_up_config.click_button_ok`
        """
        # Step generate backup file
        self.common_lib_ssh.change_file_permission(u'cs_url', strings.devices_file, u'4')
        self.cs_backup_restore.click_button_id_backup()
        self.common_lib_ssh.change_file_permission(u'cs_url', strings.devices_file, u'771')

        # Step Verify message and logs
        self.component_common.verify_notice_message(strings.backup_created_error.format(u'1'))
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.failed_generate_backup_audit_log)

        # Step Close backup dialog
        self.cs_backup_restore_dlg_back_up_config.click_button_ok()

    def restore_backup(self):
        """
        Restore backup in central server

        **Test steps:**
            * **Step 1: restore newest backup file**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_newest_restore`
                * :func:`~pagemodel.cs_backup_restore_dlg_restore_confirm.Cs_backup_restore_dlg_restore_confirm.click_button_ui_buttonset_confirm`
            * **Step 2: verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.backup_restored.format(backup_file*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *strings.restore_configuration_audit_log*
                * :func:`~pagemodel.cs_backup_restore_dlg_back_up_config.Cs_backup_restore_dlg_back_up_config.click_button_ok`
        """
        # Step Restore newest backup file
        self.cs_backup_restore.click_element_newest_restore()
        self.cs_backup_restore_dlg_restore_confirm.click_button_ui_buttonset_confirm()

        # Step Verify message and logs
        backup_file = TESTDATA.get_parameter(u'paths', u'backup_file')
        self.component_common.verify_notice_message(strings.backup_restored.format(backup_file))
        self.common_lib_ssh.verify_audit_log(u'cs_url', strings.restore_configuration_audit_log)

        self.cs_backup_restore_dlg_back_up_config.click_button_ok()

    def download_backup(self):
        """
        Download back up in central server

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_newest_download`
        """
        self.cs_backup_restore.click_element_newest_download()

    def delete_backup(self):
        """
        Delete back up in central server

        **Test steps:**
            * **Step 1: delete newest backup**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_newest_delete`
                * :func:`~pagemodel.cs_backup_restore_dlg_delete_confirm.Cs_backup_restore_dlg_delete_confirm.click_button_ui_buttonset_confirm`
            * **Step 2: verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.backup_deleted*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *event=strings.delete_backup_audit_log*
        """
        # Step delete newest backup
        self.cs_backup_restore.click_element_newest_delete()
        self.cs_backup_restore_dlg_delete_confirm.click_button_ui_buttonset_confirm()

        # Step Verify message and logs
        self.component_common.verify_notice_message(strings.backup_deleted)
        self.common_lib_ssh.verify_audit_log(u'cs_url', event=strings.delete_backup_audit_log)

    def cancel_delete_backup(self):
        """
        Delete back up in central server

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_newest_delete`
                * **Step 2:** :func:`~pagemodel.cs_backup_restore_dlg_delete_confirm.Cs_backup_restore_dlg_delete_confirm.click_button_cancel`
        """
        self.cs_backup_restore.click_element_newest_delete()
        self.cs_backup_restore_dlg_delete_confirm.click_button_cancel()

    def upload_backup(self):
        """
        Upload back up in central server

        **Test steps:**
            * **Step 1: upload backup file**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_upload_backup_file`
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_element_upload_button`
                * :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *backup_file_path*
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_dialog_confirm`
            * **Step 2: verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.backup_file_uploaded*
        """
        # Step upload backup file
        self.cs_backup_restore.click_element_upload_backup_file()
        self.cs_backup_restore_dlg_upload_backup.click_element_upload_button()

        download_folder = TESTDATA.get_parameter(u'paths', u'downloads_folder')
        backup_file = TESTDATA.get_parameter(u'paths', u'backup_file')
        backup_file_path = os.path.join(download_folder, backup_file)
        self.common_lib.type_file_name_pyautogui(backup_file_path)
        self.cs_backup_restore_dlg_upload_backup.click_dialog_confirm()

        # Step Verify message and logs
        self.component_common.verify_notice_message(strings.backup_file_uploaded)
        # TODO Autologin audit log is activated same time sometimes
        #self.common_lib_ssh.verify_audit_log(u'cs_url', event=strings.upload_backup_audit_log)

        self.wait_until_jquery_ajax_loaded()

    def upload_backup_already_exists(self):
        """
        Upload backup file that already exist

        **Test steps:**
            * **Step 1: upload backup file**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_upload_backup_file`
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_element_upload_button`
                * :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *backup_file_path*
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_dialog_confirm`
            * **Step 2: confirm already exist dialog**
                * :func:`~pagemodel.cs_backup_restore_dlg_up_back_conf_exist.Cs_backup_restore_dlg_up_back_conf_exist.click_button_confirm`
            * **Step 3: verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.backup_file_uploaded*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *event=strings.upload_backup_audit_log*
        """
        # Step upload backup file
        self.cs_backup_restore.click_element_upload_backup_file()
        self.cs_backup_restore_dlg_upload_backup.click_element_upload_button()

        download_folder = TESTDATA.get_parameter(u'paths', u'downloads_folder')
        backup_file = TESTDATA.get_parameter(u'paths', u'backup_file')
        backup_file_path = os.path.join(download_folder, backup_file)
        self.common_lib.type_file_name_pyautogui(backup_file_path)
        self.cs_backup_restore_dlg_upload_backup.click_dialog_confirm()

        # Step Confirm already exist dialog
        self.cs_backup_restore_dlg_up_back_conf_exist.click_button_confirm()

        # Step Verify message and logs
        self.component_common.verify_notice_message(strings.backup_file_uploaded)
        self.common_lib_ssh.verify_audit_log(u'cs_url', event=strings.upload_backup_audit_log)

        self.wait_until_jquery_ajax_loaded()

    def upload_backup_invalid_char(self):
        """
        Upload backup file that contains invalid characters

        **Test steps:**
            * **Step 1: upload backup file**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_upload_backup_file`
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_element_upload_button`
                * :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *invalid_file_path*
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_dialog_confirm`
            * **Step 2: verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.backup_file_upload_invalid_char.format(invalid_file*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *event=strings.upload_backup_failed_audit_log*
            * **Step 3: cancel upload dialog**
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_button_cancel`
        """
        # Step upload backup file
        self.cs_backup_restore.click_element_upload_backup_file()
        self.cs_backup_restore_dlg_upload_backup.click_element_upload_button()

        download_folder = TESTDATA.get_parameter(u'paths', u'downloads_folder')
        backup_file = TESTDATA.get_parameter(u'paths', u'backup_file')
        invalid_file = "(A-Z), (a-z), (0-9), (_), (.), (-).tar"

        backup_file_path = os.path.join(download_folder, backup_file)
        invalid_file_path = os.path.join(download_folder, invalid_file)
        os.rename(backup_file_path, invalid_file_path)

        self.common_lib.type_file_name_pyautogui(invalid_file_path)
        self.cs_backup_restore_dlg_upload_backup.click_dialog_confirm()

        # Step Verify message and logs
        self.component_common.verify_notice_message(strings.backup_file_upload_invalid_char.format(invalid_file))
        self.common_lib_ssh.verify_audit_log(u'cs_url', event=strings.upload_backup_failed_audit_log)

        os.rename(invalid_file_path, backup_file_path)

        # Step Cancel upload dialog
        self.cs_backup_restore_dlg_upload_backup.click_button_cancel()

    def upload_backup_invalid_extension(self):
        """
        Upload backup file that contains invalid extension

        **Test steps:**
            * **Step 1: upload backup file**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_upload_backup_file`
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_element_upload_button`
                * :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *invalid_file_path*
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_dialog_confirm`
            * **Step 2: verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.backup_file_uploaded_invalid_extension.format(invalid_file*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *event=strings.upload_backup_failed_audit_log*
            * **Step 3: cancel upload dialog**
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_button_cancel`
        """
        # Step upload backup file
        self.cs_backup_restore.click_element_upload_backup_file()
        self.cs_backup_restore_dlg_upload_backup.click_element_upload_button()

        download_folder = TESTDATA.get_parameter(u'paths', u'downloads_folder')
        backup_file = TESTDATA.get_parameter(u'paths', u'backup_file')
        invalid_file = backup_file[:len(".tar")] + ".txt"

        backup_file_path = os.path.join(download_folder, backup_file)
        invalid_file_path = os.path.join(download_folder, invalid_file)
        os.rename(backup_file_path, invalid_file_path)

        self.common_lib.type_file_name_pyautogui(invalid_file_path)
        self.cs_backup_restore_dlg_upload_backup.click_dialog_confirm()

        # Step Verify message and logs
        self.component_common.verify_notice_message(strings.backup_file_uploaded_invalid_extension.format(invalid_file))
        self.common_lib_ssh.verify_audit_log(u'cs_url', event=strings.upload_backup_failed_audit_log)

        os.rename(invalid_file_path, backup_file_path)

        # Step Cancel upload dialog
        self.cs_backup_restore_dlg_upload_backup.click_button_cancel()

    def upload_backup_invalid_format(self):
        """
        Upload backup file that contains invalid format

        **Test steps:**
            * **Step 1: upload backup file**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_upload_backup_file`
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_element_upload_button`
                * :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *backup_file_path*
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_dialog_confirm`
            * **Step 2: verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.backup_file_uploaded_invalid_format*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *event=strings.upload_backup_failed_audit_log*
            * **Step 3: cancel upload dialog**
                * :func:`~pagemodel.cs_backup_restore_dlg_upload_backup.Cs_backup_restore_dlg_upload_backup.click_button_cancel`
        """
        # Step upload backup file
        self.cs_backup_restore.click_element_upload_backup_file()
        self.cs_backup_restore_dlg_upload_backup.click_element_upload_button()

        download_folder = TESTDATA.get_parameter(u'paths', u'downloads_folder')
        backup_file = TESTDATA.get_parameter(u'paths', u'backup_file')
        backup_file_path = os.path.join(download_folder, "invalid_" + backup_file)
        open(backup_file_path, 'w+')

        self.common_lib.type_file_name_pyautogui(backup_file_path)
        self.cs_backup_restore_dlg_upload_backup.click_dialog_confirm()

        # Step Verify message and logs
        self.component_common.verify_notice_message(strings.backup_file_uploaded_invalid_format)
        self.common_lib_ssh.verify_audit_log(u'cs_url', event=strings.upload_backup_failed_audit_log)

        os.remove(backup_file_path)

        # Step Cancel upload dialog
        self.cs_backup_restore_dlg_upload_backup.click_button_cancel()

    def cancel_restore_backup(self):
        """
        Cancel backup restoration in

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_newest_restore`
                * **Step 2:** :func:`~pagemodel.cs_backup_restore_dlg_restore_confirm.Cs_backup_restore_dlg_restore_confirm.click_button_cancel`
        """
        self.cs_backup_restore.click_element_newest_restore()
        self.cs_backup_restore_dlg_restore_confirm.click_button_cancel()

    def restore_invalid_backup(self):
        """
        **Test steps:**
            * **Step 1: generate empty backup file to server**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.generate_empty_file`, *u'cs_url'*, *strings.invalid_backup_file*
            * **Step 2: restore newest backup**
                * :func:`~pagemodel.cs_backup_restore.Cs_backup_restore.click_element_newest_restore`
                * :func:`~pagemodel.cs_backup_restore_dlg_restore_confirm.Cs_backup_restore_dlg_restore_confirm.click_button_ui_buttonset_confirm`
            * **Step 3:s verify message and logs**
                * :func:`~common_lib.component_common.Component_common.verify_notice_message`, *strings.restore_failed.format(strings.invalid_backup_file_name*
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.verify_audit_log`, *u'cs_url'*, *event=strings.restore_backup_failed_audit_log*
            * **Step 4: delete backups from server**
                * :func:`~common_lib.common_lib_ssh.Common_lib_ssh.delete_files_from_directory`, *u'cs_url'*, *strings.backup_directory*
        """
        # Step generate empty backup file to server
        self.common_lib_ssh.generate_empty_file(u'cs_url', strings.invalid_backup_file)
        self.reload_page()

        # Step Restore newest backup
        self.cs_backup_restore.click_element_newest_restore()
        self.cs_backup_restore_dlg_restore_confirm.click_button_ui_buttonset_confirm()

        # Steps Verify message and logs
        self.component_common.verify_notice_message(strings.restore_failed.format(strings.invalid_backup_file_name))
        self.common_lib_ssh.verify_audit_log(u'cs_url', event=strings.restore_backup_failed_audit_log)

        # Step Delete backups from server
        self.common_lib_ssh.delete_files_from_directory(u'cs_url', strings.backup_directory)
        self.reload_page()
