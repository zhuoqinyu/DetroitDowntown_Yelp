#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zhuoqinyu
This is a piece of sample code I used for scraping down the custormer reviews
for the restaurants located in Downtown Detroit.

"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url="https://www.yelp.com/search?find_desc=Restaurants&find_loc=Downtown+Detroit,+Detroit,+MI"
page=requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
info=[] # list of dictionaries

allchunk= soup.find_all("div",{"class":"media-story"})
for chunk in allchunk:
    one_info={}
    if chunk.find("h3",{"class":"search-result-title"})!=None:
        if chunk.h3.find("span",{"class":"yloca-tip"})==None:#not Ad
            name=chunk.h3.a.span.get_text().strip()
            one_info["name"]=name
            one_info["reviews"]=[]
            res_url='https://www.yelp.com/' + chunk.h3.find('a').get('href')
            res_r=requests.get(res_url)
            ressoup=BeautifulSoup(res_r.content,'html.parser')
            reviews=ressoup.find_all("p",{"itemprop":"description"})
            if reviews!=None:
                for rev in reviews:
                    one_info["reviews"].append(rev.text)
            info.append(one_info)      
#i=0
#while(i<4):
#    try:
#        i+=1
#        ttag=soup.find_all('a',{'class':'u-decoration-none next pagination-links_anchor'})
#        next_url = 'https://www.yelp.com/'+ttag[0].get('href')
#        q=request.get(next_url)
#        soup=BeautifulSoup(page.content, 'html.parser')
#        allchunk= soup.find_all("div",{"class":"media-story"})
#        for chunk in allchunk:
#            one_info={}
#            if chunk.find("h3",{"class":"search-result-title"})!=None:
#                if chunk.h3.find("span",{"class":"yloca-tip"})==None:#not Ad
#                    name=chunk.h3.a.span.get_text().strip()
#                    one_info["name"]=name
#                    one_info["reviews"]=[]
#                    res_url='https://www.yelp.com/' + chunk.h3.find('a').get('href')
#                    res_r=requests.get(res_url)
#                    ressoup=BeautifulSoup(res_r.content,'html.parser')
#                    reviews=ressoup.find_all("p",{"itemprop":"description"})
#                    if reviews!=None:
#                        for rev in reviews:
#                            one_info['reviews'].append(rev.text)
#                    info.append(one_info)
#    except:
#        break
data=pd.DataFrame(info)
#data.to_csv('yelp_downtowndtw_reviews.csv', sep='\t', encoding='utf-8',index=False)
data.to_csv('yelp_downtowndtw_reviews.csv', sep='\t', encoding='utf-8',mode='a', header=False,index=False)
#redata=pd.read_pickle('yelp_downtowndtw_reviews.df')
#newdata=pd.concat([redata,data],axis=0)
#newdata.to_pickle('yelp_downtowndtw_reviews.df')
#data.to_pickle('yelp_downtowndtw_reviews.df')

