SERVICES_TABLE_ID = 'central_services'
SERVICES_TABLE_ROWS_XPATH = '//table[@id="central_services"]//tbody/tr'

SERVICE_ADD_BUTTON_ID = 'central_service_add'
SERVICE_EDIT_BUTTON_ID = 'central_service_details'
SERVICE_DELETE_BUTTON_ID = 'central_service_delete'
SERVICE_EDIT_DIALOG_CLEAR_BUTTON_ID = 'central_service_details_clear_search'


NEW_CENTRAL_SERVICE_DATA = [['CS_CODE', 'Test member 2', 'VERSION', 'Test member 2', '00000002', 'COM', 'Central monitoring client', False,
                            None, None, False],
                            ['   CS_CODE   ', '   TS1OWNER   ', '   VERSION   ', '   TS1   ', '   TS1OWNER   ', 'GOV',
                             '   Management Services   ', False, None, None, True],

                            [256 * 'C', 'CODE', 'VERSION', 'P_NAME', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                            "Parameter '{0}' input exceeds 255 characters", 'serviceCode', False],
                            ['CS_CODE', 256 * 'C', 'VERSION', 'P_NAME', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                            "Parameter '{0}' input exceeds 255 characters", 'targetServiceCode', False],
                            ['CS_CODE', 'CODE', 256 * 'V', 'P_NAME', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                            "Parameter '{0}' input exceeds 255 characters", 'targetServiceVersion', False],
                            ['CS_CODE', 'CODE', 'VERSION', 256 * 'P', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                            "Parameter '{0}' input exceeds 255 characters", 'targetProviderName', False],
                            ['CS_CODE', 'CODE', 'VERSION', 'P_NAME', 256 * 'P', 'GOV', 'SUBSYSTEM', True,
                            "Parameter '{0}' input exceeds 255 characters", 'targetProviderCode', False],
                            ['CS_CODE', 'CODE', 'VERSION', 'P_NAME', 'P_CODE', 'GOV', 256 * 'S', True,
                            "Parameter '{0}' input exceeds 255 characters", 'targetProviderSubsystem', False],

                            ['CS_CODE', 'CODE', 'VERSION', 'P_NAME', 'P_CODE', '', 'SUBSYSTEM', True,
                             'Missing parameter: {0}', 'targetProviderClass', False],
                            ['CS_CODE', 'CODE', 'VERSION', 'P_NAME', '', 'GOV', 'SUBSYSTEM', True,
                             'Missing parameter: {0}', 'targetProviderCode', False],
                            ['CS_CODE', 'CODE', 'VERSION', '', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                             'Missing parameter: {0}', 'targetProviderName', False],
                            ['CS_CODE', '', 'VERSION', 'P_NAME', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                             'Missing parameter: {0}', 'targetServiceCode', False],
                            ]

EDIT_CENTRAL_SERVICE_DATA = [['CS_CODE', 'TS1OWNER', 'VERSION', 'TS1', 'TS1OWNER', 'GOV', 'Management Services', False,
                              None, None, False],
                             ['   CS_CODE   ', '   TS1OWNER   ', '   VERSION   ', '   TS1   ', '   TS1OWNER   ', 'GOV',
                             '   Management Services   ', False, None, None, True],

                             ['CS_CODE', 256 * 'C', 'VERSION', 'P_NAME', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                              "Parameter '{0}' input exceeds 255 characters", 'targetServiceCode', False],
                             ['CS_CODE', 'CODE', 256 * 'V', 'P_NAME', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                              "Parameter '{0}' input exceeds 255 characters", 'targetServiceVersion', False],
                             ['CS_CODE', 'CODE', 'VERSION', 256 * 'P', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                              "Parameter '{0}' input exceeds 255 characters", 'targetProviderName', False],
                             ['CS_CODE', 'CODE', 'VERSION', 'P_NAME', 256 * 'P', 'GOV', 'SUBSYSTEM', True,
                              "Parameter '{0}' input exceeds 255 characters", 'targetProviderCode', False],
                             ['CS_CODE', 'CODE', 'VERSION', 'P_NAME', 'P_CODE', 'GOV', 256 * 'S', True,
                              "Parameter '{0}' input exceeds 255 characters", 'targetProviderSubsystem', False],

                             ['CS_CODE', 'CODE', 'VERSION', 'P_NAME', 'P_CODE', '', 'SUBSYSTEM', True,
                             'Missing parameter: {0}', 'targetProviderClass', False],
                             ['CS_CODE', 'CODE', 'VERSION', 'P_NAME', '', 'GOV', 'SUBSYSTEM', True,
                             'Missing parameter: {0}', 'targetProviderCode', False],
                             ['CS_CODE', 'CODE', 'VERSION', '', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                             'Missing parameter: {0}', 'targetProviderName', False],
                             ['CS_CODE', '', 'VERSION', 'P_NAME', 'P_CODE', 'GOV', 'SUBSYSTEM', True,
                             'Missing parameter: {0}', 'targetServiceCode', False],
                             ]

CENTRAL_SERVICE = ['CS_CODE', 'TS1OWNER', 'VERSION', 'TS1', 'TS1OWNER', 'GOV', 'Management Services']


def get_central_service_text(text):
    return "//table[@id='central_services']//td[text()='{0}']".format(text)
