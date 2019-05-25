from pymongo import MongoClient
import random
import pymysql
#对数据库的所有操作封装到这个类中。将UI,逻辑，数据库，分开
class process_data:
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "123456", "singer_info")
        self.client = MongoClient()
        self.my_software = self.client['music_player']
        self.song = self.my_software['song']
        self.user=self.my_software['user']
    def get_password(self,user_id):
        user_info=self.user.find_one({'userId':user_id})
        if(user_info==None):
            return None
        else:
            return user_info['password']
    def get_user_info(self,user_id):
        user_info = self.user.find_one({'userId': user_id})
        return user_info
    def insert_user(self,user_id,password):#插入一个用户
        data={'userId':user_id}
        temp={}
        data['songRecord']=temp
        data['favorite']={}
        data['password']=password
        self.user.insert_one(data)
    def get_user_music(self,user_id):
        user_info=self.user.find_one({'userId':user_id})
        music_form=user_info['songRecord']
        music_info={}
        if(len(music_form)==0):
            return music_form,music_info
        music_form=sorted(music_form.items(), key=lambda x: x[1], reverse=True)#排序，从高到低
        music_form=dict(music_form)
        for music in music_form:
            temp=self.song.find_one({'name':music})
            music_info[music]=temp
        return music_form,music_info#返回歌曲播放记录，和音乐信息
    def update_music(self,user_id,music_name):#user_id用户，播放音乐的记录加一
        user_info=self.user.find_one({'userId':user_id})
        music_form = user_info['songRecord']
        count=music_form.get(music_name)
        if(count==None):
            music_form[music_name] =[1,6.0]
        else:
            music_form[music_name][0]=music_form[music_name][0]+1
        self.user.update({'userId':user_id},{"$set":{'songRecord':music_form}})
    def update_score(self,user_id,music_name,score):#user_id用户，播放音乐的记录加一
        user_info=self.user.find_one({'userId':user_id})
        music_form = user_info['songRecord']
        count=music_form.get(music_name)
        if(count==None):
            music_form[music_name] =[1,6.0]
        else:
            music_form[music_name][1]=score
        self.user.update({'userId':user_id},{"$set":{'songRecord':music_form}})
    def get_recommend_form(self,music_list):#获取歌单
        music_form_info={}
        for music in music_list:
            music_form_info[music]=self.song.find_one({'name':music})
        return music_form_info
    def get_sousuo(self,text):
        singer_info=None
        out_song=self.song.find_one({'name':text})
        if(out_song==None):
            out_singer=self.song.find({'author':text})
            data = {}
            for song in out_singer:
                data[song['name']] = song
            if(len(data)>0):
                singer_info=self.get_songer_info(text)
                return data,singer_info
            else:
                out_style = self.song.find({'style': text})
                for song in out_style:
                    data[song['name']] = song
                return data,singer_info

        else:
            data={}
            data[out_song['name']]=out_song
            return data,singer_info
    def my_close(self):
        self.client.close()
        self.db.close()
    def get_all_style(self):#得到所有风格
        contents=self.song.find()
        style_list=[]
        for content in contents:
            style_list.append(content['style'])
        style_list=list(set(style_list))
        return style_list
    def return_song_in_style_list(self,style_list):
        len_style_list=len(style_list)
        data={}
        for i in range(len_style_list):
            songs=self.song.find({'style':style_list[i]})
            count=0
            for song in songs:
                if(count<=5):
                    data[song['name']] = song
                else:
                    break
                count = count + 1
        return data
    def get_songer_info(self,name):
        cursor = self.db.cursor()
        sql = "SELECT * FROM singer_info \
               WHERE name = '%s'" % (name)
        cursor.execute(sql)
        result = cursor.fetchone()
        if(result==None):
            out='暂无歌手信息'
        else:
            out=result[1]
        return out
    def insert_fav(self,user_id,music_name):
        user_info = self.user.find_one({'userId': user_id})
        music_form = user_info['favorite']
        count = music_form.get(music_name)
        if (count == None):
            music_form[music_name] = 1
            self.user.update({'userId': user_id}, {"$set": {'favorite': music_form}})
    def delete_fav(self,user_id,music_name):
        user_info = self.user.find_one({'userId': user_id})
        music_form = user_info['favorite']
        count = music_form.get(music_name)
        if (count != None):
            music_form.pop(music_name)
            self.user.update({'userId': user_id}, {"$set": {'favorite': music_form}})
    def get_user_music_fav(self,user_id):
        user_info=self.user.find_one({'userId':user_id})
        music_form=user_info['favorite']
        music_info={}
        for music in music_form:
            temp=self.song.find_one({'name':music})
            music_info[music]=temp
        return music_form,music_info#返回歌曲收藏记录，和音乐信息


