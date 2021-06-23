#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re
from setuptools import setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
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
    packages=['minimo'],
    package_data={
        '': ['*.md', '*.rst'],
    },
    platforms='any',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "mako>=1.0.7",
        "click",
        "unittest-xml-reporting",
        "PyYAML",
        "APScheduler"
    ],
    extras_require={
        'dev': [
            'tox',
            'check-manifest',
            'flake8'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Testing',
    ],
    keywords='Python Automation',
    entry_points={
        'console_scripts': [
            'minimo=minimo:main',
            'mmo=minimo:main',
        ],
    }
)
