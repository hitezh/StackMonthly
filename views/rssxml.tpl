%import time
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <author>Hitesh Sarda</author>
    <title>Stack Overflow Monthly</title>
    <subtitle>Last month's best of stackoverflow for {{", ".join(tags)}}</subtitle>
    %for row in rows:
    <entry>
        <title>{{row["title"]}}</title>
        <link href="http://stackoverflow.com/questions/{{row["qid"]}}"/>
        <author>
            <name>{{row["qowner_name"]}}</name>
            <uri>http://stackoverflow.com/users/{{row["qowner_id"]}}</uri>
        </author>
        <published>{{time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(row["creation_date"]))}}</published>
        <content type="html">
        {{"<p>"+row["question"]+"</p><hr/><p>"}}
        Answered by {{row["aowner_name"]}}
        {{"</p><p>"+row["answer"]+"</p>"}}
        </content>
    </entry>
    %end
</feed>