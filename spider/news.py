# -*- coding: utf-8 -*-
__author__ = 'silencedut'
import urllib2
import json
import datetime
from sqlutils import basesqlutil
from util import third_party_api
class Blog(object) :
    def __init__(self,blogid,blog,date):
        self.blogid=blogid
        self.blog=blog
        self.date=date
    def getblogid(self):
        return self.blogid
    def getBlog(self):
        return self.blog
    def getblogdate(self):
        return self.date

class News(object):
    def __init__(self):
        self.news_url = third_party_api.newsapi
        self.blog_url = third_party_api.blogapi
        self.user_agent = 'Dalvik/2.1.0 (Linux; U; Android 5.0.1; MX5 Build/LRX22C'
        self.headers = { 'User-Agent' : self.user_agent}

    def getformatdate(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    def getsameindex(self,lastnewsid,newslist):

        for index in range(len(newslist)) :
            if(str(newslist[index]['articleId'])== lastnewsid) :
                return (index)
        return -1

    def formatdate(self,newsitem):
        newsitem['putdate']=datetime.datetime.fromtimestamp(newsitem['putdate']/1000).strftime('%Y%m%d')
        return newsitem

    def setblogid(self,bloglist):
        for index in range(len(bloglist)) :
            blogItem=json.dumps(bloglist[index]).decode("unicode-escape")
            if(bloglist[index]['putdate']!=1435619291000) :
                try:
                    basesqlutil.news_insert_sql('blog',str(bloglist[index]['articleId']),blogItem,str(bloglist[index]['putdate']))
                except:
                    continue
            print(blogItem)

    def getperblog(self):
        req = urllib2.Request(self.blog_url, headers = self.headers)
        response = urllib2.urlopen(req)
        blog = json.loads(response.read())
        # blog=self.save_per_articlecontent(blog)
        return blog

    def getpernews(self):

        req = urllib2.Request(self.news_url, headers = self.headers)
        response = urllib2.urlopen(req)
        news = json.loads(response.read())
        news=news['articleList']
        imagenews=[]
        for pernews in news :
            detile_url=pernews['articleUrl']
            req = urllib2.Request(detile_url, headers = self.headers)
            response = urllib2.urlopen(req)
            newsdetile = json.loads(response.read())
            imagemap=newsdetile['articleMediaMap']
            if(len(imagemap)>2) :
                pernews['imgUrlList'].append(imagemap['img_0']['url'])
                pernews['imgUrlList'].append(imagemap['img_1']['url'])
                pernews['imgUrlList'].append(imagemap['img_2']['url'])
            imagenews.append(pernews) 
             
        return imagenews

    def save_per_articlecontent(self,news):
        correctnews=[]
        for pernews in news :
            detile_url=pernews['articleUrl']
            newsid=pernews['articleId']
            req = urllib2.Request(detile_url, headers = self.headers)
            response = urllib2.urlopen(req)
            articlecontent={}
            articlecontent['content']=json.loads(response.read())['content']
            try:
                correctnews.append(pernews)
                articlecontent=json.dumps(articlecontent).decode("unicode-escape")
                basesqlutil.newscontent_insert_sql(newsid,articlecontent)
            except:
                continue
        return correctnews



    # only use when init blog table in mysql
    def getallblog(self):
        bloglist=[]
        source=['296.json','297.json']
        for index in range(2):
            self.blog_url = third_party_api.blogapi%(source[index]);
            blogtype=self.getperblog()
            blog=blogtype['articleList'][0]
            while (blog is not None ):
                bloglist.append(blog)
                self.blog_url=blogtype['nextUrl']
                try:
                    blogtype=self.getperblog()
                    blog=blogtype['articleList'][0]
                except:
                    break
        bloglist=sorted(bloglist,key=lambda newsitem:newsitem['putdate'],reverse=False)
        self.setblogid(bloglist)
        return bloglist

    def getdailyblog(self):
        source=['296.json','297.json']
        for index in range(2):
            self.blog_url = third_party_api.blogapi%(source[index]);
            blogtype=self.getperblog()
            blog=blogtype['articleList'][0]
            blogitem=json.dumps(blog).decode("unicode-escape")
            try:
                basesqlutil.news_insert_sql('blog',str(blog['articleId']),blogitem,str(blog['putdate']))
            except:
                continue
        return blog

    def getdailynews(self):
        date=self.getformatdate()
        newslist=[]
        newsjsonlist={}
        source=['268_new.json','270_new.json']

        for index in range(2):
            self.news_url = third_party_api.newsapi%(date,source[index]);
            newslist.extend(self.getpernews())

        newslist=sorted(newslist,key=lambda newsitem:newsitem['putdate'],reverse=True)
        latestnews=basesqlutil.select_latest_news_sql()
        if(latestnews is None) :
            newsjsonlist["nextId"]='0'
            indexofsame=2
        else :
            lastnewsid=latestnews[1]
            newsjsonlist["nextId"]=lastnewsid
            indexofsame =self.getsameindex(lastnewsid,newslist)
            if((indexofsame is not -1) and (indexofsame is not 0)) :
                newslist=newslist[0:indexofsame]
        #newslist=self.save_per_articlecontent(newslist)
        newsjsonlist["newslist"]=newslist
        newsjsonlist=json.dumps(newsjsonlist).decode("unicode-escape")
        if((indexofsame is not 0) and len(newslist)>8) :
            try:
                basesqlutil.news_insert_sql('news',str(newslist[0]['articleId']),newsjsonlist,str(date))
            except:
                return "error"
        return str(newsjsonlist)


