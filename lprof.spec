# TODO:
# - optional KDE support (default off or second package)
Summary:	lprof - a colour profile construction set library and sample profilers
Summary(pl):	lprof - biblioteka i narzêdzia do konstruowania profili kolorów
Name:		lprof
Version:	1.09
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://www.littlecms.com/%{name}-%{version}.tar.gz
# Source0-md5:	731d934d2e8b6dda2e453e4b1d2be8f4
Patch0:		%{name}-opt.patch
# based on http://www.littlecms.com/lprof-1.09_mrr_patch4
Patch1:		%{name}-mrr.patch
Patch2:		%{name}-targetsdir.patch
Patch3:		%{name}-shared.patch
URL:		http://www.littlecms.com/profilers.htm
BuildRequires:	lcms-devel >= 1.09
BuildRequires:	libtool
BuildRequires:	qt-devel >= 3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lprof is a colour profile construction set library. Package contains
also sample profilers.

%description -l pl
lprof to biblioteka do konstruowania profili kolorów. Pakiet zawiera
tak¿e przyk³adowe programy do profilowania sprzêtu.

%package devel
Summary:	lprof header files and static library
Summary(pl):	Pliki nag³ówkowe i statyczna biblioteka lprof
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for lprof - a colour profile construction set library.

%description devel -l pl
Pliki nag³ówkowe lprof - biblioteki do konstruowania profili kolorów.

%package static
Summary:	Static lprof library
Summary(pl):	Statyczna biblioteka lprof
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static lprof library.

%description static -l pl
Statyczna biblioteka lprof.

%package qt
Summary:	Qt-based sample colour profilers
Summary(pl):	Oparte na Qt przyk³adowe narzêdzia do profilowania kolorów
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}

%description qt
Qt-based sample colour profilers: qtMonitorProfiler,
qtScannerProfiler, qtMeasurementTool and qtProfileChecker.

%description qt -l pl
Oparte na Qt przyk³adowe narzêdzia do profilowania kolorów:
qtMonitorProfiler, qtScannerProfiler, qtMeasurementTool i
qtProfileChecker. 

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} all \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}" \
	QTDIR=/usr \
	KDEDIR=/usr \
	%{?_with_kde:USE_KDE=}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=$RPM_BUILD_ROOT%{_bindir}

install icc2it8 $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_datadir}/lprof
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

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qt*
%{_datadir}/lprof
