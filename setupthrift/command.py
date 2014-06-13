from distutils import log
import fnmatch
import os
from setuptools import Command
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import call

namespace_declaration = '''
import pkg_resources
pkg_resources.declare_namespace(__name__)
'''


class CompileThrift(Command):
    """Command to compile thrift files into python modules"""

    description = "compile thrift files into python modules"

    user_options = [
        ('input-root=', 'i', 'Root directory to look for *.thrift files'),
        ('output-root=', 'i', 'Root directory to output python modules to')
    ]

    def initialize_options(self):
        self.input_root = 'thrifts'
        self.output_root = '.'

    def finalize_options(self):
        pass

    def run(self):
        thrift_files = self.find_thrift_files()
        if not thrift_files:
            log.warn('no thrift files found in ' + self.input_root)
        else:
            self.compile_thrift_files(thrift_files)
            self.declare_namespaces()

    def find_thrift_files(self):
        thrift_files = []
        for root, dirs, files in os.walk(self.input_root):
            for filename in fnmatch.filter(files, '*.thrift'):
                thrift_files.append(os.path.join(self.input_root, filename))
        return thrift_files

    def compile_thrift_files(self, thrift_files):
        for thrift_file in thrift_files:
            log.info('compiling thrift file ' + thrift_file)
            call(['thrift', '--gen', 'py', '-out', self.output_root, thrift_file])

    def declare_namespaces(self):
        gen_root = 'gen-py'
        init_filename = '__init__.py'
        for root, dirs, files in os.walk(gen_root):
            if files == [init_filename]:
                with open(os.path.join(gen_root, init_filename), 'w') as init_file:
                    init_file.write(namespace_declaration)


class ThriftInstall(install):

    def __init__(self, dist):
        install.__init__(self, dist)
        self.compile_thrift = CompileThrift(dist)

    def run(self):
        self.compile_thrift.run()
        install.run(self)


class ThriftDevelop(develop):

    def __init__(self, dist):
        develop.__init__(self, dist)
        self.compile_thrift = CompileThrift(dist)

    def run(self):
        self.compile_thrift.run()
        develop.run(self)