#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='setupthrift',
      version='0.1',
      packages=find_packages(),
      entry_points = {
        "distutils.commands": [
           "thrift = setupthrift.command:CompileThrift",
           "install = setupthrift.command:ThriftInstall",
           "develop = setupthrift.command:ThriftDevelop"
        ]
      }
)