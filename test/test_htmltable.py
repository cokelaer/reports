from reports import HTMLTable
import pandas as pd
from numpy.random import randn


def test_htmltable():

    df = pd.DataFrame({'A':[1,2,10], 'B':[1,10,2]})
    table = HTMLTable(df)
    table.add_bgcolor('A')
    table.sort('B')
    table.to_html()

    # use another mode
    df = pd.DataFrame({'A':[1,2,10], 'B':[1,10,2]})
    table = HTMLTable(df)
    table.add_bgcolor('A', mode='max')

    # test collapse case (needs df>20)
    df = pd.DataFrame({'A':randn(30), 'B':randn(30)})    
    table = HTMLTable(df)
    table.to_html()

    #  test add_bgcolor on empty datra
    df = pd.DataFrame({'A':[]})
    table = HTMLTable(df)
    table.add_bgcolor('A')
    table.to_html()

    #  test url 
    df = pd.DataFrame({'A':[1]})
    html = HTMLTable(df)
    html.add_href("A", url="test")
    assert html.df.ix[0].values[0] == '<a  alt="1" href="test1">1</a>'

    #  test url / newtab
    df = pd.DataFrame({'A':[1]})
    html = HTMLTable(df)
    html.add_href("A", url="test", newtab=True)
    # test url / no url
    html = HTMLTable(df)
    html.add_href("A")
    html = HTMLTable(df)
    html.add_href("A", newtab=True)

def test_wrong_cmap():
    df = pd.DataFrame({'A':[]})
    table = HTMLTable(df)
    table.add_bgcolor('A', cmap='dummy')


def test_clip():
    df = pd.DataFrame({"A":[1,2,3,4]})
    html = HTMLTable(df)
    html.add_bgcolor("A", mode="clip", threshold=2)
    assert "FFC77E" in html.df.ix[2].values[0]
    assert "FFC77E" in html.df.ix[3].values[0]

