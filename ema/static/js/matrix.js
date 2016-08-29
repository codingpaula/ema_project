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
			//console.log('newDot: '+newDot.id+', oldDot: '+oldDot.id);
			// TODO wie kann erkannt werden dass die neue Stelle nicht auch schon
			// besetzt ist?
			var cluster_id = oldDot.id;
			if (Matrix.clusters.hasOwnProperty(cluster_id) && versorgt == false) {
				//console.log('add to old cluster');
				TaskData.data[newDot.id]['cluster'] = cluster_id;
				Matrix.clusters[cluster_id]['included'].push(newDot.id);
				versorgt = true;
			} else if (versorgt == false){
				//console.log('new cluster');
				TaskData.data[newDot.id]['cluster'] = cluster_id;
				TaskData.data[cluster_id]['cluster'] = cluster_id;
				var newCluster = {
					'id': cluster_id,
					'x': oldDot.x,
					'y': oldDot.y,
				 	'included': [cluster_id, newDot.id]
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
	if (takenDot.x - 20 < newDot.x && takenDot.x + 20 > newDot.x) {
		if (takenDot.y - 20 < newDot.y && takenDot.y + 20 > newDot.y) {
			return true;
		}
	} else {
		return false;
	}
	return false;
}

// calculate cluster included coordinates so that they are in the Matrix
function coordinates(cluster, radius, bogen, runde) {
	// berechne Koordinaten
	var xC = cluster.x + (radius * Math.cos(bogen));
	var yC = cluster.y + (radius * Math.sin(bogen));
  var paket = {};
	if (xC < s.width && xC > 40 && yC > 50 && yC < s.height) {
		paket = {'x': xC, 'y': yC, 'radius': radius, 'bogen': bogen};
		return paket;
	} else {
		// rekursiver Aufruf, um mit neuen Parametern neuen Punkt zu berechnen
    paket = coordinates(cluster, radius+1.5, bogen+(Math.PI/4), runde+1);
		return paket;
	}
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
	switch(imp) {
		case '0':
			stars.append(empty_star.clone());
			stars.append(empty_star.clone());
			stars.append(empty_star.clone());
			return stars;
		case '1':
			stars.append(full_star.clone());
			stars.append(empty_star.clone());
			stars.append(empty_star.clone());
			return stars;
		case '2':
			stars.append(full_star.clone());
			stars.append(full_star.clone());
			stars.append(empty_star.clone());
			return stars;
		case '3':
			stars.append(full_star.clone());
			stars.append(full_star.clone());
			stars.append(full_star.clone());
			return stars;
		default:
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
		that.clusters = [];
		var count = 1;
		// Hilfsvariablen
		// durch alle übergebenen Aufgaben
		taskData.forEach(function(task){
			var colorIndex = task.topic;
			if(topicData[colorIndex]['displayed'] == false) {
				// don't display dot when sidebar setting says so
			} else {
				// check überschneidungen
				var dot = {id: task.id, x: task.x, y: task.y};
				if (doubles(taken, dot)) {
					// cluster is made in doubles
				} else {
					var topicColor = topicData[colorIndex]['color'];
					// eigentlichen Punkt kreieren und zeichnen
					that.drawDot(task, task.x, task.y, topicColor, "");
					// Array mit bereits gezeichneten Koordinaten
					taken.push(dot);
					count++;
				}
			}
		});
		//console.log(taken);
		that.drawCluster(count);
	},
	// Hilfsfunktion um ausführlichere Detailanzeige zu zeichnen
	drawDot: function(task, xC, yC, color, mode) {
		// eigentlicher Kreis mit task_id in entsprechender Farbe des Topics
		var clickHandler = function(){
			$('#ajaxEditTask').data = $(this).attr('id');
		};
		var taskItem = $('<div/>', {
			class: 'dot',
			id: task.id,
			css: {
				left: xC,
				bottom: yC,
				borderColor: color,
				width: 7,
				height: 7
			},
			onclick: clickHandler
		});
		taskItem.attr('data-toggle', 'modal');
		taskItem.attr('data-target', '#ajaxModal');
		taskItem.attr('data-task', task.id);
		var name = $('<p/>', {
			class: 'dotSchrift dotName',
			css: {
				color: color
			},
			text: task.name
		});
		// div mit den Aufgaben-Details
		var label = $('<div/>', {
			class: 'hoverField',
			css: {
				zIndex: 1
			}
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
		label.append(title, attributes, formatImp(task.importance));
		if (mode == "noName") {
			taskItem.attr('class', 'dot cluster'+task.cluster);
			taskItem.append(label);
			taskItem.css('display', 'none');
		} else {
			taskItem.append(name, label);
		}
		$('#dots').append(taskItem);
	},
	drawCluster: function(count) {
		var that = this;
		that.clusters.forEach(function(cluster) {
			$('#dots').children('#'+cluster.id).remove();
			// zeichnet das cluster
			var taskItem = $('<div/>', {
				class: 'dot cluster',
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
			var number = $('<p/>', {
				class: 'dotSchrift dotNumber',
				css: {
					color: 'black'
				},
				text: cluster['included'].length
			});
			taskItem.append(number);
			taskItem.click(function() {
				var query = $('#dots').find('.dot.cluster'+cluster.id);
				query.toggle();
			});
			$('#dots').append(taskItem);
			// TODO append die restlichen dots
			// startabstand (r)
			var radius = 12;
			// eine Runde = 2*pi, start = 0
			var bogen = 0;
			for(var i = 0; i < cluster['included'].length; i++) {
				var task_id = cluster['included'][i];
				var task = TaskData.data[task_id];
				var color = TopicData.data[task.topic].color;
				// Koordinaten rausfinden, damit Spirale um cluster entsteht
				var paket = coordinates(cluster, radius, bogen, 1);
				// Punkt zeichnen mit Modus "noName"
				that.drawDot(task, paket.x, paket.y, color, "noName");
				// pro Runde um 1.5 mehr fuer r, damit eine Spirale entsteht
				radius = paket.radius + 1.5;
				// pro Runde ein viertel pi mehr
				bogen = paket.bogen + Math.PI/4;
			}
		});
	},
	updateMatrixAjax: function(data) {
		var that = this;
		TaskData.getTasks(data, settings);
		that.drawTasks(TaskData.data, TopicData.data, s.width, s.height);
		//console.log(TaskData.data);
		//console.log(Matrix.clusters);
	}
};
