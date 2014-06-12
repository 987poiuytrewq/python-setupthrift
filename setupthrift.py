import fnmatch
import os
from setuptools.command.install import install
from subprocess import call

namespace_declaration = '''
import pkg_resources
pkg_resources.declare_namespace(__name__)
'''


class thrift_install(install):
    """Command to compile thrift files into python modules and then install them"""

    description = "compile thrift files into python modules"

    user_options = [
        ('thrift_root=', 'r', 'Root directory to look for *.thrift files'),
    ]

    def initialize_options(self):
        self.thrift_root = 'thrifts'
        install.initialize_options(self)

    def run(self):
        thrift_files = self.find_thrift_files()
        if not thrift_files:
            self.announce('No thrift files found in ' + self.thrift_root)
        else:
            self.compile_thrift_files(thrift_files)
            self.declare_namespaces()
        install.run(self)

    def find_thrift_files(self):
        thrift_files = []
        for root, dirs, files in os.walk(self.thrift_root):
            for filename in fnmatch.filter(files, '*.thrift'):
                thrift_files.append(os.path.join(self.thrift_root, filename))
        return thrift_files

    def compile_thrift_files(self, thrift_files):
        for thrift_file in thrift_files:
            call(['thrift', '--gen', 'py', thrift_file])

    def declare_namespaces(self):
        gen_root = 'gen-py'
        init_filename = '__init__.py'
        for root, dirs, files in os.walk(gen_root):
            if files == [init_filename]:
                with open(os.path.join(gen_root, init_filename), 'w') as init_file:
                    init_file.write(namespace_declaration)
