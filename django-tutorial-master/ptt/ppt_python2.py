
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


def writetitlesort_db(nosqltitlesort):
    #print (nosqlmain)
    db = conn.test 
    #print('connect pttdb')
    nt = 0
    for post in db.ptttitlesort.find():
            if(nosqltitlesort == post):
                nt = nt + 1
    if(nt == 0):
        db.ptttitlesort.insert(nosqltitlesort)
    
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


    
def crawler(url_list):
    count, g_id = 0, 0
    testid = 0
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
                testid+=1
                link = r_ent.find('a')
                #print('link')
                #print(link)
                if (link):

                    URL = 'https://www.ptt.cc' + link['href']
                        
                    print(URL)
                    
                    g_id = g_id + 1

                    time.sleep(0.1)

                    parseGos(URL)
                    
            print("downloadstart")        
            print("download: " + str(100 * count / total) + " %.")

        time.sleep(0.1)
        print("downloadend") 


def checkformat(soup, class_tag, data, index, link):

    try:
        content = soup.select(class_tag)[index].text
    except Exception as e:
        print("checkformatstart")
        
        print('checkformat error URL', link)
        
        # print 'checkformat:',str(e)
        content = "no " + data
        print("checkformatend")
    return content


def parseGos(link):
    
    res = rs.get(link, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    title = checkformat(soup, '.article-meta-value', 'title', 2, link)
    
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
        # print 'content:',main_content
    except Exception as e:
        print('main_content error URL' , link)
        # print 'main_content error:',str(e)

    
    g, b, n = 0, 0, 0

    for tag in soup.select('div.push'):
        try:

            push_tag = tag.find("span", {'class': 'push-tag'}).text
            #print ("push_tag:",push_tag)
            
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
    
    w = g + b + n

    p2={"title": title,"hot": w,"link":link}
    #pushnum={"link":link,"pushnum": messageNum}
    #print(p)

    writetitlesort_db(p2)

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

def pttsort():
        '''
        db = conn.test
        
        db.pttjiebatf.drop()
        db.pttlink.drop()
        db.pttmain.drop()
        db.pttnum.drop()
        db.pttpageurl.drop()
        db.pttpush.drop()
        db.pttpushid.drop()
        db.pttpushjie.drop()
        db.ptttime.drop()
        db.pttmainjie.drop()
        db.ptttitlejie.drop()
        db.ptttitle.drop()
        db.pttjiebatf.drop()
        db.pttselectdata.drop()
        '''
        
        ParsingPage =3
    
        start_time = time.time()
        print (time.localtime( start_time ))
    
        print('Start parsing ' + PttName + '....')
    

        soup = over18(PttName)
        ALLpageURL = soup.select('.btn.wide')[1]['href']
        #print('ALLpageURL')
        #print(ALLpageURL)

        ALLpage = int(getPageNumber(ALLpageURL)) + 1
        index_list = []
        for index in range(ALLpage, ALLpage - int(ParsingPage), -1):
            page_url = 'https://www.ptt.cc/bbs/' + PttName + '/index' + str(index) + '.html'
            #print('page_url',page_url)
            index_list.append(page_url)
            
        #store('[\n')
        #print(index_list)
        crawler(index_list)
        global maintitle
        maintitle = []
        '''
        # 移除最後一個  "," 號
        with open(fileName, 'r') as f:
            content = f.read()
        with open(fileName, 'w') as f:
            f.write(content[:-1] + "\n]")
        '''
    
        print("爬蟲結束...")
        print("execution time:" + str(time.time() - start_time) + "s")
    


# In[19]:

import time
import datetime
#今天日期 (2006-11-18)
today = datetime.date.today()
print (str(today))




