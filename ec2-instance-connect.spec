%global         srcname         aws-ec2-instance-connect-config
%global         debug_package   %{nil}

%global         commit          551c73e8ec1f5ade4c8b1f52cf616e75b47879b4
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           ec2-instance-connect
Version:        1.1.17
Release:        1.20240215git%{shortcommit}%{?dist}
Summary:        SSH daemon configuration for AWS EC2 Instance Connect

License:        Apache-2.0 
URL:            https://github.com/aws/%{srcname}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz 

# Upstream uses /opt/aws/bin, but we use /usr/bin here for the EIC scripts.
Patch0:         usr-bin-for-script-path.patch

BuildRequires:  systemd 

Requires:       curl
Requires:       openssh-server
Requires:       shadow-utils
Requires:       systemd

%description
This package contains the EC2 instance configuration and scripts
necessary to enable AWS EC2 Instance Connect.


%prep
%autosetup -v -p1 -n %{srcname}-%{commit}


%build
echo "No build steps required"


%install
mkdir -p %{buildroot}%{_unitdir}/sshd.service.d/
install -p -D -m 0644 src/rpm_systemd/sshd.service.d/ec2-instance-connect.conf %{buildroot}%{_unitdir}/sshd.service.d/

mkdir -p %{buildroot}%{_bindir}/
install -m 755 src/bin/* %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md
%{_unitdir}/sshd.service.d/ec2-instance-connect.conf
%{_bindir}/eic_curl_authorized_keys
%{_bindir}/eic_parse_authorized_keys
%{_bindir}/eic_run_authorized_keys


%pre
if ! getent passwd ec2-instance-connect >/dev/null; then
  useradd --system --no-create-home --shell /sbin/nologin ec2-instance-connect
fi


%post
%systemd_post sshd.service


%preun
%systemd_preun sshd.service


%postun
%systemd_postun_with_restart sshd.service


%changelog
* Thu Feb 15 2024 Major Hayden <major@mhtx.net> - 1.1.17-1.20240215git551c73e
- Initial package 
