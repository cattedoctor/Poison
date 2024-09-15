
all: clean generic

generic:
	/bin/python3 setup.py bdist_wheel

linux_wheel:
	/bin/python3 setup.py bdist_wheel --plat-name linux-x86_64

install:
	/bin/pip3 install -U dist/Poison*whl

.PHONY: clean
clean:
	@echo "Cleaning up install"
	rm -rf .eggs build dist src/*-info *egg-*
	echo "y" | sudo /bin/pip3 uninstall Poison
