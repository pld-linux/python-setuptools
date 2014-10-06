#
# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	setuptools
Summary:	A collection of enhancements to the Python distutils
Summary(pl.UTF-8):	Zestaw rozszerzeń dla pythonowych distutils
Name:		python-setuptools
Version:	6.0.2
Release:	1
Epoch:		1
License:	PSF or ZPL
Group:		Development/Languages/Python
Source0:	http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}.tar.gz
# Source0-md5:	b79fab610e362fe8e3a9cb92fb9d95ef
URL:		https://bitbucket.org/pypa/setuptools
%if %{with python2}
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
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

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

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
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt DEVGUIDE.txt 
%attr(755,root,root) %{_bindir}/easy_install
%attr(755,root,root) %{_bindir}/easy_install-2.*
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/_markerlib
%{py_sitescriptdir}/easy_install.py[co]
%{py_sitescriptdir}/pkg_resources.py[co]

%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt DEVGUIDE.txt 
%attr(755,root,root) %{_bindir}/easy_install-3.*
%{py3_sitescriptdir}/__pycache__/*
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/_markerlib
%{py3_sitescriptdir}/easy_install.py
%{py3_sitescriptdir}/pkg_resources.py
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
# %doc docs/_build/html/*
%endif


