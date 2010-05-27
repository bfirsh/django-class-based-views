#!/bin/sh
export PYTHONPATH=.:$PYTHONPATH
django-admin.py test tests --settings=class_based_views.tests.settings
