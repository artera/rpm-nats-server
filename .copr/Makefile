rpmbuild_src = $(shell rpmbuild --eval '%{_sourcedir}')

.PHONY: prepare
prepare:
	dnf -y install rpmdevtools rpm-build wget
	cp *.* $(rpmbuild_src)
	spectool -g -R $(spec)
	[ -f go1.20.10.linux-amd64.tar.gz ] || wget https://go.dev/dl/go1.20.10.linux-amd64.tar.gz
	tar -C /opt -xzf go1.20.10.linux-amd64.tar.gz

.PHONY: srpm
srpm: prepare
	rpmbuild -bs --define "_srcrpmdir $(outdir)" $(spec)

.PHONY: rpm
rpm: prepare
	rpmbuild -bb --define "_rpmdir $(outdir)" $(spec)
