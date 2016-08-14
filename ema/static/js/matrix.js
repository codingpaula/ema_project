// Helfer-Funktionen
// Verteilung
/*
	@param dots = Array mit schon eingetragenen Punkten (Objekte)
		dot = {
			date: x,
			imp: y
		}
	@param newDot_x = x-Koordinate(date) des neuen Punktes
	@param newDot_y = y-Koordinate(importance) des neuen Punktes
*/
function doubles(dots, newDot_x, newDot_y) {
	var newDot = {x: newDot_x, y: newDot_y};
	dots.forEach(function(oldDot) {
		if(liesIn(oldDot, newDot)) {
			// TODO wie kann erkannt werden dass die neue Stelle nicht auch schon
			// besetzt ist?
			newDot.x += 10;
			newDot.y += 10;
		}
	});
	// Rückgabe von 2 Werten nicht erlaubt, dadurch als Objekt
	//var dot = {
	//	'date': newDot_x,
	//	'imp': newDot_y
	//};
	return newDot;
}

// left oder bottom property gegeben, bis wo liegen die Punkte ganz oder
// teilweise aufeinander
function liesIn(takenDot, newDot) {
	if (takenDot.x - 42 < newDot.x && takenDot.x + 42 > newDot.x) {
		if (takenDot.y - 32 < newDot.y && takenDot.y + 32 > newDot.y) {
			return true;
		}
	} else {
		return false;
	}
}

// Date in lesbare Zahlen umwandeln
function formatDate(date) {
	var datum = new Date(date);
	return datum.toDateString();
}

// Wichtigkeit richtig anzeigen
function formatImp(imp) {
	if (imp == 0) return "not important";
	if (imp == 1) return "less important";
	if (imp == 2) return "important";
	if (imp == 3) return "very important";
}

// structure:
// https://css-tricks.com/how-do-you-structure-javascript-the-module-pattern-edition/
var s,
Matrix = {
	settings: {
		//canvas: $('canvas'),
		//drawing: document.getElementById('ema').getContext("2d"),
		width: $('#dots').width(),
		height: $('#dots').height()
	},
	init: function() {
		s = this.settings;
	},
	drawAxes: function(field, width, height) {
		// untere Ecke y-Wert
		var uEy = height-25;
		// rechte Ecke x-Wert
		var rEx = width-20;
		// Mitte y-Achse
		var my = (height-20-25)/2 + 20;
		// Mitte x-Achse
		var mx = (width-25-20)/2 + 25;

		// Spitze senkrechter Pfeil
		field.moveTo(25,20);
		// zur untere Ecke
		field.lineTo(25,uEy);
		field.stroke();
		// zur rechten Spitze
		field.lineTo(rEx,uEy);
		field.stroke();

		// Pfeil oben linke Seite
		field.moveTo(15,30);

		field.lineTo(25,20);
		field.stroke();

		// Pfeil oben rechte Seite
		field.lineTo(35,30);
		field.stroke();

		// Pfeil rechts oberer Teil
		field.moveTo(rEx-10,uEy-10);
		// zur rechten Spitze
		field.lineTo(rEx,uEy);
		field.stroke();
		// zum Pfeil rechts unterer Teil
		field.lineTo(rEx-10,uEy+10);
		field.stroke();

		// Mittellinie y-Achse
		field.moveTo(25,my);
		field.lineTo(rEx,my);
		field.stroke;

		// Mittellinie x-Achse
		field.moveTo(mx,20);
		field.lineTo(mx,uEy);
		field.stroke();

		// Beschriftung x-Achse
		field.font = "20px Arial";
		// field.textAlign = "center";
		field.fillText("U R G E N T", width/2-50, height);

		field.save();
		field.translate(width/2,height/2);
		// Beschriftung y-Achse
		field.font = "20px Arial";
		field.rotate(-Math.PI/2);
		field.translate(height/2,-width/2);
		field.fillText("I M P O R T A N T", -height/2-50, 15);

		field.restore();
	},
	drawTasks: function(taskData, topicData, width, height) {
		// gets correct data
		// console.log(taskData);
		// console.log(topicData);
		$('#dots').empty();
		// how to find out if tasks are on the same spot
		var that = this;
		var taken = [];
		// Hilfsvariablen
		// durch alle übergebenen Aufgaben
		taskData.forEach(function(task){
			console.log("start dot");
			var colorIndex = task.topic;
			if(topicData[colorIndex]['displayed'] == false) {

			} else {
				// check überschneidungen
				var dot = {x: task.x, y: task.y};
				//console.log("x vor doubles: "+task.x);
				//var dot = doubles(taken, task.x, task.y);
				//task.x = dot.x;
				//task.y = dot.y;
				//console.log("coordinates are: x - "+task.x+", y - "+task.y);
				var topicColor = topicData[colorIndex]['color'];
				// eigentlichen Punkt kreieren und zeichnen
				that.drawDot(task, topicColor);
				// Array mit bereits gezeichneten Koordinaten
				taken.push(dot);
			}
		});
	},
	// Hilfsfunktion um ausführlichere Detailanzeige zu zeichnen
	drawDot: function(task, color) {
		// eigentlicher Kreis mit task_id in entsprechender Farbe des Topics
		var clickHandler = "location.href='/matrix/"+task.id+"/taskediting/'"
		var taskItem = $('<div/>', {
			class: 'dot',
			id: task.id,
			css: {
				left: task.x,
				bottom: task.y,
				borderColor: color,
				width: 7,
				height: 7
			},
			onclick: clickHandler
		});
		$('#dots').append(taskItem);
		// div mit den Aufgaben-Details
		var name = $('<p/>', {
			class: 'dotName',
			css: {
				color: color
			},
			text: task.name
		})
		var label = $('<div/>', {
			class: 'hoverField'
		});
		// Titel
		var title = $('<h1/>', {
			class: 'dotLabel',
			text: task.name
		});
		// weitere Attribute
		var attributes = [$('<p/>', {
			text: 'due: '+formatDate(task.due_date)
		}),
		$('<p/>', {
			text: 'Importance: '+formatImp(task.importance)
		})];
		// anfügen, Erkennung des richtigen Kreises über task_id
		$('#dots').children('#'+task.id).append(name);
		$('#dots').children('#'+task.id).append(label);
		$('#dots').children('#'+task.id).children('.hoverField').append(title, attributes);
	},
	deleteDot: function(task) {
		$('#dots').children('#'+task.id).remove();
		console.log("i removed "+task.id);
	}
};

var Sidebar = {
	// Topic-Button steuert Matrix
	button: function(topic_id) {
		// Attribut displayed, um zu tracken, was an und was aus ist
		// nach neu-laden allerdings wieder alles an
		if(TopicData.data[topic_id].displayed == true) {
			// falls gerade noch an --> click macht aus
			// Farbenaenderung, aussen Topic-Color, innen Hintergrund
			$('button#'+topic_id).css('background-color', '#f1f1f1');
			$('button#'+topic_id).css('color', TopicData.data[topic_id].color);
			// update data, um Button-States zu tracken
			TopicData.data[topic_id].displayed = false;
			// update die Matrix
			Matrix.drawTasks(TaskData.data, TopicData.data, s.width, s.height);
		} else {
			// Farben zuruecktauschen
			$('button#'+topic_id).css('background-color', TopicData.data[topic_id].color);
			$('button#'+topic_id).css('color', '#fff');
			// Button-Status updaten
			TopicData.data[topic_id].displayed = true;
			// Matrix neu laden
			Matrix.drawTasks(TaskData.data, TopicData.data, s.width, s.height);
		}
	},
	// alle Topic-Button ein oder ausschalten
	allButton: function() {
		// die Hintergrundfarbe des Buttons entscheidet, welche Aktion vorgenommen
		// wird, da auch User anhand dieser die eine oder ander Aktion erwartet
		// Hintergrund grau --> alles ausschalten
		if($('button#all').css('background-color') == 'rgb(192, 192, 192)') {
			for(button in TopicData.data) {
				// jeder Button, der an ist, wird ausgeklickt
				if(TopicData.data[button].displayed == true) {
						$('button#'+button).click();
				}
			}
			// die Buttonfarbe des All-Buttons wird geaendert
			$('button#all').css('background-color', '#eee');
		} else {
			for(button in TopicData.data) {
				// alle Buttons, die aus sind, werden angemacht
				if(TopicData.data[button].displayed == false) {
						$('button#'+button).click();
				}
			}
			// Farbe updaten
			$('button#all').css('background-color', 'rgb(192, 192, 192)');
		}
	},
	// Moeglichkeit die Topics zu editieren
	editTopics: function() {
		// wieder Unterscheidung anhand von Hintergrundfarbe des Edit-Buttons
		if($('button#editTopics').css('background-color') == 'rgb(192, 192, 192)') {
			for(button in TopicData.data) {
				// alle onclick-Attribute der Buttons auf die Topic-Anzeige lenken
				var glyphi = $('<span/>', {
					class: 'glyphicon glyphicon-pencil pull-right'
				});
				$('button#'+button).append(glyphi);
				$('button#'+button).attr('onclick', "location.href='/matrix/"+button+"'");
			}
			// All-Button ausmachen
			$('button#all').attr('onclick', '');
			// Hintergrund anpassen
			$('button#editTopics').css('background-color', '#eee');
		} else {
			for(button in TopicData.data) {
				// zurueck zu der Button beeinflusst die Matrix
				$('button#'+button).find('span').remove();
				$('button#'+button).attr('onclick', 'Sidebar.button(button)');
			}
			// All-Button geht wieder
			$('button#all').attr('onclick', 'Sidebar.allButton()');
			// Hintergrund anpassen
			$('button#editTopics').css('background-color', 'rgb(192, 192, 192)');
		}
	}
};
