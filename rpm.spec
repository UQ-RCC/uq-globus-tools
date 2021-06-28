%define _name uq-globus-tools
%define _prefix /opt/uq-globus-tools

Name:       %{_name}
Version:    1.0.0
Release:    1
Summary:    %{_name}
License:    Proprietary
# We use Globus' embedded python
Requires:   globus-connect-server54
#Requires:   python3
Requires(post): /usr/sbin/setsebool, /usr/sbin/selinuxenabled
BuildArch:  noarch

%description
UQ Globus Utilities. currently consisting of:
* QRIScloud Globus ID Mapper

%install
mkdir -p "$RPM_BUILD_ROOT/%{_prefix}"
mv * "$RPM_BUILD_ROOT/%{_prefix}"
find "$RPM_BUILD_ROOT/%{_prefix}" -name __pycache__ -type d -print0 | xargs -0 rm -rf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, root, root, 0755)
%{_prefix}
%attr(0755, root, root) "%{_prefix}/bin/*"
%attr(0640, gcsweb, gcsweb) %config(noreplace) "%{_prefix}/etc/config.json"

%post
# Allow Globus (via httpd) to talk to ldap
if /usr/sbin/selinuxenabled ; then
 /usr/sbin/setsebool -P authlogin_nsswitch_use_ldap 1 2>/dev/null
fi