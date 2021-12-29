from flask import *
from . import app
import sqlite3
import time
from textblob import TextBlob
import spacy
import re
import multiprocessing
from flask_paginate import Pagination, get_page_args

nlp = spacy.load("en_core_web_md")


def semanticsearch(str1, str2):
    doc1 = nlp(u'%s' % str1)
    doc2 = nlp(u'%s' % str2)
    return doc1.similarity(doc2)

def keyword_extract(text):
    result = []
    punctuation = ['?','.',',',':',';','!']
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    doc = nlp(text.lower()) 
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
                
    return result

def get_pages(data,offset=0, per_page=10):

    return data[offset: offset + per_page]

def waf(query):
    return re.sub('[^A-Za-z0-9.]+', ' ', query)


@app.route('/search', methods=['GET'])
def search():
    correct = ''
    if request.args.get('q') is not None:
        query = request.args.get('q')
    else:
        query = ''
    blob = TextBlob(query)
    if blob.correct() != query:
        correct = str(blob.correct())
    if query == '':
        return render_template('index.html')
    else:
        pass
    try:
        t1 = time.time()
        queryExtracted = keyword_extract(query)
        queryExtracted = ' '.join(queryExtracted)
        queryExtracted = queryExtracted.replace(' ', '%')
        conn = sqlite3.connect('database/queries.db')
        safequery = waf(queryExtracted).replace(' ','%')
        stmt = '''select *
        , (case when title like \'%'''+safequery+'''%\' then 2 else -1 end) +
         (case when metadesc like \'%'''+safequery+'''%\' then 2 else -1 end) +
         (case when contents like \'%'''+safequery+'''%\' then 0.5 else -1 end) as [priority]
        from URLS where title like \'%'''+safequery+'''%\' or metadesc like \'%'''+safequery+'''%\' or contents 
        like \'%'''+safequery+'''%\' order by [priority] desc'''

        results = conn.execute(stmt).fetchall()
        conn.close()
        t2 = time.time()
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        pagination_pages = get_pages(results,offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=len(results),css_framework='bootstrap4')
        return render_template('results.html', suggest=correct, l=len(results), results=pagination_pages,page=page,per_page=per_page,pagination=pagination, title=query, t=round(t2-t1, 2))
    except Exception as e:
        return '%s' % e


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')






