#!/usr/bin/python3
from bs4 import *
import sqlite3
import requests
import re
from threading import *
from textblob import TextBlob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--check", help="check the number of URLs crawled",required=False,action="store_true")
parser.add_argument("--purge", help="delete the crawled URLs. Action is irreversible",required=False,action="store_true")
parser.add_argument("--run", help="run the crawler",required=False,action="store_true")
parser.add_argument("--depth", help="specify the depth of crawl",default=50)
parser.add_argument("--path", help="specify the path of the file containing unvisited links",default='./app/storage/unvisitedURL.txt')
args = parser.parse_args()


def crawl(depth, unvisitedURL, visitedURL):
    l = 0
    while len(unvisitedURL) != 0 and depth !=0:
        print(len(unvisitedURL)," urls left...")
        print(l," urls crawled...")
        url = unvisitedURL.pop(0)
        if url in visitedURL:
            pass
        else:
            visitedURL.append(url)
        try:
            page = requests.get(url)
        except:
            continue
        if page.status_code >= 400:
            continue
       # print(page)
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            conn = sqlite3.connect('database/queries.db')
            title = soup.find('title').text
            desc = soup.find('meta', attrs={'name':'description'})
            if desc is None:
                desc = soup.find('meta', attrs={'name':'Description'})
                if desc is None:
                    desc = "No description provided"
                else:
                    desc = desc['content']
            else:
                desc = desc['content']
            blob = TextBlob(soup.find('body').text)
            content = str(list(dict.fromkeys(blob.words)))
            conn.execute("INSERT INTO URLS VALUES(?,?,?,?)", (url, title, desc, content))
            conn.commit()
            l = len(conn.execute("SELECT * FROM URLS").fetchall())
            conn.close()
            for link in soup.find_all('form'):
                if link['action'] != 'action':
                    temp = link['action']
                    if re.search('http', temp) is None and re.search('www', temp) is None and re.search('com',temp) is None and re.search('org',temp) is None:
                        temp = url+link['action']
                    if re.search('http', temp) is None:
                        temp = 'https:' + temp
                    unvisitedURL.append(temp)
            for link in soup.find_all('a'):
                temp = link['href']
                if temp != '#':
                    if re.search('www', temp) is None and re.search('com', temp) is None and re.search('org', temp) is None:
                        temp = url + link['href']
                    if re.search('http', temp) is None:
                        temp = 'https:'+temp
                    unvisitedURL.append(temp)
            depth -= 1
        except sqlite3.IntegrityError:
            pass
        except KeyError:
            print("Key not found! Skipping...")
            pass

        except Exception as e:
            pass
        
        except KeyboardInterrupt:
            file = open('./app/storage/unvisitedURL.txt', 'r+')
            file.truncate(0)
            file = open('./app/storage/unvisitedURL.txt', 'w')
            for link in unvisitedURL:
                file.write(link+'\n')
            return
    print("DONE!")
    file = open('./app/storage/unvisitedURL.txt', 'r+')
    file.truncate(0)
    file = open('./app/storage/unvisitedURL.txt', 'w')
    for link in unvisitedURL:
        file.write(link + '\n')

def divide(l, n):
      
    for i in range(0, len(l), n): 
        yield l[i:i + n]

if __name__ == '__main__':
    if args.purge is False and args.run is False and args.check is False:
        print("USAGE:")
        print("To delete the crawled URLs: python3 crawler.py --purge")
        print("To crawl URLs: python3 crawler.py --run --path [path to URL list] --depth [depth of crawl]")
        print("To see the number of crawled URLs: python3 crawler.py --check")
    if args.check is True:
        try:
            conn = sqlite3.connect('database/queries.db')
            x = conn.execute('select COUNT(*) from URLS').fetchall()[0][0]
            conn.commit()
            conn.close()
            print(x," URLs crawled!")
        except Exception as e:
            print("Error: ",e)
    if args.purge is True:
        try:
            conn = sqlite3.connect('database/queries.db')
            conn.execute('delete from URLS')
            conn.commit()
            conn.close()
            print("DATABASE PURGED!")
        except Exception as e:
            print("Error: ",e)

    if args.run is True:
        unvisitedURL = [line.strip() for line in open(args.path, 'r')]
        l = len(unvisitedURL)
        dividedList = divide(unvisitedURL,l//2)
        
        for i in dividedList:
            visitedURL = []
            t = Thread(target=crawl,args=(int(args.depth),i,visitedURL))
            t.start()
