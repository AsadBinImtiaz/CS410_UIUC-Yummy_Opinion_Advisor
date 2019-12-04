#!/usr/bin/env python
# coding: utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Util Functions
from util_funcs import *
from prepare_data import process_text_str

# import libs
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import pickle as pickle
import re
from functools import reduce 
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from operator import itemgetter

def tokenizer(x):
    return ( w for w in str(x).split() if len(w) >3)
    
def get_nmf_all():
    with open('../pickles/all_nmf_model.pk', 'rb') as fin:
        return pickle.load(fin)

def get_nmf_pos():
    with open('../pickles/pos_nmf_model.pk', 'rb') as fin:
        return pickle.load(fin)

def get_nmf_neg():
    with open('../pickles/neg_nmf_model.pk', 'rb') as fin:
        return pickle.load(fin)
    
def get_pos_topics_map():
    with open('../config/pos_topics.txt', 'r') as f:
        ret = {line.split(';')[0]: line.split(';')[1].replace('\n','') for line in f.readlines()}
    return ret

def get_neg_topics_map():
    with open('../config/neg_topics.txt', 'r') as f:
        ret =  {line.split(';')[0]: line.split(';')[1].replace('\n','') for line in f.readlines()}
    return ret
    
def get_all_topics_map():
    with open('../config/all_topics.txt', 'r') as f:
         ret = {line.split(';')[0]: line.split(';')[1].replace('\n','') for line in f.readlines()}
    return ret

def get_topic_desc_map():
    with open('../config/topic_map.txt', 'r') as f:
        ret = {line.split(';')[0]: line.split(';')[1].replace('\n','') for line in f.readlines()}
    return ret

def get_all_term_vec():
    with open('../pickles/topic_term_vector_all.pk','rb') as f:
        return pickle.load(f)

def get_pos_term_vec():
    with open('../pickles/topic_term_vector_pos.pk','rb') as f:
        return pickle.load(f)

def get_neg_term_vec():
    with open('../pickles/topic_term_vector_neg.pk','rb') as f:
        return pickle.load(f)
        
def get_topics_texts(str_text, nmf_all, nmf_pos, nmf_neg, all_topic_map, pos_topic_map, neg_topic_map, topic_desc_map, all_vectors, pos_vectors, neg_vectors, stars=3):
    text = [(u''+str(str_text))]
    
    avec = all_vectors.transform(text)
    pvec = pos_vectors.transform(text)
    nvec = neg_vectors.transform(text)
    
    txt_topic_text = (topic_desc_map[all_topic_map[str(np.argmax(nmf_all.transform(avec)))]])
    pos_topic_text = (topic_desc_map[pos_topic_map[str(np.argmax(nmf_pos.transform(pvec)))]])
    neg_topic_text = (topic_desc_map[neg_topic_map[str(np.argmax(nmf_neg.transform(nvec)))]])
    
    if stars<3:
        pos_topic_text=''
    if stars>3:
        neg_topic_text=''
    
    return [txt_topic_text,pos_topic_text,neg_topic_text]
        
def give_topics_to_text(str_text):
    nmf_all     = get_nmf_all()
    nmf_pos     = get_nmf_pos()
    nmf_neg     = get_nmf_neg()
    all_topic_map = get_all_topics_map()
    pos_topic_map = get_pos_topics_map()
    neg_topic_map = get_neg_topics_map()
    topic_desc_map = get_topic_desc_map()    
    pos_vec     = get_pos_term_vec()
    neg_vec     = get_neg_term_vec()
    all_vec     = get_all_term_vec()
    
    return get_topics_texts(str_text, nmf_all, nmf_pos, nmf_neg, all_topic_map, pos_topic_map, neg_topic_map, topic_desc_map, all_vec, pos_vec, neg_vec)
    
if __name__ == "__main__":
    printTS("Initialization started")
    try:
        
        str_t = 'Good food experience. I was with my family. Food was amazing. Service was slow.'
        printTS(str_t)
        cleansed_text = process_text_str(str_t)
        
        printTS(f'*** Topic Text    : {cleansed_text[0]}')
        printTS(f'*** Sentiment Text: {cleansed_text[1]}')
        
        topics = give_topics_to_text (cleansed_text[1])
        
        printTS(f'*** Topic General : {topics[0]}')
        printTS(f'*** Topic Positive: {topics[1]}')
        printTS(f'*** Topic Negative: {topics[2]}')
        
    except Exception as SomeError:
        printTS (f"Pre Processing Falied: {str(SomeError)}")