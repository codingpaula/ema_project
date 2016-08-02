$(function() {
  Matrix.init();
  //Matrix.drawAxes(s.drawing, s.width, s.height);
  TopicData.getTopics(topic_data);
  TaskData.getTasks(task_data);
  Matrix.drawTasks(TaskData.data, TopicData.data, s.width, s.height);
});

// unten 60
// links 50
// oben 680
// rechts 880
