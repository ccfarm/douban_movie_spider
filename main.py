# coding=utf-8
import requests
import argparse
import logging
import logging.handlers
import json
import db
import time
import random

HEADERS = {
    'Host': 'movie.douban.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'utf-8',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

backup_list = list()


def get_data(movie_id):
    url = "https://movie.douban.com/subject/{}".format(movie_id)
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        raise Exception(r.status_code)
    content = r.content
    s = content.find("<span class=\"year\">")
    s = content.find("(", s+1)
    e = content.find("</span>", s+1)
    year = int(content[s+1: e-1])
    s = content.find("<script type=\"application/ld+json\">")
    s = content.find("{", s+1)
    e = content.find("</script>", s+1)
    json_data = json.loads(content[s: e-1], strict=False)
    name = json_data.get(u'name')
    score = json_data.get(u'aggregateRating').get(u'ratingValue')
    if score:
        score = float(score)
    else:
        score = "NULL"
    votes = json_data.get(u'aggregateRating').get(u'ratingCount')
    if votes:
        votes = int(votes)
    else:
        votes = "NULL"
    if db.check_exists(movie_id):
        db.update_data(movie_id, name, year, score, votes)
    else:
        db.insert_data(movie_id, name, year, score, votes)
    logging.info("finish %s %s %s %s %s", movie_id, name, year, score, votes)
    global backup_list
    if len(backup_list) < 100:
        find_next(content)


def find_next(content):
    global backup_list
    i = 0
    while content.find("movie.douban.com/subject/", i) > 0:
        s = content.find("movie.douban.com/subject/", i)
        s = content.find("subject/", s+1)
        s += 8
        e = s
        while e < len(content) and '0' <= content[e] <= '9':
            e += 1
        tmp = content[s: e]
        if tmp not in backup_list and not db.check_exists(tmp):
            backup_list.append(tmp)
        i = s


def main():
    ap = argparse.ArgumentParser(description='Abase Proxy Checker')
    ap.add_argument('--debug', action='store_true', help='In debug mode')
    args = ap.parse_args()

    if not args.debug:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.handlers.TimedRotatingFileHandler('spider.log')
        handler.setFormatter(logging.Formatter('[%(asctime)s %(levelname)-5s %(process)d %(filename)s] %(message)s'))
        logger.addHandler(handler)
    else:
        logging.basicConfig(level=logging.INFO)

    global backup_list

    while True:
        if len(backup_list) == 0:
            backup_list.extend(db.get_some_movie_id())
        movie_id = backup_list.pop()
        try:
            get_data(movie_id)
        except Exception as e:
            logging.error("get_data error movie_id: %s error: %s", movie_id, e)
        time.sleep(random.randint(10, 50))


if __name__ == "__main__":
    main()
    # get_data(6082518)
    # get_data(1418189)