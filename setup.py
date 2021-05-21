# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in pav_hr/__init__.py
from pav_hr import __version__ as version

setup(
	name='pav_hr',
	version=version,
	description='Partner Add Value in Human Resource Module',
	author='Farouk Muharram',
	author_email='farouk1dev@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
