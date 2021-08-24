#!/usr/bin/env python3
##
# uq-globus-tools
# https://github.com/UQ-RCC/uq-globus-tools
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2021 The University of Queensland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
import argparse
import json
import logging
import os.path
import ssl
import sys
import time
from logging.handlers import SysLogHandler
from typing import Optional

from qriscloud import ldap3, QRIScloudLDAP

_EXPECTED_DATA_TYPE = 'identity_mapping_input#1.0.0'
_IDENTITIES_KEYS = {'status', 'username', 'identity_provider', 'organization', 'email', 'name', 'id'}

# https://docs.globus.org/globus-connect-server/v5.4/identity-mapping-guide/
_POSIX_GATEWAY_UUID = '145812c8-decc-41f1-83cf-bb2a85a2a70b'
_EMPTY_RESPOSNE = {'DATA_TYPE': 'identity_mapping_output#1.0.0', 'result': []}
_DEFAULT_CONFIG = {
    'ldap': {
        'servers': QRIScloudLDAP.DEFAULT_SERVERS,
        'bind_dn': '',
        'bind_pw': '',
        'verify_tls': True
    },
    'user_blacklist': ["root"],
    'debug': {
        'level': 'DEBUG',
        'dump_folder': '/tmp'
    }
}


def _validate_payload(payload) -> Optional[str]:
    if type(payload) is not dict:
        return 'payload not an object'
    payload: dict

    if 'DATA_TYPE' not in payload:
        return 'Missing #/DATA_TYPE key'

    dt = payload['DATA_TYPE']
    if dt != _EXPECTED_DATA_TYPE:
        return f'Unknown DATA_TYPE, got {dt}, expected \'{_EXPECTED_DATA_TYPE}\''

    if 'identities' not in payload:
        return 'Missing #/identities key'

    identities = payload['identities']
    if type(identities) is not list:
        return '#/identities is not an array'

    identities: list

    i = 0
    for ident in identities:
        if type(ident) is not dict:
            return f'#/identities/{i} is not an object'

        ident: dict
        if _IDENTITIES_KEYS.intersection(ident.keys()) != _IDENTITIES_KEYS:
            return f'#/identities/{i} is missing keys, expected {_IDENTITIES_KEYS}, got {ident.keys()}'

    return None


def _open_ldap(cfg) -> QRIScloudLDAP:
    ldapconfig = cfg.get('ldap', _DEFAULT_CONFIG['ldap'])
    if not ldapconfig['verify_tls']:
        tls = ldap3.Tls(validate=ssl.CERT_NONE)
    else:
        tls = None

    return QRIScloudLDAP(bind_dn=ldapconfig['bind_dn'], bind_pw=ldapconfig['bind_pw'], tls=tls,
                         servers=ldapconfig['servers'])


def main() -> int:
    config_path = os.getenv('GLOBUS_IDMAP_CONFIG_PATH', 'config.json')

    # Load our config
    with open(config_path, 'r') as f:
        cfg = json.load(f)

    debugconfig = cfg.get('debug', _DEFAULT_CONFIG['debug'])

    logging.root.setLevel(debugconfig['level'])

    logging.debug('Invoked with sys.argv:   %s', sys.argv)
    logging.debug('Configuration file path: %s', config_path)

    p = argparse.ArgumentParser(sys.argv[0])
    p.add_argument('-a', dest='all', action='store_true', help='all flag')
    p.add_argument('-c', dest='collection_gateway', help='Collection Gateway ID', required=True)
    # NB: This parameter isn't documented... We accept it, but I'm not sure what to do with it...
    p.add_argument('-s', dest='storage_gateway', help='Storage Gateway ID', required=False)

    args, unk_args = p.parse_known_args(sys.argv[1:])

    logging.debug('Arguments: %s', args)

    args.payload = json.load(sys.stdin)
    logging.debug('Payload  : %s', args.payload)

    if debugconfig['dump_folder'] is not None:
        args.payload['argv'] = sys.argv

        path = os.path.join(debugconfig['dump_folder'], f'globus-idmap-{int(time.time())}.json')
        try:
            with open(path, 'w') as f:
                json.dump(args.payload, f, indent=4)
        except OSError:
            logging.exception('Error writing payload to %s', path)

        del args.payload['argv']

    if args.collection_gateway != _POSIX_GATEWAY_UUID:
        logging.warning(f'Invoked with invalid gateway uuid {args.collection_gateway}, rejecting...')
        json.dump(_EMPTY_RESPOSNE, sys.stdout, indent=4)
        return 0

    errmsg = _validate_payload(args.payload)
    if errmsg is not None:
        logging.error(f'Invalid payload provided: {errmsg}')
        json.dump(_EMPTY_RESPOSNE, sys.stdout, indent=4)
        return 0

    with _open_ldap(cfg) as qc:
        idmap = {i['email']: i['id'] for i in args.payload['identities']}
        accts = qc.get_posix_accounts_by_email([i['email'] for i in args.payload['identities']])

        results = []
        for (eml, uid) in accts.items():
            logging.info(f'Mapped id/email {idmap[eml]}/{eml} to POSIX user {uid}')

            if uid in cfg['user_blacklist']:
                logging.warning('User %s in blacklist, skipping...', uid)
                continue

            results.append({'id': idmap[eml], 'output': uid})

    out = {
        'DATA_TYPE': 'identity_mapping_output#1.0.0',
        'result': results
    }

    logging.debug('Output payload: %s', json.dumps(out))
    json.dump(out, sys.stdout, indent=4)
    return 0


def climain() -> int:
    sh = SysLogHandler(address='/dev/log')
    sh.ident = '<uq-globus-idmap> '
    sh.setFormatter(logging.Formatter('%(levelname)-8s: %(message)s'))

    # Default to debug level, this is overridden anyway
    logging.root.setLevel(logging.DEBUG)

    logging.root.addHandler(sh)
    # Uncomment this to get logs to stderr as well
    # logging.root.addHandler(logging.StreamHandler(sys.stderr))

    try:
        return main()
    except Exception as e:
        logging.exception('Caught exception during processing...')
        # import traceback
        # traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
        json.dump(_EMPTY_RESPOSNE, sys.stdout, indent=4)
        return 0
