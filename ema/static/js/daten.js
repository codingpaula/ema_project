// TODO displayed?
var TopicData = {
  data: {},
  /*
    verarbeite Daten, die Django liefert
    id = {'color': .., 'name': ..}
  */
  start: function(topics) {
    // workaround um data zu editieren
    var that = this;
    topic_data.topics.forEach(function(topic) {
      var id = topic.id;
      that.data[id] = {
        'color': topic.color,
        'name': topic.topic_name
      };
    });
  }
}

// name, id, topic, due, importance, description
var TaskData = {
  data: [],
  /*
    verarbeite Daten, die Django liefert
    index : {
      'x': relatives Datum,
      'y': Wichtigkeit,
      'id': ID,
      'name': ..,
      'description': ..,
      'topic': Topic ID
    }
  */
  start: function(tasks) {
    // workaround um data zu editieren
    var that = this;
    var index = 0;
    task_data.objects.forEach(function(task) {
      that.data[index] = {
        // TODO Berechnung?
        'x': task.due_date,
        'y': task.importance,
        'id': task.id,
        'name': task.task_name,
        'description': task.task_description,
        'topic': task.topic
      };
      index += 1;
    });
  }
};


// default settings that can be changed per user
var SettingsData = {};
