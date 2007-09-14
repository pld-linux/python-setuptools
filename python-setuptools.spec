
%define	module	setuptools
%define sub	c7

Summary:	A collection of enhancements to the Python distutils
Summary(pl.UTF-8):	Zestaw rozszerzeń dla pythonowych distutils
Name:		python-setuptools
Version:	0.6
Release:	0.%{sub}.1
Epoch:		1
License:	GPL
Group:		Development/Languages/Python
Source0:	http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}%{sub}.tar.gz
# Source0-md5:	dedbf6a4f71cd6deaf13ee885054f16b
URL:		http://peak.telecommunity.com/DevCenter/setuptools
BuildRequires:	findutils
%pyrequires_eq	python
BuildRequires:	python-devel
Requires:	python-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
setuptools is a collection of enhancements to the Python distutils
(for Python 2.3.5 and up on most platforms; 64-bit platforms require a
minimum of Python 2.4) that allow you to more easily build and
distribute Python packages, especially ones that have dependencies on
other packages.

%description -l pl.UTF-8
setuptools to zestaw rozszerzeń do pythonowych distutils (dla Pythona
2.3.5 i nowszego na większości platform; platformy 64-bitowe wymagają
co najmniej Pythona 2.4) umożliwiający łatwiejsze budowanie i
rozprowadzanie pakietów Pythona, szczególnie tych mających zależności
od innych pakietów.

%prep
%setup -q -n %{module}-%{version}%{sub}

%build
python ./setup.py build

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
%doc *.txt
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/%{module}*
%{py_sitescriptdir}/*.py[co]
%{py_sitescriptdir}/site.py
