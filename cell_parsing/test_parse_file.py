# coding: utf-8

# ##Test
#
# - 1
# - 2
#

#to_file _imports.py

from IPython.html.widgets import *
from IPython.html import widgets
import numpy as np
from bokeh.plotting import *
output_notebook()

#to_file sin_func.py


def dscatter(color="black",alpha=1.0):
    def decorator(fn):
       def make_plot(*args, **kwargs):
            x,y = fn(*args, **kwargs)
            scatter(x, y, color=color, tools="pan,wheel_zoom,box_zoom,reset,resize")
            show()
       return make_plot
    return decorator


@dscatter(color="red",alpha=0.7)
def sin_func():
    N = 100
    x = np.linspace(0, 4*np.pi, N)
    y = np.sin(x)
    return x,y

sin_func()


if __name__ == '__main__':
    sin_func()

