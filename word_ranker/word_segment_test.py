# -*- coding:utf-8 -*-

import pickle
import sys

from word_segment import break_sentence

sys.path.append('../')
from text_generator.text_generator import TextGenerator

with open('local/words', 'rb') as word_file:
    word_weights = pickle.load(word_file)

# full_folder_path = '../data/test'
mini_folder_path = '../data/mini_train'

all_text = TextGenerator(folder=mini_folder_path)
generator = all_text.sentence_generator()

for sentence in generator:
    break_sentence(sentence, word_weights)

# break_sentence(u'误导性陈述或', word_weights)


