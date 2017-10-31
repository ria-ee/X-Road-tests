SERTIFICATE_EMPTY = ('//table[@id="tsps"]//tr[@class="odd"]//td[@class="dataTables_empty"]')

SERTIFICATE_NAME = ('//table[@id="tsps"]//tr[@class="odd row_selected"]//td[1]')
SERTIFICATE_VALID_FROM = ('//table[@id="tsps"]//tr[@class="odd row_selected"]//td[2]')
SERTIFICATE_VALID_TO = ('//table[@id="tsps"]//tr[@class="odd row_selected"]//td[3]')
DATE_REGEX = '(\d{4}[-]?\d{1,2}[-]?\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})'
TEST_URL = 'http://www.asaquality.ee'
INVALID_URL = 'test.ee'
ADD_TEST_NAME = 'test_xroad_add_ts'
EDIT_TEST_NAME = 'test_xroad_edit_ts'