#define _disable_ld_no_undefined 1

%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

%bcond doc		1
%bcond linuxgpio	1
%bcond linuxspi		1
%bcond parport		1
%bcond sharedlibs	0

Summary:	Software for programming Atmel AVR Microcontroller
Name:		avrdude
Version:	8.1
Release:	1
Group:		Development/Other
License:	GPLv2+
URL:		https://github.com/avrdudes/avrdude/
Source0:	https://github.com/avrdudes/avrdude/archive/v%{version}/%{name}-%{version}.tar.gz
# (debian)
Source1:	com.github.avrdudes.avrdude.metainfo.xml
Patch0:		avrdude-7.1-fix_config_path.patch
Patch1:		avrdude-7.1-fix_manpage.patch

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(hidapi-hidraw)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(libftdi1) python-libftdi
BuildRequires:	pkgconfig(libserialport)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libftdi1)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(gpiod)
BuildRequires:	swig
BuildRequires:	texi2html
BuildRequires:	texinfo
BuildRequires:	texlive
BuildRequires:	texlive-texinfo
BuildRequires:	texlive-dvips
BuildRequires:	texlive-latex
BuildRequires:	texlive-context

%description
AVRDUDE is a program for programming Atmel's AVR CPU's. It can program the 
Flash and EEPROM, and where supported by the serial programming protocol, it 
can program fuse and lock bits. AVRDUDE also supplies a direct instruction 
mode allowing one to issue any programming instruction to the AVR chip 
regardless of whether AVRDUDE implements that specific feature of a 
particular chip.

%files
%license COPYING
%doc %{_docdir}/%{name}/%{name}-html
%doc %{_docdir}/%{name}/%{name}.{dvi,pdf,ps}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/%{name}-gui
%{_bindir}/elf2tag
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}.1*
%{_infodir}/%{name}.info*
%{_metainfodir}/*.metainfo.xml

#----------------------------------------------------------------------------

%if %{with sharedlibs}
%package -n %{libname}
Summary:	Software for programming Atmel AVR Microcontroller
Group:		System/Libraries

%description -n %{libname}
A sharedlibs for programming Atmel's AVR CPU's. It can program the 
Flash and EEPROM, and where supported by the serial programming protocol, it 
can program fuse and lock bits. AVRDUDE also supplies a direct instruction 
mode allowing one to issue any programming instruction to the AVR chip 
regardless of whether AVRDUDE implements that specific feature of a 
particular chip.

%files -n %{libname}
%license COPYING
%{_libdir}/lib%{name}.so.%{major}*
%endif

#----------------------------------------------------------------------------

%if %{with sharedlibs}
%package -n %{devname}
Summary:	Headers, libraries and docs for the %{name} sharedlibs
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package provides development files for %{name} sharedlibs.

%files -n %{devname}
%license COPYING
%doc README.md AUTHORS 
%{_includedir}/lib%{name}.h
%{_libdir}/lib%{name}.so
%endif

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
	-Wno-dev \
	-DBUILD_DOC:BOOL=%{?with_doc:ON}%{!?with_doc:OFF} \
	-DBUILD_SHARED_LIBS:BOOL=%{?with_sharedlibs:ON}%{!?with_sharedlibs:OFF} \
	-DHAVE_LINUXGPIO:BOOL=%{?with_linuxgpio:ON}%{!?with_linuxgpio:OFF} \
	-DHAVE_LINUXSPI:BOOL=%{?with_linuxspi:ON}%{!?with_linuxspi:OFF} \
	-DHAVE_PARPORT:BOOL=%{?with_parport:ON}%{!?with_parport:OFF} \
	-DUSE_EXTERNAL_LIBS:BOOL=OFF \
	-GNinja
%ninja_build 

%install
%ninja_install -C build

# metainfo
install -dp 0755 %{buildroot}/%{_datadir}/metainfo/
cp %{SOURCE1} %{buildroot}/%{_datadir}/metainfo/

# remove sharedlibs, if not needed
%if %{without sharedlibs}
rm -fr %{buildroot}/%{_includedir}
rm -fr %{buildroot}/%{_libdir}
%endif

