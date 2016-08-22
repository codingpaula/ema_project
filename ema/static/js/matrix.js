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
function doubles(dots, newDot) {
	var versorgt = false;
	dots.forEach(function(oldDot) {
		if(liesIn(oldDot, newDot)) {
			console.log('newDot: '+newDot.id+', oldDot: '+oldDot.id);
			// TODO wie kann erkannt werden dass die neue Stelle nicht auch schon
			// besetzt ist?
			var cluster_id = oldDot.id;
			if (Matrix.clusters.hasOwnProperty(cluster_id) && versorgt == false) {
				console.log('add to old cluster');
				Matrix.clusters[cluster_id]['included'].push(newDot.id);
				versorgt = true;
			} else if (versorgt == false){
				console.log('new cluster');
				var newCluster = {
					'id': oldDot.id,
					'x': oldDot.x,
					'y': oldDot.y,
				 	'included': [oldDot.id, newDot.id]
				}
				Matrix.clusters[cluster_id] = newCluster;
				versorgt = true;
			}
		}
	});
	return versorgt;
}

// left oder bottom property gegeben, bis wo liegen die Punkte ganz oder
// teilweise aufeinander
function liesIn(takenDot, newDot) {
	if (takenDot.x - 10 < newDot.x && takenDot.x + 10 > newDot.x) {
		if (takenDot.y - 10 < newDot.y && takenDot.y + 10 > newDot.y) {
			return true;
		}
	} else {
		return false;
	}
	return false;
}

// Date in lesbares Format umwandeln
function formatDate(date) {
	var datum = new Date(date);
	var jahr = datum.getFullYear();
	var month_number = datum.getMonth();
	var monat = "";
	switch(month_number) {
		case 0:
			monat = "Januar"; break;
		case 1:
			monat = "Februar"; break;
		case 2:
			monat = "März"; break;
		case 3:
			monat = "April"; break;
		case 4:
			monat = "Mai"; break;
		case 5:
			monat = "Juni"; break;
		case 6:
			monat = "Juli"; break;
		case 7:
			monat = "August"; break;
		case 8:
			monat = "September"; break;
		case 9:
			monat = "Oktober"; break;
		case 10:
			monat = "November"; break;
		case 11:
			monat = "Dezember"; break;
	}
	var tag = datum.getDate();
	var stunden = datum.getHours();
	var min = datum.getMinutes();
	// bei den Minuten und Stunden fehlt wenn sie einstellig sind die erste 0
	if (stunden < 10) {
		if (min < 10) {
			return tag+". "+monat+" "+jahr+", 0"+stunden+":0"+min;
		}
		return tag+". "+monat+" "+jahr+", 0"+stunden+":"+min;
	} else if (min < 10) {
		return tag+". "+monat+" "+jahr+", "+stunden+":0"+min;
	}
	return tag+". "+monat+" "+jahr+", "+stunden+":"+min;
}

// Wichtigkeit richtig anzeigen
function formatImp(imp) {
	var stars = $('<div/>', {
		class: 'starDiv'
	});
	var full_star = $('<span/>', {
		class: 'glyphicon glyphicon-star'
	});
	var empty_star = $('<span/>', {
		class: 'glyphicon glyphicon-star-empty'
	});
	stars.append(full_star.clone());
	if (imp == 0) {
		stars.append(empty_star.clone());
		stars.append(empty_star.clone());
		stars.append(empty_star.clone());
		return stars;
	}
	if (imp == 1) {
		stars.append(full_star.clone());
		stars.append(empty_star.clone());
		stars.append(empty_star.clone());
		return stars;
	}
	if (imp == 2) {
		stars.append(full_star.clone());
		stars.append(full_star.clone());
		stars.append(empty_star.clone());
		return stars;
	}
	if (imp == 3) {
		stars.append(full_star.clone());
		stars.append(full_star.clone());
		stars.append(full_star.clone());
		return stars;
	}
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
	// has an x and an y value, created when two dots are drawn at the same spot
	clusters: [],
	/*
	cluster-index = task_id
		'id': same id as the first task
		'x': x value of cluster,
		'y': y value of cluster,
		'included': list of included dots
	*/
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
		$('#dots').empty();
		// how to find out if tasks are on the same spot
		var that = this;
		var taken = [];
		// Hilfsvariablen
		// durch alle übergebenen Aufgaben
		taskData.forEach(function(task){
			var colorIndex = task.topic;
			if(topicData[colorIndex]['displayed'] == false) {
				// don't display dot when sidebar setting says so
			} else {
				// check überschneidungen
				var dot = {id: task.id, x: task.x, y: task.y};
				//if (doubles(taken, dot)) {
				//	console.log('should draw cluster');
				//} else {
					var topicColor = topicData[colorIndex]['color'];
					// eigentlichen Punkt kreieren und zeichnen
					that.drawDot(task, topicColor);
					// Array mit bereits gezeichneten Koordinaten
				//}
				taken.push(dot);
			}
		});
		console.log(taken);
		that.drawCluster();
	},
	// Hilfsfunktion um ausführlichere Detailanzeige zu zeichnen
	drawDot: function(task, color) {
		// eigentlicher Kreis mit task_id in entsprechender Farbe des Topics
		var clickHandler = function(){
			$('#ajaxEditTask').data = $(this).attr('id');
		};
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
		taskItem.attr('data-toggle', 'modal');
		taskItem.attr('data-target', '#ajaxModal');
		taskItem.attr('data-task', task.id);
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
		var trimmed_description = "";
		if (task.description.length > 40) {
			trimmed_description = task.description.substring(0, 40)+"...";
		} else {
			trimmed_description = task.description;
		}
		var attributes = [
			$('<p/>', {
				text: trimmed_description,
				css: {
					fontStyle: 'italic'
				}
			}),
			$('<p/>', {
				text: formatDate(task.due_date)
			})
		];
		// anfügen, Erkennung des richtigen Kreises über task_id
		$('#dots').children('#'+task.id).append(name);
		$('#dots').children('#'+task.id).append(label);
		$('#dots').children('#'+task.id).children('.hoverField').append(title, attributes, formatImp(task.importance));
	},
	drawCluster: function() {
		var that = this;
		console.log(that.clusters);
		that.clusters.forEach(function(cluster) {
			console.log('x: '+cluster.x);
			console.log('y: '+cluster.y);
			console.log('drawing '+cluster.id);
			var taskItem = $('<div/>', {
				class: 'dot',
				id: cluster.id,
				css: {
					left: cluster.x,
					bottom: cluster.y,
					borderColor: 'black',
					backgroundColor: 'grey',
					width: 7,
					height: 7
				}
			});
			var clusterDot = $('#dots').children('#'+cluster.id);
			clusterDot.css('bottom', cluster.y+12);
			// clusterDot.css('display', 'none');
			$('#dots').append(taskItem);
			// TODO append die restlichen dots
			for(var i = 1; i < cluster['included'].length; i++) {
				console.log(cluster['included'][i]);
			}
		});
	},
	updateMatrixAjax: function(data) {
		var that = this;
		TaskData.getTasks(data, settings);
		that.drawTasks(TaskData.data, TopicData.data, s.width, s.height);
		console.log(TaskData.data);
		console.log(Matrix.clusters);
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
