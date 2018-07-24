# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 13:25:59 2018

@author: liyishuai
"""
import numpy as np
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from gensim.models import CoherenceModel

f1 = open('分词结果.txt', 'r',encoding='utf-8')

# 去除太短的笔记
data = []
for post in f1.readlines():
    if len(post) >= 30:
        data.append(post)
        
# remove common words and tokenize
data = [[word for word in post.split()]for post in data]


tokens = sum(data,[]) # unfold a list


# remove words that appear only 10 times
drop = set(i for i in set(tokens) if tokens.count(i) <= 10)
contents = [[word for word in post if word not in drop] for post in data]
print('step2 complete')

dictionary = corpora.Dictionary(contents)
#dictionary.save('词典.dict') # store the dictionary
print(dictionary)

# 转化标记化文本为向量
corpus = [dictionary.doc2bow(post) for post in contents]
lda = LdaModel(corpus=corpus, num_topics=70, id2word=dictionary,
               iterations=500, eval_every=1, alpha='auto', passes=50)

f1 = open('主题new.csv', 'w')
f1.write("%s\n" % ('topic'))
for topic in lda.print_topics(num_topics=50,num_words=5):
    topic_number = topic[0]
    list = topic[1].split('+')
    n = 1
    for item in list:
        temp = item.split('*')
        keyword = temp[1]
        weight = float(temp[0])
        if n == 1:
            with open('主题new.csv', 'a') as f:
                f.write('%d,%s,%f,' %(topic_number, keyword, weight))
        elif n == 5:
            with open('主题new.csv', 'a') as f:
                f.write('%s,%f\n' %(keyword, weight))
        else:
            with open('主题new.csv', 'a') as f:
                f.write('%s,%f,' %(keyword, weight))
        n += 1

# Compute Perplexity
print('\nPerplexity: ', lda.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

# Compute Coherence Score 模型一致性
coherence_model_lda = CoherenceModel(model=lda, texts=contents, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)


#Finding the dominant topic in each post

def format_topics_sentences(model, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()

    for i, row in enumerate(model[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)
    
    
    

df_topic_sents_keywords = format_topics_sentences(model=lda, corpus=corpus, texts=contents)

# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']


# Topic distribution across documents
# Number of Documents for Each Topic
topic_counts = df_topic_sents_keywords['Dominant_Topic'].value_counts()

# Percentage of Documents for Each Topic
topic_contribution = round(topic_counts/topic_counts.sum(), 4)

# Topic Number and Keywords
topic_num_keywords = df_topic_sents_keywords[['Dominant_Topic', 'Topic_Keywords']]

# Concatenate Column
df_dominant_topics = pd.concat([topic_num_keywords, topic_counts, topic_contribution], axis=1)

# Change Column names
df_dominant_topics.columns = ['Dominant_Topic', 'Topic_Keywords', 'Num_Documents', 'Perc_Documents']
