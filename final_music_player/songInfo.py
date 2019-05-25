import requests
import pymongo
import threading

client=pymongo.MongoClient()
db=client['netCloud']
col_song=db['song']
col_user=db['user']


def threadGo(line,target):
	threads = []
	threadList = []
	for i in range(1, 21):
		threadList.append('Thread-' + str(i))
	for name in threadList:
		if len(line)==0:
			break
		url = line.pop(0)  # 从任务队列里读取消息
		thread = threading.Thread(target=target, args=(url,))
		thread.start()
		threads.append(thread)
	for t in threads:
		t.join()
		
def getStyle():#获取风格
	styleList=[]
	r=requests.get('http://101.132.105.96:3000/playlist/catlist',timeout=15)
	for i in r.json()['sub']:
		styleList.append(i['name'])
		
	return styleList
	
def getPlayList(style):#获取歌单
	r = requests.get('http://101.132.105.96:3000/top/playlist?cat=%s'%style,timeout=15)
	return r.json()['playlists'][2]['id']

def insertRecord(userId):
	try:
		r = requests.get('http://101.132.105.96:3000/user/record?uid=%d&type=1'%userId,timeout=15)
		songList=[]
		if r.json()['code']==-2:
			return
		for i in r.json()['weekData']:
			songList.append(i['song']['name'])
	
		info={'userId':userId,'songRecord':songList}
		col_user.insert_one(info)
		# print(info)
	except Exception as e:
		print(e)
		
def getUser(playlist):#获取歌单用户
	r = requests.get('http://101.132.105.96:3000/playlist/subscribers?id=%d&limit=100'%playlist,timeout=15)
	userList=[]
	for i in r.json()['subscribers']:
		userId=i['userId']
		# insertRecord(userId)
		userList.append(userId)
	threadGo(userList,insertRecord)
	

def getSong(playlist,style):#传入歌单编号，风格
	try:
		r = requests.get('http://101.132.105.96:3000/playlist/detail?id=%d'%playlist,timeout=15)
		res = r.json()
		for i in res['playlist']['tracks'][:30]:
			info={'name':i['name'],'author':i['ar'][0]['name'],'style':style,'playAdd':'http://music.163.com/song/media/outer/url?id=%s.mp3'%i['id']}
			print(info)
			col_song.insert_one(info)
	except Exception as e:
		print(e)
		
def main():
	styleList=getStyle()
	for i in styleList:
		try:
			id=getPlayList(i)
			#getSong(id,i)
			getUser(id)
		except Exception as e:
			print(e)

if __name__ == '__main__':
	main()
