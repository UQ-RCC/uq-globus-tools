%define _name uq-globus-tools
%define _prefix /opt/uq-globus-tools

Name:       %{_name}
Version:    1.0.0
Release:    2
Summary:    %{_name}
License:    Proprietary
# We use Globus' embedded python
Requires:   globus-connect-server54
Requires(post):   /usr/sbin/semodule
Requires(postun): /usr/sbin/semodule

BuildArch:  noarch

%description
UQ Globus Utilities. currently consisting of:
* QRIScloud Globus ID Mapper

%install
mkdir -p "$RPM_BUILD_ROOT/%{_prefix}"
mv * "$RPM_BUILD_ROOT/%{_prefix}"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, root, root, 0755)
%{_prefix}/lib/python/*
%attr(0755, root, root) "%{_prefix}/bin/*"
%attr(0640, gcsweb, gcsweb) %config(noreplace) "%{_prefix}/etc/config.json"
%{_datadir}/selinux/targeted/uq-globus-tools.pp

%post
/usr/sbin/semodule -s targeted -i %{_datadir}/selinux/targeted/uq-globus-tools.pp &> /dev/null || :
# Regenerate the bytecode
find %{_prefix}/lib/python -name __pycache__ -type d -print0 | xargs -0 rm -rf
/opt/globus/bin/python3 -m compileall %{_prefix}/lib/python &> /dev/null || :

%postun
if [ $1 -eq 0 ]; then
  /usr/sbin/semodule -s targeted -r uq-globus-tools &> /dev/null || :
  find %{_prefix}/lib/python -name __pycache__ -type d -print0 | xargs -0 rm -rf
fi
