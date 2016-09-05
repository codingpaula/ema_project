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
		var all_button = $('button#all');
		if(all_button.css('background-color') == 'rgb(192, 192, 192)') {
			for(button in TopicData.data) {
				// jeder Button, der an ist, wird ausgeklickt
        var toggle = $('button#'+button);
        toggle.css('background-color', '#f1f1f1');
        toggle.css('color', TopicData.data[button].color);
        TopicData.data[button].displayed = false;
			}
      // update Matrix
      $('#dots').empty();
			// die Buttonfarbe des All-Buttons wird geaendert
			clickSidebarButton(all_button);
			all_button.text('select all topics');
		} else {
			for(button in TopicData.data) {
				// alle Buttons, die aus sind, werden angemacht
        var toggle = $('button#'+button);
        toggle.css('background-color', TopicData.data[button].color);
        toggle.css('color', '#fff');
        TopicData.data[button].displayed = true;
			}
      // update Matrix
      Matrix.drawTasks(TaskData.data, TopicData.data, s.width, s.height);
			// Farbe updaten
			unclickSidebarButton(all_button);
			all_button.text('unselect all topics');
		}
	},
	// Moeglichkeit die Topics zu editieren
	editTopics: function() {
		// wieder Unterscheidung anhand von Hintergrundfarbe des Edit-Buttons
		var editButton = $('button#editTopics');
		if(editButton.css('background-color') == 'rgb(192, 192, 192)') {
			for(button in TopicData.data) {
				// alle onclick-Attribute der Buttons auf die Topic-Anzeige lenken
				var glyphi = $('<span/>', {
					id: 'icon',
					class: 'glyphicon glyphicon-pencil pull-right'
				});
				var toggling = $('button#'+button);
				toggling.append(glyphi);
				toggling.attr('onclick', "location.href='/matrix/"+button+"/edittopic'");
			}
			// All-Button ausmachen
			$('button#all').attr('onclick', '');
			// Hintergrund anpassen
			clickSidebarButton(editButton);
		} else {
			for(button in TopicData.data) {
				// zurueck zu der Button beeinflusst die Matrix
				var toggling = $('button#'+button);
				toggling.find('span#icon').remove();
				toggling.attr('onclick', 'Sidebar.button('+button+')');
			}
			// All-Button geht wieder
			$('button#all').attr('onclick', 'Sidebar.allButton()');
			// Hintergrund anpassen
			unclickSidebarButton(editButton);
		}
	}
};

function clickSidebarButton(button) {
	button.css('background-color', '#eee');
	button.css('border-color', 'black');
	button.css('color', 'black');
}

function unclickSidebarButton(button) {
	button.css('background-color', 'rgb(192, 192, 192)');
	button.css('border-color', 'white');
	button.css('color', 'white');
}
