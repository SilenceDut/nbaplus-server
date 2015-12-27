# -*- coding: utf-8 -*-
__author__ = 'silencedut'
from flask import Flask, g

app = Flask(__name__)
app.debug = True

from sqlutils import basesqlutil
from spider import statistics
from spider import news
from spider import games
from util import api



@app.route('/backend/cron/stat/update', methods=['GET'])
def statupdate():
    allstat=sinadata.getstat()
    teamsort=sinadata.getsort()
    return str(teamsort)

@app.route('/backend/cron/news/update', methods=['GET'])
def newsupdate():
    news=newsdata.getdailynews()
    return str(news)

@app.route('/backend/cron/blog/update', methods=['GET'])
def blogupdate():
    blog=newsdata.getallblog()
    return str(blog)

@app.before_request
def before_request():
    basesqlutil.connect()
    global sinadata
    global newsdata
    global gamesdate
    sinadata=statistics.Statistics()
    newsdata= news.News()
    gamesdate=games.GameDate()


@app.errorhandler(404)
def not_found(error):
    return 'nodata'

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'): g.db.close()

@app.route(api.newsupdate,methods=['GET'])
def get_latestnews(type):
    if(type=='news') :
        latestnews =str(basesqlutil.select_latest_news_sql()[2])
    else :
        latestnews =basesqlutil.select_latest_blog_sql()
    return latestnews

@app.route(api.newsloadmore,methods=['GET'])
def loadMoreNews(type,newsid):
     if(type=='news') :
         loadNews =basesqlutil.select_news_by_id_sql(newsid)
     else :
         loadNews=basesqlutil.select_blogs_by_id_sql(newsid)
     return str(loadNews)

@app.route(api.perstat,methods=['GET'])
def get_perstat(perstat):
    perstat_data=basesqlutil.select_perstat_sql(perstat)
    return perstat_data

@app.route(api.teamsort,methods=['GET'])
def get_teamsort():
    sort_data=basesqlutil.select_teamsort_sql()
    return sort_data

@app.route(api.gamesdate,methods=['GET'])
def get_gamesdate(date):
    games=gamesdate.get_perday_games(date)
    return games


