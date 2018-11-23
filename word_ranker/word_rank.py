# -*- coding:utf-8 -*-

from nltk.util import ngrams
import math

class Word:

    def __init__(self, word):
        self.word = word
        self.left_value = 1
        self.right_value = 1
        self.interior_value = None
        self.left_neighbor = set()
        self.right_neighbor = set()
        self.word_rank = 0

    def add_left_neighbor(self, left_word):
        self.left_neighbor.add(left_word)
    
    def add_right_neighbor(self, right_word):
        self.right_neighbor.add(right_word)


class WordRank:

    def __init__(self, generator, ngram=3):
        self.generator = generator
        self.ngram = ngram

        self.all_ngram = dict()
        self.all_border = dict()
        self.ngram_map = dict()
    
    # step 1: 处理原始数据，得到所有的ngram和它左右相邻的word
    def parse(self, just_parse=False):
       
        # 获得所有的ngram及其统计信息，使用nltk
        for sentence in self.generator:
            
            # print("handle sentence "+sentence)
            ngrams_in_sent = list()
            ngrams_loc = list()
            for i in range(self.ngram):
                cur_grams = ngrams(sentence, i+1)
                cur_grams = ["".join(gram) for gram in cur_grams]
                if i != 0:
                    ngrams_in_sent.extend(cur_grams)
                    ngrams_loc.extend(range(0, len(sentence)-i))
                for gram in cur_grams:
                    self.all_ngram[gram] = self.all_ngram.get(gram, 0) + 1
            '''
            for gram in ngrams_in_sent:
                self.all_ngram[gram] = self.all_ngram.get(gram, 0) + 1
            '''

            # 获取当前句子中的ngram的左右边界
            # print("update neighbor ngrams")
            if not just_parse:
                self.__get_boundaries(sentence, ngrams_in_sent, ngrams_loc)

        
        print("Statistica before filter: ")
        for i in range(self.ngram):
            self.ngram_map[i+1] = [gram for gram in self.all_ngram if len(gram)==(i+1)]
            print("#(gram_{0}): {1}".format(i+1, len(self.ngram_map[i+1])))
        

    # step 2: 计算每个ngam的左右边界值，类似PageRank
    def compute_boundary_value(self, iteration=200):
        
        for i in range(iteration):
            left_total = right_total = 0
            
            # 更新左边界值
            for cur_ngram in self.all_border:
                cur_word = self.all_border[cur_ngram]
                
                new_left_value = 1
                for left_ngram in cur_word.left_neighbor:
                    new_left_value += self.all_border[left_ngram].right_value
                    # cur_left_neighbor = self.all_border[left_ngram]
                    # new_left_value += 1.0 * cur_left_neighbor.right_value / len(cur_left_neighbor.right_neighbor)
                
                cur_word.left_value = new_left_value

                left_total += new_left_value**2
                # left_total += new_left_value
            
            
            for cur_ngram in self.all_border:
                cur_word = self.all_border[cur_ngram]
                cur_word.left_value = 1.0 * cur_word.left_value / (left_total**0.5) * len(self.all_border)
                # cur_word.left_value = 1.0 * cur_word.left_value / left_total * len(self.all_border)
             
            # 更新右边界值
            for cur_ngram in self.all_border:
                cur_word = self.all_border[cur_ngram]
                
                new_right_value = 1
                for right_ngram in cur_word.right_neighbor:
                    new_right_value += self.all_border[right_ngram].left_value
                    # cur_right_neighbor = self.all_border[right_ngram]
                    # new_right_value += 1.0 * cur_right_neighbor.left_value / len(cur_right_neighbor.left_neighbor)
                
                cur_word.right_value = new_right_value

                right_total += new_right_value**2
                # right_total += new_right_value
   
            for cur_ngram in self.all_border:
                cur_word = self.all_border[cur_ngram]
                cur_word.right_value = 1.0 * cur_word.right_value / (right_total**0.5) * len(self.all_border)
                # cur_word.right_value = 1.0 * cur_word.right_value / right_total * len(self.all_border)

    # step 3: 计算每个ngram的内聚值，bigram 表示是否根据相邻两个字的互信息决定内聚度
    def compute_interior_value(self, bigram=False):
        
        ngram_count = self.get_ngram_count()

        for cur_ngram in self.all_border:
        
            if len(cur_ngram) <= 1:
                self.all_border[cur_ngram].interior_value = 1
                continue

            split = 1
            min_interior_value = None
            while split < len(cur_ngram):
                
                if bigram:
                    prob_cur = 1.0 * self.all_ngram[cur_ngram[split-1:split+1]] / ngram_count[2]
                    prob_left = 1.0 * self.all_ngram[cur_ngram[split-1]] / ngram_count[1]
                    prob_right = 1.0 * self.all_ngram[cur_ngram[split]] / ngram_count[1]
                    cur_interior_value = math.log(prob_cur / (prob_left * prob_right), 2)
                else:
                    prob_cur = 1.0 * self.all_ngram[cur_ngram] / ngram_count[len(cur_ngram)]
                    prob_left = 1.0 * self.all_ngram[cur_ngram[0:split]] / ngram_count[split]
                    prob_right = 1.0 * self.all_ngram[cur_ngram[split:]] / ngram_count[len(cur_ngram)-split]
                    cur_interior_value = math.log(prob_cur / (prob_left * prob_right), 2)
               
                if cur_interior_value < min_interior_value or min_interior_value == None:
                    min_interior_value = cur_interior_value

                split += 1 
            
            '''
            if min_interior_value == None:
                min_interior_value = 1
            '''
            self.all_border[cur_ngram].interior_value = min_interior_value
    
    # step 4.1: 计算每个ngram的WordRank
    def compute_word_rank(self, func):
        for cur_ngram in self.all_border:
            cur_word = self.all_border[cur_ngram]
            # cur_word.word_rank = cur_word.left_value * cur_word.right_value * func(cur_word.interior_value)
            
            l_value = cur_word.left_value
            r_value = cur_word.right_value

            # print("left {0}, right {1}, interior {2}, word {3}".format(l_value, r_value, func(cur_word.interior_value), cur_ngram.encode('utf-8')))
            cur_word.word_rank = (l_value*r_value)/(l_value+r_value)*func(cur_word.interior_value)

    # step 4.2: 根据WordRank给所有ngram排序
    def sort_word(self, order=True):
        all_words = self.all_border.values()
        all_words = sorted(all_words, cmp=lambda x,y:cmp(x.word_rank,y.word_rank), reverse=order)

        words_with_rank = [(word.word, word.word_rank) for word in all_words]

        return words_with_rank
    
    # 根据 ngram 本身来过滤掉不满足条件的 ngram
    def filter_ngram_by_self(self, func):
        ngram_filter = [ngram for ngram in self.all_ngram if func(ngram)]
        self.__filter_ngram_in_graph(ngram_filter)

    # 根据 ngram 的频率过滤掉不满足条件的 ngram
    def filter_ngram_by_frequency(self, func):
        ngram_filter = [ngram for ngram in self.all_ngram if func(self.all_ngram[ngram])]
        self.__filter_ngram_in_graph(ngram_filter)

    # 根据 ngram 的左右相邻的 ngram 数量过滤掉不满足条件的 ngram
    def filter_ngram_by_degree(self, func):
        ngram_filter = [ngram for ngram in self.all_border \
                        if func(len(self.all_border[ngram].left_neighbor), len(self.all_border[ngram].right_neighbor))]
        self.__filter_ngram_in_graph(ngram_filter)

    # 如果同频词是包含关系，那么过滤掉其中较短的ngram
    def filter_ngram_by_inclusion(self):
        sorted_ngram = sorted(self.all_ngram, cmp=lambda x,y: cmp(self.all_ngram[x], self.all_ngram[y]))
        ngram_filter = set()
        
        start = 0
        point = start + 1
        while start < len(sorted_ngram)-1:
            while point < len(sorted_ngram):
                if self.all_ngram[sorted_ngram[start]] != self.all_ngram[sorted_ngram[point]]:
                    start = point
                    point = start + 1
                    break

                if sorted_ngram[start] in sorted_ngram[point]:
                    ngram_filter.add(sorted_ngram[start])
                    start += 1
                    point = start + 1
                    break
                elif sorted_ngram[point] in sorted_ngram[start]:
                    ngram_filter.add(sorted_ngram[point])
                
                point += 1
                
        self.__filter_ngram_in_graph(ngram_filter)

    def get_ngram_count(self):
        total_ngram_count = dict()
        for i in range(1, self.ngram+1):
            total_ngram_count[i] = len([ngram for ngram in self.all_ngram if len(ngram)==i])

        return total_ngram_count

    def __filter_ngram_in_graph(self, ngram_filter):
        for ngram in ngram_filter:
            if not ngram in self.all_border:
                continue
            
            cur_word = self.all_border[ngram]
            for left_ngram in cur_word.left_neighbor:
                self.all_border[left_ngram].right_neighbor.remove(ngram)
            for right_ngram in cur_word.right_neighbor:
                self.all_border[right_ngram].left_neighbor.remove(ngram)

        for ngram in ngram_filter:
            if ngram in self.all_border:
                del self.all_border[ngram]

    def __get_boundaries(self, sentence, ngrams_in_sent, ngrams_loc):
        index = 0
        while index < len(ngrams_in_sent):
            cur_ngram = ngrams_in_sent[index]
            cur_loc = ngrams_loc[index]

            if not cur_ngram in self.all_border:
                self.all_border[cur_ngram] = Word(cur_ngram)
            
            cur_word = self.all_border[cur_ngram]

            # 获取左右边界
            for i in range(2, self.ngram+1):
                if cur_loc - i >=0:
                    cur_word.add_left_neighbor(sentence[cur_loc-i:cur_loc])
                if cur_loc + len(cur_ngram) + i <= len(sentence):
                    cur_word.add_right_neighbor(sentence[cur_loc+len(cur_ngram):cur_loc + len(cur_ngram) + i])
            
            index += 1

        