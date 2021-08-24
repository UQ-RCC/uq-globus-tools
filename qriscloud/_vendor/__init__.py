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
import contextlib
import os
import sys
import importlib
from typing import Union, Iterator


# https://stackoverflow.com/a/64789046
@contextlib.contextmanager
def _add_sys_path(path: Union[str, os.PathLike]) -> Iterator[None]:
    """Temporarily add the given path to `sys.path`."""
    path = os.fspath(path)
    try:
        sys.path.insert(0, path)
        yield
    finally:
        sys.path.remove(path)


##
# Can't just import .ldap3 here, transitive dependencies need to be rewritten,
# so work around it.
##
_vendor_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
with _add_sys_path(_vendor_dir):
    # ldap3==2.9
    ldap3 = importlib.import_module('ldap3')
