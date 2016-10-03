$(function() {
  // Start der Matrix
  Matrix.init();
  // Achsen zeichnen mit vorgegebenen Massen
  //Matrix.drawAxes(s.drawing, s.width, s.height);
  // Topic-Daten behandeln
  TopicData.getTopics(topic_data);
  // Task-Daten behandlen
  TaskData.getTasks(task_data, settings);
  // Aufgaben in die Matrix zeichnen
  Matrix.drawTasks(TaskData.data, TopicData.data);
  // update Matrix wenn die groesse sich veraendert hat
  $(window).resize(function () {
    waitForFinalEvent(function(){
      Matrix.updateSettings();
      TaskData.updateCoordinates(settings);
      Matrix.drawTasks(TaskData.data, TopicData.data);
    }, 500, "matrix resize");
  });
  // CSRF-TOKEN fuer AJAX-Requests
  function getCookie(name) {
    var cookieValue = null;
    var i = 0;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (i; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
});
// erst event wenn fenster vollstaendig bewegt = veraenderung der groesse
var waitForFinalEvent = (function () {
  var timers = {};
  return function (callback, ms, uniqueId) {
    if (!uniqueId) {
      uniqueId = "Don't call this twice without a uniqueId";
    }
    if (timers[uniqueId]) {
      clearTimeout (timers[uniqueId]);
    }
    timers[uniqueId] = setTimeout(callback, ms);
  };
})();
