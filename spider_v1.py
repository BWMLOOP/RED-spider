#-*- coding:utf-8 -*-

import json
import requests
import time,random
import re
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class uid_get:

    def __init__(self):
        self.headers = {
                        'Host': 'www.xiaohongshu.com',
                        'Authorization': 'session.1205256979157764063',
                        'X-Tingyun-Id': 'LbxHzUNcfig;c=2;r=1522919134',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
                        'Accept': 'application/json',
                        'Connection': 'keep-alive',
                        'Proxy-Connection': 'keep-alive',
                        'User-Agent': 'discover/5.11.2 (iPhone; iOS 9.3.5; Scale/2.00) Resolution/640*960 Version/5.11.2 Build/511202 Device/(Apple Inc.;iPhone4,1)',
                        }
        
    def response(self, url):
        try:
            response = requests.get(url, timeout=60, headers=self.headers, verify=False)
        # print the exception information when it occurs
        except IOError as e: 
            print(e)
        except EOFError as e:
            print(e)
        else:
            if response.status_code == 200:
                return response.text
            else:
                time.sleep(1)
                print(response.status_code)
                self.response(url)

    def filter_emoji(self,desstr, restr=''):
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub(restr, desstr)

    def m_1(self,url):
        try:
            response = self.response(url)
        except Exception as e:
            print('get_info', e)
        else:
            if response:
                Json = json.loads(response)
                data = Json['data']
                for d in data:
                    try:
                        nickname = self.filter_emoji(d['user']['nickname'])
                        userid = d['user']['userid']
                    except EOFError as e:
                        print('dataSave EOFError', e)
                    except Exception as e:
                        print('dataSave Exception', e)                
                    else:
                        try:
                            with open('collectedusers.csv', 'a') as ff1:
                                ff1.write("%s,%s\n" % (userid, nickname))
                        except:
                            pass

    def m_2(self, url):
        try:
            response = self.response(url)
        except Exception as e:
            print('get_info', e)
        else:
            if response:
                Json = json.loads(response)
                data = Json['data']
                comments = data['comments']
                for d in comments:
                    try:
                        nickname = self.filter_emoji(d['user']['nickname'])
                        userid = d['user']['userid']
                    except EOFError as e:
                        print('dataSave EOFError', e)
                    except Exception as e:
                        print('dataSave Exception', e)                
                    else:
                        try:
                            with open('commentusers.csv', 'a') as ff2:
                                ff2.write("%s,%s\n" % (userid, nickname))
                        except:
                            pass
                        
    def m_3(self, url):
        try:
            response = self.response(url)
        except Exception as e:
            print('get_info', e)
        else:
            if response:
                Json = json.loads(response)
                data = Json['data']
                for d in data:
                    try:
                        nickname = self.filter_emoji(d['nickname'])
                        userid = d['userid']
                    except EOFError as e:
                        print('dataSave EOFError', e)
                    except Exception as e:
                        print('dataSave Exception', e)                
                    else:
                        try:
                            with open('likedusers.csv', 'a') as ff3:
                                ff3.write("%s,%s\n" % (userid, nickname))
                        except:
                            pass
 


if __name__ == '__main__':
    global ff1,ff2,ff3
    sleeptime = random.randint(0,2)
    with open('collectedusers.csv', 'w') as ff1:
        writer = csv.writer(ff1)
        ff1.write("%s,%s\n" %('Uid','nickname')) 
        
    with open('commentusers.csv', 'w') as ff2:
        writer = csv.writer(ff2)
        ff2.write("%s,%s\n" %('Uid','nickname'))
        
    with open('likedusers.csv', 'w') as ff3:
        writer = csv.writer(ff3)
        ff3.write("%s,%s\n" %('Uid','nickname'))
    
    f1 = open('collectedusers_url.csv','r')       
    for f1_1 in f1.readlines():
        try:
            time.sleep(sleeptime)
            uid_get().m_1(f1_1.strip())
        except Exception as e:
            print('uid_get', e)


    f2 = open('commentusers_url.csv','r')        
    for f2_1 in f2.readlines():
        try:
            time.sleep(sleeptime)
            uid_get().m_2(f2_1.strip())
        except Exception as e:
            print('uid_get', e)
            
    f3 = open('likedusers_url.csv','r')
    for f3_1 in f3.readlines():
        try:
            time.sleep(sleeptime)
            uid_get().m_3(f3_1.strip())
        except Exception as e:
            print('uid_get', e)
