
%define	module	setuptools
%define	snap	20051219

Summary:	A collection of enhancements to the Python distutils
Summary(pl):	Zestaw rozszerzeń dla pythonowych distutils
Name:		python-setuptools
Version:	0.6a9
Release:	0.%{snap}.1
License:	GPL
Group:		Development/Languages/Python
# Source0:	http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}.zip
Source0:	setuptools-%{snap}.tar.gz
# Source0-md5:	594f178498539c14f646bb00fb382a98
URL:		http://peak.telecommunity.com/DevCenter/setuptools
BuildRequires:	findutils
%pyrequires_eq	python
BuildRequires:	python-devel
BuildRequires:	unzip
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
setuptools is a collection of enhancements to the Python distutils
(for Python 2.3.5 and up on most platforms; 64-bit platforms require a
minimum of Python 2.4) that allow you to more easily build and
distribute Python packages, especially ones that have dependencies on
other packages.

%description -l pl
setuptools to zestaw rozszerzeń do pythonowych distutils (dla Pythona
2.3.5 i nowszego na większości platform; platformy 64-bitowe wymagają
co najmniej Pythona 2.4) umożliwiający łatwiejsze budowanie i
rozprowadzanie pakietów Pythona, szczególnie tych mających zależności
od innych pakietów.

%prep
%setup  -q -n %{module}

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.txt
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/%{module}*
%{py_sitescriptdir}/*.py[co]
