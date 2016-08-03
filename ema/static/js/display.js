$(function() {
  // Start der Matrix
  Matrix.init();
  // Achsen zeichnen mit vorgegebenen Massen
  // Matrix.drawAxes(s.drawing, s.width, s.height);
  // Topic-Daten behandeln
  TopicData.getTopics(topic_data);
  // Task-Daten behandlen
  TaskData.getTasks(task_data);
  // Aufgaben in die Matrix zeichnen
  Matrix.drawTasks(TaskData.data, TopicData.data, s.width, s.height);
});
