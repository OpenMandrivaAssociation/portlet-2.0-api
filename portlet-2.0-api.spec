%{?_javapackages_macros:%_javapackages_macros}
%global api_version 2.0
%global pkg_name portlet-api_%{api_version}_spec
Name:          portlet-2.0-api
Version:       1.0
Release:       7.0%{?dist}
Summary:       Java Portlet Specification V2.0
License:       ASL 2.0
Url:           http://portals.apache.org/
# svn export http://svn.apache.org/repos/asf/portals/portlet-spec/tags/portlet-api_2.0_spec-1.0 portlet-2.0-api-1.0
# tar czf portlet-2.0-api-1.0-src-svn.tar.gz portlet-2.0-api-1.0
Source0:       %{name}-%{version}-src-svn.tar.gz

BuildRequires: java-devel
BuildRequires: mvn(org.apache.portals:portals-pom)
BuildRequires: mvn(org.apache.tomcat:tomcat-servlet-api)
BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
Requires:      mvn(org.apache.portals:portals-pom)
BuildArch:     noarch

%description
The Java Portlet API version 2.0 developed by the
Java Community Process JSR-286 Expert Group.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
# cleanup
find . -name '*.class' -delete
find . -name '*.jar' -delete

for p in LICENSE NOTICE;do
  iconv -f iso8859-1 -t utf-8 ${p} > ${p}.conv && mv -f ${p}.conv ${p}
  sed -i 's/\r//' ${p}
done

# change apis version
sed -i "s|javax.servlet.http;version=2.4,*|javax.servlet.http;version=3.0,*|" pom.xml

# Force tomcat apis
%pom_remove_dep javax.servlet:servlet-api
%pom_add_dep org.apache.tomcat:tomcat-servlet-api::provided

%mvn_file :%{pkg_name} %{name}
%mvn_alias :%{pkg_name} javax.portlet:portlet-api

%build

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 gil cattaneo <puntogil@libero.it> 1.0-6
- switch to XMvn, minor changes to adapt to current guideline

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 01 2012 gil cattaneo <puntogil@libero.it> 1.0-2
- Install NOTICE file along with javadoc package

* Sat May 19 2012 gil cattaneo <puntogil@libero.it> 1.0-1
- initial rpm