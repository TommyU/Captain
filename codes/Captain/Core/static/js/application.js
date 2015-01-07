// booting script 
// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

  // Menu Model
  // ----------

  // Our Menu **Todo** model has `name`, `url`, `res_model`, and `state` attributes.
  var Menu = Backbone.Model.extend({
  });

  // Menu Collection
  // ---------------

  // The collection of Menu 
  var MenuList = Backbone.Collection.extend({
    url:'ttp://localhost:8000/api/users/?format=json',

    // Reference to this collection's model.
    model: Menu,

    // We keep the Menus in sequential order, despite being saved by unordered
    // GUID in the database. This generates the next order number for new items.
    nextOrder: function() {
      if (!this.length) return 1;
      return this.last().get('order') + 1;
    },

    // Menus are sorted by their original insertion order.
    comparator: 'order'

  });

  // Create our global collection of **Menus**.
  var Menus = new MenuList;

  // Menu Item View
  // --------------

  // The DOM element for a Menus item...
  var MenuView = Backbone.View.extend({

    el: $("#menu"),

    //... is a list tag.
    tagName:  "li",

    // Cache the template function for a single item.
    template: _.template($('#t_main_menu').html()),

    // The DOM events specific to an item.
    events: {
      "click .menu_item"   : "loadContent",
    },

    // The MenuView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Menu** and a **MenuView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },

    // Re-render the titles of the todo item.
    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },

    // Toggle the `"done"` state of the model.
    loadContent: function() {
      //this.model.toggle();
    },

  });

  // The Application
  // ---------------

  // Our overall **AppView** is the top-level piece of UI.
  var AppView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $("#root"),

    render: function() {

    },


  });

  // Finally, we kick things off by creating the **App**.
  var App = new AppView;

});
