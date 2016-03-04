# coding=utf-8
# -*- python -*-
#
#  This file is part of report software
#
#  Copyright (c) 2016
#  All rights reserved
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the BSD 3-Clause License.
#  See accompanying file LICENSE.txt distributed with this software
#
##############################################################################
"""Base classes to create HTML reports easily"""
import os
import shutil
import glob

import easydev
import pandas as pd
from jinja2.environment import Environment
from jinja2 import FileSystemLoader

from .htmltable import HTMLTable

__all__ = ['Report']


def _get_report_version():
    # cannot use from report import version since it imports the module (not the
    # package) due to identical name. Hopefully, easydev does help:        
    deps = easydev.get_dependencies('reports')
    index = [x.project_name for x in deps].index('reports')
    return deps[index].version


class Report(object):
    """A base class to create HTML pages

    The :class:`Report` is used to 

    #. fetch Jinja templates and css from a user directory (by default a generic
       set of files is provided as an example
    #. fetch the CSS and images
    #. hold variables and contents within a dictionary (:attr:`jinja`)
    #. Create the HTML document in a local directory.

    ::

        from report import Report
        r = Report()
        r.create_report(onweb=True)

    The next step is for you to copy the templates in a new directory, edit them
    and fill the :attr:`jinja` attribute to fulfil your needs::


        from report import Report
        r = Report("myreport_templates")
        r.jinja["section1"] = "<h1></h1>" 
        r.create_report() 


    """

    def __init__(self, template_path="generic",
                filename='index.html', directory='report',
                 overwrite=True, verbose=True, 
                template_filename='index.html', css_path="generic"):
        """.. rubric:: Constructor

        :param filename: default to **index.html**
        :param directory: defaults to **report**
        :param overwrite: default to True
        :param verbose: default to True
        :param dependencies: add the dependencies table at the end of the
            document if True.
        :param template_filename: entry point of the jinja code
        :param template_path: where to find the templates. If not provided, uses
            the generic version

        a template directory should contain a set of jinja files including
        *template_filename*. 
        """

        self._directory = directory
        self._filename = filename

        # This contains the sections and their names when
        # method add_section is used
        self.sections = []
        self.section_names = []

        #: flag to add dependencies
        self.add_dependencies = False

        self.title = 'Title undefined'

        # For jinja2 inheritance, we need to use the environment
        # to indicate where are the parents' templates
        if template_path  == "generic":
            share_path = easydev.get_shared_directory_path('reports')
            self.template_path = os.sep.join([share_path, 'data', 
                'templates', "generic"])
        else:
            self.template_path = template_path

        self.env = Environment()
        self.env.loader = FileSystemLoader(self.template_path)

        # use template provided inside gdsctools
        self.template = self.env.get_template(template_filename)

        self.jinja = {
                'time_now': self.get_time_now(),
                "title": self.title,
                'dependencies': self.get_table_dependencies().to_html(),
                "report_version": _get_report_version()
                }

        self._to_create = ['images', 'css', 'js',]

        self._init_report()

    def _get_filename(self):
        return self._filename
    def _set_filename(self, filename):
        self._filename = filename
    filename = property(_get_filename, _set_filename,
        doc="The filename of the HTML document")

    def _get_directory(self):
        return self._directory
    def _set_directory(self, directory):
        self._directory = directory
    directory = property(_get_directory, _set_directory,
            doc="The directory where to save the HTML document")

    def _get_abspath(self):
        return self.directory + os.sep + self.filename
    abspath = property(_get_abspath,
            doc="The absolute path of the document (read only)")

    def _init_report(self):
        """create the report directory and return the directory name"""
        self.sections = []
        self.section_names = []
        # if the directory already exists, print a warning

        try:
            if os.path.isdir(self.directory) is False:
                print("Created directory {}".format(self.directory))
                os.mkdir(self.directory)
            # list of directories created in the constructor
            for this in self._to_create:
                try:
                    os.mkdir(self.directory + os.sep + this)
                except:
                    pass # already created ?
        except Exception:
            pass
        finally:
            temp_path = easydev.get_shared_directory_path("reports")

            filenames = glob.glob(self.template_path + os.sep + "*css")
            filenames += glob.glob(os.sep.join([temp_path, "data", "css", "*css"]))

            for filename in filenames:
                target = os.sep.join([self.directory, 'css' ])
                if os.path.isfile(target) is False:
                    shutil.copy(filename, target)
            for filename in ['sorttable.js', 'highlight.pack.js']:
                target = os.sep.join([self.directory, 'js', filename ])
                if os.path.isfile(target) is False:
                    filename = easydev.get_share_file("reports", "data",
                        filename)
                    shutil.copy(filename, target)


    def to_html(self):
        self.jinja['time_now'] = self.get_time_now()
        return self.template.render(self.jinja)

    def write(self):
        with open(self.abspath, "w") as fh:
            data = self.to_html()
            fh.write(data)

    def onweb(self):
        """Open the HTML document in a browser"""
        from easydev import onweb
        onweb(self.abspath)

    def create_report(self, onweb=True):
        self.write()
        if onweb is True:
            self.onweb()

    def get_time_now(self):
        """Returns a time stamp"""
        import datetime
        import getpass
        username = getpass.getuser()
        # this is not working on some systems: os.environ["USERNAME"]
        timenow = str(datetime.datetime.now())
        timenow = timenow.split('.')[0]
        msg = '<div class="date">Created on ' + timenow
        msg += " by " + username +'</div>'
        return msg

    def get_table_dependencies(self):
        """Returns dependencies of the pipeline as an HTML/XML table

        The dependencies are the python dependencies as returned by
        pkg_resource module.

        """
        dependencies = easydev.get_dependencies("reports")
        # TODO: Could re-use new method in HTMLTable for adding href
        # but needs some extra work in the add_href method.
        names = [x.project_name for x in dependencies]
        versions = [x.version for x in dependencies]
        links = ["""https://pypi.python.org/pypi/%s""" % p for p in names]
        df = pd.DataFrame({
            'package': ["""<a href="%s">%s</a>""" % (links[i], p)
                for i, p in enumerate(names)],
            'version': versions})
        table = HTMLTable(df, name="dependencies", escape=False)
        table.sort('package')
        return table
