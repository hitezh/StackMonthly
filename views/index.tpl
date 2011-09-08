%import calendar
%from urllib import quote
<!doctype html>
<html>
  <head>
    <title>{{title}}</title>
    <link rel="stylesheet" href="/static/css/stackstyle.css" type="text/css" media="all">
    <link rel="alternate" type="application/atom+xml" title="Last month's best of Stack Overflow" href="http://stackmonthly.com/feed/{{tag.lower()}}.xml" /> 
	<script type="text/javascript">
	  var _gaq = _gaq || [];
	  _gaq.push(['_setAccount', 'UA-7349669-4']);
	  _gaq.push(['_trackPageview']);
	  (function() {
	    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
	    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
	  })();
	</script>
  </head>
  
<body >
    <div id="wrapper" >
      <div id="header-container" >
	<div id="header" class="fix" >
	  <h1 ><a href="/">StackMonthly</a></h1>
	  <div ><a href="/about">About</a>
	    <a href="/feeds" class="feed">Feeds</a></div>
	</div><!-- /header -->
      </div><!-- //#header-container -->
      <div id="container" class="fix">
	<div id="main-col" >
	  <div id="content" >
	    <h2 >{{title}}</h2>
        %include
	  </div> 
    </div>
	<div id="sidebar-shell-1" >
	  <div id="sidebar" class="rounded5px">
	<!--widget start -->
	<div id="archives" ><h3 >{{tag}} in other months</h3>
	  <div >
	    <ul>
	      <!--% for yr in range(2009,2012):-->
	      %years = archives.keys()
	      %years.reverse()
	      %for yr in years:
		<li >{{yr}}
	        %for mon in archives[yr]:
		  <ul >
		    %if tag == "Questions":
		      <li ><a href="{{"/%s/%s/" % (yr,mon)}}">{{calendar.month_name[mon]}}</a></li>
		    %else:
		      <li ><a href="{{"/%s/%s/%s" % (yr,mon,quote(tag))}}">{{calendar.month_name[mon]}}</a></li>
		    %end
		  </ul>
		%end
		</li>
	      %end
	    </ul>
	  </div>
	</div>
	<!--widget end -->
	<!--widget start -->
	<div id="tags" ><h3 >Other tags for {{calendar.month_name[int(month)] if len(month)> 0 else ""}} {{year}} </h3>
	  <div >
	    <ul>
	      %for tag in tags:
	      <li><a href="{{"/%s/%s/%s" % (year,month,quote(tag["tag"]))}}"><span>{{!tag["tag"]}} ({{tag["total"]}})</span></a></li>
	      %end
	    </ul>
	  </div>
	</div>
</div>
</div>
	</div>
	<div id="footer">
		<table>
			<tbody><tr>
				<td >Content licensed under <a href="http://creativecommons.org/licenses/by-sa/3.0/" rel="license">cc-wiki</a> from <a href="http://www.stackoverflow.com/">Stack Overflow</a>. </td>
				<td class="rightcol">Weekend project of <a href="http://hitesh.in/">Hitesh</a> Sarda. <a href="https://github.com/hitezh/StackMonthly">Source Code</a>.</td>
			</tr>
		</tbody></table>
	</div>
	<script src="http://yandex.st/highlightjs/6.0/highlight.min.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<script src="/static/stack.js"></script>
    <link  href="http://fonts.googleapis.com/css?family=Artifika:regular" rel="stylesheet" type="text/css" >
    <link rel="stylesheet" href="/static/css/zenburn.css" type="text/css" media="all">
  </body>
</html>