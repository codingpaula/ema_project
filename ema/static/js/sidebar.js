/* $(function() {
  $('.topicButton').click(function() {
    var topicColorIndex = $(this).children('input').attr('id');
    console.log(topicColorIndex);
    if ($(this).children('input').is(":checked")) {
      $(this).css('background-color', TopicData.data[topicColorIndex].color);
      $(this).children('a').css('color', '#fff');
    } else {
      $(this).css('background-color', '#f1f1f1');
      $(this).children('a').css('color', TopicData.data[topicColorIndex].color);
    }
  });
}); */


/*var jsonData = {
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

}*/
