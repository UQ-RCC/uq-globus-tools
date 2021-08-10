.PHONY: all
all:

uq-globus-tools.mod: uq-globus-tools.te
	checkmodule -M -m -o $@ $^

uq-globus-tools.pp: uq-globus-tools.mod
	semodule_package -o $@ -m $^

.PHONY: rpm
rpm: SHELL=fakeroot -- bash
rpm: uq-globus-tools.pp
	# RPM building is gross
	rm -rf rpmbuild/* && mkdir -p rpmbuild/BUILD/{lib/python,share/selinux/targeted}
	cp -R rpmroot/* rpmbuild/BUILD/
	cp -R qriscloud rccutil rpmbuild/BUILD/lib/python
	python3 -m compileall rpmbuild/BUILD/lib/python
	cp uq-globus-tools.pp rpmbuild/BUILD/share/selinux/targeted
	# rpmbuild does NOT like relative paths...
	rpmbuild --define "_topdir ${PWD}/rpmbuild" -bb rpm.spec

clean:
	rm -rf rpmbuild
	rm -f uq-globus-tools.{mod,pp}
