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
