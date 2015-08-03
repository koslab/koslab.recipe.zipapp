import argh
import tempfile
import urllib
import shutil
import os
import sys

BUILDOUT_CFG = """
[buildout]
extensions = mr.developer
parts = 
    omelette
    builder
sources-dir = dev
auto-checkout = *

[sources]
koslab.recipe.zipapp = git https://github.com/kagesenshi/koslab.recipe.pyzipper

[omelette]
recipe = collective.recipe.omelette
eggs = 
    %(egg)s

[builder]
recipe = koslab.recipe.zipapp
omelette-part = omelette
entry-point = %(entry_point)s
output-file = %(output_file)s

"""

@argh.arg('module', help='Name of egg from pypi')
@argh.arg('-o', '--output', help='Output filename')
@argh.arg('-m', '--main', help='Main function')
def build(module, *args, **kwargs):
    cwd = os.getcwd()
    tempdir = tempfile.mkdtemp()
    output_file = kwargs['output'] or (module + '.pyz')
    with open(os.path.join(tempdir, 'buildout.cfg'), 'w') as f:
        f.write(BUILDOUT_CFG % {
            'egg': module,
            'entry_point': kwargs['main'],
            'output_file': output_file,
        })
    with open(os.path.join(tempdir, 'bootstrap.py'), 'w') as f:
        b = urllib.urlopen('http://downloads.buildout.org/2/bootstrap.py').read()
        f.write(b)
    os.chdir(tempdir)
    os.system(sys.executable + ' bootstrap.py')
    os.system('./bin/buildout -vvv')
    shutil.copy(output_file, cwd)
    print "Written %s" % output_file

parser = argh.ArghParser()
parser.add_commands([build])

def main():
    parser.dispatch()        
