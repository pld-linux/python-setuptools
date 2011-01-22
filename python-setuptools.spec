%define		module	setuptools
%define		subver 	c11
%define		rel	3
Summary:	A collection of enhancements to the Python distutils
Summary(pl.UTF-8):	Zestaw rozszerzeń dla pythonowych distutils
Name:		python-setuptools
Version:	0.6
Release:	2.%{subver}.%{rel}
Epoch:		1
License:	GPL
Group:		Development/Languages/Python
Source0:	http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}%{subver}.tar.gz
# Source0-md5:	7df2a529a074f613b509fb44feefe74e
URL:		http://peak.telecommunity.com/DevCenter/setuptools
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
setuptools is a collection of enhancements to the Python distutils
that allow you to more easily build and distribute Python packages,
especially ones that have dependencies on other packages.

This package contains the runtime components of setuptools, necessary
to execute the software that requires pkg_resources.py.

%description -l pl.UTF-8
setuptools to zestaw rozszerzeń do pythonowych distutils umożliwiający
łatwiejsze budowanie i rozprowadzanie pakietów Pythona, szczególnie
tych mających zależności od innych pakietów.

Ten pakiet zawiera składniki uruchomieniowe setuptools, potrzebne do
uruchamiania kodu wymagającego pkg_resources.py.

%package devel
Summary:	Download, install, upgrade, and uninstall Python packages
Summary(pl.UTF-8):	Ściąganie, instalacja, uaktualnianie i usuwanie pakietów Pythona
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python-devel

%description devel
setuptools is a collection of enhancements to the Python distutils
that allow you to more easily build and distribute Python packages,
especially ones that have dependencies on other packages.

This package contains the components necessary to build and install
software requiring setuptools.

%description devel -l pl.UTF-8
setuptools to zestaw rozszerzeń do pythonowych distutils umożliwiający
łatwiejsze budowanie i rozprowadzanie pakietów Pythona, szczególnie
tych mających zależności od innych pakietów.

Ten pakiet zawiera składniki potrzebne do budowania i instalacji
oprogramowania wymagającego setuptools.

%prep
%setup -q -n %{module}-%{version}%{subver}

%build
%{__python} ./setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} ./setup.py install \
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
