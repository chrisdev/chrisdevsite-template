
$('a.frontendadmin_edit').hover(
   function(){$(this).parent().css('outline', '4px solid #E9B007')},
   function(){$(this).parent().css('outline', '')}
);

$(".fallback-flip").click(function(){
   $("body").toggleClass("wf-inactive");
});
	