# -*- coding: utf-8 -*-
__revision__ = "$Id$" # for the SVN Id
import sys
import os
from setuptools import setup, find_packages
import glob

_MAJOR               = 0
_MINOR               = 0
_MICRO               = 1
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {"main": ("Thomas Cokelaer", "cokelaer@gmail.com")},
    'version': version,
    'license' : 'GPL',
    'download_url' : ['http://pypi.python.org/pypi/report'],
    'url' : ["http://pythonhosted.org/report/"],
    'description': "A simple HTML report builder based on jinja" ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : ['HTML', 'table', 'jinja', 'report'],
    'classifiers' : [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics']
    }

# files in share/data
datadir = os.path.join('share','data')
datafiles = [(datadir, [f for f in glob.glob(os.path.join(datadir, '*'))])]


setup(
    name             = "report",
    version          = version,
    maintainer       = metainfo['authors']['main'][0],
    maintainer_email = metainfo['authors']['main'][1],
    author           = metainfo['authors']['main'][0],
    author_email     = metainfo['authors']['main'][1],
    long_description = open("README.rst").read(),
    keywords         = metainfo['keywords'],
    description      = metainfo['description'],
    license          = metainfo['license'],
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    download_url     = metainfo['download_url'],
    classifiers      = metainfo['classifiers'],

    # package installation
    package_dir = {'':'src'},
    packages = ["report"],

    install_requires = ["easydev", "pandas", "colormap"],

    # uncomment if you have share/data files
    #data_files = datafiles,

    #use_2to3 = True, # causes issue with nosetests
)
