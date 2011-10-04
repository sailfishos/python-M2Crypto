%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Keep this value in sync with the definition in openssl.spec.
%define multilib_arches %{ix86} ia64 ppc ppc64 s390 s390x x86_64 sparc sparcv9 sparc64

Summary: Support for using OpenSSL in python scripts
Name: m2crypto
Version: 0.20.2
Release: 1
Source0: http://pypi.python.org/packages/source/M/M2Crypto/M2Crypto-%{version}.tar.gz
# https://bugzilla.osafoundation.org/show_bug.cgi?id=2341
Patch0: m2crypto-0.18-timeouts.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12855
Patch2: m2crypto-0.20.1-openssl1.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12935
Patch3: m2crypto-0.20.2-threads.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12936
Patch4: m2crypto-0.20.2-testsuite.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12972
Patch5: m2crypto-0.20.2-fips.patch
# https://bugzilla.osafoundation.org/show_bug.cgi?id=12973
Patch6: m2crypto-0.20.2-check.patch
License: MIT
Group: System/Libraries
URL: http://wiki.osafoundation.org/bin/view/Projects/MeTooCrypto
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel, python-devel
BuildRequires: perl, pkgconfig, swig
Requires: python

%description
This package allows you to call OpenSSL functions from python scripts.


%package docs
Summary: Documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description docs
Documentation and test code for %{name}


%prep
%setup -q -n M2Crypto-%{version}
%patch0 -p1
%patch2 -p0 -b .openssl1
%patch3 -p1 -b .threads
%patch4 -p0 -b .testsuite
%patch5 -p1 -b .fips
%patch6 -p1 -b .check

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
%ifarch %{multilib_arches}
for i in SWIG/_ec.i SWIG/_evp.i; do
	sed -i -e "s/opensslconf/opensslconf-${basearch}/" "$i"
done
%endif

%build
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

# -cpperraswarn is necessary for including opensslconf-${basearch} directly
SWIG_FEATURES=-cpperraswarn python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`" ; export CFLAGS
	LDFLAGS="$LDFLAGS`pkg-config --libs-only-L openssl`" ; export LDFLAGS
fi

python setup.py install --root=$RPM_BUILD_ROOT

for i in medusa medusa054; do
	sed -i -e '1s,#! /usr/local/bin/python,#! /usr/bin/python,' \
		demo/$i/http_server.py
done

# Windows-only
rm demo/Zope/starts.bat
# Fix up documentation permssions
find demo tests -type f -perm -111 -print0 | xargs -0 chmod a-x

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENCE README
%{python_sitearch}/M2Crypto
%{python_sitearch}/M2Crypto-*.egg-info

%files docs
%defattr(-,root,root,-)
%doc CHANGES demo tests
