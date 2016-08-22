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
