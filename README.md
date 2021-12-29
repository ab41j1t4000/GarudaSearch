# GARUDA SEARCH

Author: Abhijith P Kumar

Made as a part of Secure Coding Challenge(Level 3) in Sainya Ranakshetram Hackathon 2021

A working video of the search engine is available in the repo titled as WORKING_VIDEO.mp4

The search engine application uses spaCy NLP library for correcting mistakes and extracting keywords from the user's search queries.

Heroku App link: https://garudasearch.herokuapp.com/

# USAGE (Flask application):

### Note: Use the commands without quotes ' '
### In the place of [NAME], give the name you want

## Docker method:

1. Run '*docker build -t [NAME] .*'
2. Run '*docker run -p 8080:8080 [NAME]*'
3. Access the search engine by typing http://0.0.0.0:8080/


## For users without docker:

Run the following commands in the main folder (GarudaSearch):

1. '*pip3 install -r requirements.txt*' 
2. '*python3 -m textblob.download_corpora*'
3. '*sudo cp crawlcrontab /etc/cron.d/crawlcrontab*'
4. '*sudo chmod 0644 /etc/cron.d/crawlcrontab*'
5. '*sudo crontab /etc/cron.d/crawlcrontab*'
6. '*python3 run.py*'
7. Access the search engine by typing http://0.0.0.0:8080/ 

# NOTE:

If you using the search engine for the first time:
1. Run '*docker run -p 8080:8080 -it [NAME]* /bin/bash'
This will launch the docker application in interactive shell mode.

2. In the spawned shell, run crawler.py to crawl the internet. The crawler uses First-in-First-Out method using a queue for URL crawling.

USAGE:
To delete the crawled URLs

>python3 crawler.py --purge

To crawl URLs

>python3 crawler.py --run --path [PATH_TO_URL_LIST] --depth [DEPTH_OF_CRAWL]

default depth = 50
default path = ./app/storage/unvisitedURL.txt

To see the number of crawled URLs

>python3 crawler.py --check

3. Run '*python3 run.py*' and access the site by typing http://0.0.0.0:8080/
4. Note: check the number of crawled URLs using the '--check' flag. If the number of crawled URLs is less than 50, it is recomended to run the crawler atleast once with a depth of 50.
5. The crawler python script automatically runs every midnight as a cron job.
