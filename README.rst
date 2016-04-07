REPORTS
=========

.. image:: https://badge.fury.io/py/reports.svg
    :target: https://pypi.python.org/pypi/reports

.. image:: https://travis-ci.org/cokelaer/reports.svg?branch=master
    :target: https://travis-ci.org/cokelaer/reports

.. image:: https://coveralls.io/repos/github/cokelaer/reports/badge.svg?branch=master
    :target: https://coveralls.io/github/cokelaer/reports?branch=master 

.. image:: http://readthedocs.org/projects/reports/badge/?version=latest
    :target: http://reports.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

:Python version: Python 2.7, 3.4 and 3.5
:Online documentation: `On readthedocs <http://reports.readthedocs.org/>`_
:Issues and bug reports: `On github <https://github.com/cokelaer/reports/issues>`_


This is a simple package to easily build HTML reports using JINJA templating. 

Installation
--------------

:: 

    pip install reports

Example
----------

Here is a simple example that creates an empty report based on the **generic**
templates provided::

    from reports import Report
    r = Report()
    r.create_report(onweb=True)

The next step is for you to copy the templates in a new directory, edit them
and fill the *jinja* attribute to fulfil your needs::

    from report import Report
    r = Report("myreport_templates")

    r.jinja["section1"] = "<h1></h1>" 

    r.create_report() 


See Sphinx documentation for more details

