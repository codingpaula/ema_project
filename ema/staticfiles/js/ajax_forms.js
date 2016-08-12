$('.ajaxFormCreateTask').on('submit', function(form) {
  // var $form = $(form);
  $.ajax({
    url: "/matrix/create_task",
    type: form.method,
    data: $form.serialize(),
    success: function(json) {
      $form.replace(json);
    }
  });
});


//  taskName: $('#id_task_name').val(),
//  taskDescription: $('#id_task_description').val(),
//  dueDate: $('#id_due_date').val(),
//  taskImportance: $('#id_importance').val(),
//  taskTopic: $('#id_topic').val(),
//  erledigt: $('#id_done').val()
