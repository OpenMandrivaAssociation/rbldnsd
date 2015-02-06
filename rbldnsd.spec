Summary:	Small, fast daemon to serve DNSBLs
Name:		rbldnsd
Version:	0.996b
Release:	4
License:	GPLv2+
Group:		System/Servers
URL:		http://www.corpit.ru/mjt/rbldnsd.html
Source0:	http://www.corpit.ru/mjt/rbldnsd/rbldnsd_%{version}.tar.gz
Source1:	rbldnsd.init
Patch0:		rbldnsd-0.996b-format_not_a_string_literal_and_no_format_arguments.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	gawk
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Rbldnsd is a small, authoritative-only DNS nameserver designed to serve
DNS-based blocklists (DNSBLs). It may handle IP-based and name-based
blocklists.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

sed -i	-e 's@/var/lib/rbldns\([/ ]\)@/var/lib/rbldnsd\1@g' \
    -e 's@\(-r/[a-z/]*\) -b@\1 -q -b@g' debian/rbldnsd.default

%build
%serverbuild

# this is not an autotools-generated configure script, and does not support --libdir
CFLAGS="$CFLAGS" ./configure

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}/var/lib/rbldnsd

install -m0755 rbldnsd %{buildroot}%{_sbindir}
install -m0644 rbldnsd.8 %{buildroot}%{_mandir}/man8
install -m0644 debian/rbldnsd.default %{buildroot}%{_sysconfdir}/sysconfig/rbldnsd
install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/rbldnsd

%pre
%_pre_useradd rbldns /var/lib/rbldnsd /sbin/nologin

%post
%_post_service rbldnsd

%preun
%_preun_service rbldnsd

%postun
%_postun_userdel rbldns

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root,-)
%doc README.user NEWS TODO debian/changelog CHANGES-0.81
%{_initrddir}/rbldnsd
%config(noreplace) %{_sysconfdir}/sysconfig/rbldnsd
%{_sbindir}/rbldnsd
%{_mandir}/man8/rbldnsd.8*
%dir /var/lib/rbldnsd


%changelog
* Mon Oct 05 2009 Oden Eriksson <oeriksson@mandriva.com> 0.996b-3mdv2010.0
+ Revision: 454032
- P0: fix format string errors
- rebuild

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild

* Sun Sep 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.996b-1mdv2009.0
+ Revision: 282185
- 0.996b

* Fri Aug 01 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.996a-4mdv2009.0
+ Revision: 260093
- rebuild

* Fri Jul 25 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.996a-3mdv2009.0
+ Revision: 247968
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Nov 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.996a-1mdv2008.1
+ Revision: 108681
- import rbldnsd


* Wed Nov 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.996a-1mdv2008.1
- initial Mandriva package (fc8 import)

* Thu Aug 23 2007 Paul Howarth <paul@city-fan.org> 0.996a-4
- add buildreq gawk

* Thu Aug 23 2007 Paul Howarth <paul@city-fan.org> 0.996a-3
- upstream released a new version without changing the version number (the
  only changes are in debian/control and debian/changelog, neither of which
  are used in the RPM package)
- unexpand tabs in spec
- use the standard scriptlet for user/group creation in %%pre
- drop scriptlet dependencies on /sbin/service by calling initscript directly
- clarify license as GPL version 2 or later

* Wed Aug 30 2006 Paul Howarth <paul@city-fan.org> 0.996a-2
- FE6 mass rebuild

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 0.996a-1
- update to 0.996a

* Tue Feb 21 2006 Paul Howarth <paul@city-fan.org> 0.996-1
- update to 0.996
- use /usr/sbin/useradd instead of %%{_sbindir}/useradd
- add buildreq zlib-devel to support gzipped zone files

* Wed Feb 15 2006 Paul Howarth <paul@city-fan.org> 0.995-5
- license text not included in upstream tarball, so don't include it

* Tue Jun 28 2005 Paul Howarth <paul@city-fan.org> 0.995-4
- include gpl.txt as %%doc

* Mon Jun 27 2005 Paul Howarth <paul@city-fan.org> 0.995-3
- fix /etc/sysconfig/rbldnsd references to /var/lib/rbldns to point to
  %%{_localstatedir}/lib/rbldnsd instead
- don't enable daemons in any runlevel by default
- add -q option to sample entries in /etc/sysconfig/rbldnsd

* Fri Jun 17 2005 Paul Howarth <paul@city-fan.org> 0.995-2
- first Fedora Extras build, largely based on upstream spec file
