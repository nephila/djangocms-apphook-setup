#!/usr/bin/env python
# -*- coding: utf-8 -*-

import djangocms_apphook_setup

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djangocms_apphook_setup.__version__

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='djangocms-apphook-setup',
    version=version,
    description='Library to auto setup apphooks',
    long_description=readme + '\n\n' + history,
    author='Iacopo Spalletti',
    author_email='i.spalletti@nephila.it',
    url='https://github.com/nephila/djangocms-apphook-setup',
    packages=[
        'djangocms_apphook_setup',
    ],
    include_package_data=True,
    install_requires=[
        'django-cms',
    ],
    license='BSD',
    zip_safe=False,
    keywords='djangocms-apphook-setup, django CMS, apphook',
    test_suite='cms_helper.run',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
