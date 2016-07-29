$(function() {
  Matrix.init();
  Matrix.drawAxes(s.drawing, s.width, s.height);
  TopicData.start(topic_data);
  TaskData.start(task_data);
  Matrix.drawTasks(s.canvas, TaskData.data, TopicData.data, s.width, s.height);
});
