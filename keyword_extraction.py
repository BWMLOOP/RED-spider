#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 16:42:34 2018

@author: liyishuai
"""


import jieba.analyse
jieba.load_userdict('userdict.txt')

f1 = open('分词结果.txt', 'r',encoding='utf-8')
content = f1.read()
  
f2 = open('关键词提取new.csv', 'w')
f2.write("%s,%s\n" % ('keywords','frequency'))

keywords = jieba.analyse.extract_tags(content, topK=1000, withWeight=True)

with open('关键词提取new.csv', 'a') as f:
    for (keyword,fre) in keywords:
        f.write('%s,%s\n' %(keyword,fre))
        
keywords_dict = {keywords[i][0]: keywords[i][1] for i in range(0, len(keywords))}
  
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread



def draw_cloud(word_freq, save_path):
    wc = WordCloud(font_path='fz.ttf',  # 设置字体
                   background_color="white",  # 背景颜色
                   width=1086, 
                   height=302,
                   max_words=1000,  # 词云显示的最大词数
                   mask=imread('red.jpg'),  # 设置背景图片
                   max_font_size=80,  # 字体最大值
                   min_font_size=6,
                   random_state=42,
                   scale=5,
                   prefer_horizontal=0.9,
                   )
    # create a word_cloud from dict(words and frequencies) 
    wc.generate_from_frequencies(word_freq)

    plt.figure()

    # 采用自定义颜色
    image_colors = ImageColorGenerator(imread('red.jpg'))

    plt.imshow(wc.recolor(color_func=image_colors, random_state=3),
               interpolation="bilinear")

    plt.axis("off")
    wc.to_file(save_path)
    plt.show()
    
# 获取关键词及词频
input_freq = keywords_dict
# 经过手动调整过的词频文件,供参考
# freq = pd.read_csv("data/cntliu.csv", header=None, index_col=0)
# input_freq = freq[1].to_dict()
draw_cloud(input_freq, "output.png")
