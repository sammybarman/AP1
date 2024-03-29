$(document).ready(function(){
  $('.sidenav').sidenav();
  $('.dropdown-trigger').dropdown({
    hover: true,
    belowOrigin: true,
    alignment: 'right',
    coverTrigger: false,
    closeOnClick: false
  })
  $.ajax({url: "getuser", success: function(result) {
    if (result.status == 1) {
      $('#signup').remove();
      $('#login').remove();
      document.getElementById('side_pic').setAttribute('style', 'display: block');
      document.getElementById('side_name').innerHTML = result.name;
      document.getElementById('side_email').innerHTML = result.email;
    }
    else {
      $('#logout').remove();
    }
  },
    error: function (xhr, ajaxOptions, thrownError) {
    }
  });
  $.ajax({url: "getphones", success: function(result) {
    addPhone(result);
  }});
  $('.modal').modal();
  $('.collapsible').collapsible();
});

function addPhone(result) {
  $('#phones').empty();
  sect = document.getElementById('phones');
  row_div = document.createElement('div');
  row_div.setAttribute('class', 'row');
  for(var i=0; i<result.phones.length; i++) {
    console.log(result.phones[i]);
    if (i%3 == 0){
      sect.appendChild(row_div);
      row_div = document.createElement('div');
      row_div.setAttribute('class', 'row');
    }
    col_div = document.createElement('div');
    col_div.setAttribute('class', 'col s12 m4');
    card_div = document.createElement('div');
    card_div.setAttribute('class', 'card');
    card_img = document.createElement('div');
    card_img.setAttribute('class', 'card-image waves-effect waves-block waves-light');
    img = document.createElement('img');
    img.setAttribute('class','activator');
    img.setAttribute('src', result.phones[i].img_link);
    card_img.appendChild(img);
    content_div = document.createElement('div');
    content_div.setAttribute('class', 'card-content');
    span = document.createElement('span');
    span.setAttribute('class', 'card-title center activator grey-text text-darken-4');
    span.innerHTML = result.phones[i].name;
    p = document.createElement('p');
    p.setAttribute('class', 'center');
    a = document.createElement('a');
    a.setAttribute('style', 'color:white');
    a.setAttribute('class', 'btn black buynowbtn');
    a.setAttribute('href', '/getproduct?phone_id='+result.phones[i].phone_id+'&phone_data_id='+result.phones[i].phone_data_id);
    a.innerHTML = 'Details';
    p.appendChild(a);
    content_div.appendChild(span);
    content_div.appendChild(p);
    reveal_div = document.createElement('div');
    reveal_div.setAttribute('class', 'card-reveal');
    span = document.createElement('span');
    span.setAttribute('class', 'card-title grey-text text-darken-4');
    i_elem = document.createElement('i');
    i_elem.setAttribute('class', 'material-icons right');
    i_elem.innerHTML = 'close';
    span.innerHTML = result.phones[i].name;
    span.appendChild(i_elem);
    ul = document.createElement('ul');
    li = document.createElement('li');
    li.innerHTML = 'Price - ₹' + result.phones[i].price;
    ul.appendChild(li);
    li = document.createElement('li');
    li.innerHTML = 'Display Size - ';
    ul.appendChild(li);
    li = document.createElement('li');
    li.innerHTML = 'Ram - ' + result.phones[i].ram + 'GB';
    ul.appendChild(li);
    li = document.createElement('li');
    li.innerHTML = 'Memory - ' + result.phones[i].storage + 'GB';
    ul.appendChild(li);
    reveal_div.appendChild(span);
    reveal_div.appendChild(ul);
    card_div.appendChild(card_img);
    card_div.appendChild(content_div);
    card_div.appendChild(reveal_div);
    col_div.appendChild(card_div);
    row_div.appendChild(col_div);
  }
  if(result.phones.length %3 != 0) {
    sect.appendChild(row_div);
  }
}

$(window).scroll(function(){

  if($(window).scrollTop()>20){
    $('nav').addClass('bg');
    $('.brand-logo').addClass('black-text');
    $('.forjq').addClass('bg2');
    $('.material-icons').addClass('icon-white');
  }else{
    $('nav').removeClass('bg');
    $('.brand-logo').removeClass('black-text');
    $('.forjq').removeClass('bg2');
    $('.material-icons').removeClass('icon-white');
  }
});

function addToCart() {
  link = '/' + window.location.href.split('/')[3];
  body = {'product_id': window.location.href.split('=')[window.location.href.split('=').length-1]};
  console.log(body);
  $.ajax({
    url: window.location.protocol+"//"+window.location.hostname+':8000'+'/cart_ops',
    type: 'POST',
    data: JSON.stringify(body),
    contentType: 'application/json',
    dataType: 'json',
    success: function (data) {
      if (data.redirect) {
        window.location.href = data.redirect;
      }
      else {
        console.log('Updated Cart');
        console.log(data);
      }
    }
  });
}

function addToWish() {
  link = '/' + window.location.href.split('/')[3];
  body = {'product_id': window.location.href.split('=')[window.location.href.split('=').length-1]};
  console.log(body);
  $.ajax({
    url: window.location.protocol+"//"+window.location.hostname+':8000'+'/wish_ops',
    type: 'POST',
    data: JSON.stringify(body),
    contentType: 'application/json',
    dataType: 'json',
    success: function (data) {
      if (data.redirect) {
        window.location.href = data.redirect;
      }
      else {
        console.log('Updated wishlist');
        console.log(data);
      }
    }
  });
}

$("#test5").change(function(){
 $.ajax({url: "search?price_max="+$(this).val()+'&search_term='+$('#search').val(), success: function(result) {
   addPhone(result);
 }});
});

$("#search").change(function(){
 $.ajax({url: "search?price_max="+$('#test5').val()+'&search_term='+$(this).val(), success: function(result) {
   console.log(result);
   addPhone(result);
 }});
});

function submitUser() {
  body = {'firstname': $('#first_name').val(),'lastname': $('#last_name').val(), 'email': $('#email').val(),'password': $('#password').val()}
  $.ajax({
    url: window.location.protocol+"//"+window.location.hostname+':8000'+'/createuser',
    type: 'POST',
    data: JSON.stringify(body),
    contentType: 'application/json',
    dataType: 'json',
    success: function (data) {
      console.log('Created user');
      console.log(data);
    },
    error: function (xhr, ajaxOptions, thrownError) {
      console.log('failed');
    }
  });
}

$("#search").submit(function() {
    return false;
});
// $('.carousel.carousel-slider').carousel({
//     fullWidth: true,
//     indicators: true
//   });
//   var autoplay = true;
//   setInterval(function() { if(autoplay) $('.carousel.carousel-slider').carousel('next'); }, 2000);
//   $('.carousel.carousel-slider').hover(function(){ autoplay = false; },function(){ autoplay = true; });
//
// $(document).ready(function(){
//     $('.parallax').parallax();
//   });
//
// $(document).ready(function(){
//       $('.fixed-action-btn').floatingActionButton();
//
//   });
//
// $(document).ready(function(){
//
//       $(window).scroll(function(){
//
//        if($(window).scrollTop()>20){
//          $('nav').addClass('bg');
//          $('.brand-logo').removeClass('black-text');
//          $('.brand-logo').addClass('red-text');
//        }else{
//          $('nav').removeClass('bg');
//          $('.brand-logo').removeClass('red-text');
//          $('.brand-logo').addClass('black-text');
//        }
//     });
//   });

  // Sidenav Implementation
// $(function() {
//         $('.sidenav').sidenav();
//     })
//
// $(document).ready(function(){
//         $('.fixed-action-btn').floatingActionButton();
//     });
//
// $(document).ready(function(){
//         $('.tap-target').tapTarget();
//     });
//
// $(document).ready(function(){
//       	$('.materialboxed').materialbox();
//       });
// $(document).ready(function(){
//         $('.scrollspy').scrollSpy();
//       });
