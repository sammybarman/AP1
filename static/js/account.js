function changePwd() {
  body = {'password': $('#password2').val()}
  $.ajax({
    url: window.location.protocol+"//"+window.location.hostname+':8000'+'/changepwd',
    type: 'POST',
    data: JSON.stringify(body),
    contentType: 'application/json',
    dataType: 'json',
    success: function (data) {
      console.log('Changed pwd');
      console.log(data);
    },
    error: function (xhr, ajaxOptions, thrownError) {
      console.log('failed');
    }
  });
}
