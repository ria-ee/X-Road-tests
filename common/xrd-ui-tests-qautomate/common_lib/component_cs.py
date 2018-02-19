# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from common_lib import Common_lib
from pagemodel.cs_login import Cs_login
from pagemodel.open_application import Open_application
from pagemodel.cs_sidebar import Cs_sidebar
from common_lib_ssh import Common_lib_ssh

class Component_cs(CommonUtils):
    """
    Common components to central server

    Changelog:

    * 11.07.2017
        | Documentation updated
    """
    common_lib = Common_lib()
    cs_login = Cs_login()
    open_application = Open_application()
    cs_sidebar = Cs_sidebar()
    common_lib_ssh = Common_lib_ssh()

    def login(self, section=u'cs_url', initial_conf=False):
        """
        Login to central server

        *Updated: 11.07.2017*

        :param section:  Test data section name
        :param initial_conf:  If true server is in configurations state
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.open_application.Open_application.open_application_url`, *TESTDATA[section]*
                * **Step 2:** :func:`~pagemodel.cs_login.Cs_login.login_dev_cs`, *TESTDATA[section]*
                * **Step 3:** :func:`~pagemodel.cs_sidebar.Cs_sidebar.verify_central_server_title`
        """
        ## Login
        self.open_application.open_application_url(TESTDATA[section])
        self.cs_login.login_dev_cs(TESTDATA[section])
        if not initial_conf:
            self.cs_sidebar.verify_central_server_title()

    def open_central_server_url(self, section=u'cs_static_url'):
        """
        Open central server url

        *Updated: 11.07.2017*

        :param section:  Test data section name
        
        **Test steps:**
                * **Step 1:** :func:`~pagemodel.open_application.Open_application.open_application_url`, *TESTDATA[section]*
        """
        self.open_application.open_application_url(TESTDATA[section])

    def verify_configuratio_file(self, content):
        """
        """
        print content
        for x in content.split("\n"):
            if x.strip().startswith("Content-Type:") or x.strip().startswith("Content-type:") or x.strip().startswith("Verification-certificate-hash:"):
                print x