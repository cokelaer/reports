changelog
===============

:version 0.3.1: Fix License and RTD 
:version 0.3.0: Fix call to easydev.precision for the case where data contains
    infinite/nan values
:version 0.2.1: Fix warnings due to division by zero; add some tests
:version 0.2.0: outer class of the table is always used (no check of a minimal size)
:version 0.1.9: Add new option to not create the sub directories (css/js...)
:version 0.1.8: fix another bug/typo in js_list
:version 0.1.7: fix bug/typo in js_list
:version 0.1.6: extra js can now be added (similarly to the CSS)

:version 0.1.5: get_dependencies now accept an input package argument (defaults
    to reports)

:version 0.1.4: HTMLTable sorting is confused with the content of scientific
    notation that are used as characters. The user should change te dataframe
    types but we change the type is we can from object to float.

    Second fix is related to CSS. We were already including CSS from reports/resources/css, 
    from a list of user-defined CSS. We now also include CSS found in the JINJA
    searchpath provided by the user.

:version 0.1.3:

* change css_path into   extra_css_list parameter
* change parameter names to allow to get all set of jinja files instead of just one.

:version 0.1.2:

* refactoring: moved ./src/reports into ./reports and mv ./share into ./reports
  this was done to ease the modifications of setup.py so that the templates
  can be accessed to using python setupy install or develop mode AND pip
  install.

:version 0.1.1:

* added jquery javascript

:version 0.1: 

* first functional release used in sequana project and gdsctools project
