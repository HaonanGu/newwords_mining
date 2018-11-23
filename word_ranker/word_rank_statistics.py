# -*- coding:utf-8 -*-

class WordRankHelper:

    def __init__(self, word_ranker):
        self.word_ranker = word_ranker
       
    def get_total_ngram_num(self, with_one=True):
        ngrams_num = self.word_ranker.get_ngram_count()
        if with_one:
            return sum([count for count in ngrams_num.values()])
        else:
            return sum([count for count in ngrams_num.values()]) - ngrams_num[1]

    def get_total_border_num(self):
        all_borders = self.word_ranker.all_border
        border_sum = sum([len(word.left_neighbor) for word in all_borders.values()])
        
        return border_sum

    def ngram_statistics(self):
        all_ngrams = self.word_ranker.all_ngram
        max_freq = max(all_ngrams.values())
        
        freq_to_ngrams = dict()
        for freq in range(1, max_freq+1):
            freq_to_ngrams[freq] = list()
        for ngram in all_ngrams:
            freq_to_ngrams[all_ngrams[ngram]].append(ngram)

        for freq in freq_to_ngrams:
            print("频数 {0}， #ngram {1}".format(freq, len(freq_to_ngrams[freq])))
            
        return freq_to_ngrams

    def border_statistics(self):
        all_borders = self.word_ranker.all_border

        left_border_dict = dict()
        right_border_dict = dict()
        max_length = max([max(len(word.left_neighbor), len(word.right_neighbor)) for word in all_borders.values()])
        
        for border_num in range(max_length+1):
            left_border_dict[border_num] = list()
            right_border_dict[border_num] = list()
        
        for word in all_borders.values():
            left_border_dict[len(word.left_neighbor)].append(word.word)
            right_border_dict[len(word.right_neighbor)].append(word.word)

        print("Statistics of borders:")
        for border_num in range(max_length+1):
            left_ngram = len(left_border_dict[border_num])
            right_ngram = len(right_border_dict[border_num])
            print("边数 {0}, #ngram left {1}; #ngram right {2}".format(border_num, left_ngram, right_ngram))

        return left_border_dict, right_border_dict
