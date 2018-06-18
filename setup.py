#!/usr/bin/env python
from setuptools import setup

setup(name='LeAnBundle',
      version='1.0',
      description='Learning Analytics Bundle Toolkit',
      author='Daniel Schiffner and Marcel Ritter',
      author_email='schiffner@studiumdigitale.uni-frankfurt.de',
      url='https://github.com/dschiffner/lean-bundle/',
      license='MIT',
      packages=['lean_bundle'],
      scripts=['bin/from-xapi', 'bin/lean-dump', 'bin/lean-mining']
      )