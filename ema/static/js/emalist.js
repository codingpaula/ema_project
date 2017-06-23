/* EMA List = Aufgaben als Liste anzeigen */
var EmaList = {
  drawTable: function(taskData, topicData) {
    $('#EmaListBody').empty();
    var that = this;
    taskData.forEach(function(task){
      var colorIndex = task.topic;
      if(topicData[colorIndex]['displayed'] == false) {

      } else {
        var topic = topicData[colorIndex];
        that.drawRow(task, topic);
      }
    });
  },
  drawRow: function(task, topic) {
    var row = $('<tr/>', {
      id: task.id,
      class: 'emaListItem'
    });
    var emptyTd = $('<td/>', {
      class: 'surroundingTd'
    });
    var done = $('<div/>', {
      class: 'doneTable',
      text: 'no'
    });
    var topic = $('<div/>', {
      class: 'topicTable',
      text: topic.name,
      css: {
        backgroundColor: topic.color,
        color: 'white'
      }
    });
    var name = $('<div/>', {
      class: 'nameTable',
      text: task.name
    });
    var description = $('<div/>', {
      class: 'descriptionTable',
      text: task.description
    });
    var due_date = $('<div/>', {
      class: 'dueDateTable',
      text: formatDate(task.due_date),
      css: {
        backgroundColor: colorDueDate(task.due_date),
        color: 'white'
      }
    });
    var importance = $('<div/>', {
      class: 'descriptionTable',
      text: impToText(task.importance),
      css: {
        backgroundColor: impColor(task.importance),
        color: 'white'
      }
    });
    var duration = $('<div/>', {
      class: 'durationTable',
      text: task.duration
    });
    var rating = $('<div/>', {
      class: 'ratingTable',
    });
    row.append(
      emptyTd.clone().append(done),
      emptyTd.clone().append(topic),
      emptyTd.clone().append(name),
      emptyTd.clone().append(description),
      emptyTd.clone().append(due_date),
      emptyTd.clone().append(importance),
      emptyTd.clone().append(duration),
      emptyTd.clone().append(rating));
    $('#EmaListBody').append(row);
  }
};

function impToText(imp) {
  if(imp == 0) {
    return 'not important';
  } else if (imp == 1) {
    return 'less important';
  } else if (imp == 2){
    return 'important';
  } else if (imp == 3) {
    return 'very important';
  } else {
    return 'error';
  }
}

function impColor(imp) {
  if(imp == 0) {
    return 'green';
  } else if (imp == 1) {
    return 'yellow';
  } else if (imp == 2) {
    return 'orange';
  } else if (imp == 3) {
    return 'red';
  }
}

function colorDueDate(due_date) {
  var today = new Date();
  var distance2today = Date.parse(due_date) - Date.parse(today);
  var oneDay = 24*60*60*1000;
  if(distance2today < oneDay) {
    return "darkred";
  } else if (distance2today < 2*oneDay) {
    return "red";
  } else if (distance2today < 4*oneDay) {
    return "orange";
  } else if (distance2today < 7*oneDay) {
    return "yellow";
  } else if (distance2today < 14*oneDay) {
    return "green";
  } else if (distance2today < 21*oneDay) {
    return "turquoise";
  } else {
    return "blue";
  }
}
