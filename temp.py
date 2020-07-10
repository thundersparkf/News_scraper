import requests
from bs4 import BeautifulSoup
import re
import feedparser
from pandas.io.json import json_normalize
import pandas as pd
sum = 0


class Scraper:
    def __init__(self, URL,class_crawl,class_extract, tags_crawl, tags_extract):
        self.url = URL
        self.class_crawl = class_crawl
        self.class_extract = class_extract
        self.tags_crawl = tags_crawl
        self.tags_extract = tags_extract
        
    def extractor(self, link):
        '''
        

        Parameters
        ----------
        link : Link of the page containing the article.

        Returns
        -------
        data : Extracted article content.

        '''
        print('Extracting...')
        try:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(self.tags_extract, class_=self.class_extract)
            texts = results.find_all('p')
        except:
            return None
        data = []
        for text in texts:
            data.append(text.text)
        data = ' '.join(data)
        return data
    
    def crawler(self):
        '''
        Function to crawl through the link of the given news website to search for links and write article 
        data into individual file.

        Returns
        -------
        None.

        '''
        # Supply your own header
        header ={'User-Agent':""}
        try:    
            page = requests.get(self.url, headers = header)  
            print(page)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find_all(self.tags_crawl, class_=self.class_crawl)
            for result in results:
                link = result.find('a')['href']
                link = link.replace('/india','')
                self.writer(link)
        except:
            pass
            
    def writer(self, link):
        global sum
        print
        sum+=1
        with open('NEWS/ARTICLE_'+str(sum),'at') as f:
            print(link)
            
            data = self.extractor(link)
            if data != None:
                f.write(data+str('\n'))

