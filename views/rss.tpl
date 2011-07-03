%import time
%from urllib import quote
            <div class="question rounded5px">
              <h3>Select the RSS link of the tags that interest you&hellip;</h3>
              <p>The format of the link is:
                <ul>
                  <li><a href="http://stackmonthly.com/feed/questions.xml">http://stackmonthly.com/feed/questions.xml</a> (all questions)</li>
                  %tags.sort()
                  %for tag in tags:
                  <li><a href="http://stackmonthly.com/feed/{{quote(tag["tag"])}}.xml">
                  http://stackmonthly.com/feed/{{quote(tag["tag"])}}.xml</a>
                  %if tag["tag"] <> quote(tag["tag"]):
                    ({{tag["tag"]}})
                  %end
                  </li>
                  %end
                </ul>
              </p>
              <h3>&hellip; or make your own.</h3>
              <p>The format of the link is:
                <ul>
                  <li>http://stackmonthly.com/feed/<i>tag</i>.xml</li>
                  <li>http://stackmonthly.com/feed/<i>tag1</i>,<i>tag2</i>,<i>tagn</i>.xml</li>
                </ul>
              </p>
            </div>
%rebase index title=title, month=month, year=year,tags=tags,tag=seltag,archives=archives