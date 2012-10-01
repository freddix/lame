Summary:	Software to create compressed audio files
Name:		lame
Version:	3.99.5
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	http://downloads.sourceforge.net/lame/%{name}-%{version}.tar.gz
# Source0-md5:	84835b313d4a8b68f5349816d33e07ce
Patch0:		%{name}-link.patch
Patch1:		%{name}-without_gtk.patch
URL:		http://lame.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	nasm
BuildRequires:	ncurses-devel
Requires:	%{name}-libs = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fomit-frame-pointer

%description
Lame is a program which can be used to create compressed audio files.
(Lame aint MP3 encoder). These audio files can be played back by
popular MP3 players such as mpg123.

%package libs
Summary:	LAME MP3 encoding library
Group:		Libraries

%description libs
LAME MP3 encoding library.

%package libs-devel
Summary:	Header files and devel documentation
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description libs-devel
Header files and devel documentation for LAME libraries.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# fix deprecated AM
sed -i "s|AM_C_PROTOTYPES.*||" configure.in
sed -i "s| ansi2knr||" doc/*/Makefile.am
sed -i "s| \$(top_srcdir)/ansi2knr||" libmp3lame/i386/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-cpml		\
	--disable-static	\
	--enable-brhist		\
	--enable-mp3rtp		\
	--enable-shared
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_docdir}/lame/html

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog TODO USAGE doc/html/*.html
%attr(755,root,root) %{_bindir}/lame
%attr(755,root,root) %{_bindir}/mp3rtp
%{_mandir}/man1/lame.1*

%files libs
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files libs-devel
%defattr(644,root,root,755)
%doc API DEFINES
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/lame

