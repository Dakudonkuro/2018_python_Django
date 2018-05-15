
# coding: utf-8
# -*- coding: utf-8 -*-
# In[7]:
# -*- coding: utf-8 -*-
import re
import sys
import nltk
import math
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
import datetime
import string

import jieba
import jieba.posseg as pseg
import jieba.analyse

import json

from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn import feature_extraction
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer

from operator import itemgetter, attrgetter

from nltk.corpus import reuters
from math import log 
from nltk import WordNetLemmatizer

from pymongo import MongoClient 
conn = MongoClient('localhost',27017) 
print ('connect db ok')
 
PttName = 'Gossiping'
today = datetime.date.today()

pushg = {}
pushb = {}

def writemain_db(nosqlmain):
    #print (nosqlmain)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.pttmain.find():
            if(nosqlmain == post):
                nt = nt + 1
    if(nt == 0):
        db.pttmain.insert(nosqlmain)
        
def writemainjie_db(nosqlmainjie):
    #print (nosqlmain)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.pttmainjie.find():
            if(nosqlmainjie == post):
                nt = nt + 1
    if(nt == 0):
        db.pttmainjie.insert(nosqlmainjie)
    
def writetitle_db(nosqltitle):
    #print (nosqlmain)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.ptttitle.find():
            if(nosqltitle == post):
                nt = nt + 1
    if(nt == 0):
        db.ptttitle.insert(nosqltitle)

def writetitlejie_db(nosqltitlejie):
    #print (nosqlmain)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.ptttitlejie.find():
            if(nosqltitlejie == post):
                nt = nt + 1
    if(nt == 0):
        db.ptttitlejie.insert(nosqltitlejie)

def writepush_db(nosqlpush):
    #print (nosqlpush)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.pttpush.find():
            if(nosqlpush == post):
                nt = nt + 1
    if(nt == 0):
        db.pttpush.insert(nosqlpush)

def writepushjie_db(nosqlpushjieex):
    #print (nosqlpush)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.pttpushjie.find():
            if(nosqlpushjieex == post):
                nt = nt + 1
    if(nt == 0):
        db.pttpushjie.insert(nosqlpushjieex)
    
def writepushid_db(nosqlpushid):
    #print (nosqlpush)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.pttpushid.find():
            if(nosqlpushid == post):
                nt = nt + 1
    if(nt == 0):
        db.pttpushid.insert(nosqlpushid)
    
def writelink_db(nosqllink):
    #print (nosqllink)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.pttlink.find():
            if(nosqllink == post):
                nt = nt + 1
    if(nt == 0):
        db.pttlink.insert(nosqllink)

def writepageurl_db(nosqlpageurl):
    #print (nosqlpageurl)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.pttpageurl.find():
            if(nosqlpageurl == post):
                nt = nt + 1
    if(nt == 0):
        db.pttpageurl.insert(nosqlpageurl)
    
def writetime_db(nosqltime):
    #print (nosqlmain)
    db = conn.test 
    nt = 0
    for post in db.ptttime.find():
            if(nosqltime == post):
                nt = nt + 1
    if(nt == 0):
        db.ptttime.insert(nosqltime)
def number_db(nosqlnum):
    db = conn.test
    db.pttnum.insert(nosqlnum)

def writejiebatf_db(nosqljiebatf):
    #print (nosqlmain)
    db = conn.test 
    nt = 0
    for post in db.pttjiebatf.find():
            if(nosqljiebatf == post):
                nt = nt + 1
    if(nt == 0):
        db.pttjiebatf.insert(nosqljiebatf)

def writeaar_db(nosqlaar):
    #print (nosqlmain)
    db = conn.test 
    db.pttaar.remove({})
    db.pttaar.insert(nosqlaar)
        
def writearr_db(nosqlarr):
    #print (nosqlmain)
    db = conn.test 
    db.pttarr.remove({})
    db.pttarr.insert(nosqlarr)
    
requests.packages.urllib3.disable_warnings()

load = {
    'from': '/bbs/' + PttName + '/index.html',
    'yes': 'yes'
}


rs = requests.session()


def getPageNumber(content):
    startIndex = content.find('index')
    endIndex = content.find('.html')
    pageNumber = content[startIndex + 5: endIndex]
    return pageNumber


def over18(board):
    res = rs.get('https://www.ptt.cc/bbs/' + board + '/index.html', verify=False)

    if (res.url.find('over18') > -1):
        print("18禁網頁")
        load = {
            'from': '/bbs/' + board + '/index.html',
            'yes': 'yes'
        }
        res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
        return BeautifulSoup(res.text, 'html.parser')
    return BeautifulSoup(res.text, 'html.parser')


    
def crawler(url_list,a,arr,aar):
    count, g_id = 0, 0
    total = len(url_list)
    while url_list:
        url = url_list.pop(0)
        res = rs.get(url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')

        if (soup.title.text.find('Service Temporarily') > -1):
            url_list.append(url)
            # print u'error_URL:', url
            # print u'error_URL head:', soup.title.text
            time.sleep(1)
        else:
            count += 1
            # print u'OK_URL:', url
            # print u'OK_URL head:', soup.title.text
            for r_ent in soup.find_all(class_="r-ent"):

                link = r_ent.find('a')
                #print('link')
                #print(link)
                if (link):

                    URL = 'https://www.ptt.cc' + link['href']
                    
                    l={"board": PttName,"link":str(URL),"crawldate":str(today)}
                    writelink_db(l)
                    g_id = g_id + 1
                    number={"number":g_id}
                    number_db(number)

                    time.sleep(0.1)

                    
                    parseGos(URL,a,arr,aar)
                    
            print("download: " + str(100 * count / total) + " %.")

        time.sleep(0.1)


def checkformat(soup, class_tag, data, index, link):

    try:
        content = soup.select(class_tag)[index].text
    except Exception as e:
        print('checkformat error URL', link)
        
        # print 'checkformat:',str(e)
        content = "no " + data
    return content


def parseGos(link,a,arr,aar):
    
    jiebatf = {}
    
    res = rs.get(link, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    

    # author  = soup.select('.article-meta-value')[0].text
    author = checkformat(soup, '.article-meta-value', 'author', 0, link)
    # print 'author:',author
    

    # board  = soup.select('.article-meta-value')[1].text
    board = checkformat(soup, '.article-meta-value', 'board', 1, link)
    # print (board)


    # title = soup.select('.article-meta-value')[2].text
    title = checkformat(soup, '.article-meta-value', 'title', 2, link)
    # print 'title:',title

    jiebatf[0] = {"文章標題：":title}
    
    
    # date = soup.select('.article-meta-value')[3].text
    date = checkformat(soup, '.article-meta-value', 'date', 3, link)
    # print 'date:',date
    
    
    try:
        targetIP = u'※ 發信站: 批踢踢實業坊'
        ip = soup.find(string=re.compile(targetIP))
        ip = re.search(r"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*", ip).group()
    except:
        ip = "ip is not find"
    # print 'ip:',ip


    try:
        content = soup.find(id="main-content").text
        target_content = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
        content = content.split(target_content)
        content = content[0].split(date)
        main_content = content[1].replace('\n', '  ')
        # print 'content:',main_content
    except Exception as e:
        main_content = 'main_content error'
        print('main_content error URL' , link)
        # print 'main_content error:',str(e)


    lastt = {}
    
    num, g, b, n, message,lasttime = 0, 0, 0, 0, {}, {}

    for tag in soup.select('div.push'):
        try:

            push_tag = tag.find("span", {'class': 'push-tag'}).text
            #print ("push_tag:",push_tag)

            # push_userid 推文使用者id
            push_userid = tag.find("span", {'class': 'push-userid'}).text
            #print ("push_userid:",push_userid)


            push_content = tag.find("span", {'class': 'push-content'}).text
            #push_content = push_content[1:]
            #print ("push_content:",push_content)

            push_ipdatetime = tag.find("span", {'class': 'push-ipdatetime'}).text
            push_ipdatetime = push_ipdatetime.rstrip()
            #print ("push-ipdatetime:",push_ipdatetime)
            
            num += 1
            
            message[num] = {"push_tag": push_tag, "push_userid": push_userid,
                            "push_content": push_content, "push_ipdatetime": push_ipdatetime}
            
            lasttime[num] = {"push_ipdatetime": push_ipdatetime}
            message2 = {"board": board,"link":link,"push_tag": push_tag,"push_content": push_content, "push_ipdatetime": push_ipdatetime,"crawldate":str(today)}
            
            cutpush(push_content)
            
            writepushid_db({"userid": push_userid})
            writepush_db(message2)

            
            lastt = push_ipdatetime
            
            #print('pushlink',link)
            #print('pushmessage',message)
            
        
            #print()
            #print(type(message[num]))
            #print(message)


            if push_tag == u'推 ':
                g += 1
            elif push_tag == u'噓 ':
                b += 1
            else:
                n += 1
        except Exception as e:
            print("push error URL:" + link)
            
            # print "push error:",str(e)
        #w = g+b+n
    #messageNum = {"g": g, "b": b, "n": n, "all": num}
    #print(type(messageNum))
    
    lasttime1 = {"link":link,"last time": lastt}
    writetime_db(lasttime1)
    p={"board": board,"author": author, "title": title, "date": date,"ip": ip, "link":link,"main_content": main_content,"crawldate":str(today)}
    p1={"title": title}
    #pushnum={"link":link,"pushnum": messageNum}
    #print(p)
    writemain_db(p)
    writetitle_db(p1)
    if(link!="https://www.ptt.cc/bbs/Gossiping/M.1510415718.A.D77.html"):
        if(title!="no title"):
            cutword(main_content,title,jiebatf,a,arr,aar,link)
    #print('ptitle',title)
    #print('plink',link)
        
    '''
    print('title')
    
    m=message
    print(m)
    print('push')
    print(message)
    print('messageNum')
    print(messageNum)
    print("a_ID")
    print(g_id)
    print('board')
    print (board)
    print("b_作者")
    print(author)
    print("c_標題")
    print(title)
    print('link')
    print(link)
    print("d_日期")
    print(date)
    print("e_ip")
    print(ip)
    print("f_內文")
    print(main_content)
    
    print("g_推文")
    print(message)
    print("h_推文總數")
    print(messageNum)
    '''

def tf(data,ni):
    nimtf = {}
    chineseFilter1 =  [u'．',u' ',u'<',u'>',u'　',u'的',u'〔',u'〕',u'〝',u'〞',u'『 ',u'』',u'〈',u'〉',u'\\',u'（', u'）',u'[',u']',u'～',u'u3000',u'"',u'&gt',u'&lt',u';',u'，', u'。', u'、', u'；', u'：', u'?', u'「', u'」', u'%', u'.', u',', u'？', u'-', u'~',u'!',u'！', u'&nbsp', u'<BR>', u'“', u'”', u'【', u'】', u'《', u'》',u'：',u':',u'+',u'●',u'(',u')',u'；']
    for x in range(ni):
        m = 0
        tfnumber = 0
        for cfr in chineseFilter1:
            if data[x]==cfr:
                tfnumber += 1
        for y in range(ni):
            if data[x] == data[y]:
                if tfnumber == 0:
                    m += 1
        nimtf[x] = m
    return nimtf

def cutpush(push_content):
    cutpush=0
    cutpushdata = {}
    wordspush = jieba.cut(push_content, cut_all=False)
    for  wordpush in wordspush:
        if wordpush != " ":     
            cutpushdata[cutpush] = wordpush
            cutpush += 1
    wordpushdata = {"wordcut":str(cutpushdata)}
    writepushjie_db(wordpushdata)
    
def cutword(main_content,title,jiebatf,a,arr,aar,link):
    cutmain=0
    anum = 0
    cutmaindata = {}
    cutsmaindata = {}
    jieba.set_dictionary('dict.txt.big')
    wordsmain = jieba.cut(main_content, cut_all=False)
    for  wordmain in wordsmain:
        mnorepeat=0
        if wordmain != " ":     
            cutsmaindata[cutmain] = wordmain
            for notrepeat in cutmaindata:
                if wordmain == cutmaindata[notrepeat]:
                    mnorepeat += 1
            if mnorepeat == 0:
                cutmaindata[cutmain] = wordmain
                cutmain += 1
            if a == wordmain:
                anum += 1
    if anum >= 5:
        arr.append({"標題":title,"網址":link})
    wordmaindata = {"wordcut":str(cutsmaindata)}
    writemainjie_db(wordmaindata)
    
    cuttitle=0
    rnum = 0
    cuttitledata = {}
    cutstitledata = {}
    wordstitle = jieba.cut(title, cut_all=False)
    for wordtitle in wordstitle:
        tnorepeat=0
        if wordtitle != " ":   
            cutstitledata[cuttitle] = wordtitle
            for notrepeat in cuttitledata:
                if wordtitle == cuttitledata[notrepeat]:
                    tnorepeat += 1
            if tnorepeat == 0:
                cuttitledata[cuttitle] = wordtitle
                cuttitle += 1
            if a == wordtitle:
                rnum += 1
    if rnum > 0:
        aar.append({"標題":title,"網址":link})
    wordtitledata = {"wordcut":str(cutstitledata)}
    writetitlejie_db(wordtitledata)
    tfd = tf(cuttitledata,cuttitle)
    tftfin = {}
    for tfmathone in range(cuttitle):
        test = 0
        for tfmathtwo in range(cuttitle):
            test = test + tfd[tfmathtwo]
        tftfin[tfmathone] = tfd[tfmathone]/test
    print(title+'------標題的tf值(不包含tf小於0.1)')
    for eee in range(cuttitle):
        if tftfin[eee] >= 0.1:
            print("[",cuttitledata[eee],"]的tf:",tftfin[eee])
    titletidf = jieba.analyse.extract_tags(title,5)
    print(title+"___的前5個標題關鍵字"+",網址:"+link)
    print(",".join(titletidf))
    jiebatf[1] = {"標題的5個關鍵字":titletidf}
    mfd = tf(cutmaindata,cutmain)
    tfmfin = {}
    for tfmathone in range(cutmain):
        test = 0
        for tfmathtwo in range(cutmain):
            test = test + mfd[tfmathtwo]
        tfmfin[tfmathone] = mfd[tfmathone]/test
    print(title+'------內文標題的tf值(不包含tf小於0.05)')
    for eee in range(cutmain):
        if tfmfin[eee] >= 0.05:
            print("[",cutmaindata[eee],"]的tf:",tfmfin[eee])
    maintidf = jieba.analyse.extract_tags(main_content,10)
    print(title+"___的前10個內文關鍵字"+",網址:"+link)
    print(",".join(maintidf))
    jiebatf[2] = {"內文的10個關鍵字":maintidf}
    
    wordjiebatf = {"文章關鍵字":str(jiebatf)}
    writejiebatf_db(wordjiebatf)


def pttmain(key):  
        
       db = conn.test
       db.pttaar.drop()
       db.pttarr.drop()
  
        ParsingPage = 10
    
        start_time = time.time()
        print (time.localtime( start_time ))
    
        a = key
    
        arr = []
        aar = []
    
        print('Start parsing ' + PttName + '....')
    

        soup = over18(PttName)
        ALLpageURL = soup.select('.btn.wide')[1]['href']
        #print('ALLpageURL')
        #print(ALLpageURL)

        ALLpage = int(getPageNumber(ALLpageURL)) + 1
        index_list = []
        for index in range(ALLpage, ALLpage - int(ParsingPage), -1):
            page_url = 'https://www.ptt.cc/bbs/' + PttName + '/index' + str(index) + '.html'
            writepageurl_db({"board": PttName,"page_url":page_url,"crawldate":str(today)})
            #print('page_url',page_url)
            index_list.append(page_url)
            break

        #store('[\n')
        #print(index_list)
        crawler(index_list,a,arr,aar)
        global maintitle
        maintitle = []
        '''
        # 移除最後一個  "," 號
        with open(fileName, 'r') as f:
            content = f.read()
        with open(fileName, 'w') as f:
            f.write(content[:-1] + "\n]")
        '''

        print('有搜尋字的標題:')
        print(str(aar))
        if(aar!=[]):
            writeaar_db(aar)  
        print('有搜尋字的內文:')
        print(str(arr))
        if(arr!=[]):
            writearr_db(arr)
    
        print("爬蟲結束...")
        print("execution time:" + str(time.time() - start_time) + "s")
    


# In[19]:

import time
import datetime
#今天日期 (2006-11-18)
today = datetime.date.today()
print (str(today))




