import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_cs_delete_member import deleting_in_cs
from tests.xroad_logging_in_cs_2111.logging_in_cs import USERNAME


class XroadCsDeleteMemberWithSS(unittest.TestCase):
    """
    MEMBER_26 4a Delete member with owned security server
    RIA URL: https://jira.ria.ee/browse/XTKB-41
    Depends on finishing other test(s): MEMBER_14
    Requires helper scenarios:
    X-Road version: 6.16.0
    """
    def test_xroad_cs_delete_member_with_security_server(self):
        main = MainController(self)
        main.test_number = 'UC MEMBER_26 4a'
        main.test_name = self.__class__.__name__

        main.url = main.config.get('cs.host')
        main.username = main.config.get('cs.user')
        main.password = main.config.get('cs.pass')

        cs_host = main.config.get('cs.host')
        cs_username = main.config.get('cs.user')
        cs_password = main.config.get('cs.pass')

        cs_ssh_host = main.config.get('cs.ssh_host')
        cs_ssh_user = main.config.get('cs.ssh_user')
        cs_ssh_pass = main.config.get('cs.ssh_pass')

        client_id = main.config.get('ss2.client2_id')
        client_name = main.config.get('ss2.client2_name')
        client = xroad.split_xroad_subsystem(client_id)
        client['name'] = client_name

        user = {USERNAME: cs_username}

        test_deleting_member_with_security_server = deleting_in_cs.test_deleting_member_with_security_server(
            main,
            cs_ssh_host=cs_ssh_host,
            cs_ssh_user=cs_ssh_user,
            cs_ssh_pass=cs_ssh_pass,
            client=client,
            user=user)
        try:
            main.reload_webdriver(url=cs_host, username=cs_username, password=cs_password)
            test_deleting_member_with_security_server()
        except:
            main.save_exception_data()
            assert False
        finally:
            main.tearDown()
