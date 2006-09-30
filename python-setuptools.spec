
%define	module	setuptools
%define sub	c3

Summary:	A collection of enhancements to the Python distutils
Summary(pl):	Zestaw rozszerzeñ dla pythonowych distutils
Name:		python-setuptools
Version:	0.6
Release:	0.%{sub}.2
Epoch:		1
License:	GPL
Group:		Development/Languages/Python
Source0:	http://cheeseshop.python.org/packages/source/s/setuptools/setuptools-%{version}%{sub}.tar.gz
# Source0-md5:	76cb98b779d356c64323125490f88d17
URL:		http://peak.telecommunity.com/DevCenter/setuptools
BuildRequires:	findutils
%pyrequires_eq	python
BuildRequires:	python-devel
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
%setup  -q -n %{module}-%{version}%{sub}

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
