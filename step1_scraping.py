#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zhuoqinyu

This is a piece of sample code I used for scraping down the restaurants 
information from yelp located in Downtown Detroit.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url="https://www.yelp.com/search?find_desc=Restaurants&find_loc=Downtown+Detroit,+Detroit,+MI&start=0"
page=requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())
names=[]
categories=[]
review_count=[]
ratings=[]
price=[]
allchunk= soup.find_all("div",{"class":"media-story"})
for chunk in allchunk:
    if chunk.find("h3",{"class":"search-result-title"})!=None:
        if chunk.h3.find("span",{"class":"yloca-tip"})==None:#not Ad
            names.append(chunk.h3.a.span.get_text().strip())       
        # Get the numbers of reviews
            link=chunk.find("span",{"class":"review-count rating-qualifier"})
            if link!=None:
                review_count.append(int(link.get_text().strip().split()[0]))
            else:
                review_count.append(np.nan)
        # Get the star ratings
            link=chunk.find("div",{"class":"biz-rating biz-rating-large clearfix"})
            if link!=None:
                ratings.append(float(link.img['alt'].split()[0]))
            else:
                ratings.append(np.nan)
        # Get price
            link=chunk.find("span",{"class":"business-attribute price-range"})
            if link!=None:
                price.append(link.get_text().strip())
            else:
                price.append(np.nan)
        # Get category
            link=chunk.find("span",{"class":"category-str-list"})
            if link!=None:
                cat=link.get_text().strip().split(",")
                newcat=(",").join([i.strip(' \t\n\r') for i in cat])
                categories.append(newcat)
            else:
                categories.append(np.nan)
print(names[0],review_count[0],ratings[0],price[0],categories[0])
i=0
while (i<4):
    try:
        i+=1
        ttag=soup.find_all('a',{'class':'u-decoration-none next pagination-links_anchor'})
        next_url='https://www.yelp.com'+ttag[0].get('href')
        q=requests.get(next_url)
        soup=BeautifulSoup(q.content,'html.parser')
        allchunk= soup.find_all("div",{"class":"media-story"})
        for chunk in allchunk:
            if chunk.find("h3",{"class":"search-result-title"})!=None:
                if chunk.h3.find("span",{"class":"yloca-tip"})==None:#not Ad
                    names.append(chunk.h3.a.span.get_text().strip())       
                # Get the numbers of reviews
                    link=chunk.find("span",{"class":"review-count rating-qualifier"})
                    if link!=None:
                        review_count.append(int(link.get_text().strip().split()[0]))
                    else:
                        review_count.append(np.nan)
                # Get the star ratings
                    link=chunk.find("div",{"class":"biz-rating biz-rating-large clearfix"})
                    if link!=None:
                        ratings.append(float(link.img['alt'].split()[0]))
                    else:
                        ratings.append(np.nan)
                # Get price
                    link=chunk.find("span",{"class":"business-attribute price-range"})
                    if link!=None:
                        price.append(link.get_text().strip())
                    else:
                        price.append(np.nan)
                # Get category
                    link=chunk.find("span",{"class":"category-str-list"})
                    if link!=None:
                        cat=link.get_text().strip().split(",")
                        newcat=(",").join([i.strip(' \t\n\r') for i in cat])
                        categories.append(newcat)
                    else:
                        categories.append(np.nan)
    except:
        break
data = pd.DataFrame({"Name":names,"review_count":review_count,"rating":ratings,"price":price,"category":categories})
#data.to_csv('yelp_downtowndtw.csv', sep='\t', encoding='utf-8',index=False)
data.to_csv('yelp_downtowndtw.csv', sep='\t', encoding='utf-8',mode='a', header=False,index=False)