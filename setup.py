# -*- coding: utf-8 -*-
__revision__ = "$Id$" # for the SVN Id
import sys
import os
from setuptools import setup, find_packages
import glob

_MAJOR               = 0
_MINOR               = 3
_MICRO               = 1
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {"main": ("Thomas Cokelaer", "cokelaer@gmail.com")},
    'version': version,
    'license' : 'LGPL',
    'download_url' : ['http://pypi.python.org/pypi/reports'],
    'url' : ["http://github.com/cokelaer/reports/"],
    'description': "Quickly create HTML reports using a set of JINJA templates" ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : ['HTML', 'table', 'jinja', 'report', 'reports'],
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


setup(
    name             = "reports",
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

    zip_safe=False,
    # package installation
    packages = ["reports", "reports.resources"],
    include_package_data = True,
    package_data = {"reports.resources": ['javascript/*', 'templates/generic/*', 'css/*']},

    install_requires = ["easydev", "pandas", "colormap", "jinja2"],
)
