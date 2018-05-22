from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response

import operator 
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

from ptt.ppt_python1 import pttmain

conn = MongoClient('localhost',27017) 
PttName = 'Gossiping'
today = datetime.date.today()

requests.packages.urllib3.disable_warnings()

load = {
        'from': '/bbs/' + PttName + '/index.html',
        'yes': 'yes'
        }
        
rs = requests.session()
 
# 表单
def search_form(request):
    db = conn.test
    runtitle = []
    for tit in db.ptttitle.find():
            title = tit['title']
            runtitle.append(title)
    return render(request, 'search_form.html',{
        'runtitle': str(runtitle),
    })
 
# 接收请求数据
def search(request):  
    request.encoding='utf-8'
    if 'q' in request.GET:
        m = request.GET['q']
        
        db = conn.test
        
        selectdata = []
        runtitle = []
        
        for select in db.pttselectdata.find():
            if select['keyword'] == m:
                senum = 0
                point = select['point']
                selecttitle = select['title']
                link = select['link']
                for selectright in selectdata:
                    if selecttitle != selectright['title']:
                        senum += 1
                if senum == len(selectdata):
                    selectdata.append({"point":point,"title":selecttitle,"link":link})
        
        sorted_p = sorted(selectdata, key=operator.itemgetter("point"), reverse=True)
        
        for tit in db.ptttitle.find():
            title = tit['title']
            runtitle.append(title)
        return render(request, 'search.html', {
        'runtitle': str(runtitle),
        'data':sorted_p,
    })

    else:
        pttmain()
        message = '資料更新中'
    return HttpResponse(message)
