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
  getTasks: function(tasks, urgent_axis) {
    // workaround um data zu editieren
    var that = this;
    that.data = [];
    tasks.forEach(function(task) {
      index = task.id;
      that.data[index] = {
        'x': getDateCoordinate(task.due_date, urgent_axis),
        'y': getImportanceCoordinate(task.importance),
        'due_date': task.due_date,
        'importance': task.importance,
        'id': task.id,
        'name': task.task_name,
        'description': task.task_description,
        'topic': task.topic,
        'cluster': undefined
      };
    });
    console.log(that.data);
  },
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
// unten 60
// links 50
// oben 680
// rechts 880
function dateCoordinate(date) {
  // aktuelles Datum, Grenze 2 Monate = 5184000000
  var coordinate = 1-(Date.parse(date) - Date.parse(today))/5184000000;
	// damit Aufgaben, die noch zu weit links sind nicht verschwinden
  if (coordinate < 0) return 50;
	// damit ueberfaellige Aufgaben nicht verschwinden
	if (coordinate > 1) return (s.width-20);
  else {
    if(coordinate*s.width < 50) return 50;
    else return coordinate*s.width;
  }
}

function getDateCoordinate(date, urgent_axis) {
  TWOMONTHS = [2, 7, 15, 60];
  ONEMONTH = [1, 4, 7, 30];
  FOURMONTHS = [4, 14, 30, 120];
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
  // 12.08.16 bis 24.09.16
  var distance2today = Date.parse(date) - Date.parse(today)
  var oneDay = 24*60*60*1000;
  // weiter weg als 2 Monate (matrix maximum) --> linke seite
  if (distance2today > abstand[3]*oneDay) return 50;
  // ueberfaellige aufgaben verschwinden nicht, sondern am rechten rand
  if (distance2today <= 0) return s.width-10;
  // assure: everything is between 2 months and today!
  if (distance2today <= abstand[0]*oneDay) {
    // ein viertel der Achse
    // beinhaltet 2 tage
    var coordinate = (((1-(distance2today/(abstand[0]*oneDay)))/4)+0.75)*(s.width-70)+50;
    return coordinate;
  }
  if (distance2today <= abstand[1]*oneDay) {
    var bet0and1 = 1-(distance2today - (abstand[0]*oneDay))/((abstand[1]-abstand[0])*oneDay);
    var axespart = bet0and1/4;
    var verschieben = axespart+0.5;
    var coordinate = (verschieben*(s.width-70))+50;
    return coordinate;
  }
  if (distance2today <= abstand[2]*oneDay) {
    var bet0and1 = 1-(distance2today - (abstand[1]*oneDay))/((abstand[2]-abstand[1])*oneDay);
    var axespart = bet0and1/8;
    var verschieben = axespart+0.375;
    var coordinate = (verschieben*(s.width-70))+50;
    return coordinate;
  }
  if (distance2today <= abstand[3]*oneDay) {
    var bet0and1 = 1-(distance2today - (abstand[2]*oneDay))/((abstand[3]-abstand[2])*oneDay);
    var axespart = bet0and1/8*3;
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
