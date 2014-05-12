import pandas
import datetime
import dateutil
import numpy as np
import bokeh.plotting as bpl
from IPython.html import widgets
from IPython.display import display_html
from plot_decorators import selectable, dscatter, dtable
from custom.DateWidget import DateWidget
bpl.output_notebook()

#################
# Example usage #
#################

@selectable("trig", widgets.RadioButtonsWidget, {"values":["sin", "cos", "tan"]})
@selectable("freq", widgets.DropdownWidget, {"values":[1, 2, 3, 4]})
@selectable("date", DateWidget, {"value":"2012-12-31"})
@dscatter("red")
def periodic_func(freq=4, trig="sin", date=None):
    print date
    N = 100
    x = np.linspace(0, freq*np.pi, N)
    y = getattr(np, trig)(x)
    return x,y 
 
periodic_func()



# Control a DataFrame as a table.
@selectable("nrows", widgets.RadioButtonsWidget, {"values":[5, 10, 15, 20]})
@selectable("ncols", widgets.DropdownWidget, {"values":[1, 2, 3, 4]})
@dtable()
def pandas_table(nrows=10, ncols=3):
    return pandas.DataFrame(np.random.randn(nrows, ncols))

#pandas_table()


# Control aggregations of a table.
@selectable("nrows",   
            widgets.RadioButtonsWidget, 
            {"values":[5, 10, 15, 20]})

@selectable("groupby", 
            widgets.SelectWidget, 
            {"values":['A', 'B', 'C', 'D']})

@selectable("agg_op",  
            widgets.SelectWidget, 
            {"values":['sum', 'mean', 'median', 'min', 'max', 'var']})

@dtable()
def agg_table(nrows=20, groupby=None, agg_op='sum'):
    np.random.seed(42)
    groupby = ['A'] if groupby is None else groupby
    data = pandas.DataFrame(
        np.random.randint(4, size=(nrows, 4)), 
        columns=['A', 'B', 'C', 'D']
    )
    data['value'] = 10*np.random.randn(nrows)
    display_html(data.to_html(), raw=True)
    return data.groupby(groupby).agg({"value":agg_op})

#agg_table()
