# coding=utf-8
# -*- python -*-
#
#  This file is part of GDSCTools software
#
#  Copyright (c) 2015 - Wellcome Trust Sanger Institute
#  All rights reserved
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the BSD 3-Clause License.
#  See accompanying file LICENSE.txt distributed with this software
#
#  website: http://github.com/CancerRxGene/gdsctools
#
##############################################################################
"""Base classes to create HTML reports easily"""
import os
import shutil

import easydev
import pandas as pd

from colormap import rgb2hex, cmap_builder
# note that the sorttable javascript is from
# `http://www.kryogenix.org/code/browser/sorttable/
# with an X11 license


__all__ = ['HTMLTable']


class HTMLTable(object):
    """Handler to export dataframe into HTML table.

    Dataframe in Pandas already have a to_html method to export the dataframe
    into a HTML formatted table. However, we provide here a few handy features:

        * Takes each cell in a given column and creates an HTML
          reference in each cell. See :meth:`add_href` method.
        * add an HTML background into cells (numeric content) of
          a given column using different methods (e.g., normalise).
          See :meth:`add_bgcolor`

    ::

        import pandas as pd
        df = pd.DataFrame({'A':[1,2,10], 'B':[1,10,2]})
        from gdsctools import HTMLTable
        html = HTMLTable(df)

    .. note:: similar project exists such as prettytable but could not do
        exactly what we wanted at the time gdsctools was developed.

    .. note:: Could be moved to biokit or easydev package.

    """
    def __init__(self, df, name=None, **kargs):
        """.. rubric:: Constructor


        :param dataframe df: a pandas dataframe to transform into a table
        :param str name: not used yet

        There is an :attr:`pd_options` attribute to reduce the max column
        width or the precision of the numerical values.

        """
        self.df = df.copy() # because we will change its contents possibly
        self.name = name
        self.pd_options = {
                'max_colwidth': -1,
                'precision': 2}

    def to_html(self, index=False, escape=False, header=True,
            collapse_table=True, class_outer="table_outer", **kargs):
        """Return HTML version of the table

        This is a wrapper of the to_html method of the pandas dataframe.

        :param bool index: do not include the index
        :param bool escape: do not escape special characters
        :param bool header: include header
        :param bool collapse_table: long tables are shorten with a scroll bar
        :param kargs: any parameter accepted by
            :meth:`pandas.DataFrame.to_html`

        """
        _buffer = {}
        for k, v in self.pd_options.items():
            # save the current option
            _buffer[k] = pd.get_option(k)
            # set with user value
            pd.set_option(k, v)

        # class sortable is to use the sorttable javascript
        # note that the class has one t and the javascript library has 2
        # as in the original version of sorttable.js
        table = self.df.to_html(escape=escape, header=header, index=index,
                classes='sortable', **kargs)

        # get back to default options
        for k, v in _buffer.items():
            pd.set_option(k, v)

        # We wrap the table in a dedicated class/div nammed table_scroller
        # that users must define.
        return '<div class="%s">' % class_outer + table+"</div>"

    def add_bgcolor(self, colname, cmap='copper', mode='absmax',
            threshold=2):
        """Change column content into HTML paragraph with background color

        :param colname:
        :param cmap: a colormap (matplotlib) or created using
            colormap package (from pypi).
        :param mode: type of normalisation in 'absmax', 'max', 'clip'
            (see details below)
        :param threshold: used if mode is set to 'clip'

        Colormap have values between 0 and 1 so we need to normalised the data
        between 0 and 1. There are 3 mode to normalise the data so far.

        If mode is set to 'absmax', negatives and positives values are
        expected to be found in a range from -inf to inf. Values are
        scaled in between [0,1] X' = (X / M +1) /2. where m is the absolute
        maximum. Ideally a colormap should be made of 3 colors, the first
        color used for negative values, the second for zeros and third color
        for positive values.

        If mode is set to 'clip', values are clipped to a max value (parameter
        *threshold* and values are normalised by that same threshold.

        If mode is set to 'max', values are normalised by the max.

        """
        try:
            # if a cmap is provided, it may be just a known cmap name
            cmap = cmap_builder(cmap)
        except:
            pass

        data = self.df[colname].values

        if len(data) == 0:
            return

        if mode == 'clip':
            data = [min(x, threshold)/float(threshold) for x in data]
        elif mode == 'absmax':
            m = abs(data.min())
            M = abs(data.max())
            M = max([m, M])
            if M != 0:
                data = (data / M + 1)/2.
        elif mode == 'max':
            if data.max() != 0:
                data = data / float(data.max())

        # the expected RGB values for a given data point
        rgbcolors = [cmap(x)[0:3] for x in data]
        hexcolors = [rgb2hex(*x, normalised=True) for x in rgbcolors]

        # need to read original data again
        data = self.df[colname].values
        # need to set precision since this is going to be a text not a number
        # so pandas will not use the precision for those cases:

        def prec(x):
            try:
                # this may fail if for instance x is nan or inf
                x = easydev.precision(x, self.pd_options['precision'])
                return x
            except:
                return x

        data = [prec(x) for x in data]
        html_formatter = '<p style="background-color:{0}">{1}</p>'
        self.df[colname] = [html_formatter.format(x, y)
                for x, y in zip(hexcolors, data)]

    def add_href(self, colname, url=None, newtab=False, suffix=None):
        """

        default behaviour: takes column content and put into::

            <a href={content}.html>content</a>

        This is used to link to local files. If url is provided, you typically
        want to link to an external url where the content is an identifier::

            <a href={url}{content}>content</a>

        Note that in the first case, *.html* is appended but not in the second
        case, which means cell's content should already have the .html
        Also in the second case, a new tab is open whereas in the first case
        the url is open in the current tab.

        .. note:: this api may change in the future.

        """
        if url is not None:
            if suffix is None:
                suffix = ''
            if newtab is False:
                formatter = '<a  alt="{1}" href="{0}{1}{2}">{1}</a>'
            else:
                formatter = '<a target="_blank" alt={1} href="{0}{1}{2}">{1}</a>'
            self.df[colname] = self.df[colname].apply(lambda x:
                    formatter.format(url, x, suffix))
        else:
            if suffix is None:
                suffix = '.html'

            if newtab is False:
                formatter = '<a alt="{1}" href="{0}{2}">{1}</a>'
            else:
                formatter = '<a target="_blank" alt="{1}" href="{0}{2}">{1}</a>'
            self.df[colname] = self.df[colname].apply(lambda x:
                formatter.format(x,x, suffix))

    def sort(self, name, ascending=True):
        # for different pandas implementations
        try:
            self.df.sort_values(by=name, inplace=True, ascending=ascending)
        except:
            self.df.sort(columns=name, inplace=True, ascending=ascending)


