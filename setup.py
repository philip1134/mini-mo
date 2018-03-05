#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re
from setuptools import setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('minimo/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \"(.*?)\"', f.read()).group(1)

setup(
    name='minimo',
    version=version,
    url='https://github.com/philip1134/mini-mo',
    license='MIT',
    author='Philip CHAN',
    author_email='philip1134@imior.com',
    description='A lightweight automation framework.',
    long_description=readme,
    packages=['minimo', 'minimo.ext'],
    package_data={
        '': ['*.md'],
    },
    platforms='any',
    include_package_data=True,
    zip_safe=False,
    # install_requires=[],
    extras_require={
        'dev': [
            'tox',
            'check-manifest',
            'flake8'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Test Automation',
        'Framework :: minimo',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='Python Test Automation',
    entry_points={
        'console_scripts': [
            'minimo = minimo:main',
        ],
    }
)