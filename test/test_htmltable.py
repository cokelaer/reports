from reports import HTMLTable




def test_htmltable():

    import pandas as pd
    df = pd.DataFrame({'A':[1,2,10], 'B':[1,10,2]})
    from reports import HTMLTable
    table = HTMLTable(df)


    table.add_bgcolor('A')
    table.sort('B')
    table.to_html()


    

