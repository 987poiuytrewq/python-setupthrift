#!/usr/bin/env python

from setuptools import setup

setup(entry_points = {
        "distutils.commands": [
           "install = setupthrift:thrift_install",
        ],
        "distutils.setup_keywords": [
            "thrift_root = setupthrift:thrift_root",
        ],
      },
      modules=['setupthrift'],
      version='0.1',
      name='setupthrift')