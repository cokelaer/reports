Reports documentation
===========================

|version|, |today|


Reports is a  simple Python package that provides tools to create HTML
documents. It is based on a set of JINJA templates and a class called
**Report**. In addition tools such as HTMLTable can help in the creation of HTML
table to be included in the report.

The package relies on Pandas for the HTML table creation, as shown in the
example below. 


We provide a simple JINJA example (stored with the pacakge in
./share/data/templates/generic directory) and we let the users design their own
templates.

This is used in GDSCTools and Sequoia packages

Usage
======


::

    # We will create a Report and insert an HTML table in it
    from reports import Report, HTMLTable

    # Let us create some data we wish to add as a table in our report
    import pandas as pd

    # create a dataframe to play with. It contains a colum with numeric values
    # that will be used later. In addition, there is a column (Entry name)
    # that will be replaced with URLs
    df = pd.DataFrame({
        "Entry name":["ZAP70_HUMAN", "TBK1_HUMAN"], 
        "Entry": ["P43403", "Q9UHD2"], 
        "Frequency": [0.5,0.9]})


    table = HTMLTable(df)
    # a numeric column can be colorized
    table.add_bgcolor('Frequency')
    # part of URLs can be added to the content of a column
    table.add_href('Entry', url='http://uniprot.org/uniprot/', suffix="")
    html = table.to_html()


    # Create a generic report. It has a set of tags that can be filled
    # using the **jinja** attribute
    r = Report("generic")

    # set the **summary** tag with the HTML code of the table
    r.jinja['summary'] = html

    # Generate and show the report
    r.create_report(onweb=True)


See the results in `example <_static/report/index.html>`_




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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
