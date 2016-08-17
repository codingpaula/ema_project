$('#ajaxCreateTask').submit(function(e) {
  e.preventDefault();
  var form = $('form#ajaxCreateTask');
  $.ajax({
    url: "/matrix/adding/",
    type: "POST",
    dataType: "json",
    data: {
      'task_name': form.find('#id_task_name').val(),
      'task_description': form.find('#id_task_description').val(),
      'due_date': form.find('#id_due_date').val(),
      'importance': form.find('#id_importance').val(),
      'topic': form.find('#id_topic').val()
    },
    success: function(data) {
      TaskData.getTasks(data, settings);
      Matrix.drawTasks(TaskData.data, TopicData.data, s.width, s.height);
      // reset or close after success?
      $('#ajaxCreateTask')[0].reset();
    },
    error: function(data) {
      console.log("an error occurred!");
      console.log(data);
      console.log(form.find('#id_due_date').val());
      // TODO fehlerbehandlung
    }
  });
});

// from bootstrap modal
$('#editTask').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var task_id = button.data('task'); // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this);
  modal.find('.modal-title').text('Edit task "' + TaskData.data[task_id].name + '"');
  var modal_body = modal.find('form#ajaxEditTask').children('.modal-body');
  var submit_footer = modal.find('.modal-footer');
  prefillForm(task_id, modal_body, submit_footer);
});

$('#ajaxEditTask').submit(function(e) {
  e.preventDefault();
  var task_id = $(this).find('input[type="submit"]#ajaxEditSubmit').data('task_id');
  var form = $('form#ajaxEditTask');
  $.ajax({
    url: "/matrix/"+task_id+"/taskediting/",
    type: "POST",
    dataType: "json",
    data: {
      'task_name': form.find('#id_task_name').val(),
      'task_description': form.find('#id_task_description').val(),
      'due_date': form.find('#id_due_date').val(),
      'importance': form.find('#id_importance').val(),
      'topic': form.find('#id_topic').val()
    },
    success: function(data) {
      TaskData.getTasks(data, settings);
      Matrix.drawTasks(TaskData.data, TopicData.data, s.width, s.height);
      $('.ajaxFormEditTask').find('button[data-dismiss="modal"]').click();
    },
    error: function(data) {
      console.log("an error occurred!");
      console.log(data);
    }
  });
});

function prefillForm(task_id, editForm, submit_footer) {
  var task = TaskData.data[task_id];
  editForm.find('input#id_task_name').val(task.name);
  editForm.find('textarea#id_task_description').val(task.description);
  // TODO display due date right!
  console.log(task.due_date);
  console.log(new Date(task.due_date));
  editForm.find('input#id_due_date').val(formatDate2Form(task.due_date));
  editForm.find('select#id_importance').val(task.importance).attr('selected', 'selected');
  editForm.find('select#id_topic').val(task.topic).attr('selected', 'selected');
  submit_footer.find('input[type="submit"]#ajaxEditSubmit').data('task_id', task_id);
  submit_footer.find('input[type="submit"]#ajaxDeleteSubmit').data('task_id', task_id);
  console.log(submit_footer.find('input[type="submit"]#ajaxDeleteSubmit').data('task_id'));
}

function formatDate2Form(date) {
  var dueDate = new Date(date);
  var formattedDate = "";
  if(dueDate.getDate() < 10) {
    formattedDate += "0";
  }
  formattedDate += dueDate.getDate();
  formattedDate += "/";
  if(dueDate.getMonth() < 9) {
    formattedDate += "0";
  }
  formattedDate += (dueDate.getMonth()+1);
  formattedDate += "/";
  formattedDate += dueDate.getFullYear();
  formattedDate += " ";
  if(dueDate.getHours() < 10) {
    formattedDate += "0";
  }
  formattedDate += dueDate.getHours();
  formattedDate += ":"
  if(dueDate.getMinutes() < 10) {
    formattedDate += "0";
  }
  formattedDate += dueDate.getMinutes();
  console.log(formattedDate);
  return formattedDate;
}
