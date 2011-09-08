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
      $("body").keypress(function(event) {
	if ( event.which == 106 ) { // j - move up
	  $(".on").slideToggle(500).removeClass("on").parent().prev().addClass("seen").find(".entry-container").slideToggle(500).addClass("on");
	} else if ( event.which == 107 ) { // k - move down
	  done = $(".on").slideToggle(500).removeClass("on").parent().next().addClass("seen").find(".entry-container").slideToggle(500).addClass("on");
	  if(done.length == 0) { // nothing opened
	    $(".question").first().addClass("seen").find(".entry-container").slideToggle(500).addClass("on");
	  }
	}
      }
      )
    });