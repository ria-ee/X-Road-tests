import os
from webframework.extension.parsers.parameter_parser import get_parameter, get_all_parameters, set_parameter_file

# audit log events
login_user = u'Log in user'
logout_user = u'Log out user'
login_user_failed = u'Log in user failed'

login_token = u'Log in to token'
logout_token = u'Log out from token'

add_timestamping_services = u'Add timestamping service'
add_timestamping_services_failed = u'Add timestamping service failed'

delete_timestamping_services = u'Delete timestamping service'
set_ui_language = u'Set UI language'

edit_cs_address = u'Edit central server address'
edit_cs_address_failed = u'Edit central server address failed'

recreate_internal_configuration_anchor = u'Re-create internal configuration anchor'
generate_internal_config_signing_key = u'Generate internal configuration signing key'
activate_internal_config_signing_key = u'Activate internal configuration signing key'
delete_internal_config_signing_key = u'Delete internal configuration signing key'

recreate_external_configuration_anchor = u'Re-create external configuration anchor'
generate_external_config_signing_key = u'Generate external configuration signing key'
activate_external_config_signing_key = u'Activate external configuration signing key'
delete_external_config_signing_key = u'Delete external configuration signing key'

restore_backup_failed_audit_log = u'Restore configuration failed'
restore_configuration_audit_log = u'Restore configuration'
delete_backup_audit_log = u'Delete backup file'
upload_backup_audit_log = u'Upload backup file'
upload_backup_failed_audit_log = u'Upload backup file failed'
generate_backup_audit_log = u'Back up configuration'
failed_generate_backup_audit_log = u'Back up configuration failed'

# Ui strings
authentication_failed = u'Authentication failed'
login_restore_in_progress = u'Restore in progress, try again later'
message_failed_to_add_timestamping = u'Failed to add timestamping service: timestamping service already exists'
request_cert_deletion = u'Certificate deletion'
request_client_deletion = u'Client deletion'
security_server_version = u'Security Server version 6'
reg_auth_cert_deletion = u'Authentication certificate deletion'

# Messages
key_success_deleted_from_cs = u'Key successfully deleted from central server configuration'
internal_conf_anchor_generated_success = u'Internal configuration anchor generated successfully'
token_key_removed = u'Key successfully deleted from token'
change_address_error = u'Central server address must be DNS name or IP address'
external_conf_anchor_generated_success = u'External configuration anchor generated successfully'
restore_failed = u"Failed to restore configuration: Restoring configuration from file '{}' failed."
backup_restored = u"Configuration restored successfully from file '{}'."
backup_deleted = u'Selected backup deleted successfully'
backup_created = u'Configuration backup created'
backup_created_error = u"Failed to back up configuration: Error making configuration backup, script exited with status code '{}'"
backup_file_uploaded = u'New backup file uploaded successfully'
backup_file_upload_invalid_char = u"Failed to upload new backup file: Filename '{}' contains invalid characters. Valid characters include: (A-Z), (a-z), (0-9), (_), (.), (-)."
backup_file_uploaded_invalid_extension = u"Failed to upload new backup file: Uploaded file name '{}' has an invalid extension, the only valid one is 'tar'"
backup_file_uploaded_invalid_format = u"Failed to upload new backup file: Content of uploaded file must be in tar format"

lanquage_eng = u'ENGLISH (EN)'

# enviroment information
ssh_type_environment = "ssh"
lxd_type_environment = "lxd"

# Key types
sign_key_usage = "Sign"
auth_key_usage = "Auth"

# Backup paths

# Log file names and paths
backup_directory = "/var/lib/xroad/backup"

invalid_backup_file_name = "invalid.tar"
invalid_backup_file = os.path.join(backup_directory, invalid_backup_file_name)

devices_file = "/etc/xroad/devices.ini"

audit_log = "/var/log/xroad/audit.log"
jetty_log = "/var/log/xroad/jetty/jetty.log"
signer_log = "/var/log/xroad/signer.log"
signer_console_log = "/var/log/xroad/signer-console.log"
configuration_client_log = "/var/log/xroad/configuration_client.log"
monitor_log = "/var/log/xroad/monitor.log"
proxy_log = "/var/log/xroad/proxy.log"
ss_all_logs = [jetty_log, audit_log, signer_log, signer_console_log, configuration_client_log, monitor_log, proxy_log]

# key names
sign_key_label = "ta_generated_key_sign"
auth_key_label = "ta_generated_key_auth"
sign_key_label_2 = "ta_generated_key_sign_b"
auth_key_label_2 = "ta_generated_key_auth_b"


def generate_subject_name(section=u'member1_configuration'):
    parameters = get_all_parameters()
    member_name = parameters[section][u'member_name']
    member_code = parameters[section][u'member_code']
    instance_identifier = parameters[section][u'instance_identifier']
    subject_name_string = u'C=FI, O={}, CN={}, serialNumber={}/'.format(member_name, member_code, instance_identifier)
    print(subject_name_string)
    return subject_name_string


def generate_member_id_short(parameters=None):
    instance_identifier = parameters[u'instance_identifier']
    member_class = parameters[u'member_class']
    member_code = parameters[u'member_code']
    member_id_short = u'{}:{}:{}:*'.format(instance_identifier, member_class, member_code)
    print(member_id_short)
    return member_id_short


def server_environment_type():
    return get_parameter(section=u'server_environment', name=u'type')


def server_environment_csr_format():
    return get_parameter(section=u'server_environment', name=u'csr_format')


def server_environment_approved_ca():
    return get_parameter(section=u'server_environment', name=u'approved_ca')


def server_request_comment(section=u'member1_configuration'):
        parameters = get_all_parameters()
        instance_identifier = parameters[section][u'instance_identifier']
        member_class = parameters[section][u'member_class']
        member_code = parameters[section][u'member_code']
        member_server = parameters[section][u'security_server_code']
        request_comment = u'\'SERVER:{}/{}/{}/{}\' deletion'.format(instance_identifier, member_class,
                                                                    member_code, member_server)
        return request_comment
