$(document).ready(function() {
  $.ajax({url: "cart_ops", success: function(result) {
    console.log(result);
  }});
});
