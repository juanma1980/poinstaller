#!/usr/bin/env python3

from setuptools import setup

if __name__ == '__main__':
	setup(name='poinstaller',
		version='0.1.1',
		description='Utility for install ',
		long_description="""""",
		author='Lliurex Team',
		author_email='raurodse@gmail.com',
		maintainer='Raul Rodrigo Segura',
		maintainer_email='raurodse@gmail.com',
		keywords=['software',''],
		url='https://github.com/lliurex/poinstaller',
		license='GPL',
		platforms='UNIX',
		packages = ['lliurex.i18n'],
		package_dir = {'lliurex.i18n':'src'},
		scripts=['dh_poinstaller'],
		data_files=[('/usr/share/perl5/Debian/Debhelper/Sequence/',['i18n.pm'])]
	)
