Summary: Support for using OpenSSL in python scripts
Name: python-M2Crypto
Version: 0.37.1
Release: 1
Source: %{name}-%{version}.tar.gz

License: MIT
URL: https://gitlab.com/m2crypto/m2crypto/
BuildRequires: openssl, openssl-devel, python3-devel, python3-setuptools
BuildRequires: pkgconfig, swig, which
Provides:   m2crypto = %{version}
Provides:   python-m2crypto = %{version}

%description
This package allows you to call OpenSSL functions from python scripts.

%prep
%autosetup -p1 -n %{name}-%{version}/m2crypto
sed -e 's/parameterized//' -i setup.py

%build
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
        CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
        LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

%py3_build

%install
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
        CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
        LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

%py3_install

%files
%defattr(-,root,root,-)
%license LICENCE
%{python3_sitearch}/M2Crypto
%{python3_sitearch}/M2Crypto-*.egg-info/
