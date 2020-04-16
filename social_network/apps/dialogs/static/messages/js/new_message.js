setInterval(function () {
      $.ajax({
          url: "{% url 'dialogs:post' friend.username %}",
          type: 'GET',
          data: {'check': true},

          success: function (json) {
              if (json.result) {
                  var doc = $.parseHTML(json.messages_list);
                  $('#message_block').append(doc);
                  $('#message_block').scrollTop(9999);
              }
          }
      });
  }, 1000);

  window.onload = function(){ document.getElementById('message_block').scrollTop = 9999;}

  $(document).on('submit', '#leave_message', function(e){
  e.preventDefault();

   $.ajax({
      type:'POST',
      url:'{% url "dialogs:leave_message" friend.username %}',
      data:{
        message_text:$('#message_text').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success:function (json) {
          if (json.result) {
              var doc = $.parseHTML(json.messages_list);
              $('#message_text').val('');
              $('#message_block').append(doc);
              $('#message_block').scrollTop(9999);
        }
      }
    });
  });


  $('#previous_messages').on('click', function(e) {
    e.preventDefault();
    var message_block = $('#message_block');
    message_block.scrollTop(message_block.get(0).scrollHeight);
    var scrollHeight = message_block.scrollTop() + message_block.height();
    message_block.scrollTop(0);

    $('#previous_messages').remove();
       {% for message in messages2 %}
         {% if message.sender == user.username %}
              message_block.prepend('<p> <img class="img-fluid" src="{{ user.profile.avatar.url }}" width="30px" alt="{{ user.username }}" > {{message.message_text|linebreaks}}</p>');
              message_block.prepend("<h5>{{user.first_name}} {{user.last_name}} <time>{{message.message_time}}</time></h5>");
         {% else %}
              message_block.prepend('<p><img class="img-fluid" src="{{ friend.profile.avatar.url }}" width="30px" alt="{{ friend.username }}" > {{message.message_text|linebreaks}}</p>');
              message_block.prepend("<h5>{{friend.first_name}} {{friend.last_name}} <time>{{message.message_time}}</time></h5>");
         {% endif %}
       {% endfor %}
    message_block.scrollTop(message_block.get(0).scrollHeight);
    var new_scrollHeight = message_block.scrollTop() + message_block.height();
    message_block.scrollTop(0);
    message_block.scrollTop(new_scrollHeight - scrollHeight);
   });
