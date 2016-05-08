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

    def __init__(self,
                 searchpath=None,
                 filename='index.html',
                 directory='report',
                 overwrite=True,
                 verbose=True,
                 template_filename='index.html',
                 extra_css_list=[],
                 extra_js_list=[],
                init_report=True):
        """.. rubric:: Constructor


        :param searchpath: where to find the jina templates. 
            If not provided, uses the generic template
        :param filename: output filename (default to **index.html**)
        :param directory: defaults to **report**
        :param overwrite: default to True
        :param verbose: default to True
        :param template_filename: entry point of the jinja code
        :param extra_css_list: where to find the extra css 
        :param extra_js_list: where to find the extra css 
        :param bool init_report: init the report that is create 
            the directories to store css and JS.

        """
        self.verbose = verbose
        self._directory = directory
        self._filename = filename
        self.extra_css_list = extra_css_list
        self.extra_js_list = extra_js_list

        # This contains the sections and their names
        # Not used yet but could be in jinja templating
        self.sections = []
        self.section_names = []

        #: flag to add dependencies
        self.add_dependencies = False

        # For jinja2 inheritance, we need to use the environment
        # to indicate where are the parents' templates
        if searchpath  is None:
            thispath = easydev.get_package_location('reports')
            thispath += os.sep + "reports"
            thispath += os.sep + "resources"
            self.searchpath = os.sep.join([thispath, 'templates', "generic"])
        else:
            # path to the template provided by the user 
            self.searchpath = searchpath

        # The JINJA environment
        # TODO check that the path exists
        self.env = Environment()
        self.env.loader = FileSystemLoader(self.searchpath)

        # input template file 
        self.template = self.env.get_template(template_filename)

        # This dictionary will be used to populate the JINJA template
        self.jinja = {
            'time_now': self.get_time_now(),
            "title": "Title to be defined",
            'dependencies': self.get_table_dependencies().to_html(),
            "report_version": _get_report_version()
        }

        # Directories to create 
        self._to_create = ['images', 'css', 'js',]

        # Create directories and stored css/js/images
        if init_report:
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
                if self.verbose:
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
            # Once the main directory is created, copy files required
            temp_path = easydev.get_package_location("reports")
            temp_path += os.sep + "reports" + os.sep + "resources"

            # Copy the CSS from reports/resources/css
            filenames = glob.glob(os.sep.join([temp_path, "css", "*.css"]))

            # If there are CSS in the directory with JINJA templates, use them
            # as well
            filenames += glob.glob(os.sep.join([self.searchpath, '*.css']))


            # In addition, the user may also provide his own CSS as a list
            filenames += self.extra_css_list
            for filename in filenames:
                target = os.sep.join([self.directory, 'css' ])
                if os.path.isfile(target) is False:
                    shutil.copy(filename, target)

            # We copy all javascript from reports resources
            for filename in ['sorttable.js', 'highlight.pack.js', "jquery-1.12.3.min.js"]:
                target = os.sep.join([self.directory, 'js', filename ])
                if os.path.isfile(target) is False:
                    filename = os.sep.join([temp_path, "javascript", filename])
                    shutil.copy(filename, target)
            for filename in self.extra_js_list:
                basename = os.path.basename(filename)
                target = os.sep.join([self.directory, 'js', basename ])
                if os.path.isfile(target) is False:
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

    def get_table_dependencies(self, package="reports"):
        """Returns dependencies of the pipeline as an HTML/XML table

        The dependencies are the python dependencies as returned by
        pkg_resource module.

        """
        dependencies = easydev.get_dependencies(package)
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
