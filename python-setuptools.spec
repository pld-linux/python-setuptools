# TODO:
# - sync -pl
%define		module	setuptools
%define		subver 	c8
%define		rel		2
Summary:	A collection of enhancements to the Python distutils
Summary(pl.UTF-8):	Zestaw rozszerzeń dla pythonowych distutils
Name:		python-setuptools
Version:	0.6
Release:	1.%{subver}.%{rel}
Epoch:		1
License:	GPL
Group:		Development/Languages/Python
Source0:	http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}%{subver}.tar.gz
# Source0-md5:	0e9bbe1466f3ee29588cc09d3211a010
URL:		http://peak.telecommunity.com/DevCenter/setuptools
BuildRequires:	python-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
setuptools is a collection of enhancements to the Python distutils
that allow you to more easily build and distribute Python packages,
especially ones that have dependencies on other packages.

This package contains the runtime components of setuptools, necessary
to execute the software that requires pkg_resources.py.

%description -l pl.UTF-8
setuptools to zestaw rozszerzeń do pythonowych distutils (dla Pythona
2.3.5 i nowszego na większości platform; platformy 64-bitowe wymagają
co najmniej Pythona 2.4) umożliwiający łatwiejsze budowanie i
rozprowadzanie pakietów Pythona, szczególnie tych mających zależności
od innych pakietów.

%package devel
Summary:	Download, install, upgrade, and uninstall Python packages
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	python-devel

%description devel
setuptools is a collection of enhancements to the Python distutils
that allow you to more easily build and distribute Python packages,
especially ones that have dependencies on other packages.

This package contains the components necessary to build and install
software requiring setuptools.

%prep
%setup -q -n %{module}-%{version}%{subver}

%build
%{__python} ./setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python ./setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{py_sitescriptdir}/*/*.exe

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
install site.py $RPM_BUILD_ROOT%{py_sitescriptdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc pkg_resources.txt setuptools.txt
%{py_sitescriptdir}/%{module}*
%{py_sitescriptdir}/pkg_resources.py[co]
%{py_sitescriptdir}/site.py[co]
%{py_sitescriptdir}/site.py

%files devel
%defattr(644,root,root,755)
%doc EasyInstall.txt README.txt api_tests.txt
%attr(755,root,root) %{_bindir}/easy_install*
%{py_sitescriptdir}/easy_install.py[co]
