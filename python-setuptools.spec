
%define	module	setuptools

Summary:	A collection of enhancements to the Python distutils
Summary(pl):	Zestaw rozszerzeñ dla pythonowych distutils
Name:		python-setuptools
Version:	0.6a8
Release:	1
License:	GPL
Group:		Development/Languages/Python
Source0:	http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}.zip
# Source0-md5:	3eecdf66c1a2cf8a6556bc00b69d572a
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
setuptools to zestaw rozszerzeñ do pythonowych distutils (dla Pythona
2.3.5 i nowszego na wiêkszo¶ci platform; platformy 64-bitowe wymagaj±
co najmniej Pythona 2.4) umo¿liwiaj±cy ³atwiejsze budowanie i
rozprowadzanie pakietów Pythona, szczególnie tych maj±cych zale¿no¶ci
od innych pakietów.

%prep
%setup  -q -n %{module}-%{version}

%build
python ./setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python ./setup.py install \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name '*.pyc' -exec rm "{}" ";"
find $RPM_BUILD_ROOT -type f -name '*.pyo' -exec rm "{}" ";"
find $RPM_BUILD_ROOT -type f -exec sed -i -e "s#$RPM_BUILD_ROOT##g" "{}" ";"

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

echo '%{module}-%{version}-py%{py_ver}.egg' > $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}.pth

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.txt
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/%{module}*
