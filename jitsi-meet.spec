%define author Christopher Miersma

%define debug_package %{nil}

%{!?local_prefix:%define local_prefix local}
%if "%{local_prefix}" != "false"
%define _prefix /opt/%{local_prefix}
%define _sysconfdir /etc%{_prefix}
%define _datadir %{_prefix}/share
%define _docdir %{_datadir}/doc
%define _mandir %{_datadir}/man
%define _bindir %{_prefix}/bin
%define _sbindir %{_prefix}/sbin
%define _libdir %{_prefix}/lib
%define _libexecdir %{_prefix}/libexec
%define _includedir %{_prefix}/include
%endif

Name:		jitsi-meet
Version:        1.0.2148
Release:        2.local

Summary:	Jitsi-Meet
Group:		local
License:	Apache
URL:		https://gitlab.com/ccmiersma/%{name}/
Source0:        %{name}-%{version}.tar.gz
BuildArch:      x86_64
BuildRequires:  pandoc npm
Requires:       local-httpd-vhosts


%description
This is the Jitsi Meet web application that provides access to Jicofo and Jitsi-Videobridge.


%prep

%setup



%build

npm install

make

%install

mkdir -p %buildroot%_prefix
mkdir -p %buildroot%_datadir
mkdir -p %buildroot%_docdir
mkdir -p %buildroot%_mandir
mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_sbindir
mkdir -p %buildroot%_libdir/scripts
mkdir -p %buildroot%_libexecdir 
mkdir -p %buildroot%_includedir 
mkdir -p %buildroot%_sysconfdir/jitsi-meet
mkdir -p %buildroot/etc/httpd/conf.d/local-webapps.d/
mkdir -p %buildroot/var/www/local-webapps.d/
mkdir -p %buildroot/var/opt/%{local_prefix}

mkdir -p %buildroot%_mandir/man7
mkdir -p %buildroot%_prefix/app
mkdir -p %buildroot%_prefix/webapps
mkdir -p %buildroot%_prefix/lib64

cp -r ./ %buildroot/var/www/local-webapps.d/jitsi-meet
mv %buildroot/var/www/local-webapps.d/jitsi-meet/jitsi-meet.conf %buildroot/etc/httpd/conf.d/local-webapps.d/
rm %buildroot/var/www/local-webapps.d/jitsi-meet/jitsi-meet.spec

mv %buildroot/var/www/local-webapps.d/jitsi-meet/config.js %buildroot%_sysconfdir/jitsi-meet/
ln -sT %_sysconfdir/jitsi-meet/config.js %buildroot/var/www/local-webapps.d/jitsi-meet/config.js

#Run this script in advance so that our find command picks it up.
/usr/lib/rpm/brp-python-bytecompile


##Manually defined files and dirs that need special designation.
##This will end up in the files section.
cat > %{name}-defined-files-list << EOF
%docdir %{_mandir}
%docdir %{_docdir}
%dir /var/www/local-webapps.d/jitsi-meet/
%config(noreplace) /etc/httpd/conf.d/local-webapps.d/jitsi-meet.conf
%config(noreplace) %_sysconfdir/jitsi-meet/config.js
EOF

##Convoluted stuff to combine the manual list above with any new files we find, into a correct list with no duplicates
find %buildroot -type f -o -type l | sed -e "s#${RPM_BUILD_ROOT}##g"|sed -e "s#\(.*\)#\"\1\"#" > %{name}-all-files-list
cat %{name}-defined-files-list | cut -f2 -d' ' | sed -e "s#\(.*\)#\"\1\"#" | sort > %{name}-defined-files-list.tmp
cat %{name}-all-files-list | sort > %{name}-auto-files-list.tmp
diff -e %{name}-defined-files-list.tmp %{name}-auto-files-list.tmp | grep "^\"" > %{name}-auto-files-list
cat %{name}-defined-files-list %{name}-auto-files-list > %{name}-files-list



%clean
%__rm -rf %buildroot

%files -f %{name}-files-list
%defattr(-,root,root, -)


# The post and postun update the man page database
%post



%postun


%changelog
* Mon Aug 07 2017 Christopher Miersma <ccmiersma@gmail.com> 1.0.2148-2.local
- new package built with tito



