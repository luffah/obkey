
lang:
	cd po; make

installdeb:
	dpkg -i deb_dist/obkey_1.2-1_all.deb

installpy:
	python setup.py install

deb: lang
	python setup.py \
		--command-packages=stdeb.command sdist_dsc \
		--package obkey \
		--section x11
	cd deb_dist/obkey-*/; \
	dpkg-buildpackage -rfakeroot -uc -us

lint:
	pylint --output-format=parseable --reports=y ./obkey_parts | tee pylint.log
