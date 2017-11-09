# -*- coding: utf-8 -*-
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from time import sleep
from pagemodel.ss_version import Ss_version

class Component_component_cs_version(CommonUtils):
    ss_version = Ss_version()

    def verify_version(self, text=u'Central Server version 6'):
        """
        Verify version view contains right version

        *Updated: 11.07.2017*

        :param text:  String value for text

        **Test steps:**
                * **Step 1:** :func:`~pagemodel.ss_version.Ss_version.verify_version_text`, *text*
        """
        self.ss_version.verify_version_text(text)
        print("Version text contains '{}'".format(text))
