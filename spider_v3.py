#-*- coding:utf-8 -*-

import json
import requests
import time
import re
import random
# import proxy
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class get_content:

    def __init__(self):
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36'
                        }
        
        self.title = ''
        self.content = ''
        self.keywords = ''
        self.tags = ''

        
    def response(self, url):
        
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = "HC9D86343A07L44D"
        proxyPass = "D8505DD40CA7AB1A"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                                                                    "host": proxyHost, 
                                                                    "port": proxyPort,
                                                                    "user": proxyUser,
                                                                    "pass": proxyPass,
                                                                   }
        proxies = {
                   "http": proxyMeta,
                   "https": proxyMeta,
                  }
        
        time.sleep(0.2)
        try:
            response = requests.get(url, timeout=60, headers=self.headers, proxies=proxies, verify=False)
            # response = requests.get(url, timeout=60, headers=self.headers, proxies=proxy.get_proxy_list()[0], verify=False)
        except IOError as e:
            print(e)
        except EOFError as e:
            print(e)
        else:
            if response.status_code == 200:
                return response.text
            else:
                time.sleep(0.2)
                print(response.status_code)
                self.response(url)

    def filter_emoji(self,desstr, restr=''):
        '''''
        过滤表情
        '''
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub(restr, desstr)
    

    def m_0(self,Uid): #用户专辑
        url = 'https://www.xiaohongshu.com/user/profile/' + Uid + '?tab=album'
        try:
            response = self.response(url)
        except Exception as e:
            print('get_info', e)
        else:
            if response:
                response = re.findall('__INITIAL_SSR_STATE__=(.*?)</script><!',response,re.S)
                if response:
                    Json = json.loads(response[0])
                                         
                    boardData = Json['ProfileLayout']['boardData'] #收藏部分
                    if boardData:
                        for each_b in boardData: #遍历专辑
                            try:
                                bid = each_b['id'] #记录一个专辑id：bid
                                print(bid)
                                self.m_3(Uid,bid) #进入专辑页面进行下一步处理
                            except:
                                pass

    def m_1(self,Uid):
        url = 'https://www.xiaohongshu.com/user/profile/' + Uid + '?tab=note'
        try:
            response = self.response(url)
        except Exception as e:
            print('get_info', e)
        else:
            if response:
                response = re.findall('__INITIAL_SSR_STATE__=(.*?)</script><!',response,re.S)
                if response:
                    Json = json.loads(response[0])  
                                       
                    noteData = Json['ProfileLayout']['noteData'] #笔记部分
                    if noteData:
                        for each_n in noteData:
                            try:
                                nid = each_n['id'] #记录一个笔记id：nid
                                self.m_2(Uid,nid,'Y') #进入笔记页面
                            except:
                                pass
                                

                



    def m_2(self,Uid,id,author): #进入用户发布笔记的页面
        url = 'https://www.xiaohongshu.com/discovery/item/' + id
        try:
            response = self.response(url)
        except Exception as e:
            print('get_info', e)
        else:
            if response:
                response = re.findall('__INITIAL_SSR_STATE__=(.*?)</script><!',response,re.S)
                if response:
                    Json = json.loads(response[0])

                    self.title = self.filter_emoji(Json['NoteView']['content']['title'].replace(',',' '))
                    self.content = self.filter_emoji(Json['NoteView']['content']['desc'].replace(',',' '))
                     
                    keywords = ''                                      
                    keyword_list = Json['NoteView']['content']['keywords']
                    k_num = 1 #至少一个关键词
                    for k in keyword_list: #关键词遍历
                        if k_num == 1: 
                            keywords = k 
                        else: 
                            keywords = keywords + ';' + k
                        k_num += 1
                    self.keywords = keywords                    
                    tags = ''
                    tag_list = Json['NoteView']['content']['tagCategories']

                    del tag_list[0] #tag_list第一元素为空
                    t_num = 1 #至少一个关键词
                    for t in tag_list:
                        if t_num == 1:
                            tags = t
                        else:
                            tags = tags + ';' + t
                        t_num += 1
                    self.tags = tags

                 
                    with open('beginner_contents.csv', 'a') as f1:
                        f1.write('%s,%s,%s,%s,%s,%s,%s\n' %
                        (Uid, id, author, self.title, self.tags, self.keywords, self.content.replace('\n',';'))) 
                    

                    
    def m_3(self,Uid,id): #进入用户收藏专辑的页面
        url = 'https://www.xiaohongshu.com/board/' + id
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
                        BoardInfo = Json['BoardInfo']['notes'] #遍历笔记
                        for each in BoardInfo:
                            try:
                                cid = each['id'] #记录笔记id
                                self.m_2(Uid,cid,'N') #进入笔记页面
                            except:
                                pass
                    except:
                        pass
                  
                   
if __name__ == '__main__':
    global f1
    f1 = open('beginner_contents.csv', 'w')
    f1.write("%s,%s,%s,%s,%s,%s,%s\n" % ('Uid', 'id', 'author', 'title', 'tags', 'keywords', 'content'))
    
    ff = open('undo_uid.txt')
    lines = ff.readlines()
    for line in lines:
        time.sleep(random.uniform(0,2))
        try:
            get_content().m_0(line.strip())
            get_content().m_1(line.strip())
        except Exception as e:
            print('get_content', e)
