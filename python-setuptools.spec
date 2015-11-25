#
# Conditional build:
%bcond_without	apidocs	# sphinx based documentation
%bcond_with	tests	# "test" action (fails?)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_with 	bootstrap # build using old distribute

%define		module	setuptools
Summary:	A collection of enhancements to the Python distutils
Summary(pl.UTF-8):	Zestaw rozszerzeń dla pythonowych distutils
Name:		python-setuptools
Version:	18.6.1
Release:	1
Epoch:		1
License:	PSF or ZPL
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/pypi/setuptools
Source0:	https://pypi.python.org/packages/source/s/setuptools/setuptools-%{version}.tar.gz
# Source0-md5:	d4797a533b3c7466fd36a791c2de94d2
URL:		https://bitbucket.org/pypa/setuptools
%if %(locale -a | grep -q '^en_US.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
%if %{with bootstrap}
BuildRequires:	python-distribute < 0.7
%else
#BuildRequires:	python-setuptools > 7.0
BuildConflicts:	python-distribute < 0.7
%endif
BuildRequires:	python-modules >= 1:2.6
%endif
%if %{with python3}
%if %{with bootstrap}
BuildRequires:	python3-distribute < 0.7
%else
#BuildRequires:	python3-setuptools > 7.0
BuildConflicts:	python3-distribute < 0.7
%endif
BuildRequires:	python3-modules >= 1:3.2
%endif
%if %{with apidocs}
BuildRequires:	python-rst.linker
BuildRequires:	sphinx-pdg
%endif
BuildRequires:	rpm-pythonprov
Requires:	python-modules >= 1:2.6
Obsoletes:	python-distribute < 0.7
Obsoletes:	python-setuptools-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
setuptools is a collection of enhancements to the Python distutils
that allow you to more easily build and distribute Python 2.x
packages, especially ones that have dependencies on other packages.

%description -l pl.UTF-8
setuptools to zestaw rozszerzeń do pythonowych distutils umożliwiający
łatwiejsze budowanie i rozprowadzanie pakietów Pythona 2.x,
szczególnie tych mających zależności od innych pakietów.

Ten pakiet zawiera składniki uruchomieniowe setuptools, potrzebne do
uruchamiania kodu wymagającego pkg_resources.py, przeznaczone dla
Pythona 2.x.

%package -n python3-%{module}
Summary:	A collection of enhancements to the Python distutils
Summary(pl.UTF-8):	Zestaw rozszerzeń dla pythonowych distutils
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2
Obsoletes:	python3-distribute < 0.7

%description -n python3-%{module}
setuptools is a collection of enhancements to the Python distutils
that allow you to more easily build and distribute Python 3.x
packages, especially ones that have dependencies on other packages.

%description -n python3-%{module} -l pl.UTF-8
setuptools to zestaw rozszerzeń do pythonowych distutils umożliwiający
łatwiejsze budowanie i rozprowadzanie pakietów Pythona 3.x,
szczególnie tych mających zależności od innych pakietów.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

# missing file, required by docs build (as of 18.3)
touch CHANGES.txt

%build
%if %{with python2}
LC_ALL=en_US.UTF-8 \
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
LC_ALL=en_US.UTF-8 \
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with apidocs}
#%{__make} -C docs html
# rst.linker needs sphinx-build to be run from directory containing "CHANGES.txt"
sphinx-build -b html -d build/doctrees -D latex_paper_size=a4 docs build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/easy_install
%attr(755,root,root) %{_bindir}/easy_install-2.*
%{py_sitescriptdir}/pkg_resources
%{py_sitescriptdir}/setuptools
%{py_sitescriptdir}/_markerlib
%{py_sitescriptdir}/easy_install.py[co]
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/easy_install-3.*
%{py3_sitescriptdir}/__pycache__/easy_install.*.py[co]
%{py3_sitescriptdir}/pkg_resources
%{py3_sitescriptdir}/setuptools
%{py3_sitescriptdir}/_markerlib
%{py3_sitescriptdir}/easy_install.py
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/html/*
%endif
