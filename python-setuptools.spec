#
# Conditional build:
%bcond_without	apidocs		# Sphinx based documentation
%bcond_with	tests		# "test" action (fails, pytest-runner doesn't support build-base)
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module
%bcond_without	python3_default	# Use Python 3.x for easy_install executable

%if %{without python3}
%undefine	python3_default
%endif

%define		module	setuptools
Summary:	A collection of enhancements to the Python distutils
Summary(pl.UTF-8):	Zestaw rozszerzeń dla pythonowych distutils
Name:		python-setuptools
Version:	21.0.0
Release:	2
Epoch:		1
License:	PSF or ZPL
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/simple/setuptools/
Source0:	https://pypi.python.org/packages/ff/d4/209f4939c49e31f5524fa0027bf1c8ec3107abaf7c61fdaad704a648c281/setuptools-%{version}.tar.gz
# Source0-md5:	81964fdb89534118707742e6d1a1ddb4
Patch0:		%{name}-missing.patch
URL:		https://github.com/pypa/setuptools
%if %(locale -a | grep -q '^en_US.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildConflicts:	python-distribute < 0.7
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytest >= 2.8
BuildRequires:	python-pytest-runner
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildConflicts:	python3-distribute < 0.7
%if %{with tests}
%if "%{py3_ver}" < "3.3"
BuildRequires:	python3-mock
%endif
BuildRequires:	python3-pytest >= 2.8
BuildRequires:	python3-pytest-runner
%endif
%endif
%if %{with apidocs}
BuildRequires:	python3-rst.linker >= 1.4
BuildRequires:	sphinx-pdg-3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
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

%package -n easy_install
Summary:	Python software installer
Summary(pl.UTF-8):	Instalator oprogramowania napisanego w Pythonie
Group:		Libraries/Python
%if %{with python3_default}
Requires:	python3-%{module} = %{epoch}:%{version}-%{release}
%else
Requires:	python-%{module} = %{epoch}:%{version}-%{release}
%endif
Conflicts:	python-setuptools < 1:18.6.1-2

%description -n easy_install
Python software installer.

%description -n easy_install -l pl.UTF-8
Instalator oprogramowania napisanego w Pythonie.

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
%patch0 -p1

%build
%if %{with python2}
LC_ALL=en_US.UTF-8 \
%py_build %{?with_tests:test}
%endif

%if %{with python3}
LC_ALL=en_US.UTF-8 \
%py3_build %{?with_tests:test}
%endif

%if %{with apidocs}
#%{__make} -C docs html SPHINXBUILD=sphinx-build-3
# rst.linker needs sphinx-build to be run from directory containing "CHANGES.txt"
sphinx-build-3 -b html -d build/doctrees -D latex_paper_size=a4 docs build/html
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
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/easy_install-%{py_ver}
%{py_sitescriptdir}/pkg_resources
%{py_sitescriptdir}/setuptools
%{py_sitescriptdir}/easy_install.py[co]
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
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
%doc build/html/*
%endif
