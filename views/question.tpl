%import time
%from urllib import quote

%for row in rows:
%post_date = time.gmtime(row["creation_date"])
	<div class="rounded5px question" >
          <div class="title-container fix">
	    <div class="title">
	      <h2 class="questiontitle">{{row["title"]}}</h2>
	      <div class="questiondata fix">
                <span class="author">Asked <a href="http://stackoverflow.com/questions/{{row["qid"]}}">on {{time.strftime("%a, %d %b %Y",time.gmtime(row["creation_date"]))}}</a>
    by <a href="http://stackoverflow.com/users/{{row["qowner_id"]}}" target="blank" >{{row["qowner_name"]}}</a></span>
                <span class="tags">
                  %for tag in row["tags"].split(','):
                  {{!"<a href='/%s/%s/%s'>%s</a>" % (year,month,quote(tag),tag)}}
                  %end
                </span>
              </div>
            </div>
            <div class="date">
              <span class="month"></span>
              <span class="day">{{row["up_vote_count"]}}</span>
              <span class="year">votes</span>
            </div>
          </div>
          <div class="entry-container fix">
            <div class="entry entry-content fix">
    
    {{!row["question"]}}
          <div class="question-footer fix">
            <h1 class="answer questiontitle">
              Answered by <a href="http://stackoverflow.com/users/{{row["aowner_id"]}}" target="blank" >{{row["aowner_name"]}}</a>
            </h1>
          </div>
    <p>{{!row["answer"]}}</p>

            </div>
          </div>

        </div>
%end
%rebase index title=title, month=month, year=year,tags=tags,tag=seltag,archives=archives