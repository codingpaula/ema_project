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
    that.data = [];
    var index = 0;
    tasks.forEach(function(task) {
      console.log("daten.js-Schleife");
      that.data[index] = {
        // TODO Berechnung?
        'x': newDateCoordinate(task.due_date),
        'y': importanceCoordinate(task.importance),
        'due_date': task.due_date,
        'importance': task.importance,
        'id': task.id,
        'name': task.task_name,
        'description': task.task_description,
        'topic': task.topic
      };
      index += 1;
      help = task.task_name;
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
	// damit ueberfaellige Aufgaben nicht verschwinden
	if (coordinate > 1) return (s.width-20);
  else {
    if(coordinate*s.width < 50) return 50;
    else return coordinate*s.width;
  }
}

function newDateCoordinate(date) {
  // millisecond from task due date to this moment
  // 12.08.16 bis 24.09.16
  var distance2today = Date.parse(date) - Date.parse(today)
  // whole x-axis = 1 with 1 at the cross with the y-axis
  // 1----------------------------------0
  // 2M---------------------------------0
  // 2M----------------2W---------------0
  // 2M---6W---1M--3W--2W---1W---2d--1d-0
  // 1----------------0,5---------------0
  // millisekunden auf 1 bis 0 runtergekuerzt
  var one2zero = distance2today/2*30*24*60*60*1000;
  var matrixDimension = 2*30*24*60*60*1000;
  var oneDay = 24*60*60*1000;
  // weiter weg als 2 Monate (matrix maximum) --> linke seite
  if (distance2today > 60*oneDay) return 50;
  // ueberfaellige aufgaben verschwinden nicht, sondern am rechten rand
  if (distance2today <= 0) return s.width-10;
  // assure: everything is between 2 months and today!
  if (distance2today <= 2*oneDay) {
    // ein viertel der Achse
    // beinhaltet 2 tage
    var coordinate = (((1-(distance2today/(2*oneDay)))/4)+0.75)*(s.width-70)+50;
    return coordinate;
  }
  if (distance2today <= 7*oneDay) {
    var bet0and1 = 1-(distance2today - (2*oneDay))/(5*oneDay);
    var axespart = bet0and1/4;
    var verschieben = axespart+0.5;
    var coordinate = (verschieben*(s.width-70))+50;
    return coordinate;
  }
  if (distance2today <= 15*oneDay) {
    var bet0and1 = 1-(distance2today - (7*oneDay))/(8*oneDay);
    var axespart = bet0and1/8;
    var verschieben = axespart+0.375;
    var coordinate = (verschieben*(s.width-70))+50;
    return coordinate;
  }
  if (distance2today <= 60*oneDay) {
    var bet0and1 = 1-(distance2today - (15*oneDay))/(45*oneDay);
    var axespart = bet0and1/8*3;
    var verschieben = axespart;
    var coordinate = (verschieben*(s.width-70))+50;
    return coordinate;
  }
}

// Wichtigkeitskoordinate
function importanceCoordinate(imp) {
	return imp/4*s.height + 60;
}

// -----------------------------------------------------------------------------
// default settings that can be changed per user
var SettingsData = {};
