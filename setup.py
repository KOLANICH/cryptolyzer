#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import unittest

from setuptools import setup

this_directory = os.getenv('REQUIREMENTS_DIR', '')
with open(os.path.join(this_directory, 'requirements.txt')) as f:
    install_requirements = f.read().splitlines()
this_directory = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


test_requirements = [
    "unittest2",
    "coverage",
    "six",
]


def test_discover():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite


setup(
    name='cryptolyzer',
    version='0.2.0',
    description='Fast and flexible cryptographic protocol analyzer',
    long_description=long_description,
    author='Szilárd Pfeiffer',
    author_email='coroner@pfeifferszilard.hu',
    maintainer='Szilárd Pfeiffer',
    maintainer_email='coroner@pfeifferszilard.hu',
    license='MPL-2.0',
    url='https://gitlab.com/coroner/cryptolyzer',
    entry_points={
        'console_scripts': ['cryptolyze = cryptolyzer.__main__:main']
    },
    install_requires=install_requirements,
    extras_require={
        ":python_version < '3'": ["enum34==1.1.6", "Mock", ],

        "test": test_requirements,
        "pep8": ["flake8", ],
        "pylint": ["pylint", ],
    },

    packages=[
        'cryptolyzer',
        'cryptolyzer.common',
        'cryptolyzer.ja3',
        'cryptolyzer.tls',
    ],

    test_suite='setup.test_discover',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'Topic :: Software Development :: Testing',
    ],
)
