# -*- coding:utf-8 -*-

import sys
import time

from pmi_spliter import PMISpliter

sys.path.append('../')
from text_generator.text_generator import TextGenerator

# full_folder_path = '../data/major_contracts_3000'
mini_folder_path = '../data/mini_train'

all_text = TextGenerator(folder=mini_folder_path)
pmi_spliter = PMISpliter(all_text)

# step 1: 处理原始数据，得到所有的分割点
start = time.time()

print("start parse dataset ../data/mini_train")
pmi_spliter.parse()
end = time.time()
print("Number of character {0}".format(len(pmi_spliter.char_map)))
print("Number of pair {0}".format(len(pmi_spliter.pair_map)))
print("finish parse, time consuming {0}".format(end-start))

# step 2: 计算每个ngam的左右相邻的ngram
start = time.time()

print("compute left/right boundary values")
pmi_spliter.split()
end = time.time()
total_boundary = 0
for word in pmi_spliter.words_map:
    total_boundary += len(pmi_spliter.words_map[word]['left'])

print("Total number of boundaries {0}".format(total_boundary))
print("finish compute boundary values, time consuming {0}".format(end-start))
