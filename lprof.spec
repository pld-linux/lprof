#
# Conditional build:
%bcond_without	kde	# without KDE version of utilities
#
Summary:	lprof - a colour profile construction set library
Summary(pl.UTF-8):	lprof - biblioteka do konstruowania profili kolorów
Name:		lprof
# Available version:	1.11.4.1
Version:	1.09
Release:	3.1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/lprof/%{name}-%{version}.tar.gz
# Source0-md5:	2177c77c24aa10db9b7681d264735ea9
Patch0:		%{name}-opt.patch
# based on http://www.littlecms.com/lprof-1.09_mrr_patch4
Patch1:		%{name}-mrr.patch
Patch2:		%{name}-targetsdir.patch
Patch3:		%{name}-shared.patch
Patch4:		%{name}-kde.patch
Patch5:		%{name}-qtmt.patch
URL:		http://lprof.sourceforge.net/
%{?with_kde:BuildRequires:	kdelibs-devel >= 3.0}
BuildRequires:	lcms-devel >= 1.09
BuildRequires:	libtool
BuildRequires:	qt-devel >= 1:3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lprof is a colour profile construction set library. Package contains
also sample profilers.

%description -l pl.UTF-8
lprof to biblioteka do konstruowania profili kolorów. Pakiet zawiera
także przykładowe programy do profilowania sprzętu.

%package devel
Summary:	lprof header files and static library
Summary(pl.UTF-8):	Pliki nagłówkowe i statyczna biblioteka lprof
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for lprof - a colour profile construction set library.

%description devel -l pl.UTF-8
Pliki nagłówkowe lprof - biblioteki do konstruowania profili kolorów.

%package static
Summary:	Static lprof library
Summary(pl.UTF-8):	Statyczna biblioteka lprof
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lprof library.

%description static -l pl.UTF-8
Statyczna biblioteka lprof.

%package data
Summary:	Colour profiling targets data
Summary(pl.UTF-8):	Dane urządzeń do profilowania kolorów
Group:		Libraries

%description data
Colour profiling targets data.

%description data -l pl.UTF-8
Dane urządzeń do profilowania kolorów.

%package qt
Summary:	Qt-based sample colour profilers
Summary(pl.UTF-8):	Oparte na Qt przykładowe narzędzia do profilowania kolorów
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-data = %{version}-%{release}

%description qt
Qt-based sample colour profilers: qtMonitorProfiler,
qtScannerProfiler, qtMeasurementTool and qtProfileChecker.

%description qt -l pl.UTF-8
Oparte na Qt przykładowe narzędzia do profilowania kolorów:
qtMonitorProfiler, qtScannerProfiler, qtMeasurementTool i
qtProfileChecker.

%package kde
Summary:	KDE-based sample colour profilers
Summary(pl.UTF-8):	Oparte na KDE przykładowe narzędzia do profilowania kolorów
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-data = %{version}-%{release}

%description kde
KDE-based sample colour profilers: kMonitorProfiler, kScannerProfiler,
kMeasurementTool and kProfileChecker.

%description kde -l pl.UTF-8
Oparte na KDE przykładowe narzędzia do profilowania kolorów:
kMonitorProfiler, kScannerProfiler, kMeasurementTool i
kProfileChecker.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%build
%{__make} all \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}" \
	LIBDIR=%{_libdir} \
	QTDIR=/usr

%if %{with kde}
for d in qt/qt[MPS]* ; do
	%{__make} -C $d clean \
		BINDIR=fake
done

%{__make} all \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}" \
	LIBDIR=%{_libdir} \
	QTDIR=/usr \
	KDEDIR=/usr \
	USE_KDE=y
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/lprof}

%{__make} install -C src \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}

install icc2it8 qt[mps]* $RPM_BUILD_ROOT%{_bindir}

%if %{with kde}
install k[mps]* $RPM_BUILD_ROOT%{_bindir}
%endif

cp -rf targets $RPM_BUILD_ROOT%{_datadir}/lprof

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README manual.txt
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_bindir}/icc*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/liblprof.la
%{_includedir}/lcmsprf.h

%files static
%defattr(644,root,root,755)
%{_libdir}/liblprof.a

%files data
%defattr(644,root,root,755)
%{_datadir}/lprof

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qt*

%if %{with kde}
%files kde
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/k*
%endif
