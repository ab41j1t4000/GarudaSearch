from flask import *
from . import app
import sqlite3
import time
from textblob import TextBlob
import spacy
import re
from app import crawler
#import threading
import multiprocessing

nlp = spacy.load("en_core_web_md")


def semanticsearch(str1, str2):
    doc1 = nlp(u'%s' % str1)
    doc2 = nlp(u'%s' % str2)
    return doc1.similarity(doc2)


def waf(query):
    return re.sub('[^A-Za-z0-9.]+', ' ', query)


@app.route('/search', methods=['GET'])
def search():
    correct = ''
    query = request.args.get('q')
    blob = TextBlob(query)
    if blob.correct() != query:
        correct = str(blob.correct())
    if query == '':
        return redirect(url_for(index()))
    try:
        t1 = time.time()
        query = query.replace(' ', '%')
        conn = sqlite3.connect('database/queries.db')
        safequery = waf(query).replace(' ','%')
        stmt = '''select *
        , (case when title like \'%'''+safequery+'''%\' then 1 else 0 end) +
         (case when metadesc like \'%'''+safequery+'''%\' then 1 else 0 end) +
         (case when contents like \'%'''+safequery+'''%\' then 1 else 0 end) as [priority]
        from URLS where title like \'%'''+safequery+'''%\' or metadesc like \'%'''+safequery+'''%\' or contents 
        like \'%'''+safequery+'''%\' order by [priority] desc'''

        results = conn.execute(stmt).fetchall()
        conn.close()
        t2 = time.time()
        return render_template('results.html', suggest=correct, l=len(results), results=results, title=query.replace('%', ' '), t=round(t2-t1, 2))
    except Exception as e:
        return '%s' % e


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/developer', methods=['GET','POST'])
def developer():
    lines = 0
    if request.method == 'GET':
        return render_template('developer.html')
    elif request.method == 'POST':
        if 'crawl' in request.form:
            depth = request.form['depth']
            if depth == "" or depth is None or int(depth)!=depth:
                depth = 100
            unvisitedURL = [line.strip() for line in open('./app/storage/unvisitedURL.txt', 'r')]
            visitedURL = []
            th = multiprocessing.Process(name='crawl', target=crawler.crawl, args=(depth, unvisitedURL, visitedURL))
            th.daemon = True 
            th.start()
            return render_template('developer.html')
        elif 'purge' in request.form:
            try:
                conn = sqlite3.connect('database/queries.db')
                conn.execute('delete from URLS')
                conn.commit()
                conn.close()
                return render_template('developer.html')
            except Exception as e:
                return '%s' % e
        elif 'stop' in request.form:
            for process in multiprocessing.active_children():
                if process.name == 'crawl':
                    print('Process Found')
                    process.kill()
                    print('Process Closed')
                    print(process.is_alive())
                    process.join()
                    print('Process Joined')
                    break
                    
            return render_template('developer.html')
        elif 'check' in request.form:
            try:
                conn = sqlite3.connect('database/queries.db')
                l = len(conn.execute('select * from URLS').fetchall())
                conn.close()
                return render_template('developer.html',lines="URLs crawled: "+str(l))
            except Exception as e:
                return '%s' % e

    else:
        return 'Method Not Allowed'


@app.route('/uploader', methods=['POST'])
def upload_file():
    f = request.files['file']
    f.filename = 'unvisitedURL.txt'
    f.save('./app/storage/'+f.filename)
    return render_template('developer.html')



