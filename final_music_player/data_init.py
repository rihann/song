from pymongo import MongoClient
import json
import random
import pymysql
import pandas as pd
def init_song():#初始化数据库中音乐列表
    client = MongoClient()
    my_software = client['music_player']
    song = my_software['song']
    with open("json_data//song.json", 'r',encoding='utf8') as load_f:
        load_dicts = json.load(load_f)
    song_list=[]
    for data in load_dicts:
        data.pop('_id')
        song_name=data['name']
        song_name=song_name.replace('.','')
        song_list.append(song_name)
        data['name']=song_name
        data['is_download']=0
        data['download_path']=''
        data['time']=0
        temp=song.find_one({'name':data['name']})
        if(temp==None):
            song.insert_one(data)
    return song_list
def init_user(song_list):#初始化数据库中用户数据
    client = MongoClient()
    my_software = client['music_player']
    user = my_software['user']
    with open("json_data//user.json", 'r',encoding='utf8') as load_f:
        load_dicts = json.load(load_f)
    for data in load_dicts:
        data.pop('_id')
        temp_song_list=data['songRecord']#得到每个用户听过的歌单
        for i in range(len(temp_song_list)):
            temp_song_list[i]=temp_song_list[i].replace('.','')
            if(temp_song_list[i] not in song_list):
                temp_song_list[i]=' '
        while ' ' in temp_song_list:
            temp_song_list.remove(' ')
        if(len(temp_song_list)>0):
            len_list=len(temp_song_list)
            song_info={}
            for i in range(len_list):
                counts = []
                counts.append(random.randint(1,50))#随机化播放量1-50
                counts.append(random.uniform(0.0,10.0) )#随机化评分0-10
                song_info[temp_song_list[i]]=counts
            data['songRecord']=song_info
            data['favorite']={}
            data['password']='123'
            user.insert_one(data)
def init_singer_info():#初始化mysql
    data=pd.read_csv('json_data\\singers.csv')
    print(data.shape[0])
    db = pymysql.connect("localhost", "root", "123456", "singer_info")
    cursor = db.cursor()
    count=0
    for i in range(data.shape[0]):
        temp=data.iloc[i,:]
        sql = "INSERT INTO singer_info(name, \
                   info) \
                   VALUES ('%s', '%s')" % \
              (temp['name'], temp['info'])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            count=count+1
            print(temp['name'])
            print(len(temp['info']))
            # 如果发生错误则回滚
            db.rollback()


    # 关闭数据库连接
    db.close()
    print(count)
song_list=init_song()
init_user(song_list)
init_singer_info()