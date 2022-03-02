#
# Conditional build:
%bcond_without	apidocs		# Sphinx based documentation
%bcond_with	system_libs	# use system modules (appdirs, packaging, pyparsing, six) # TODO
%bcond_with	tests		# py.test tests (few failures)
%bcond_with	bootstrap	# convenience alias for without: apidocs,system_libs,tests
%bcond_without	python2		# CPython 2.x module
%bcond_with	python3		# CPython 3.x module
%bcond_with	python3_default	# Use Python 3.x for easy_install executable

%if %{without python3}
%undefine	python3_default
%endif
%if %{with bootstrap}
%undefine	with_apidocs
%undefine	with_system_libs
%undefine	with_tests
%endif

%define		module		setuptools
%define		pypi_name	setuptools
Summary:	A collection of enhancements to the Python distutils
Summary(pl.UTF-8):	Zestaw rozszerzeń dla pythonowych distutils
Name:		python-setuptools
Version:	42.0.2
Release:	6
Epoch:		1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/setuptools/
Source0:	https://files.pythonhosted.org/packages/source/s/setuptools/%{pypi_name}-%{version}.zip
# Source0-md5:	5ac69b66a6f7d4785517017f37df28e9
URL:		https://github.com/pypa/setuptools
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
%if %{with system_libs}
# versions from pkg_resources/_vendor/vendored.txt
BuildRequires:	python-appdirs >= 1.4.3
BuildRequires:	python-packaging >= 19.2
BuildRequires:	python-pyparsing >= 2.2.1
BuildRequires:	python-six >= 1.10.0
%endif
BuildConflicts:	python-distribute < 0.7
%if %{with tests}
# https://raw.githubusercontent.com/pypa/setuptools/v%{version}/tests/requirements.txt
BuildRequires:	python-coverage >= 4.5.1
BuildRequires:	python-futures
BuildRequires:	python-mock
BuildRequires:	python-pip >= 19.1
BuildRequires:	python-pytest >= 3.7
BuildRequires:	python-pytest-cov >= 2.5.1
BuildRequires:	python-pytest-fixture-config
BuildRequires:	python-pytest-flake8
BuildRequires:	python-pytest-virtualenv >= 1.2.7
BuildRequires:	python-virtualenv >= 13.0.0
BuildRequires:	python-wheel
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
%if %{with system_libs}
# versions from pkg_resources/_vendor/vendored.txt
BuildRequires:	python3-appdirs >= 1.4.3
BuildRequires:	python3-packaging >= 19.2
BuildRequires:	python3-pyparsing >= 2.2.1
BuildRequires:	python3-six >= 1.10.0
%endif
BuildConflicts:	python3-distribute < 0.7
%if %{with tests}
BuildRequires:	python3-coverage >= 4.5.1
# FIXME: patch to use unittest.mock
#BuildRequires:	python3-mock
%if "%{py3_ver}" >= "3.6"
BuildRequires:	python3-paver
%endif
BuildRequires:	python3-pip >= 19.1
BuildRequires:	python3-pytest >= 3.7
BuildRequires:	python3-pytest-cov >= 2.5.1
BuildRequires:	python3-pytest-fixture-config
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-pytest-virtualenv >= 1.2.7
BuildRequires:	python3-virtualenv >= 13.0.0
BuildRequires:	python3-wheel
%endif
%endif
%if %{with apidocs}
BuildRequires:	python3-jaraco
BuildRequires:	python3-jaraco.packaging >= 6.1
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	python3-setuptools >= 1:34
BuildRequires:	sphinx-pdg-3 >= 1.4
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
Requires:	python-modules >= 1:2.7
%if %{with system_libs}
# versions from pkg_resources/_vendor/vendored.txt
Requires:	python-appdirs >= 1.4.0
Requires:	python-packaging >= 16.8
Requires:	python-pyparsing >= 2.1.10
Requires:	python-six >= 1.10.0
%endif
Obsoletes:	python-distribute < 0.7
Obsoletes:	python-setuptools-devel < 1:6.0
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
Requires:	python3-modules >= 1:3.4
%if %{with system_libs}
# versions from pkg_resources/_vendor/vendored.txt
Requires:	python3-appdirs >= 1.4.0
Requires:	python3-packaging >= 16.8
Requires:	python3-pyparsing >= 2.1.10
Requires:	python3-six >= 1.10.0
%endif
Obsoletes:	python3-distribute < 0.7

%description -n python3-%{module}
setuptools is a collection of enhancements to the Python distutils
that allow you to more easily build and distribute Python 3.x
packages, especially ones that have dependencies on other packages.

%description -n python3-%{module} -l pl.UTF-8
setuptools to zestaw rozszerzeń do pythonowych distutils umożliwiający
łatwiejsze budowanie i rozprowadzanie pakietów Pythona 3.x,
szczególnie tych mających zależności od innych pakietów.

%package -n easy_install
Summary:	Python software installer (deprecated)
Summary(pl.UTF-8):	Instalator oprogramowania napisanego w Pythonie (przestarzały)
Group:		Libraries/Python
%if %{with python3_default}
Requires:	python3-%{module} = %{epoch}:%{version}-%{release}
%else
Requires:	python-%{module} = %{epoch}:%{version}-%{release}
%endif
Conflicts:	python-setuptools < 1:18.6.1-2

%description -n easy_install
Python software installer. It's deprecated in favour of pip.

%description -n easy_install -l pl.UTF-8
Instalator oprogramowania napisanego w Pythonie. Jest przestarzały,
aktualnym zamiennikiem jest pip.

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

%if %{with system_libs}
exit 1 # TODO: unvendor modules from pkg_resources/_vendor
%endif

%build
%if %{with python2}
LC_ALL=C.UTF-8 \
%py_build

%{?with_tests:%{__python} -m pytest pkg_resources/tests setuptools/tests tests}
%endif

%if %{with python3}
LC_ALL=C.UTF-8 \
%py3_build

%{?with_tests:%{__python3} -m pytest pkg_resources/tests setuptools/tests tests}
%endif

%if %{with apidocs}
%{__make} -C docs html SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install
%endif

%if %{with python2}
%py_install

# note: setuptools/command/easy_install.py expects setuptools/site-patch.py to exist
%py_postclean -x site-patch.py
%endif

%if %{with python3_default}
ln -sf easy_install-%{py3_ver} $RPM_BUILD_ROOT%{_bindir}/easy_install
%else
ln -sf easy_install-%{py_ver} $RPM_BUILD_ROOT%{_bindir}/easy_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/easy_install-%{py_ver}
%{py_sitescriptdir}/pkg_resources
%{py_sitescriptdir}/setuptools
%{py_sitescriptdir}/easy_install.py[co]
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/easy_install-%{py3_ver}
%{py3_sitescriptdir}/__pycache__/easy_install.*.py[co]
%{py3_sitescriptdir}/pkg_resources
%{py3_sitescriptdir}/setuptools
%{py3_sitescriptdir}/easy_install.py
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%files -n easy_install
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/easy_install

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
