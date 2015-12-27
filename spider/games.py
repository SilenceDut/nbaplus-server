__author__ = 'silencedut'
import urllib2
import json
from bs4 import BeautifulSoup
import lxml
import datetime
from util import third_party_api
class GameDate(object):
    def __init__(self):
        self.gamedate_url =third_party_api.gamedateapi
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        self.headers = { 'User-Agent' : self.user_agent}

    def getformatdate(self):
        print(datetime.datetime.now().strftime("%Y-%m-%d"))
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def get_perday_games(self,date):
        self.gamedate_url=self.gamedate_url%date
        req = urllib2.Request(self.gamedate_url, headers = self.headers)
        gamesresponse = urllib2.urlopen(req)
        gamespage = gamesresponse.read()
        unicodepage = gamespage.decode("utf-8")
        soup = BeautifulSoup(unicodepage,"lxml")
        htmldata =soup.find_all('div',{"class":"livemate_items"})
        # print(htmldata)
        gamesjson={}
        games=self.getteamsort(htmldata,date)
        gamesjson["games"]=games
        jsondata=json.dumps(gamesjson).decode("unicode-escape")
        return jsondata

    def getteamsort(self,htmldata,date):
        allteam=[]
        game={}
        game['type']=0
        game['date']=date[5:10]
        game['statusText']=''
        game['statusUrl']=''
        game['stateText']=''
        game['stateUrl']=''
        game['status']=''
        game['leftTeam']=''
        game['rightTeam']=''
        game['leftScore']=''
        game['rightScore']=''
        allteam.append(game)
        for href in htmldata:
            game={}
            game['status'] = href.find('div',{'class':'livemate_t'}).text.strip()
            classgameleft=href.find('div',{'class':'livemate_l'})
            game['leftTeam']=classgameleft.find('p',{'class':'live_top_t'}).text.strip()
            try:
                game['leftScore']=classgameleft.find('p',{'class':'live_num_t'}).text.strip()
            except:
                game['leftScore']=0
            classgamemid=href.find('div',{'class':'livemate_m'})
            if classgamemid.find('p',{'class':'live_top_t'}) is not None:
                game['status']=classgamemid.find('p',{'class':'live_top_t'}).text.strip()
                element_a=classgamemid.find('p',{'class':'live_linkbox'}).find_all('a')
                if(len(element_a)==1) :
                    game['statusText']=element_a[0].text.strip()
                    game['statusUrl']=element_a[0].get('href')
                    game['stateText']=''
                    game['stateUrl']=''
                else:
                    game['statusText']=element_a[0].text.strip()
                    game['statusUrl']=element_a[0].get('href')
                    game['stateText']=element_a[1].text.strip()
                    game['stateUrl']=element_a[1].get('href')
            else:
                game['statusUrl']=classgamemid.find_all('p',{'class':'live_linkbox'})[0].a.get('href')
                game['stateText']=classgamemid.find_all('p',{'class':'live_linkbox'})[1].text.strip()
                game['stateUrl']=classgamemid.find_all('p',{'class':'live_linkbox'})[1].a.get('href')
            classgameright=href.find('div',{'class':'livemate_r'})
            game['rightTeam']=classgameright.find('p',{'class':'live_top_t'}).text.strip()
            try:
                game['rightScore']=classgameright.find('p',{'class':'live_num_t'}).text.strip()
            except:
                game['rightScore']=0
            game['type']=1
            game['date']=date[5:10]
            allteam.append(game)
        return allteam