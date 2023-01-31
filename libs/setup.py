#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

short_description = '{}'.format(
    'Automated RPC GUI API based communication with BOINC clients')

setup(
    name='PyBOINC',
    version='0.0.1',
    description=short_description,
    author='nielstron',
    author_email='n.muendler@web.de',
    url='https://github.com/nielstron/pyboinc/',
    py_modules=['pyboinc'],
    packages=find_packages(),
    install_requires=[
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Object Brokering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='python boinc xml api rpc gui science computing',
    python_requires='>=3',
    test_suite='pyboinc.tests',
)
