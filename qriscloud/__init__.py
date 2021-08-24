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

import io
import logging
import ssl
from typing import Optional, List, Iterable, Dict

from ._vendor import ldap3


class QRIScloudLDAP(object):
    DEFAULT_SERVERS = ['ldaps://idm1.qriscloud.org.au:636', 'ldaps://idm2.qriscloud.org.au:636']
    USER_SEARCH_BASE = 'ou=users,ou=universal,dc=qriscloud,dc=org,dc=au'

    def __init__(self, bind_dn: str, bind_pw: str, servers: List[str] = None, tls: ldap3.Tls = None, logger: logging.Logger = None):
        if not servers or len(servers) == 0:
            servers = QRIScloudLDAP.DEFAULT_SERVERS

        if not tls:
            tls = ldap3.Tls(validate=ssl.CERT_REQUIRED)

        if logger is None:
            logger = logging.getLogger(__name__)

        self._logger = logger

        conn = None
        ex = None
        for i in servers:
            try:
                conn = ldap3.Connection(ldap3.Server(i, tls=tls), user=bind_dn, password=bind_pw, auto_bind=True)
                break
            except ldap3.core.exceptions.LDAPException as e:
                self._logger.error(e)
                ex = e
                conn = None

        if not conn:
            raise ex

        self._conn = conn

    def __enter__(self):
        self._conn.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._conn.__exit__(exc_type, exc_val, exc_tb)

    @staticmethod
    def _build_email_filter(emails: Iterable[str]) -> str:
        filter = io.StringIO()
        filter.write('(&(objectClass=inetOrgPerson)(objectClass=posixAccount)(|')
        for email in emails:
            filter.write('(mail=')
            filter.write(ldap3.utils.conv.escape_filter_chars(email))
            filter.write(')')
        filter.write('))')
        return filter.getvalue()

    def get_posix_accounts_by_email(self, emails: Iterable[str]) -> Dict[str, str]:
        r = self._conn.search(
            search_base=QRIScloudLDAP.USER_SEARCH_BASE,
            search_filter=QRIScloudLDAP._build_email_filter(emails),
            search_scope=ldap3.LEVEL,
            attributes=['uid', 'mail']
        )
        if not r:
            return {}

        return {u.mail.value: u.uid.value for u in self._conn.entries}

    # Use this sparingly, it's much more efficient to use the batched version
    def get_posix_account_by_email(self, email: str) -> Optional[str]:
        return self.get_posix_accounts_by_email([email]).get(email, None)
