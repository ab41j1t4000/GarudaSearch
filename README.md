Author: Abhijith P Kumar

#USAGE:

###Note: Use the commands without quotes ' '
##Docker method:

1. Run '*docker build -t [NAME] .*'
2. Run '*docker run -p 8080:8080 [NAME]*'
3. Access the search engine by typing http://0.0.0.0:8080/


##For users without docker:

Run the following commands in the main folder (GarudaSearch):

1. '*pip3 install -r requirements.txt*' 
2. '*python3 -m textblob.download_corpora*'
3. '*python3 run.py*'
4. Access the search engine by typing http://0.0.0.0:8080/ 

#NOTE:

1. If you using the search engine for the first time, go to the developer options in the top right corner.
2. Create a text file with few URLs line by line. These URLs will serve as the starting point for the crawling.
3. Upload the file in the application.
4. Specify the depth of the crawl and press the crawl button. You can stop the crawling in the mid process. 
5. If you want to delete all the crawled URL then click the purge button. This action cannot be reversed and you would have to use the crawl function again to use the search engine.
