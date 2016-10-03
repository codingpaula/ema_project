$(function() {
  // onclick fuer Nachrichten oben rechts
  $('.closeNotification').click(function(){
    $('.messages').css('display', 'none');
    $('.messages .text').empty();
  });
});
