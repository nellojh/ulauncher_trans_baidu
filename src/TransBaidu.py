import requests
import random
import hashlib
APPID=''
KEY=''

class TransBaidu:
    def __init__(self,perferences):
        self.APPID=perferences.get('app_id')
        self.KEY=perferences.get('key')
    def MD5(self,appid,q,key,salt):
        print(appid,q,key,salt)
        return hashlib.md5((appid+q+str(salt)+key).encode(encoding='UTF-8')).hexdigest()
    def trans(self,q):
        salt= random.randrange(10000000,99999999)
        md5str=self.MD5(self.APPID,q,self.KEY,salt)
        trans_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        trans_headers = {
            'Content-Type':'application/x-www-form-urlencoded'
        }
        trans_params = {
            'q':q,
            'from':'auto',
            'to':'auto',
            'appid':self.APPID,
            'salt':salt,
            'sign':md5str
        }
        addtional = {
            'tts':0,
            'dict':0
        }
        trans_params.update(addtional)
        result = requests.post(url=trans_url,headers=trans_headers,params=trans_params)
        t=eval(result.text)
        return t.get('trans_result')