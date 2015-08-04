.. contents::

Introduction
============

Support for executing python zip files was added in Python2.6_, and in
Python3.6, emphasis was added through the zipapp_ module.

This module contains a buildout recipe and a command line utility to help 
package Python applications into a zipapp, complete with its setup.py 
dependencies. 

One of the use-case for this module is for building complex Hadoop MapReduce 
job in Python that relies in many dependencies. The zipapp can be distributed
easily to Hadoop nodes for execution, or packaged as a script for Hive's
``TRANSFORM`` function

.. _Python2.6: https://docs.python.org/2/whatsnew/2.6.html?highlight=__main__.py#other-language-changes

.. _zipapp: https://docs.python.org/dev/library/zipapp.html

Command Line Tool
==================

Installation
-------------

::

    pip install koslab.recipe.zipapp

Usage
------

The following example packages Spotify's Luigi_ daemon as a zipapp.

::

    # Creates luigi zipapp as luigi.egg
    zipapp build luigi -m luigi.cmdline:luigid -o luigi.egg

    # Run luigid
    python luigi.egg

.. _Luigi: http://luigi.readthedocs.org/en/stable/


Buildout Recipe
================

Configuration
--------------

This recipe depends on ``collective.recipe.omelette`` from Plone.

buildout.cfg::

    [buildout]
    parts = 
        omelette
        zipapp

    [omelette]
    recipe = collective.recipe.omelette
    eggs = 
        # Eggs to be included into the zipapp
        MyApp

    [zipapp]
    recipe = koslab.recipe.zipapp
    omelette-part = omelette
    main-function = MyApp.main:main
    output-file = MyApp.pyz

Output file will be created everytime buildout is run
