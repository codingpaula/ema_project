// Verarbeitung der von django erhaltenen JSON-Objekte
// Themen
var TopicData = {
  data: [],
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
    that.data = [];
    topics.topics.forEach(function(topic) {
      var id = topic.id;
      that.data[id] = {
        'color': topic.color,
        'name': topic.topic_name,
        'displayed': true,
        'count': 0
      };
    });
  },
  resetCounts: function() {
    var that = this;
    that.data.forEach(function(topic) {
      topic['count'] = 0;
    });
  }
}

// Aufgaben -------------------------------------------------------------------
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
  getTasks: function(tasks, urgent_axis) {
    // workaround um data zu editieren
    var that = this;
    that.data = [];
    tasks.forEach(function(task) {
      index = task.id;
      topic = task.topic;
      that.data[index] = {
        'x': getDateCoordinate(task.due_date, urgent_axis),
        'y': getImportanceCoordinate(task.importance),
        'due_date': task.due_date,
        'importance': task.importance,
        'id': task.id,
        'name': task.task_name,
        'description': task.task_description,
        'duration': task.duration,
        'topic': topic,
        'cluster': undefined
      };
      TopicData.data[topic].count++;
    });
  },
  // bei einer Veraenderung der Matrix-Groesse nur Koordinaten aendern
  updateCoordinates: function(urgent_axis) {
    var that = this;
    that.data.forEach(function(task) {
      task.x = getDateCoordinate(task.due_date, urgent_axis);
      task.y = getImportanceCoordinate(task.importance);
    })
  }
};

// Helfer-Funktionen
// Datumskoordinate herausfinden
// Rahmen min und max:
// unten 60
// links 50
// oben 680
// rechts 880
// params: date: datum, das umgewandelt werden soll
// params: urgent_axis: einstellung wie viele tage auf der achse
var oneDay = 24*60*60*1000;
function getDateCoordinate(date, urgent_axis) {
  var today = new Date();
  // Einteilung Tage pro Phase
  ONEMONTH = [1, 4, 7, 30];
  TWOMONTHS = [2, 7, 15, 60];
  FOURMONTHS = [4, 14, 30, 120];
  // welche einstellung wird verwendet?
  var abstand = [];
  switch(urgent_axis) {
    case 0:
      abstand = ONEMONTH;
      break;
    case 1:
      abstand = TWOMONTHS;
      break;
    case 2:
      abstand = FOURMONTHS;
      break;
    default:
      abstand = TWOMONTHS;
  }
  // millisecond from task due date to this moment
  var distance2today = Date.parse(date) - Date.parse(today);
  // ein Tag in milliseconds
  // weiter weg als matrix maximum --> linke seite
  if (distance2today > abstand[3]*oneDay) return 50;
  // ueberfaellige aufgaben verschwinden nicht, sondern am rechten rand
  if (distance2today <= 0) return s.width-10;
  // assure: everything is between maximum and today!
  if (distance2today <= abstand[0]*oneDay) {
    return calculateDistanceBetween0and1(distance2today, 0, abstand[0], 4, 0.75);
  }
  if (distance2today <= abstand[1]*oneDay) {
    return calculateDistanceBetween0and1(distance2today, abstand[0], abstand[1]-abstand[0], 4, 0.5);
  }
  if (distance2today <= abstand[2]*oneDay) {
    return calculateDistanceBetween0and1(distance2today, abstand[1], abstand[2]-abstand[1], 8, 0.375);
  }
  if (distance2today <= abstand[3]*oneDay) {
    return calculateDistanceBetween0and1(distance2today, abstand[2], abstand[3]-abstand[2], 8*3, 0);
  }
}

// Funktion:
// (1-(x - (block[y]*oneDay))/((block[y+1]-block[y])*oneDay))/block_breite + step_before
// @param: distance = Datum Aufgabe bis jetzt
// @param: abstand = wo beginnt der Abschnitt auf der Zeitachse
// @param: davor = wo endet der Abschnitt auf der Zeitachse
// @param: step_size = wie lang ist der Abschnitt
// @param: teil = wie viel liegt vor dem Abschnitt
function calculateDistanceBetween0and1(distance, abstand, davor, step_size, teil) {
  return (((1-(distance-(abstand*oneDay))/(davor*oneDay))/step_size)+teil)*(s.width-70)+50;
}


// Wichtigkeitskoordinate
function getImportanceCoordinate(imp) {
  // Abstand zur unteren Kante = 100
	return imp/4*s.height + 100;
}
