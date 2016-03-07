from reports import HTMLTable
import pandas as pd



def test_htmltable():

    df = pd.DataFrame({'A':[1,2,10], 'B':[1,10,2]})
    table = HTMLTable(df)


    table.add_bgcolor('A')
    table.sort('B')
    table.to_html()


    

