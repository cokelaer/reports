REPORT
=======


This is a simple package to easily build HTML reports using JINJA templating. 

HTML Table of CSV files can be included (based on Pandas and some code from
report package itself).

The is only one simple template provided with **report**, which is called
**generic** and can be found in the source code in ./share/data/templates/generic and new templates can be provided in reports. 

Here is an example that creates an empty report::

    from report import Report
    r = Report()
    r.create_report(onweb=True)

The next step is for you to copy the templates in a new directory, edit them
and fill the :attr:`jinja` attribute to fulfil your needs::

    from report import Report
    r = Report("myreport_templates")

    r.jinja["section1"] = "<h1></h1>" 

    r.create_report() 




