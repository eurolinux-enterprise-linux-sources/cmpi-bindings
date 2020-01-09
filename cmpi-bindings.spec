Name:           cmpi-bindings
Version:        0.9.5
Release:        6%{?dist}
Summary:        Adapter to write and run CMPI-type CIM providers

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/kkaempf/cmpi-bindings
Source0:        https://github.com/kkaempf/%{name}/archive/v%{version}.tar.gz

#Patch0: don't build ruby and perl bingings
Patch0:         cmpi-bindings-0.4.17-no-ruby-perl.patch
#Patch1: removes workaround no longer needed
Patch1:         cmpi-bindings-0.4.17-sblim-sigsegv.patch
#Patch2: fixes placement of *.py[co] file
Patch2:         cmpi-bindings-0.9.5-python-lib-dir.patch

BuildRequires:  cmake gcc-c++ swig >= 1.3.34
BuildRequires:  curl-devel pkgconfig sed
BuildRequires:  sblim-cmpi-devel
BuildRequires:  python2-devel

%description
CMPI-compliant provider interface for various languages via SWIG


%package -n cmpi-bindings-pywbem
Summary:        Adapter to write and run CMPI-type CIM providers in Python
Group:          Development/Languages
Requires:       pywbem
 
%description -n cmpi-bindings-pywbem
CMPI-compliant provider interface for Python


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .python-lib-dir

# change hardcoded path from /usr/lib/pycim/ to something better
sed -i 's@/usr/lib/pycim/@'`echo %{python_sitelib}/pycim/`'@' swig/python/cmpi_pywbem_bindings.py
# let user know where the providers have to be placed
cat > README.Fedora << EOS 
Python provider interface expects the providers to be placed in:
%{python_sitelib}/pycim/

You can customize the path - edit line 428 in:
%{python_sitelib}/cmpi_pywbem_bindings.py
EOS


%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%_prefix \
      -DLIB=%{_lib} \
      -DCMAKE_VERBOSE_MAKEFILE=TRUE \
      -DCMAKE_C_FLAGS:STRING="%{optflags}" \
      -DCMAKE_CXX_FLAGS_RELEASE:STRING="%{optflags}" \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_SKIP_RPATH=1 \
      ..  
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
mkdir -p $RPM_BUILD_ROOT%{_datadir}/cmpi
make install DESTDIR=$RPM_BUILD_ROOT
# create directory for providers
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/pycim/
rmdir $RPM_BUILD_ROOT%{_datadir}/cmpi


%clean
rm -rf $RPM_BUILD_ROOT


%files -n cmpi-bindings-pywbem
%defattr(-,root,root,-)
%doc README ANNOUNCE COPYING LICENSE.BSD README.Fedora
%dir %{_libdir}/cmpi
%{_libdir}/cmpi/libpyCmpiProvider.so
%{python_sitearch}/cmpi_pywbem_bindings.py*
%{python_sitearch}/cmpi.py*
%dir %{python_sitelib}/pycim/

%changelog
* Wed Mar 19 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.9.5-6
- Fix cflags propagation
  Resolves: #1070791

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.5-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.5-4
- Mass rebuild 2013-12-27

* Tue Aug 13 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.9.5-3
- Fix placement of *.py[co] files
  Resolves: #921547
- Remove /usr/share/cmpi - it's used by ruby binding that we don't build

* Wed Jul 17 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.9.5-2
- Fix URL, fix sources

* Thu Apr 11 2013 Jan Safranek <jsafrane@redhat.com> - 0.9.5-1
- Update to 0.9.5

* Thu Apr 11 2013 Jan Safranek <jsafrane@redhat.com> - 0.9.4-1
- Update to 0.9.4

* Thu Mar 28 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.2-6
- Fixed 'env' parameter value in 'get_providers()' function
  Resolves: #919082
- Fixed embedded instance properties
  Resolves: #919081

* Fri Feb 15 2013 Jan Safranek <jsafrane@redhat.com> - 0.5.2-5
- Fixed passing NULL array from get_instance
  Resolves: #883041

* Wed Jan 30 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.5.2-4
- Fix memory leaks
  Resolves: #902809

* Thu Jan 10 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.5.2-3
- Fixed passing NULL array from get_instance
- Add bindings for CMTraceMessage
  (patches by Jan Safranek)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May  7 2012 Jan Safranek <jsafrane@redhat.com> - 0.5.2
- Update to 0.5.2

* Thu Mar 08 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.4.17-2
- Create and own "pycim" directory
- Add documentation and create README.Fedora

* Thu Mar 01 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.4.17-1
- Initial support (ruby and perl bindings are disabled)
