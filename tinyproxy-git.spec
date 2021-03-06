# spec file for tinyproxy built from github
#
#   https://github.com/tinyproxy/tinyproxy
#
# created from tinyproxy-1.8.3-2.el7.src.rpm which provided Source{1..4}
#
# use 'rpmbuild --undefine=_disable_source_fetch -bs tinyproxy.spec'
# to create a new srpm after updating the commit id

#%global commit c651664720d1fc21aeb36ca8dbb625a874af1d97
%global commit 78959fe5b22344f520fa5d5f47a240e7314d6fcb
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%define tinyproxy_confdir %{_sysconfdir}/tinyproxy
%define tinyproxy_datadir %{_datadir}/tinyproxy
%define tinyproxy_rundir  %{_localstatedir}/run/tinyproxy
%define tinyproxy_logdir  %{_localstatedir}/log/tinyproxy
%define tinyproxy_docdir  %{_docdir}/tinyproxy-%{version}
%define tinyproxy_user    tinyproxy
%define tinyproxy_group   tinyproxy

Name:           tinyproxy
Version:        1.9.0
Release:        1.%(date +%%Y%%m%%d)git%{shortcommit}%{?dist}
Summary:        A small, efficient HTTP/SSL proxy daemon

Group:          System Environment/Daemons
License:        GPLv2+
URL:            https://www.banu.com/tinyproxy/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#Source0:        https://github.com/%{name}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source0:        https://github.com/allesmetkaas/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.conf
Source3:        %{name}.logrotate
Source4:        %{name}.tmpfiles

Requires(post):     systemd
Requires(preun):    systemd
Requires(preun):    systemd
BuildRequires:      asciidoc automake

%description
tinyproxy is a small, efficient HTTP/SSL proxy daemon that is very useful in a
small network setting, where a larger proxy like Squid would either be too
resource intensive, or a security risk.  

%prep
%setup -q -n %{name}-%{commit}


%build
./autogen.sh
%configure --docdir=%{tinyproxy_docdir} \
    --enable-reverse \
    --enable-transparent 

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
sed -i 's/\/sbin\//\/bin\//' %{SOURCE1}
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system/%{name}.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{tinyproxy_confdir}/%{name}.conf
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/run/%{name}
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/log/%{name}

%clean
rm -rf %{buildroot}


%pre
if [ $1 == 1 ]; then
    %{_sbindir}/useradd -c "tinyproxy user" -s /bin/false -r -d %{tinyproxy_rundir} %{tinyproxy_user} 2>/dev/null || :
fi


%post
if [ $1 == 1 ]; then
    /bin/systemctl enable %{name}.service
fi
    

%preun
if [ $1 = 0 ]; then
    /bin/systemctl stop %{name}.service
    /bin/systemctl disable %{name}.service
fi  
    

%postun
if [ $1 == 2 ]; then
    /bin/systemctl condrestart %{name}.service > /dev/null 2>&1 || :
fi  
 


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS docs/*.txt
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man5/%{name}.conf.5.gz
%{_prefix}/lib/systemd/system/%{name}.service
%{_sysconfdir}/tmpfiles.d/%{name}.conf
%{tinyproxy_datadir}/*.html
%dir %{tinyproxy_datadir}
%dir %{tinyproxy_confdir}
%config(noreplace) %{tinyproxy_confdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,%{tinyproxy_user},%{tinyproxy_group}) %dir %{tinyproxy_rundir}
%attr(-,%{tinyproxy_user},%{tinyproxy_group}) %dir %{tinyproxy_logdir}

%changelog
* Wed Sep 12 2018 Chris Hockey <allesmetkaas@users.noreply.github.com> - 1.9.0-78959f
- Updated to git commit 78959fe5b22344f520fa5d5f47a240e7314d6fcb

* Tue Sep 11 2018 Chris Hockey <allesmetkaas@users.noreply.github.com> - 1.9.0-2aa1d3
- Forked tinyproxy to fix upstream password datatype

* Fri Aug 31 2018 Chris Hockey <allesmetkaas@users.noreply.github.com> - 1.9.0-c65166
- Updated to git commit c651664720d1fc21aeb36ca8dbb625a874af1d97

* Wed Jul 29 2015 Arnaud Begot <arnaud.begot@worldline.com> - 1.8.3-2
- initial version for rhel/CentOS 7

* Mon Sep 09 2013 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.8.3-1
- update to upstream 1.8.3

* Sat Jun 05 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.8.2-1
- update to upstream 1.8.2

* Tue Apr 06 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.8.1-1
- update to upstream 1.8.1

* Wed Feb 17 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.8.0-1
- update to upstream 1.8.0
- add logrotate configuration

* Sun Oct 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.5-1
- update to upstream 1.6.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.4-3
- add --enable-transparent-proxy option (#466808)

* Sun Aug 24 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.4-2
- update to upstream 1.6.4 final

* Sun Jun 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.4-1
- update to upstream candidate 1.6.4

* Wed Apr 16 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.3-2
- fix spec review issues
- fix initscript

* Sun Mar 09 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.6.3-1
- Initial rpm configuration
