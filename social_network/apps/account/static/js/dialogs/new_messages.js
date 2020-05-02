function new_messages() {
      $.ajax({
          url: "/new_messages/",
          type: 'GET',
          data: {'check': true},

          success: function (json) {
              if (json.result) {
                var doc = json.messages_count;
                var new_friends = json.new_friends;
                if (doc != 0){
                  $('#messages_count').text(doc);
                }
                if (new_friends != 0){
                  $('#new_friends').text(new_friends);
                }
              }
          }
      });
  }
new_messages();
setInterval(new_messages, 10000);
