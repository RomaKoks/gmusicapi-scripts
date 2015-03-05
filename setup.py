#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import sys
from setuptools import setup

if not ((2, 6, 0) <= sys.version_info[:3] < (2, 8)):
	sys.exit("gmusicapi-scripts only supports Python 2.6 and 2.7.")

# From http://stackoverflow.com/a/7071358/1231454
version_file = "gmusicapi_scripts/_version.py"
version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"

version_file_contents = open(version_file).read()
match = re.search(version_re, version_file_contents, re.M)

if match:
    version = match.group(1)
else:
    raise RuntimeError("Could not find version in '%s'" % version_file)

setup(
	name='gmusicapi_scripts',
	version=version,
	description='A collection of scripts using gmusicapi-wrapper and gmusicapi.',
	license='MIT',
	author='thebigmunch',
	author_email='mail@thebigmunch.me',
	url='https://github.com/thebigmunch/gmusicapi-scripts',
	download_url='https://github.com/thebigmunch/gmusicapi-scripts',
	keywords=[],
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
	],
	packages=['gmusicapi_scripts'],
	entry_points={
		'console_scripts': [
			'gmdelete=gmusicapi_scripts.gmdelete:main',
			'gmdownload=gmusicapi_scripts.gmdownload:main',
			'gmsearch=gmusicapi_scripts.gmsearch:main',
			'gmsync=gmusicapi_scripts.gmsync:main',
			'gmupload=gmusicapi_scripts.gmupload:main'
		]
	},
	install_requires=[
		'gmusicapi-wrapper',
		'gmusicapi',
		'mutagen'
	],
)