%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Summary: Support for using OpenSSL in python scripts
Name: python-M2Crypto
Version: 0.35.2
Release: 1
Source: python-M2Crypto-%{version}.tar.gz 

License: MIT
Group: System Environment/Libraries
URL: https://gitlab.com/m2crypto/m2crypto/
BuildRequires: openssl, openssl-devel, python3-devel, python3-setuptools
BuildRequires: pkgconfig, swig, which
Provides:   m2crypto = %{version}
Provides:   python-m2crypto = %{version}

%description
This package allows you to call OpenSSL functions from python scripts.

%prep
%setup -q -n python-M2Crypto-%{version}/m2crypto 

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

%{__python3} setup.py build

%install
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

%{__python3} setup.py install --root=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES LICENCE README.rst
%{python3_sitearch}/M2Crypto*
