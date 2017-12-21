#! /usr/bin/env python3
#
# Remove wildcard imports from Python code.
#
# Takes Python code on stdin and copies it to stdout,
# replacing any 'from foo import *' with a multi-line
# import of all the symbols in foo.
#
# You can then use pylint or similar to identify and
# delete the unneeded symbols.
#
# See http://github.com/quentinsf/dewildcard for info.
#
# Quentin Stafford-Fraser, 2015

import fileinput
import importlib
import re
import os
import sys
import glob

from contextlib import suppress
from concurrent.futures import ProcessPoolExecutor

IMPORT_ALL_RE = re.compile(r'^\s*from\s*([\w.]*)\s*import\s*[*]')

def import_all_string(module_name, package):
    importlib.import_module(package)
    module = importlib.import_module(module_name, package)

    import_line = 'from %s import (%%s)\n' % module_name
    length = len(import_line) - 4
    return import_line % (',\n' + length * ' ').join(
        [a for a in dir(module) if not a.startswith('_')])


def process_file(file):
    module_name = os.path.relpath(file, os.getcwd())
    module_name = '.'.join(module_name.split(os.sep))
    module_name, _ = os.path.splitext(module_name)
    
    package_name, _ = os.path.splitext(module_name)

    with fileinput.input(files=(file), inplace=True) as fi:
        for line in fi:
            match = IMPORT_ALL_RE.match(line)
            try:
                if not match:
                    raise ValueError()

                indentation = len(line) - len(line.lstrip())
                sys.stdout.write(
                    line[:indentation] +
                    import_all_string(match.group(1),
                                    package=package_name))
            except:
                sys.stdout.write(line)

    return module_name


def main():
    files = glob.glob('./**/*.py', recursive=True)
    executor = ProcessPoolExecutor()
    for module_name in executor.map(process_file, files):
        print(module_name)

if __name__ == '__main__':
    main()
