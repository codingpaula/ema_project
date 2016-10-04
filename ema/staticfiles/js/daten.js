// Verarbeitung der von django erhaltenen JSON-Objekte
// Themen
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
    topics.topics.forEach(function(topic) {
      var id = topic.id;
      that.data[id] = {
        'color': topic.color,
        'name': topic.topic_name,
        'displayed': true,
        'count': 0
      };
    });
    console.log(that.data);
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
var today = new Date();
// Rahmen min und max:
// unten 60
// links 50
// oben 680
// rechts 880
// params: date: datum, das umgewandelt werden soll
// params: urgent_axis: einstellung wie viele tage auf der achse
function getDateCoordinate(date, urgent_axis) {
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
  var distance2today = Date.parse(date) - Date.parse(today)
  // ein Tag in milliseconds
  var oneDay = 24*60*60*1000;
  // weiter weg als matrix maximum --> linke seite
  if (distance2today > abstand[3]*oneDay) return 50;
  // ueberfaellige aufgaben verschwinden nicht, sondern am rechten rand
  if (distance2today <= 0) return s.width-10;
  // assure: everything is between maximum and today!
  if (distance2today <= abstand[0]*oneDay) {
    // 1 = abstand[0]+today, 0 = today
    // wo liegt die Aufgabe zwischen diesen beiden?
    var bet0and1 = 1-(distance2today/(abstand[0]*oneDay))
    // wird auf einem viertel der achse angezeigt
    // 0 bis 0,25
    var axespart = bet0and1/4;
    // verschiebung nach rechts
    // 0,75 bis 1
    var verschieben = axespart+0.75;
    // eigentliche Koordinate berechnen
    var coordinate = verschieben*(s.width-70)+50;
    return coordinate;
  }
  if (distance2today <= abstand[1]*oneDay) {
    // 1 = abstand[1]+today, 0 = abstand[0]+today
    // 0 bis 1
    var bet0and1 = 1-(distance2today - (abstand[0]*oneDay))/((abstand[1]-abstand[0])*oneDay);
    // viertel der achse
    // 0 bis 0,25
    var axespart = bet0and1/4;
    // 0,5 bis 0,75
    var verschieben = axespart+0.5;
    var coordinate = (verschieben*(s.width-70))+50;
    return coordinate;
  }
  if (distance2today <= abstand[2]*oneDay) {
    // 1 = abstand[2]+today, 0 = abstand[1]+today
    // 0 bis 1
    var bet0and1 = 1-(distance2today - (abstand[1]*oneDay))/((abstand[2]-abstand[1])*oneDay);
    // achtel der achse
    // 0 bis 0,125
    var axespart = bet0and1/8;
    // 0,375 bis 0,5
    var verschieben = axespart+0.375;
    var coordinate = (verschieben*(s.width-70))+50;
    return coordinate;
  }
  if (distance2today <= abstand[3]*oneDay) {
    // 1 = abstand[3]+today, 0 = abstand[2]+today
    // 0 bis 1
    var bet0and1 = 1-(distance2today - (abstand[2]*oneDay))/((abstand[3]-abstand[2])*oneDay);
    // drei achtel der achse
    // 0 bis 0,375
    var axespart = bet0and1/8*3;
    // muss nicht verschoben werden
    var verschieben = axespart;
    var coordinate = (verschieben*(s.width-70))+50;
    return coordinate;
  }
}

// Wichtigkeitskoordinate
function getImportanceCoordinate(imp) {
  // Abstand zur unteren Kante = 100
	return imp/4*s.height + 100;
}
