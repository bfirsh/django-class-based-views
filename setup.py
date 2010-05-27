#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup, Command
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'class_based_views.tests.settings'

from django.conf import settings
from django.test.utils import get_runner

class TestCommand(Command):
    def run(self):
        test_runner = get_runner(settings)
        failures = test_runner([], verbosity=1, interactive=True)
        sys.exit(failures)


setup(
    name='django-class-based-views',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='http://github.com/bfirsh/django-class-based-views/',
    packages=[
        'class_based_views',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    cmdclass={'test': TestCommand},
)
