Summary:	Small, fast daemon to serve DNSBLs
Name:		rbldnsd
Version:	0.996b
Release:	%mkrel 2
License:	GPLv2+
Group:		System/Servers
URL:		http://www.corpit.ru/mjt/rbldnsd.html
Source0:	http://www.corpit.ru/mjt/rbldnsd/rbldnsd_%{version}.tar.gz
Source1:	rbldnsd.init
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
