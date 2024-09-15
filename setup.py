from setuptools import setup, find_packages
import pkg_resources, os, sys

with open(os.path.join(os.getcwd(), 'DESCRIPTION.rst'), encoding='utf-8') as f:
	description = f.read()

setup(
	name="Poison",

	description=description,

	url="None",

	author="catte",
	author_email="cattedoctor@gmail.com",

	version="0.0.1",
	license="CC BY-NC 4.0",

	use_scm_version=True,
	setup_requires=['setuptools_scm'],

	classifiers=["Development Status :: 3 - Alpha",
	             "License :: Free for non-commercial use"],

	keywords=[],

	packages=['Poison'],
	package_dir={"": "src"}
)