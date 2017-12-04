import email

import time

from helpers.list_utils import flatten
from view_models.configuration_proxy import IDENTIFIERS


def test_generate_configuration_dir(self, cp_ssh_client, cs_ssh_client, instance_conf_dir, conf_dir, cs_identifier,
                                    hash_algorithm, cp_url):
    def generate_configuration_dir():
        metadata_file = '{}/conf-v2'.format(instance_conf_dir)
        self.log('Get configuration folder age in seconds')
        file_age = int(flatten(
            cp_ssh_client.exec_command('echo $(($(date +"%s")-$(date +"%s" -r {})))'.format(metadata_file)))[0])
        self.log('Configuration was updated {} seconds ago'.format(file_age))
        if file_age > 60:
            raise AssertionError('Configuration was last edited more than a minute ago')
        if file_age > 55:
            time_to_wait = 65 - file_age
            self.log('Waiting {} seconds for configuration update'.format(time_to_wait))
            time.sleep(time_to_wait)
        self.log('Getting metadata file content')
        conf_v2_content = flatten(cp_ssh_client.exec_command('cat {}'.format(metadata_file)))
        self.log('Parsing metadata')
        msg = email.message_from_string('\n'.join(conf_v2_content))
        self.log('Checking if content is multipart')
        self.is_true(msg.is_multipart())
        self.log('CP_16 4. System makes the configuration available to clients')
        self.log('Checking if cs configuration client got same metadata')
        cs_conf_client_output = flatten(cs_ssh_client.exec_command('curl -s {}'.format(cp_url)))
        self.is_equal(conf_v2_content, cs_conf_client_output)

        signature_found = False
        found_identifiers = 0
        found_digests = 0
        expire_date_found = False

        for part in msg.walk():
            self.log('-------------------')
            content_type = part.get_content_type()
            self.log('CP_16 1. Information about "content type" '
                     'present in configuration directory: {}'.format(content_type))
            self.is_not_none(content_type)
            if content_type == 'application/octet-stream':
                transfer_encoding = part.get('content-transfer-encoding')
                self.log('CP_16 1. Information about "content transfer encoding" '
                         'present in configuration directory: {}'.format(transfer_encoding))
                self.is_not_none(transfer_encoding, msg='Content transfer encoding not found')
                signature_algorithm_id = part.get('signature-algorithm-id')
                if signature_algorithm_id is not None:
                    signature_found = True
                    verification_certificate_hash = part.get('verification-certificate-hash')
                    self.is_not_none(verification_certificate_hash, msg='Vertification certificate hash not found')
                    self.log('CP_16 3. Information about "signature algorithm id" '
                             'present in configuration directory: {}'.format(signature_algorithm_id))
                    self.log('CP_16 3. Information about "verification certificate hash" '
                             'present in configuration directory: {}'.format(verification_certificate_hash))
            content_identifier = part.get('content-identifier')
            if content_identifier is not None:
                found_identifiers += 1
                parsed_content_identifier = content_identifier.split('; ')
                instance = parsed_content_identifier[1].split('=')[1].replace('"', '')
                identifier = parsed_content_identifier[0]
                hash_algorithm_id = part.get('hash-algorithm-id')
                content_location = part.get('content-location')

                self.log('Checking if identifier is valid')
                self.is_true(any(identifier == a for a in IDENTIFIERS), msg='Invalid identifier: {}'.format(identifier))
                self.log('CP_16 1. Information about "instance" '
                         'present in configuration directory: {}'.format(instance))
                self.is_equal(cs_identifier, instance, msg='Instance is not equal to {}'.format(cs_identifier))
                self.log('CP_16 1. Information about "identifier" '
                         'present in configuration directory: {}'.format(identifier))
                self.is_not_none(identifier, msg='Identifier not found')
                self.log('CP_16 1. Information about "hash algorithm id" '
                         'present in configuration directory: {}'.format(hash_algorithm_id))
                self.is_equal(hash_algorithm, hash_algorithm_id,
                              msg='Hash algorithm not equal to {}'.format(hash_algorithm))
                self.log('CP_16 1. Information about "content location" '
                         'present in configuration directory: {}'.format(content_location))
                self.is_not_none(content_location, msg='Content location not found')
                found_msg = 'found'
                file_location = '{}{}'.format(conf_dir, content_location)
                folder_path = flatten(cp_ssh_client.exec_command('[ -e {} ] && echo "{}"'
                                                                 .format(file_location, found_msg)))[0]
                self.is_equal(found_msg, folder_path,
                              msg='Could not find file in provided location {}'.format(file_location))
            if content_type == 'text/plain':
                expire_date = part.get('expire-date')
                self.log('CP_16 1. Information about "expire date" '
                         'present in configuration directory: {}'.format(expire_date))
                self.is_not_none(expire_date, msg='Expire date not found')
                expire_date_found = True
            if not any(a in content_type for a in ['multipart', 'text']):
                payload = part.get_payload()
                self.log('CP_16 1. Information about "digest" '
                         'present in configuration directory: {}'.format(payload))
                self.is_not_none(payload, msg='Digest not found')
                found_digests += 1

        self.is_true(expire_date_found, msg='Expire date found')
        self.is_true(signature_found, msg='No signature found')
        self.is_equal(len(IDENTIFIERS), found_identifiers, msg='Expected two identifiers, '
                                                               'got {}'.format(found_identifiers))
        self.is_equal(3, found_digests, msg='Expected three digests, got {}'.format(found_digests))

    return generate_configuration_dir
