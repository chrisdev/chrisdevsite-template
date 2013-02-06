
$('a.frontendadmin_edit').hover(
   function(){$(this).parent().css('outline', '4px solid #E9B007')},
   function(){$(this).parent().css('outline', '')}
);

$('a.frontendadmin').click(function(event) {
            event.preventDefault();
            var $div = $('<div>').addClass('reveal-modal').appendTo('body');
            $this = $(this);
            $.get($this.attr('href'), function(data) {
              return $div.empty().html(data).append('<a class="close-reveal-modal">&#215;</a>').reveal();
            });
    });

$(".fallback-flip").click(function(){
   $("body").toggleClass("wf-inactive");
});

