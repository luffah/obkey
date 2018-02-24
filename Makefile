

deb:
	python setup.py \
		--command-packages=stdeb.command sdist_dsc \
		--package obkey \
		--section x11
	cd deb_dist/obkey-*/; \
	dpkg-buildpackage -rfakeroot -uc -us

lint:
	pylint --output-format=parseable --reports=y obkey_classes | tee pylint.log
