import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import mongo_process
import re
from pymongo import MongoClient
import time
import pandas as pd
def get_url_sing(sing_name):
    browser = webdriver.Chrome()

    browser.get("https://music.douban.com/")
    input_first = browser.find_element_by_id("inp-query")
    input_first.send_keys(sing_name)
    button = browser.find_element_by_class_name('inp-btn')
    button.click()
    page_content=browser.page_source
    soup=BeautifulSoup(page_content,'lxml')
    out=soup.find('div',{'class':'title'}).find('a',{'class':'title-text'})
    if(out!=None):
        url = out['href']
        return url
    else:
        return None
def get_all_singer_url():
    client = MongoClient()
    my_software = client['singer']
    sing_url = my_software['sing_url']
    mongo=mongo_process.process_data()
    songs=mongo.song.find()
    singer_list=[]
    for song in songs:
        singer_list.append(song['author'])
    singer_list=list(set(singer_list))
    for singer in singer_list:
        data=sing_url.find_one({'name':singer})
        if(data==None):
            print(singer)
            url=get_url_sing(singer)
            sing_url.insert_one({"name":singer,'url':url})
            time.sleep(3)
def is_right(text):
    if(text==None):
        return False
    else:
        out=re.findall('musician',text)
        if(len(out)>0):
            return True
        else:
            return False
def get_info(url):
    browser = webdriver.Chrome()

    browser.get(url)
    page_content = browser.page_source
    soup = BeautifulSoup(page_content, 'lxml')
    p = soup.find('div', id='intro').find('div', {'class': 'bd'})
    out=p.find('span',{'class':'all hidden'})
    if(out!=None):
        text=out.get_text()
    else:
        text=p.get_text()
    return text
def down_load_singer_all():
    client = MongoClient()
    my_software = client['singer']
    sing_url = my_software['sing_url']
    sing_info=my_software['sing_info']
    sings=sing_url.find()
    count=0
    for sing in sings:
        print(count)
        url=sing['url']
        flag=is_right(url)
        if(flag):
            sing_info.insert_one({"name":sing['name'],"info":get_info(url)})
            time.sleep(2)
        else:
            sing_info.insert_one({"name": sing['name'], "info": '暂无歌手信息'})
        count = count + 1
def data_to_csv():
    client = MongoClient()
    my_software = client['singer']
    sing_info = my_software['sing_info']
    singers=sing_info.find()
    list_singer=[]
    for singer in singers:
        list_singer.append({'name':singer['name'],'info':singer['info']})
    data=pd.DataFrame(list_singer)
    data.to_csv('json_data\\singers.csv')
data_to_csv()