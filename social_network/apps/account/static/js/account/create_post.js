$(document).on('submit', '#create_post', function(e){
  e.preventDefault();
  var post_title = $('#post_title').val();
  var post_text = $('#post_text').val();
  var post_image = $('#post_image').val();

  if (post_text != ''){
    $('#post_title').val('');
    $('#post_text').val('');
    $('#post_image').val('');
     $.ajax({
      type:'POST',
      url:"/account/",
      data:{
        post_title:post_title,
        post_text:post_text,
        post_image:post_image,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success:function () {
        alert('Успешно создан!');
      }
    });
  };
});
