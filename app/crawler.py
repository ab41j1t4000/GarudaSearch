from bs4 import *
import sqlite3
import requests
import re
from textblob import TextBlob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--depth", help="specify the depth of crawl")
parser.add_argument("--path", help="specify the path of the file containing unvisited links")
args = parser.parse_args()


def crawl(depth, unvisitedURL, visitedURL):
    while len(unvisitedURL) != 0 and depth !=0:
        print(len(unvisitedURL)," urls left...")
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
            conn.close()
            for link in soup.find_all('form'):
                if link['action'] != 'action':
                    temp = link['action']
                    if re.search('http', temp) is None and re.search('www', temp) is None and re.search('com',temp) is None and re.search('org',temp) is None:
                        temp = url+link['action']
                    if re.search('http', temp) is None:
                        temp = 'https:' + temp
                    unvisitedURL.append(temp)
                #print(unvisitedURL)
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
            print("Error: ", e)
            pass
        
        except KeyboardInterrupt:
            print('s')
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


if __name__ == '__main__':
    if args.depth is None or args.path is None:
        print('Specify the depth using --depth parameter')
    else:
        unvisitedURL = [line.strip() for line in open('./storage/'+args.path, 'r')]
        visitedURL = []
        crawl(args.depth,unvisitedURL,visitedURL)
