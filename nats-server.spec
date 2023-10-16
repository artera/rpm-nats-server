%define _sysusersdir %{_prefix}/lib/sysusers.d
%undefine _missing_build_ids_terminate_build
%global gopath %{_datadir}/gocode
%global gobuilddir %{_builddir}/_build

%global goipath github.com/nats-io/nats-server
Version: 2.10.3

%gometa

%global golicenses LICENSE

Name:    nats-server
Release: 1%{?dist}
Summary: High-Performance server for NATS, the cloud native messaging system
License: Apache License
URL:     %{gourl}
Source0: %{gosource}
Source1: nats.user

BuildRequires: systemd-rpm-macros
BuildRequires: wget

%description
NATS is a simple, secure and performant communications system for digital
systems, services and devices.
NATS is part of the Cloud Native Computing Foundation (CNCF).
NATS has over 40 client language implementations, and its server can run
on-premise, in the cloud, at the edge, and even on a Raspberry Pi.
NATS can secure and simplify design and operation of modern distributed
systems.

%global debug_package %{nil}

%prep
%setup
mkdir -p %{gobuilddir}/src/$(dirname %{goipath})
ln -s $(pwd) %{gobuilddir}/src/%{goipath}
export GOPATH="%{gobuilddir}:${GOPATH:+${GOPATH}:}%{?gopath}"
wget https://go.dev/dl/go1.20.10.linux-amd64.tar.gz -O- | tar -C /opt -xzf -

%build
cd %{gobuilddir}/src/%{goipath}
/opt/go/bin/go build \
  -trimpath \
  -buildmode=pie \
  -o %{gobuilddir}/bin/nats-server .

%install
install -Dm0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/nats.conf
install -Dm0755 %{gobuilddir}/bin/nats-server %{buildroot}%{_sbindir}/nats-server
install -Dm0644 util/nats-server.service %{buildroot}%{_unitdir}/nats-server.service

%files
%license LICENSE
%{_sbindir}/nats-server
%{_unitdir}/*.service
%{_sysusersdir}/*.conf

%post
/usr/bin/systemd-sysusers nats.conf
%systemd_post nats-server.service

%preun
%systemd_preun nats-server.service

%postun
%systemd_postun_with_restart nats-server.service

%changelog
