import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.decomposition import NMF
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
class my_model_nmf:#基于nmf的协同过滤推荐
    def __init__(self):
        pass
    def init_datebase(self):
        self.client = MongoClient()
        self.my_software = self.client['music_player']
        self.song = self.my_software['song']
        self.user = self.my_software['user']
        #首先，取出所有音乐，得到音乐列表
        songs=self.song.find()
        song_list=[]
        for song in songs:
            song_list.append(song['name'])
        #然后，取出所有用户的行为集合,评分信息
        users=self.user.find()
        user_count=0
        user_list=[]
        user_id=[]
        for user in users:
            user_id.append(user['userId'])
            user_list.append(user)
            user_count=user_count+1
        data=np.zeros((user_count,len(song_list)))
        data=pd.DataFrame(data,columns=song_list,index=user_id)
        for i in range(user_count):
            song_records=user_list[i]['songRecord']
            for song_record in song_records:
                data.loc[user_id[i],song_record]=song_records[song_record][1]
        data.to_csv('models//data.csv')
    def train_model(self):
        data=pd.read_csv('models//data.csv',index_col=0)
        train_data=data.values
        model = NMF(n_components=40, init='random', random_state=0)
        model.fit(train_data)
        joblib.dump(model,'models//nmf.m')

    def recommed_song(self,user_id):
        data = pd.read_csv('models//data.csv', index_col=0)
        user_index=list(data.index)
        song_index=list(data.columns)
        rec_userid=user_index.index(user_id)
        train_data = data.values
        model=joblib.load('models//nmf.m')
        item_dis=model.transform(train_data)
        user_dis=model.components_
        filter_matrix = train_data < 1e-8
        rec_mat = np.dot(item_dis, user_dis)
        rec_filter_mat=(filter_matrix*rec_mat).T
        rec_list = rec_filter_mat[rec_userid, :]
        out=np.argsort(rec_list)
        recommond=[]
        for temp in out[-10:]:#推荐10首音乐
            recommond.append(song_index[temp])
        return recommond


class my_model_knn:
    def __init__(self):
        pass
    def init_datebase(self):
        self.client = MongoClient()
        self.my_software = self.client['music_player']
        self.song = self.my_software['song']
        self.user = self.my_software['user']
        songs=self.song.find()
        song_list=[]
        singer_list=[]
        style_list=[]
        time_list=['short','mid','long']
        for song in songs:
            song_list.append(song['name'])
            singer_list.append(song['author'])
            style_list.append(song['style'])
        singer_list=list(set(singer_list))
        style_list = list(set(style_list))
        len_features=len(singer_list)+len(style_list)+len(time_list)
        len_music=len(song_list)
        feature=singer_list+style_list+time_list
        data=np.zeros((len_music,len_features))
        data=pd.DataFrame(data,index=song_list,columns=feature)
        songs = self.song.find()
        for song in songs:
            name=song['name']
            singer=song['author']
            style=song['style']
            data.loc[name,singer]=1
            data.loc[name,style]=1
            data.loc[name,self.procee_time(song['time'])]=1
        data.to_csv('models//song_feature.csv')
    def procee_time(self,time):
        if(time <=80):
            a='short'
        elif(time <=200):
            a='mid'
        else:
            a='long'
        return a
    def process_score(self,score):
        if(score>=6):
            return 1
        else:
            return 0
    def recommend_Logistic(self,id):
        data=pd.read_csv('models//song_feature.csv',index_col=0)
        all_song_index=list(data.index)
        user_info=self.user.find_one({'userId':id})['songRecord']
        song_list=[]
        scores=[]
        for music_name in user_info:
            song_list.append(music_name)
            scores.append(self.process_score(user_info[music_name][1]))
        train_data=data.loc[song_list]
        train_label=np.array(scores)
        test_data_index=[]
        for song in all_song_index:
            if(song not in song_list):
                test_data_index.append(song)
        test_data=data.loc[test_data_index]
        model=LogisticRegression(penalty='l1')
        model.fit(train_data.values,train_label)
        test_label=model.predict_proba(test_data)
        out_song_list=[]
        count=0
        for song in test_data_index:
            if(test_label[count][1]>=0.8):
                out_song_list.append(song)
            count=count+1
        if(len(out_song_list)>20):
            return out_song_list[:20]
        else:
            return out_song_list

#test=my_model_nmf()
#test.init_datebase()
#test.train_model()
#test.recommed_song(386727941)

#test=my_model_knn()
#test.init_datebase()
#test.recommend_knn(10086)