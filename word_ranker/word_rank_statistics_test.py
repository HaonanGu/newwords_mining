# -*- coding:utf-8 -*-

from word_rank import WordRank
from text_generator import TextGenerator
from word_rank_statistics import WordRankHelper

# full_folder_path = '../data/major_contracts_3000'

mini_folder_path = '../data/mini_train'

all_text = TextGenerator(folder=mini_folder_path)
generator = all_text.sentence_generator()

word_ranker = WordRank(generator, 5)
word_ranker.parse()

helper = WordRankHelper(word_ranker)

print("Before frequency filter")
print("Total number of ngrams {0}".format(helper.get_total_ngram_num()))
print("Total number of border {0}".format(helper.get_total_border_num()))

word_ranker.filter_ngram_by_frequency(lambda x: x<2)

print("After frequency filter")
print("Total number of ngrams {0}".format(helper.get_total_ngram_num()))
print("Total number of border {0}".format(helper.get_total_border_num()))

word_ranker.filter_ngram_by_degree(lambda x, y: x<2 and y<2)

print("After degree filter")
print("Total number of ngrams {0}".format(helper.get_total_ngram_num()))
print("Total number of border {0}".format(helper.get_total_border_num()))

word_ranker.filter_ngram_by_inclusion()

print("After inclusion filter")
print("Total number of ngrams {0}".format(helper.get_total_ngram_num()))
print("Total number of border {0}".format(helper.get_total_border_num()))

# helper.ngram_statistics()
# helper.border_statistics()