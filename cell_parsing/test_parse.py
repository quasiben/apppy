#cell
from bokehapp import *


#cell
@selectable("trig", widgets.RadioButtonsWidget, {"values":["sin", "cos", "tan"]})
@selectable("freq", widgets.DropdownWidget, {"values":[1, 2, 3, 4]})
@dscatter("red")
def periodic_func(freq=4, trig="sin"):

    N = 100
    x = np.linspace(0, freq*np.pi, N)
    y = getattr(np, trig)(x)
    return x,y

periodic_func()



#cell
@selectable("trig", widgets.RadioButtonsWidget, {"values":["sin", "cos", "tan"]})
@selectable("freq", widgets.DropdownWidget, {"values":[1, 2, 3, 4]})
@selectable("freq", widgets.IntSliderWidget, {"values":[1, 2, 3, 4]})
@dscatter("red")
def periodic_func_log(freq=4, trig="sin"):

    N = 100
    x = np.logspace(0, freq*np.pi, N)
    y = getattr(np, trig)(x)
    return x,y

periodic_func_log()


#cell
