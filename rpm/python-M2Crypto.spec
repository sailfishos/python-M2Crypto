Summary: Support for using OpenSSL in python scripts
Name: python-M2Crypto
Version: 0.41.0
Release: 1
Source: %{name}-%{version}.tar.gz

License: MIT
URL: https://gitlab.com/m2crypto/m2crypto/
BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(openssl)
BuildRequires: python3-setuptools
BuildRequires: pkgconfig
BuildRequires: swig
BuildRequires: fdupes
%description
This package allows you to call OpenSSL functions from python scripts.

%prep
%autosetup -p1 -n %{name}-%{version}/m2crypto

%build
export CFLAGS="%{optflags}"
%py3_build

%install
%py3_install

%fdupes %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENCE
%{python3_sitearch}/M2Crypto
%{python3_sitearch}/M2Crypto-*.egg-info/
