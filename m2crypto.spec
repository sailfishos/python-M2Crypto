%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Support for using OpenSSL in python scripts
Name: m2crypto
Version: 0.21.1
Release: 1
Source0: http://pypi.python.org/packages/source/M/M2Crypto/M2Crypto-%{version}.tar.gz
# https://bugzilla.osafoundation.org/show_bug.cgi?id=2341
Patch0: m2crypto-0.21.1-timeouts.patch
# This is only precautionary, it does fix anything - not sent upstream
Patch1: m2crypto-0.21.1-gcc_macros.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12972
Patch2: m2crypto-0.20.2-fips.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12973
Patch3: m2crypto-0.20.2-check.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13005
Patch4: m2crypto-0.21.1-memoryview.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13020
Patch5: m2crypto-0.21.1-smime-doc.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12999
Patch6: m2crypto-0.21.1-AES_crypt.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13044
Patch7: m2crypto-0.21.1-IPv6.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=13049
Patch8: m2crypto-0.21.1-https-proxy.patch
License: MIT
Group: System Environment/Libraries
URL: http://wiki.osafoundation.org/bin/view/Projects/MeTooCrypto
BuildRequires: openssl-devel, python2-devel
BuildRequires: perl, pkgconfig, swig, which
Provides:   python-m2crypto = %{version}
Provides:   python-M2Crypto = %{version}
Obsoletes:   python-m2crypto <= %{version}
Obsoletes:   python-M2Crypto <= %{version}

%filter_provides_in %{python_sitearch}/M2Crypto/__m2crypto.so
%filter_setup

%description
This package allows you to call OpenSSL functions from python scripts.

%prep
%setup -q -n M2Crypto-%{version}
%patch0 -p1 -b .timeouts
%patch1 -p1 -b .gcc_macros
%patch2 -p1 -b .fips
%patch3 -p1 -b .check
%patch4 -p1 -b .memoryview
%patch5 -p0
%patch6 -p0 -b .AES_crypt
%patch7 -p1 -b .IPv6
%patch8 -p1 -b .https-proxy

# Red Hat opensslconf.h #includes an architecture-specific file, but SWIG
# doesn't follow the #include.

# Determine which arch opensslconf.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif
%ifarch sparcv9
basearch=sparc
%endif

gcc -E -dM - < /dev/null | grep -v __STDC__ \
	| sed 's/^\(#define \([^ ]*\) .*\)$/#undef \2\n\1/' > SWIG/gcc_macros.h

%build
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

# -cpperraswarn is necessary for including opensslconf-${basearch} directly
SWIG_FEATURES=-cpperraswarn %{__python} setup.py build

%install
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

%{__python} setup.py install --root=$RPM_BUILD_ROOT

for i in medusa medusa054; do
	sed -i -e '1s,#! /usr/local/bin/python,#! %{__python},' \
		demo/$i/http_server.py
done

# Windows-only
rm demo/Zope/starts.bat
# Fix up documentation permissions
find demo tests -type f -perm -111 -print0 | xargs -0 chmod a-x

grep -rl '/usr/bin/env python' demo tests \
	| xargs sed -i "s,/usr/bin/env python,%{__python},"

rm tests/*.py.* # Patch backup files

%files
%defattr(-,root,root)
%doc CHANGES LICENCE README demo tests
%{python_sitearch}/M2Crypto
%{python_sitearch}/M2Crypto-*.egg-info

