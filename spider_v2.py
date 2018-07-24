#-*- coding:utf-8 -*-

import json
import requests
import time
import random
import re
import csv
# import proxy
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class spider:

    def __init__(self):
        self.headers = {
                        'Host': 'www.xiaohongshu.com',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36'
                        }
        
        self.fans = ''
        self.follows = ''
        self.gender = ''
        self.level = ''
        self.liked = ''
        self.nickname = ''
        self.boards = ''
        self.notes = ''
        self.collected = ''
        self.officialVerified = ''
        
    def response(self, url):
        try:
            response = requests.get(url, timeout=60, headers=self.headers, verify=False)
            # response = requests.get(url, timeout=60, headers=self.headers, proxies=proxy.get_proxy_list()[0], verify=False)
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
    # 过滤表情
    def filter_emoji(self,desstr, restr=''):
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub(restr, desstr)

    def m_1(self,Uid):
        global f1,f2,f3
        url = 'https://www.xiaohongshu.com/user/profile/' + Uid
        try:
            response = self.response(url)
        except Exception as e:
            print('get_info', e)
        else:
            if response:
                response = re.findall('__INITIAL_SSR_STATE__=(.*?)</script><!',response,re.S)
                if response:
                    Json = json.loads(response[0])

                    try:
                        self.fans = Json['ProfileLayout']['userInfo']['fans']
                    except:
                        pass
                    
                    try:
                        self.follows = Json['ProfileLayout']['userInfo']['follows']
                    except:
                        pass
                    
                    try:
                        self.gender = Json['ProfileLayout']['userInfo']['gender']
                    except:
                        pass
                    
                    try:
                        self.level = self.filter_emoji(Json['ProfileLayout']['userInfo']['level']['name'])
                    except:
                        pass
                    
                    try:
                        self.liked = Json['ProfileLayout']['userInfo']['liked']
                    except:
                        pass

                    try:
                        self.nickname = self.filter_emoji(Json['ProfileLayout']['userInfo']['nickname'])
                    except:
                        pass

                    try:
                        self.boards = Json['ProfileLayout']['userInfo']['boards']
                    except:
                        pass
                    
                    try:
                        self.notes = Json['ProfileLayout']['userInfo']['notes']
                    except:
                        pass
                    
                    try:
                        self.collected = Json['ProfileLayout']['userInfo']['collected']
                    except:
                        pass

                    try:
                        self.officialVerified = Json['ProfileLayout']['userInfo']['officialVerified']
                        if self.officialVerified == True:
                            self.officialVerified = 'Y'
                        else:
                            self.officialVerified = 'N'
                    except:
                        pass
                    with open('user.csv', 'a') as f1:
                        f1.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" %
                        (Uid, self.nickname, self.gender, self.level, self.fans, self.follows, self.boards, self.notes, self.liked, self.collected, self.officialVerified))
                       
                    boardData = Json['ProfileLayout']['boardData']
                    if boardData:
                        boards_fans = 0
                        collected_notes = 0
                        for each_b in boardData:
                            try:
                                fans = each_b['fans']
                                notes = each_b['notes']
                                boards_fans += fans
                                collected_notes += notes
                            except:
                                pass

                        try:
                            with open('boardData.csv', 'a') as f2:
                                f2.write("%s,%s,%s\n" % (Uid, boards_fans, collected_notes))
                        except:
                            pass
                                
                    print('done')


if __name__ == '__main__':
    global f1,f2
    
    with open('user.csv', 'w') as f1:
        writer = csv.writer(f1)
        f1.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" %
        ('Uid','nickname','gender','level','fans','follows','boards','notes','liked','collected','officialVerified'))
    
    with open('boardData.csv', 'w') as f2:
        writer = csv.writer(f2)
        f2.write("%s,%s,%s\n" % ('Uid', 'boards fans', 'collected notes', ))

    ff = open('selected_users_uid.csv','r')
    lines = ff.readlines()
    for line in lines:
        time.sleep(random.uniform(0,2))
        print(line.strip())
        try:
            time.sleep(random.choice(range(1,5))*0.1+1)
            spider().m_1(line.strip())
        except Exception as e:
            print('spider', e)
