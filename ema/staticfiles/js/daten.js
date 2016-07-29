// name, id, color, displayed (boolean)
var TopicData = {
  data: [],
  start: function(topics) {
    topic_data.topics.forEach(function(topic) {
      var a = topic.topic_name;
      data[a] = topic.color;
    });
  }
};


// name, id, topic, due, importance, description
var TaskData = {};


// default settings that can be changed per user
var SettingsData = {};
