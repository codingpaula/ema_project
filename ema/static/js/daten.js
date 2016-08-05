// TODO displayed?
var TopicData = {
  data: {},
  /*
    verarbeite Daten, die Django liefert
    id = {
      'color': ..,
      'name': ..,
      'displayed': true or false
    }
  */
  getTopics: function(topics) {
    // workaround um data zu editieren
    var that = this;
    topic_data.topics.forEach(function(topic) {
      var id = topic.id;
      that.data[id] = {
        'color': topic.color,
        'name': topic.topic_name,
        'displayed': true
      };
    });
  }
}

// -----------------------------------------------------------------------------
// name, id, topic, due, importance, description
var TaskData = {
  data: [],
  /*
    verarbeite Daten, die Django liefert
    index : {
      'x': relatives Datum als Koordinate,
      'y': Wichtigkeit als Koordinate,
      'due_date': richtiges Datum,
      'importance': Wichtigkeit,
      'id': ID,
      'name': ..,
      'description': ..,
      'topic': Topic ID
    }
  */
  getTasks: function(tasks) {
    // workaround um data zu editieren
    var that = this;
    var index = 0;
    task_data.objects.forEach(function(task) {
      that.data[index] = {
        // TODO Berechnung?
        'x': dateCoordinate(task.due_date),
        'y': importanceCoordinate(task.importance),
        'due_date': task.due_date,
        'importance': task.importance,
        'id': task.id,
        'name': task.task_name,
        'description': task.task_description,
        'topic': task.topic
      };
      index += 1;
    });
  }
};

// Helfer-Funktionen
// Datumskoordinate herausfinden
var today = new Date();
// unten 60
// links 50
// oben 680
// rechts 880
function dateCoordinate(date) {
  // aktuelles Datum, Grenze 2 Monate = 5184000000
  var coordinate = 1-(Date.parse(date) - Date.parse(today))/5184000000;
	// damit Aufgaben, die noch zu weit links sind nicht verschwinden
  if (coordinate < 0) return 50;
	// damit überfällige Aufgaben nicht verschwinden
	if (coordinate > 1) return (s.width-20);
  else {
    if(coordinate*s.width < 50) return 50;
    else return coordinate*s.width;
  }
}

// Wichtigkeitskoordinate
function importanceCoordinate(imp) {
	return imp/4*s.height + 60;
}

// -----------------------------------------------------------------------------
// default settings that can be changed per user
var SettingsData = {};
