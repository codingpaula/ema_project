(function(exports) {

// Helpers
// ------------

function htmlId(obj) {
  return obj._id.split('/').join('_');
}

var arr = [];
var today = new Date();

function dateCoordinate(date) {
  // aktuelles Datum, Grenze 2 Monate = 5184000000
  var coordinate = (Date.parse(date) - Date.parse(today))/5184000000;
  // damit Aufgaben nicht verschwinden
  if (coordinate < 0) return 0;
  else return coordinate;
}

// Collections you wanna dance with
// ------------

var collections = {
  "items": {
    enter: function(items) {
      items.each(function(item) {

        var dot = $('<div class="dot" id="'+htmlId(item)+'"><div class="label">'+item.properties.task_name+'</div></div>')
                     .css('left', dateCoordinate(item.properties.due_date)*$('#canvas').width())
                     .css('bottom', item.properties.importance*$('#canvas').height())
                     .css('width', 1)
                     .css('height', 1);
        $('#canvas').append(dot);
        arr.push(Date.parse(item.properties.due_date));
        arr.push(dateCoordinate(item.properties.due_date));
      });
      alert(arr);

      // Delegate to update (motion tweening fun)
      _.delay(this.collections["items"].update, 200, items);
    },

    update: function(items) {
      items.each(function(item) {
        var cell = $('#'+htmlId(item))
                     .css('left', item.pos.x)
                     .css('bottom', item.pos.y)
                     .css('width', 10)
                     .css('height', 10);
      });
    },

    exit: function(items) {
      items.each(function(i) { $('#'+htmlId(i)).remove() });
    }
  }
};

// Scatterplot Visualization
// ------------

var Scatterplot = Dance.Performer.extend({

  collections: collections,

  initialize: function(options) {
    this.data["items"] = options.items;

  },

  layout: function(properties) {
    var that = this;

    // Prepare scales
    function aggregate(p, fn) {
      var values = _.map(that.data["items"].objects, function(i) { return i.get(p); });
      return fn.apply(this, values);
    }

    var minX = aggregate(properties[0], Math.min);
    var maxX = aggregate(properties[0], Math.max);

    var minY = aggregate(properties[1], Math.min);
    var maxY = aggregate(properties[1], Math.max);

    function x(val) {
      return (((val-minX) * $('#canvas').width()) / (maxX-minX));
    }

    function y(val) {
      return (((val-minY) * $('#canvas').height()) / (maxY-minY));
    }

    // Apply layout
    this.data["items"].each(function(item, key, index) {
      item.pos = {
        x: x(item.get(properties[0])),
        y: y(item.get(properties[1]))
      };
    });
  },

  update: function(items, properties) {
    this.data["items"] = items;
    this.layout(properties);
    this.refresh();
  }
});

exports.Scatterplot = Scatterplot;

})(window);
