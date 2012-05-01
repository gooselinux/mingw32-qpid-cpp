%global __strip %{_mingw32_strip}
%global __objdump %{_mingw32_objdump}
%global _use_internal_dependency_generator 0
%global __find_requires %{_mingw32_findrequires}
%global __find_provides %{_mingw32_findprovides}
%define __debug_install_post %{_mingw32_debug_install_post}

Name:		mingw32-qpid-cpp
Version:	0.10
Release:	1%{?dist}
Summary:	MinGW Windows port of AMQP C++ Daemons and Libraries

Group:		Development/Libraries
License:	ASL 2.0
URL:		http://qpid.apache.org

Source0:	http://people.apache.org/~robbie/qpid/%{version}/RC3/qpid-%{version}.tar.gz

Patch0:		qpid.patch
Patch1:         mingw32.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:	redhat-rpm-config cmake make ruby ruby-devel python-devel
BuildRequires:	mingw32-gcc-c++ mingw32-boost mingw32-libxslt mingw32-gnutls
BuildRequires:	mingw32-filesystem >= 57
Requires:	mingw32-boost mingw32-libxslt mingw32-gnutls 

%description
MinGW cross-compiled daemons and run-time libraries for AMQP client
applications developed using Qpid C++. Clients exchange messages with
an AMQP message broker using the AMQP protocol.

%{_mingw32_debug_package}

%prep
%setup -q -n qpid-%{version}
%patch0 -p2
%patch1 -p2

%build
%{__mkdir_p} build
pushd build
%_mingw32_cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo	\
		-DBUILD_MSCLFS:BOOL=OFF			\
		-DBUILD_MSSQL:BOOL=OFF			\
		-DBUILD_SSL:BOOL=OFF			\
                -DBoost_DETAILED_FAILURE_MSG:BOOL=ON	\
		-DBoost_COMPILER:STRING=-gcc44 ../cpp
popd

make -C build VERBOSE=1 %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT make -C build VERBOSE=1 install

# Don't package sources in the examples directory
rm -rf $RPM_BUILD_ROOT%{_mingw32_prefix}/examples
rm -rf $RPM_BUILD_ROOT%{_mingw32_prefix}/bin/qpid-latency-test.exe
rm -rf $RPM_BUILD_ROOT%{_mingw32_prefix}/bin/qpid-perftest.exe

# Maybe install some test programs for validation
#{__install} -d $RPM_BUILD_ROOT $RPM_BUILD_ROOT{_mingw32_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc %{_mingw32_prefix}/LICENSE
%doc %{_mingw32_prefix}/NOTICE
%{_mingw32_prefix}/conf
%{_mingw32_prefix}/plugins
%{_mingw32_prefix}/managementgen
%{_mingw32_includedir}/qpid
%{_mingw32_includedir}/qmf
%{_mingw32_bindir}/qpidd.exe
%{_mingw32_bindir}/*.dll
%{_mingw32_bindir}/lib*.dll.a
%doc cpp/RELEASE_NOTES

%changelog
* Mon Mar 28 2011 Ted Ross <tross@redhat.com> - 0.10-1
- Rebase the build to match the native RHEL6 package (qpid-cpp)
- Related: rhbz#690268

* Thu Feb 10 2011 Ted Ross <tross@redhat.com> - 0.8-0.6
- Synchronize the qmf patch set with the native RHEL6 package (qpid-cpp)
- Related: rhbz#658833

* Thu Jan 13 2011 Andrew Beekhof <abeekhof@redhat.com> - 0.8-0.5
- Finalize compilation
  Related: rhbz#658833

* Wed Jan 12 2011 Ted Ross <tross@redhat.com> - 0.8-0.4
- Remove the reference to .fc13 in determining the gcc version
- Related: rhbz#658833

* Wed Jan 12 2011 Ted Ross <tross@redhat.com> - 0.8-0.3
- Initial build in RHEL
- Related: rhbz#658833

* Tue Dec 21 2010 Andrew Beekhof <andrew@beekhof.net> - 0.8-0.2
- Add dependancy on minw32-filesystem

* Fri Dec 3 2010 Andrew Beekhof <andrew@beekhof.net> - 0.8-0.1
- Update to upstream 0.8-rc3

* Fri Sep 10 2010 Andrew Beekhof <andrew@beekhof.net> - 0.6.895736-1
- Initial package creation
