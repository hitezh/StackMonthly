#Add current directory to path, if isn't already 
import os, sys
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

#import needed libraries
import time, datetime, calendar
from utils import *
import bottle
from bottle import route, run, template, install, static_file, response
from bottle_sqlite import SQLitePlugin

# init SQLitePlugin with the db
install(SQLitePlugin(dbfile='db/stack.db'))

# dreamhost passenger hook
def application(environ, start_response):
    return bottle.default_app().wsgi(environ,start_response)

@route('/')
def index(db):
    dt = datetime.date.today()
    lastmonth = datetime.date(dt.year, dt.month, 1) - datetime.timedelta(days=1)
    return month_listing(str(lastmonth.year), str(lastmonth.month), db = db) 

#About page
@route('/about')
def about(db):
    year = str(datetime.date.today().year)
    from_date = int(time.mktime((int(year),1,1,0,0,0,0,0,0))) #first of the needed year
    to_date   = int(time.mktime((int(year)+1,1,1,0,0,0,0,0,0))) #first of the next year

    return template("about",
		    title="About StackMonthly",
		    tags = get_tags(from_date,to_date,db),
		    archives = get_archives(db),
		    year = year,
		    month = str(datetime.date.today().month-1),
		    seltag="Questions"
		    ) 

#List of RSS feeds, based on top 20 tags
@route('/feeds')
def rss(db):
    year = str(datetime.date.today().year)
    from_date = int(time.mktime((int(year),1,1,0,0,0,0,0,0))) #first of the needed year
    to_date   = int(time.mktime((int(year)+1,1,1,0,0,0,0,0,0))) #first of the next year

    return template("rss",
		    title="RSS Links",
		    tags = get_tags(from_date,to_date,db),
		    archives = get_archives(db),
		    year = year,
		    month = str(datetime.date.today().month-1),
		    seltag="Questions"
		    ) 

#Questions for a tag, special handling for tag='question'
@route('/feed/:taglist')
def rssxml(taglist,db):
    tags = taglist[:-4].split(",")
    
    query = """ select distinct questions.title as title, questions.body as question, questions.creation_date as creation_date,
		questions.owner_id as qowner_id, questions.owner_name as qowner_name, questions.id as qid,
		answers.body as answer, answers.owner_id as aowner_id, answers.owner_name as aowner_name,
		tags, questions.up_vote_count as up_vote_count
		from questions, answers, tags
		where questions.id = answers.question_id
                and  questions.id = tags.question_id
                %s
		order by questions.creation_date desc limit 20""" 
    
    if tags[0] != "questions": #return questions for the given tag
	query = query % ("and  tags.tag IN ("+','.join('?'*len(tags))+") ")
        questions = db.execute(query,tags).fetchall()

    else: # return top questions across all tags
	query = query % ""
        questions = db.execute(query).fetchall()

    response.content_type = "application/atom+xml; charset=utf-8"
    return template("rssxml",rows=questions,tags=tags)

#to match /2010/
@route('/:year#[2-9][0-9][0-9][0-9]#')
@route('/:year#[2-9][0-9][0-9][0-9]#/')
def year_listing(year,db): 
    from_date = int(time.mktime((int(year),1,1,0,0,0,0,0,0))) #first of the needed year
    to_date   = int(time.mktime((int(year)+1,1,1,0,0,0,0,0,0))) #first of the next year
    questions = questions_without_tag(from_date, to_date, db)
    return template("question",
		    rows=questions,
		    title=get_title(year, "", ""),
		    tags = get_tags(from_date,to_date,db),
		    archives = get_archives(db),
		    year=year,
		    month="01",
		    seltag="Questions"
		    )
    
#to match /2010/12/
@route('/:year#[2-9][0-9][0-9][0-9]#/:month')
@route('/:year#[2-9][0-9][0-9][0-9]#/:month/')
def month_listing(year, month, db):
    from_date = int(time.mktime((int(year),int(month),1,0,0,0,0,0,0))) #first of the needed month
    to_date   = int(time.mktime((int(year),int(month)+1,1,0,0,0,0,0,0))) #first of the next month
    questions = questions_without_tag(from_date, to_date, db)
    return template("question",
		    rows=questions,
		    title=get_title(year, month, ""),
		    tags = get_tags(from_date,to_date,db),
		    archives = get_archives(db),
		    year=year,
		    month=month,
		    seltag="Questions"
		    )
#to match /2010/12/java
@route('/:year#[2-9][0-9][0-9][0-9]#/:month/:tag')
@route('/:year#[2-9][0-9][0-9][0-9]#/:month/:tag/')
def listing(year, month, tag, db):
    from_date = int(time.mktime((int(year),int(month),1,0,0,0,0,0,0))) #first of the needed month
    to_date   = int(time.mktime((int(year),int(month)+1,1,0,0,0,0,0,0))) #first of the next month
    questions = db.execute("""
			    select questions.title as title, questions.body as question, questions.creation_date,
			    questions.owner_id as qowner_id, questions.owner_name as qowner_name, questions.id as qid,
			    answers.body as answer, answers.owner_id as aowner_id, answers.owner_name as aowner_name,
			    tags, questions.up_vote_count as up_vote_count
			    from questions, answers, tags
			    where questions.id = answers.question_id
                            and  questions.id = tags.question_id
                            and  tags.tag = ?
			    and questions.creation_date >= ? and questions.creation_date < ?
			    order by questions.up_vote_count desc limit 20
			    """,(tag.lower(),from_date,to_date)).fetchall() 
    return template("question",
		    rows=questions,
		    title=get_title(year, month, tag),
		    tags = get_tags(from_date,to_date,db),
		    archives = get_archives_for_tag(tag,db),
		    year=year,
		    month=month,
		    seltag=tag
		    )

# to match /tag/java. Currently unused
@route('/tag/:tag')
def listing(tag, db):
    dt = datetime.date.today()
    lastmonth = datetime.date(dt.year, dt.month, 1) - datetime.timedelta(days=1)
    return listing(str(lastmonth.year), str(lastmonth.month), tag, db) 

#server static files locally. On dreamhost anything under public is served by Apache
@route('/:filename')
def server_static(filename):
    return static_file(filename, root='public/')

@route('/static/css/:filename')
def server_css(filename):
    return static_file(filename, root='public/static/css')

@route('/static/images/:filename')
def server_imgs(filename):
    return static_file(filename, root='public/static/images')
# there is a public static void main joke somewhere here.

#Main method for local developement	using "python passenger_wsgi.py"
if __name__ == "__main__":
    bottle.debug(True)
    run(reloader=True)

