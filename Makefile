.PHONY: all
all:

.PHONY: rpm
rpm: SHELL=fakeroot -- bash
rpm:
	# RPM building is gross
	rm -rf rpmbuild/* && mkdir -p rpmbuild/BUILD/lib/python
	cp -R rpmroot/* rpmbuild/BUILD/
	cp -R qriscloud rccutil rpmbuild/BUILD/lib/python
	# rpmbuild does NOT like relative paths...
	rpmbuild --define "_topdir ${PWD}/rpmbuild" -bb rpm.spec

