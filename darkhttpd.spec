Summary:	A secure, lightweight, fast, single-threaded HTTP/1.1 server
Name:		darkhttpd
Version:	1.11
Release:	1
License:	BSD
Group:		Networking/Daemons/HTTP
Source0:	http://unix4lyfe.org/darkhttpd/%{name}-%{version}.tar.bz2
# Source0-md5:	050e5a821b1fa71a82c6efba7fda1323
Source1:	%{name}.service
Source2:	%{name}.sysconfig
URL:		http://unix4lyfe.org/darkhttpd/
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	systemd-devel
Requires(post,preun,postun):	systemd-units >= 38
Requires:	/etc/mime.types
Requires:	systemd-units >= 0.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
darkhttpd is a secure, lightweight, fast and single-threaded HTTP/1.1
server.

Features:
- Simple to set up:
  - Single binary, no other files.
  - Standalone, doesn't need inetd or ucspi-tcp.
  - No messing around with config files.
- Written in C - efficient and portable.
- Small memory footprint.
- Event loop, single threaded - no fork() or pthreads.
- Generates directory listings.
- Supports HTTP GET and HEAD requests.
- Supports Range / partial content.
- Supports If-Modified-Since.
- Supports Keep-Alive connections.
- Can serve 301 redirects based on Host header.
- Uses sendfile().

Security:
- Can log accesses, including Referer and User-Agent.
- Can chroot.
- Can drop privileges.
- Impervious to /../ sniffing.
- Times out idle connections.
- Drops overly long requests.

Limitations:
- This server only serves static content - *NO* CGI supported!

%prep
%setup -q

%build
%{__cc} %{rpmcflags} %{rpmcppflags} darkhttpd.c -o %{name} %{rpmldflags}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/sysconfig,%{systemdunitdir}}

install -p %{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_reload

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%{systemdunitdir}/%{name}.service
