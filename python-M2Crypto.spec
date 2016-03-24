%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Support for using OpenSSL in python scripts
Name: python-M2Crypto
Version: 0.23.0
Release: 1
Source0: http://pypi.python.org/packages/source/M/M2Crypto/M2Crypto-%{version}.tar.gz
# This is only precautionary, it does fix anything - not sent upstream
Patch0: python-M2Crypto-0.21.1-gcc_macros.patch
# https://gitlab.com/m2crypto/m2crypto/merge_requests/4
Patch1: python-M2Crypto-0.21.1-supported-ec.patch
Patch2: python-M2Crypto-0.23.0-no-weak-crypto.patch

License: MIT
Group: System Environment/Libraries
URL: https://gitlab.com/m2crypto/m2crypto/
BuildRequires: openssl, openssl-devel, python2-devel, python-setuptools
BuildRequires: perl, pkgconfig, swig, which
Provides:   m2crypto = %{version}
Provides:   python-m2crypto = %{version}

%description
This package allows you to call OpenSSL functions from python scripts.

%prep
%setup -q -n M2Crypto-%{version}
%patch0 -p1 -b .gcc_macros
%patch1 -p1 -b .supported-ec
%patch2 -p1 -b .no-weak-crypto

# __REGISTER_PREFIX__ is defined to unquoted $ on some platforms; gcc handles
# this fine, but swig chokes on it.
gcc -E -dM - < /dev/null | grep -v __STDC__ | grep -v __REGISTER_PREFIX__  \
	| sed 's/^\(#define \([^ ]*\) .*\)$/#undef \2\n\1/' > SWIG/gcc_macros.h

%build
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

%{__python} setup.py build

%install
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

%{__python} setup.py install --root=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
# >> files
%doc CHANGES LICENCE README.rst
%{python_sitearch}/*
# << files
