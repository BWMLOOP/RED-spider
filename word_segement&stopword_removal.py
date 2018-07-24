# -*- coding: utf-8 -*-
'''
Created on Thu May 31 10:50:29 2018

@author: liyishuai
'''
import pandas as pd
import re
import jieba
import jieba.posseg as pseg
jieba.load_userdict('userdict.txt')

# 数据筛选
def select(value):
    temp = data.loc[data['author'] == value,['title','content']]
    return temp



# remove emoji
def remove_emoji(text):
    emoji_pattern = re.compile(u'(\ud83d[\ude00-\ude4f])|'
                           u'(\ud83d[\u0000-\uddff])|' 
                           u'(\ud83d[\ude80-\udeff])|'  
                           u'(\uD83E[\uDD00-\uDDFF])|'
                           u'(\ud83c[\udf00-\uffff])|'  
                           u'(\ud83c[\udde0-\uddff])|'  
                           u'([\u2934\u2935]\uFE0F?)|'
                           u'([\u3030\u303D]\uFE0F?)|'
                           u'([\u3297\u3299]\uFE0F?)|'
                           u'([\u203C\u2049]\uFE0F?)|'
                           u'([\u00A9\u00AE]\uFE0F?)|'
                           u'([\u2122\u2139]\uFE0F?)|'
                           u'(\uD83C\uDC04\uFE0F?)|'
                           u'(\uD83C\uDCCF\uFE0F?)|'
                           u'([\u0023\u002A\u0030-\u0039]\uFE0F?\u20E3)|'
                           u'(\u24C2\uFE0F?|[\u2B05-\u2B07\u2B1B\u2B1C\u2B50\u2B55]\uFE0F?)|'
                           u'([\u2600-\u26FF]\uFE0F?)|'
                           u'([\u2700-\u27BF]\uFE0F?)'
                           '+', flags=re.UNICODE)
    return emoji_pattern.sub(r'',text).encode('utf8')

# 创建停用词列表
def get_stopwords(file):
    with open(file,'r',encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
    return stopwords
# 分词标记词性
def part_of_speech(text):
    seg = pseg.cut(text)
    temp = []
    for item in seg:
        if item.flag in ['a','v','n','x','an','vn','nz','nt','nr','ns']:
            temp.append(item.word)
    return temp

# 对内容进行分词 去停用词
def segmentation(post):
    # 过滤表情符号
    temp = remove_emoji(post).decode()
    # 分词 词性筛选
    seg = part_of_speech(temp.strip())
    # 加载停用词
    stopwords = get_stopwords('stopwords.txt')  
    output = ''
    for word in seg:
        if word not in stopwords:
            # 控制词长
            if len(word.strip())>1:
                if (word!='\t') and (word!='\r'):
                    output += word
                    output += ' '
    return output

data = pd.read_csv('beginner_contents.csv')
# 选择原创笔记
#posts = select()
posts = data[['title','content']]
# 标题和内容不能全为空
posts.dropna(thresh=1,inplace=True)
posts.fillna('',inplace=True)
# 拼接标题和内容
posts['text'] = posts['title'] + ' ' + posts['content']
text = posts['text'].values.tolist()


output = open('分词结果.txt','w',encoding='utf-8')
for post in text:
    temp = remove_emoji(post).decode()
    post_seged = segmentation(temp)
    output.write(post_seged+'\n')
output.close()
