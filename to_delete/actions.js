$(function () {
  $('.RESTAPI').hide();
  $('.ServerStatus').hide();
  $('.crMany').hide();
  $('.readOne').hide();
  $('.readAll').hide();
  $('.update').hide();
  $('.delete').hide();

  $('.item1').on("click",function () {
  	$('.item1').addClass("active");
    $('.RESTAPI').hide();
    $('.ServerStatus').hide();
    $('.Description').show();
    $('.item2').removeClass("active");
    $('.item3').removeClass("active");
  });

  $('.item2').on("click",function () {
    $('.RESTAPI').show();
    $('.item2').addClass("active");
    $('.ServerStatus').hide();
    $('.Description').hide();
    $('.item3').removeClass("active");
    $('.item1').removeClass("active");
  });

  $('.item3').on("click",function () {
    $('.RESTAPI').hide();
    $('.item2').removeClass("active");
    $('.ServerStatus').show();
    $('.item3').addClass("active");
    $('.Description').hide();
    $('.item1').removeClass("active");
  });

  $('.c1').on("click",function () {
  	$('.crMany').hide();
  	$('.readOne').hide();
  	$('.readAll').hide();
  	$('.update').hide();
  	$('.delete').hide();
  	$('.crOne').show();
  	$('.c1').addClass("active");
  	$('.c2').removeClass("active");
  	$('.r1').removeClass("active");
  	$('.r2').removeClass("active");
  	$('.upd').removeClass("active");
  	$('.del').removeClass("active");
  });

  $('.c2').on("click",function () {
	$('.crMany').show();
  	$('.readOne').hide();
  	$('.readAll').hide();
  	$('.update').hide();
  	$('.delete').hide();
  	$('.crOne').hide();
  	$('.c1').removeClass("active");
  	$('.c2').addClass("active");
  	$('.r1').removeClass("active");
  	$('.r2').removeClass("active");
  	$('.upd').removeClass("active");
  	$('.del').removeClass("active");
  });

  $('.r1').on("click",function () {
  	$('.crMany').hide();
  	$('.readOne').show();
  	$('.readAll').hide();
  	$('.update').hide();
  	$('.delete').hide();
  	$('.crOne').hide();
  	$('.c1').removeClass("active");
  	$('.c2').removeClass("active");
  	$('.r1').addClass("active");
  	$('.r2').removeClass("active");
  	$('.upd').removeClass("active");
  	$('.del').removeClass("active");
  });

  $('.r2').on("click",function () {
  	$('.crMany').hide();
  	$('.readOne').hide();
  	$('.readAll').show();
  	$('.update').hide();
  	$('.delete').hide();
  	$('.crOne').hide();
  	$('.c1').removeClass("active");
  	$('.c2').removeClass("active");
  	$('.r1').removeClass("active");
  	$('.r2').addClass("active");
  	$('.upd').removeClass("active");
  	$('.del').removeClass("active");
  });

  $('.upd').on("click",function () {
  	$('.crMany').hide();
  	$('.readOne').hide();
  	$('.readAll').hide();
  	$('.update').show();
  	$('.delete').hide();
  	$('.crOne').hide();
  	$('.c1').removeClass("active");
  	$('.c2').removeClass("active");
  	$('.r1').removeClass("active");
  	$('.r2').removeClass("active");
  	$('.upd').addClass("active");
  	$('.del').removeClass("active");
  });

  $('.del').on("click",function () {
  	$('.crMany').hide();
  	$('.readOne').hide();
  	$('.readAll').hide();
  	$('.update').hide();
  	$('.delete').show();
  	$('.crOne').hide();
  	$('.c1').removeClass("active");
  	$('.c2').removeClass("active");
  	$('.r1').removeClass("active");
  	$('.r2').removeClass("active");
  	$('.upd').removeClass("active");
  	$('.del').addClass("active");
  });

  $('.ui .item .outermenu').on('click', function() {
      $('.ui .item .outermenu').removeClass('active');
      $(this).addClass('active');
   });

});
