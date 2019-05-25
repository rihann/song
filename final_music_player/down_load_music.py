from pymongo import MongoClient
import requests
import random
import time
import os
import shutil
import eyed3
def download_music():#下载音乐
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    }
    #连接数据库
    client = MongoClient()
    my_software = client['music_player']
    song = my_software['song']
    all_data=song.find()
    count=1
    #获得已经下载歌曲，避免重复下载
    song_list = os.listdir('song\\')
    print(song_list)
    for data in all_data:
        music_url=data['playAdd']
        music_name=data['name']
        music_name=music_name.replace('"','')
        music_name = music_name.replace('<', '_')
        music_name = music_name.replace('>', '_')
        music_name = music_name.replace('?', '_')
        music_name = music_name.replace('/', '_')
        music_name = music_name.replace(':', '_')
        print(music_name)
        if(music_name+'.mp3' in song_list):
            song.update({"name": data['name']}, {"$set": {"is_download": 1, "download_path": 'song//'+music_name+'.mp3'}})
        else:
            r = requests.get(music_url, headers=headers)
            download_path = "song//" + music_name + '.mp3'
            with open(download_path, 'wb') as f:
                f.write(r.content)
            song.update({"name": data['name']}, {"$set": {"is_download": 1, "download_path": download_path}})
            time.sleep(random.randint(1, 5))
        print('download_index:'+str(count))
        count=count+1
def update_music():#因为有60多首无法下载，将这60多首音乐，统一进行替换
    replace_path='song//paper messages.mp3'
    # 获得已经下载的没有问题的歌曲
    song_list = os.listdir('song\\')
    client = MongoClient()
    my_software = client['music_player']
    song = my_software['song']
    songs=song.find()
    for song in songs:
        download_path=song['download_path']
        download_name=download_path[6:]
        if(download_name not in song_list):
            src=replace_path
            dis=download_path
            shutil.copy(src, dis)
def update_music_time():#获取所有音乐的播放时间
    client = MongoClient()
    my_software = client['music_player']
    song_db = my_software['song']
    songs = song_db.find()
    count=1
    for song in songs:
        print(count)
        download_path = song['download_path']
        src = download_path
        print(src)
        dis = 'song\\temp\\0.mp3'
        shutil.copy(src, dis)
        # 加载本地文件
        voice_file = eyed3.load(dis)
        # 获取音频时长
        secs = int(voice_file.info.time_secs)
        song_db.update({'name':song['name']},{"$set":{'time':secs}})
        count=count+1

download_music()
#update_music()
update_music_time()