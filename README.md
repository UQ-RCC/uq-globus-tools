# uq-globus-tools

## Build Instructions

### NixOS

```
$ nix-shell --pure --command 'make rpm'
```

The RPM will be placed in `rpmbuild/RPMS/noarch`.

## License
This project is licensed under the [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0):

Copyright &copy; 2021 [The University of Queensland](http://uq.edu.au/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

### 3rd-party Licenses


| Project | License | License URL |
| ------- | ------- | ----------- |
| [pyasn1](https://github.com/etingof/pyasn1)| BSD-2-Clause License | https://raw.githubusercontent.com/etingof/pyasn1/master/LICENSE.rst |
| [ldap3](https://github.com/cannatag/ldap3) | LGPLv3 | https://raw.githubusercontent.com/cannatag/ldap3/dev/LICENSE.txt |
