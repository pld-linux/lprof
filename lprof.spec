# TODO:
# - optional KDE support (default off or second package)
# - install targets data - where?
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
URL:		http://www.littlecms.com/profilers.htm
BuildRequires:	lcms-devel >= 1.09
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
# doesn't require base

%description devel
Header files and static library for lprof - a colour profile
construction set library.

%description devel -l pl
Pliki nag³ówkowe i statyczna biblioteka lprof - s³u¿±ca do
konstruowania profili kolorów.

%prep
%setup -q
%patch -p1

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README manual.txt
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/liblprof.a
%{_includedir}/lcmsprf.h
