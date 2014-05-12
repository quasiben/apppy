require(["widgets/js/widget"], function(WidgetManager){
    
    // Define the DatePickerView
    var DatePickerView = IPython.DOMWidgetView.extend({
        render: function(){
            this.$el.addClass('widget-hbox-single'); /* Apply this class to the widget container to make
                                                        it fit with the other built in widgets.*/
            // Create a label.
            this.$label = $('<div />')
                .addClass('widget-hlabel')
                .appendTo(this.$el)
                .hide(); // Hide the label by default.
            
            // Create the date picker control.
            this.$date = $('<input />')
                .attr('type', 'date')
                .appendTo(this.$el);
        },
        
        update: function() {
            
            // Set the value of the date control and then call base.
            this.$date.val(this.model.get('value')); // ISO format "YYYY-MM-DDTHH:mm:ss.sssZ" is required
            
            // Hide or show the label depending on the existance of a description.
            var description = this.model.get('description');
            if (description == undefined || description == '') {
                this.$label.hide();
            } else {
                this.$label.show();
                this.$label.text(description);
            }
            
            return DatePickerView.__super__.update.apply(this);
        },
        
        // Tell Backbone to listen to the change event of input controls (which the HTML date picker is)
        events: {"change": "handle_date_change"},
        
        // Callback for when the date is changed.
        handle_date_change: function(event) {
            this.model.set('value', this.$date.val());
            this.touch();
        },
    });
    
    // Register the DatePickerView with the widget manager.
    WidgetManager.register_widget_view('DatePickerView', DatePickerView);
});