Reports documentation
===========================

|version|, |today|

.. image:: https://badge.fury.io/py/reports.svg
    :target: https://pypi.python.org/pypi/reports

.. image:: https://travis-ci.org/cokelaer/reports.svg?branch=master
    :target: https://travis-ci.org/cokelaer/reports

.. image::  https://coveralls.io/repos/github/cokelaer/reports/badge.svg?branch=master
    :target: https://coveralls.io/github/cokelaer/reports?branch=master 

.. image:: http://readthedocs.org/projects/reports/badge/?version=latest
    :target: http://reports.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

:Python version: Python 2.7, 3.4 and 3.5
:documentation: `On readthedocs <http://reports.readthedocs.org/>`_
:Issues: Please fill form on `On github <https://github.com/cokelaer/reports/issues>`_





Reports is a  simple Python package that provides tools to create HTML
documents. It is based on a set of JINJA templates and a class called
**Report**. In addition tools such as HTMLTable can help in the creation of HTML
table to be included in the report.

The package relies on Pandas for the HTML table creation, as shown in the
example below. 


We provide a simple JINJA example (stored with the pacakge in
./share/data/templates/generic directory) and we let the users design their own
templates.

This is used in `GDSCTools <http://gdsctools.readthedocs.org>`_ and 
`Sequana <http://sequana.readthedocs.org>`_ packages.



Usage
======

Example
----------------
Here below, we show the code used to create this `example <_static/report/index.html>`_.

::

    # We will create a Report and insert an HTML table in it
    from reports import Report, HTMLTable

    # Let us create some data. It will be a HTML table built using Pandas
    # but you could create the HTML table code yourself.
    import pandas as pd

    # create a dataframe to play with. Note that there is a numeric column
    # In addition, there is a column (Entry name) that will be transformed into URLs
    df = pd.DataFrame({
        "Entry name":["ZAP70_HUMAN", "TBK1_HUMAN"], 
        "Entry": ["P43403", "Q9UHD2"], 
        "Frequency": [0.5,0.9]})

    # From reports, we convert the dataframe into a HTMLTable
    table = HTMLTable(df)

    # a numeric column can be colorized
    table.add_bgcolor('Frequency', cmap="copper")

    # part of URLs can be added to the content of a column
    table.add_href('Entry', url='http://uniprot.org/uniprot/', suffix="")
    html = table.to_html()

    # Create a generic report. It has a set of tags that can be filled
    # using the **jinja** attribute.
    r = Report("generic")

    # set the **summary** tag with the HTML code of the table
    r.jinja['summary'] = html

    # Generate and show the report
    r.create_report(onweb=True)


See the results in `example <_static/report/index.html>`_


Using your own JINJA template
-------------------------------------

Create a directory called **test** and add a file called **index.html**

Add this code::

    <h1> {{ title }} </h1>
    <p> Number of reads : {{ reads }} </p>

Now, create your HTML files::

    from reports import Report
    report = Report("test")
    report.jinja['title'] = 'Simple Example'
    report.jinja['reads'] = "123456"
    report.create_report(onweb=True)


Issues
===========

Please fill bug report in https://github.com/cokelaer/reports

Contributions
================

Please join https://github.com/cokelaer/reports

.. toctree::
    :numbered:
    :maxdepth: 1

    references.rst

Changelog
=============

.. toctree::

    Changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
