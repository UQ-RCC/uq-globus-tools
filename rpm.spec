%define _name uq-globus-tools
%define _prefix /opt/uq-globus-tools

Name:       %{_name}
Version:    1.0.0
Release:    1
Summary:    %{_name}
License:    Proprietary
Requires:   globus-connect-server54
BuildArch:  noarch

%description
UQ Globus Utilities. currently consisting of:
* QRIScloud Globus ID Mapper

%install
mkdir -p "$RPM_BUILD_ROOT/%{_prefix}"
mv * "$RPM_BUILD_ROOT/%{_prefix}"
find "$RPM_BUILD_ROOT/%{_prefix}" -name __pycache__ -type d -print0 | xargs -0 rm -rf
find "$RPM_BUILD_ROOT/%{_prefix}/lib" -type f -print0 | xargs -0 chmod 0644
find "$RPM_BUILD_ROOT/%{_prefix}/lib" -type d -print0 | xargs -0 chmod 0755

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}
%config(noreplace) "%{_prefix}/etc/config.json"
