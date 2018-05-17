from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response

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

from ptt.ppt_python import pttmain

conn = MongoClient('localhost',27017) 
PttName = 'Gossiping'
today = datetime.date.today()

pushg = {}
pushb = {}
        
db = conn.test 

db.pttaar.drop()
db.pttarr.drop()

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
        
        pttmain(m)
        
        db = conn.test
        
        messageaar = []
        messagearr = []
        runtitle = []
        for aarr in db.pttaar.find():
            messageaar.append(aarr)
        for arar in db.pttarr.find():
            messagearr.append(arar)
        for tit in db.ptttitle.find():
            title = tit['title']
            runtitle.append(title)
        return render(request, 'search.html', {
        'aardata': messageaar,
        'arrdata': messagearr,
        'runtitle': str(runtitle),
    })

    else:
        message = '你沒有輸入'
    return HttpResponse(message)
