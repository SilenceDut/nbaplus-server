# -*- coding: utf-8 -*-
__author__ = 'silencedut'
import urllib2
import json
from bs4 import BeautifulSoup
import datetime
from sqlutils import basesqlutil
from util import third_party_api
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
class Statistics(object):
    def __init__(self):
        self.sina_url =third_party_api.statisticsapi
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        self.headers = { 'User-Agent' : self.user_agent}

    def getperdata(self,htmldata,statkind):
        index=0
        alldata=[]
        for href in htmldata:
            if (index>1)and(index!=len(htmldata)-1)and(index<12):
                perdata={}
                if(href.find('p',{"class":"w_15"}) ==None):
                    index+=1
                    break
                perdata['statkind']=statkind
                perdata['place'] =href.find('p',{"class":"w_15"}).text
                perdata['playerurl']=href.find('p',{"class":"w_45 text_l"}).a.get('href').strip()
                perdata['name'] = href.find('p',{"class":"w_45 text_l"}).text
                perdata['statdata'] = href.find('p',{"class":"w_20"}).text
                perdata['team'] = href.find('p',{"class":"w_20 text_l"}).text
                alldata.append(perdata)
            index+=1
        return alldata

    def getteamsort(self,htmldata):
        allteam=[]
        for href in htmldata:
            perteam={}
            try:
                w_20=href.find_all('p',{"class":"w_20"})
                w_15=href.find_all('p',{"class":"w_15"})
                perteam['sort']=w_15[0].text.strip()
                perteam['win']=w_15[1].text.strip()
                perteam['lose']=w_15[2].text.strip()
                perteam['gap']=w_15[3].text.strip()
                perteam['team']=w_20[0].text.strip()
                if(perteam['team']!='球队'):
                    perteam['teamurl']=w_20[0].a.get('href').strip()
                perteam['winPercent']=w_20[1].text.strip()
                allteam.append(perteam)
            except :
                continue
        return allteam

    def getdata(self,statkind):
        self.sina_url = third_party_api.statisticsapi%statkind;
        req = urllib2.Request(self.sina_url, headers = self.headers)
        statresponse = urllib2.urlopen(req)
        statpage = statresponse.read()
        #encode的作用是将unicode编码转换成其他编码的字符串
        #decode的作用是将其他编码的字符串转换成unicode编码
        unicodepage = statpage.decode("utf-8")
        soup = BeautifulSoup(unicodepage,"lxml")
        allstat={}
        htmldata =soup.find_all(u'ul',{"class":"data_topmate"})
        dailystat=self.getperdata(htmldata[0],statkind)
        everageStat=self.getperdata(htmldata[1],statkind)
        allstat["dailyStat"]=dailystat
        allstat["everageStat"]=everageStat
        return allstat

    def getsort(self):
        self.sina_url = third_party_api.teamsortapi
        req = urllib2.Request(self.sina_url, headers = self.headers)
        statresponse = urllib2.urlopen(req)
        statpage = statresponse.read()
        #encode的作用是将unicode编码转换成其他编码的字符串
        #decode的作用是将其他编码的字符串转换成unicode编码
        unicodepage = statpage.decode("utf-8")
        soup = BeautifulSoup(unicodepage,"lxml")
        teamsort={}
        allteam=[]
        htmldata =soup.find_all(u'ul',{"class":"data_topmate"})
        eastteams=self.getteamsort(htmldata[0])
        westteams=self.getteamsort(htmldata[1])
        allteam.extend(eastteams)
        allteam.extend(westteams)
        teamsort["teamsort"]=allteam
        jsondata=json.dumps(teamsort).decode("unicode-escape")
        basesqlutil.teamsort_insertsql(jsondata)
        return allteam

    def getstat(self):
        allstat=[]
        statkinds =('points','reb','assi','ste','blk','to','goal','three','free')
        for statkind in statkinds:
            perdata=self.getdata(statkind)
            jsondata=json.dumps(perdata).decode("unicode-escape")
            allstat.append(jsondata)
        basesqlutil.stat_insertsql(allstat)
        #basesqlutil.stat_insertSql(allstat,datetime.datetime.now().strftime("%Y%m%d"))
        return allstat


