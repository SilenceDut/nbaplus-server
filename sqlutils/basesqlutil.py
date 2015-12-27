# -*- coding: utf-8 -*-
__author__ = 'silencedut'
import MySQLdb
import json
from flask import g
from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def connect():
    status=0
    try:
        g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                           MYSQL_DB, port=int(MYSQL_PORT))
        g.db.ping(True)
        dbc=g.db.cursor()
        g.db.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')
    except Exception,e:
        status=1
    return status

def select_teamsort_sql():
    c = g.db.cursor()
    sql ="select sort from teamsort "
    c.execute(sql)
    sort_data=c.fetchone()
    return sort_data

def select_perstat_sql(colum):
    c = g.db.cursor()
    sql ="select %s from nbastat "%(colum)
    c.execute(sql)
    stat_data=c.fetchone()
    return stat_data
def select_latest_news_sql():
    c = g.db.cursor()
    sql ="select * from news order by id DESC limit 1"
    c.execute(sql)
    news=c.fetchone()
    return news
def select_latest_blog_sql():
    c = g.db.cursor()
    sql ="select * from blog order by id DESC limit 10"
    c.execute(sql)
    results=c.fetchall()
    blogs=[]
    blogjsonlist={}
    for perblog in results :
        blogs.append(json.loads(perblog[2]))
    blogjsonlist['nextId']=results[4][1]
    blogjsonlist['newslist']=blogs
    blogs=json.dumps(blogjsonlist).decode("unicode-escape")
    return blogs
def select_news_by_id_sql(newsid):
    c = g.db.cursor()
    sql ="select * from news where newsid =%s" %(newsid)
    c.execute(sql)
    news=c.fetchone()
    return str(news[2])
def select_blogs_by_id_sql(newsid):
    c = g.db.cursor()
    sql ="select  * from blog where newsid =%s" %(newsid)
    c.execute(sql)
    results=c.fetchone()
    index=results[0]
    sql ="select  * from blog where id< %d and id>%d" %(index,index-9)
    c.execute(sql)
    results=c.fetchall()
    blogs=[]
    blogjsonlist={}
    for index in range(8) :
        blogs.append(json.loads(results[7-index][2]))
   
    blogjsonlist['nextId']=results[0][1]
    blogjsonlist['newslist']=blogs
    blogs=json.dumps(blogjsonlist).decode("unicode-escape")
    return blogs
def select_all_blog_sql(colum,table_name):
    c = g.db.cursor()
    sql ="select %s from %s"%(colum,table_name)
    c.execute(sql)
    stat_data=c.fetchall()
    return stat_data
def news_insert_sql(table_name,newsid,newslist,date):
    c = g.db.cursor()
    sql ="insert into %s (newsid,newslist,date) VALUES ('%s','%s','%s')" % (table_name,newsid,newslist,date)
    c.execute(sql)

def newscontent_insert_sql(newsid,content):
    c = g.db.cursor()
    sql ="insert into articlecontent (articleId,content) VALUES ('%s','%s')" % (newsid,content)
    c.execute(sql)

def teamsort_insertsql(teamsort):
    c = g.db.cursor()
    delete_sql('teamsort')
    sql ="insert into teamsort VALUES ('%s')" % (teamsort)
    c.execute(sql)

def stat_insertsql(allstat):
    c = g.db.cursor()
    delete_sql('nbastat')
    sql ="insert into nbastat VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (allstat[0],allstat[1],allstat[2],allstat[3],allstat[4],allstat[5],allstat[6],allstat[7],allstat[8])
    c.execute(sql)

def delete_sql(table_name):
    c = g.db.cursor()
    c.execute('delete from %s'%(table_name))
