# This package may contain traces of nuts

import zc.buildout
import os
import logging

import os
import zipfile

MAINSCRIPT = """#!/usr/bin/env python
import sys
import %(module)s

if __name__ == '__main__':
    sys.exit(%(module)s.%(method)s())
"""

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path, followlinks=True):
        for f in files:
            filename = os.path.join(root, f)
            ziph.write(filename)

class ZipApp(object):
    def __init__(self, buildout, name, options):
        self.name, self.options = name, options
        self.buildout = buildout
        self.main_function = options['main-function']
        self.parts_directory = os.path.join(
            buildout['buildout']['parts-directory'], self.name
        )
        if not os.path.exists(self.parts_directory):
            os.mkdir(self.parts_directory)

        options['eggs'] = buildout[options['omelette-part']]['eggs']
        self.omelette_directory = os.path.join(
            buildout['buildout']['parts-directory'], options['omelette-part']
        )

        self.output_file = os.path.join(
            buildout['buildout']['directory'], options['output-file']
        )

    def install(self):
        zipf = zipfile.ZipFile(self.output_file, 'w')
        os.chdir(self.omelette_directory)
        zipdir('.', zipf)
        os.chdir(self.parts_directory)
        with open('__main__.py', 'w') as f:
            module, method = self.main_function.strip().split(':')
            f.write(MAINSCRIPT % {'module': module, 'method': method})
        zipf.write('__main__.py')
        zipf.close()
        return [self.output_file]

    def update(self):
        pass
