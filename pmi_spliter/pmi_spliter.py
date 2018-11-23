# -*- coding:utf-8 -*-

import math
import sys

from nltk.util import ngrams as ngrams_tool

sys.path.append('../')
from word_ranker.word_rank import Word

class PMISpliter:

    def __init__(self, text_generator, pmi_threshold=1):
        self.generator = text_generator
        self.pmi_threshold = pmi_threshold
        self.char_map = dict()              # 保存所有 unigram 及其频数
        self.pair_map = dict()              # 保存所有 bigram 及其频数
        self.words_map = dict()             # 切分后的词及其相邻的词
        
    def parse(self):
        sentences = self.generator.sentence_generator()
        for sent in sentences:
            for index, char in enumerate(sent):
                self.char_map[char] = self.char_map.get(char, 0) + 1
                if index < len(sent)-1:
                    self.pair_map[sent[index:index+2]] = self.pair_map.get(sent[index:index+2], 0) + 1
    
    def split(self, filter=False):
        sentences = self.generator.sentence_generator()
        for sent in sentences:
            ngrams = list()
            cur_start = 0
            for index in range(len(sent)):
                if index < len(sent)-1:
                    log_pair = math.log(self.pair_map[sent[index:index+2]], 2)
                    log_l_char = math.log(self.char_map[sent[index]], 2)
                    log_r_char = math.log(self.char_map[sent[index+1]], 2)
                    if log_pair-log_l_char-log_r_char < self.pmi_threshold:
                        ngrams.append(sent[cur_start:index+1])   # 如果内聚度小于阈值，从当前位置切分
                        cur_start = index + 1
                    print("{0}: 内聚度 {1}".format(sent[index:index+2].encode('utf-8'), log_pair-log_l_char-log_r_char))
            ngrams.append(sent[cur_start:])

            if filter:
                ngrams = self.__filter_combine_alnum(ngrams)     # 把连续的数字或字母放在同一个词中

            self.__create_words_with_boundary(ngrams)  # 根据切分后的句子，记录每个词的相邻词

    def __create_words_with_boundary(self, ngrams_in_sent):
        for loc, ngram in enumerate(ngrams_in_sent):
            if not ngram in self.words_map:
                self.words_map[ngram] = Word(ngram)
            cur_map = self.words_map[ngram]
            if loc + 1 < len(ngrams_in_sent):
                cur_map.add_right_neighbor(ngrams_in_sent[loc+1])
            if loc - 1 >= 0:
                cur_map.add_left_neighbor(ngrams_in_sent[loc-1])

    '''
    def __create_boundaries(self, ngrams_in_sent, cur_ngrams, indexes):
        length = len(ngrams_in_sent) - len(cur_ngrams) + 1
        for i in range(len(indexes)):
            if not cur_ngrams[i] in self.words_map:
                self.words_map[cur_ngrams[i]] = {'left':set(), 'right':set()}
            cur_map = self.words_map[cur_ngrams[i]]

            for win in range(1, self.hyper_ngram+1):
                if i - win >=0:
                    l_neighbor = "".join(ngrams_in_sent[i-win:i])
                    cur_map['left'].add(l_neighbor)
                if i + length + win <= len(ngrams_in_sent):
                    r_neighbor = "".join(ngrams_in_sent[i+length:i+length+win])
                    cur_map['right'].add(r_neighbor)
    '''
               
    def __filter_combine_alnum(self, ngrams):
        for index in range(len(ngrams)):
            if index < len(ngrams) - 1:
                cur_ngram = ngrams[index]
                next_ngram = ngrams[index+1]     
                while len(cur_ngram)!=0 and not self.__is_chinese(cur_ngram[-1]) and not self.__is_chinese(next_ngram[0]):
                    next_ngram = cur_ngram[-1] + next_ngram
                    cur_ngram = cur_ngram[0:-1]
                
                ngrams[index] = cur_ngram
                ngrams[index+1] = next_ngram
        
        ngrams = [ngram for ngram in ngrams if len(ngram)!=0]
        return ngrams

    def __is_chinese(self, uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fff':
            return True
        else:
            return False            
