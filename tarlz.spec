Summary:	Parallel combined implementation of tar archiver and lzip compressor
Summary(pl.UTF-8):	Równoległa, połączona implementacja archiwizera tar oraz kompresora lzip
Name:		tarlz
Version:	0.28.1
Release:	1
License:	GPL v2+
Group:		Applications/Archiving
Source0:	http://download.savannah.gnu.org/releases/lzip/tarlz/%{name}-%{version}.tar.lz
# Source0-md5:	48dadfef0249e882047445f0a4765f1b
Patch0:		%{name}-info.patch
URL:		http://savannah.nongnu.org/projects/lzip/
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	lzip
BuildRequires:	lzlib-devel >= 1.14
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
Requires:	lzlib >= 1.14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tarlz is a massively parallel (multi-threaded) combined implementation
of the tar archiver and the lzip compressor. Tarlz creates, lists and
extracts archives in a simplified posix pax format compressed with
lzip, keeping the alignment between tar members and lzip members. This
method adds an indexed lzip layer on top of the tar archive, making it
possible to decode the archive safely in parallel. The resulting
multimember tar.lz archive is fully backward compatible with standard
tar tools like GNU tar, which treat it like any other tar.lz archive.
Tarlz can append files to the end of such compressed archives.

%description -l pl.UTF-8
Tarlz to intensywnie zrównoleglona (wielowątkowa) połączona
implementacja archiwizera tar oraz kompresora lzip. Tarlz tworzy,
wypisuje zawartość oraz rozpakowuje archiwa w uproszczonym formacie
posix pax, skompresowane przy użyciu lzipa, z zachowaniem wyrównań
pomiędzy elementami archiwum tar oraz elementami lzipa. Ta metoda
dodaje indeksowaną warstwę lzip powyżej archiwum tar, dzięki czemu
można bezpiecznie dekodować równolegle archiwum. Wynikowe archiwum
tar.lz z wieloma plikami jest w pełni wstecznie kompatybilne ze
standardowymi narzędziami tar, takimi jak GNU tar, traktującymi
takie archiwa identycznie, jak inne archiwa tar.lz. Tarlz potrafi
dołączać pliki na końcu takich skompresowanych archiwów.

%prep
%setup -q
%patch -P0 -p1

%build
# not autoconf configure, imitates 2.50+ style invocation (exported variables don't work)
./configure \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}" \
	CPPFLAGS="%{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	--prefix=%{_prefix}

%{__make} all info

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/tarlz
%{_mandir}/man1/tarlz.1*
%{_infodir}/tarlz.info*
