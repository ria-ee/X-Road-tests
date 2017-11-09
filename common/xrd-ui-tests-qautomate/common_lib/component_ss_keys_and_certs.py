# -*- coding: utf-8 -*-
from variables import errors
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.ss_keys_and_cert_dlg_registration_req import Ss_keys_and_cert_dlg_registration_req
from pagemodel.ss_keys_and_cert import Ss_keys_and_cert
from pagemodel.ss_keys_and_cert_dlg_import_cert import Ss_keys_and_cert_dlg_import_cert
from pagemodel.ss_keys_and_cert_generate_csr import Ss_keys_and_cert_generate_csr
from pagemodel.ss_keys_cert_dlg_generate_key import Ss_keys_cert_dlg_generate_key
from pagemodel.ss_keys_and_cert_dlg_subject_dname import Ss_keys_and_cert_dlg_subject_dname
from pagemodel.ss_enter_pin_dlg import Ss_enter_pin_dlg
from pagemodel.ss_keys_and_cert_dlg_delete import Ss_keys_and_cert_dlg_delete
from pagemodel.ss_softoken_enter_pin import Ss_softoken_enter_pin
from pagemodel.ss_keys_and_cert_details import Ss_keys_and_cert_details

class Component_ss_keys_and_certs(CommonUtils):
    """
    Components common to security server keys and certificate view

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    ss_keys_and_cert_dlg_registration_req = Ss_keys_and_cert_dlg_registration_req()
    ss_keys_and_cert = Ss_keys_and_cert()
    ss_keys_and_cert_dlg_import_cert = Ss_keys_and_cert_dlg_import_cert()
    ss_keys_and_cert_generate_csr = Ss_keys_and_cert_generate_csr()
    ss_keys_cert_dlg_generate_key = Ss_keys_cert_dlg_generate_key()
    ss_keys_and_cert_dlg_subject_dname = Ss_keys_and_cert_dlg_subject_dname()
    ss_enter_pin_dlg = Ss_enter_pin_dlg()
    ss_keys_and_cert_dlg_delete = Ss_keys_and_cert_dlg_delete()
    ss_softoken_enter_pin = Ss_softoken_enter_pin()
    ss_keys_and_cert_details = Ss_keys_and_cert_details()

    def generate_and_select_certificate_key_in_ss(self, text=u'ta_generated_key_sign'):
        """
        Generate and select certificate key in security server

        *Updated: 11.07.2017*
        
        :param text:  String value for text
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.verify_keys_and_cert_title`
                * **Step 2:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_soft_token`
                * **Step 3:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_generate_key`
                * **Step 4:** :func:`~pagemodel.ss_keys_cert_dlg_generate_key.Ss_keys_cert_dlg_generate_key.generate_key_label`, *text*
                * **Step 5:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.wait_until_cert_req_active`
                * **Step 6:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_generated_key_request`, *text*
        """
        self.ss_keys_and_cert.verify_keys_and_cert_title()
        self.ss_keys_and_cert.click_soft_token()
        self.ss_keys_and_cert.click_generate_key()
        self.ss_keys_cert_dlg_generate_key.generate_key_label(text)
        self.ss_keys_and_cert.wait_until_cert_req_active()
        self.ss_keys_and_cert.click_generated_key_request(text)
        sleep(2)

    def generate_sign_certificate_request_in_ss(self, section=u'member1_configuration'):
        """
        Generate signing certificate request in security server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_generate_certificate_request`
                * **Step 2:** :func:`~pagemodel.ss_keys_and_cert_generate_csr.Ss_keys_and_cert_generate_csr.fill_input_values_keys_csr_sign`, *TESTDATA[section]*
                * **Step 3:** :func:`~pagemodel.ss_keys_and_cert_generate_csr.Ss_keys_and_cert_generate_csr.click_button_id_generate_csr_submit`
                * **Step 4:** :func:`~pagemodel.ss_keys_and_cert_dlg_subject_dname.Ss_keys_and_cert_dlg_subject_dname.fill_input_values_keys_dname_sign`, *TESTDATA[section]*
                * **Step 5:** :func:`~pagemodel.ss_keys_and_cert_dlg_subject_dname.Ss_keys_and_cert_dlg_subject_dname.submit_keys_dname`
        """
        self.ss_keys_and_cert.click_generate_certificate_request()
        self.ss_keys_and_cert_generate_csr.fill_input_values_keys_csr_sign(TESTDATA[section])
        self.ss_keys_and_cert_generate_csr.click_button_id_generate_csr_submit()
        self.ss_keys_and_cert_dlg_subject_dname.fill_input_values_keys_dname_sign(TESTDATA[section])
        self.ss_keys_and_cert_dlg_subject_dname.submit_keys_dname()

    def generate_auth_certificate_request_in_ss(self, section=u'member1_configuration'):
        """
        Generate authentication certificate request in security server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_generate_certificate_request`
                * **Step 2:** :func:`~pagemodel.ss_keys_and_cert_generate_csr.Ss_keys_and_cert_generate_csr.fill_input_values_keys_csr_auth`
                * **Step 3:** :func:`~pagemodel.ss_keys_and_cert_generate_csr.Ss_keys_and_cert_generate_csr.click_button_id_generate_csr_submit`
                * **Step 4:** :func:`~pagemodel.ss_keys_and_cert_dlg_subject_dname.Ss_keys_and_cert_dlg_subject_dname.fill_input_values_keys_dname_auth`, *TESTDATA[section]*
                * **Step 5:** :func:`~pagemodel.ss_keys_and_cert_dlg_subject_dname.Ss_keys_and_cert_dlg_subject_dname.submit_keys_dname`
        """
        self.ss_keys_and_cert.click_generate_certificate_request()
        self.ss_keys_and_cert_generate_csr.fill_input_values_keys_csr_auth()
        self.ss_keys_and_cert_generate_csr.click_button_id_generate_csr_submit()
        self.ss_keys_and_cert_dlg_subject_dname.fill_input_values_keys_dname_auth(TESTDATA[section])
        self.ss_keys_and_cert_dlg_subject_dname.submit_keys_dname()

    def import_and_upload_key_certificate(self, value_string=None):
        """
        Import and upload key certification

        *Updated: 11.07.2017*

        :param value_string:  String value
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_import_cert`
                * **Step 2:** :func:`~pagemodel.ss_keys_and_cert_dlg_import_cert.Ss_keys_and_cert_dlg_import_cert.verify_title_file_dlg`
                * **Step 3:** :func:`~pagemodel.ss_keys_and_cert_dlg_import_cert.Ss_keys_and_cert_dlg_import_cert.click_browse_upload_button`
                * **Step 5:** :func:`~pagemodel.ss_keys_and_cert_dlg_import_cert.Ss_keys_and_cert_dlg_import_cert.file_upload_ok`
        """
        self.ss_keys_and_cert.click_import_cert()
        self.ss_keys_and_cert_dlg_import_cert.verify_title_file_dlg()
        self.ss_keys_and_cert_dlg_import_cert.click_browse_upload_button()
        self.make_cert_file_upload(value_string)
        sleep(7)
        self.ss_keys_and_cert_dlg_import_cert.file_upload_ok()
        sleep(7)

    def register_auth_certificate_in_ss(self, value_string=None, section=u'member1_configuration'):
        """
        Register authentication certification in security server

        *Updated: 11.07.2017*
        '

        :param value_string:  String value
        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.register_auth_cert`, *value_string*
                * **Step 2:** :func:`~pagemodel.ss_keys_and_cert_dlg_registration_req.Ss_keys_and_cert_dlg_registration_req.input_text_to_server_address`, *TESTDATA[section]*
                * **Step 3:** :func:`~pagemodel.ss_keys_and_cert_dlg_registration_req.Ss_keys_and_cert_dlg_registration_req.submit_register_request`
        """
        # step Send register request #Webpage: ss_keys_and_cert
        self.ss_keys_and_cert.register_auth_cert(value_string)
        self.ss_keys_and_cert_dlg_registration_req.input_text_to_server_address(TESTDATA[section])
        self.ss_keys_and_cert_dlg_registration_req.submit_register_request()

    def active_token_and_insert_pin_code_if_needed(self, section=u'cs_url'):
        """
        Activate token and inster pin code if needed

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_softoken_enter_pin.Ss_softoken_enter_pin.click_button_activate_token_enter_pin`
                * **Step 2:** :func:`~pagemodel.ss_enter_pin_dlg.Ss_enter_pin_dlg.input_text_to_id_activate_token_pin`, *TESTDATA[section]*
                * **Step 3:** :func:`~pagemodel.ss_enter_pin_dlg.Ss_enter_pin_dlg.click_button_ok`
                * **Step 4:** :func:`~pagemodel.ss_softoken_enter_pin.Ss_softoken_enter_pin.wait_until_softoken_pin_query_is_not_visible`
        """
        # Sometimes it will not ask pin code, recovery added
        try:
            self.ss_softoken_enter_pin.click_button_activate_token_enter_pin()
            self.ss_enter_pin_dlg.input_text_to_id_activate_token_pin(TESTDATA[section])
            self.ss_enter_pin_dlg.click_button_ok()
        except:
            print("Pin code query not prompted this time")
        self.ss_softoken_enter_pin.wait_until_softoken_pin_query_is_not_visible()

    def make_cert_file_upload(self, parameters="sign"):
        """
        Upload certification file

        *Updated: 11.07.2017*

        :param parameters:  Test data section dictionary
        
        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib.Common_lib.type_file_name_pyautogui`, *str(type_string*
        """
        sleep(6)
        path = os.getcwd() + "/scripts/" + parameters + "-cert_automation.der"
        print(path)
        type_string = path
        self.common_lib.type_file_name_pyautogui(str(type_string))
        print("done upload")
        sleep(2)

    def verify_key_and_sign_certificate_sign(self, section=u'paths'):
        """
        Verify key and sign certificate sign

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib.Common_lib.copy_and_sign_cert_request`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.fail(errors.Fail(errors.could_not_verify_certificate)`, *errors.could_not_verify_certificate*
        """
        if self.common_lib.verify_cert_request(TESTDATA[section]):
            print("cert sign ok")
            self.common_lib.copy_and_sign_cert_request(TESTDATA[section])
        else:
            self.fail(errors.could_not_verify_certificate)

    def verify_key_and_sign_certificate_auth(self, section=u'paths'):
        """
        Verify key and sign certificate authentication

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~common_lib.common_lib.Common_lib.copy_and_auth_cert_request`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.fail(errors.Fail(errors.could_not_verify_certificate)`, *errors.could_not_verify_certificate*
        """
        if self.common_lib.verify_cert_request(TESTDATA[section]):
            print("cert auth ok")
            self.common_lib.copy_and_auth_cert_request(TESTDATA[section])
        else:
            self.fail(errors.could_not_verify_certificate)

    def verify_key_request(self, section=u'paths'):
        """
        Verify key request

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.fail(errors.Fail(errors.could_not_verify_certificate)`, *errors.could_not_verify_certificate*
        """
        if self.common_lib.verify_cert_request(TESTDATA[section]):
            print("cert ok")
        else:
            self.fail(errors.could_not_verify_certificate)

    def verify_uploaded_certificate(self, value_string=None):
        """
        Verify uploaded certificate

        *Updated: 11.07.2017*
        :param value_string:  String value
        """
        cert_number = self.common_lib.read_cert_number_request(value_string)
        cert_key = self.ss_keys_and_cert.find_texts_from_table_keys(cert_number)
        return cert_number, cert_key

    def delete_key_by_label(self, text=u'ta_generated_key_sign'):
        """
        Open details dialog and delete certificate by key label

        *Updated: 11.07.2017*

        :param text:  String value for text
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_generated_key_request_to_signed_label`, *text*
                * **Step 2:** :func:`~pagemodel.ss_keys_and_cert.Ss_keys_and_cert.click_delete_cert`
                * **Step 3:** :func:`~pagemodel.ss_keys_and_cert_dlg_delete.Ss_keys_and_cert_dlg_delete.click_delete_cert_confirm`, *text*
        """
        self.ss_keys_and_cert.click_generated_key_request_to_signed_label(text)
        self.ss_keys_and_cert.click_delete_cert()
        self.ss_keys_and_cert_dlg_delete.click_delete_cert_confirm(text)

    def verify_details_dlg(self):
        """
        Verify detail dialogs hash value

        *Updated: 11.07.2017*

        **Test steps:**
                * **Step 2:** :func:`~pagemodel.ss_keys_and_cert_details.Ss_keys_and_cert_details.verify_hash`
        """
        self.wait_until_jquery_ajax_loaded()
        self.ss_keys_and_cert_details.verify_hash()
