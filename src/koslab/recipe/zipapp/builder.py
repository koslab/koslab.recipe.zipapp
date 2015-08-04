import argh
import tempfile
import urllib
import shutil
import os
import sys

DEV_CFG = """
[buildout]
extensions = mr.developer
parts = 
    omelette
    builder
sources-dir = dev
auto-checkout = *

[sources]
koslab.recipe.zipapp = git https://github.com/koslab/koslab.recipe.zipapp

[omelette]
recipe = collective.recipe.omelette
eggs = 
    %(egg)s

[builder]
recipe = koslab.recipe.zipapp
omelette-part = omelette
main-function = %(main_function)s
output-file = %(output_file)s

"""

BUILDOUT_CFG = """
[buildout]
extensions = mr.developer
parts = 
    omelette
    builder

[omelette]
recipe = collective.recipe.omelette
eggs = 
    %(egg)s

[builder]
recipe = koslab.recipe.zipapp
omelette-part = omelette
main-function = %(main_function)s
output-file = %(output_file)s

"""

@argh.arg('module', help='Name of egg from pypi')
@argh.arg('-o', '--output', help='Output filename (default = module.pyz)')
@argh.arg('-m', '--main', help='Main function (default = module:main)')
@argh.arg('-d', '--development', help='Use development version of buildout',
            default=False)
def build(module, *args, **kwargs):
    cwd = os.getcwd()
    tempdir = tempfile.mkdtemp()
    output_file = kwargs['output'] or (module + '.pyz')
    main_function = kwargs['main'] or (module + ':main')
    with open(os.path.join(tempdir, 'buildout.cfg'), 'w') as f:
        buildout_cfg = DEV_CFG if kwargs['development'] else BUILDOUT_CFG
        f.write(buildout_cfg % {
            'egg': module,
            'main_function': main_function,
            'output_file': output_file,
        })
    with open(os.path.join(tempdir, 'bootstrap.py'), 'w') as f:
        print "Downloading: http://downloads.buildout.org/2/bootstrap.py"
        b = urllib.urlopen('http://downloads.buildout.org/2/bootstrap.py').read()
        f.write(b)
    os.chdir(tempdir)
    print "Initializing Buildout"
    os.system(sys.executable + ' bootstrap.py')
    print "Starting build"
    os.system('./bin/buildout -vvv')
    shutil.copy(output_file, cwd)
    print "Cleanup"
    shutil.rmtree(tempdir)
    print "Written %s" % output_file

parser = argh.ArghParser()
parser.add_commands([build])

def main():
    parser.dispatch()        
