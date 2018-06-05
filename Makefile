default: help

# Prepare #
lang: ## Generate locales
	cd po; make

lint: ## Check code syntax
	pylint --output-format=parseable --reports=y ./obkey_parts | tee pylint.log

clean: 
	rm -rf deb_dist dist build obkey.egg-info

# Generate package #
deb: lang ## Debian
	python setup.py \
		--command-packages=stdeb.command sdist_dsc \
		--package obkey \
		--section x11
	cd deb_dist/obkey-*/; \
	dpkg-buildpackage -rfakeroot -uc -us
	find . -mtime 0 -name '*.deb' -exec cp {} ./obkey.deb \;

deb-pub: lang ## Debian (signed)
	python setup.py \
		--command-packages=stdeb.command sdist_dsc \
		--package obkey \
		--section x11
	cd deb_dist/obkey-*/; \
	dpkg-buildpackage -k${DEBEMAIL}
	find . -mtime 0 -name '*.deb' -exec cp {} ./obkey.deb \;

# Install #
installdeb: deb ## Install as a Debian package
	sudo dpkg -i ./obkey.deb
	# find . -mtime 0 -name '*.deb' -exec sudo dpkg -i {} +

installpy: ## Install as a python package
	python setup.py install


help: ## Show this help
	@sed -n \
	 's/^\(\([a-zA-Z_-]\+\):.*\)\?#\(#\s*\([^#]*\)$$\|\s*\(.*\)\s*#$$\)/\2=====\4=====\5/p' \
	 $(MAKEFILE_LIST) | \
	 awk 'BEGIN {FS = "====="}; {printf "\033[1m%-4s\033[4m\033[36m%-14s\033[0m %s\n", $$3, $$1, $$2 }' | \
	 sed 's/\s\{14\}//'
