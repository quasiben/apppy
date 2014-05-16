import functools
import bokeh.plotting as bpl
from IPython.html import widgets
from IPython.display import display, display_html, HTML

def selectable(arg, widget, props, source_viewable=True):
    kwargs = {arg:widget(**props)}
    def decorator(thing):
        if not isinstance(thing, Selector):
            s = Selector(thing, source_viewable=source_viewable)
            s.kwargs.update(kwargs)
            return s
        else:
            thing.kwargs.update(kwargs)
            return thing
    return decorator

class Selector(object):
    def __init__(self, function, source_viewable=True):
        self.kwargs = {}
        self._base_function = function
        if source_viewable:
            def make_function():
                @functools.wraps(self._base_function)
                def new_function(*args, **kwargs):
                    if kwargs.get("SourceCode", False):
                        self.view_source()
                    else:
                        non_source_args = {
                            x:y for x,y in kwargs.iteritems() 
                            if x != "SourceCode"
                        }
                        self._base_function(*args, **non_source_args)
                return new_function
            self.function = make_function()
            self.kwargs.update({"SourceCode":False})
        else:
            self.function = self._base_function
                    
    def __call__(self):
        widgets.interact(self.function, **self.kwargs)

    def view_source(self):
        """
    	Encapsulates the action of taking an object and producing a
    	displayed window of that object's source code. Relies on the
    	inspect module and thus has any of the same limitations in
    	terms of what source it can retrieve.
    	"""
        import inspect
    	from pygments import highlight
    	from pygments.lexers import PythonLexer
    	from pygments.formatters import HtmlFormatter
    	
    	# Tools for parsing the displayed code.
    	lexer = PythonLexer()
    	formatter = HtmlFormatter()
    	
    	# Configure the popup window that will hold the code.
    	popup = widgets.PopupWidget()
    	popup.description = "Source Code Widget"
    	popup.button_text = "Render Window"
    	popup.set_css({'width':'580px', 'height':'350px'}, selector='modal')
    	
    	# Configure the body features of the window.
    	modal_body = widgets.ContainerWidget()
    	modal_body.set_css('overflow-y', 'scroll', 'overflow-x')
    	
    	# Get and format source code into an HTML widget.
        code_to_get = (
            self._base_function.original_func_code 
            if hasattr(self._base_function, "original_func_code")
            else self._base_function.func_code
        )
    	source_code = inspect.getsource(code_to_get)
    	highlighted_source = highlight(source_code, lexer, formatter)
    	html_widget = widgets.HTMLWidget(value=highlighted_source)
    	html_widget.set_css({'width': '580px',
    	                     'height': '350px',
    	                     'font-size':'100px',
    	                     'overflow-y':'true', 
    	                     'scroll':'true'})
    	
    	# Apply the HTML widget to the body of the window.
    	modal_body_label = html_widget
    	modal_body.children = [modal_body_label]
    	
    	# Notify the popup window that is controls the HTML widget.
    	popup.children = [html_widget]
    	display(popup)

def code_wraps(function):
    def decorator(other_function):
        other_function.original_func_code = function.func_code
        return other_function
    return decorator

# Bokeh scatter plot
def dscatter(color="black", tools="pan,wheel_zoom,box_zoom,reset,resize"):
    def decorator(fn):
        @code_wraps(fn)
        def make_plot(*args, **kwargs):
            x,y = fn(*args, **kwargs)
            bpl.scatter(x, y, color=color, tools=tools)
            bpl.show()
        return make_plot
    return decorator

# Basic HTML table from Pandas.
def dtable():
   def decorator(fn):
       @code_wraps(fn)
       def make_table(*args, **kwargs):
           display_html(fn(*args, **kwargs).to_html(), raw=True)
       return make_table
   return decorator
