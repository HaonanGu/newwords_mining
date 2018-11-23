# -*- coding:utf-8 -*-

import time
import pickle

from word_ranker.word_rank import WordRank, Word
from word_ranker.word_rank_statistics import WordRankHelper
from pmi_spliter.pmi_spliter import PMISpliter
from text_generator.text_generator import TextGenerator


full_folder_path = './data/major_contracts_3000'
# mini_folder_path = './data/mini_train'

all_text = TextGenerator(folder=full_folder_path)

# step 1.1: 使用最小熵原理对数据进行预处理
start = time.time()

# 阈值太大会导致句子切的非常碎，反之，句子很少被切分; mini 取 -10， full 取 -15
pmi_threshold = -15  
print("preprocess data")
pmi_spliter = PMISpliter(all_text, pmi_threshold=pmi_threshold)
pmi_spliter.parse()  # 统计所有的 unigram 和 bigram
pmi_spliter.split()  # 根据 bigram 的内聚度对文本进行切割
end = time.time()
print("finish preprocess {0}".format(end-start))

# step 1.2: 初始化 WordRanker, 这里的 ngram 长度取2即可
start = time.time()

print("start parse data, use preprocessed boundaries")
word_ranker = WordRank(all_text.sentence_generator(), 5)
word_ranker.parse(just_parse=True)

# 是用预处理得到的 Word 和 相应的 boundaries 替换 WordRanker中相应的结构
word_ranker.all_border = pmi_spliter.words_map
end = time.time()
print("finish parse {0}".format(end-start))

# step 2: 计算每个ngam的左右边界值，类似PageRank
start = time.time()

print("compute left/right boundary values")
word_ranker.filter_ngram_by_self(lambda x: len(x)<2)     # 这一步是必须的，新词的长度必须大于等于2
word_ranker.filter_ngram_by_frequency(lambda x: x<5)
word_ranker.filter_ngram_by_inclusion()
word_ranker.compute_boundary_value(25)
end = time.time()
print("finish compute boundary values, time consuming {0}".format(end-start))

# step 3: 计算每个ngram的内聚值
start = time.time()

print("compute interior values")
word_ranker.compute_interior_value(bigram=True)
end = time.time()
print("finish compute interior values, time consuming {0}".format(end-start))

# step 4.1: 计算每个ngram的WordRank
start = time.time()

print("compute word_rank")
word_ranker.compute_word_rank(lambda x: x)
end = time.time()
print("finish compute word_rank, time consuming {0}".format(end-start))

# step 4.2: 根据WordRank给所有ngram排序
start = time.time()

print("sort word by word_rank")
words_with_rank = word_ranker.sort_word()
end = time.time()
print("finish sort word, time consuming {0}".format(end-start))

# 保存当前的结果便于之后分词
word_file = open('combiner/words', 'wb')
pickle.dump(words_with_rank, word_file)

# 打印当前结果
with open('words_result', 'w') as res_file:
    for word in words_with_rank:
        res_file.write("{0} : {1}\n".format(word[0].encode('utf-8'), word[1]))



