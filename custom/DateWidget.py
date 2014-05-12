import inspect
import IPython
import os.path as ospath
from dateutil import parser
from IPython.html import widgets
from IPython.utils.traitlets import Unicode

# Enure class's underlying javascript is loaded.

class DateWidget(widgets.DOMWidget):
    _view_name = Unicode('DatePickerView', sync=True)
    value = Unicode(sync=True)
    description = Unicode(sync=True)
    def __init__(self, **kwargs):
        # Before creating the class, ensure Javascript is loaded.
        cur_file = ospath.dirname(inspect.getfile(inspect.currentframe()))
        widget_source = ospath.join(cur_file, 
                                    "javascript", 
                                    self.__class__.__name__) + ".js"
        
        with open(widget_source, 'r') as js_code:
            IPython.get_ipython().run_cell_magic(
                'javascript', 
                '', 
                js_code.read()
            )

        self.validate = widgets.CallbackDispatcher()
        super(DateWidget, self).__init__(**kwargs)        
    
    # This function automatically gets called by the traitlet machinery when
    # value is modified because of this function's name.
    def _value_changed(self, name, old_value, new_value):
        
        # Parse the date time value.
        try:
            parsed_date = parser.parse(new_value)
            parsed_date_string = parsed_date.strftime("%Y-%m-%d")
        except:
            parsed_date_string = ''
        
        # Set the parsed date string if the current date string is different.
        if old_value != new_value:

            print hasattr(self, 'validate')


            valid = self.validate(parsed_date)
            if valid in (None, True):
                self.value = parsed_date_string
            else:
                self.value = old_value
                self.send_state() # The traitlet event won't fire since the value isn't changing.
                                  # We need to force the back-end to send the front-end the state
                                  # to make sure that the date control date doesn't change.
