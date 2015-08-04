from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='koslab.recipe.zipapp',
      version=version,
      description="Python ZipApp Packager",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='buildout zipapp',
      author='Izhar Firdaus',
      author_email='izhar@kagesenshi.org',
      url='http://github.com/koslab/koslab.recipe.zipapp/',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['koslab', 'koslab.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'argh',
          # -*- Extra requirements: -*-
      ],
      entry_points={
        'zc.buildout': ['default = koslab.recipe.zipapp.buildout_recipe:ZipApp'],
        'console_scripts': [
            'zipapp = koslab.recipe.zipapp.builder:main'
        ]
      }
      )
