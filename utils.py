import time, datetime, calendar

def get_title(year, month, tag):
    if len(month) > 0:
	return "Best %s questions in %s %s" % (tag,calendar.month_name[int(month)], year)
    else:
        return "Best %s questions in %s" % (tag,year)

def get_tags(from_date,to_date,db):
    query = """select tag, total from (
	select tag, count(1) as total from tags 
        where [date] >= ? and [date] < ?
        group by tag
        order by count(1) desc
        limit 30
	) order by tag asc"""
    
    result =  db.execute(query,(from_date,to_date)).fetchall()
    # cast to list as resultset seems to lose sort data
    return [{"tag": row["tag"], "total":row["total"]} for row in result]
    

def get_archives(db):
    rows = db.execute("""select distinct strftime("%Y %m",date([date],'unixepoch'))
		      as month from tags order by 1 desc""").fetchall()
    return rejig_months(rows)

def get_archives_for_tag(tag, db):
    rows = db.execute("""select distinct strftime("%Y %m",date([date],'unixepoch'))
		      as month from tags where tag=?  order by 1 desc""", (tag,)).fetchall()
    return rejig_months(rows)
    
def rejig_months(rows):
    months = [[int(x) for x in row[0].split(" ")] for row in rows]
    year_list = {}
    for month in months:
	if year_list.has_key(month[0]):
		year_list[month[0]].append(month[1])
	else:
		year_list[month[0]] = [month[1]]
    return year_list

def questions_without_tag(from_date, to_date, db):
    return db.execute("""
                select questions.title as title, questions.body as question, questions.creation_date,
                questions.owner_id as qowner_id, questions.owner_name as qowner_name, questions.id as qid,
                answers.body as answer, answers.owner_id as aowner_id, answers.owner_name as aowner_name,
                tags, questions.up_vote_count as up_vote_count
                from questions, answers
                where questions.id = answers.question_id
                and questions.creation_date >= ? and questions.creation_date < ?
                order by questions.up_vote_count desc limit 20
                """,(from_date,to_date)).fetchall()