#!/usr/bin/python
#  -*- coding: UTF-8 -*-
import os, sys
import collections
import pickle
from os import listdir
import operator
import nltk
import re
import sys
import numpy as np

def addtoindex(sentence):
    words=nltk.word_tokenize(sentence)+['.']
    if len(words) > 2:
        for index, word in enumerate(words[0:-3]):

            if len(word)>0:
                words_count[0] += 1
                next = words[index + 1]
                nnext = words[index + 2]
                if word in words_dct:
                    words_dct[word][0] += 1
                    if next in words_dct[word][1]:
                        words_dct[word][1][next][0] += 1
                        words_dct[word][1][next][1][nnext] += 1
                    else:
                        words_dct[word][1][next] = [1, collections.Counter()]
                        words_dct[word][1][next][1][nnext] += 1
                else:
                    words_dct[word] = [1, {}]
                    words_dct[word][1][next] = [1, collections.Counter()]
                    words_dct[word][1][next][1][nnext] += 1
        first_word_cnt[words[0]] += 1

def index(dir_name):
    for file_number, file_name in enumerate(listdir(dir_name)):
        print file_number, file_name
        sentences = []
        with open(dir_name+'/'+file_name,'r') as fin:
            lines = fin.read()
            try:
                sentences += nltk.sent_tokenize(lines)
            except:
                nltk.download('punkt')
                try:
                    sentences += nltk.sent_tokenize(lines)
                except:
                    pass
            if len(sentences) > 0:
                sentences = sentences[100:-100]
                punc = ".,:;“\"#%^&*()[]_„”\'“’‘"
                dict.fromkeys(map(ord, punc))
                mapping = dict.fromkeys(map(ord, punc))
                for sentence in sentences:
                    sentence_clean = sentence.lower().replace(u'-', u' ').translate(mapping)
                    if len(sentence_clean) > 12 and sentence_clean[-1] != '?' and sentence_clean[-1] != '!':
                        addtoindex(sentence_clean)

def to_disk():
    output = open('data.pkl', 'wb')
    pickle.dump([words_count, words_dct, first_word_cnt], output, 2)
    output.close()

def get_from_disk():
     input = open('data.pkl', 'rb')
     obj = pickle.load(input)
     input.close()
     return obj

def random_choice(sum_counts, counts):
    randnum = np.random.randint(0, sum_counts)
    sum_c = 0
    for word in list(counts):
        sum_c += counts[word]
        if sum_c >= randnum:
            return word

def new_sentence(first_word):
    try:
        randnum = np.random.randint(0, words_dct[first_word][0])
    except:
        first_word = 'the'
        randnum = np.random.randint(0, words_dct[first_word][0])
    sum_c = 0
    for word in words_dct[first_word][1].keys():
        sum_c += words_dct[first_word][1][word][0]
        if sum_c >= randnum:
            second_word = word
    if second_word == '.':
        text_words_count[0] += 1
        return ' ' + first_word.capitalize() + second_word
    sentence = ' ' + first_word.capitalize()
    f_word = first_word
    third_word = ''
    while third_word != '.' and len(sentence) < 70:
        sentence += ' ' + second_word
        try:
            text_words_count[0] += 1
            third_word = random_choice(words_dct[f_word][1][second_word][0], words_dct[f_word][1][second_word][1])
        except:
            third_word = '.'
        f_word = second_word
        second_word = third_word
    sentence += '.'
    return sentence

def generate(text_length):
    text=''
    first_word_count = sum(first_word_cnt.values())
    for num_par in range(text_length):
        num_sen = np.random.randint(5,15)
        for n_sen in range(num_sen):
            first_word = random_choice(first_word_count, first_word_cnt)
            sentence = new_sentence(first_word)
            text += sentence
        text+='\n   '
    return text

directory='corpus'
words_count = [0]
words_dct = {}
text_length = 500
reload(sys)
sys.setdefaultencoding('utf8')
first_word_cnt = collections.Counter();
index(directory)
to_disk()
words_count, words_dct, first_word_cnt = get_from_disk()
text_words_count = [0]
text = generate(text_length)
with open('random_text.txt','w') as fout:
    fout.write(text)
print text_words_count[0]
