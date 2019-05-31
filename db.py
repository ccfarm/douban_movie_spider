# coding=utf-8
import sqlite3

DB_PATH = "spider.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE movie
        (
        id int primary key,
        name varchar ,
        year int , 
        score real ,
        votes int
        )
          ''')

    conn.commit()
    conn.close()


def insert_data(movie_id, name, year, score, votes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = u"INSERT INTO movie VALUES ({id}, \"{name}\", {year}, {score}, {votes})".format(
        id=movie_id,
        name=name,
        year=year,
        score=score,
        votes=votes
    )
    print sql
    c.execute(sql)
    conn.commit()
    conn.close()


def update_data(movie_id, name, year, score, votes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = u"UPDATE movie SET name=\"{name}\",year={year}, score={score}, votes={votes} WHERE id={id}".format(
        id=movie_id,
        name=name,
        year=year,
        score=score,
        votes=votes
    )
    c.execute(sql)
    conn.commit()
    conn.close()


def check_exists(movie_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = "select count(*) from movie where id={}".format(movie_id)
    response = c.execute(sql)
    r = response.next()
    conn.commit()
    conn.close()
    return r[0] == 1


def get_some_movie_id():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = "SELECT id FROM movie ORDER BY RANDOM() limit 10"
    r = c.execute(sql)
    l = list()
    for item in r.fetchall():
        l.append(item[0])
    conn.commit()
    conn.close()
    return l


if __name__ == "__main__":
    # d = {
    #     "movie_id": 25890017,
    #     "name": "'哥斯拉2：怪兽之王 Godzilla: King of the Monsters'",
    #     "year": 2019,
    #     "score": 6.9,
    #     "votes": 11820
    # }
    # insert_data(**d)
    #
    # check_exists(25890017)

    # create_table()
    # update_data(25890017, "111", 2019, 1.1, 100)
    get_some_movie_id()