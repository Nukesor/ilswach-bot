.PHONY: default, dev-install, upload

default: dev-install

dev-install:
	sudo python setup.py develop

install:
	sudo python setup.py install

upload: clean dist
	twine upload dist/*
