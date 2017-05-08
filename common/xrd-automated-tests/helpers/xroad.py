def split_xroad_id(xroad_id, type=None):
    '''
    Creates a dictionary {type, instance, class, code, subsystem} from an XRoad ID string.
    :param xroad_id: str - XRoad ID string
    :return: dict{type, instance, class, code, subsystem}
    '''
    xroad_id = xroad_id.replace(' : ', ':').split(':')

    subsystem = None
    service = None
    service_name = None
    service_version = None

    if len(xroad_id) > 3:
        subsystem = xroad_id[3]

    if len(xroad_id) > 4:
        service = xroad_id[4]
        split_service = service.split('.')
        service_name = split_service[0]
        if len(split_service) > 1:
            service_version = split_service[1]

    return {'type': type, 'instance': xroad_id[0], 'class': xroad_id[1], 'code': xroad_id[2],
            'subsystem': subsystem, 'service': service, 'service_name': service_name,
            'service_version': service_version}


def split_xroad_member(xroad_id, member_type='MEMBER'):
    return split_xroad_id(xroad_id=xroad_id, type=member_type)


def split_xroad_subsystem(xroad_id, member_type='SUBSYSTEM'):
    return split_xroad_id(xroad_id=xroad_id, type=member_type)


def get_xroad_id(xroad_data):
    '''
    Returns the XRoad ID string using an xroad data dict. Type (member/subsystem) is automatically detected from
    'subsystem' value - if it exists, return a subsystem; if not, return a member.
    :param xroad_data: dict - XRoad data from get_xroad_id()
    :return: str - XRoad ID string
    '''
    if xroad_data['subsystem'] is None or xroad_data['subsystem'] == '':
        return get_xroad_member(xroad_data)
    else:
        return get_xroad_subsystem(xroad_data)


def get_xroad_member(xroad_data, xroad_type='MEMBER'):
    '''
    Returns an XRoad ID member string using an xroad data dict.
    Example result: MEMBER : KS1 : GOV : TS2OWNER
    :param xroad_data: dict - XRoad data from get_xroad_id()
    :param xroad_type: str - subsystem type string, default=MEMBER
    :return: str - XRoad ID string
    '''
    return '{0} : {1} : {2} : {3}'.format(xroad_type, xroad_data['instance'], xroad_data['class'], xroad_data['code'])


def get_xroad_subsystem(xroad_data, xroad_type='SUBSYSTEM'):
    '''
    Returns an XRoad ID subsystem string using an xroad data dict.
    Example result: SUBSYSTEM : KS1 : COM : CLIENT1 : sub
    :param xroad_data: dict - XRoad data from get_xroad_id()
    :param xroad_type: str - subsystem type string, default=SUBSYSTEM
    :return: str - XRoad ID string
    '''
    return '{0} : {1} : {2} : {3} : {4}'.format(xroad_type, xroad_data['instance'], xroad_data['class'],
                                                xroad_data['code'],
                                                xroad_data['subsystem'])


def fill_upload_input(self, upload_button_element, local_path):
    '''
    Fills upload element input[type="file"] without using the file open dialog.
    :param self: MainController object
    :param upload_button_element: WebElement - "Upload" or "Browse" button (label[class="upload"])
    :param local_path: str - file path on local computer
    :return: None
    '''
    # Save element classes for restoring them later
    file_input_container_classes = upload_button_element.get_attribute('class')

    # Remove all classes from the container. This should make the file input visible.
    self.js('arguments[0].removeAttribute("class");', upload_button_element)

    # Find the file input inside the upload element
    file_input = upload_button_element.find_element_by_xpath('.//input[@type="file"]')

    # Send the path to the input. This should fill the field with a valid file path.
    file_input.send_keys(local_path)

    # Restore classes.
    self.js('arguments[0].setAttribute("class", arguments[1]);', upload_button_element, file_input_container_classes)
