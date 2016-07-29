$(function() {
  var topicsArray = button.update(topic_data.topics);
  $('.topicButton').click(function() {
    var topicColor = $(this).children('input').attr('id');
    if ($(this).children('input').is(":checked")) {
      $(this).css('background-color', topicColor);
      $(this).children('a').css('color', '#fff');
    } else {
      $(this).css('background-color', '#f1f1f1');
      $(this).children('a').css('color', topicColor);
    }
  });
});

var buttons = {};
var jsonData = {
    "topics": {
      start: function(topics) {
        topic_data.topics.forEach(function(topic) {
          var a = topic.topic_name;
          buttons[a] = topic.color;
        });
      },
      delete: function(topic) {

      }
    }
}
var data = {};
var button = {
  data: data,
  update: function(topics) {
    this.data["topics"] = jsonData["topics"].start(topics);
  }
  /*
  onClick: function() {
    this.changeValue()
  }
  changeValue: function() {

  }
  colorChange: function() {

  }
  reloadMatrix: function() {

  }
  */
}
