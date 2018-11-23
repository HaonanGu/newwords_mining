# -*- coding:utf-8 -*-

import math
import numpy as np

# 使用类似 Viterbi 方法切分句子，使切分后的句子的可能性最大
def break_sentence(sentence, word_weights):

    word_weights = { word: weight for word, weight in word_weights}

    length = max([len(word) for word in word_weights])
    loc_weights = dict(zip(range(len(sentence)), [-float('inf')]*len(sentence)))
    loc_back = [-1] * len(sentence)

    default_weight = 0.333 * min(word_weights.values())
    
    # len_to_weight = map_weight_by_length(word_weights, length)

    for loc in range(len(sentence)):
        most_prob = -float('inf')
        most_back = -1
        for i in range(length):
            split_loc = loc - i
            if split_loc < 0:
                break
            
            # last_point = split_loc - 1
            curr_word = sentence[split_loc:loc+1]
        
            if split_loc-1 < 0:
                if curr_word in word_weights:
                    curr_prob = word_weights[curr_word]
                else:
                    # curr_prob = math.log(len_to_weight[len(curr_word)], 2)
                    curr_prob = default_weight
            else:
                if curr_word in word_weights:
                    curr_prob = loc_weights[split_loc-1] + word_weights[curr_word]
                else:
                    # curr_prob = loc_weights[last_point] + math.log(len_to_weight[len(curr_word)], 2)
                    curr_prob = loc_weights[split_loc-1] + default_weight

            if most_prob < curr_prob:
                most_prob = curr_prob
                most_back = split_loc
        
        loc_weights[loc] = most_prob
        loc_back[loc] = most_back

    # print("maximum probability of the sentence is {0}".format(loc_weights[len(sentence)-1]))
    
    # print(loc_weights)
    # print(loc_back)
    words = list()
    curr_loc = len(sentence) - 1
    while curr_loc > 0:
        last_loc = loc_back[curr_loc]
        words.append(sentence[last_loc:curr_loc+1])

        curr_loc = last_loc - 1

    words = [word.encode('utf-8') for word in words[::-1]]
    sentence_div = ' | '.join(words)
    print(sentence_div)

    return words

'''
def map_weight_by_length(weights, length):
    len_to_weight = dict()

    # default_weight = sum(weights.values()) / len(weights.values())
    default_weight = 1

    for cur_len in range(1, length+1):
        cur_list = [weights[word] for word in weights if len(word)==cur_len]
        if len(cur_list) !=0:
            cur_weight = 1.0 * sum(cur_list) / len(cur_list)
        else:
            cur_weight = default_weight
        len_to_weight[cur_len] = cur_weight

    return len_to_weight
'''
         