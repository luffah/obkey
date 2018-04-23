
lang:
	cd po; make

installdeb: deb
	sudo dpkg -i ./obkey.deb
	# find . -mtime 0 -name '*.deb' -exec sudo dpkg -i {} +

installpy:
	python setup.py install

deb: lang
	python setup.py \
		--command-packages=stdeb.command sdist_dsc \
		--package obkey \
		--section x11
	cd deb_dist/obkey-*/; \
	dpkg-buildpackage -rfakeroot -uc -us
	find . -mtime 0 -name '*.deb' -exec cp {} ./obkey.deb \;

deb-pub: lang
	python setup.py \
		--command-packages=stdeb.command sdist_dsc \
		--package obkey \
		--section x11
	cd deb_dist/obkey-*/; \
	dpkg-buildpackage -k${DEBEMAIL}
	find . -mtime 0 -name '*.deb' -exec cp {} ./obkey.deb \;

lint:
	pylint --output-format=parseable --reports=y ./obkey_parts | tee pylint.log

clean:
	rm -rf deb_dist dist build obkey.egg-info
