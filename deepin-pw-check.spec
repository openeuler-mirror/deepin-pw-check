# Run tests in check section
# disable for bootstrapping
%bcond_with check
%global with_debug 1
%if 0%{?with_debug}
%global debug_package   %{nil}
%endif
Name:           deepin-pw-check
Version:        5.0.20.7
Release:        2
Summary:        Used to check password and manager the configuration for password.
License:        GPL-3.0
URL:            https://github.com/linuxdeepin/%{name}
Source0:        %{name}-%{version}.orig.tar.xz
Source1:        vendor.tar.gz
Source2:        dde.conf

BuildRequires:  golang
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  deepin-gettext-tools
BuildRequires:  cracklib-devel
BuildRequires:  iniparser

Patch0:	        fix-pwd-pam-update-error.patch
Patch1:         fix-deepin_pw_check.c-sprintf-error.patch

Requires:       polkit

%description
In order to unify the authentication interface,
this interface is designed to adapt to fingerprint, face and other authentication methods.

%package devel
Summary: Header files and libraries used to build deepin-pw-check
Requires: %{name} = %{version}-%{release}
Requires: cracklib-devel iniparser

%description devel
In order to unify the authentication interface,
this interface is designed to adapt to fingerprint, face and other authentication methods.

%prep
%setup -q
patch -p1 < rpm/0001-fix-for-UonioTech.patch
%patch0 -p1
%patch1 -p1

tar -xf %{SOURCE1}

%build
go env -w GO111MODULE=auto
BUILDID="0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
export GOPATH=%{_builddir}/%{name}-%{version}/vendor:$GOPATH
%make_build GO_BUILD_FLAGS=-trimpath GOBUILD="go build -compiler gc -ldflags \"-B $BUILDID\""

%post


%postun


%install
mkdir -p %{buildroot}/%{_sysconfdir}/deepin
export GOPATH=%{_datadir}/gocode
export PKG_FILE_DIR=%{_libdir}/pkgconfig
%make_install PKG_FILE_DIR=%{_libdir}/pkgconfig LIBDIR=lib64 PAM_MODULE_DIR=%{_libdir}/security GOBUILD="go build -compiler gc -ldflags \"-B $BUILDID\""
%find_lang deepin-pw-check

install -Dm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/deepin/dde.conf


%files -f deepin-pw-check.lang
%doc README.md
%license
%dir %{_sysconfdir}/deepin
%{_sysconfdir}/deepin/dde.conf
%{_bindir}/pwd-conf-update
%{_prefix}/lib/deepin-pw-check/deepin-pw-check
%{_libdir}/libdeepin_pw_check.so.*
%{_libdir}/security/pam_deepin_pw_check.so
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/polkit-1/actions/*.policy

%files devel
%{_libdir}/libdeepin_pw_check.a
%{_libdir}/libdeepin_pw_check.so
%{_libdir}/pkgconfig/libdeepin_pw_check.pc
%{_includedir}/deepin_pw_check.h

%changelog
* Tue Aug 02 2022 liweiganga <liweiganga@uniontech.com> - 5.0.20.7-2
- add dde.conf

* Fri Jul 22 2022 konglidong <konglidong@uniontech.com> - 5.0.20.7-1
- package init
