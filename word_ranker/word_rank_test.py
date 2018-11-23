# -*- coding:utf-8 -*-

import pickle
import sys
import time

sys.path.append('../')
from text_generator.text_generator import TextGenerator
from word_rank import WordRank

# full_folder_path = '../data/major_contracts_3000'
mini_folder_path = '../data/mini_train'

all_text = TextGenerator(folder=mini_folder_path)
generator = all_text.sentence_generator()

word_ranker = WordRank(generator, 10)

# step 1: 处理原始数据，得到所有的ngram和它左右相邻的word
start = time.time()

print("start parse dataset ../data/mini_train")
word_ranker.parse()
# word_ranker.filter_ngram_by_frequency(lambda x: x<2)
# word_ranker.filter_ngram_by_degree(lambda x, y: x<2 and y<2)
# word_ranker.filter_ngram_by_inclusion()
end = time.time()
print("finish parse, time consuming {0}".format(end-start))

# step 2: 计算每个ngam的左右边界值，类似PageRank
start = time.time()

print("compute left/right boundary values")
word_ranker.compute_boundary_value(20)
end = time.time()
print("finish compute boundary values, time consuming {0}".format(end-start))

# step 3: 计算每个ngram的内聚值
start = time.time()

print("compute interior values")
word_ranker.compute_interior_value(bigram=False)
end = time.time()
print("finish compute interior values, time consuming {0}".format(end-start))

# step 4.1: 计算每个ngram的WordRank
start = time.time()

print("compute word_rank")
word_ranker.compute_word_rank(lambda x: x*2)
end = time.time()
print("finish compute word_rank, time consuming {0}".format(end-start))

# step 4.2: 根据WordRank给所有ngram排序
start = time.time()

print("sort word by word_rank")
words_with_rank = word_ranker.sort_word()
end = time.time()
print("finish sort word, time consuming {0}".format(end-start))

# 保存当前的结果便于之后分词
with open('local/words', 'wb') as word_file:
    pickle.dump(words_with_rank, word_file)

# 打印当前结果
with open('words_result', 'w') as res_file:
    for word in words_with_rank:
        res_file.write("{0} : {1}\n".format(word[0].encode('utf-8'), word[1]))
