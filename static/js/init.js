$(document).ready(function(){
  $('.sidenav').sidenav();
  $('.dropdown-trigger').dropdown({
    hover: true,
    belowOrigin: true,
    alignment: 'right',
    coverTrigger: false
  }
  );
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
        }
      )
  $('.modal').modal();
  $('.collapsible').collapsible();
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
