Summary:       Support for using OpenSSL in python scripts
Name:          python-M2Crypto
Version:       0.46.2
Release:       1
Source:        %{name}-%{version}.tar.gz
License:       BSD-2-Clause
URL:           https://github.com/sailfishos/python-M2Crypto.git

BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(openssl)
BuildRequires: python3-setuptools
BuildRequires: pkgconfig
BuildRequires: swig
BuildRequires: fdupes
Patch1:        0001-fix-allow-64-bit-time_t-on-32-bit-systems-in-test_is.patch
Patch2:        0002-fix-correct-struct-packing-on-32-bit-with-_TIME_BITS.patch

%description
This package allows you to call OpenSSL functions from python scripts.

%prep
%autosetup -p1 -n %{name}-%{version}/m2crypto

%build
%py3_build

%install
%py3_install

%fdupes %{buildroot}

%files
%license LICENSES/BSD-2-Clause.txt
%{python3_sitearch}/M2Crypto
%{python3_sitearch}/M2Crypto-*.egg-info/
