hljs.initHighlightingOnLoad();
$(document).ready(function() {
  $(".entry-container").hide();
  //toggle the componenet with class msg_body
  $(".title-container").click(function()
  {
    var div = $(this).next(".entry-container").slideToggle(500);
    if (!div.hasClass("on")){
      div.addClass("on").parent().addClass("seen");
    } else {
      div.removeClass("on");
    }
  });
  
  $(document).keypress(function(event) {
    var done = null;
    if ( event.which == 107 ) { // k - move up
      done = $(".on").toggle().removeClass("on").parent().prev().addClass("seen").find(".entry-container").toggle().addClass("on");
    } else if ( event.which == 106 ) { // j - move down
      done = $(".on").toggle().removeClass("on").parent().next().addClass("seen").find(".entry-container").toggle().addClass("on");
      if(done.length == 0) { // nothing opened
	done = $(".question").first().addClass("seen").find(".entry-container").toggle().addClass("on");
      }
    }
    if (done && done.length > 0) {
      $("html,body").animate(
	{scrollTop: done.parent().offset().top -10}, 500
      );
    }
  }
  )
});