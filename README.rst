REPORTS
=========


This is a simple package to easily build HTML reports using JINJA templating. 

Installation
--------------

:: 

    pip install reports

Example
----------

Here is a simple example that creates an empty report based on the **generic**
templates provided::

    from report import Report
    r = Report()
    r.create_report(onweb=True)

The next step is for you to copy the templates in a new directory, edit them
and fill the *jinja* attribute to fulfil your needs::

    from report import Report
    r = Report("myreport_templates")

    r.jinja["section1"] = "<h1></h1>" 

    r.create_report() 


See Sphinx documentation for more details

