import bokeh.plotting as bpl
from IPython.html import widgets
from IPython.display import display_html

class Selector(object):
    def __init__(self, function):
        self.kwargs = {}
        self.function = function
    def __call__(self):
        widgets.interact(self.function, **self.kwargs)

def selectable(arg, widget, props):
    kwargs = {arg:widget(**props)}
    def decorator(thing):
        if not isinstance(thing, Selector):
            s = Selector(thing)
            s.kwargs.update(kwargs)
            return s
        else:
            thing.kwargs.update(kwargs)
            return thing
    return decorator

# Bokeh scatter plot
def dscatter(color="black", tools="pan,wheel_zoom,box_zoom,reset,resize"):
    def decorator(fn):
        def make_plot(*args, **kwargs):
            x,y = fn(*args, **kwargs)
            bpl.scatter(x, y, color=color, tools=tools)
            bpl.show()
        return make_plot
    return decorator

# Basic HTML table from Pandas.
def dtable():
   def decorator(fn):
       def make_table(*args, **kwargs):
           display_html(fn(*args, **kwargs).to_html(), raw=True)
       return make_table
   return decorator
